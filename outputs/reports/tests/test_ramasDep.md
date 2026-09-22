# Test de independencia — Rama(Departamento) vs. Estado de Solicitud

_Generado el 2026-07-15 19:54_

> Nota metodológica: la tabla es de 7 ramas × 2 estados. El test exacto de Fisher clásico de scipy solo admite tablas 2×2, así que se combinan tres aproximaciones: **chi-cuadrado** sobre la tabla completa, **Fisher exacto de tabla completa vía R** (rpy2), y **Fisher exacto** de cada par de ramas comparadas entre sí (2×2), con los p-valores corregidos por comparaciones múltiples (método: bonferroni).

## GENERAL — Todos los años

| Rama | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Ciencias - Ciencias de la Salud | 194 | 448 | 642 |
| Ciencias - Resto | 128 | 296 | 424 |
| Ingenierías | 103 | 327 | 430 |
| Ciencias Sociales - Resto | 63 | 259 | 322 |
| Filosofía y Letras | 62 | 175 | 237 |
| Ciencias - Matemáticas y Física | 72 | 156 | 228 |
| Ciencias Sociales - Educación | 8 | 90 | 98 |
| **Total** | **630** | **1751** | **2381** |

**Chi-cuadrado de independencia** (tabla 7×2)

- χ² = `36.8857`
- gl = `6`
- p-valor = `0.00000`
- **Conclusión:** Hay asociación significativa entre Rama y Estado (α = 0.05)

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.00001` (método: simulado (Monte Carlo, B=100000))
- **Conclusión:** Hay asociación significativa entre Rama y Estado (α = 0.05)

**Test exacto de Fisher — comparaciones dos a dos entre ramas** (corrección: Bonferroni (FWER))

| Par de ramas | p-valor crudo | p-valor ajustado | Odds Ratio | Significativo |
|---|---:|---:|---:|:---:|
| Ciencias - Ciencias de la Salud vs. Ciencias - Resto | 1.00000 | 1.00000 | 1.001 | no |
| Ciencias - Ciencias de la Salud vs. Ingenierías | 0.02596 | 0.54506 | 1.375 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias Sociales - Resto | 0.00038 | 0.00794 | 1.780 | ✅ sí |
| Ciencias - Ciencias de la Salud vs. Filosofía y Letras | 0.27679 | 1.00000 | 1.222 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias - Matemáticas y Física | 0.73797 | 1.00000 | 0.938 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias Sociales - Educación | 0.00000 | 0.00002 | 4.872 | ✅ sí |
| Ciencias - Resto vs. Ingenierías | 0.04515 | 0.94808 | 1.373 | no |
| Ciencias - Resto vs. Ciencias Sociales - Resto | 0.00096 | 0.02023 | 1.778 | ✅ sí |
| Ciencias - Resto vs. Filosofía y Letras | 0.28354 | 1.00000 | 1.221 | no |
| Ciencias - Resto vs. Ciencias - Matemáticas y Física | 0.72238 | 1.00000 | 0.937 | no |
| Ciencias - Resto vs. Ciencias Sociales - Educación | 0.00000 | 0.00003 | 4.865 | ✅ sí |
| Ingenierías vs. Ciencias Sociales - Resto | 0.15625 | 1.00000 | 1.295 | no |
| Ingenierías vs. Filosofía y Letras | 0.57388 | 1.00000 | 0.889 | no |
| Ingenierías vs. Ciencias - Matemáticas y Física | 0.04126 | 0.86652 | 0.682 | no |
| Ingenierías vs. Ciencias Sociales - Educación | 0.00030 | 0.00639 | 3.544 | ✅ sí |
| Ciencias Sociales - Resto vs. Filosofía y Letras | 0.08054 | 1.00000 | 0.687 | no |
| Ciencias Sociales - Resto vs. Ciencias - Matemáticas y Física | 0.00176 | 0.03697 | 0.527 | ✅ sí |
| Ciencias Sociales - Resto vs. Ciencias Sociales - Educación | 0.00840 | 0.17641 | 2.736 | no |
| Filosofía y Letras vs. Ciencias - Matemáticas y Física | 0.21942 | 1.00000 | 0.768 | no |
| Filosofía y Letras vs. Ciencias Sociales - Educación | 0.00018 | 0.00376 | 3.986 | ✅ sí |
| Ciencias - Matemáticas y Física vs. Ciencias Sociales - Educación | 0.00000 | 0.00005 | 5.192 | ✅ sí |

> Se han realizado **21** comparaciones dos a dos; el p-valor ajustado es el que debe compararse contra α = 0.05 para decidir significancia.

## AÑO 2010

| Rama | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Ciencias - Ciencias de la Salud | 21 | 44 | 65 |
| Ciencias - Resto | 19 | 28 | 47 |
| Ingenierías | 14 | 53 | 67 |
| Ciencias Sociales - Resto | 24 | 42 | 66 |
| Filosofía y Letras | 26 | 28 | 54 |
| Ciencias - Matemáticas y Física | 3 | 21 | 24 |
| Ciencias Sociales - Educación | 7 | 17 | 24 |
| **Total** | **114** | **233** | **347** |

**Chi-cuadrado de independencia** (tabla 7×2)

- χ² = `16.3231`
- gl = `6`
- p-valor = `0.01212`
- **Conclusión:** Hay asociación significativa entre Rama y Estado (α = 0.05)

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.01064` (método: simulado (Monte Carlo, B=100000))
- **Conclusión:** Hay asociación significativa entre Rama y Estado (α = 0.05)

