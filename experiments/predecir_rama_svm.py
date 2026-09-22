from pathlib import Path
import sys
import pandas as pd
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

# ── CONFIG ───────────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from db_config import MONGO_URI, DB_NAME
COL_SALIDA = "solicitudesSVM"
MODELO_EMB = "intfloat/multilingual-e5-large"
# ─────────────────────────────────────────────────────────────────────────────

client = MongoClient(MONGO_URI)
db     = client[DB_NAME]
col    = db[COL_SALIDA]

# ── CARGAR DATOS ──────────────────────────────────────────────────────────────
df = pd.DataFrame(list(col.find({}, {"_id": 1, "Descripción": 1, "Rama": 1})))
print(f"Total documentos: {len(df)}")

df_train = df[df["Rama"].notna() & (df["Rama"] != "")].copy()
df_pred  = df[df["Rama"].isna()  | (df["Rama"] == "")].copy()

print(f"Train: {len(df_train)} | A clasificar: {len(df_pred)}")
print(f"\nDistribución train por rama:")
print(df_train["Rama"].value_counts().to_string())

# ── EMBEDDINGS ────────────────────────────────────────────────────────────────
print(f"\nCargando modelo: {MODELO_EMB}...")
modelo_emb = SentenceTransformer(MODELO_EMB)

print("Generando embeddings de entrenamiento...")
X_train = modelo_emb.encode(
    ["passage: " + t for t in df_train["Descripción"].fillna("").tolist()],
    show_progress_bar=True
)

print("Generando embeddings de predicción...")
X_pred = modelo_emb.encode(
    ["passage: " + t for t in df_pred["Descripción"].fillna("").tolist()],
    show_progress_bar=True
)

# ── ENTRENAR SVM ──────────────────────────────────────────────────────────────
le = LabelEncoder()
y_train = le.fit_transform(df_train["Rama"])

print("\nEntrenando SVM...")
svm = SVC(kernel="rbf", C=10, gamma="scale", probability=True)
svm.fit(X_train, y_train)

y_pred_train = svm.predict(X_train)
print("\nRendimiento sobre datos de entrenamiento:")
print(classification_report(y_train, y_pred_train, target_names=le.classes_))

# ── PREDECIR Y ACTUALIZAR ─────────────────────────────────────────────────────
print("Clasificando documentos sin rama...")
y_pred  = svm.predict(X_pred)
y_proba = svm.predict_proba(X_pred).max(axis=1)

ramas_pred = le.inverse_transform(y_pred)

print(f"\nDistribución ramas predichas:")
print(pd.Series(ramas_pred).value_counts().to_string())

for i, (idx, row) in enumerate(df_pred.iterrows()):
    col.update_one(
        {"_id": row["_id"]},
        {"$set": {"Rama": ramas_pred[i], "Confianza SVM": float(y_proba[i])}}
    )

print(f"\nActualizados en MongoDB: {len(df_pred)} documentos")