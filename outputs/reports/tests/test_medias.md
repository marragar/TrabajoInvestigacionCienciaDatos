# Comparación de medias — variables numéricas vs. categóricas

_Generado el 2026-07-15 22:18_

> Nota metodológica: se comparan las medias de las variables NUMÉRICAS (Nota, Nº Contratos) entre los grupos de cada variable CATEGÓRICA. Con 2 grupos se usa el **t de Student**; con 3 o más, **ANOVA** (que es su generalización). Ambos en variante de **Welch**, que no asume varianzas iguales — prudente aquí porque los grupos tienen tamaños muy dispares. El ANOVA es un test global (dice que hay diferencia, no dónde), así que cuando sale significativo se añaden comparaciones **dos a dos** con corrección por múltiples tests (método: bonferroni). Se reporta el tamaño del efecto (**d de Cohen** con 2 grupos, **η²** con 3+) porque el p-valor dice si la diferencia es real, no si es relevante.

## Nota

### Nota × Estado Solicitud

> ⚠ Si el procedimiento consiste en ordenar por nota y aceptar de arriba abajo, este test saldrá significativo POR CONSTRUCCIÓN: confirma el procedimiento, no es un hallazgo.

| Estado Solicitud | n | Media | Mediana | Desv. típica | Mín | Máx |
|---|---:|---:|---:|---:|---:|---:|
| Aceptada | 218 | 8.603 | 8.585 | 0.364 | 7.880 | 9.670 |
| Suplente | 687 | 7.177 | 7.430 | 0.989 | 1.600 | 8.440 |

**Homocedasticidad (Levene):** W = `89.6754`, p = `0.00000` — las varianzas NO son homogéneas entre grupos; por eso se usa la variante de Welch como referencia.

**t de Student**

- Welch (no asume varianzas iguales): t = `31.6242`, p = `0.00000`
- Clásico (asume varianzas iguales): t = `20.8344`, p = `0.00000`
- Diferencia de medias (Aceptada − Suplente) = `+1.426`
- **Conclusión (Welch):** Hay diferencia significativa de Nota entre Aceptada y Suplente (α = 0.05)

**Tamaño del efecto**

- d de Cohen = `+1.620` (grande)

### Nota × Género

| Género | n | Media | Mediana | Desv. típica | Mín | Máx |
|---|---:|---:|---:|---:|---:|---:|
| Masculino | 564 | 7.583 | 7.805 | 1.068 | 1.600 | 9.670 |
| Femenino | 341 | 7.417 | 7.630 | 1.070 | 3.070 | 9.550 |

**Homocedasticidad (Levene):** W = `0.0987`, p = `0.75347` — las varianzas son homogéneas entre grupos.

**t de Student**

- Welch (no asume varianzas iguales): t = `2.2613`, p = `0.02404`
- Clásico (asume varianzas iguales): t = `2.2625`, p = `0.02391`
- Diferencia de medias (Masculino − Femenino) = `+0.166`
- **Conclusión (Welch):** Hay diferencia significativa de Nota entre Masculino y Femenino (α = 0.05)

**Tamaño del efecto**

- d de Cohen = `+0.155` (despreciable)

### Nota × Centro

| Centro | n | Media | Mediana | Desv. típica | Mín | Máx |
|---|---:|---:|---:|---:|---:|---:|
| Universidad de Valladolid | 312 | 7.461 | 7.655 | 1.058 | 1.600 | 9.450 |
| Universidad de Salamanca | 256 | 7.612 | 7.905 | 1.070 | 3.250 | 9.550 |
| Universidad de León | 151 | 7.260 | 7.440 | 1.120 | 3.480 | 9.100 |
| Universidad de Burgos | 107 | 7.649 | 7.750 | 1.069 | 4.350 | 9.540 |
| CSIC | 48 | 8.051 | 8.210 | 0.794 | 5.700 | 9.670 |

**Homocedasticidad (Levene):** W = `1.5670`, p = `0.18105` — las varianzas son homogéneas entre grupos.

**ANOVA** (tabla de 5 grupos)

- Clásico: F = `6.3940`, p = `0.00005`
- Welch: F = `8.2489`, gl = `4, 243.22`, p = `0.00000`
- **Conclusión (Welch):** Hay diferencia significativa de Nota entre los 5 grupos de Centro (α = 0.05)

**Tamaño del efecto**

- η² = `0.0286` (pequeño) — el grupo explica el 2.9% de la variabilidad de Nota

**Post-hoc — comparaciones dos a dos** (t de Welch, corrección: Bonferroni (FWER))

