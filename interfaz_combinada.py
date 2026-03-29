import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import os
from analizador_sintactico import parsear_tokens, AnalizadorSintactico, imprimir_arbol
from analizador_semantico import AnalizadorSemantico
from traductor_javascript import TraductorJavaScript
from generador_intermedio import GeneradorCodigoIntermedio

class AnalizadorCompletoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Compilador Completo - Enyer Estrella")
        self.root.geometry("1200x750")
        
        bg_color = "#f0f0f0"
        self.root.configure(bg=bg_color)
        
        main_frame = tk.Frame(root, bg=bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Variables
        self.arbol_actual = None
        
        # FRAME DE ENTRADA
        entrada_frame = tk.LabelFrame(main_frame,
                                      text="  Codigo Fuente  ",
                                      font=("Arial", 11, "bold"),
                                      bg=bg_color,
                                      fg="#34495e",
                                      padx=10,
                                      pady=10)
        entrada_frame.pack(fill=tk.BOTH, pady=(0, 10))
        
        self.entrada = scrolledtext.ScrolledText(entrada_frame,
                                                 height=5,
                                                 width=120,
                                                 font=("Consolas", 11),
                                                 wrap=tk.WORD,
                                                 borderwidth=2,
                                                 relief=tk.GROOVE)
        self.entrada.pack(padx=5, pady=5)
        
        ejemplo = "x = 3 + 5\ny = x * 2\nprint(y)"
        self.entrada.insert("1.0", ejemplo)
        self.entrada.tag_add("ejemplo", "1.0", tk.END)
        self.entrada.tag_config("ejemplo", foreground="gray")
        
        self.entrada.bind("<FocusIn>", self.limpiar_ejemplo)
        self.es_ejemplo = True
        
        # BOTONES
        botones_frame = tk.Frame(main_frame, bg=bg_color)
        botones_frame.pack(pady=10)
        
        self.btn_analizar = tk.Button(botones_frame,
                                      text="▶ Analizar",
                                      command=self.analizar_completo,
                                      bg="#27ae60",
                                      fg="white",
                                      font=("Arial", 12, "bold"),
                                      width=12,
                                      height=1,
                                      cursor="hand2",
                                      relief=tk.RAISED,
                                      borderwidth=3)
        self.btn_analizar.pack(side=tk.LEFT, padx=5)
        
        # BOTON: Código Intermedio
        self.btn_intermedio = tk.Button(botones_frame,
                                       text="📋 Código TAC",
                                       command=self.mostrar_codigo_intermedio,
                                       bg="#9b59b6",
                                       fg="white",
                                       font=("Arial", 12, "bold"),
                                       width=12,
                                       height=1,
                                       cursor="hand2",
                                       relief=tk.RAISED,
                                       borderwidth=3)
        self.btn_intermedio.pack(side=tk.LEFT, padx=5)
        
        # BOTON: Traducir a JS
        self.btn_traducir = tk.Button(botones_frame,
                                      text="🔄 Traducir JS",
                                      command=self.traducir_a_javascript,
                                      bg="#3498db",
                                      fg="white",
                                      font=("Arial", 12, "bold"),
                                      width=12,
                                      height=1,
                                      cursor="hand2",
                                      relief=tk.RAISED,
                                      borderwidth=3)
        self.btn_traducir.pack(side=tk.LEFT, padx=5)
        
        btn_limpiar = tk.Button(botones_frame,
                               text="Limpiar",
                               command=self.limpiar,
                               bg="#e74c3c",
                               fg="white",
                               font=("Arial", 12, "bold"),
                               width=12,
                               height=1,
                               cursor="hand2",
                               relief=tk.RAISED,
                               borderwidth=3)
        btn_limpiar.pack(side=tk.LEFT, padx=5)
        
        # FRAME DE RESULTADOS
        resultados_frame = tk.Frame(main_frame, bg=bg_color)
        resultados_frame.pack(fill=tk.BOTH, expand=True)
        
        # Panel 1: Tokens
        tokens_frame = tk.LabelFrame(resultados_frame,
                                     text="  Analisis Lexico (Tokens)  ",
                                     font=("Arial", 10, "bold"),
                                     bg=bg_color,
                                     fg="#34495e",
                                     padx=10,
                                     pady=10)
        tokens_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 3))
        
        self.resultado_tokens = scrolledtext.ScrolledText(tokens_frame,
                                                          height=15,
                                                          width=30,
                                                          font=("Consolas", 9),
                                                          wrap=tk.WORD,
                                                          state='disabled',
                                                          borderwidth=2,
                                                          relief=tk.GROOVE,
                                                          bg="#ffffff")
        self.resultado_tokens.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        # Panel 2: Arbol sintactico
        arbol_frame = tk.LabelFrame(resultados_frame,
                                    text="  Analisis Sintactico (Arbol)  ",
                                    font=("Arial", 10, "bold"),
                                    bg=bg_color,
                                    fg="#34495e",
                                    padx=10,
                                    pady=10)
        arbol_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(3, 3))
        
        self.resultado_arbol = scrolledtext.ScrolledText(arbol_frame,
                                                         height=15,
                                                         width=30,
                                                         font=("Consolas", 9),
                                                         wrap=tk.WORD,
                                                         state='disabled',
                                                         borderwidth=2,
                                                         relief=tk.GROOVE,
                                                         bg="#ffffff")
        self.resultado_arbol.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        # Panel 3: Semantico
        semantico_frame = tk.LabelFrame(resultados_frame,
                                       text="  Analisis Semantico  ",
                                       font=("Arial", 10, "bold"),
                                       bg=bg_color,
                                       fg="#34495e",
                                       padx=10,
                                       pady=10)
        semantico_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(3, 0))
        
        self.resultado_semantico = scrolledtext.ScrolledText(semantico_frame,
                                                             height=15,
                                                             width=30,
                                                             font=("Consolas", 9),
                                                             wrap=tk.WORD,
                                                             state='disabled',
                                                             borderwidth=2,
                                                             relief=tk.GROOVE,
                                                             bg="#ffffff")
        self.resultado_semantico.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        # Footer
        footer = tk.Label(main_frame,
                         text="Lexico (Flex) | Sintactico (Python) | Semantico | Codigo Intermedio TAC | Traductor JavaScript",
                         font=("Arial", 8),
                         bg=bg_color,
                         fg="#95a5a6")
        footer.pack(side=tk.BOTTOM, pady=(10, 0))
        
        self.verificar_ejecutable()
    
    def limpiar_ejemplo(self, event):
        if self.es_ejemplo:
            self.entrada.delete("1.0", tk.END)
            self.entrada.tag_remove("ejemplo", "1.0", tk.END)
            self.es_ejemplo = False
    
    def verificar_ejecutable(self):
        if not os.path.exists("analizador.exe"):
            respuesta = messagebox.askyesno(
                "Analizador no encontrado",
                "No se encontro 'analizador.exe'.\n\n"
                "¿Deseas compilarlo ahora?\n\n"
                "Requiere Flex y GCC instalados"
            )
            if respuesta:
                self.compilar_analizador()
    
    def compilar_analizador(self):
        try:
            self.mostrar_tokens("Compilando...\n")
            self.root.update()
            
            resultado_flex = subprocess.run(
                ["flex", "analizador.l"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if resultado_flex.returncode != 0:
                self.mostrar_tokens("Error en Flex:\n" + resultado_flex.stderr)
                return
            
            self.mostrar_tokens("Flex OK\n")
            self.root.update()
            
            resultado_gcc = subprocess.run(
                ["gcc", "lex.yy.c", "-o", "analizador.exe"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if resultado_gcc.returncode != 0:
                self.mostrar_tokens("Error en GCC:\n" + resultado_gcc.stderr)
                return
            
            self.mostrar_tokens("Compilacion exitosa\n")
            messagebox.showinfo("Analizador compilado correctamente")
            
        except FileNotFoundError:
            error_msg = (
                "No se encontro Flex o GCC\n\n"
                "Instala con: pacman -S flex gcc"
            )
            self.mostrar_tokens(error_msg)
            messagebox.showerror("Error", error_msg)
        except Exception as e:
            self.mostrar_tokens(f"Error: {str(e)}")
    
    def analizar_completo(self):
        codigo = self.entrada.get("1.0", tk.END).strip()
        
        if not codigo or self.es_ejemplo:
            messagebox.showwarning("Advertencia", "Digite codigo para analizar")
            return
        
        if not os.path.exists("analizador.exe"):
            messagebox.showerror("Error", "Compila el analizador primero")
            self.verificar_ejecutable()
            return
        
        # PASO 1: Analisis Lexico
        try:
            with open("temp_input.txt", "w") as f:
                f.write(codigo)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear archivo:\n{e}")
            return
        
        try:
            resultado = subprocess.run(
                ["./analizador.exe", "temp_input.txt"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            salida_lexico = resultado.stdout
            
            if not salida_lexico.strip():
                self.mostrar_tokens("Sin salida del lexico")
                self.mostrar_arbol("")
                self.mostrar_semantico("")
                return
            
            # Mostrar tokens
            self.mostrar_tokens(salida_lexico)
            
            # PASO 2: Analisis Sintactico
            tokens = parsear_tokens(salida_lexico)
            
            if not tokens:
                self.mostrar_arbol("No hay tokens para analizar")
                self.mostrar_semantico("")
                return
            
            analizador_sintactico = AnalizadorSintactico(tokens)
            arbol, errores_sintacticos = analizador_sintactico.analizar()
            
            # Guardar el arbol
            self.arbol_actual = arbol
            
            # Mostrar resultado sintáctico
            if errores_sintacticos:
                resultado_sintactico = "❌ ERRORES DE SINTAXIS:\n\n"
                for error in errores_sintacticos:
                    resultado_sintactico += f"  • {error}\n"
                self.mostrar_arbol(resultado_sintactico)
                self.mostrar_semantico("No se puede analizar semantica\n(hay errores de sintaxis)")
                self.arbol_actual = None
                return
            else:
                resultado_sintactico = "✅ SINTAXIS CORRECTA\n\n"
                resultado_sintactico += "Arbol Sintactico:\n\n"
                if arbol:
                    resultado_sintactico += imprimir_arbol(arbol)
                else:
                    resultado_sintactico += "(arbol vacio)"
                
                self.mostrar_arbol(resultado_sintactico)
            
            # PASO 3: Analisis Semantico
            analizador_semantico = AnalizadorSemantico()
            es_valido = analizador_semantico.analizar(arbol)
            
            # Mostrar resultado semantico
            resultado_semantico = analizador_semantico.obtener_reporte()
            self.mostrar_semantico(resultado_semantico)
                
        except FileNotFoundError:
            error_msg = "No se encontro analizador.exe"
            self.mostrar_tokens(error_msg)
            messagebox.showerror("Error", error_msg)
        except subprocess.TimeoutExpired:
            self.mostrar_tokens("Tiempo de espera agotado")
        except Exception as e:
            self.mostrar_tokens(f"Error: {str(e)}")
        finally:
            if os.path.exists("temp_input.txt"):
                try:
                    os.remove("temp_input.txt")
                except:
                    pass
    
    def mostrar_codigo_intermedio(self):
        """Muestra el codigo intermedio TAC"""
        if self.arbol_actual is None:
            messagebox.showwarning(
                "Advertencia",
                "Primero debes analizar el codigo\n\n"
                "Presiona 'Analizar' antes de generar codigo intermedio"
            )
            return
        
        # Generar codigo intermedio
        generador = GeneradorCodigoIntermedio()
        codigo_tac = generador.generar(self.arbol_actual)
        
        # Mostrar ventana popup
        self.mostrar_ventana_intermedio(codigo_tac)
    
    def mostrar_ventana_intermedio(self, codigo_tac):
        """Muestra ventana popup con codigo intermedio"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Codigo Intermedio (TAC)")
        ventana.geometry("600x500")
        ventana.configure(bg="#f0f0f0")
        
        main_frame = tk.Frame(ventana, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        titulo = tk.Label(main_frame,
                         text="Codigo Intermedio (Three Address Code)",
                         font=("Arial", 14, "bold"),
                         bg="#f0f0f0",
                         fg="#2c3e50")
        titulo.pack(pady=(0, 10))
        
        texto_frame = tk.LabelFrame(main_frame,
                                    text="  Codigo TAC  ",
                                    font=("Arial", 10, "bold"),
                                    bg="#f0f0f0",
                                    fg="#34495e",
                                    padx=10,
                                    pady=10)
        texto_frame.pack(fill=tk.BOTH, expand=True)
        
        texto = scrolledtext.ScrolledText(texto_frame,
                                          height=15,
                                          width=70,
                                          font=("Consolas", 11),
                                          wrap=tk.WORD,
                                          borderwidth=2,
                                          relief=tk.GROOVE,
                                          bg="#ffffff")
        texto.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        texto.insert("1.0", codigo_tac)
        texto.config(state='disabled')
        
        botones_frame = tk.Frame(main_frame, bg="#f0f0f0")
        botones_frame.pack(pady=10)
        
        btn_copiar = tk.Button(botones_frame,
                              text="📋 Copiar",
                              command=lambda: self.copiar_portapapeles(codigo_tac, ventana),
                              bg="#27ae60",
                              fg="white",
                              font=("Arial", 11, "bold"),
                              width=15,
                              cursor="hand2",
                              relief=tk.RAISED,
                              borderwidth=2)
        btn_copiar.pack(side=tk.LEFT, padx=5)
        
        btn_cerrar = tk.Button(botones_frame,
                              text="✖ Cerrar",
                              command=ventana.destroy,
                              bg="#e74c3c",
                              fg="white",
                              font=("Arial", 11, "bold"),
                              width=10,
                              cursor="hand2",
                              relief=tk.RAISED,
                              borderwidth=2)
        btn_cerrar.pack(side=tk.LEFT, padx=5)
        
        instrucciones = tk.Label(main_frame,
                                text="TAC = Three Address Code (Codigo de Tres Direcciones)",
                                font=("Arial", 9),
                                bg="#f0f0f0",
                                fg="#7f8c8d")
        instrucciones.pack(pady=(5, 0))
    
    def traducir_a_javascript(self):
        """Traduce a JavaScript"""
        if self.arbol_actual is None:
            messagebox.showwarning(
                "Advertencia",
                "Primero debes analizar el codigo\n\n"
                "Presiona 'Analizar' antes de traducir"
            )
            return
        
        traductor = TraductorJavaScript()
        codigo_js = traductor.traducir(self.arbol_actual)
        
        self.mostrar_ventana_traduccion(codigo_js)
    
    def mostrar_ventana_traduccion(self, codigo_js):
        """Muestra ventana popup con JavaScript"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Codigo JavaScript Generado")
        ventana.geometry("600x500")
        ventana.configure(bg="#f0f0f0")
        
        main_frame = tk.Frame(ventana, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        titulo = tk.Label(main_frame,
                         text="Codigo JavaScript Generado",
                         font=("Arial", 14, "bold"),
                         bg="#f0f0f0",
                         fg="#2c3e50")
        titulo.pack(pady=(0, 10))
        
        texto_frame = tk.LabelFrame(main_frame,
                                    text="  Codigo  ",
                                    font=("Arial", 10, "bold"),
                                    bg="#f0f0f0",
                                    fg="#34495e",
                                    padx=10,
                                    pady=10)
        texto_frame.pack(fill=tk.BOTH, expand=True)
        
        texto = scrolledtext.ScrolledText(texto_frame,
                                          height=15,
                                          width=70,
                                          font=("Consolas", 11),
                                          wrap=tk.WORD,
                                          borderwidth=2,
                                          relief=tk.GROOVE,
                                          bg="#ffffff")
        texto.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        texto.insert("1.0", codigo_js)
        texto.config(state='disabled')
        
        botones_frame = tk.Frame(main_frame, bg="#f0f0f0")
        botones_frame.pack(pady=10)
        
        btn_copiar = tk.Button(botones_frame,
                              text="📋 Copiar",
                              command=lambda: self.copiar_portapapeles(codigo_js, ventana),
                              bg="#27ae60",
                              fg="white",
                              font=("Arial", 11, "bold"),
                              width=15,
                              cursor="hand2",
                              relief=tk.RAISED,
                              borderwidth=2)
        btn_copiar.pack(side=tk.LEFT, padx=5)
        
        btn_cerrar = tk.Button(botones_frame,
                              text="✖ Cerrar",
                              command=ventana.destroy,
                              bg="#e74c3c",
                              fg="white",
                              font=("Arial", 11, "bold"),
                              width=10,
                              cursor="hand2",
                              relief=tk.RAISED,
                              borderwidth=2)
        btn_cerrar.pack(side=tk.LEFT, padx=5)
        
        instrucciones = tk.Label(main_frame,
                                text="Para probar: Navegador → F12 → Console → Pega el codigo",
                                font=("Arial", 9),
                                bg="#f0f0f0",
                                fg="#7f8c8d")
        instrucciones.pack(pady=(5, 0))
    
    def copiar_portapapeles(self, texto, ventana):
        """Copia texto al portapapeles"""
        ventana.clipboard_clear()
        ventana.clipboard_append(texto)
        messagebox.showinfo("Copiado", "Codigo copiado al portapapeles")
    
    def limpiar(self):
        self.entrada.delete("1.0", tk.END)
        self.mostrar_tokens("")
        self.mostrar_arbol("")
        self.mostrar_semantico("")
        self.arbol_actual = None
        self.es_ejemplo = False
    
    def mostrar_tokens(self, texto):
        self.resultado_tokens.config(state='normal')
        self.resultado_tokens.delete("1.0", tk.END)
        self.resultado_tokens.insert("1.0", texto)
        self.resultado_tokens.config(state='disabled')
    
    def mostrar_arbol(self, texto):
        self.resultado_arbol.config(state='normal')
        self.resultado_arbol.delete("1.0", tk.END)
        self.resultado_arbol.insert("1.0", texto)
        self.resultado_arbol.config(state='disabled')
    
    def mostrar_semantico(self, texto):
        self.resultado_semantico.config(state='normal')
        self.resultado_semantico.delete("1.0", tk.END)
        self.resultado_semantico.insert("1.0", texto)
        self.resultado_semantico.config(state='disabled')

def main():
    root = tk.Tk()
    app = AnalizadorCompletoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()