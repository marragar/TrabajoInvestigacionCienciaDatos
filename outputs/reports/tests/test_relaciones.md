# Relaciones entre Centro, Género y Rama

_Generado el 2026-07-15 20:21_

> Nota metodológica: aquí se exploran relaciones ENTRE variables categóricas (no contra el Estado de Solicitud). Para cada par se calculan tres medidas: **chi-cuadrado** de independencia (¿hay asociación?), **V de Cramér** (tamaño del efecto, simétrico) y **U de Theil** (coeficiente de incertidumbre basado en entropía, asimétrico — se calcula en ambas direcciones). Cada relación se analiza tres veces: con todas las solicitudes (GENERAL), solo con las Aceptadas y solo con las Suplentes, para ver si el patrón cambia según el resultado de la solicitud.

## Centro de Investigación × Género

### GENERAL — Todas las solicitudes

**Tabla de contingencia: Centro de Investigación (filas) × Género Solicitante (columnas)**

| Centro de Investigación \\ Género Solicitante | Masculino | Femenino | Total |
|---|---|---|---|
| Universidad de Valladolid | 481 | 274 | 755 |
| Universidad de Salamanca | 493 | 250 | 743 |
| Universidad de León | 248 | 142 | 390 |
| Universidad de Burgos | 140 | 100 | 240 |
| CSIC | 73 | 46 | 119 |
| **Total** | 1435 | 812 | **2247** |

**Chi-cuadrado de independencia** (tabla 5×2)

- χ² = `5.5228`
- gl = `4`
- p-valor = `0.23773`
- **Conclusión:** No hay asociación significativa entre Centro de Investigación y Género Solicitante (α = 0.05)

**V de Cramér (tamaño del efecto, simétrico)**

- V = `0.050`
- Interpretación orientativa: muy débil / prácticamente despreciable

**U de Theil / coeficiente de incertidumbre (asimétrico)**

- U(Centro de Investigación | Género Solicitante) = `0.001` — cuánto reduce conocer Género Solicitante la incertidumbre sobre Centro de Investigación
- U(Género Solicitante | Centro de Investigación) = `0.002` — cuánto reduce conocer Centro de Investigación la incertidumbre sobre Género Solicitante

### ACEPTADA

**Tabla de contingencia: Centro de Investigación (filas) × Género Solicitante (columnas)**

| Centro de Investigación \\ Género Solicitante | Masculino | Femenino | Total |
|---|---|---|---|
| Universidad de Valladolid | 134 | 55 | 189 |
| Universidad de Salamanca | 144 | 53 | 197 |
| Universidad de León | 62 | 30 | 92 |
| Universidad de Burgos | 47 | 24 | 71 |
| CSIC | 41 | 13 | 54 |
| **Total** | 428 | 175 | **603** |

**Chi-cuadrado de independencia** (tabla 5×2)

- χ² = `2.4339`
- gl = `4`
- p-valor = `0.65651`
- **Conclusión:** No hay asociación significativa entre Centro de Investigación y Género Solicitante (α = 0.05)

**V de Cramér (tamaño del efecto, simétrico)**

- V = `0.064`
- Interpretación orientativa: muy débil / prácticamente despreciable

**U de Theil / coeficiente de incertidumbre (asimétrico)**

- U(Centro de Investigación | Género Solicitante) = `0.001` — cuánto reduce conocer Género Solicitante la incertidumbre sobre Centro de Investigación
- U(Género Solicitante | Centro de Investigación) = `0.003` — cuánto reduce conocer Centro de Investigación la incertidumbre sobre Género Solicitante

### SUPLENTE

**Tabla de contingencia: Centro de Investigación (filas) × Género Solicitante (columnas)**

| Centro de Investigación \\ Género Solicitante | Masculino | Femenino | Total |
|---|---|---|---|
| Universidad de Valladolid | 347 | 219 | 566 |
| Universidad de Salamanca | 349 | 197 | 546 |
| Universidad de León | 186 | 112 | 298 |
| Universidad de Burgos | 93 | 76 | 169 |
| CSIC | 32 | 33 | 65 |
| **Total** | 1007 | 637 | **1644** |

**Chi-cuadrado de independencia** (tabla 5×2)

- χ² = `8.5225`
- gl = `4`
- p-valor = `0.07421`
- **Conclusión:** No hay asociación significativa entre Centro de Investigación y Género Solicitante (α = 0.05)

**V de Cramér (tamaño del efecto, simétrico)**

- V = `0.072`
- Interpretación orientativa: muy débil / prácticamente despreciable

**U de Theil / coeficiente de incertidumbre (asimétrico)**

- U(Centro de Investigación | Género Solicitante) = `0.002` — cuánto reduce conocer Género Solicitante la incertidumbre sobre Centro de Investigación
- U(Género Solicitante | Centro de Investigación) = `0.004` — cuánto reduce conocer Centro de Investigación la incertidumbre sobre Género Solicitante

## Rama × Género

### GENERAL — Todas las solicitudes