| Par | Dif. de medias | p crudo | p ajustado | d de Cohen | Significativo |
|---|---:|---:|---:|---:|:---:|
| Universidad de Valladolid vs. Universidad de Salamanca | -0.151 | 0.09228 | 0.92282 | -0.142 | no |
| Universidad de Valladolid vs. Universidad de León | +0.201 | 0.06612 | 0.66116 | +0.187 | no |
| Universidad de Valladolid vs. Universidad de Burgos | -0.188 | 0.11743 | 1.00000 | -0.177 | no |
| Universidad de Valladolid vs. CSIC | -0.591 | 0.00002 | 0.00019 | -0.575 | ✅ sí |
| Universidad de Salamanca vs. Universidad de León | +0.352 | 0.00199 | 0.01987 | +0.324 | ✅ sí |
| Universidad de Salamanca vs. Universidad de Burgos | -0.036 | 0.76721 | 1.00000 | -0.034 | no |
| Universidad de Salamanca vs. CSIC | -0.439 | 0.00139 | 0.01388 | -0.426 | ✅ sí |
| Universidad de León vs. Universidad de Burgos | -0.389 | 0.00515 | 0.05151 | -0.354 | no |
| Universidad de León vs. CSIC | -0.792 | 0.00000 | 0.00000 | -0.753 | ✅ sí |
| Universidad de Burgos vs. CSIC | -0.403 | 0.01022 | 0.10224 | -0.406 | no |

> 10 comparaciones dos a dos; el p-valor ajustado es el que se compara contra α = 0.05.

### Nota × Rama

| Rama | n | Media | Mediana | Desv. típica | Mín | Máx |
|---|---:|---:|---:|---:|---:|---:|
| Ciencias - Ciencias de la Salud | 261 | 7.532 | 7.700 | 1.063 | 1.600 | 9.670 |
| Ciencias - Resto | 200 | 7.696 | 7.905 | 1.004 | 3.070 | 9.300 |
| Ingenierías | 178 | 7.278 | 7.495 | 1.134 | 3.250 | 9.460 |
| Ciencias Sociales - Resto | 79 | 7.310 | 7.470 | 1.221 | 3.660 | 9.540 |
| Filosofía y Letras | 54 | 7.729 | 7.905 | 0.957 | 4.710 | 9.550 |
| Ciencias - Matemáticas y Física | 93 | 7.905 | 8.030 | 0.761 | 5.400 | 9.400 |
| Ciencias Sociales - Educación | 40 | 6.885 | 7.015 | 1.068 | 4.350 | 8.430 |

**Homocedasticidad (Levene):** W = `2.9756`, p = `0.00698` — las varianzas NO son homogéneas entre grupos; por eso se usa la variante de Welch como referencia.

**ANOVA** (tabla de 7 grupos)

- Clásico: F = `7.9731`, p = `0.00000`
- Welch: F = `9.0171`, gl = `6, 236.34`, p = `0.00000`
- **Conclusión (Welch):** Hay diferencia significativa de Nota entre los 7 grupos de Rama (α = 0.05)

**Tamaño del efecto**

- η² = `0.0506` (pequeño) — el grupo explica el 5.1% de la variabilidad de Nota

**Post-hoc — comparaciones dos a dos** (t de Welch, corrección: Bonferroni (FWER))

| Par | Dif. de medias | p crudo | p ajustado | d de Cohen | Significativo |
|---|---:|---:|---:|---:|:---:|
| Ciencias - Ciencias de la Salud vs. Ciencias - Resto | -0.164 | 0.09080 | 1.00000 | -0.158 | no |
| Ciencias - Ciencias de la Salud vs. Ingenierías | +0.254 | 0.01852 | 0.38898 | +0.233 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias Sociales - Resto | +0.222 | 0.14836 | 1.00000 | +0.201 | no |
| Ciencias - Ciencias de la Salud vs. Filosofía y Letras | -0.197 | 0.18147 | 1.00000 | -0.188 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias - Matemáticas y Física | -0.373 | 0.00035 | 0.00730 | -0.376 | ✅ sí |
| Ciencias - Ciencias de la Salud vs. Ciencias Sociales - Educación | +0.647 | 0.00078 | 0.01636 | +0.609 | ✅ sí |
| Ciencias - Resto vs. Ingenierías | +0.418 | 0.00019 | 0.00390 | +0.392 | ✅ sí |
| Ciencias - Resto vs. Ciencias Sociales - Resto | +0.386 | 0.01398 | 0.29363 | +0.361 | no |
| Ciencias - Resto vs. Filosofía y Letras | -0.033 | 0.82670 | 1.00000 | -0.033 | no |
| Ciencias - Resto vs. Ciencias - Matemáticas y Física | -0.209 | 0.04997 | 1.00000 | -0.224 | no |
| Ciencias - Resto vs. Ciencias Sociales - Educación | +0.811 | 0.00005 | 0.00099 | +0.799 | ✅ sí |
| Ingenierías vs. Ciencias Sociales - Resto | -0.033 | 0.84060 | 1.00000 | -0.028 | no |
| Ingenierías vs. Filosofía y Letras | -0.451 | 0.00458 | 0.09615 | -0.411 | no |
| Ingenierías vs. Ciencias - Matemáticas y Física | -0.627 | 0.00000 | 0.00000 | -0.614 | ✅ sí |
| Ingenierías vs. Ciencias Sociales - Educación | +0.393 | 0.04189 | 0.87960 | +0.350 | no |
| Ciencias Sociales - Resto vs. Filosofía y Letras | -0.418 | 0.02892 | 0.60726 | -0.373 | no |
| Ciencias Sociales - Resto vs. Ciencias - Matemáticas y Física | -0.595 | 0.00026 | 0.00555 | -0.595 | ✅ sí |
| Ciencias Sociales - Resto vs. Ciencias Sociales - Educación | +0.426 | 0.05379 | 1.00000 | +0.363 | no |
| Filosofía y Letras vs. Ciencias - Matemáticas y Física | -0.177 | 0.24905 | 1.00000 | -0.211 | no |
| Filosofía y Letras vs. Ciencias Sociales - Educación | +0.844 | 0.00017 | 0.00347 | +0.839 | ✅ sí |
| Ciencias - Matemáticas y Física vs. Ciencias Sociales - Educación | +1.020 | 0.00000 | 0.00002 | +1.181 | ✅ sí |

