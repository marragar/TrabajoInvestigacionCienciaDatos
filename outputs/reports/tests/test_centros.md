# Test de independencia — Centro de Investigación vs. Estado de Solicitud

_Generado el 2026-07-15 19:54_

> Nota metodológica: la tabla es de 5 centros × 2 estados. El test exacto de Fisher clásico de scipy solo admite tablas 2×2, así que se combinan tres aproximaciones: **chi-cuadrado** sobre la tabla completa, **Fisher exacto de tabla completa vía R** (rpy2), y **Fisher exacto** de cada par de centros comparados entre sí (2×2), con los p-valores corregidos por comparaciones múltiples (método: bonferroni).

## GENERAL — Todos los años

| Centro | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Universidad de Valladolid | 189 | 566 | 755 |
| Universidad de Salamanca | 197 | 546 | 743 |
| Universidad de León | 92 | 298 | 390 |
| Universidad de Burgos | 71 | 169 | 240 |
| CSIC | 54 | 65 | 119 |
| **Total** | **603** | **1644** | **2247** |

**Chi-cuadrado de independencia** (tabla 5×2)

- χ² = `25.1429`
- gl = `4`
- p-valor = `0.00005`
- **Conclusión:** Hay asociación significativa entre Centro y Estado (α = 0.05)

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.00011` (método: simulado (Monte Carlo, B=100000))
- **Conclusión:** Hay asociación significativa entre Centro y Estado (α = 0.05)

**Test exacto de Fisher — comparaciones dos a dos entre centros** (corrección: Bonferroni (FWER))

| Par de centros | p-valor crudo | p-valor ajustado | Odds Ratio | Significativo |
|---|---:|---:|---:|:---:|
| Universidad de Valladolid vs. Universidad de Salamanca | 0.51641 | 1.00000 | 0.925 | no |
| Universidad de Valladolid vs. Universidad de León | 0.61256 | 1.00000 | 1.082 | no |
| Universidad de Valladolid vs. Universidad de Burgos | 0.17721 | 1.00000 | 0.795 | no |
| Universidad de Valladolid vs. CSIC | 0.00001 | 0.00014 | 0.402 | ✅ sí |
| Universidad de Salamanca vs. Universidad de León | 0.31531 | 1.00000 | 1.169 | no |
| Universidad de Salamanca vs. Universidad de Burgos | 0.35990 | 1.00000 | 0.859 | no |
| Universidad de Salamanca vs. CSIC | 0.00005 | 0.00050 | 0.434 | ✅ sí |
| Universidad de León vs. Universidad de Burgos | 0.11115 | 1.00000 | 0.735 | no |
| Universidad de León vs. CSIC | 0.00001 | 0.00009 | 0.372 | ✅ sí |
| Universidad de Burgos vs. CSIC | 0.00461 | 0.04606 | 0.506 | ✅ sí |

> Se han realizado **10** comparaciones dos a dos; el p-valor ajustado es el que debe compararse contra α = 0.05 para decidir significancia.

## AÑO 2010

| Centro | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Universidad de Valladolid | 34 | 59 | 93 |
| Universidad de Salamanca | 37 | 66 | 103 |
| Universidad de León | 24 | 44 | 68 |
| Universidad de Burgos | 6 | 27 | 33 |
| CSIC | 5 | 3 | 8 |
| **Total** | **106** | **199** | **305** |

**Chi-cuadrado de independencia** (tabla 5×2)

- χ² = `6.9172`
- gl = `4`
- p-valor = `0.14033`
- **Conclusión:** No hay asociación significativa entre Centro y Estado (α = 0.05)

> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable, revisa los tests de Fisher de abajo.

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.13315` (método: exacto)
- **Conclusión:** No hay asociación significativa entre Centro y Estado (α = 0.05)

**Test exacto de Fisher — comparaciones dos a dos entre centros** (corrección: Bonferroni (FWER))