**Test exacto de Fisher — comparaciones dos a dos entre ramas** (corrección: Bonferroni (FWER))

| Par de ramas | p-valor crudo | p-valor ajustado | Odds Ratio | Significativo |
|---|---:|---:|---:|:---:|
| Ciencias - Ciencias de la Salud vs. Ciencias - Resto | 0.42700 | 1.00000 | 0.703 | no |
| Ciencias - Ciencias de la Salud vs. Ingenierías | 0.16877 | 1.00000 | 1.807 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias Sociales - Resto | 0.71367 | 1.00000 | 0.835 | no |
| Ciencias - Ciencias de la Salud vs. Filosofía y Letras | 0.09203 | 1.00000 | 0.514 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias - Matemáticas y Física | 0.10428 | 1.00000 | 3.341 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias Sociales - Educación | 1.00000 | 1.00000 | 1.159 | no |
| Ciencias - Resto vs. Ingenierías | 0.03523 | 0.73983 | 2.569 | no |
| Ciencias - Resto vs. Ciencias Sociales - Resto | 0.69746 | 1.00000 | 1.188 | no |
| Ciencias - Resto vs. Filosofía y Letras | 0.54752 | 1.00000 | 0.731 | no |
| Ciencias - Resto vs. Ciencias - Matemáticas y Física | 0.02833 | 0.59485 | 4.750 | no |
| Ciencias - Resto vs. Ciencias Sociales - Educación | 0.43886 | 1.00000 | 1.648 | no |
| Ingenierías vs. Ciencias Sociales - Resto | 0.05646 | 1.00000 | 0.462 | no |
| Ingenierías vs. Filosofía y Letras | 0.00191 | 0.04016 | 0.284 | ✅ sí |
| Ingenierías vs. Ciencias - Matemáticas y Física | 0.54356 | 1.00000 | 1.849 | no |
| Ingenierías vs. Ciencias Sociales - Educación | 0.41095 | 1.00000 | 0.642 | no |
| Ciencias Sociales - Resto vs. Filosofía y Letras | 0.20002 | 1.00000 | 0.615 | no |
| Ciencias Sociales - Resto vs. Ciencias - Matemáticas y Física | 0.03723 | 0.78175 | 4.000 | no |
| Ciencias Sociales - Resto vs. Ciencias Sociales - Educación | 0.62042 | 1.00000 | 1.388 | no |
| Filosofía y Letras vs. Ciencias - Matemáticas y Física | 0.00253 | 0.05318 | 6.500 | no |
| Filosofía y Letras vs. Ciencias Sociales - Educación | 0.14152 | 1.00000 | 2.255 | no |
| Ciencias - Matemáticas y Física vs. Ciencias Sociales - Educación | 0.28647 | 1.00000 | 0.347 | no |

> Se han realizado **21** comparaciones dos a dos; el p-valor ajustado es el que debe compararse contra α = 0.05 para decidir significancia.

## AÑO 2014

| Rama | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Ciencias - Ciencias de la Salud | 22 | 71 | 93 |
| Ciencias - Resto | 9 | 44 | 53 |
| Ingenierías | 10 | 44 | 54 |
| Ciencias Sociales - Resto | 5 | 56 | 61 |
| Filosofía y Letras | 7 | 39 | 46 |
| Ciencias - Matemáticas y Física | 5 | 31 | 36 |
| Ciencias Sociales - Educación | 0 | 10 | 10 |
| **Total** | **58** | **295** | **353** |

**Chi-cuadrado de independencia** (tabla 7×2)

- χ² = `8.9157`
- gl = `6`
- p-valor = `0.17838`
- **Conclusión:** No hay asociación significativa entre Rama y Estado (α = 0.05)

> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable, revisa los tests de Fisher de abajo.

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.19760` (método: simulado (Monte Carlo, B=100000))
- **Conclusión:** No hay asociación significativa entre Rama y Estado (α = 0.05)

**Test exacto de Fisher — comparaciones dos a dos entre ramas** (corrección: Bonferroni (FWER))

| Par de ramas | p-valor crudo | p-valor ajustado | Odds Ratio | Significativo |
|---|---:|---:|---:|:---:|
| Ciencias - Ciencias de la Salud vs. Ciencias - Resto | 0.40402 | 1.00000 | 1.515 | no |
| Ciencias - Ciencias de la Salud vs. Ingenierías | 0.53774 | 1.00000 | 1.363 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias Sociales - Resto | 0.01653 | 0.34719 | 3.470 | no |
| Ciencias - Ciencias de la Salud vs. Filosofía y Letras | 0.27692 | 1.00000 | 1.726 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias - Matemáticas y Física | 0.33420 | 1.00000 | 1.921 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias Sociales - Educación | 0.11415 | 1.00000 | inf | no |
| Ciencias - Resto vs. Ingenierías | 1.00000 | 1.00000 | 0.900 | no |
| Ciencias - Resto vs. Ciencias Sociales - Resto | 0.16758 | 1.00000 | 2.291 | no |
| Ciencias - Resto vs. Filosofía y Letras | 1.00000 | 1.00000 | 1.140 | no |
| Ciencias - Resto vs. Ciencias - Matemáticas y Física | 0.77382 | 1.00000 | 1.268 | no |
| Ciencias - Resto vs. Ciencias Sociales - Educación | 0.33244 | 1.00000 | inf | no |
| Ingenierías vs. Ciencias Sociales - Resto | 0.16397 | 1.00000 | 2.545 | no |
| Ingenierías vs. Filosofía y Letras | 0.79134 | 1.00000 | 1.266 | no |
| Ingenierías vs. Ciencias - Matemáticas y Física | 0.77382 | 1.00000 | 1.409 | no |
| Ingenierías vs. Ciencias Sociales - Educación | 0.33982 | 1.00000 | inf | no |
| Ciencias Sociales - Resto vs. Filosofía y Letras | 0.35506 | 1.00000 | 0.497 | no |
| Ciencias Sociales - Resto vs. Ciencias - Matemáticas y Física | 0.49225 | 1.00000 | 0.554 | no |
| Ciencias Sociales - Resto vs. Ciencias Sociales - Educación | 1.00000 | 1.00000 | inf | no |
| Filosofía y Letras vs. Ciencias - Matemáticas y Física | 1.00000 | 1.00000 | 1.113 | no |
| Filosofía y Letras vs. Ciencias Sociales - Educación | 0.33014 | 1.00000 | inf | no |
| Ciencias - Matemáticas y Física vs. Ciencias Sociales - Educación | 0.57027 | 1.00000 | inf | no |

> Se han realizado **21** comparaciones dos a dos; el p-valor ajustado es el que debe compararse contra α = 0.05 para decidir significancia.

## AÑO 2015

| Rama | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Ciencias - Ciencias de la Salud | 29 | 73 | 102 |
| Ciencias - Resto | 8 | 38 | 46 |
| Ingenierías | 9 | 51 | 60 |
| Ciencias Sociales - Resto | 7 | 59 | 66 |
| Filosofía y Letras | 6 | 45 | 51 |
| Ciencias - Matemáticas y Física | 8 | 28 | 36 |
| Ciencias Sociales - Educación | 0 | 14 | 14 |
| **Total** | **67** | **308** | **375** |

**Chi-cuadrado de independencia** (tabla 7×2)

- χ² = `15.2770`
- gl = `6`
- p-valor = `0.01821`
- **Conclusión:** Hay asociación significativa entre Rama y Estado (α = 0.05)

> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable, revisa los tests de Fisher de abajo.

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.02159` (método: simulado (Monte Carlo, B=100000))
- **Conclusión:** Hay asociación significativa entre Rama y Estado (α = 0.05)

**Test exacto de Fisher — comparaciones dos a dos entre ramas** (corrección: Bonferroni (FWER))

| Par de ramas | p-valor crudo | p-valor ajustado | Odds Ratio | Significativo |
|---|---:|---:|---:|:---:|
| Ciencias - Ciencias de la Salud vs. Ciencias - Resto | 0.21796 | 1.00000 | 1.887 | no |
| Ciencias - Ciencias de la Salud vs. Ingenierías | 0.05689 | 1.00000 | 2.251 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias Sociales - Resto | 0.00675 | 0.14168 | 3.348 | no |
| Ciencias - Ciencias de la Salud vs. Filosofía y Letras | 0.02446 | 0.51375 | 2.979 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias - Matemáticas y Física | 0.51956 | 1.00000 | 1.390 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias Sociales - Educación | 0.01975 | 0.41472 | inf | no |
| Ciencias - Resto vs. Ingenierías | 0.79329 | 1.00000 | 1.193 | no |
| Ciencias - Resto vs. Ciencias Sociales - Resto | 0.39904 | 1.00000 | 1.774 | no |
| Ciencias - Resto vs. Filosofía y Letras | 0.56514 | 1.00000 | 1.579 | no |
| Ciencias - Resto vs. Ciencias - Matemáticas y Física | 0.58942 | 1.00000 | 0.737 | no |
| Ciencias - Resto vs. Ciencias Sociales - Educación | 0.17898 | 1.00000 | inf | no |
| Ingenierías vs. Ciencias Sociales - Resto | 0.59388 | 1.00000 | 1.487 | no |
| Ingenierías vs. Filosofía y Letras | 0.78210 | 1.00000 | 1.324 | no |
| Ingenierías vs. Ciencias - Matemáticas y Física | 0.41459 | 1.00000 | 0.618 | no |
| Ingenierías vs. Ciencias Sociales - Educación | 0.19304 | 1.00000 | inf | no |
| Ciencias Sociales - Resto vs. Filosofía y Letras | 1.00000 | 1.00000 | 0.890 | no |
| Ciencias Sociales - Resto vs. Ciencias - Matemáticas y Física | 0.14571 | 1.00000 | 0.415 | no |
| Ciencias Sociales - Resto vs. Ciencias Sociales - Educación | 0.34357 | 1.00000 | inf | no |
| Filosofía y Letras vs. Ciencias - Matemáticas y Física | 0.24079 | 1.00000 | 0.467 | no |
| Filosofía y Letras vs. Ciencias Sociales - Educación | 0.32653 | 1.00000 | inf | no |
| Ciencias - Matemáticas y Física vs. Ciencias Sociales - Educación | 0.08675 | 1.00000 | inf | no |

> Se han realizado **21** comparaciones dos a dos; el p-valor ajustado es el que debe compararse contra α = 0.05 para decidir significancia.

## AÑO 2016