> 21 comparaciones dos a dos; el p-valor ajustado es el que se compara contra α = 0.05.

## Nº Contratos

> Filtrado a solicitudes con Estado = **Aceptada** (n = 218): fuera de ahí esta variable está a 0 por definición, así que incluir el resto sería circular.

### Nº Contratos × Género

| Género | n | Media | Mediana | Desv. típica | Mín | Máx |
|---|---:|---:|---:|---:|---:|---:|
| Masculino | 155 | 1.077 | 1.000 | 0.576 | 0.000 | 2.000 |
| Femenino | 62 | 1.000 | 1.000 | 0.601 | 0.000 | 2.000 |

**Homocedasticidad (Levene):** W = `0.0732`, p = `0.78704` — las varianzas son homogéneas entre grupos.

**t de Student**

- Welch (no asume varianzas iguales): t = `0.8679`, p = `0.38735`
- Clásico (asume varianzas iguales): t = `0.8837`, p = `0.37782`
- Diferencia de medias (Masculino − Femenino) = `+0.077`
- **Conclusión (Welch):** No hay diferencia significativa de Nº Contratos entre Masculino y Femenino (α = 0.05)

**Tamaño del efecto**

- d de Cohen = `+0.133` (despreciable)

### Nº Contratos × Centro

| Centro | n | Media | Mediana | Desv. típica | Mín | Máx |
|---|---:|---:|---:|---:|---:|---:|
| Universidad de Valladolid | 59 | 1.000 | 1.000 | 0.616 | 0.000 | 2.000 |
| Universidad de Salamanca | 76 | 0.987 | 1.000 | 0.600 | 0.000 | 2.000 |
| Universidad de León | 26 | 0.846 | 1.000 | 0.368 | 0.000 | 1.000 |
| Universidad de Burgos | 29 | 1.241 | 1.000 | 0.577 | 0.000 | 2.000 |
| CSIC | 21 | 1.286 | 1.000 | 0.463 | 1.000 | 2.000 |

**Homocedasticidad (Levene):** W = `1.2112`, p = `0.30716` — las varianzas son homogéneas entre grupos.

**ANOVA** (tabla de 5 grupos)

- Clásico: F = `2.9113`, p = `0.02258`
- Welch: F = `4.2111`, gl = `4, 76.07`, p = `0.00392`
- **Conclusión (Welch):** Hay diferencia significativa de Nº Contratos entre los 5 grupos de Centro (α = 0.05)

**Tamaño del efecto**

- η² = `0.0535` (pequeño) — el grupo explica el 5.4% de la variabilidad de Nº Contratos

**Post-hoc — comparaciones dos a dos** (t de Welch, corrección: Bonferroni (FWER))

