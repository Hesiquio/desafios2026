class Cajero:
    def __init__(self, usuario, saldo_inicial):
        self.usuario = usuario
        self.saldo = saldo_inicial
        self.limite_retiro = 5000
    def retirar_efectivo(self, monto):
        if monto <= self.limite_retiro:
            if monto <= self.saldo:
                nuevo_saldo = self.saldo - monto
                print(f"Retiro exitoso de: ${monto}")
                print(f"Su nuevo saldo es: ${nuevo_saldo}")
            else:
                print("Saldo insuficiente.")
        else:
            print("El monto excede el límite de retiro diario.")
# --- Ejecución ---
mi_cuenta = Cajero("Diego G.", 8000)
mi_cuenta.retirar_efectivo(3000)
print(f"Saldo real en cuenta tras el retiro: ${mi_cuenta.saldo}")