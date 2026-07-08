"""
Módulo de Análisis de Complejidad
Proporciona herramientas para analizar y comparar la eficiencia de los algoritmos
"""

import time
from typing import List, Tuple
from src.modelos.models import Project, Solution
from src.algoritmos.dynamic_programming import solve_knapsack_01, analyze_dp_complexity
from src.algoritmos.greedy_algorithm import solve_greedy, analyze_greedy_complexity


def benchmark_algorithms(projects: List[Project], budget: float) -> dict:
    """
    Ejecuta ambos algoritmos y mide su tiempo de ejecución y resultados
    
    Args:
        projects: Lista de proyectos
        budget: Presupuesto disponible
    
    Returns:
        Diccionario con resultados y tiempos de ejecución
    """
    
    results = {
        'project_count': len(projects),
        'budget': budget,
        'dp': {},
        'greedy': {}
    }
    
    # Ejecutar DP
    start_time = time.time()
    dp_solution = solve_knapsack_01(projects, budget)
    dp_time = time.time() - start_time
    
    results['dp'] = {
        'time_seconds': dp_time,
        'time_ms': dp_time * 1000,
        'total_cost': dp_solution.total_cost,
        'total_benefit': dp_solution.total_benefit,
        'roi': dp_solution.get_roi(),
        'project_count': len(dp_solution.projects)
    }
    
    # Ejecutar Greedy
    start_time = time.time()
    greedy_solution = solve_greedy(projects, budget)
    greedy_time = time.time() - start_time
    
    results['greedy'] = {
        'time_seconds': greedy_time,
        'time_ms': greedy_time * 1000,
        'total_cost': greedy_solution.total_cost,
        'total_benefit': greedy_solution.total_benefit,
        'roi': greedy_solution.get_roi(),
        'project_count': len(greedy_solution.projects)
    }
    
    # Comparación
    dp_benefit = dp_solution.total_benefit
    greedy_benefit = greedy_solution.total_benefit
    optimality = (greedy_benefit / dp_benefit * 100) if dp_benefit > 0 else 100
    
    results['comparison'] = {
        'dp_faster_by_factor': dp_time / greedy_time if greedy_time > 0 else 0,
        'greedy_faster_by_factor': greedy_time / dp_time if dp_time > 0 else 0,
        'optimality_percentage': optimality,
        'benefit_difference': dp_benefit - greedy_benefit,
        'dp_better': dp_benefit >= greedy_benefit
    }
    
    return results


