# =============================================================================
#  sorteo/__main__.py
#  Permite ejecutar el paquete directamente: python -m sorteo
# =============================================================================

from .app import SorteoApp

if __name__ == "__main__":
    app = SorteoApp()
    app.mainloop()
