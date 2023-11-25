# ------------------------------------------------------------
# Lexer para C
# ------------------------------------------------------------
import ply.lex as lex

S = 0
S2 = 1
T = 2
T2 = 3
F = 4

# List of token names. This is always required
tokens = (
    "NUMBER",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "LPAREN",
    "RPAREN",
    "keyword",
    "identificador",
    "inicioBloque",
    "finBloque",
    "finInstruccion",
    "asignacion",
    "comentario",
    "comentario_bloque",
    "cadena",
    "coma",
    "eof",
    "int",
    "float"
    #'vacia'
)

# Regular expression rules for simple tokens
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_inicioBloque = r"\{"
t_finBloque = r"\}"
t_finInstruccion = r"\;"
t_asignacion = r"\="
t_coma = r"\,"
t_eof = r"\$"


# t_vacia= r'\'


def t_int(t):
    r"(int)"
    return t


def t_float(t):
    r"(float)"
    return t


# A regular expression rule with some action code
def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = " \t"


def t_keyword(t):
    r"(char)|(return)|(if)|(else)|(do)|(while)|(for)|(void)"
    return t


def t_identificador(t):
    r"([a-z]|[A-Z]|_)([a-z]|[A-Z]|\d|_)*"
    return t


def t_cadena(t):
    r"\".*\" "
    return t


def t_comentario(t):
    r"\/\/.*"
    return t


def t_comentario_bloque(t):
    r"\/\*(.|\n)*\*\/"
    # return t


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    return t


TT = 1
D = 2
tabla = [
    [S, "identificador", None],
    [S, "int", [TT, "identificador", D]],
    [S, "float", [TT, "identificador", D]],
    [S, "coma", None],
    [S, "finInstruccion", None],
    [TT, "identificador", None],
    [TT, "int", ["int"]],
    [TT, "float", ["float"]],
    [TT, "coma", None],
    [TT, "finInstruccion", None],
    [D, "identificador", None],
    [D, "int", None],
    [D, "float", None],
    [D, "coma", ["coma", "identificador", D]],
    [D, "finInstruccion", ["finInstruccion"]],
]

stack = ["eof", 0]


# Build the lexer
lexer = lex.lex()


def miParser():
    # f = open('fuente.c','r')
    # lexer.input(f.read())
    # lexer.input("int a, b c;$")
    lexer.input("int a, c;$")

    tok = lexer.token()
    x = stack[-1]  # primer elemento de der a izq (Ultimo elemento)
    while True:
        if x == tok.type and x == "eof":
            print("Cadena reconocida exitosamente")
            return  # aceptar
        else:
            if x == tok.type and x != "eof":
                stack.pop()
                x = stack[-1]
                tok = lexer.token()
            if x in tokens and x != tok.type:
                print("Error: se esperaba ", tok.type)
                return 0
            if x not in tokens:  # es no terminal
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
                    print(stack)
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
        if elemento != "vacia":  # la vacía no la inserta
            stack.append(elemento)


miParser()
