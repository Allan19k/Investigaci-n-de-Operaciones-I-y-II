# Importar la librería 
from pulp import *

# Crear el problema de maximización 
problema = LpProblem("Ejercicio_de_la_dieta", LpMinimize)

# Definir las variables
x = LpVariable('x', lowBound=0)  # x1 >= 0
y = LpVariable('y', lowBound=0)  # x2 >= 0

# Función objetivo
problema += 0.3*x + 0.9*y  # Minimizar z = 0.3x + 0.9y

# Restricciones
problema += x + y >= 800, "restriccion_1"
problema += 0.21*x - 0.3*y <= 0, "restriccion_2"  
problema += 0.03*x - 0.01* y >= 0, "restriccion_3"

# Resolver el problema
problema.solve()

# Imprimir resultados
print(f"Status: {LpStatus[problema.status]}")
print(f"Solucion Factible: {value(problema.objective)}")
print(f"Valor de x1: {value(x)}")
print(f"Valor de x2: {value(y)}")