| Par de centros | p-valor crudo | p-valor ajustado | Odds Ratio | Significativo |
|---|---:|---:|---:|:---:|
| Universidad de Valladolid vs. Universidad de Salamanca | 1.00000 | 1.00000 | 1.028 | no |
| Universidad de Valladolid vs. Universidad de León | 1.00000 | 1.00000 | 1.056 | no |
| Universidad de Valladolid vs. Universidad de Burgos | 0.08030 | 0.80305 | 2.593 | no |
| Universidad de Valladolid vs. CSIC | 0.25493 | 1.00000 | 0.346 | no |
| Universidad de Salamanca vs. Universidad de León | 1.00000 | 1.00000 | 1.028 | no |
| Universidad de Salamanca vs. Universidad de Burgos | 0.08402 | 0.84019 | 2.523 | no |
| Universidad de Salamanca vs. CSIC | 0.15224 | 1.00000 | 0.336 | no |
| Universidad de León vs. Universidad de Burgos | 0.10455 | 1.00000 | 2.455 | no |
| Universidad de León vs. CSIC | 0.24688 | 1.00000 | 0.327 | no |
| Universidad de Burgos vs. CSIC | 0.02184 | 0.21840 | 0.133 | no |

> Se han realizado **10** comparaciones dos a dos; el p-valor ajustado es el que debe compararse contra α = 0.05 para decidir significancia.

## AÑO 2014

| Centro | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Universidad de Valladolid | 20 | 100 | 120 |
| Universidad de Salamanca | 20 | 102 | 122 |
| Universidad de León | 6 | 36 | 42 |
| Universidad de Burgos | 5 | 27 | 32 |
| CSIC | 6 | 12 | 18 |
| **Total** | **57** | **277** | **334** |

**Chi-cuadrado de independencia** (tabla 5×2)

- χ² = `3.6943`
- gl = `4`
- p-valor = `0.44896`
- **Conclusión:** No hay asociación significativa entre Centro y Estado (α = 0.05)

> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable, revisa los tests de Fisher de abajo.

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.48830` (método: exacto)
- **Conclusión:** No hay asociación significativa entre Centro y Estado (α = 0.05)

**Test exacto de Fisher — comparaciones dos a dos entre centros** (corrección: Bonferroni (FWER))

| Par de centros | p-valor crudo | p-valor ajustado | Odds Ratio | Significativo |
|---|---:|---:|---:|:---:|
| Universidad de Valladolid vs. Universidad de Salamanca | 1.00000 | 1.00000 | 1.020 | no |
| Universidad de Valladolid vs. Universidad de León | 0.81112 | 1.00000 | 1.200 | no |
| Universidad de Valladolid vs. Universidad de Burgos | 1.00000 | 1.00000 | 1.080 | no |
| Universidad de Valladolid vs. CSIC | 0.10860 | 1.00000 | 0.400 | no |
| Universidad de Salamanca vs. Universidad de León | 1.00000 | 1.00000 | 1.176 | no |
| Universidad de Salamanca vs. Universidad de Burgos | 1.00000 | 1.00000 | 1.059 | no |
| Universidad de Salamanca vs. CSIC | 0.10451 | 1.00000 | 0.392 | no |
| Universidad de León vs. Universidad de Burgos | 1.00000 | 1.00000 | 0.900 | no |
| Universidad de León vs. CSIC | 0.15583 | 1.00000 | 0.333 | no |
| Universidad de Burgos vs. CSIC | 0.17175 | 1.00000 | 0.370 | no |

> Se han realizado **10** comparaciones dos a dos; el p-valor ajustado es el que debe compararse contra α = 0.05 para decidir significancia.

## AÑO 2015

| Centro | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Universidad de Valladolid | 22 | 103 | 125 |
| Universidad de Salamanca | 16 | 103 | 119 |
| Universidad de León | 12 | 55 | 67 |
| Universidad de Burgos | 4 | 20 | 24 |
| CSIC | 7 | 11 | 18 |
| **Total** | **61** | **292** | **353** |

**Chi-cuadrado de independencia** (tabla 5×2)

- χ² = `7.1380`
- gl = `4`
- p-valor = `0.12877`
- **Conclusión:** No hay asociación significativa entre Centro y Estado (α = 0.05)

> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable, revisa los tests de Fisher de abajo.

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.16023` (método: exacto)
- **Conclusión:** No hay asociación significativa entre Centro y Estado (α = 0.05)

**Test exacto de Fisher — comparaciones dos a dos entre centros** (corrección: Bonferroni (FWER))

