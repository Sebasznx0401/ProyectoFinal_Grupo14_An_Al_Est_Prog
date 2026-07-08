"""
Módulo de Interfaz de Usuario
Proporciona un menú interactivo para utilizar el sistema de planificación
"""

import sys
from typing import List, Tuple

try:
    from tabulate import tabulate
except ModuleNotFoundError:  # pragma: no cover - fallback for environments without tabulate
    def tabulate(rows, headers=None, tablefmt="simple"):
        """Fallback simple table formatter used when tabulate is unavailable."""
        if not rows:
            return ""

        if headers is None:
            headers = []

        data = [list(map(str, row)) for row in rows]
        if headers:
            header_row = [str(h) for h in headers]
            data = [header_row] + data

        widths = []
        for col in zip(*data):
            widths.append(max(len(str(item)) for item in col))

        lines = []
        for idx, row in enumerate(data):
            cells = [str(item).ljust(widths[col]) for col, item in enumerate(row)]
            line = " | ".join(cells)
            lines.append(line)
            if idx == 0 and headers:
                lines.append("-+-".join("-" * width for width in widths))

        return "\n".join(lines)

from src.modelos.models import Project, Solution
from src.algoritmos.dynamic_programming import solve_knapsack_01
from src.algoritmos.greedy_algorithm import solve_greedy, solve_greedy_by_benefit, solve_greedy_by_priority
from src.algoritmos.analyzer import benchmark_algorithms, generate_complexity_report, print_benchmark_results


def print_header():
    """Imprime el encabezado del programa"""
    print("\n" + "="*80)
    print("SISTEMA DE PLANIFICACIÓN DE INVERSIONES CON PRESUPUESTO LIMITADO".center(80))
    print("Proyecto 14 - Algoritmos Comparativos".center(80))
    print("="*80 + "\n")


def print_menu():
    """Imprime el menú principal"""
    print("\n" + "-"*80)
    print("MENÚ PRINCIPAL")
    print("-"*80)
    print("1. Cargar proyectos desde archivo")
    print("2. Cargar proyectos de ejemplo")
    print("3. Agregar proyecto manualmente")
    print("4. Resolver con Programación Dinámica (DP)")
    print("5. Resolver con Algoritmo Voraz (Greedy)")
    print("6. Resolver con ambos y comparar")
    print("7. Ver análisis de complejidad")
    print("8. Ejecutar benchmark")
    print("9. Ver proyectos cargados")
    print("10. Limpiar proyectos")
    print("0. Salir")
    print("-"*80)


def load_sample_projects() -> List[Project]:
    """
    Carga proyectos de ejemplo para pruebas
    
    Returns:
        Lista de proyectos de ejemplo
    """
    projects = [
        Project(1, "Software Development Tool", 50000, 80000, 1),
        Project(2, "Mobile App", 30000, 45000, 2),
        Project(3, "Cloud Infrastructure", 40000, 65000, 3),
        Project(4, "Security Update", 15000, 25000, 4),
        Project(5, "Documentation", 10000, 15000, 5),
        Project(6, "API Integration", 20000, 35000, 2),
        Project(7, "Database Optimization", 25000, 40000, 3),
        Project(8, "Testing Framework", 12000, 20000, 4),
    ]
    return projects


def display_projects(projects: List[Project]) -> None:
    """
    Muestra los proyectos en formato tabla
    
    Args:
        projects: Lista de proyectos a mostrar
    """
    if not projects:
        print("\n⚠️  No hay proyectos cargados.")
        return
    
    print("\n" + "="*100)
    print("PROYECTOS CARGADOS".center(100))
    print("="*100)
    
    headers = ["ID", "Nombre", "Costo", "Beneficio", "ROI", "Prioridad"]
    data = []
    
    for p in projects:
        data.append([
            p.id,
            p.name[:30],  # Truncar nombre si es muy largo
            f"${p.cost:,.0f}",
            f"${p.benefit:,.0f}",
            f"{p.roi():.2f}",
            p.priority
        ])
    
    print(tabulate(data, headers=headers, tablefmt="grid"))
    print(f"\nTotal de proyectos: {len(projects)}\n")


