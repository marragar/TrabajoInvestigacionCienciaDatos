# Test de independencia — Rama(Departamento) vs. Estado de Solicitud

_Generado el 2026-07-09 15:58_

> Nota metodológica: la tabla es de 7 ramas × 2 estados. El test exacto de Fisher clásico de scipy solo admite tablas 2×2, así que se combinan tres aproximaciones: **chi-cuadrado** sobre la tabla completa, **Fisher exacto de tabla completa vía R** (rpy2), y **Fisher exacto** de cada rama comparada contra el resto agrupado (2×2).

## GENERAL — Todos los años

| Rama | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Ciencias - Ciencias de la Salud | 66 | 195 | 261 |
| Ciencias - Resto | 53 | 147 | 200 |
| Ingenierías | 35 | 143 | 178 |
| Ciencias Sociales - Resto | 18 | 61 | 79 |
| Filosofía y Letras | 16 | 38 | 54 |
| Ciencias - Matemáticas y Física | 30 | 63 | 93 |
| Ciencias Sociales - Educación | 0 | 40 | 40 |
| **Total** | **218** | **687** | **905** |

**Chi-cuadrado de independencia** (tabla 7×2)

- χ² = `19.8153`
- gl = `6`
- p-valor = `0.00299`
- **Conclusión:** Hay asociación significativa entre Rama y Estado (α = 0.05)

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.00026` (método: simulado (Monte Carlo, B=100000))
- **Conclusión:** Hay asociación significativa entre Rama y Estado (α = 0.05)

**Test exacto de Fisher — cada rama vs. el resto**

| Rama | p-valor | Odds Ratio | Significativo |
|---|---:|---:|:---:|
| Ciencias - Ciencias de la Salud | 0.60713 | 1.096 | no |
| Ciencias - Resto | 0.39915 | 1.180 | no |
| Ingenierías | 0.14229 | 0.728 | no |
| Ciencias Sociales - Resto | 0.89060 | 0.924 | no |
| Filosofía y Letras | 0.32704 | 1.353 | no |
| Ciencias - Matemáticas y Física | 0.05554 | 1.581 | no |
| Ciencias Sociales - Educación | 0.00002 | 0.000 | ✅ sí |

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

- p-valor = `0.00358` (método: simulado (Monte Carlo, B=100000))
- **Conclusión:** Hay asociación significativa entre Rama y Estado (α = 0.05)

**Test exacto de Fisher — cada rama vs. el resto**

| Rama | p-valor | Odds Ratio | Significativo |
|---|---:|---:|:---:|
| Ciencias - Ciencias de la Salud | 0.26048 | 1.407 | no |
| Ciencias - Resto | 0.41298 | 1.329 | no |
| Ingenierías | 0.06215 | 0.521 | no |
| Ciencias Sociales - Resto | 0.70989 | 0.824 | no |
| Filosofía y Letras | 1.00000 | 0.876 | no |
| Ciencias - Matemáticas y Física | 0.01518 | 3.309 | ✅ sí |
| Ciencias Sociales - Educación | 0.00785 | 0.000 | ✅ sí |

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

**Test exacto de Fisher — cada rama vs. el resto**

| Rama | p-valor | Odds Ratio | Significativo |
|---|---:|---:|:---:|
| Ciencias - Ciencias de la Salud | 0.05057 | 2.086 | no |
| Ciencias - Resto | 0.67375 | 1.234 | no |
| Ingenierías | 0.49346 | 0.633 | no |
| Ciencias Sociales - Resto | 0.67459 | 1.261 | no |
| Filosofía y Letras | 0.22659 | 0.000 | no |
| Ciencias - Matemáticas y Física | 0.77588 | 0.674 | no |
| Ciencias Sociales - Educación | 0.37953 | 0.000 | no |

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

**Test exacto de Fisher — cada rama vs. el resto**

| Rama | p-valor | Odds Ratio | Significativo |
|---|---:|---:|:---:|
| Ciencias - Ciencias de la Salud | 0.24725 | 0.570 | no |
| Ciencias - Resto | 0.53460 | 1.335 | no |
| Ingenierías | 0.82837 | 0.859 | no |
| Ciencias Sociales - Resto | 0.74483 | 0.568 | no |
| Filosofía y Letras | 0.02625 | 3.707 | ✅ sí |
| Ciencias - Matemáticas y Física | 0.27023 | 1.864 | no |
| Ciencias Sociales - Educación | 0.12940 | 0.000 | no |

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

**Test exacto de Fisher — cada rama vs. el resto**

| Rama | p-valor | Odds Ratio | Significativo |
|---|---:|---:|:---:|
| Ciencias - Ciencias de la Salud | 0.33233 | 0.648 | no |
| Ciencias - Resto | 0.67966 | 1.211 | no |
| Ingenierías | 0.82335 | 1.082 | no |
| Ciencias Sociales - Resto | 0.53015 | 0.469 | no |
| Filosofía y Letras | 0.23464 | 2.450 | no |
| Ciencias - Matemáticas y Física | 0.26326 | 1.882 | no |
| Ciencias Sociales - Educación | 0.34019 | 0.000 | no |
