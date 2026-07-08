"""
Tests para el módulo de Algoritmo Voraz
"""

import pytest
from src.modelos.models import Project
from src.algoritmos.greedy_algorithm import solve_greedy, solve_greedy_by_benefit, solve_greedy_by_priority


class TestGreedy:
    """Tests para el algoritmo Voraz"""
    
    def test_greedy_empty_projects(self):
        """Verifica que funciona con lista vacía"""
        solution = solve_greedy([], 1000)
        assert len(solution.projects) == 0
        assert solution.total_benefit == 0
    
    def test_greedy_zero_budget(self):
        """Verifica que funciona con presupuesto cero"""
        projects = [Project(1, "A", 100, 200)]
        solution = solve_greedy(projects, 0)
        assert len(solution.projects) == 0
    
    def test_greedy_simple_case(self):
        """Caso simple: un proyecto que cabe"""
        projects = [Project(1, "A", 100, 200)]
        solution = solve_greedy(projects, 100)
        
        assert len(solution.projects) == 1
        assert solution.total_cost == 100
        assert solution.total_benefit == 200
    
    def test_greedy_by_roi(self):
        """Verifica que selecciona por ROI en orden correcto"""
        projects = [
            Project(1, "A", 50, 100),    # ROI = 2.0
            Project(2, "B", 100, 150),   # ROI = 1.5
            Project(3, "C", 75, 120),    # ROI = 1.6
        ]
        solution = solve_greedy(projects, 150)
        
        # Debería seleccionar primero A (ROI=2.0), luego C (ROI=1.6)
        # A + C = 125 costo, 220 beneficio
        assert len(solution.projects) == 2
        assert solution.total_cost == 125
        assert solution.total_benefit == 220
    
    def test_greedy_respects_budget(self):
        """Verifica que respeta el presupuesto"""
        projects = [
            Project(1, "A", 100, 200),
            Project(2, "B", 100, 200),
            Project(3, "C", 100, 200),
        ]
        solution = solve_greedy(projects, 250)
        
        assert solution.total_cost <= 250
    
    def test_greedy_by_benefit(self):
        """Verifica selección por beneficio absoluto"""
        projects = [
            Project(1, "A", 50, 300),    # Mayor beneficio
            Project(2, "B", 100, 200),
            Project(3, "C", 10, 100),
        ]
        solution = solve_greedy_by_benefit(projects, 150)
        
        # Debería seleccionar primero A (beneficio=300), luego B no cabe
        assert len(solution.projects) >= 1
        assert 300 in [p.benefit for p in solution.projects]
    
    def test_greedy_by_priority(self):
        """Verifica selección por prioridad"""
        projects = [
            Project(1, "A", 50, 100, priority=1),
            Project(2, "B", 100, 200, priority=10),  # Mayor prioridad
            Project(3, "C", 75, 120, priority=5),
        ]
        solution = solve_greedy_by_priority(projects, 150)
        
        # Debería seleccionar primero B (prioridad=10)
        if len(solution.projects) > 0:
            first_priority = solution.projects[0].priority
            assert first_priority >= 5
    
    def test_greedy_algorithm_name(self):
        """Verifica que la solución indica el algoritmo correcto"""
        projects = [Project(1, "A", 100, 200)]
        solution = solve_greedy(projects, 100)
        
        assert "Greedy" in solution.algorithm_used


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
