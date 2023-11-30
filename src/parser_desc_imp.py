import ply.lex as lex
import json
from tabulate import tabulate
from gramaticas import general_table


# Definición de Tabla Hash
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity

    def _hash(self, key):
        return hash(key) % self.capacity

    def insert(self, key, value):
        index = self._hash(key)

        if self.table[index] is None:
            self.table[index] = Node(key, value)
            self.size += 1
        else:
            current = self.table[index]
            while current:
                if current.key == key:
                    current.value = value
                    return
                current = current.next
            new_node = Node(key, value)
            new_node.next = self.table[index]
            self.table[index] = new_node
            self.size += 1

    def search(self, key):
        index = self._hash(key)

        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next

        raise KeyError(key)

    def remove(self, key):
        index = self._hash(key)

        previous = None
        current = self.table[index]

        while current:
            if current.key == key:
                if previous:
                    previous.next = current.next
                else:
                    self.table[index] = current.next
                self.size -= 1
                return
            previous = current
            current = current.next

        raise KeyError(key)

    def __len__(self):
        return self.size

    def __contains__(self, key):
        try:
            self.search(key)
            return True
        except KeyError:
            return False

    def printProperties(self):
        print("Length: " + str(self.size))


# ANSI color codes
class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    RESET = "\033[0m"


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
tokenCount = 0
retrievedTokensList = []
errorsList = []


def executeCustomParser():
    global x
    global currentToken
    global lexer
    global stack
    global errorCount
    global tokenCount
    global retrievedTokensList

    print(f"{Colors.CYAN}Starting syntax check... \n{Colors.RESET}")
    retrievedTokensList.append(currentToken)
    tokenCount += 1

    while True:
        if x == currentToken.type and x == "EOF":
            perform_end_action()
            return
        else:
            if x == currentToken.type and x != "EOF":
                # X es el token esperado y no ha terminado
                print("Expected type: ", currentToken.type)
                print("Current X: ", x)
                print("\n")

                stack.pop()
                x = stack[-1]

                currentToken = lexer.token()
                retrievedTokensList.append(currentToken)
                tokenCount += 1
            if x in tokens and x != currentToken.type:
                # X es un token pero no el esperado
                handle_error()
            if x not in tokens:  # X es no terminal
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
    "INT",
    "CHAR",
    "STRING",
    "FLOAT",
    "IF",
    "ELSE",
]


def handle_error():
    global x
    global currentToken
    global lexer
    global stack
    global synchronization_tokens
    global errorCount
    global tokenCount
    global retrievedTokensList
    global errorsList

    errorCount += 1
    errorsList.append([currentToken, stack])

    print("\n")
    print("----------------->")
    print(
        f"{Colors.RED}Syntax error found at{Colors.RESET}",
        f"{Colors.RED}line",
        currentToken.lineno,
        ", position ",
        currentToken.lexpos,
        f"{Colors.RESET}",
    )
    print(f"{Colors.RED}Triggering panic mode...{Colors.RESET}")
    print(f"{Colors.YELLOW}Current stack: ", stack, f"{Colors.RESET}")
    print("\n")

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
                print("<-----------------")
                return

            if currentToken.type == "EOF":
                print("Did not find sync tokens.")
                print("Proceeding to end parsing.")
                print("<-----------------")
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
            retrievedTokensList.append(currentToken)
            tokenCount += 1

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
            retrievedTokensList.append(currentToken)
            tokenCount += 1
            continue

        if hasFoundMatchingSyncToken:
            x = currentToken.type
            print("Proceeding to recover with token: ", currentToken)
            print("New Stack: ", stack)
            print("New x: ", x)
            print("<-----------------")
            return


def perform_end_action():
    global x
    global currentToken
    global lexer
    global stack
    global errorCount
    global tokenCount
    global retrievedTokensList
    global errorsList

    print(f"{Colors.GREEN}File scan ended{Colors.RESET}")

    print(f"{Colors.MAGENTA}Found", tokenCount, f"tokens{Colors.RESET}")
    create_tokens_hash_table(retrievedTokensList)

    print("\n")
    print(
        f"{Colors.RED}Errors found: ",
        errorCount,
        f"{Colors.RESET}",
    )

    if len(errorsList) > 0:
        create_errors_hash_table(errorsList)

    return


def create_tokens_hash_table(tokens):
    counter = 1
    table = HashTable(len(tokens))

    keys = []
    for i in range(0, len(tokens)):
        key = i + 1
        keys.append(str(key))
        table.insert(str(key), tokens[i])

    formattedData = []
    for key in keys:
        token = table.search(key)
        formattedData.append([key, token.type, token.value, token.lineno, token.lexpos])

    print("\nHashed Tokens table")
    headers = ["Id", "Token type", "Value", "Line", "Pos"]
    print(tabulate(formattedData, headers, tablefmt="fancy_grid"))


def create_errors_hash_table(errors):
    counter = 1
    table = HashTable(len(errors))

    keys = []
    for i in range(0, len(errors)):
        key = i + 1
        keys.append(str(key))
        table.insert(str(key), errors[i])

    formattedData = []
    for key in keys:
        error = table.search(key)
        formattedData.append(
            [key, error[0].type, error[0].lineno, error[0].lexpos, error[1]]
        )

    print(
        f"{Colors.RED}Hashed errors table",
    )
    headers = ["Id", "Unexpected Token", "Line", "Pos", "Stack"]
    print(tabulate(formattedData, headers, tablefmt="fancy_grid"), f"{Colors.RESET}")


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


executeCustomParser()
