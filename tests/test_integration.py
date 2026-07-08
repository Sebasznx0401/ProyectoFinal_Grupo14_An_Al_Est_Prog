"""
Tests de integración del sistema completo
"""

import pytest
from src.modelos.models import Project, Solution
from src.algoritmos.dynamic_programming import solve_knapsack_01
from src.algoritmos.greedy_algorithm import solve_greedy


def test_full_workflow():
    """Test de flujo completo"""
    # Crear proyectos
    projects = [
        Project(1, "A", 50, 100, 1),
        Project(2, "B", 100, 150, 2),
        Project(3, "C", 75, 120, 3),
    ]
    
    budget = 150
    
    # Resolver con DP
    dp_solution = solve_knapsack_01(projects, budget)
    assert dp_solution is not None
    assert len(dp_solution.projects) > 0
    assert dp_solution.total_cost <= budget
    
    # Resolver con Greedy
    greedy_solution = solve_greedy(projects, budget)
    assert greedy_solution is not None
    assert len(greedy_solution.projects) > 0
    assert greedy_solution.total_cost <= budget
    
    # Comparar
    assert dp_solution.total_benefit >= greedy_solution.total_benefit * 0.8  # DP es óptimo


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
