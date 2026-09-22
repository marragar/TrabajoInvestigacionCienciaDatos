import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pymongo import MongoClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from db_config import MONGO_URI, DB_NAME

# ── CONEXIÓN ────────────────────────────────────────────────────────────────
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
col = db["solicitudes"]

df = pd.DataFrame(list(col.find({}, {"_id": 0})))
df["Cantidad Total"] = pd.to_numeric(df["Cantidad Total"], errors="coerce")

# ── TOP 4 CENTROS + OTROS ────────────────────────────────────────────────────
top4 = df["Centro de Investigación"].value_counts().nlargest(4).index.tolist()
df["Centro Agrupado"] = df["Centro de Investigación"].apply(
    lambda x: x if x in top4 else "Otros"
)

# ── 1. Nº DE SOLICITUDES POR CENTRO ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
conteo = df["Centro Agrupado"].value_counts()
conteo.plot(kind="bar", ax=ax, color="steelblue")
ax.set_title("Nº de solicitudes por centro de investigación")
ax.set_xlabel("")
ax.set_ylabel("Solicitudes")
ax.tick_params(axis="x", rotation=45)
plt.tight_layout()
plt.savefig("solicitudes_por_centro.png", dpi=150)
plt.close()

# ── 2. DINERO TOTAL DESTINADO POR CENTRO ────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
dinero = df.groupby("Centro Agrupado")["Cantidad Total"].sum().sort_values(ascending=False)
dinero.plot(kind="bar", ax=ax, color="seagreen")
ax.set_title("Cantidad total destinada por centro de investigación (€)")
ax.set_xlabel("")
ax.set_ylabel("€")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.tick_params(axis="x", rotation=45)
plt.tight_layout()
plt.savefig("dinero_por_centro.png", dpi=150)
plt.close()

# ── 3. SOLICITUDES POR CENTRO Y ESTADO ──────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
pivot = df.groupby(["Centro Agrupado", "Estado Solicitud"]).size().unstack(fill_value=0)
pivot.plot(kind="bar", ax=ax)
ax.set_title("Solicitudes por centro y estado")
ax.set_xlabel("")
ax.set_ylabel("Solicitudes")
ax.tick_params(axis="x", rotation=45)
ax.legend(title="Estado")
plt.tight_layout()
plt.savefig("solicitudes_centro_estado.png", dpi=150)
plt.close()

# ── 4. NOTA MEDIA POR CENTRO ─────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
nota_media = df.groupby("Centro Agrupado")["Nota"].mean().sort_values(ascending=False)
nota_media.plot(kind="bar", ax=ax, color="coral")
ax.set_title("Nota media por centro de investigación")
ax.set_xlabel("")
ax.set_ylabel("Nota media")
ax.set_ylim(0, 10)
ax.tick_params(axis="x", rotation=45)
plt.tight_layout()
plt.savefig("nota_media_por_centro.png", dpi=150)
plt.close()

print("Gráficas guardadas.")