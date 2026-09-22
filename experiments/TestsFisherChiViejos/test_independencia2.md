# Test de independencia — Centro de Investigación vs. Estado de Solicitud

_Generado el 2026-07-09 15:57_

> Nota metodológica: la tabla es de 5 centros × 2 estados. El test exacto de Fisher clásico de scipy solo admite tablas 2×2, así que se combinan tres aproximaciones: **chi-cuadrado** sobre la tabla completa, **Fisher exacto de tabla completa vía R** (rpy2), y **Fisher exacto** de cada centro comparado contra el resto agrupado (2×2).

## GENERAL — Todos los años

| Centro | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Universidad de Valladolid | 59 | 253 | 312 |
| Universidad de Salamanca | 77 | 179 | 256 |
| Universidad de León | 26 | 125 | 151 |
| Universidad de Burgos | 29 | 78 | 107 |
| CSIC | 21 | 27 | 48 |
| **Total** | **212** | **662** | **874** |

**Chi-cuadrado de independencia** (tabla 5×2)

- χ² = `24.0467`
- gl = `4`
- p-valor = `0.00008`
- **Conclusión:** Hay asociación significativa entre Centro y Estado (α = 0.05)

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.00019` (método: simulado (Monte Carlo, B=100000))
- **Conclusión:** Hay asociación significativa entre Centro y Estado (α = 0.05)

**Test exacto de Fisher — cada centro vs. el resto**

| Centro | p-valor | Odds Ratio | Significativo |
|---|---:|---:|:---:|
| Universidad de Valladolid | 0.00651 | 0.623 | ✅ sí |
| Universidad de Salamanca | 0.01182 | 1.539 | ✅ sí |
| Universidad de León | 0.02821 | 0.601 | ✅ sí |
| Universidad de Burgos | 0.47103 | 1.186 | no |
| CSIC | 0.00268 | 2.586 | ✅ sí |

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

**Test exacto de Fisher — cada centro vs. el resto**

| Centro | p-valor | Odds Ratio | Significativo |
|---|---:|---:|:---:|
| Universidad de Valladolid | 0.00954 | 0.469 | ✅ sí |
| Universidad de Salamanca | 0.06257 | 1.752 | no |
| Universidad de León | 0.39409 | 0.706 | no |
| Universidad de Burgos | 1.00000 | 0.978 | no |
| CSIC | 0.00278 | 5.357 | ✅ sí |

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

**Test exacto de Fisher — cada centro vs. el resto**

| Centro | p-valor | Odds Ratio | Significativo |
|---|---:|---:|:---:|
| Universidad de Valladolid | 0.00313 | 0.225 | ✅ sí |
| Universidad de Salamanca | 1.00000 | 0.999 | no |
| Universidad de León | 0.81931 | 0.816 | no |
| Universidad de Burgos | 0.02581 | 2.883 | ✅ sí |
| CSIC | 0.00754 | 5.314 | ✅ sí |

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

**Test exacto de Fisher — cada centro vs. el resto**

| Centro | p-valor | Odds Ratio | Significativo |
|---|---:|---:|:---:|
| Universidad de Valladolid | 0.71732 | 0.844 | no |
| Universidad de Salamanca | 0.03989 | 2.151 | ✅ sí |
| Universidad de León | 0.21919 | 0.403 | no |
| Universidad de Burgos | 1.00000 | 0.969 | no |
| CSIC | 0.35616 | 0.000 | no |

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

**Test exacto de Fisher — cada centro vs. el resto**

| Centro | p-valor | Odds Ratio | Significativo |
|---|---:|---:|:---:|
| Universidad de Valladolid | 0.71540 | 1.205 | no |
| Universidad de Salamanca | 0.28882 | 1.581 | no |
| Universidad de León | 0.09270 | 0.327 | no |
| Universidad de Burgos | 0.78732 | 0.778 | no |
| CSIC | 0.71440 | 1.297 | no |