| Rama | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Ciencias - Ciencias de la Salud | 23 | 28 | 51 |
| Ciencias - Resto | 17 | 11 | 28 |
| Ingenierías | 10 | 11 | 21 |
| Ciencias Sociales - Resto | 2 | 7 | 9 |
| Filosofía y Letras | 1 | 8 | 9 |
| Ciencias - Matemáticas y Física | 10 | 2 | 12 |
| Ciencias Sociales - Educación | 0 | 3 | 3 |
| **Total** | **63** | **70** | **133** |

**Chi-cuadrado de independencia** (tabla 7×2)

- χ² = `18.0607`
- gl = `6`
- p-valor = `0.00608`
- **Conclusión:** Hay asociación significativa entre Rama y Estado (α = 0.05)

> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable, revisa los tests de Fisher de abajo.

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.00492` (método: exacto)
- **Conclusión:** Hay asociación significativa entre Rama y Estado (α = 0.05)

**Test exacto de Fisher — comparaciones dos a dos entre ramas** (corrección: Bonferroni (FWER))

| Par de ramas | p-valor crudo | p-valor ajustado | Odds Ratio | Significativo |
|---|---:|---:|---:|:---:|
| Ciencias - Ciencias de la Salud vs. Ciencias - Resto | 0.24100 | 1.00000 | 0.532 | no |
| Ciencias - Ciencias de la Salud vs. Ingenierías | 1.00000 | 1.00000 | 0.904 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias Sociales - Resto | 0.28150 | 1.00000 | 2.875 | no |
| Ciencias - Ciencias de la Salud vs. Filosofía y Letras | 0.07212 | 1.00000 | 6.571 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias - Matemáticas y Física | 0.02405 | 0.50507 | 0.164 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias Sociales - Educación | 0.25262 | 1.00000 | inf | no |
| Ciencias - Resto vs. Ingenierías | 0.39841 | 1.00000 | 1.700 | no |
| Ciencias - Resto vs. Ciencias Sociales - Resto | 0.06250 | 1.00000 | 5.409 | no |
| Ciencias - Resto vs. Filosofía y Letras | 0.01875 | 0.39380 | 12.364 | no |
| Ciencias - Resto vs. Ciencias - Matemáticas y Física | 0.27138 | 1.00000 | 0.309 | no |
| Ciencias - Resto vs. Ciencias Sociales - Educación | 0.08098 | 1.00000 | inf | no |
| Ingenierías vs. Ciencias Sociales - Resto | 0.24871 | 1.00000 | 3.182 | no |
| Ingenierías vs. Filosofía y Letras | 0.10003 | 1.00000 | 7.273 | no |
| Ingenierías vs. Ciencias - Matemáticas y Física | 0.06715 | 1.00000 | 0.182 | no |
| Ingenierías vs. Ciencias Sociales - Educación | 0.23913 | 1.00000 | inf | no |
| Ciencias Sociales - Resto vs. Filosofía y Letras | 1.00000 | 1.00000 | 2.286 | no |
| Ciencias Sociales - Resto vs. Ciencias - Matemáticas y Física | 0.00920 | 0.19326 | 0.057 | no |
| Ciencias Sociales - Resto vs. Ciencias Sociales - Educación | 1.00000 | 1.00000 | inf | no |
| Filosofía y Letras vs. Ciencias - Matemáticas y Física | 0.00191 | 0.04001 | 0.025 | ✅ sí |
| Filosofía y Letras vs. Ciencias Sociales - Educación | 1.00000 | 1.00000 | inf | no |
| Ciencias - Matemáticas y Física vs. Ciencias Sociales - Educación | 0.02198 | 0.46154 | inf | no |

> Se han realizado **21** comparaciones dos a dos; el p-valor ajustado es el que debe compararse contra α = 0.05 para decidir significancia.

## AÑO 2017

| Rama | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Ciencias - Ciencias de la Salud | 19 | 17 | 36 |
| Ciencias - Resto | 15 | 8 | 23 |
| Ingenierías | 12 | 4 | 16 |
| Ciencias Sociales - Resto | 5 | 12 | 17 |
| Filosofía y Letras | 2 | 10 | 12 |
| Ciencias - Matemáticas y Física | 6 | 6 | 12 |
| Ciencias Sociales - Educación | 1 | 2 | 3 |
| **Total** | **60** | **59** | **119** |

**Chi-cuadrado de independencia** (tabla 7×2)

- χ² = `14.7832`
- gl = `6`
- p-valor = `0.02201`
- **Conclusión:** Hay asociación significativa entre Rama y Estado (α = 0.05)

> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable, revisa los tests de Fisher de abajo.

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.01707` (método: exacto)
- **Conclusión:** Hay asociación significativa entre Rama y Estado (α = 0.05)

**Test exacto de Fisher — comparaciones dos a dos entre ramas** (corrección: Bonferroni (FWER))