def add_project_manual(projects: List[Project]) -> List[Project]:
    """
    Permite agregar un proyecto manualmente
    
    Args:
        projects: Lista actual de proyectos
    
    Returns:
        Lista con el nuevo proyecto agregado
    """
    try:
        print("\n" + "-"*80)
        print("AGREGAR PROYECTO MANUALMENTE")
        print("-"*80)
        
        project_id = len(projects) + 1
        name = input("Nombre del proyecto: ").strip()
        cost = float(input("Costo ($): "))
        benefit = float(input("Beneficio esperado ($): "))
        priority = int(input("Prioridad (1-10): "))
        
        new_project = Project(project_id, name, cost, benefit, priority)
        projects.append(new_project)
        
        print(f"\n✓ Proyecto agregado exitosamente: {new_project}")
        return projects
        
    except ValueError as e:
        print(f"\n✗ Error: Entrada inválida. {e}")
        return projects
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return projects


def get_budget() -> float:
    """
    Solicita el presupuesto disponible al usuario
    
    Returns:
        Presupuesto como número flotante
    """
    while True:
        try:
            budget = float(input("\nPresupuesto disponible ($): "))
            if budget <= 0:
                print("El presupuesto debe ser positivo.")
                continue
            return budget
        except ValueError:
            print("Por favor, ingresa un número válido.")


def display_solution(solution: Solution, budget: float) -> None:
    """
    Muestra una solución de forma legible
    
    Args:
        solution: Solución a mostrar
        budget: Presupuesto disponible
    """
    print("\n" + "="*100)
    print(f"SOLUCIÓN: {solution.algorithm_used}".center(100))
    print("="*100)
    
    # Información de la solución
    print(f"\nResultados:")
    print(f"  Proyectos seleccionados: {len(solution.projects)}")
    print(f"  Costo total: ${solution.total_cost:,.0f} (Presupuesto: ${budget:,.0f})")
    print(f"  Beneficio total: ${solution.total_benefit:,.0f}")
    print(f"  ROI: {solution.get_roi():.2f}")
    print(f"  Presupuesto utilizado: {(solution.total_cost/budget)*100:.1f}%")
    print(f"  Presupuesto restante: ${budget - solution.total_cost:,.0f}")
    
    # Tabla de proyectos seleccionados
    if solution.projects:
        print(f"\nProyectos seleccionados:")
        headers = ["#", "Nombre", "Costo", "Beneficio", "ROI", "Prioridad"]
        data = []
        
        for i, p in enumerate(solution.projects, 1):
            data.append([
                i,
                p.name[:40],
                f"${p.cost:,.0f}",
                f"${p.benefit:,.0f}",
                f"{p.roi():.2f}",
                p.priority
            ])
        
        print(tabulate(data, headers=headers, tablefmt="grid"))
    else:
        print("\nNo hay proyectos en la solución.")
    
    print("="*100 + "\n")


def display_comparison(dp_solution: Solution, greedy_solution: Solution, budget: float) -> None:
    """
    Muestra una comparación lado a lado de dos soluciones
    
    Args:
        dp_solution: Solución de Programación Dinámica
        greedy_solution: Solución del Algoritmo Voraz
        budget: Presupuesto disponible
    """
    print("\n" + "="*100)
    print("COMPARACIÓN DE SOLUCIONES".center(100))
    print("="*100)
    
    # Tabla comparativa
    comparison_data = [
        ["Algoritmo", "DP (Óptimo)", "Voraz (Heurística)"],
        ["Proyectos", len(dp_solution.projects), len(greedy_solution.projects)],
        ["Costo total", f"${dp_solution.total_cost:,.0f}", f"${greedy_solution.total_cost:,.0f}"],
        ["Beneficio total", f"${dp_solution.total_benefit:,.0f}", f"${greedy_solution.total_benefit:,.0f}"],
        ["ROI", f"{dp_solution.get_roi():.2f}", f"{greedy_solution.get_roi():.2f}"],
        ["% Presupuesto usado", f"{(dp_solution.total_cost/budget)*100:.1f}%", 
         f"{(greedy_solution.total_cost/budget)*100:.1f}%"],
    ]
    
    print()
    for row in comparison_data:
        print(f"  {row[0]:.<25} {row[1]:>30} | {row[2]:>30}")
    
    # Análisis
    dp_better = dp_solution.total_benefit > greedy_solution.total_benefit
    difference = abs(dp_solution.total_benefit - greedy_solution.total_benefit)
    optimality = (greedy_solution.total_benefit / dp_solution.total_benefit * 100) \
        if dp_solution.total_benefit > 0 else 100
    
    print(f"\n  {'ANÁLISIS':.<25}")
    print(f"  {'Diferencia en beneficio':.<25} ${difference:,.0f}")
    print(f"  {'Optimalidad de Voraz':.<25} {optimality:.1f}%")
    
    if dp_better:
        print(f"  {'Recomendación':.<25} DP produce {optimality:.1f}% más beneficio")
    else:
        print(f"  {'Recomendación':.<25} Ambas dan resultados similares")
    
    print("="*100 + "\n")


