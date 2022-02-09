import ply.lex as lex
import ply.yacc as yacc
import sys
# (Sintaxis) - lex
# Reserverd works -- tokens
# Se usa este diccionario para obtener el token
keywords = {
    'program': 'PROGRAM',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'print': 'PRINT',
    'if': 'IF',
    'else': 'ELSE',
}

# tokens
tokens = [
    'PARENTHESESOPEN', 'PARENTHESESCLOSE', 'BRACEOPEN', 'BRACECLOSE',
    'PLUS', 'MINUS', 'TIMES', 'DIVISION',
    'GREATER', 'LESS', 'DIFFERENT',
    'COLON', 'EQUAL', 'SEMICOLON', 'COMMA',
    'CTEF', 'CTEI', 'CTESTRING',
    'ID'
]
# Add reserved words to list of tokens
tokens += list(keywords.values())

# ==================================================================
# Define regex for tokens

t_PARENTHESESOPEN = r'\('
t_PARENTHESESCLOSE = r'\)'
t_BRACEOPEN = r'\{'
t_BRACECLOSE = r'\}'

t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVISION = r'\/'

t_GREATER = r'\>'
t_LESS = r'\<'
t_DIFFERENT = r'\<>'

t_COLON = r'\:'
t_EQUAL = r'\='
t_SEMICOLON = r'\;'
t_COMMA = r'\,'
t_CTESTRING = r'\".*\"'

# Ignored characters 
t_ignore = " \t"


# SPECIFICATION OF TOKENS
# Tokens ID
def t_ID(t):
    r'[A-za-z]([A-za-z]|[0-9])*'
    t.type = keywords.get(t.value, 'ID')
    return t
# Tokens float constants
def t_CTEF(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t
# Tokens int constants
def t_CTEI(t):
    r'\d+'
    t.value = int(t.value)
    return t
# Define a new line or multiple new lines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
# Tokens error
def t_error(t):
    print("Error: character invalid", t)
    t.lexer.skip(1)

# Build the lexer
lex.lex()
    

# ==================================================================
# (Semántica) - yacc
# 

# PROGRAM
def p_program(p):
    '''program : PROGRAM ID SEMICOLON bloque
        | PROGRAM ID SEMICOLON vars bloque'''
    p[0] = 'correct'

# VARS
def p_vars(p):
    '''vars : VAR vars_prima_1'''

def p_vars_prima_1(p):
    '''vars_prima_1 : vars_prima_2 COLON tipo SEMICOLON vars_prima_1 
        | vars_prima_2 COLON tipo SEMICOLON'''

def p_vars_prima_2(p):
    '''vars_prima_2 : ID 
        | ID COMMA vars_prima_2'''

# TIPO
def p_tipo(p):
    '''tipo : INT
        | FLOAT'''

# BLOQUE
def p_bloque(p):
    '''bloque : BRACEOPEN bloque_prima_1'''

def p_bloque_prima_1(p):
    '''bloque_prima_1 : estatuto bloque_prima_1
        | BRACECLOSE'''

# ESTATUTO
def p_estatuto(p):
    '''estatuto : asignacion
        | condicion
        | escritura'''

# ASIGNACION
def p_asignacion(p):
    '''asignacion : ID EQUAL expresion SEMICOLON'''

# EXPRESION
def p_expresion(p):
    '''expresion : exp
        | exp LESS exp
        | exp GREATER exp
        | exp DIFFERENT exp
    '''

# EXP
def p_exp(p):
    '''exp : termino exp
        | termino PLUS
        | termino MINUS
        | termino'''

# TERMINO
def p_termino(p):
    '''termino : factor termino
        | factor TIMES
        | factor DIVISION
        | factor'''

# factor
def p_factor(p):
    '''factor : PARENTHESESOPEN expresion PARENTHESESCLOSE
        | factor_prima_1'''

def p_factor_prima_1(p):
    '''factor_prima_1 : PLUS varcte
        | MINUS varcte
        | varcte'''

# CONDICION
def p_condicion(p):
    '''condicion : condicion_prima_1 bloque SEMICOLON
        | condicion_prima_1 bloque ELSE bloque SEMICOLON'''

def p_condicion_prima_1(p):
    '''condicion_prima_1 : IF PARENTHESESOPEN expresion PARENTHESESCLOSE'''

# ESCRITURA
def p_escritura(p):
    '''escritura : PRINT PARENTHESESOPEN escritura_prima_1 PARENTHESESCLOSE SEMICOLON'''

def p_escritura_prima_1(p):
    '''escritura_prima_1 : expresion
        | expresion COMMA escritura_prima_1
        | CTESTRING
        | CTESTRING COMMA'''

# varcte
def p_varcte(p):
    '''varcte : ID
        | CTEI
        | CTEF'''


# Error rule for syntax errors
def p_error(p):
   print("Archivo inválido \n error de sintaxis", p)


# Build the parser
yacc.yacc()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = sys.argv[1]
        try:
            f = open(file, 'r')
            data = f.read()
            f.close()
            if yacc.parse(data) == "correct":
                print("Archivo válido")
        except EOFError:
            print(EOFError)
    else:
        print("No file was found")