| Par de centros | p-valor crudo | p-valor ajustado | Odds Ratio | Significativo |
|---|---:|---:|---:|:---:|
| Universidad de Valladolid vs. Universidad de Salamanca | 0.38403 | 1.00000 | 1.375 | no |
| Universidad de Valladolid vs. Universidad de León | 1.00000 | 1.00000 | 0.979 | no |
| Universidad de Valladolid vs. Universidad de Burgos | 1.00000 | 1.00000 | 1.068 | no |
| Universidad de Valladolid vs. CSIC | 0.05549 | 0.55495 | 0.336 | no |
| Universidad de Salamanca vs. Universidad de León | 0.52211 | 1.00000 | 0.712 | no |
| Universidad de Salamanca vs. Universidad de Burgos | 0.74704 | 1.00000 | 0.777 | no |
| Universidad de Salamanca vs. CSIC | 0.01403 | 0.14033 | 0.244 | no |
| Universidad de León vs. Universidad de Burgos | 1.00000 | 1.00000 | 1.091 | no |
| Universidad de León vs. CSIC | 0.10670 | 1.00000 | 0.343 | no |
| Universidad de Burgos vs. CSIC | 0.15864 | 1.00000 | 0.314 | no |

> Se han realizado **10** comparaciones dos a dos; el p-valor ajustado es el que debe compararse contra α = 0.05 para decidir significancia.

## AÑO 2016

| Centro | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Universidad de Valladolid | 16 | 17 | 33 |
| Universidad de Salamanca | 19 | 27 | 46 |
| Universidad de León | 5 | 13 | 18 |
| Universidad de Burgos | 14 | 3 | 17 |
| CSIC | 7 | 3 | 10 |
| **Total** | **61** | **63** | **124** |

**Chi-cuadrado de independencia** (tabla 5×2)

- χ² = `13.6661`
- gl = `4`
- p-valor = `0.00844`
- **Conclusión:** Hay asociación significativa entre Centro y Estado (α = 0.05)

> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable, revisa los tests de Fisher de abajo.

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.00764` (método: exacto)
- **Conclusión:** Hay asociación significativa entre Centro y Estado (α = 0.05)

**Test exacto de Fisher — comparaciones dos a dos entre centros** (corrección: Bonferroni (FWER))

| Par de centros | p-valor crudo | p-valor ajustado | Odds Ratio | Significativo |
|---|---:|---:|---:|:---:|
| Universidad de Valladolid vs. Universidad de Salamanca | 0.64684 | 1.00000 | 1.337 | no |
| Universidad de Valladolid vs. Universidad de León | 0.23427 | 1.00000 | 2.447 | no |
| Universidad de Valladolid vs. Universidad de Burgos | 0.03232 | 0.32319 | 0.202 | no |
| Universidad de Valladolid vs. CSIC | 0.29381 | 1.00000 | 0.403 | no |
| Universidad de Salamanca vs. Universidad de León | 0.39597 | 1.00000 | 1.830 | no |
| Universidad de Salamanca vs. Universidad de Burgos | 0.00463 | 0.04632 | 0.151 | ✅ sí |
| Universidad de Salamanca vs. CSIC | 0.16158 | 1.00000 | 0.302 | no |
| Universidad de León vs. Universidad de Burgos | 0.00205 | 0.02046 | 0.082 | ✅ sí |
| Universidad de León vs. CSIC | 0.04967 | 0.49668 | 0.165 | no |
| Universidad de Burgos vs. CSIC | 0.63819 | 1.00000 | 2.000 | no |

> Se han realizado **10** comparaciones dos a dos; el p-valor ajustado es el que debe compararse contra α = 0.05 para decidir significancia.

## AÑO 2017

| Centro | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Universidad de Valladolid | 20 | 13 | 33 |
| Universidad de Salamanca | 16 | 28 | 44 |
| Universidad de León | 13 | 9 | 22 |
| Universidad de Burgos | 3 | 1 | 4 |
| CSIC | 5 | 5 | 10 |
| **Total** | **57** | **56** | **113** |

**Chi-cuadrado de independencia** (tabla 5×2)

- χ² = `6.4765`
- gl = `4`
- p-valor = `0.16628`
- **Conclusión:** No hay asociación significativa entre Centro y Estado (α = 0.05)

> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable, revisa los tests de Fisher de abajo.

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.16016` (método: exacto)
- **Conclusión:** No hay asociación significativa entre Centro y Estado (α = 0.05)