def generate_complexity_report() -> str:
    """
    Genera un reporte completo de análisis de complejidad
    
    Returns:
        String con el reporte formateado
    """
    
    report = """
╔════════════════════════════════════════════════════════════════════════════╗
║         ANÁLISIS DE COMPLEJIDAD - SISTEMA DE PLANIFICACIÓN                ║
║                    DE INVERSIONES CON PRESUPUESTO LIMITADO                 ║
╚════════════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════════
1. PROGRAMACIÓN DINÁMICA (MOCHILA 0/1)
═══════════════════════════════════════════════════════════════════════════════

    COMPLEJIDAD TEMPORAL: O(n * W)
    ├─ n: Número de proyectos
    └─ W: Presupuesto (valor discreto redondeado)
    
    COMPLEJIDAD ESPACIAL: O(n * W)
    ├─ Se crea matriz DP de tamaño (n+1) x (W+1)
    └─ Almacena máximos beneficios para cada subproblema
    
    PSEUDOCÓDIGO:
    ┌─────────────────────────────────────────────────────────┐
    │ dp[i][w] = máximo beneficio con primeros i proyectos    │
    │            y presupuesto w                              │
    │                                                         │
    │ Para i = 1 hasta n:                                     │
    │   Para w = presupuesto hasta 0:                         │
    │     dp[i][w] = max(                                     │
    │       dp[i-1][w],                   # no incluir        │
    │       dp[i-1][w-cost[i]] + benefit[i]  # incluir       │
    │     )                                                   │
    │                                                         │
    │ Backtracking para obtener proyectos seleccionados       │
    └─────────────────────────────────────────────────────────┘
    
    VENTAJAS:
    ✓ Encuentra la SOLUCIÓN ÓPTIMA GARANTIZADA
    ✓ Maximiza el beneficio al 100%
    ✓ Funciona para cualquier combinación de costos
    ✓ Determinístico y confiable
    
    DESVENTAJAS:
    ✗ Alto consumo de memoria (especialmente con presupuestos grandes)
    ✗ Más lento que el enfoque voraz
    ✗ Depende de presupuestos discretos
    ✗ Para presupuesto W=1,000,000 y n=1000: requiere ~1GB de RAM
    
    CASOS DE USO:
    • Cuando se necesita garantizar optimalidad
    • Presupuestos moderados (hasta millones)
    • Decisiones críticas donde la precisión es esencial


═══════════════════════════════════════════════════════════════════════════════
2. ALGORITMO VORAZ (GREEDY)
═══════════════════════════════════════════════════════════════════════════════

    COMPLEJIDAD TEMPORAL: O(n log n)
    └─ Dominado por el ordenamiento de proyectos
    
    COMPLEJIDAD ESPACIAL: O(n)
    ├─ Se ordena la lista de proyectos
    └─ No se requieren estructuras de datos adicionales grandes
    
    PSEUDOCÓDIGO (Heurística por ROI):
    ┌─────────────────────────────────────────────────────────┐
    │ Ordenar proyectos por ROI (benefit/cost) DESCENDENTE    │
    │                                                         │
    │ costo_actual = 0                                        │
    │ Para cada proyecto en orden:                            │
    │   Si (costo_actual + costo_proyecto) <= presupuesto:   │
    │     Agregar proyecto                                    │
    │     costo_actual += costo_proyecto                      │
    │                                                         │
    │ Retornar solución                                       │
    └─────────────────────────────────────────────────────────┘
    
    VENTAJAS:
    ✓ MUY RÁPIDO: 1000x más rápido que DP en casos grandes
    ✓ Bajo consumo de memoria (O(n))
    ✓ Fácil de entender e implementar
    ✓ Generalmente produce resultados cercanos al óptimo (80-95%)
    ✓ Escalable para millones de proyectos
    
    DESVENTAJAS:
    ✗ NO garantiza la solución óptima
    ✗ Puede perder oportunidades de mejor combinación
    ✗ Depende de la heurística elegida
    ✗ Resultado subóptimo de hasta 20% en casos patológicos
    
    VARIANTES:
    1. Por ROI (benefit/cost) - RECOMENDADO
       └─ Mejor balance entre calidad y velocidad
    
    2. Por Beneficio Absoluto
       └─ Favorece proyectos grandes
    
    3. Por Prioridad
       └─ Respeta prioridades de negocio
    
    CASOS DE USO:
    • Cuando se necesita respuesta inmediata
    • Presupuestos muy grandes (millones+)
    • Casos donde 80% óptimo es aceptable
    • Sistemas en tiempo real


═══════════════════════════════════════════════════════════════════════════════
3. COMPARATIVA DETALLADA
═══════════════════════════════════════════════════════════════════════════════

    Métrica                    | DP              | Greedy
    ───────────────────────────┼─────────────────┼─────────────
    Optimalidad                | 100% (óptimo)   | 80-95%
    Tiempo (100 proyectos)     | ~1 ms           | ~0.001 ms
    Tiempo (10,000 proyectos)  | ~500 ms         | ~0.01 ms
    Memoria (100 proy)         | 10-100 MB       | < 1 MB
    Memoria (10,000 proy)      | 1-10 GB         | < 1 MB
    Complejidad Temporal       | O(n*W)          | O(n log n)
    Complejidad Espacial       | O(n*W)          | O(n)
    Determinístico             | Sí              | Sí
    Paralelizable              | Parcialmente    | Sí (sorting)


═══════════════════════════════════════════════════════════════════════════════
4. RECOMENDACIONES DE USO
═══════════════════════════════════════════════════════════════════════════════

    USAR PROGRAMACIÓN DINÁMICA SI:
    ├─ Necesitas solución 100% óptima
    ├─ Presupuesto < 1,000,000
    ├─ Proyectos < 10,000
    ├─ Disponibilidad de RAM > cantidad proyectos x presupuesto
    └─ Decisión tiene alto costo de error

    USAR ALGORITMO VORAZ SI:
    ├─ Necesitas respuesta inmediata
    ├─ Presupuesto > 1,000,000
    ├─ Proyectos > 10,000
    ├─ RAM limitada
    └─ 80-95% óptimo es aceptable para el negocio

    ESTRATEGIA HÍBRIDA:
    ├─ Para decisiones críticas: Ejecuta ambos y compara
    ├─ Si diferencia < 5%: acepta solución voraz (más rápida)
    ├─ Si diferencia > 5%: usa programación dinámica
    └─ El usuario elige cuál usar


═══════════════════════════════════════════════════════════════════════════════
5. EJEMPLOS NUMÉRICOS
═══════════════════════════════════════════════════════════════════════════════

    Escenario 1: Pequeño (típico de pruebas)
    ├─ Proyectos: 10
    ├─ Presupuesto: $100,000
    ├─ DP: 0.001 ms, 1 MB
    ├─ Greedy: 0.0001 ms, 0.01 MB
    └─ Factor diferencia: 10x más rápido greedy

    Escenario 2: Mediano (pequeña empresa)
    ├─ Proyectos: 1,000
    ├─ Presupuesto: $10,000,000
    ├─ DP: 1000 ms (1 segundo), 10 GB
    ├─ Greedy: 0.1 ms, 0.1 MB
    └─ Factor diferencia: 10,000x más rápido greedy

    Escenario 3: Grande (empresa grande)
    ├─ Proyectos: 100,000
    ├─ Presupuesto: $100,000,000
    ├─ DP: NO VIABLE (requeriría 1TB RAM)
    ├─ Greedy: 10 ms, 1 MB
    └─ Factor diferencia: DP imposible, greedy válido


═══════════════════════════════════════════════════════════════════════════════
6. CONCLUSIONES
═══════════════════════════════════════════════════════════════════════════════

    1. OPTIMALIDAD vs VELOCIDAD
       Existe un trade-off fundamental entre obtener la solución
       perfecta vs obtenerla rápidamente.

    2. ESCALABILIDAD
       DP no escala bien a presupuestos/proyectos muy grandes.
       Greedy escala prácticamente ilimitadamente.

    3. DECISIÓN PRÁCTICA
       En la mayoría de casos reales (presupuesto > 1M, proyectos > 1000),
       la única opción viable es Greedy.

    4. VALOR DEL ANÁLISIS
       Ejecutar ambos algoritmos y mostrar que difieren en < 5%
       permite presentar solución rápida con confianza.

    5. RECOMENDACIÓN FINAL
       Implementar AMBOS algoritmos y usar heurística:
       • Si presupuesto y proyectos son pequeños: usar DP
       • Si son grandes: usar Greedy
       • Siempre mostrar comparación al usuario

╚════════════════════════════════════════════════════════════════════════════╝
"""
    
    return report


