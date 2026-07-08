# Proyecto 14: Sistema de Planificación de Inversiones con Presupuesto Limitado

## Descripción del Problema
Una organización debe elegir proyectos de inversión para maximizar beneficios sin superar un presupuesto disponible.

## Objetivos
- Aplicar estrategias algorítmicas: **Programación Dinámica** (Mochila 0/1) y **Enfoque Voraz**
- Modelar correctamente el problema computacional
- Implementar una solución funcional en Python con buenas prácticas
- Analizar complejidad temporal y espacial
- Comparar eficiencia de diferentes enfoques
- Presentar y defender la solución

## Estrategias Principales
1. **Programación Dinámica (Knapsack 0/1)**: Solución óptima global
2. **Enfoque Voraz (Greedy)**: Heurística por beneficio/costo
3. **Comparación y análisis**: Validación de resultados

## Estructura del Proyecto

```
PROYECTO FINAL PY/
├── src/
│   ├── models.py              # Clases del dominio
│   ├── dynamic_programming.py # Algoritmo DP
│   ├── greedy_algorithm.py    # Algoritmo Voraz
│   ├── analyzer.py            # Análisis de complejidad
│   ├── ui.py                  # Interfaz de usuario
│   └── main.py                # Punto de entrada
├── tests/
│   ├── test_models.py
│   ├── test_dp.py
│   ├── test_greedy.py
│   └── test_cases.csv
├── docs/
│   ├── WORKFLOW_GIT.md        # Guía de workflow Git
│   ├── ASSIGNMENT.md          # Asignación por integrante
│   └── COMPLEXITY_ANALYSIS.md # Análisis de complejidad
├── README.md
└── .gitignore
```

## Requisitos Mínimos a Cumplir
- ✅ Registrar proyectos con costo, beneficio y prioridad
- ✅ Calcular combinación óptima bajo presupuesto
- ✅ Comparar con solución voraz por beneficio/costo
- ✅ Presentar decisión recomendada y justificación
- ✅ Código documentado y organizado
- ✅ Control de versiones con Git
- ✅ Datos de prueba y casos de entrada

## Equipo (5 Integrantes)
| # | Integrante | Rol | Rama |
|---|-----------|-----|------|
| 1 | Jefe de Proyecto + Git Merge | `main` |
| 2 | Integrante 2 | Modelos de Datos | `feature/models` |
| 3 | Integrante 3 | Programación Dinámica | `feature/dynamic-programming` |
| 4 | Integrante 4 | Algoritmo Voraz | `feature/greedy-algorithm` |
| 5 | Integrante 5 | Interfaz + Análisis | `feature/ui-analysis` |

## Cómo Iniciar
```bash
# Clone del repositorio
git clone <URL_REPO>
cd PROYECTO\ FINAL\ PY

# Cada integrante en su rama
git checkout -b feature/<su-asignacion>

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python src/main.py

# Ejecutar pruebas
pytest tests/
```
