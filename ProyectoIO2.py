import tkinter as tk
from tkinter import ttk, messagebox
from pulp import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class OptimizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Solucionador de problemas de PL de 2 variables")
        self.root.geometry("1000x800")
        
        self.create_widgets()
        self.constraint_frames = []
        
    def create_widgets(self):
        # Frame de configuración
        config_frame = ttk.LabelFrame(self.root, text="Datos del Problema")
        config_frame.pack(pady=10, padx=10, fill=tk.X)
        
        # Tipo de optimización (solo lectura)
        ttk.Label(config_frame, text="Objetivo:").grid(row=0, column=0, padx=5)
        self.opt_type = ttk.Combobox(config_frame, values=["Maximizar", "Minimizar"], state="readonly")
        self.opt_type.grid(row=0, column=1, padx=5)
        self.opt_type.current(0)
        
        # Función objetivo
        ttk.Label(config_frame, text="Z =").grid(row=0, column=2, padx=5)
        self.coeff_x1 = ttk.Entry(config_frame, width=5)
        self.coeff_x1.grid(row=0, column=3, padx=2)
        ttk.Label(config_frame, text="x1 +").grid(row=0, column=4, padx=2)
        self.coeff_x2 = ttk.Entry(config_frame, width=5)
        self.coeff_x2.grid(row=0, column=5, padx=2)
        ttk.Label(config_frame, text="x2").grid(row=0, column=6, padx=5)
        
        # Frame de restricciones
        self.constraint_container = ttk.LabelFrame(self.root, text="Restricciones (Formato: ax1 + bx2 ≤|≥|= c)")
        self.constraint_container.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        btn_frame = ttk.Frame(self.constraint_container)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="➕ Agregar Restricción", command=self.add_constraint).pack()
        
        # Botón resolver
        ttk.Button(self.root, text="🔍 RESOLVER", command=self.solve_problem).pack(pady=10)
        
        # Frame de resultados
        result_frame = ttk.LabelFrame(self.root, text="Resultados")
        result_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.result_text = tk.Text(result_frame, height=8, state="disabled")
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Frame del gráfico
        graph_frame = ttk.LabelFrame(self.root, text="Espacio de Soluciones")
        graph_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def add_constraint(self):
        constraint_frame = ttk.Frame(self.constraint_container)
        constraint_frame.pack(fill=tk.X, pady=2)
        self.constraint_frames.append(constraint_frame)
        
        # Componentes de la restricción
        entry_x1 = ttk.Entry(constraint_frame, width=5)
        entry_x1.pack(side=tk.LEFT, padx=2)
        ttk.Label(constraint_frame, text="x1 +").pack(side=tk.LEFT)
        
        entry_x2 = ttk.Entry(constraint_frame, width=5)
        entry_x2.pack(side=tk.LEFT, padx=2)
        ttk.Label(constraint_frame, text="x2").pack(side=tk.LEFT)
        
        # Operador (solo lectura)
        operator = ttk.Combobox(constraint_frame, values=["≤", "≥", "="], state="readonly", width=3)
        operator.pack(side=tk.LEFT, padx=2)
        operator.current(0)
        
        entry_rhs = ttk.Entry(constraint_frame, width=5)
        entry_rhs.pack(side=tk.LEFT, padx=2)
        
        # Botón eliminar (NO se incluye en get_constraints)
        ttk.Button(constraint_frame, text="❌", width=3,
                 command=lambda f=constraint_frame: f.destroy()).pack(side=tk.RIGHT)

    def get_constraints(self):
        constraints = []
        for frame in self.constraint_frames:
            # Filtrar solo Entry y Combobox (excluir botones)
            children = [
                child for child in frame.winfo_children() 
                if isinstance(child, ttk.Entry) or isinstance(child, ttk.Combobox)
            ]
            try:
                a = float(children[0].get())  # Coeficiente x1
                b = float(children[1].get())  # Coeficiente x2
                op = children[2].get()        # Operador
                c = float(children[3].get())  # Valor RHS
                constraints.append((a, b, op, c))
            except (ValueError, IndexError):
                pass
        return constraints

    def solve_problem(self):
        try:
            # Validar función objetivo
            if not self.coeff_x1.get() or not self.coeff_x2.get():
                raise ValueError("Complete la función objetivo")
                
            constraints = self.get_constraints()
            if not constraints:
                raise ValueError("Agregue al menos una restricción válida")
            
            # Configurar problema
            prob = LpProblem("Optimización", 
                            LpMaximize if self.opt_type.get() == "Maximizar" else LpMinimize)
            
            # Variables
            x1 = LpVariable('x1', lowBound=0)
            x2 = LpVariable('x2', lowBound=0)
            
            # Función objetivo
            prob += float(self.coeff_x1.get())*x1 + float(self.coeff_x2.get())*x2
            
            # Restricciones
            for a, b, op, c in constraints:
                if op == "≤":
                    prob += a*x1 + b*x2 <= c
                elif op == "≥":
                    prob += a*x1 + b*x2 >= c
                else:
                    prob += a*x1 + b*x2 == c
            
            # Resolver
            prob.solve()
            
            # Validar solución
            if LpStatus[prob.status] == "Unbounded":
                raise ValueError("Problema no acotado (agregue más restricciones)")
            elif LpStatus[prob.status] != "Optimal":
                raise ValueError("No se encontró solución óptima")
            
            # Mostrar resultados
            self.result_text.config(state="normal")
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"● Estado: {LpStatus[prob.status]}\n")
            self.result_text.insert(tk.END, f"● Valor Óptimo z: {value(prob.objective):.2f}\n")
            self.result_text.insert(tk.END, "\n● Solución Óptima:\n")
            self.result_text.insert(tk.END, f"   x1 = {value(x1):.2f}\n")
            self.result_text.insert(tk.END, f"   x2 = {value(x2):.2f}")
            self.result_text.config(state="disabled")
            
            # Graficar
            self.plot_solution(value(x1), value(x2))
            
        except Exception as e:
            messagebox.showerror("Error", f"{str(e)}")

    def plot_solution(self, x_opt, y_opt):
        self.ax.clear()
        constraints = self.get_constraints()
        x = np.linspace(0, max(10, x_opt*1.5), 400)
        
        # Graficar restricciones
        for a, b, op, c in constraints:
            if b != 0:
                y = (c - a*x)/b
                if op == "≤":
                    self.ax.plot(x, y, label=f"{a}x1 + {b}x2 ≤ {c}")
                    self.ax.fill_between(x, 0, y, alpha=0.1)
                elif op == "≥":
                    self.ax.plot(x, y, label=f"{a}x1 + {b}x2 ≥ {c}")
                    self.ax.fill_between(x, y, 1000, alpha=0.1)
                else:
                    self.ax.plot(x, y, '--', label=f"{a}x1 + {b}x2 = {c}")
            else:
                x_val = c/a
                if op == "≤":
                    self.ax.axvline(x_val, color='red', label=f"x1 ≤ {x_val:.1f}")
                elif op == "≥":
                    self.ax.axvline(x_val, color='red', label=f"x1 ≥ {x_val:.1f}")
                else:
                    self.ax.axvline(x_val, linestyle='--', color='red', label=f"x1 = {x_val:.1f}")
        
        # Punto óptimo
        self.ax.plot(x_opt, y_opt, 'ro', markersize=8, label="Óptimo")
        
        # Configuración del gráfico
        self.ax.set_xlim(0, max(10, x_opt*1.5))
        self.ax.set_ylim(0, max(10, y_opt*1.5))
        self.ax.set_xlabel("x1")
        self.ax.set_ylabel("x2")
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = OptimizationApp(root)
    root.mainloop()