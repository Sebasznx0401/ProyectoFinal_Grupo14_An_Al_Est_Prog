"""
Módulo de Programación Dinámica
Implementa el algoritmo de la Mochila 0/1 (Knapsack Problem)
para resolver el problema de planificación de inversiones de forma óptima.
"""

from typing import List, Tuple
from src.modelos.models import Project, Solution


def solve_knapsack_01(projects: List[Project], budget: float) -> Solution:
    """
    Resuelve el problema usando Programación Dinámica (Mochila 0/1)
    
    Esta función encuentra la combinación óptima de proyectos que maximiza
    el beneficio total sin exceder el presupuesto disponible.
    
    Complejidad Temporal: O(n * W) donde n = cantidad de proyectos, W = presupuesto
    Complejidad Espacial: O(n * W)
    
    Args:
        projects: Lista de proyectos disponibles
        budget: Presupuesto máximo disponible
    
    Returns:
        Solution: Objeto con los proyectos seleccionados (solución óptima)
    
    Ejemplo:
        >>> projects = [Project(1, "A", 10, 20), Project(2, "B", 15, 30)]
        >>> solution = solve_knapsack_01(projects, 20)
        >>> print(solution.total_benefit)
    """
    
    n = len(projects)
    
    # Si no hay proyectos o presupuesto es cero
    if n == 0 or budget <= 0:
        return Solution("Dynamic Programming (DP)")
    
    # Convertir presupuesto a entero para usar como índice
    W = int(budget)
    
    # Crear tabla DP: dp[i][w] = máximo beneficio con primeros i proyectos y presupuesto w
    # Primera fila y columna son 0 (caso base)
    dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]
    
    # Llenar la tabla DP
    for i in range(1, n + 1):
        project = projects[i - 1]
        project_cost = int(project.cost)
        project_benefit = project.benefit
        
        for w in range(W + 1):
            # Opción 1: No incluir el proyecto
            dp[i][w] = dp[i - 1][w]
            
            # Opción 2: Incluir el proyecto (si cabe)
            if project_cost <= w:
                include_benefit = dp[i - 1][w - project_cost] + project_benefit
                dp[i][w] = max(dp[i][w], include_benefit)
    
    # Backtracking: Encontrar qué proyectos fueron seleccionados
    selected_projects = _backtrack_selected_projects(dp, projects, budget)
    
    # Crear solución
    solution = Solution("Dynamic Programming (Mochila 0/1)")
    for project in selected_projects:
        solution.add_project(project)
    
    return solution


def _backtrack_selected_projects(dp, projects: List[Project], budget: float) -> List[Project]:
    """
    Realiza backtracking para encontrar qué proyectos fueron seleccionados
    
    Args:
        dp: Tabla DP generada por solve_knapsack_01
        projects: Lista de proyectos
        budget: Presupuesto utilizado
    
    Returns:
        Lista de proyectos seleccionados
    """
    
    n = len(projects)
    W = int(budget)
    selected = []
    
    # Empezar desde la esquina inferior derecha de la tabla
    i = n
    w = W
    
    while i > 0 and w > 0:
        # Si el valor cambió, significa que este proyecto fue incluido
        if dp[i][w] != dp[i - 1][w]:
            project = projects[i - 1]
            selected.append(project)
            w -= int(project.cost)
        
        i -= 1
    
    return selected


def analyze_dp_complexity() -> dict:
    """
    Analiza la complejidad del algoritmo de Programación Dinámica
    
    Returns:
        Diccionario con análisis de complejidad
    """
    return {
        'algorithm': 'Dynamic Programming (Knapsack 0/1)',
        'time_complexity': 'O(n * W)',
        'space_complexity': 'O(n * W)',
        'where': 'n = número de proyectos, W = presupuesto (redondeado)',
        'advantages': [
            'Encuentra la solución óptima global',
            'Garantiza maximizar el beneficio',
            'Funciona para cualquier combinación de costos'
        ],
        'disadvantages': [
            'Alto consumo de memoria con presupuestos grandes',
            'Más lento que el enfoque voraz',
            'Depende de presupuestos discretos'
        ]
    }