**Test exacto de Fisher — comparaciones dos a dos entre centros** (corrección: Bonferroni (FWER))

| Par de centros | p-valor crudo | p-valor ajustado | Odds Ratio | Significativo |
|---|---:|---:|---:|:---:|
| Universidad de Valladolid vs. Universidad de Salamanca | 0.04089 | 0.40892 | 2.692 | no |
| Universidad de Valladolid vs. Universidad de León | 1.00000 | 1.00000 | 1.065 | no |
| Universidad de Valladolid vs. Universidad de Burgos | 1.00000 | 1.00000 | 0.513 | no |
| Universidad de Valladolid vs. CSIC | 0.71735 | 1.00000 | 1.538 | no |
| Universidad de Salamanca vs. Universidad de León | 0.11480 | 1.00000 | 0.396 | no |
| Universidad de Salamanca vs. Universidad de Burgos | 0.28640 | 1.00000 | 0.190 | no |
| Universidad de Salamanca vs. CSIC | 0.48557 | 1.00000 | 0.571 | no |
| Universidad de León vs. Universidad de Burgos | 1.00000 | 1.00000 | 0.481 | no |
| Universidad de León vs. CSIC | 0.71195 | 1.00000 | 1.444 | no |
| Universidad de Burgos vs. CSIC | 0.58042 | 1.00000 | 3.000 | no |

> Se han realizado **10** comparaciones dos a dos; el p-valor ajustado es el que debe compararse contra α = 0.05 para decidir significancia.

## AÑO 2019

| Centro | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Universidad de Valladolid | 18 | 21 | 39 |
| Universidad de Salamanca | 12 | 41 | 53 |
| Universidad de León | 6 | 16 | 22 |
| Universidad de Burgos | 10 | 13 | 23 |
| CSIC | 3 | 4 | 7 |
| **Total** | **49** | **95** | **144** |

**Chi-cuadrado de independencia** (tabla 5×2)

- χ² = `7.2207`
- gl = `4`
- p-valor = `0.12467`
- **Conclusión:** No hay asociación significativa entre Centro y Estado (α = 0.05)

> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable, revisa los tests de Fisher de abajo.

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.11131` (método: exacto)
- **Conclusión:** No hay asociación significativa entre Centro y Estado (α = 0.05)

**Test exacto de Fisher — comparaciones dos a dos entre centros** (corrección: Bonferroni (FWER))

| Par de centros | p-valor crudo | p-valor ajustado | Odds Ratio | Significativo |
|---|---:|---:|---:|:---:|
| Universidad de Valladolid vs. Universidad de Salamanca | 0.02436 | 0.24363 | 2.929 | no |
| Universidad de Valladolid vs. Universidad de León | 0.17981 | 1.00000 | 2.286 | no |
| Universidad de Valladolid vs. Universidad de Burgos | 1.00000 | 1.00000 | 1.114 | no |
| Universidad de Valladolid vs. CSIC | 1.00000 | 1.00000 | 1.143 | no |
| Universidad de Salamanca vs. Universidad de León | 0.76827 | 1.00000 | 0.780 | no |
| Universidad de Salamanca vs. Universidad de Burgos | 0.09775 | 0.97746 | 0.380 | no |
| Universidad de Salamanca vs. CSIC | 0.35149 | 1.00000 | 0.390 | no |
| Universidad de León vs. Universidad de Burgos | 0.35341 | 1.00000 | 0.487 | no |
| Universidad de León vs. CSIC | 0.64239 | 1.00000 | 0.500 | no |
| Universidad de Burgos vs. CSIC | 1.00000 | 1.00000 | 1.026 | no |

> Se han realizado **10** comparaciones dos a dos; el p-valor ajustado es el que debe compararse contra α = 0.05 para decidir significancia.

## AÑO 2021

| Centro | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Universidad de Valladolid | 24 | 64 | 88 |
| Universidad de Salamanca | 35 | 38 | 73 |
| Universidad de León | 14 | 30 | 44 |
| Universidad de Burgos | 11 | 18 | 29 |
| CSIC | 12 | 4 | 16 |
| **Total** | **96** | **154** | **250** |

**Chi-cuadrado de independencia** (tabla 5×2)

- χ² = `17.2874`
- gl = `4`
- p-valor = `0.00170`
- **Conclusión:** Hay asociación significativa entre Centro y Estado (α = 0.05)

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.00182` (método: exacto)
- **Conclusión:** Hay asociación significativa entre Centro y Estado (α = 0.05)

