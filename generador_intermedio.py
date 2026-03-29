# Generador de Codigo Intermedio
# Genera codigo de tres direcciones (TAC - Three Address Code)

class GeneradorCodigoIntermedio:
    """Genera codigo intermedio en formato TAC"""
    
    def __init__(self):
        self.codigo = []  # Lista de instrucciones TAC
        self.temp_count = 0  # Contador de temporales
    
    def generar(self, arbol):
        """Genera el codigo intermedio completo"""
        if arbol is None:
            return "// Error: No hay arbol para generar codigo"
        
        # Limpiar codigo anterior
        self.codigo = []
        self.temp_count = 0
        
        # Generar codigo del programa
        self.generar_nodo(arbol)
        
        # Retornar codigo generado
        return "\n".join(self.codigo)
    
    def nuevo_temporal(self):
        """Genera un nuevo temporal: t1, t2, t3..."""
        self.temp_count += 1
        return f"t{self.temp_count}"
    
    def generar_nodo(self, nodo):
        """Genera codigo para un nodo del arbol"""
        if nodo is None:
            return None
        
        if nodo.tipo == "Programa":
            # Generar codigo para todas las sentencias
            for hijo in nodo.hijos:
                self.generar_nodo(hijo)
        
        elif nodo.tipo == "Asignacion":
            return self.generar_asignacion(nodo)
        
        elif nodo.tipo == "Print":
            return self.generar_print(nodo)
    
    def generar_asignacion(self, nodo):
        """Genera codigo para una asignacion: x = expresion"""
        # Obtener el nombre de la variable
        nombre_var = nodo.hijos[0].valor
        
        # Generar codigo de la expresion del lado derecho
        temp_expr = self.generar_expresion(nodo.hijos[1])
        
        # Generar instruccion de asignacion
        self.codigo.append(f"{nombre_var} = {temp_expr}")
        
        return nombre_var
    
    def generar_print(self, nodo):
        """Genera codigo para print(expresion)"""
        # Generar codigo de la expresion
        temp = self.generar_expresion(nodo.hijos[0])
        
        # Generar instruccion PRINT
        self.codigo.append(f"PRINT {temp}")
        
        return temp
    
    def generar_expresion(self, nodo):
        """Genera codigo para una expresion y retorna el temporal/variable"""
        if nodo is None:
            return ""
        
        if nodo.tipo == "Numero":
            # Es un numero literal
            return nodo.valor
        
        elif nodo.tipo == "Decimal":
            # Es un decimal literal
            return nodo.valor
        
        elif nodo.tipo == "Identificador":
            # Es una variable
            return nodo.valor
        
        elif nodo.tipo == "Operacion":
            # Es una operacion binaria
            return self.generar_operacion(nodo)
        
        return ""
    
    def generar_operacion(self, nodo):
        """Genera codigo para una operacion binaria"""
        # Generar codigo para el operando izquierdo
        temp_izq = self.generar_expresion(nodo.hijos[0])
        
        # Generar codigo para el operando derecho
        temp_der = self.generar_expresion(nodo.hijos[1])
        
        # Obtener el operador
        operador = nodo.valor
        
        # Crear un nuevo temporal para el resultado
        temp_resultado = self.nuevo_temporal()
        
        # Generar instruccion de tres direcciones
        self.codigo.append(f"{temp_resultado} = {temp_izq} {operador} {temp_der}")
        
        return temp_resultado


def generar_codigo_intermedio(arbol):
    """Funcion auxiliar para generar codigo intermedio facilmente"""
    generador = GeneradorCodigoIntermedio()
    return generador.generar(arbol)