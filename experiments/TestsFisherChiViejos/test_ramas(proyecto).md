# Test de independencia — Rama(Proyecto) vs. Estado de Solicitud

_Generado el 2026-07-07 23:15_

> Nota metodológica: la tabla es de 7 ramas × 2 estados, por lo que el test exacto de Fisher clásico (solo válido en tablas 2×2) no puede aplicarse directamente a la tabla completa. Por eso se combina un **chi-cuadrado de independencia** sobre la tabla completa con un **Fisher exacto** de cada rama comparada contra el resto agrupado.

## GENERAL — Todos los años

| Rama | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Ciencias - Ciencias de la Salud | 93 | 238 | 331 |
| Ciencias - Resto | 48 | 159 | 207 |
| Ingenierías | 24 | 109 | 133 |
| Ciencias Sociales - Resto | 15 | 65 | 80 |
| Filosofía y Letras | 17 | 41 | 58 |
| Ciencias - Matemáticas y Física | 19 | 38 | 57 |
| Ciencias Sociales - Educación | 2 | 37 | 39 |
| **Total** | **218** | **687** | **905** |

**Chi-cuadrado de independencia** (tabla 7×2)

- χ² = `18.0993`
- gl = `6`
- p-valor = `0.00599`
- **Conclusión:** Hay asociación significativa entre Rama y Estado (α = 0.05)



**Test exacto de Fisher — cada rama vs. el resto**

| Rama | p-valor | Odds Ratio | Significativo |
|---|---:|---:|:---:|
| Ciencias - Ciencias de la Salud | 0.03589 | 1.404 | ✅ sí |
| Ciencias - Resto | 0.78161 | 0.938 | no |
| Ingenierías | 0.07993 | 0.656 | no |
| Ciencias Sociales - Resto | 0.27494 | 0.707 | no |
| Filosofía y Letras | 0.34246 | 1.333 | no |
| Ciencias - Matemáticas y Física | 0.10862 | 1.631 | no |
| Ciencias Sociales - Educación | 0.00331 | 0.163 | ✅ sí |

## AÑO 2021

| Rama | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Ciencias - Ciencias de la Salud | 49 | 52 | 101 |
| Ciencias - Resto | 20 | 29 | 49 |
| Ingenierías | 10 | 31 | 41 |
| Ciencias Sociales - Resto | 8 | 25 | 33 |
| Filosofía y Letras | 5 | 13 | 18 |
| Ciencias - Matemáticas y Física | 8 | 3 | 11 |
| Ciencias Sociales - Educación | 0 | 9 | 9 |
| **Total** | **100** | **162** | **262** |

**Chi-cuadrado de independencia** (tabla 7×2)

- χ² = `22.6826`
- gl = `6`
- p-valor = `0.00091`
- **Conclusión:** Hay asociación significativa entre Rama y Estado (α = 0.05)

> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable, revisa los tests de Fisher por rama abajo.

**Test exacto de Fisher — cada rama vs. el resto**

| Rama | p-valor | Odds Ratio | Significativo |
|---|---:|---:|:---:|
| Ciencias - Ciencias de la Salud | 0.00881 | 2.032 | ✅ sí |
| Ciencias - Resto | 0.74477 | 1.147 | no |
| Ingenierías | 0.05475 | 0.470 | no |
| Ciencias Sociales - Resto | 0.08698 | 0.477 | no |
| Filosofía y Letras | 0.45392 | 0.603 | no |
| Ciencias - Matemáticas y Física | 0.02385 | 4.609 | ✅ sí |
| Ciencias Sociales - Educación | 0.01440 | 0.000 | ✅ sí |

## AÑO 2024

| Rama | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Ciencias - Ciencias de la Salud | 17 | 67 | 84 |
| Ciencias - Resto | 12 | 56 | 68 |
| Ingenierías | 2 | 30 | 32 |
| Ciencias Sociales - Resto | 1 | 11 | 12 |
| Filosofía y Letras | 1 | 14 | 15 |
| Ciencias - Matemáticas y Física | 2 | 15 | 17 |
| Ciencias Sociales - Educación | 1 | 9 | 10 |
| **Total** | **36** | **202** | **238** |

