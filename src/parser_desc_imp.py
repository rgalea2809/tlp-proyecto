import ply.lex as lex

# reserved words list:
reserved = {
    "int": "INT",
    "char": "CHAR",
    "float": "FLOAT",
    "void": "VOID",
    "if": "IF",
    "else": "ELSE",
    "return": "RETURN",
    "while": "WHILE",
    "printf": "PRINTF",
    "fgets": "FGETS",
    "stdin": "STDIN",
    "#include": "INCLUDE",
}

# token list
tokens = [
    "IDENTIFIER",
    "EQUAL",
    "LEFT_PARENTHESIS",
    "RIGHT_PARENTHESIS",
    "LEFT_BLOCK",
    "RIGHT_BLOCK",
    "LINE_COMMENT",
    "BLOCK_COMMENT",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "AND",
    "OR",
    "NOT",
    "EQUALS",
    "INSTRUCTION_END",
    "NUMBER",
    "COMMA",
    "STRING_DEFINITION",
    "EOF",
] + list(reserved.values())

# Regular expressions


def t_IDENTIFIER(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = reserved.get(t.value, "IDENTIFIER")  # Check for reserved words
    return t


t_EQUAL = r"\="
t_LEFT_PARENTHESIS = r"\("
t_RIGHT_PARENTHESIS = r"\("
t_LEFT_BLOCK = r"\{"
t_RIGHT_BLOCK = r"\}"


def t_LINE_COMMENT(t):
    r"\/\/.*"
    return t


def t_BLOCK_COMMENT(t):
    r"\/\*(.|\n)*\*\/"
    return t


t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_AND = r"&&"
t_OR = r"\|"
t_NOT = r"\!"
t_EQUALS = r"\=\="
t_INSTRUCTION_END = r"\;"


def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


t_COMMA = r"\,"


def t_STRING_DEFINITION(t):
    r"^\"(.+)\"$"
    return t


t_EOF = r"\$"


# Track line numbers
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# Ignored characters (spaces and tabs)
t_ignore = " \t"


# Error handling rule
# TODO: Implement this
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    return t


# No Terminales
S = 0
Sp = 1
O = 2
Op = 3
T = 4
Tp = 5
F = 6
Fp = 7
V = 8
Vp = 9
N = 10
Np = 11
Val = 12
Dt = 13
I = 14
Ip = 15
M = 16
C = 17
Cp = 18
B = 19
G = 20
P = 21
Pp = 22
L = 23
Lp = 24
R = 25
Sc = 26
Pr = 27
W = 28
A = 29
D = 30
E = 31

# Tabla de gramaticas
general_table = [
    [S, "EOF", None],
    [S, "#INCLUDE", ["#INCLUDE", "LESS_THAN", "IDENTIFIER", "GREATER_THAN", Sp]],
    [S, "LEFT_PARENTHESIS", None],
    [S, "RIGHT_PARENTHESIS", None],
    [S, "COMMENT", ["#INCLUDE", "LESS_THAN", "IDENTIFIER", "GREATER_THAN", Sp]],
]

tabla = [
    [S, "IDENTIFIER", None],
    [S, "INT", [Tp, "IDENTIFIER", D]],
    [S, "FLOAT", [Tp, "IDENTIFIER", D]],
    [S, "COMMA", None],
    [S, "INSTRUCTION_END", None],
    [Tp, "IDENTIFIER", None],
    [Tp, "INT", ["INT"]],
    [Tp, "FLOAT", ["FLOAT"]],
    [Tp, "COMMA", None],
    [Tp, "INSTRUCTION_END", None],
    [D, "IDENTIFIER", None],
    [D, "INT", None],
    [D, "FLOAT", None],
    [D, "COMMA", ["COMMA", "IDENTIFIER", D]],
    [D, "INSTRUCTION_END", ["INSTRUCTION_END"]],
]

stack = ["EOF", 0]

# Lexer
lexer = lex.lex()


def executeCustomParser():
    # f = open('fuente.c','r')
    # lexer.input(f.read())
    # lexer.input("int a, b c;$")

    lexer.input("int a, c;$")

    tok = lexer.token()
    x = stack[-1]  # primer elemento de der a izq (Ultimo elemento)

    while True:
        if x == tok.type and x == "EOF":
            print("Cadena reconocida exitosamente")
            return  # aceptar
        else:
            if x == tok.type and x != "EOF":
                stack.pop()
                x = stack[-1]
                tok = lexer.token()
            if x in tokens and x != tok.type:
                print("Error: se esperaba ", tok.type)
                return 0
            if x not in tokens:  # X es no terminal
                print("Non terminal found...")
                print("X: " + str(x))
                print("Token type: " + str(tok.type))
                print("Token: " + str(tok))

                celda = buscar_en_tabla(x, tok.type)

                if celda is None:
                    print("Error: No se esperaba ", tok.type)
                    print("En posición: ", tok.lexpos)

                    return 0
                else:
                    stack.pop()
                    agregar_pila(celda)
                    print("New Stack State: ", stack)
                    print("------------")
                    x = stack[-1]

        # if not tok:
        # break
        # print(tok)
        # print(tok.type, tok.value, tok.lineno, tok.lexpos)


def buscar_en_tabla(no_terminal, terminal):
    for i in range(len(tabla)):
        if tabla[i][0] == no_terminal and tabla[i][1] == terminal:
            return tabla[i][2]  # retorno la celda


def agregar_pila(produccion):
    for elemento in reversed(produccion):
        if elemento != "VACIA":  # la vacía no la inserta
            stack.append(elemento)


executeCustomParser()