**Tabla de contingencia: ramaDep (filas) × Género Solicitante (columnas)**

| ramaDep \\ Género Solicitante | Masculino | Femenino | Total |
|---|---|---|---|
| Ciencias - Ciencias de la Salud | 406 | 236 | 642 |
| Ciencias - Resto | 244 | 180 | 424 |
| Ingenierías | 323 | 107 | 430 |
| Ciencias Sociales - Resto | 204 | 118 | 322 |
| Filosofía y Letras | 127 | 110 | 237 |
| Ciencias - Matemáticas y Física | 174 | 54 | 228 |
| Ciencias Sociales - Educación | 55 | 43 | 98 |
| **Total** | 1533 | 848 | **2381** |

**Chi-cuadrado de independencia** (tabla 7×2)

- χ² = `59.8795`
- gl = `6`
- p-valor = `0.00000`
- **Conclusión:** Hay asociación significativa entre ramaDep y Género Solicitante (α = 0.05)

**V de Cramér (tamaño del efecto, simétrico)**

- V = `0.159`
- Interpretación orientativa: débil

**U de Theil / coeficiente de incertidumbre (asimétrico)**

- U(ramaDep | Género Solicitante) = `0.007` — cuánto reduce conocer Género Solicitante la incertidumbre sobre ramaDep
- U(Género Solicitante | ramaDep) = `0.020` — cuánto reduce conocer ramaDep la incertidumbre sobre Género Solicitante

### ACEPTADA

**Tabla de contingencia: ramaDep (filas) × Género Solicitante (columnas)**

| ramaDep \\ Género Solicitante | Masculino | Femenino | Total |
|---|---|---|---|
| Ciencias - Ciencias de la Salud | 146 | 48 | 194 |
| Ciencias - Resto | 81 | 47 | 128 |
| Ingenierías | 86 | 17 | 103 |
| Ciencias Sociales - Resto | 46 | 17 | 63 |
| Filosofía y Letras | 28 | 34 | 62 |
| Ciencias - Matemáticas y Física | 59 | 13 | 72 |
| Ciencias Sociales - Educación | 5 | 3 | 8 |
| **Total** | 451 | 179 | **630** |

**Chi-cuadrado de independencia** (tabla 7×2)

- χ² = `38.2789`
- gl = `6`
- p-valor = `0.00000`
- **Conclusión:** Hay asociación significativa entre ramaDep y Género Solicitante (α = 0.05)

> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable en esta tabla.

**V de Cramér (tamaño del efecto, simétrico)**

- V = `0.246`
- Interpretación orientativa: moderada

**U de Theil / coeficiente de incertidumbre (asimétrico)**

- U(ramaDep | Género Solicitante) = `0.017` — cuánto reduce conocer Género Solicitante la incertidumbre sobre ramaDep
- U(Género Solicitante | ramaDep) = `0.049` — cuánto reduce conocer ramaDep la incertidumbre sobre Género Solicitante

### SUPLENTE

**Tabla de contingencia: ramaDep (filas) × Género Solicitante (columnas)**

| ramaDep \\ Género Solicitante | Masculino | Femenino | Total |
|---|---|---|---|
| Ciencias - Ciencias de la Salud | 260 | 188 | 448 |
| Ciencias - Resto | 163 | 133 | 296 |
| Ingenierías | 237 | 90 | 327 |
| Ciencias Sociales - Resto | 158 | 101 | 259 |
| Filosofía y Letras | 99 | 76 | 175 |
| Ciencias - Matemáticas y Física | 115 | 41 | 156 |
| Ciencias Sociales - Educación | 50 | 40 | 90 |
| **Total** | 1082 | 669 | **1751** |

**Chi-cuadrado de independencia** (tabla 7×2)

- χ² = `37.1287`
- gl = `6`
- p-valor = `0.00000`
- **Conclusión:** Hay asociación significativa entre ramaDep y Género Solicitante (α = 0.05)

**V de Cramér (tamaño del efecto, simétrico)**

- V = `0.146`
- Interpretación orientativa: débil

**U de Theil / coeficiente de incertidumbre (asimétrico)**

- U(ramaDep | Género Solicitante) = `0.006` — cuánto reduce conocer Género Solicitante la incertidumbre sobre ramaDep
- U(Género Solicitante | ramaDep) = `0.016` — cuánto reduce conocer ramaDep la incertidumbre sobre Género Solicitante

## Centro de Investigación × Rama

### GENERAL — Todas las solicitudes

**Tabla de contingencia: Centro de Investigación (filas) × ramaDep (columnas)**

| Centro de Investigación \\ ramaDep | Ciencias - Ciencias de la Salud | Ciencias - Resto | Ingenierías | Ciencias Sociales - Resto | Filosofía y Letras | Ciencias - Matemáticas y Física | Ciencias Sociales - Educación | Total |
|---|---|---|---|---|---|---|---|---|
| Universidad de Valladolid | 116 | 123 | 222 | 99 | 72 | 94 | 29 | 755 |
| Universidad de Salamanca | 206 | 120 | 76 | 122 | 96 | 95 | 28 | 743 |
| Universidad de León | 130 | 80 | 66 | 49 | 33 | 12 | 20 | 390 |
| Universidad de Burgos | 35 | 65 | 57 | 40 | 16 | 13 | 14 | 240 |
| CSIC | 88 | 21 | 1 | 1 | 8 | 0 | 0 | 119 |
| **Total** | 575 | 409 | 422 | 311 | 225 | 214 | 91 | **2247** |