**Chi-cuadrado de independencia** (tabla 7×2)

- χ² = `5.6320`
- gl = `6`
- p-valor = `0.46565`
- **Conclusión:** No hay asociación significativa entre Rama y Estado (α = 0.05)

> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable, revisa los tests de Fisher por rama abajo.

**Test exacto de Fisher — cada rama vs. el resto**

| Rama | p-valor | Odds Ratio | Significativo |
|---|---:|---:|:---:|
| Ciencias - Ciencias de la Salud | 0.12970 | 1.803 | no |
| Ciencias - Resto | 0.54883 | 1.304 | no |
| Ingenierías | 0.18502 | 0.337 | no |
| Ciencias Sociales - Resto | 0.69896 | 0.496 | no |
| Filosofía y Letras | 0.47985 | 0.384 | no |
| Ciencias - Matemáticas y Física | 1.00000 | 0.733 | no |
| Ciencias Sociales - Educación | 1.00000 | 0.613 | no |

## AÑO 2025

| Rama | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Ciencias - Ciencias de la Salud | 15 | 68 | 83 |
| Ciencias - Resto | 4 | 37 | 41 |
| Ingenierías | 6 | 26 | 32 |
| Ciencias Sociales - Resto | 3 | 15 | 18 |
| Filosofía y Letras | 6 | 10 | 16 |
| Ciencias - Matemáticas y Física | 6 | 12 | 18 |
| Ciencias Sociales - Educación | 1 | 13 | 14 |
| **Total** | **41** | **181** | **222** |

**Chi-cuadrado de independencia** (tabla 7×2)

- χ² = `9.7986`
- gl = `6`
- p-valor = `0.13339`
- **Conclusión:** No hay asociación significativa entre Rama y Estado (α = 0.05)

> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable, revisa los tests de Fisher por rama abajo.

**Test exacto de Fisher — cada rama vs. el resto**

| Rama | p-valor | Odds Ratio | Significativo |
|---|---:|---:|:---:|
| Ciencias - Ciencias de la Salud | 1.00000 | 0.959 | no |
| Ciencias - Resto | 0.12437 | 0.421 | no |
| Ingenierías | 1.00000 | 1.022 | no |
| Ciencias Sociales - Resto | 1.00000 | 0.874 | no |
| Filosofía y Letras | 0.08541 | 2.931 | no |
| Ciencias - Matemáticas y Física | 0.11076 | 2.414 | no |
| Ciencias Sociales - Educación | 0.47547 | 0.323 | no |

## AÑO 2026

| Rama | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Ciencias - Ciencias de la Salud | 12 | 51 | 63 |
| Ciencias - Resto | 12 | 37 | 49 |
| Ingenierías | 6 | 22 | 28 |
| Ciencias Sociales - Resto | 3 | 14 | 17 |
| Filosofía y Letras | 5 | 4 | 9 |
| Ciencias - Matemáticas y Física | 3 | 8 | 11 |
| Ciencias Sociales - Educación | 0 | 6 | 6 |
| **Total** | **41** | **142** | **183** |

**Chi-cuadrado de independencia** (tabla 7×2)

- χ² = `8.3394`
- gl = `6`
- p-valor = `0.21428`
- **Conclusión:** No hay asociación significativa entre Rama y Estado (α = 0.05)

> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable, revisa los tests de Fisher por rama abajo.

**Test exacto de Fisher — cada rama vs. el resto**

| Rama | p-valor | Odds Ratio | Significativo |
|---|---:|---:|:---:|
| Ciencias - Ciencias de la Salud | 0.46209 | 0.738 | no |
| Ciencias - Resto | 0.69201 | 1.174 | no |
| Ingenierías | 1.00000 | 0.935 | no |
| Ciencias Sociales - Resto | 0.76698 | 0.722 | no |
| Filosofía y Letras | 0.02793 | 4.792 | ✅ sí |
| Ciencias - Matemáticas y Física | 0.71188 | 1.322 | no |
| Ciencias Sociales - Educación | 0.34019 | 0.000 | no |
