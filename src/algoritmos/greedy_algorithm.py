"""
Módulo de Algoritmo Voraz (Greedy)
Implementa una heurística rápida basada en ROI (Retorno sobre Inversión)
para resolver el problema de planificación de inversiones.
"""

from typing import List
from src.modelos.models import Project, Solution


def solve_greedy(projects: List[Project], budget: float) -> Solution:
    """
    Resuelve el problema usando un enfoque Voraz (Greedy)
    
    Estrategia: Ordena los proyectos por ROI (beneficio/costo) en orden descendente
    y selecciona proyectos de forma glotona hasta agotar el presupuesto.
    
    Esta es una heurística que NO garantiza la solución óptima, pero es
    muy rápida y generalmente produce buenos resultados.
    
    Complejidad Temporal: O(n log n) por el ordenamiento
    Complejidad Espacial: O(n)
    
    Args:
        projects: Lista de proyectos disponibles
        budget: Presupuesto máximo disponible
    
    Returns:
        Solution: Objeto con los proyectos seleccionados (solución aproximada)
    
    Ejemplo:
        >>> projects = [Project(1, "A", 10, 20), Project(2, "B", 15, 30)]
        >>> solution = solve_greedy(projects, 20)
        >>> print(solution.total_benefit)
    """
    
    if not projects or budget <= 0:
        return Solution("Greedy Algorithm (por ROI)")
    
    # Ordenar proyectos por ROI (beneficio/costo) en orden DESCENDENTE
    # Los proyectos con mejor ROI se seleccionan primero
    sorted_projects = sorted(projects, key=lambda p: p.roi(), reverse=True)
    
    # Seleccionar proyectos de forma glotona
    solution = Solution("Greedy Algorithm (por ROI)")
    remaining_budget = budget
    
    for project in sorted_projects:
        # Si el proyecto cabe en el presupuesto, agregarlo
        if project.cost <= remaining_budget:
            solution.add_project(project)
            remaining_budget -= project.cost
    
    return solution


def solve_greedy_by_benefit(projects: List[Project], budget: float) -> Solution:
    """
    Variante: Ordena por beneficio (no por ROI)
    
    Estrategia: Selecciona proyectos con mayor beneficio absoluto primero
    (sin considerar el costo relativo)
    
    Complejidad: O(n log n)
    
    Args:
        projects: Lista de proyectos disponibles
        budget: Presupuesto máximo disponible
    
    Returns:
        Solution: Objeto con los proyectos seleccionados
    """
    
    if not projects or budget <= 0:
        return Solution("Greedy Algorithm (por Beneficio)")
    
    # Ordenar por beneficio en orden descendente
    sorted_projects = sorted(projects, key=lambda p: p.benefit, reverse=True)
    
    solution = Solution("Greedy Algorithm (por Beneficio)")
    remaining_budget = budget
    
    for project in sorted_projects:
        if project.cost <= remaining_budget:
            solution.add_project(project)
            remaining_budget -= project.cost
    
    return solution


def solve_greedy_by_priority(projects: List[Project], budget: float) -> Solution:
    """
    Variante: Ordena por prioridad
    
    Estrategia: Selecciona proyectos según su prioridad definida
    
    Complejidad: O(n log n)
    
    Args:
        projects: Lista de proyectos disponibles
        budget: Presupuesto máximo disponible
    
    Returns:
        Solution: Objeto con los proyectos seleccionados
    """
    
    if not projects or budget <= 0:
        return Solution("Greedy Algorithm (por Prioridad)")
    
    # Ordenar por prioridad en orden descendente (10 es máxima prioridad)
    sorted_projects = sorted(projects, key=lambda p: p.priority, reverse=True)
    
    solution = Solution("Greedy Algorithm (por Prioridad)")
    remaining_budget = budget
    
    for project in sorted_projects:
        if project.cost <= remaining_budget:
            solution.add_project(project)
            remaining_budget -= project.cost
    
    return solution


def analyze_greedy_complexity() -> dict:
    """
    Analiza la complejidad del algoritmo Voraz
    
    Returns:
        Diccionario con análisis de complejidad
    """
    return {
        'algorithm': 'Greedy Algorithm (Knapsack Approximation)',
        'time_complexity': 'O(n log n)',
        'space_complexity': 'O(n)',
        'where': 'n = número de proyectos',
        'advantages': [
            'Muy rápido (O(n log n))',
            'Bajo consumo de memoria (O(n))',
            'Fácil de implementar y entender',
            'Generalmente produce buenos resultados',
            'Escalable para muchos proyectos'
        ],
        'disadvantages': [
            'NO garantiza la solución óptima',
            'Puede producir resultados subóptimos',
            'Depende de la heurística elegida (ROI, beneficio, prioridad)'
        ]
    }