"""
Tests para el módulo de Programación Dinámica
"""

import pytest
from src.modelos.models import Project
from src.algoritmos.dynamic_programming import solve_knapsack_01


class TestDynamicProgramming:
    """Tests para el algoritmo de Programación Dinámica"""
    
    def test_dp_empty_projects(self):
        """Verifica que funciona con lista vacía"""
        solution = solve_knapsack_01([], 1000)
        assert len(solution.projects) == 0
        assert solution.total_benefit == 0
    
    def test_dp_zero_budget(self):
        """Verifica que funciona con presupuesto cero"""
        projects = [Project(1, "A", 100, 200)]
        solution = solve_knapsack_01(projects, 0)
        assert len(solution.projects) == 0
    
    def test_dp_simple_case(self):
        """Caso simple: un proyecto que cabe"""
        projects = [Project(1, "A", 100, 200)]
        solution = solve_knapsack_01(projects, 100)
        
        assert len(solution.projects) == 1
        assert solution.total_cost == 100
        assert solution.total_benefit == 200
    
    def test_dp_exceeds_budget(self):
        """Caso: proyecto que no cabe en presupuesto"""
        projects = [Project(1, "A", 100, 200)]
        solution = solve_knapsack_01(projects, 50)
        
        assert len(solution.projects) == 0
        assert solution.total_benefit == 0
    
    def test_dp_multiple_projects(self):
        """Caso: múltiples proyectos"""
        projects = [
            Project(1, "A", 50, 100),   # ROI = 2.0
            Project(2, "B", 100, 150),  # ROI = 1.5
            Project(3, "C", 75, 120),   # ROI = 1.6
        ]
        solution = solve_knapsack_01(projects, 150)
        
        # Presupuesto: 150
        # Óptimo: A (50, 100) + C (75, 120) = 125 costo, 220 beneficio
        # O: B (100, 150) + A (50) no cabe
        assert solution.total_cost <= 150
        assert solution.total_benefit >= 220
    
    def test_dp_knapsack_classic(self):
        """Caso clásico de mochila 0/1"""
        # Capacidad: 10, valores: [60, 100, 120], pesos: [5, 4, 3]
        projects = [
            Project(1, "Item1", 5, 60),
            Project(2, "Item2", 4, 100),
            Project(3, "Item3", 3, 120),
        ]
        solution = solve_knapsack_01(projects, 10)
        
        # Óptimo: Item2 (4, 100) + Item3 (3, 120) = 7 costo, 220 beneficio
        assert solution.total_cost == 7
        assert solution.total_benefit == 220
    
    def test_dp_algorithm_name(self):
        """Verifica que la solución indica el algoritmo correcto"""
        projects = [Project(1, "A", 100, 200)]
        solution = solve_knapsack_01(projects, 100)
        
        assert "Dynamic Programming" in solution.algorithm_used


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
"""
Tests para el módulo de Programación Dinámica
"""

import pytest
from src.modelos.models import Project
from src.algoritmos.dynamic_programming import solve_knapsack_01


class TestDynamicProgramming:
    """Tests para el algoritmo de Programación Dinámica"""
    
    def test_dp_empty_projects(self):
        """Verifica que funciona con lista vacía"""
        solution = solve_knapsack_01([], 1000)
        assert len(solution.projects) == 0
        assert solution.total_benefit == 0
    
    def test_dp_zero_budget(self):
        """Verifica que funciona con presupuesto cero"""
        projects = [Project(1, "A", 100, 200)]
        solution = solve_knapsack_01(projects, 0)
        assert len(solution.projects) == 0
    
    def test_dp_simple_case(self):
        """Caso simple: un proyecto que cabe"""
        projects = [Project(1, "A", 100, 200)]
        solution = solve_knapsack_01(projects, 100)
        
        assert len(solution.projects) == 1
        assert solution.total_cost == 100
        assert solution.total_benefit == 200
    
    def test_dp_exceeds_budget(self):
        """Caso: proyecto que no cabe en presupuesto"""
        projects = [Project(1, "A", 100, 200)]
        solution = solve_knapsack_01(projects, 50)
        
        assert len(solution.projects) == 0
        assert solution.total_benefit == 0
    
    def test_dp_multiple_projects(self):
        """Caso: múltiples proyectos"""
        projects = [
            Project(1, "A", 50, 100),   # ROI = 2.0
            Project(2, "B", 100, 150),  # ROI = 1.5
            Project(3, "C", 75, 120),   # ROI = 1.6
        ]
        solution = solve_knapsack_01(projects, 150)
        
        # Presupuesto: 150
        # Óptimo: A (50, 100) + C (75, 120) = 125 costo, 220 beneficio
        # O: B (100, 150) + A (50) no cabe
        assert solution.total_cost <= 150
        assert solution.total_benefit >= 220
    
    def test_dp_knapsack_classic(self):
        """Caso clásico de mochila 0/1"""
        # Capacidad: 10, valores: [60, 100, 120], pesos: [5, 4, 3]
        projects = [
            Project(1, "Item1", 5, 60),
            Project(2, "Item2", 4, 100),
            Project(3, "Item3", 3, 120),
        ]
        solution = solve_knapsack_01(projects, 10)
        
        # Óptimo: Item2 (4, 100) + Item3 (3, 120) = 7 costo, 220 beneficio
        assert solution.total_cost == 7
        assert solution.total_benefit == 220
    
    def test_dp_algorithm_name(self):
        """Verifica que la solución indica el algoritmo correcto"""
        projects = [Project(1, "A", 100, 200)]
        solution = solve_knapsack_01(projects, 100)
        
        assert "Dynamic Programming" in solution.algorithm_used


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
