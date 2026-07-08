"""
Tests para el módulo de Modelos
"""

import pytest
from src.modelos.models import Project, Solution


class TestProject:
    """Tests para la clase Project"""
    
    def test_project_creation(self):
        """Verifica que se puede crear un proyecto"""
        p = Project(1, "Test", 100, 200)
        assert p.id == 1
        assert p.name == "Test"
        assert p.cost == 100
        assert p.benefit == 200
        assert p.priority == 1
    
    def test_project_roi(self):
        """Verifica el cálculo de ROI"""
        p = Project(1, "Test", 100, 300)
        assert p.roi() == 3.0
    
    def test_project_roi_division_by_zero(self):
        """Verifica que ROI maneja división por cero"""
        p = Project(1, "Test", 0, 100)
        assert p.roi() == float('inf')
    
    def test_project_negative_cost(self):
        """Verifica que rechaza costos negativos"""
        with pytest.raises(ValueError):
            Project(1, "Test", -100, 200)
    
    def test_project_negative_benefit(self):
        """Verifica que rechaza beneficios negativos"""
        with pytest.raises(ValueError):
            Project(1, "Test", 100, -200)
    
    def test_project_invalid_priority(self):
        """Verifica que rechaza prioridad inválida"""
        with pytest.raises(ValueError):
            Project(1, "Test", 100, 200, priority=11)
    
    def test_project_to_dict(self):
        """Verifica conversión a diccionario"""
        p = Project(1, "Test", 100, 200)
        d = p.to_dict()
        assert d['id'] == 1
        assert d['name'] == "Test"
        assert d['cost'] == 100
        assert d['benefit'] == 200


class TestSolution:
    """Tests para la clase Solution"""
    
    def test_solution_creation(self):
        """Verifica que se puede crear una solución"""
        s = Solution("TestAlgo")
        assert s.total_cost == 0
        assert s.total_benefit == 0
        assert len(s.projects) == 0
    
    def test_solution_add_project(self):
        """Verifica agregar proyectos a la solución"""
        s = Solution()
        p = Project(1, "Test", 100, 200)
        s.add_project(p)
        
        assert len(s.projects) == 1
        assert s.total_cost == 100
        assert s.total_benefit == 200
    
    def test_solution_no_duplicate_projects(self):
        """Verifica que no se agregan duplicados"""
        s = Solution()
        p = Project(1, "Test", 100, 200)
        s.add_project(p)
        s.add_project(p)
        
        assert len(s.projects) == 1
    
    def test_solution_is_valid(self):
        """Verifica validación de presupuesto"""
        s = Solution()
        p = Project(1, "Test", 100, 200)
        s.add_project(p)
        
        assert s.is_valid(100)
        assert s.is_valid(150)
        assert not s.is_valid(50)
    
    def test_solution_get_roi(self):
        """Verifica cálculo de ROI total"""
        s = Solution()
        s.add_project(Project(1, "A", 100, 200))
        s.add_project(Project(2, "B", 100, 300))
        
        # Total: 200 costo, 500 beneficio → ROI = 2.5
        assert s.get_roi() == 2.5
    
    def test_solution_to_dict(self):
        """Verifica conversión a diccionario"""
        s = Solution("DP")
        s.add_project(Project(1, "Test", 100, 200))
        d = s.to_dict()
        
        assert d['algorithm'] == "DP"
        assert d['project_count'] == 1
        assert d['total_cost'] == 100
        assert d['total_benefit'] == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
