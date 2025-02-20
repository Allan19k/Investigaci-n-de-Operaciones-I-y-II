from pulp import *

# Pedir datos de la función objetivo
print("Ingrese los coeficientes de la función objetivo (Max z = a*x1 + b*x2):")
a = float(input("Coeficiente de x1: "))
b = float(input("Coeficiente de x2: "))

# Pedir datos de las restricciones
restricciones = []
n = int(input("Ingrese el número de restricciones: "))
for i in range(n):
    print(f"Ingrese los coeficientes y tipo de la restricción {i+1} (ax1 + bx2 <= c, ax1 + bx2 >= c o ax1 + bx2 = c)")
    coef_x1 = float(input("Coeficiente de x1: "))
    coef_x2 = float(input("Coeficiente de x2: "))
    tipo = input("Tipo (<=, >=, =): ").strip()
    c = float(input("Valor en el lado derecho: "))
    restricciones.append((coef_x1, coef_x2, tipo, c))

# Crear el problema de maximización
problema = LpProblem("Optimización_Usuario", LpMaximize)

# Definir las variables
x1 = LpVariable('x1', lowBound=0)  # x1 >= 0
x2 = LpVariable('x2', lowBound=0)  # x2 >= 0

# Función objetivo
problema += a * x1 + b * x2, "Función Objetivo"

# Agregar restricciones
i = 1
for coef_x1, coef_x2, tipo, c in restricciones:
    if tipo == "<=":
        problema += coef_x1 * x1 + coef_x2 * x2 <= c, f"Restricción_{i}"
    elif tipo == ">=":
        problema += coef_x1 * x1 + coef_x2 * x2 >= c, f"Restricción_{i}"
    elif tipo == "=":
        problema += coef_x1 * x1 + coef_x2 * x2 == c, f"Restricción_{i}"
    else:
        print(f"Tipo de restricción inválido: {tipo}")
    i += 1

# Resolver el problema
problema.solve()

# Imprimir resultados
print(f"Status: {LpStatus[problema.status]}")
print(f"Función objetivo: {value(problema.objective)}")
print(f"Valor de x1: {value(x1)}")
print(f"Valor de x2: {value(x2)}")

