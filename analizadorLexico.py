import ply.lex as lex
import ply.yacc as yacc

class LexerAnalyzer:
    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self)
        self.errors = []
        self.variables = {}
        self.imp_outputs = []
        self.in_if_condition = False
        self.if_condition_result = False
        self.in_function = False
        

    tokens = [
        'IDENTIFICADOR', 'TIPO', 'PUNTOYCOMA', 'NUMERO', 'IGUAL', 'STRING',
        'FUN', 'MALPH', 'IMP', 'LBRACKET', 'RBRACKET', 'LPAREN', 'RPAREN', 'FUNCION',
        'VI', 'LBRACE', 'RBRACE', 'GT', 'LT', 'EQ','INCREMENTO', 'WAR'
    ]

    t_PUNTOYCOMA = r'\;'
    t_ignore = ' \t\n'
    t_IGUAL = r'\='
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_GT = r'\>'
    t_LT = r'\<'
    t_EQ = r'\=\='
    t_INCREMENTO = r'\+\+'

    def t_TIPO(self, t):
        r'int|string'
        return t

    def t_STRING(self, t):
        r'"[^"]*"'
        t.value = t.value[1:-1]
        return t

    def t_NUMERO(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_FUN(self, t):
        r'Fun'
        return t

    def t_VI(self, t):
        r'Vi'
        return t

    def t_MALPH(self, t):
        r'Malph'
        return t
    
    def t_WAR(self, t):
        r'War'
        return t

    def t_IMP(self, t):
        r'imp'
        return t

    def t_FUNCION(self, t):
        r'[A-Z][a-zA-Z_0-9]*'
        return t

    def t_IDENTIFICADOR(self, t):
        r'[a-z_][a-z_0-9]*'
        return t

    def t_error(self, t):
        print(f"Carácter desconocido '{t.value[0]}'")
        t.lexer.skip(1)

    def analyze(self, data):
        self.lexer.input(data)
        result = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            result.append((tok.type, tok.value))
        return result

    def parse(self, data):
        self.errors = []
        self.parser.parse(data)
        if self.errors:
            return False, self.errors
        return True, None

    def p_program(self, p):
        '''
        program : expression
                | program expression
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_expression(self, p):
        '''
        expression : variable_declaration
                   | variable_assignment
                   | main_function
                   | function_definition
                   | if_statement
                   | while_statement
                   
                   
        '''
        p[0] = p[1]

    def p_main_function(self, p): 
        '''
        main_function : FUN MALPH LBRACKET RBRACKET LPAREN imp_statement RPAREN
        '''
        self.in_function = True
        self.execute_imp(p[6])
        self.in_function = False

    def p_function_definition(self, p):
        '''
        function_definition : FUN FUNCION LBRACKET RBRACKET LPAREN imp_statement RPAREN
        '''
        self.in_function = True
        self.execute_imp(p[6])
        self.in_function = False

    def execute_imp(self, imp_data):
        action, identifier = imp_data
        if identifier:
            if identifier in self.variables:
                var_info = self.variables[identifier]
                tipo = var_info.get('tipo', 'Tipo desconocido')
                valor = var_info.get('valor', 'Valor no asignado')
                output = f"{identifier} ({tipo}): {valor}"
            else:
                output = f"{identifier}: Variable no declarada."
        else:
            output = "imp sin variable especificada."
        self.imp_outputs.append(output)
    
    
    def p_imp_statement(self, p):
        '''
        imp_statement : IMP IDENTIFICADOR PUNTOYCOMA
                    | IMP PUNTOYCOMA
        '''
        if len(p) == 4:
            p[0] = ('imp', p[2])  # Retorna una acción imp con una variable
        else:
            p[0] = ('imp', None)  # Retorna una acción imp sin variable

    def convert_if_number(self, operand):
        try:
            return int(operand)
        except ValueError:
            return operand

    def p_variable_declaration(self, p):
        '''
        variable_declaration : IDENTIFICADOR PUNTOYCOMA TIPO IGUAL valor
                             | IDENTIFICADOR PUNTOYCOMA TIPO
        '''
        if len(p) == 6:
            self.variables[p[1]] = {'tipo': p[3], 'valor': p[5]}
            p[0] = ('variable_declaration_assignment', p[1], p[3], p[5])
        else:
            self.variables[p[1]] = {'tipo': p[3], 'valor': None}
            p[0] = ('variable_declaration', p[1], p[3])

    def p_variable_assignment(self, p):
        '''
        variable_assignment : IDENTIFICADOR PUNTOYCOMA TIPO IGUAL valor
        '''
        tipo = p[3]
        valor = p[5]
        if tipo == "int":
            try:
                valor = int(valor)
            except ValueError:
                self.errors.append(f"Error: se esperaba un valor entero para la variable '{p[1]}'.")
                return
        self.variables[p[1]] = {'tipo': tipo, 'valor': valor}
        p[0] = ('variable_assignment', p[1], tipo, valor)

    def p_valor(self, p):
        '''
        valor : NUMERO
              | STRING
        '''
        p[0] = p[1]

    def p_if_statement(self, p):
        '''
        if_statement : VI LBRACE condition RBRACE LPAREN imp_statement RPAREN
        '''
    
        condition_result = self.evaluate_condition(p[3])
        print(condition_result)
        if condition_result:
            print('si llego')
            self.execute_imp(p[6])

    def p_condition(self, p):
        '''
        condition : IDENTIFICADOR GT IDENTIFICADOR
                  | IDENTIFICADOR GT NUMERO
                  | NUMERO GT IDENTIFICADOR
                  | IDENTIFICADOR LT IDENTIFICADOR
                  | IDENTIFICADOR LT NUMERO
                  | NUMERO LT IDENTIFICADOR
                  | IDENTIFICADOR EQ IDENTIFICADOR
                  | IDENTIFICADOR EQ NUMERO
                  | NUMERO EQ IDENTIFICADOR
        '''
        p[0] = ('condition', p[1], p[2], p[3])

    def evaluate_condition(self, condition):
        _, left, operator, right = condition

        
        def get_value(val):
            if isinstance(val, str):
                
                if val in self.variables:
                    return self.variables[val]['valor']
                try:
                    
                    return int(val)
                except ValueError:
                    
                    return val
            else:
                
                return val

        left_val = get_value(left)
        right_val = get_value(right)

        if operator == '>':
            return left_val > right_val
        elif operator == '<':
            return left_val < right_val
        elif operator == '==':
            return left_val == right_val
        else:
            return False
        
    def p_while_statement(self, p):
        '''
        while_statement : WAR LBRACE condition RBRACE LPAREN imp_statement INCREMENTO IDENTIFICADOR PUNTOYCOMA RPAREN
        '''
        condition_result = self.evaluate_condition(p[3])
        while condition_result:
            self.execute_imp(p[6])
            # Incrementa la variable especificada en p[8]
            if p[8] in self.variables:
                if 'valor' in self.variables[p[8]] and isinstance(self.variables[p[8]]['valor'], int):
                    self.variables[p[8]]['valor'] += 1
                else:
                    self.errors.append(f"Error: la variable '{p[8]}' no es un entero o no está definida.")
            else:
                self.errors.append(f"Error: la variable '{p[8]}' no está definida.")
            condition_result = self.evaluate_condition(p[3])
    
    
    def p_error(self, p):
        if p:
            error_msg = f"Error de sintaxis en '{p.value}', línea {p.lineno}"
            self.errors.append(error_msg)
            print(error_msg)
        else:
            self.errors.append("Error de sintaxis al final del archivo")