| Par de ramas | p-valor crudo | p-valor ajustado | Odds Ratio | Significativo |
|---|---:|---:|---:|:---:|
| Ciencias - Ciencias de la Salud vs. Ciencias - Resto | 0.42297 | 1.00000 | 0.596 | no |
| Ciencias - Ciencias de la Salud vs. Ingenierías | 0.22039 | 1.00000 | 0.373 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias Sociales - Resto | 0.14488 | 1.00000 | 2.682 | no |
| Ciencias - Ciencias de la Salud vs. Filosofía y Letras | 0.04387 | 0.92121 | 5.588 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias - Matemáticas y Física | 1.00000 | 1.00000 | 1.118 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias Sociales - Educación | 0.60499 | 1.00000 | 2.235 | no |
| Ciencias - Resto vs. Ingenierías | 0.72618 | 1.00000 | 0.625 | no |
| Ciencias - Resto vs. Ciencias Sociales - Resto | 0.05355 | 1.00000 | 4.500 | no |
| Ciencias - Resto vs. Filosofía y Letras | 0.01164 | 0.24449 | 9.375 | no |
| Ciencias - Resto vs. Ciencias - Matemáticas y Física | 0.47692 | 1.00000 | 1.875 | no |
| Ciencias - Resto vs. Ciencias Sociales - Educación | 0.53846 | 1.00000 | 3.750 | no |
| Ingenierías vs. Ciencias Sociales - Resto | 0.01492 | 0.31330 | 7.200 | no |
| Ingenierías vs. Filosofía y Letras | 0.00633 | 0.13292 | 15.000 | no |
| Ingenierías vs. Ciencias - Matemáticas y Física | 0.24254 | 1.00000 | 3.000 | no |
| Ingenierías vs. Ciencias Sociales - Educación | 0.22188 | 1.00000 | 6.000 | no |
| Ciencias Sociales - Resto vs. Filosofía y Letras | 0.66453 | 1.00000 | 2.083 | no |
| Ciencias Sociales - Resto vs. Ciencias - Matemáticas y Física | 0.43844 | 1.00000 | 0.417 | no |
| Ciencias Sociales - Resto vs. Ciencias Sociales - Educación | 1.00000 | 1.00000 | 0.833 | no |
| Filosofía y Letras vs. Ciencias - Matemáticas y Física | 0.19303 | 1.00000 | 0.200 | no |
| Filosofía y Letras vs. Ciencias Sociales - Educación | 0.51648 | 1.00000 | 0.400 | no |
| Ciencias - Matemáticas y Física vs. Ciencias Sociales - Educación | 1.00000 | 1.00000 | 2.000 | no |

> Se han realizado **21** comparaciones dos a dos; el p-valor ajustado es el que debe compararse contra α = 0.05 para decidir significancia.

## AÑO 2019

| Rama | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Ciencias - Ciencias de la Salud | 14 | 20 | 34 |
| Ciencias - Resto | 7 | 20 | 27 |
| Ingenierías | 13 | 21 | 34 |
| Ciencias Sociales - Resto | 2 | 22 | 24 |
| Filosofía y Letras | 4 | 7 | 11 |
| Ciencias - Matemáticas y Física | 10 | 5 | 15 |
| Ciencias Sociales - Educación | 0 | 4 | 4 |
| **Total** | **50** | **99** | **149** |

**Chi-cuadrado de independencia** (tabla 7×2)

- χ² = `18.2069`
- gl = `6`
- p-valor = `0.00574`
- **Conclusión:** Hay asociación significativa entre Rama y Estado (α = 0.05)

> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable, revisa los tests de Fisher de abajo.

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.00405` (método: simulado (Monte Carlo, B=100000))
- **Conclusión:** Hay asociación significativa entre Rama y Estado (α = 0.05)

**Test exacto de Fisher — comparaciones dos a dos entre ramas** (corrección: Bonferroni (FWER))

| Par de ramas | p-valor crudo | p-valor ajustado | Odds Ratio | Significativo |
|---|---:|---:|---:|:---:|
| Ciencias - Ciencias de la Salud vs. Ciencias - Resto | 0.28111 | 1.00000 | 2.000 | no |
| Ciencias - Ciencias de la Salud vs. Ingenierías | 1.00000 | 1.00000 | 1.131 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias Sociales - Resto | 0.00716 | 0.15034 | 7.700 | no |
| Ciencias - Ciencias de la Salud vs. Filosofía y Letras | 1.00000 | 1.00000 | 1.225 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias - Matemáticas y Física | 0.12835 | 1.00000 | 0.350 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias Sociales - Educación | 0.27587 | 1.00000 | inf | no |
| Ciencias - Resto vs. Ingenierías | 0.41242 | 1.00000 | 0.565 | no |
| Ciencias - Resto vs. Ciencias Sociales - Resto | 0.14650 | 1.00000 | 3.850 | no |
| Ciencias - Resto vs. Filosofía y Letras | 0.69558 | 1.00000 | 0.613 | no |
| Ciencias - Resto vs. Ciencias - Matemáticas y Física | 0.02018 | 0.42375 | 0.175 | no |
| Ciencias - Resto vs. Ciencias Sociales - Educación | 0.54972 | 1.00000 | inf | no |
| Ingenierías vs. Ciencias Sociales - Resto | 0.01428 | 0.29983 | 6.810 | no |
| Ingenierías vs. Filosofía y Letras | 1.00000 | 1.00000 | 1.083 | no |
| Ingenierías vs. Ciencias - Matemáticas y Física | 0.11917 | 1.00000 | 0.310 | no |
| Ingenierías vs. Ciencias Sociales - Educación | 0.27792 | 1.00000 | inf | no |
| Ciencias Sociales - Resto vs. Filosofía y Letras | 0.06323 | 1.00000 | 0.159 | no |
| Ciencias Sociales - Resto vs. Ciencias - Matemáticas y Física | 0.00022 | 0.00463 | 0.045 | ✅ sí |
| Ciencias Sociales - Resto vs. Ciencias Sociales - Educación | 1.00000 | 1.00000 | inf | no |
| Filosofía y Letras vs. Ciencias - Matemáticas y Física | 0.23286 | 1.00000 | 0.286 | no |
| Filosofía y Letras vs. Ciencias Sociales - Educación | 0.51648 | 1.00000 | inf | no |
| Ciencias - Matemáticas y Física vs. Ciencias Sociales - Educación | 0.03251 | 0.68266 | inf | no |

> Se han realizado **21** comparaciones dos a dos; el p-valor ajustado es el que debe compararse contra α = 0.05 para decidir significancia.

## AÑO 2021

| Rama | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Ciencias - Ciencias de la Salud | 33 | 42 | 75 |
| Ciencias - Resto | 21 | 27 | 48 |
| Ingenierías | 15 | 41 | 56 |
| Ciencias Sociales - Resto | 12 | 23 | 35 |
| Filosofía y Letras | 6 | 11 | 17 |
| Ciencias - Matemáticas y Física | 13 | 7 | 20 |
| Ciencias Sociales - Educación | 0 | 11 | 11 |
| **Total** | **100** | **162** | **262** |

**Chi-cuadrado de independencia** (tabla 7×2)

- χ² = `17.9633`
- gl = `6`
- p-valor = `0.00632`
- **Conclusión:** Hay asociación significativa entre Rama y Estado (α = 0.05)

> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable, revisa los tests de Fisher de abajo.

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.00415` (método: simulado (Monte Carlo, B=100000))
- **Conclusión:** Hay asociación significativa entre Rama y Estado (α = 0.05)

