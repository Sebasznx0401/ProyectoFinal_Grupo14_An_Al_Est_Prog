"""
Punto de entrada principal del Sistema de Planificación de Inversiones
"""

import sys
import os

# Agregar directorio raíz del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utilidades.ui import main

if __name__ == "__main__":
    main()