| Par | Dif. de medias | p crudo | p ajustado | d de Cohen | Significativo |
|---|---:|---:|---:|---:|:---:|
| Universidad de Valladolid vs. Universidad de Salamanca | +0.013 | 0.90110 | 1.00000 | +0.022 | no |
| Universidad de Valladolid vs. Universidad de León | +0.154 | 0.15794 | 1.00000 | +0.278 | no |
| Universidad de Valladolid vs. Universidad de Burgos | -0.241 | 0.07625 | 0.76253 | -0.400 | no |
| Universidad de Valladolid vs. CSIC | -0.286 | 0.03164 | 0.31644 | -0.492 | no |
| Universidad de Salamanca vs. Universidad de León | +0.141 | 0.16258 | 1.00000 | +0.255 | no |
| Universidad de Salamanca vs. Universidad de Burgos | -0.255 | 0.05070 | 0.50702 | -0.429 | no |
| Universidad de Salamanca vs. CSIC | -0.299 | 0.01891 | 0.18909 | -0.521 | no |
| Universidad de León vs. Universidad de Burgos | -0.395 | 0.00361 | 0.03606 | -0.808 | ✅ sí |
| Universidad de León vs. CSIC | -0.440 | 0.00108 | 0.01079 | -1.065 | ✅ sí |
| Universidad de Burgos vs. CSIC | -0.044 | 0.76460 | 1.00000 | -0.083 | no |

> 10 comparaciones dos a dos; el p-valor ajustado es el que se compara contra α = 0.05.

### Nº Contratos × Rama

| Rama | n | Media | Mediana | Desv. típica | Mín | Máx |
|---|---:|---:|---:|---:|---:|---:|
| Ciencias - Ciencias de la Salud | 65 | 1.200 | 1.000 | 0.474 | 0.000 | 2.000 |
| Ciencias - Resto | 53 | 1.170 | 1.000 | 0.509 | 0.000 | 2.000 |
| Ingenierías | 35 | 1.029 | 1.000 | 0.514 | 0.000 | 2.000 |
| Ciencias Sociales - Resto | 18 | 0.833 | 1.000 | 0.786 | 0.000 | 2.000 |
| Filosofía y Letras | 16 | 0.438 | 0.000 | 0.727 | 0.000 | 2.000 |
| Ciencias - Matemáticas y Física | 30 | 1.033 | 1.000 | 0.556 | 0.000 | 2.000 |

**Homocedasticidad (Levene):** W = `1.8979`, p = `0.09596` — las varianzas son homogéneas entre grupos.

**ANOVA** (tabla de 6 grupos)

- Clásico: F = `5.9701`, p = `0.00003`
- Welch: F = `3.9070`, gl = `5, 64.96`, p = `0.00370`
- **Conclusión (Welch):** Hay diferencia significativa de Nº Contratos entre los 6 grupos de Rama (α = 0.05)

**Tamaño del efecto**

- η² = `0.1239` (medio) — el grupo explica el 12.4% de la variabilidad de Nº Contratos

**Post-hoc — comparaciones dos a dos** (t de Welch, corrección: Bonferroni (FWER))

| Par | Dif. de medias | p crudo | p ajustado | d de Cohen | Significativo |
|---|---:|---:|---:|---:|:---:|
| Ciencias - Ciencias de la Salud vs. Ciencias - Resto | +0.030 | 0.74176 | 1.00000 | +0.062 | no |
| Ciencias - Ciencias de la Salud vs. Ingenierías | +0.171 | 0.10699 | 1.00000 | +0.351 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias Sociales - Resto | +0.367 | 0.07343 | 1.00000 | +0.661 | no |
| Ciencias - Ciencias de la Salud vs. Filosofía y Letras | +0.762 | 0.00084 | 0.01260 | +1.434 | ✅ sí |
| Ciencias - Ciencias de la Salud vs. Ciencias - Matemáticas y Física | +0.167 | 0.16179 | 1.00000 | +0.333 | no |
| Ciencias - Resto vs. Ingenierías | +0.141 | 0.20922 | 1.00000 | +0.276 | no |
| Ciencias - Resto vs. Ciencias Sociales - Resto | +0.336 | 0.10331 | 1.00000 | +0.571 | no |
| Ciencias - Resto vs. Filosofía y Letras | +0.732 | 0.00127 | 0.01903 | +1.295 | ✅ sí |
| Ciencias - Resto vs. Ciencias - Matemáticas y Física | +0.136 | 0.27295 | 1.00000 | +0.259 | no |
| Ingenierías vs. Ciencias Sociales - Resto | +0.195 | 0.34916 | 1.00000 | +0.316 | no |
| Ingenierías vs. Filosofía y Letras | +0.591 | 0.00767 | 0.11509 | +1.006 | no |
| Ingenierías vs. Ciencias - Matemáticas y Física | -0.005 | 0.97168 | 1.00000 | -0.009 | no |
| Ciencias Sociales - Resto vs. Filosofía y Letras | +0.396 | 0.13714 | 1.00000 | +0.521 | no |
| Ciencias Sociales - Resto vs. Ciencias - Matemáticas y Física | -0.200 | 0.35204 | 1.00000 | -0.307 | no |
| Filosofía y Letras vs. Ciencias - Matemáticas y Física | -0.596 | 0.00850 | 0.12749 | -0.961 | no |

> 15 comparaciones dos a dos; el p-valor ajustado es el que se compara contra α = 0.05.
