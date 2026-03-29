class Token:
    """Representa un token del analisis lexico"""
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor
    
    def __repr__(self):
        return f"Token({self.tipo}, '{self.valor}')"


class NodoArbol:
    """Nodo del arbol sintactico"""
    def __init__(self, tipo, valor=None, hijos=None):
        self.tipo = tipo
        self.valor = valor
        self.hijos = hijos if hijos else []
    
    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)
    
    def __repr__(self):
        if self.valor:
            return f"{self.tipo}({self.valor})"
        return f"{self.tipo}"


class AnalizadorSintactico:
    """Analizador sintactico descendente recursivo"""
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errores = []
    
    def token_actual(self):
        """Retorna el token actual sin avanzar"""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def avanzar(self):
        """Avanza al siguiente token"""
        self.pos += 1
    
    def esperar(self, tipo_esperado):
        """Verifica que el token actual sea del tipo esperado y avanza"""
        token = self.token_actual()
        if token is None:
            self.errores.append(f"Error: Se esperaba '{tipo_esperado}' pero se llego al final")
            return False
        
        if token.tipo != tipo_esperado:
            self.errores.append(f"Error: Se esperaba '{tipo_esperado}' pero se encontro '{token.tipo}' ('{token.valor}')")
            return False
        
        self.avanzar()
        return True
    
    def analizar(self):
        """Punto de entrada del analisis sintactico"""
        try:
            arbol = self.programa()
            
            # Verificar que se consumieron todos los tokens
            if self.token_actual() is not None:
                self.errores.append(f"Error: Tokens extra despues del final del programa")
            
            return arbol, self.errores
        except Exception as e:
            self.errores.append(f"Error de analisis: {str(e)}")
            return None, self.errores
    
    # ==================== REGLAS GRAMATICALES ====================
    
    def programa(self):
        """Programa → Sentencia+"""
        nodo = NodoArbol("Programa")
        
        # Debe haber al menos una sentencia
        if self.token_actual() is None:
            self.errores.append("Error: Programa vacio")
            return nodo
        
        # Analizar todas las sentencias
        while self.token_actual() is not None:
            sentencia = self.sentencia()
            if sentencia:
                nodo.agregar_hijo(sentencia)
            else:
                # Si hubo error, intentar recuperarse
                break
        
        return nodo
    
    def sentencia(self):
        """Sentencia → Asignacion | Print | Expresion"""
        token = self.token_actual()
        
        if token is None:
            return None
        
        # Si es print
        if token.tipo == "PRINT":
            return self.print_stmt()
        
        # Si es un identificador, podría ser asignación o expresión
        if token.tipo == "IDENTIFICADOR":
            # Mirar el siguiente token (lookahead)
            if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].tipo == "ASIGNACION":
                return self.asignacion()
            else:
                return self.expresion()
        else:
            # Si no es identificador, solo puede ser expresión
            return self.expresion()
    
    def asignacion(self):
        """Asignacion → IDENTIFICADOR '=' Expresion"""
        nodo = NodoArbol("Asignacion")
        
        # Obtener el identificador
        token = self.token_actual()
        if token.tipo != "IDENTIFICADOR":
            self.errores.append(f"Error: Se esperaba un identificador en asignación")
            return None
        
        nodo_id = NodoArbol("Identificador", token.valor)
        nodo.agregar_hijo(nodo_id)
        self.avanzar()
        
        # Esperar '='
        if not self.esperar("ASIGNACION"):
            return None
        
        # Analizar la expresión
        expr = self.expresion()
        if expr:
            nodo.agregar_hijo(expr)
        
        return nodo
    
    def expresion(self):
        """Expresion → Termino (('+' | '-') Termino)*"""
        nodo = self.termino()
        
        if nodo is None:
            return None
        
        # Mientras haya + o -
        while self.token_actual() and self.token_actual().tipo in ["SUMA", "RESTA"]:
            operador = self.token_actual()
            self.avanzar()
            
            termino_derecho = self.termino()
            if termino_derecho is None:
                self.errores.append(f"Error: Se esperaba un termino despues de '{operador.valor}'")
                return None
            
            # Crear nodo operador
            nodo_op = NodoArbol("Operacion", operador.valor)
            nodo_op.agregar_hijo(nodo)
            nodo_op.agregar_hijo(termino_derecho)
            nodo = nodo_op
        
        return nodo
    
    def termino(self):
        """Termino → Factor (('*' | '/') Factor)*"""
        nodo = self.factor()
        
        if nodo is None:
            return None
        
        # Mientras haya * o /
        while self.token_actual() and self.token_actual().tipo in ["MULTIPLICACION", "DIVISION"]:
            operador = self.token_actual()
            self.avanzar()
            
            factor_derecho = self.factor()
            if factor_derecho is None:
                self.errores.append(f"Error: Se esperaba un factor despues de '{operador.valor}'")
                return None
            
            # Crear nodo operador
            nodo_op = NodoArbol("Operacion", operador.valor)
            nodo_op.agregar_hijo(nodo)
            nodo_op.agregar_hijo(factor_derecho)
            nodo = nodo_op
        
        return nodo
    
    def factor(self):
        """Factor → NUMERO | DECIMAL | IDENTIFICADOR | '(' Expresion ')'"""
        token = self.token_actual()
        
        if token is None:
            self.errores.append("Error: Se esperaba un factor pero se llego al final")
            return None
        
        # Caso 1: Número
        if token.tipo == "NUMERO":
            nodo = NodoArbol("Numero", token.valor)
            self.avanzar()
            return nodo
        
        # Caso 2: Decimal
        elif token.tipo == "DECIMAL":
            nodo = NodoArbol("Decimal", token.valor)
            self.avanzar()
            return nodo
        
        # Caso 3: Identificador (variable)
        elif token.tipo == "IDENTIFICADOR":
            nodo = NodoArbol("Identificador", token.valor)
            self.avanzar()
            return nodo
        
        # Caso 4: Expresión entre paréntesis
        elif token.tipo == "PARENTESIS_IZQ":
            self.avanzar()  # Consumir '('
            
            nodo = self.expresion()
            
            if not self.esperar("PARENTESIS_DER"):
                self.errores.append("Error: Falta parentesis de cierre ')'")
                return None
            
            return nodo
        
        # Error: token inesperado
        else:
            self.errores.append(f"Error: Token inesperado '{token.tipo}' ('{token.valor}')")
            return None
    
    def print_stmt(self):
        """Print → 'print' '(' Expresion ')'"""
        # Consumir 'print'
        self.avanzar()
        
        # Esperar '('
        if not self.esperar("PARENTESIS_IZQ"):
            self.errores.append("Error: Se esperaba '(' despues de print")
            return None
        
        # Analizar la expresión dentro del print
        expr = self.expresion()
        
        if expr is None:
            self.errores.append("Error: Se esperaba una expresion dentro de print")
            return None
        
        # Esperar ')'
        if not self.esperar("PARENTESIS_DER"):
            self.errores.append("Error: Se esperaba ')' para cerrar print")
            return None
        
        # Crear nodo print
        nodo_print = NodoArbol("Print")
        nodo_print.agregar_hijo(expr)
        
        return nodo_print


def parsear_tokens(salida_lexico):
    """Convierte la salida del analizador lexico en lista de tokens"""
    tokens = []
    lineas = salida_lexico.strip().split('\n')
    
    for linea in lineas:
        linea = linea.strip()
        if not linea or linea.startswith('---'):
            continue
        
        if ':' in linea:
            partes = linea.split(':', 1)
            tipo = partes[0]
            valor = partes[1] if len(partes) > 1 else ''
            
            if tipo != "ERROR":
                tokens.append(Token(tipo, valor))
    
    return tokens


def imprimir_arbol(nodo, nivel=0, prefijo=""):
    """Imprime el arbol sintactico de forma visual"""
    if nodo is None:
        return ""
    
    resultado = ""
    indent = "  " * nivel
    
    if nodo.valor:
        resultado += f"{indent}{prefijo}{nodo.tipo}: {nodo.valor}\n"
    else:
        resultado += f"{indent}{prefijo}{nodo.tipo}\n"
    
    for i, hijo in enumerate(nodo.hijos):
        es_ultimo = (i == len(nodo.hijos) - 1)
        prefijo_hijo = "└─ " if es_ultimo else "├─ "
        resultado += imprimir_arbol(hijo, nivel + 1, prefijo_hijo)
    
    return resultado