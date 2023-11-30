import ply.lex as lex
from gramaticas import general_table

# reserved words list:
reserved = {
    "int": "INT",
    "char": "CHAR",
    "string": "STRING",
    "float": "FLOAT",
    "void": "VOID",
    "if": "IF",
    "else": "ELSE",
    "return": "RETURN",
    "while": "WHILE",
    "printf": "PRINTF",
    "scanf": "SCANF",
}

# token list
tokens = [
    "IDENTIFIER",
    "EQUAL",
    "LESS_THAN",
    "GREATER_THAN",
    "LEFT_PARENTHESIS",
    "RIGHT_PARENTHESIS",
    "LEFT_BLOCK",
    "RIGHT_BLOCK",
    "COMMENT",
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
    "CHAR_DEFINITION",
    "EOF",
    "INCLUDE",
    "AMPERSAND",
] + list(reserved.values())

# Regular expressions


def t_IDENTIFIER(t):
    r"[a-zA-Z_][a-zA-Z_0-9.]*"
    t.type = reserved.get(t.value, "IDENTIFIER")  # Check for reserved words
    return t


t_EQUALS = r"\=\="
t_EQUAL = r"\="
t_LESS_THAN = r"\<"
t_GREATER_THAN = r"\>"
t_LEFT_PARENTHESIS = r"\("
t_RIGHT_PARENTHESIS = r"\)"
t_LEFT_BLOCK = r"\{"
t_RIGHT_BLOCK = r"\}"


def t_COMMENT(t):
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
t_OR = r"\|\|"
t_NOT = r"\!"
t_INSTRUCTION_END = r"\;"


def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


t_COMMA = r"\,"


def t_STRING_DEFINITION(t):
    r'"([^"]*)"'
    return t


def t_CHAR_DEFINITION(t):
    r'"(.)"'
    return t


t_EOF = r"\$"

t_INCLUDE = r"\#include"
t_AMPERSAND = r"\&"


# Track line numbers
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# Ignored characters (spaces and tabs)
t_ignore = " \t"


# Error handling rule (Token not defined)
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
Ov = 6
V = 7
Vp = 8
N = 9
Np = 10
Val = 11
Dt = 12
I = 13
Ip = 14
M = 15
C = 16
Ol = 161
Cp = 17
B = 18
F = 19
Fp = 20
G = 21
P = 22
Pp = 23
Dtp = 231
L = 24
Lp = 25
R = 26
Sc = 27
Pr = 28
W = 29
A = 30
D = 31
E = 32

# Gramaticas
tabla = general_table


stack = ["EOF", 0]

# Lexer
lexer = lex.lex()
f = open("c_example_full.c", "r")
file_content = f.read()
file_content += "$"
lexer.input(file_content)

currentToken = lexer.token()
x = stack[-1]  # primer elemento de der a izq (Ultimo elemento)
errorCount = 0


def executeCustomParser():
    global x
    global currentToken
    global lexer
    global stack
    global errorCount

    while True:
        if x == currentToken.type and x == "EOF":
            print("File recognized successfully with ", errorCount, " errors.")
            return
        else:
            if x == currentToken.type and x != "EOF":
                # X es el token esperado y no ha terminado
                print("Current X: ", x)
                print("Expected type: ", currentToken.type)
                print("\n")

                stack.pop()
                x = stack[-1]
                currentToken = lexer.token()
            if x in tokens and x != currentToken.type:
                # X es un token pero no el esperado
                handle_error()
            if x not in tokens:  # X es no terminal
                print("\n")
                print("Non terminal found: ", x)
                print("Current Token: " + str(currentToken))
                print("\n")

                celda = buscar_en_tabla(x, currentToken.type)

                if celda is None:
                    handle_error()
                else:
                    print("Found matching Pair")
                    stack.pop()
                    agregar_pila(celda)
                    print("New Stack State: ", stack)
                    print("\n")
                    x = stack[-1]


synchronization_tokens = [
    "INSTRUCTION_END",
    "RIGHT_PARENTHESIS",
    "RIGHT_BLOCK",
    "RETURN",
    "EOF",
]


def handle_error():
    global x
    global currentToken
    global lexer
    global stack
    global synchronization_tokens
    global errorCount

    errorCount += 1
    print("Found error!")
    print("Triggering panic mode...")
    print("Current stack: ", stack)

    recoveredFromError = False
    recoveryIterations = 1
    while not recoveredFromError:
        if not currentToken:
            # No more tokens left :(
            return

        print("Recovery iteration number: ", recoveryIterations)
        recoveryIterations += 1

        hasFoundSyncTokenInTokens = False
        hasTokensLeft = True
        while not hasFoundSyncTokenInTokens and hasTokensLeft:
            print("Evaluating token: ", currentToken)
            # No tokens left
            # Cannot recover
            if not currentToken:
                hasTokensLeft = False
                print("Cannot recover from error")
                return

            if currentToken.type == "EOF":
                print("Did not find sync tokens")
                print("Proceeding to end parsing.")
                x = currentToken.type
                return

            # Can recover from this error
            # Current token is a sync token
            if currentToken.type in synchronization_tokens:
                print("Token is candidate for recovery.")
                hasFoundSyncTokenInTokens = True
                break

            # Token is not sync token
            # Get next token
            currentToken = lexer.token()

        hasFoundMatchingSyncToken = False
        if currentToken.type in stack:
            print("Token is in current stack...")
            while len(stack) > 0:
                if stack[-1] == currentToken.type:
                    hasFoundMatchingSyncToken = True
                    recoveredFromError = True
                    break
                else:
                    stack.pop()
        else:
            print("Token is not in current stack.")
            currentToken = lexer.token()
            continue

        if hasFoundMatchingSyncToken:
            x = currentToken.type
            print("Proceeding to recover with token: ", currentToken)
            print("New Stack: ", stack)
            print("New x: ", x)
            return


def buscar_en_tabla(no_terminal, terminal):
    # Returns the array for said pair (Or null if not found)
    print("Retrieving Cell: [", no_terminal, "][", terminal, "]")
    for i in range(len(tabla)):
        if tabla[i][0] == no_terminal and tabla[i][1] == terminal:
            return tabla[i][2]


def agregar_pila(produccion):
    for elemento in reversed(produccion):
        if elemento != "VACIA":  # la vacía no la inserta
            stack.append(elemento)
        else:
            print("--------------")
            print("-Found VACIA-")
            print("--------------")


executeCustomParser()