**Test exacto de Fisher — comparaciones dos a dos entre ramas** (corrección: Bonferroni (FWER))

| Par de ramas | p-valor crudo | p-valor ajustado | Odds Ratio | Significativo |
|---|---:|---:|---:|:---:|
| Ciencias - Ciencias de la Salud vs. Ciencias - Resto | 1.00000 | 1.00000 | 1.010 | no |
| Ciencias - Ciencias de la Salud vs. Ingenierías | 0.04644 | 0.97529 | 2.148 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias Sociales - Resto | 0.40696 | 1.00000 | 1.506 | no |
| Ciencias - Ciencias de la Salud vs. Filosofía y Letras | 0.59380 | 1.00000 | 1.440 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias - Matemáticas y Física | 0.13124 | 1.00000 | 0.423 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias Sociales - Educación | 0.00550 | 0.11543 | inf | no |
| Ciencias - Resto vs. Ingenierías | 0.09788 | 1.00000 | 2.126 | no |
| Ciencias - Resto vs. Ciencias Sociales - Resto | 0.49647 | 1.00000 | 1.491 | no |
| Ciencias - Resto vs. Filosofía y Letras | 0.58151 | 1.00000 | 1.426 | no |
| Ciencias - Resto vs. Ciencias - Matemáticas y Física | 0.18263 | 1.00000 | 0.419 | no |
| Ciencias - Resto vs. Ciencias Sociales - Educación | 0.00509 | 0.10683 | inf | no |
| Ingenierías vs. Ciencias Sociales - Resto | 0.48536 | 1.00000 | 0.701 | no |
| Ingenierías vs. Filosofía y Letras | 0.54740 | 1.00000 | 0.671 | no |
| Ingenierías vs. Ciencias - Matemáticas y Física | 0.00336 | 0.07050 | 0.197 | no |
| Ingenierías vs. Ciencias Sociales - Educación | 0.05860 | 1.00000 | inf | no |
| Ciencias Sociales - Resto vs. Filosofía y Letras | 1.00000 | 1.00000 | 0.957 | no |
| Ciencias Sociales - Resto vs. Ciencias - Matemáticas y Física | 0.04781 | 1.00000 | 0.281 | no |
| Ciencias Sociales - Resto vs. Ciencias Sociales - Educación | 0.04370 | 0.91775 | inf | no |
| Filosofía y Letras vs. Ciencias - Matemáticas y Física | 0.10314 | 1.00000 | 0.294 | no |
| Filosofía y Letras vs. Ciencias Sociales - Educación | 0.05492 | 1.00000 | inf | no |
| Ciencias - Matemáticas y Física vs. Ciencias Sociales - Educación | 0.00044 | 0.00919 | inf | ✅ sí |

> Se han realizado **21** comparaciones dos a dos; el p-valor ajustado es el que debe compararse contra α = 0.05 para decidir significancia.

## AÑO 2024

| Rama | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Ciencias - Ciencias de la Salud | 16 | 56 | 72 |
| Ciencias - Resto | 10 | 48 | 58 |
| Ingenierías | 5 | 41 | 46 |
| Ciencias Sociales - Resto | 2 | 9 | 11 |
| Filosofía y Letras | 0 | 13 | 13 |
| Ciencias - Matemáticas y Física | 3 | 24 | 27 |
| Ciencias Sociales - Educación | 0 | 11 | 11 |
| **Total** | **36** | **202** | **238** |

**Chi-cuadrado de independencia** (tabla 7×2)

- χ² = `8.3717`
- gl = `6`
- p-valor = `0.21212`
- **Conclusión:** No hay asociación significativa entre Rama y Estado (α = 0.05)

> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable, revisa los tests de Fisher de abajo.

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.24669` (método: exacto)
- **Conclusión:** No hay asociación significativa entre Rama y Estado (α = 0.05)

**Test exacto de Fisher — comparaciones dos a dos entre ramas** (corrección: Bonferroni (FWER))

| Par de ramas | p-valor crudo | p-valor ajustado | Odds Ratio | Significativo |
|---|---:|---:|---:|:---:|
| Ciencias - Ciencias de la Salud vs. Ciencias - Resto | 0.51615 | 1.00000 | 1.371 | no |
| Ciencias - Ciencias de la Salud vs. Ingenierías | 0.14268 | 1.00000 | 2.343 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias Sociales - Resto | 1.00000 | 1.00000 | 1.286 | no |
| Ciencias - Ciencias de la Salud vs. Filosofía y Letras | 0.11551 | 1.00000 | inf | no |
| Ciencias - Ciencias de la Salud vs. Ciencias - Matemáticas y Física | 0.26271 | 1.00000 | 2.286 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias Sociales - Educación | 0.11199 | 1.00000 | inf | no |
| Ciencias - Resto vs. Ingenierías | 0.41144 | 1.00000 | 1.708 | no |
| Ciencias - Resto vs. Ciencias Sociales - Resto | 1.00000 | 1.00000 | 0.938 | no |
| Ciencias - Resto vs. Filosofía y Letras | 0.19015 | 1.00000 | inf | no |
| Ciencias - Resto vs. Ciencias - Matemáticas y Física | 0.53759 | 1.00000 | 1.667 | no |
| Ciencias - Resto vs. Ciencias Sociales - Educación | 0.34547 | 1.00000 | inf | no |
| Ingenierías vs. Ciencias Sociales - Resto | 0.61029 | 1.00000 | 0.549 | no |
| Ingenierías vs. Filosofía y Letras | 0.57626 | 1.00000 | inf | no |
| Ingenierías vs. Ciencias - Matemáticas y Física | 1.00000 | 1.00000 | 0.976 | no |
| Ingenierías vs. Ciencias Sociales - Educación | 0.57129 | 1.00000 | inf | no |
| Ciencias Sociales - Resto vs. Filosofía y Letras | 0.19928 | 1.00000 | inf | no |
| Ciencias Sociales - Resto vs. Ciencias - Matemáticas y Física | 0.61539 | 1.00000 | 1.778 | no |
| Ciencias Sociales - Resto vs. Ciencias Sociales - Educación | 0.47619 | 1.00000 | inf | no |
| Filosofía y Letras vs. Ciencias - Matemáticas y Física | 0.53816 | 1.00000 | 0.000 | no |
| Filosofía y Letras vs. Ciencias Sociales - Educación | 1.00000 | 1.00000 | nan | no |
| Ciencias - Matemáticas y Física vs. Ciencias Sociales - Educación | 0.54232 | 1.00000 | inf | no |

> Se han realizado **21** comparaciones dos a dos; el p-valor ajustado es el que debe compararse contra α = 0.05 para decidir significancia.

## AÑO 2025

| Rama | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Ciencias - Ciencias de la Salud | 8 | 54 | 62 |
| Ciencias - Resto | 11 | 39 | 50 |
| Ingenierías | 7 | 35 | 42 |
| Ciencias Sociales - Resto | 2 | 15 | 17 |
| Filosofía y Letras | 6 | 8 | 14 |
| Ciencias - Matemáticas y Física | 7 | 18 | 25 |
| Ciencias Sociales - Educación | 0 | 12 | 12 |
| **Total** | **41** | **181** | **222** |

**Chi-cuadrado de independencia** (tabla 7×2)

- χ² = `12.0442`
- gl = `6`
- p-valor = `0.06099`
- **Conclusión:** No hay asociación significativa entre Rama y Estado (α = 0.05)

> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable, revisa los tests de Fisher de abajo.

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.07118` (método: exacto)
- **Conclusión:** No hay asociación significativa entre Rama y Estado (α = 0.05)

**Test exacto de Fisher — comparaciones dos a dos entre ramas** (corrección: Bonferroni (FWER))