**Test exacto de Fisher — comparaciones dos a dos entre centros** (corrección: Bonferroni (FWER))

| Par de centros | p-valor crudo | p-valor ajustado | Odds Ratio | Significativo |
|---|---:|---:|---:|:---:|
| Universidad de Valladolid vs. Universidad de Salamanca | 0.00856 | 0.08561 | 0.407 | no |
| Universidad de Valladolid vs. Universidad de León | 0.68399 | 1.00000 | 0.804 | no |
| Universidad de Valladolid vs. Universidad de Burgos | 0.35001 | 1.00000 | 0.614 | no |
| Universidad de Valladolid vs. CSIC | 0.00043 | 0.00431 | 0.125 | ✅ sí |
| Universidad de Salamanca vs. Universidad de León | 0.12144 | 1.00000 | 1.974 | no |
| Universidad de Salamanca vs. Universidad de Burgos | 0.38662 | 1.00000 | 1.507 | no |
| Universidad de Salamanca vs. CSIC | 0.05801 | 0.58009 | 0.307 | no |
| Universidad de León vs. Universidad de Burgos | 0.62186 | 1.00000 | 0.764 | no |
| Universidad de León vs. CSIC | 0.00379 | 0.03785 | 0.156 | ✅ sí |
| Universidad de Burgos vs. CSIC | 0.02868 | 0.28678 | 0.204 | no |

> Se han realizado **10** comparaciones dos a dos; el p-valor ajustado es el que debe compararse contra α = 0.05 para decidir significancia.

## AÑO 2024

| Centro | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Universidad de Valladolid | 4 | 69 | 73 |
| Universidad de Salamanca | 11 | 59 | 70 |
| Universidad de León | 6 | 38 | 44 |
| Universidad de Burgos | 9 | 20 | 29 |
| CSIC | 6 | 7 | 13 |
| **Total** | **36** | **193** | **229** |

**Chi-cuadrado de independencia** (tabla 5×2)

- χ² = `20.1437`
- gl = `4`
- p-valor = `0.00047`
- **Conclusión:** Hay asociación significativa entre Centro y Estado (α = 0.05)

> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable, revisa los tests de Fisher de abajo.

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.00057` (método: exacto)
- **Conclusión:** Hay asociación significativa entre Centro y Estado (α = 0.05)

**Test exacto de Fisher — comparaciones dos a dos entre centros** (corrección: Bonferroni (FWER))

| Par de centros | p-valor crudo | p-valor ajustado | Odds Ratio | Significativo |
|---|---:|---:|---:|:---:|
| Universidad de Valladolid vs. Universidad de Salamanca | 0.05755 | 0.57546 | 0.311 | no |
| Universidad de Valladolid vs. Universidad de León | 0.17355 | 1.00000 | 0.367 | no |
| Universidad de Valladolid vs. Universidad de Burgos | 0.00131 | 0.01309 | 0.129 | ✅ sí |
| Universidad de Valladolid vs. CSIC | 0.00056 | 0.00559 | 0.068 | ✅ sí |
| Universidad de Salamanca vs. Universidad de León | 1.00000 | 1.00000 | 1.181 | no |
| Universidad de Salamanca vs. Universidad de Burgos | 0.10231 | 1.00000 | 0.414 | no |
| Universidad de Salamanca vs. CSIC | 0.02201 | 0.22008 | 0.218 | no |
| Universidad de León vs. Universidad de Burgos | 0.08426 | 0.84263 | 0.351 | no |
| Universidad de León vs. CSIC | 0.02002 | 0.20022 | 0.184 | no |
| Universidad de Burgos vs. CSIC | 0.48805 | 1.00000 | 0.525 | no |

> Se han realizado **10** comparaciones dos a dos; el p-valor ajustado es el que debe compararse contra α = 0.05 para decidir significancia.

## AÑO 2025

| Centro | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Universidad de Valladolid | 13 | 65 | 78 |
| Universidad de Salamanca | 19 | 53 | 72 |
| Universidad de León | 3 | 30 | 33 |
| Universidad de Burgos | 5 | 23 | 28 |
| CSIC | 0 | 8 | 8 |
| **Total** | **40** | **179** | **219** |

**Chi-cuadrado de independencia** (tabla 5×2)

- χ² = `6.9678`
- gl = `4`
- p-valor = `0.13760`
- **Conclusión:** No hay asociación significativa entre Centro y Estado (α = 0.05)

> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable, revisa los tests de Fisher de abajo.

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.17166` (método: exacto)
- **Conclusión:** No hay asociación significativa entre Centro y Estado (α = 0.05)

