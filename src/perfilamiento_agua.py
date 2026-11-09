"""Caso: perfilamiento de la calidad del agua (3.276 muestras, 9 variables)."""
import numpy as np
import pandas as pd
import polars as pl

RUTA = "data/calidad_agua.csv"
LIMITES = {"pH": (6.5, 8.5), "Cloraminas": (0, 4), "Trihalometanos": (0, 80),
           "Turbidez": (0, 5)}          # referencias del diccionario de datos

# 1. Carga y dimensión -------------------------------------------------------
df = pd.read_csv(RUTA)
print("Dimensión:", df.shape)
print(df.dtypes.value_counts().to_string())

# 2. Calidad: nulos y duplicados ----------------------------------------------
nulos = (df.isna().mean() * 100).round(1)
print("\nNulos (%):\n" + nulos[nulos > 0].to_string())
print("Filas duplicadas:", int(df.duplicated().sum()))

# 3. Estadísticos descriptivos y balance de clases ---------------------------
print("\n" + df.describe().T[["count", "mean", "std", "min", "max"]].round(2).to_string())
print("\nBalance de clases:\n" + df["Potabilidad"].value_counts(normalize=True).round(3).to_string())

# 4. Rangos de referencia con máscaras de NumPy -------------------------------
print("\nValores fuera del rango de referencia:")
for col, (lo, hi) in LIMITES.items():
    v = df[col].to_numpy()
    fuera = int(((v < lo) | (v > hi)).sum())      # NaN compara False
    print(f"  {col:<15} {fuera:>5} de {int((~np.isnan(v)).sum())} medidos")

# 5. Atípicos por puntaje z (Dureza) ------------------------------------------
x = df["Dureza"].to_numpy()
z = (x - np.nanmean(x)) / np.nanstd(x)
print("\nAtípicos en Dureza (|z| > 3):", int((np.abs(z) > 3).sum()))

# 6. Perfil por clase con Pandas ----------------------------------------------
print("\nMedias por clase:\n" + df.groupby("Potabilidad")[["pH", "Dureza", "Sólidos", "Turbidez"]].mean().round(2).to_string())

# 7. La misma consulta con Polars en modo diferido ----------------------------
consulta = (pl.read_csv(RUTA).lazy()
            .filter(pl.col("Sólidos") > 20000)
            .group_by("Potabilidad")
            .agg(pl.col("pH").mean().round(2).alias("pH_medio"),
                 pl.len().alias("n_filas"))
            .sort("Potabilidad"))
print("\n", consulta.collect(), sep="")
