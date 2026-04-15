class Producto:
    def __init__(self, nombre, stock_inicial):
        self.nombre = nombre
        self.stock = stock_inicial
    def agregar_stock(self, cantidad):
        self.stock = self.stock + cantidad
    def vender(self, cantidad):
        self.stock = self.stock - cantidad
        if self.stock < 0:
            print("Error: No hay suficiente stock.")
            self.stock = 0 
        else:
            print(f"Venta exitosa de {cantidad} unidades.")
# --- Prueba de ejecución ---
laptop = Producto("Laptop", 5)
laptop.vender(10) 
print(f"Stock final de {laptop.nombre}: {laptop.stock}")