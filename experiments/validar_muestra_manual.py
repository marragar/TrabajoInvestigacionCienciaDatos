import pandas as pd
import os

# ── CONFIG ───────────────────────────────────────────────────────────────────
INPUT_FILE = "muestra_validacion.csv"
# ─────────────────────────────────────────────────────────────────────────────

df = pd.read_csv(INPUT_FILE)

resultados = []

print("\n" + "═"*60)
print("  VALIDACIÓN DE CLASIFICACIÓN DE RAMAS")
print("  [v] = correcto  |  [f] = incorrecto  |  [q] = salir")
print("═"*60)

for i, row in df.iterrows():
    os.system("cls" if os.name == "nt" else "clear")
    print(f"\n  [{i+1}/{len(df)}]")
    print(f"\n  Solicitante : {row['Solicitante']}")
    print(f"  Género      : {row['Género']}")
    print(f"\n  Descripción :\n  {row['Descripción']}")
    print(f"\n  Rama predicha: {row['Rama']}")
    print("\n" + "─"*60)

    while True:
        resp = input("  ¿Correcto? [v/f/q]: ").strip().lower()
        if resp in ("v", "f", "q"):
            break
        print("  Introduce v, f o q")

    if resp == "q":
        print("\n  Validación interrumpida.")
        break

    resultados.append({
        "Solicitante": row["Solicitante"],
        "Género":      row["Género"],
        "Rama":        row["Rama"],
        "Correcto":    resp == "v",
    })

# ── RESULTADOS ────────────────────────────────────────────────────────────────
if resultados:
    df_res = pd.DataFrame(resultados)
    total      = len(df_res)
    correctos  = df_res["Correcto"].sum()
    incorrectos = total - correctos

    print("\n" + "═"*60)
    print("  RESULTADOS FINALES")
    print("═"*60)
    print(f"  Total validados : {total}")
    print(f"  Correctos       : {correctos} ({correctos/total:.0%})")
    print(f"  Incorrectos     : {incorrectos} ({incorrectos/total:.0%})")

    print("\n  Por género:")
    for genero, grupo in df_res.groupby("Género"):
        acc = grupo["Correcto"].mean()
        print(f"    {genero}: {acc:.0%} ({grupo['Correcto'].sum()}/{len(grupo)})")

    print("\n  Por rama:")
    for rama, grupo in df_res.groupby("Rama"):
        acc = grupo["Correcto"].mean()
        print(f"    {rama}: {acc:.0%} ({grupo['Correcto'].sum()}/{len(grupo)})")

    print("═"*60)