| Par de ramas | p-valor crudo | p-valor ajustado | Odds Ratio | Significativo |
|---|---:|---:|---:|:---:|
| Ciencias - Ciencias de la Salud vs. Ciencias - Resto | 0.21718 | 1.00000 | 0.525 | no |
| Ciencias - Ciencias de la Salud vs. Ingenierías | 0.58523 | 1.00000 | 0.741 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias Sociales - Resto | 1.00000 | 1.00000 | 1.111 | no |
| Ciencias - Ciencias de la Salud vs. Filosofía y Letras | 0.01752 | 0.36788 | 0.198 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias - Matemáticas y Física | 0.11878 | 1.00000 | 0.381 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias Sociales - Educación | 0.33922 | 1.00000 | inf | no |
| Ciencias - Resto vs. Ingenierías | 0.60335 | 1.00000 | 1.410 | no |
| Ciencias - Resto vs. Ciencias Sociales - Resto | 0.48967 | 1.00000 | 2.115 | no |
| Ciencias - Resto vs. Filosofía y Letras | 0.17030 | 1.00000 | 0.376 | no |
| Ciencias - Resto vs. Ciencias - Matemáticas y Física | 0.57796 | 1.00000 | 0.725 | no |
| Ciencias - Resto vs. Ciencias Sociales - Educación | 0.10248 | 1.00000 | inf | no |
| Ingenierías vs. Ciencias Sociales - Resto | 1.00000 | 1.00000 | 1.500 | no |
| Ingenierías vs. Filosofía y Letras | 0.06737 | 1.00000 | 0.267 | no |
| Ingenierías vs. Ciencias - Matemáticas y Física | 0.35412 | 1.00000 | 0.514 | no |
| Ingenierías vs. Ciencias Sociales - Educación | 0.32754 | 1.00000 | inf | no |
| Ciencias Sociales - Resto vs. Filosofía y Letras | 0.09714 | 1.00000 | 0.178 | no |
| Ciencias Sociales - Resto vs. Ciencias - Matemáticas y Física | 0.27077 | 1.00000 | 0.343 | no |
| Ciencias Sociales - Resto vs. Ciencias Sociales - Educación | 0.49754 | 1.00000 | inf | no |
| Filosofía y Letras vs. Ciencias - Matemáticas y Física | 0.48164 | 1.00000 | 1.929 | no |
| Filosofía y Letras vs. Ciencias Sociales - Educación | 0.01706 | 0.35819 | inf | no |
| Ciencias - Matemáticas y Física vs. Ciencias Sociales - Educación | 0.07209 | 1.00000 | inf | no |

> Se han realizado **21** comparaciones dos a dos; el p-valor ajustado es el que debe compararse contra α = 0.05 para decidir significancia.

## AÑO 2026

| Rama | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Ciencias - Ciencias de la Salud | 9 | 43 | 52 |
| Ciencias - Resto | 11 | 33 | 44 |
| Ingenierías | 8 | 26 | 34 |
| Ciencias Sociales - Resto | 2 | 14 | 16 |
| Filosofía y Letras | 4 | 6 | 10 |
| Ciencias - Matemáticas y Física | 7 | 14 | 21 |
| Ciencias Sociales - Educación | 0 | 6 | 6 |
| **Total** | **41** | **142** | **183** |

**Chi-cuadrado de independencia** (tabla 7×2)

- χ² = `6.8312`
- gl = `6`
- p-valor = `0.33674`
- **Conclusión:** No hay asociación significativa entre Rama y Estado (α = 0.05)

> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable, revisa los tests de Fisher de abajo.

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.37210` (método: exacto)
- **Conclusión:** No hay asociación significativa entre Rama y Estado (α = 0.05)

**Test exacto de Fisher — comparaciones dos a dos entre ramas** (corrección: Bonferroni (FWER))

| Par de ramas | p-valor crudo | p-valor ajustado | Odds Ratio | Significativo |
|---|---:|---:|---:|:---:|
| Ciencias - Ciencias de la Salud vs. Ciencias - Resto | 0.45115 | 1.00000 | 0.628 | no |
| Ciencias - Ciencias de la Salud vs. Ingenierías | 0.58209 | 1.00000 | 0.680 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias Sociales - Resto | 1.00000 | 1.00000 | 1.465 | no |
| Ciencias - Ciencias de la Salud vs. Filosofía y Letras | 0.19594 | 1.00000 | 0.314 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias - Matemáticas y Física | 0.20949 | 1.00000 | 0.419 | no |
| Ciencias - Ciencias de la Salud vs. Ciencias Sociales - Educación | 0.57599 | 1.00000 | inf | no |
| Ciencias - Resto vs. Ingenierías | 1.00000 | 1.00000 | 1.083 | no |
| Ciencias - Resto vs. Ciencias Sociales - Resto | 0.48136 | 1.00000 | 2.333 | no |
| Ciencias - Resto vs. Filosofía y Letras | 0.43761 | 1.00000 | 0.500 | no |
| Ciencias - Resto vs. Ciencias - Matemáticas y Física | 0.55815 | 1.00000 | 0.667 | no |
| Ciencias - Resto vs. Ciencias Sociales - Educación | 0.31676 | 1.00000 | inf | no |
| Ingenierías vs. Ciencias Sociales - Resto | 0.46844 | 1.00000 | 2.154 | no |
| Ingenierías vs. Filosofía y Letras | 0.42179 | 1.00000 | 0.462 | no |
| Ingenierías vs. Ciencias - Matemáticas y Física | 0.53658 | 1.00000 | 0.615 | no |
| Ingenierías vs. Ciencias Sociales - Educación | 0.31797 | 1.00000 | inf | no |
| Ciencias Sociales - Resto vs. Filosofía y Letras | 0.16266 | 1.00000 | 0.214 | no |
| Ciencias Sociales - Resto vs. Ciencias - Matemáticas y Física | 0.24789 | 1.00000 | 0.286 | no |
| Ciencias Sociales - Resto vs. Ciencias Sociales - Educación | 1.00000 | 1.00000 | inf | no |
| Filosofía y Letras vs. Ciencias - Matemáticas y Física | 1.00000 | 1.00000 | 1.333 | no |
| Filosofía y Letras vs. Ciencias Sociales - Educación | 0.23352 | 1.00000 | inf | no |
| Ciencias - Matemáticas y Física vs. Ciencias Sociales - Educación | 0.15485 | 1.00000 | inf | no |

> Se han realizado **21** comparaciones dos a dos; el p-valor ajustado es el que debe compararse contra α = 0.05 para decidir significancia.
