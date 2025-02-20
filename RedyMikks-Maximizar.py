# Importar la librería 
from pulp import *

# Crear el problema de maximización 
problema = LpProblem("Ejercicio_de_Reddy_Mikks", LpMaximize)

# Definir las variables
x = LpVariable('x', lowBound=0)  # x1 >= 0
y = LpVariable('y', lowBound=0)  # x2 >= 0

# Función objetivo
problema += 5*x + 4*y  # Maximizar z = 5x + 4y

# Restricciones
problema += 6*x + 4*y <= 24, "restriccion_1"
problema += x + 2*y <= 6, "restriccion_2"  
problema += -x + y <= 1, "restriccion_3"
problema += y <= 2, "restriccion_4" 

# Resolver el problema
problema.solve()

# Imprimir resultados
print(f"Status: {LpStatus[problema.status]}")
print(f"Solucion Factible: {value(problema.objective)}")
print(f"Valor de x1: {value(x)}")
print(f"Valor de x2: {value(y)}")



