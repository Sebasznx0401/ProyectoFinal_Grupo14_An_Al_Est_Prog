"""
Módulo de Modelos de Datos
Contiene las clases fundamentales para el Sistema de Planificación de Inversiones
"""

from typing import List, Dict
from dataclasses import dataclass


@dataclass
class Project:
    """
    Representa un proyecto de inversión
    
    Attributes:
        id: Identificador único del proyecto
        name: Nombre del proyecto
        cost: Costo del proyecto en dinero
        benefit: Beneficio esperado del proyecto
        priority: Prioridad del proyecto (1-10, donde 10 es máxima)
    """
    
    id: int
    name: str
    cost: float
    benefit: float
    priority: int = 1
    
    def _post_init_(self):
        """Validaciones después de inicializar"""
        if self.cost < 0:
            raise ValueError(f"El costo no puede ser negativo: {self.cost}")
        if self.benefit < 0:
            raise ValueError(f"El beneficio no puede ser negativo: {self.benefit}")
        if not 1 <= self.priority <= 10:
            raise ValueError(f"La prioridad debe estar entre 1 y 10: {self.priority}")
    
    def roi(self) -> float:
        """
        Calcula el Retorno sobre la Inversión (ROI)
        ROI = benefit / cost
        """
        if self.cost == 0:
            return float('inf') if self.benefit > 0 else 0
        return self.benefit / self.cost
    
    def to_dict(self) -> Dict:
        """Convierte el proyecto a diccionario"""
        return {
            'id': self.id,
            'name': self.name,
            'cost': self.cost,
            'benefit': self.benefit,
            'priority': self.priority,
            'roi': self.roi()
        }
    
    def _str_(self) -> str:
        return (f"Proyecto(ID={self.id}, Nombre='{self.name}', "
                f"Costo=${self.cost:,.0f}, Beneficio=${self.benefit:,.0f}, "
                f"ROI={self.roi():.2f})")
    
    def _repr_(self) -> str:
        return self._str_()


class Solution:
    """
    Representa una solución al problema de planificación de inversiones
    
    Attributes:
        projects: Lista de proyectos seleccionados
        total_cost: Costo total de los proyectos seleccionados
        total_benefit: Beneficio total esperado
        algorithm_used: Nombre del algoritmo utilizado
    """
    
    def _init_(self, algorithm_used: str = "Unknown"):
        """
        Inicializa una solución vacía
        
        Args:
            algorithm_used: Nombre del algoritmo que generó esta solución
        """
        self.projects: List[Project] = []
        self.total_cost: float = 0.0
        self.total_benefit: float = 0.0
        self.algorithm_used: str = algorithm_used
    
    def add_project(self, project: Project) -> None:
        """
        Agrega un proyecto a la solución y recalcula totales
        
        Args:
            project: Proyecto a agregar
        """
        if project not in self.projects:
            self.projects.append(project)
            self._calculate_totals()
    
    def _calculate_totals(self) -> None:
        """Calcula los totales de costo y beneficio"""
        self.total_cost = sum(p.cost for p in self.projects)
        self.total_benefit = sum(p.benefit for p in self.projects)
    
    def calculate_totals(self) -> tuple:
        """
        Retorna una tupla (total_cost, total_benefit)
        """
        self._calculate_totals()
        return self.total_cost, self.total_benefit
    
    def is_valid(self, budget: float) -> bool:
        """
        Verifica si la solución respeta el presupuesto
        
        Args:
            budget: Presupuesto disponible
            
        Returns:
            True si el costo total <= presupuesto
        """
        return self.total_cost <= budget
    
    def get_roi(self) -> float:
        """Calcula el ROI total de la solución"""
        if self.total_cost == 0:
            return 0
        return self.total_benefit / self.total_cost
    
    def to_dict(self) -> Dict:
        """Convierte la solución a diccionario"""
        return {
            'algorithm': self.algorithm_used,
            'projects': [p.to_dict() for p in self.projects],
            'total_cost': self.total_cost,
            'total_benefit': self.total_benefit,
            'total_roi': self.get_roi(),
            'project_count': len(self.projects)
        }
    
    def _str_(self) -> str:
        summary = f"\n{'='*60}\n"
        summary += f"SOLUCIÓN: {self.algorithm_used}\n"
        summary += f"{'='*60}\n"
        summary += f"Proyectos seleccionados: {len(self.projects)}\n"
        summary += f"Costo total: ${self.total_cost:,.0f}\n"
        summary += f"Beneficio total: ${self.total_benefit:,.0f}\n"
        summary += f"ROI total: {self.get_roi():.2f}\n"
        
        if self.projects:
            summary += f"\nDetalles:\n"
            for i, project in enumerate(self.projects, 1):
                summary += f"  {i}. {project.name}: ${project.cost:,.0f} → ${project.benefit:,.0f}\n"
        else:
            summary += "No hay proyectos seleccionados.\n"
        
        summary += f"{'='*60}\n"
        return summary
    
    def _repr_(self) -> str:
        return f"Solution(algorithm={self.algorithm_used}, projects={len(self.projects)}, cost={self.total_cost})"