**Test exacto de Fisher — comparaciones dos a dos entre centros** (corrección: Bonferroni (FWER))

| Par de centros | p-valor crudo | p-valor ajustado | Odds Ratio | Significativo |
|---|---:|---:|---:|:---:|
| Universidad de Valladolid vs. Universidad de Salamanca | 0.16624 | 1.00000 | 0.558 | no |
| Universidad de Valladolid vs. Universidad de León | 0.38493 | 1.00000 | 2.000 | no |
| Universidad de Valladolid vs. Universidad de Burgos | 1.00000 | 1.00000 | 0.920 | no |
| Universidad de Valladolid vs. CSIC | 0.60080 | 1.00000 | inf | no |
| Universidad de Salamanca vs. Universidad de León | 0.06849 | 0.68487 | 3.585 | no |
| Universidad de Salamanca vs. Universidad de Burgos | 0.44271 | 1.00000 | 1.649 | no |
| Universidad de Salamanca vs. CSIC | 0.18763 | 1.00000 | inf | no |
| Universidad de León vs. Universidad de Burgos | 0.45146 | 1.00000 | 0.460 | no |
| Universidad de León vs. CSIC | 1.00000 | 1.00000 | inf | no |
| Universidad de Burgos vs. CSIC | 0.56551 | 1.00000 | inf | no |

> Se han realizado **10** comparaciones dos a dos; el p-valor ajustado es el que debe compararse contra α = 0.05 para decidir significancia.

## AÑO 2026

| Centro | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Universidad de Valladolid | 18 | 55 | 73 |
| Universidad de Salamanca | 12 | 29 | 41 |
| Universidad de León | 3 | 27 | 30 |
| Universidad de Burgos | 4 | 17 | 21 |
| CSIC | 3 | 8 | 11 |
| **Total** | **40** | **136** | **176** |

**Chi-cuadrado de independencia** (tabla 5×2)

- χ² = `4.2121`
- gl = `4`
- p-valor = `0.37806`
- **Conclusión:** No hay asociación significativa entre Centro y Estado (α = 0.05)

> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable, revisa los tests de Fisher de abajo.

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.34736` (método: exacto)
- **Conclusión:** No hay asociación significativa entre Centro y Estado (α = 0.05)

**Test exacto de Fisher — comparaciones dos a dos entre centros** (corrección: Bonferroni (FWER))

| Par de centros | p-valor crudo | p-valor ajustado | Odds Ratio | Significativo |
|---|---:|---:|---:|:---:|
| Universidad de Valladolid vs. Universidad de Salamanca | 0.65963 | 1.00000 | 0.791 | no |
| Universidad de Valladolid vs. Universidad de León | 0.11223 | 1.00000 | 2.945 | no |
| Universidad de Valladolid vs. Universidad de Burgos | 0.77233 | 1.00000 | 1.391 | no |
| Universidad de Valladolid vs. CSIC | 1.00000 | 1.00000 | 0.873 | no |
| Universidad de Salamanca vs. Universidad de León | 0.07645 | 0.76446 | 3.724 | no |
| Universidad de Salamanca vs. Universidad de Burgos | 0.54223 | 1.00000 | 1.759 | no |
| Universidad de Salamanca vs. CSIC | 1.00000 | 1.00000 | 1.103 | no |
| Universidad de León vs. Universidad de Burgos | 0.42669 | 1.00000 | 0.472 | no |
| Universidad de León vs. CSIC | 0.31615 | 1.00000 | 0.296 | no |
| Universidad de Burgos vs. CSIC | 0.66749 | 1.00000 | 0.627 | no |

> Se han realizado **10** comparaciones dos a dos; el p-valor ajustado es el que debe compararse contra α = 0.05 para decidir significancia.