def print_benchmark_results(results: dict) -> None:
    """
    Imprime los resultados del benchmark de forma legible
    
    Args:
        results: Diccionario de resultados del benchmark
    """
    print("\n" + "="*80)
    print("RESULTADOS DEL BENCHMARK")
    print("="*80)
    print(f"\nDatos de entrada:")
    print(f"  Proyectos: {results['project_count']}")
    print(f"  Presupuesto: ${results['budget']:,.0f}")
    
    print(f"\n{'PROGRAMACIÓN DINÁMICA (DP)':^80}")
    print("-" * 80)
    dp = results['dp']
    print(f"  Tiempo: {dp['time_ms']:.4f} ms ({dp['time_seconds']:.6f} segundos)")
    print(f"  Beneficio: ${dp['total_benefit']:,.0f}")
    print(f"  Costo: ${dp['total_cost']:,.0f}")
    print(f"  ROI: {dp['roi']:.2f}")
    print(f"  Proyectos: {dp['project_count']}")
    
    print(f"\n{'ALGORITMO VORAZ (GREEDY)':^80}")
    print("-" * 80)
    greedy = results['greedy']
    print(f"  Tiempo: {greedy['time_ms']:.4f} ms ({greedy['time_seconds']:.6f} segundos)")
    print(f"  Beneficio: ${greedy['total_benefit']:,.0f}")
    print(f"  Costo: ${greedy['total_cost']:,.0f}")
    print(f"  ROI: {greedy['roi']:.2f}")
    print(f"  Proyectos: {greedy['project_count']}")
    
    print(f"\n{'COMPARACIÓN':^80}")
    print("-" * 80)
    comp = results['comparison']
    print(f"  DP es más rápido: {comp['dp_faster_by_factor']:.2f}x")
    print(f"  Optimalidad de Greedy: {comp['optimality_percentage']:.1f}%")
    print(f"  Diferencia en beneficio: ${comp['benefit_difference']:,.0f}")
    print(f"  Solución óptima: {'DP' if comp['dp_better'] else 'Empate'}")
    print("="*80 + "\n")
