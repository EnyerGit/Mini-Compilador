# Analizador Semantico
# Valida que las variables existan y crea la tabla de simbolos

class AnalizadorSemantico:
    """Analizador semantico que valida el uso de variables"""
    
    def __init__(self):
        # Tabla de simbolos: almacena las variables declaradas
        self.tabla_simbolos = {}
        
        # Listas de errores y advertencias
        self.errores = []
        self.warnings = []
    
    def analizar(self, arbol):
        """Analiza el arbol sintactico y valida semantica"""
        if arbol is None:
            return False
        
        # Limpiar analisis previo
        self.tabla_simbolos = {}
        self.errores = []
        self.warnings = []
        
        # Analizar el programa
        self.analizar_nodo(arbol)
        
        # Verificar variables no usadas
        self.verificar_variables_no_usadas()
        
        # Retornar si hubo errores
        return len(self.errores) == 0
    
    def analizar_nodo(self, nodo):
        """Analiza un nodo del arbol recursivamente"""
        if nodo is None:
            return
        
        # Segun el tipo de nodo, hacer diferente validacion
        if nodo.tipo == "Programa":
            # Analizar todas las sentencias
            for hijo in nodo.hijos:
                self.analizar_nodo(hijo)
        
        elif nodo.tipo == "Asignacion":
            # Una asignacion declara una variable
            self.analizar_asignacion(nodo)
        
        elif nodo.tipo == "Print":
            # Print usa una variable
            self.analizar_print(nodo)
        
        elif nodo.tipo == "Operacion":
            # Las operaciones pueden usar variables
            self.analizar_operacion(nodo)
        
        elif nodo.tipo == "Identificador":
            # Verificar que la variable exista
            self.verificar_variable_existe(nodo.valor)
    
    def analizar_asignacion(self, nodo):
        """Analiza una asignacion: x = expresion"""
        # El primer hijo es el identificador (variable)
        if len(nodo.hijos) < 2:
            return
        
        nombre_var = nodo.hijos[0].valor
        expresion = nodo.hijos[1]
        
        # Analizar la expresion (lado derecho)
        self.analizar_expresion(expresion)
        
        # Determinar el tipo de la expresion
        tipo = self.obtener_tipo(expresion)
        
        # Agregar variable a la tabla de simbolos
        if nombre_var in self.tabla_simbolos:
            # Variable ya existe, actualizar
            self.tabla_simbolos[nombre_var]['tipo'] = tipo
            self.tabla_simbolos[nombre_var]['declaraciones'] += 1
        else:
            # Variable nueva
            self.tabla_simbolos[nombre_var] = {
                'tipo': tipo,
                'usada': False,
                'declaraciones': 1
            }
    
    def analizar_print(self, nodo):
        """Analiza un print(expresion)"""
        if len(nodo.hijos) < 1:
            return
        
        # Analizar la expresion dentro del print
        expresion = nodo.hijos[0]
        self.analizar_expresion(expresion)
    
    def analizar_operacion(self, nodo):
        """Analiza una operacion aritmetica"""
        # Analizar ambos lados de la operacion
        for hijo in nodo.hijos:
            self.analizar_expresion(hijo)
    
    def analizar_expresion(self, nodo):
        """Analiza cualquier tipo de expresion"""
        if nodo is None:
            return
        
        if nodo.tipo == "Numero" or nodo.tipo == "Decimal":
            # Es un literal, no hace falta validar
            pass
        
        elif nodo.tipo == "Identificador":
            # Es una variable, verificar que exista
            self.verificar_variable_existe(nodo.valor)
        
        elif nodo.tipo == "Operacion":
            # Es una operacion, analizar recursivamente
            self.analizar_operacion(nodo)
    
    def verificar_variable_existe(self, nombre_var):
        """Verifica que una variable exista en la tabla de simbolos"""
        if nombre_var not in self.tabla_simbolos:
            # Error: variable no declarada
            self.errores.append(f"Variable '{nombre_var}' no esta declarada")
        else:
            # Marcar que la variable fue usada
            self.tabla_simbolos[nombre_var]['usada'] = True
    
    def verificar_variables_no_usadas(self):
        """Genera warnings para variables declaradas pero no usadas"""
        for nombre_var, info in self.tabla_simbolos.items():
            if not info['usada']:
                self.warnings.append(f"Variable '{nombre_var}' declarada pero nunca usada")
    
    def obtener_tipo(self, nodo):
        """Determina el tipo de una expresion"""
        if nodo is None:
            return "desconocido"
        
        if nodo.tipo == "Numero":
            return "int"
        elif nodo.tipo == "Decimal":
            return "float"
        elif nodo.tipo == "Identificador":
            # Buscar el tipo en la tabla de simbolos
            if nodo.valor in self.tabla_simbolos:
                return self.tabla_simbolos[nodo.valor]['tipo']
            return "desconocido"
        elif nodo.tipo == "Operacion":
            # El tipo de una operacion depende de los operandos
            tipo_izq = self.obtener_tipo(nodo.hijos[0]) if len(nodo.hijos) > 0 else "int"
            tipo_der = self.obtener_tipo(nodo.hijos[1]) if len(nodo.hijos) > 1 else "int"
            
            # Si alguno es float, el resultado es float
            if tipo_izq == "float" or tipo_der == "float":
                return "float"
            return "int"
        
        return "desconocido"
    
    def obtener_reporte(self):
        """Genera un reporte del analisis semantico"""
        reporte = ""
        
        # Mostrar si hay errores o no
        if self.errores:
            reporte += "ERRORES SEMANTICOS:\n\n"
            for error in self.errores:
                reporte += f"  • {error}\n"
            reporte += "\n"
        else:
            reporte += "Semantica correcta\n\n"
        
        # Mostrar warnings
        if self.warnings:
            reporte += "ADVERTENCIAS:\n\n"
            for warning in self.warnings:
                reporte += f"  • {warning}\n"
            reporte += "\n"
        
        # Mostrar tabla de simbolos
        if self.tabla_simbolos:
            reporte += "TABLA DE SIMBOLOS:\n\n"
            reporte += "┌─────────────┬───────┬─────────┐\n"
            reporte += "│ Variable    │ Tipo  │ Usada   │\n"
            reporte += "├─────────────┼───────┼─────────┤\n"
            
            for nombre, info in self.tabla_simbolos.items():
                usada = "Si" if info['usada'] else "No"
                simbolo = "" if info['usada'] else " ⚠️"
                reporte += f"│ {nombre:<11} │ {info['tipo']:<5} │ {usada:<7}{simbolo} │\n"
            
            reporte += "└─────────────┴───────┴─────────┘\n\n"
        
        # Estadisticas
        reporte += "ESTADISTICAS:\n"
        reporte += f"  • Variables declaradas: {len(self.tabla_simbolos)}\n"
        
        usadas = sum(1 for info in self.tabla_simbolos.values() if info['usada'])
        reporte += f"  • Variables usadas: {usadas}\n"
        
        reporte += f"  • Errores: {len(self.errores)}\n"
        reporte += f"  • Warnings: {len(self.warnings)}\n"
        
        return reporte