**Chi-cuadrado de independencia** (tabla 5×7)

- χ² = `362.1290`
- gl = `24`
- p-valor = `0.00000`
- **Conclusión:** Hay asociación significativa entre Centro de Investigación y ramaDep (α = 0.05)

> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable en esta tabla.

**V de Cramér (tamaño del efecto, simétrico)**

- V = `0.201`
- Interpretación orientativa: moderada

**U de Theil / coeficiente de incertidumbre (asimétrico)**

- U(Centro de Investigación | ramaDep) = `0.059` — cuánto reduce conocer ramaDep la incertidumbre sobre Centro de Investigación
- U(ramaDep | Centro de Investigación) = `0.046` — cuánto reduce conocer Centro de Investigación la incertidumbre sobre ramaDep

### ACEPTADA

**Tabla de contingencia: Centro de Investigación (filas) × ramaDep (columnas)**

| Centro de Investigación \\ ramaDep | Ciencias - Ciencias de la Salud | Ciencias - Resto | Ingenierías | Ciencias Sociales - Resto | Filosofía y Letras | Ciencias - Matemáticas y Física | Ciencias Sociales - Educación | Total |
|---|---|---|---|---|---|---|---|---|
| Universidad de Valladolid | 22 | 38 | 64 | 15 | 19 | 26 | 5 | 189 |
| Universidad de Salamanca | 64 | 26 | 15 | 30 | 26 | 35 | 1 | 197 |
| Universidad de León | 41 | 22 | 11 | 8 | 6 | 3 | 1 | 92 |
| Universidad de Burgos | 10 | 33 | 12 | 8 | 4 | 4 | 0 | 71 |
| CSIC | 42 | 7 | 0 | 0 | 5 | 0 | 0 | 54 |
| **Total** | 179 | 126 | 102 | 61 | 60 | 68 | 7 | **603** |

**Chi-cuadrado de independencia** (tabla 5×7)

- χ² = `202.2977`
- gl = `24`
- p-valor = `0.00000`
- **Conclusión:** Hay asociación significativa entre Centro de Investigación y ramaDep (α = 0.05)

> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable en esta tabla.

**V de Cramér (tamaño del efecto, simétrico)**

- V = `0.290`
- Interpretación orientativa: moderada

**U de Theil / coeficiente de incertidumbre (asimétrico)**

- U(Centro de Investigación | ramaDep) = `0.117` — cuánto reduce conocer ramaDep la incertidumbre sobre Centro de Investigación
- U(ramaDep | Centro de Investigación) = `0.099` — cuánto reduce conocer Centro de Investigación la incertidumbre sobre ramaDep

### SUPLENTE

**Tabla de contingencia: Centro de Investigación (filas) × ramaDep (columnas)**

| Centro de Investigación \\ ramaDep | Ciencias - Ciencias de la Salud | Ciencias - Resto | Ingenierías | Ciencias Sociales - Resto | Filosofía y Letras | Ciencias - Matemáticas y Física | Ciencias Sociales - Educación | Total |
|---|---|---|---|---|---|---|---|---|
| Universidad de Valladolid | 94 | 85 | 158 | 84 | 53 | 68 | 24 | 566 |
| Universidad de Salamanca | 142 | 94 | 61 | 92 | 70 | 60 | 27 | 546 |
| Universidad de León | 89 | 58 | 55 | 41 | 27 | 9 | 19 | 298 |
| Universidad de Burgos | 25 | 32 | 45 | 32 | 12 | 9 | 14 | 169 |
| CSIC | 46 | 14 | 1 | 1 | 3 | 0 | 0 | 65 |
| **Total** | 396 | 283 | 320 | 250 | 165 | 146 | 84 | **1644** |

**Chi-cuadrado de independencia** (tabla 5×7)

- χ² = `198.0507`
- gl = `24`
- p-valor = `0.00000`
- **Conclusión:** Hay asociación significativa entre Centro de Investigación y ramaDep (α = 0.05)

> ⚠ Alguna celda esperada < 5: el chi-cuadrado puede no ser fiable en esta tabla.

**V de Cramér (tamaño del efecto, simétrico)**

- V = `0.174`
- Interpretación orientativa: débil

**U de Theil / coeficiente de incertidumbre (asimétrico)**

- U(Centro de Investigación | ramaDep) = `0.045` — cuánto reduce conocer ramaDep la incertidumbre sobre Centro de Investigación
- U(ramaDep | Centro de Investigación) = `0.034` — cuánto reduce conocer Centro de Investigación la incertidumbre sobre ramaDep
