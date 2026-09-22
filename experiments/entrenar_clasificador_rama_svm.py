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
MODELO_EMB  = "intfloat/multilingual-e5-large"
COL_SALIDA  = "solicitudesSVM"
# ─────────────────────────────────────────────────────────────────────────────

client = MongoClient(MONGO_URI)
db     = client[DB_NAME]

# ── 1. CARGAR SOLICITUDESG Y SOLICITUDESM ────────────────────────────────────
campos_rama = {"_id": 0, "Referencia": 1, "Descripción": 1, "Rama": 1}

df_g = pd.DataFrame(list(db["solicitudesG"].find({"Rama": {"$nin": ["", None]}}, campos_rama)))
df_m = pd.DataFrame(list(db["solicitudesM"].find({"Rama": {"$nin": ["", None]}}, campos_rama)))

print(f"solicitudesG: {len(df_g)} | solicitudesM: {len(df_m)}")

# ── 2. CRUZAR: CON REFERENCIA POR REFERENCIA, SIN REFERENCIA POR DESCRIPCIÓN ─
def cruzar(df_g, df_m, key):
    g = df_g[df_g[key].notna() & (df_g[key] != "")].drop_duplicates(subset=key)
    m = df_m[df_m[key].notna() & (df_m[key] != "")].drop_duplicates(subset=key)
    merged = g.merge(m, on=key, suffixes=("_g", "_m"))
    coinciden = merged[merged["Rama_g"] == merged["Rama_m"]].copy()
    coinciden["Rama"] = coinciden["Rama_g"]
    return coinciden[[key, "Rama"]]

coin_ref  = cruzar(df_g, df_m, "Referencia")
coin_desc = cruzar(df_g, df_m, "Descripción")

print(f"Coincidentes por Referencia: {len(coin_ref)}")
print(f"Coincidentes por Descripción (suplentes): {len(coin_desc)}")

# ── 3. CARGAR SOLICITUDESCOPIA ────────────────────────────────────────────────
campos_base = {"_id": 0, "Referencia": 1, "Solicitante": 1, "Género Solicitante": 1,
               "Descripción": 1, "Estado Solicitud": 1, "Centro de Investigación": 1,
               "CIF": 1, "DNI": 1, "Nº Petición": 1, "Nota": 1, "Cantidad Total": 1,
               "Personal Contratado": 1, "Nº Contratos": 1,
               "Año Inicio": 1, "Año1": 1, "Año2": 1, "Año3": 1, "Año4": 1, "Año5": 1}

df_copia = pd.DataFrame(list(db["solicitudesCopia"].find({}, campos_base)))
print(f"solicitudesCopia raw: {len(df_copia)}")

# ── 4. SEPARAR TRAIN Y PRED ───────────────────────────────────────────────────
# Con referencia
df_con_ref  = df_copia[df_copia["Referencia"].notna() & (df_copia["Referencia"] != "")].drop_duplicates(subset="Referencia")
# Sin referencia (suplentes)
df_sin_ref  = df_copia[df_copia["Referencia"].isna() | (df_copia["Referencia"] == "")].drop_duplicates(subset="Descripción")

print(f"Con referencia: {len(df_con_ref)} | Sin referencia: {len(df_sin_ref)}")

# Train con referencia
train_ref = df_con_ref[df_con_ref["Referencia"].isin(coin_ref["Referencia"])].copy()
train_ref = train_ref.merge(coin_ref, on="Referencia")

# Train sin referencia
train_desc = df_sin_ref[df_sin_ref["Descripción"].isin(coin_desc["Descripción"])].copy()
train_desc = train_desc.merge(coin_desc, on="Descripción")

df_train = pd.concat([train_ref, train_desc], ignore_index=True)

# Pred con referencia
pred_ref  = df_con_ref[~df_con_ref["Referencia"].isin(coin_ref["Referencia"])].copy()
# Pred sin referencia
pred_desc = df_sin_ref[~df_sin_ref["Descripción"].isin(coin_desc["Descripción"])].copy()

df_pred = pd.concat([pred_ref, pred_desc], ignore_index=True)

print(f"Train: {len(df_train)} | A clasificar: {len(df_pred)}")

# ── 5. EMBEDDINGS ─────────────────────────────────────────────────────────────
print(f"\nCargando modelo de embeddings: {MODELO_EMB}...")
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

# ── 6. ENTRENAR SVM ───────────────────────────────────────────────────────────
le = LabelEncoder()
y_train = le.fit_transform(df_train["Rama"])

print("\nEntrenando SVM...")
svm = SVC(kernel="rbf", C=10, gamma="scale", probability=True)
svm.fit(X_train, y_train)

y_pred_train = svm.predict(X_train)
print("\nRendimiento sobre datos de entrenamiento:")
print(classification_report(y_train, y_pred_train, target_names=le.classes_))

# ── 7. PREDECIR ───────────────────────────────────────────────────────────────
print("Clasificando documentos sin rama...")
y_pred  = svm.predict(X_pred)
y_proba = svm.predict_proba(X_pred).max(axis=1)

df_pred = df_pred.copy()
df_pred["Rama"]      = le.inverse_transform(y_pred)
df_pred["Confianza"] = y_proba

print(f"\nDistribución de ramas predichas:")
print(df_pred["Rama"].value_counts().to_string())

# ── 8. GUARDAR EN MONGODB ─────────────────────────────────────────────────────
col_salida = db[COL_SALIDA]
col_salida.drop()

df_train["Confianza"] = 1.0
df_final = pd.concat([df_train, df_pred], ignore_index=True)

col_salida.insert_many(df_final.to_dict("records"))
print(f"\nGuardado en {COL_SALIDA}: {len(df_final)} documentos")