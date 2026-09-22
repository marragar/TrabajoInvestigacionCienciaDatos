# Test de independencia — Género Solicitante vs. Estado de Solicitud

_Generado el 2026-07-09 15:55_

> Nota metodológica: al ser una tabla 2×2 (Masculino/Femenino × Aceptada/Suplente), el test exacto de Fisher se aplica directamente sobre la tabla completa (scipy), junto con el chi-cuadrado de independencia y una verificación cruzada del Fisher exacto vía R (rpy2).

## GENERAL — Todos los años

| Género | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Masculino | 155 | 409 | 564 |
| Femenino | 63 | 278 | 341 |
| **Total** | **218** | **687** | **905** |

**Chi-cuadrado de independencia**

- χ² = `8.9425`
- gl = `1`
- p-valor = `0.00279`
- **Conclusión:** Hay asociación significativa entre Género y Estado (α = 0.05)

**Test exacto de Fisher (scipy)**

- p-valor = `0.00227`
- Odds Ratio = `1.672`
- **Conclusión:** Hay asociación significativa entre Género y Estado (α = 0.05)

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.00227` (método: exacto)
- **Conclusión:** Hay asociación significativa entre Género y Estado (α = 0.05)

**% de aceptación por género**

- Masculino: 27.5% (155/564)
- Femenino: 18.5% (63/341)

## AÑO 2021

| Género | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Masculino | 72 | 97 | 169 |
| Femenino | 28 | 65 | 93 |
| **Total** | **100** | **162** | **262** |

**Chi-cuadrado de independencia**

- χ² = `3.4573`
- gl = `1`
- p-valor = `0.06297`
- **Conclusión:** No hay asociación significativa entre Género y Estado (α = 0.05)

**Test exacto de Fisher (scipy)**

- p-valor = `0.04777`
- Odds Ratio = `1.723`
- **Conclusión:** Hay asociación significativa entre Género y Estado (α = 0.05)

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.04777` (método: exacto)
- **Conclusión:** Hay asociación significativa entre Género y Estado (α = 0.05)

**% de aceptación por género**

- Masculino: 42.6% (72/169)
- Femenino: 30.1% (28/93)

## AÑO 2024

| Género | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Masculino | 29 | 121 | 150 |
| Femenino | 7 | 81 | 88 |
| **Total** | **36** | **202** | **238** |

**Chi-cuadrado de independencia**

- χ² = `4.7423`
- gl = `1`
- p-valor = `0.02943`
- **Conclusión:** Hay asociación significativa entre Género y Estado (α = 0.05)

**Test exacto de Fisher (scipy)**

- p-valor = `0.02354`
- Odds Ratio = `2.773`
- **Conclusión:** Hay asociación significativa entre Género y Estado (α = 0.05)

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.02354` (método: exacto)
- **Conclusión:** Hay asociación significativa entre Género y Estado (α = 0.05)

**% de aceptación por género**

- Masculino: 19.3% (29/150)
- Femenino: 8.0% (7/88)

## AÑO 2025

| Género | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Masculino | 27 | 109 | 136 |
| Femenino | 14 | 72 | 86 |
| **Total** | **41** | **181** | **222** |

**Chi-cuadrado de independencia**

- χ² = `0.2411`
- gl = `1`
- p-valor = `0.62344`
- **Conclusión:** No hay asociación significativa entre Género y Estado (α = 0.05)

**Test exacto de Fisher (scipy)**

- p-valor = `0.59543`
- Odds Ratio = `1.274`
- **Conclusión:** No hay asociación significativa entre Género y Estado (α = 0.05)

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.59543` (método: exacto)
- **Conclusión:** No hay asociación significativa entre Género y Estado (α = 0.05)

**% de aceptación por género**

- Masculino: 19.9% (27/136)
- Femenino: 16.3% (14/86)

## AÑO 2026

| Género | Aceptada | Suplente | Total |
|---|---:|---:|---:|
| Masculino | 27 | 82 | 109 |
| Femenino | 14 | 60 | 74 |
| **Total** | **41** | **142** | **183** |

**Chi-cuadrado de independencia**

- χ² = `0.5642`
- gl = `1`
- p-valor = `0.45257`
- **Conclusión:** No hay asociación significativa entre Género y Estado (α = 0.05)

**Test exacto de Fisher (scipy)**

- p-valor = `0.37309`
- Odds Ratio = `1.411`
- **Conclusión:** No hay asociación significativa entre Género y Estado (α = 0.05)

**Test exacto de Fisher — tabla completa (vía R / rpy2)**

- p-valor = `0.37309` (método: exacto)
- **Conclusión:** No hay asociación significativa entre Género y Estado (α = 0.05)

**% de aceptación por género**

- Masculino: 24.8% (27/109)
- Femenino: 18.9% (14/74)