def main():
    """Función principal - Menú interactivo"""
    print_header()
    
    projects: List[Project] = []
    budget: float = 0
    
    while True:
        try:
            print_menu()
            choice = input("Selecciona una opción: ").strip()
            
            if choice == "1":
                # Cargar desde archivo
                print("\n⚠️  Opción no implementada en esta versión.")
                print("Por favor, usa la opción 2 (proyectos de ejemplo) o 3 (agregar manualmente).")
                
            elif choice == "2":
                # Cargar proyectos de ejemplo
                projects = load_sample_projects()
                print(f"\n✓ {len(projects)} proyectos de ejemplo cargados.")
                display_projects(projects)
                
            elif choice == "3":
                # Agregar proyecto manualmente
                if not projects:
                    print("\nPrimero debe cargar proyectos (opción 2) o agregar uno (opción 3).")
                projects = add_project_manual(projects)
                
            elif choice == "4":
                # Resolver con DP
                if not projects:
                    print("\n✗ Error: No hay proyectos cargados.")
                    continue
                budget = get_budget()
                print("\n⏳ Resolviendo con Programación Dinámica...")
                solution = solve_knapsack_01(projects, budget)
                display_solution(solution, budget)
                
            elif choice == "5":
                # Resolver con Voraz
                if not projects:
                    print("\n✗ Error: No hay proyectos cargados.")
                    continue
                budget = get_budget()
                print("\n⏳ Resolviendo con Algoritmo Voraz...")
                solution = solve_greedy(projects, budget)
                display_solution(solution, budget)
                
            elif choice == "6":
                # Comparar ambos
                if not projects:
                    print("\n✗ Error: No hay proyectos cargados.")
                    continue
                budget = get_budget()
                print("\n⏳ Resolviendo con ambos algoritmos...")
                dp_solution = solve_knapsack_01(projects, budget)
                greedy_solution = solve_greedy(projects, budget)
                display_solution(dp_solution, budget)
                display_solution(greedy_solution, budget)
                display_comparison(dp_solution, greedy_solution, budget)
                
            elif choice == "7":
                # Análisis de complejidad
                print(generate_complexity_report())
                
            elif choice == "8":
                # Benchmark
                if not projects:
                    print("\n✗ Error: No hay proyectos cargados.")
                    continue
                budget = get_budget()
                print("\n⏳ Ejecutando benchmark...")
                results = benchmark_algorithms(projects, budget)
                print_benchmark_results(results)
                
            elif choice == "9":
                # Ver proyectos
                display_projects(projects)
                
            elif choice == "10":
                # Limpiar proyectos
                projects = []
                print("\n✓ Proyectos eliminados.")
                
            elif choice == "0":
                # Salir
                print("\n¡Hasta luego! 👋")
                sys.exit(0)
                
            else:
                print("\n✗ Opción no válida. Por favor, intenta de nuevo.")
                
        except KeyboardInterrupt:
            print("\n\n¡Programa interrumpido por el usuario!")
            sys.exit(0)
        except Exception as e:
            print(f"\n✗ Error inesperado: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()