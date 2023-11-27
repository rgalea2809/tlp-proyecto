# No Terminales
S = 0
Sp = 1
O = 2
Op = 3
T = 4
Tp = 5
Ov = 51
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

# Gramaticas
S_table = [
    [S, "EOF", None],
    [S, "INCLUDE", ["#INCLUDE", "LESS_THAN", "IDENTIFIER", "GREATER_THAN", Sp]],
    [S, "LEFT_PARENTHESIS", None],
    [S, "RIGHT_PARENTHESIS", None],
    [S, "LEFT_BLOCK", None],
    [S, "RIGHT_BLOCK", None],
    [S, "INSTRUCTION_END", None],
    [S, "COMMA", None],
    [S, "EQUAL", None],
    [S, "LESS_THAN", None],
    [S, "GREATER_THAN", None],
    [S, "PLUS", None],
    [S, "MINUS", None],
    [S, "TIMES", None],
    [S, "DIVIDE", None],
    [S, "IDENTIFIER", None],
    [S, "CHAR_DEFINITION", None],
    [S, "NUMBER", None],
    [S, "STRING_DEFINITION", None],
    [S, "IF", None],
    [S, "ELSE", None],
    [S, "COMMENT", ["COMMENT", S]],
    [S, "STRING", [F, Sp]],
    [S, "CHAR", [F, Sp]],
    [S, "INT", [F, Sp]],
    [S, "FLOAT", [F, Sp]],
    [S, "PRINTF", None],
    [S, "SCANF", None],
    [S, "WHILE", None],
    [S, "return", None],
]

Sp_table = [
    [Sp, "EOF", "VACIA"],
    [Sp, "INCLUDE", None],
    [Sp, "LEFT_PARENTHESIS", None],
    [Sp, "RIGHT_PARENTHESIS", None],
    [Sp, "LEFT_BLOCK", None],
    [Sp, "RIGHT_BLOCK", None],
    [Sp, "INSTRUCTION_END", None],
    [Sp, "COMMA", None],
    [Sp, "EQUAL", None],
    [Sp, "LESS_THAN", None],
    [Sp, "GREATER_THAN", None],
    [Sp, "PLUS", None],
    [Sp, "MINUS", None],
    [Sp, "TIMES", None],
    [Sp, "DIVIDE", None],
    [Sp, "IDENTIFIER", None],
    [Sp, "CHAR_DEFINITION", None],
    [Sp, "NUMBER", None],
    [Sp, "STRING_DEFINITION", None],
    [Sp, "IF", None],
    [Sp, "ELSE", None],
    [Sp, "COMMENT", ["COMMENT", S]],
    [Sp, "STRING", [F, Sp]],
    [Sp, "CHAR", [F, Sp]],
    [Sp, "INT", [F, Sp]],
    [Sp, "FLOAT", [F, Sp]],
    [Sp, "PRINTF", None],
    [Sp, "SCANF", None],
    [Sp, "WHILE", None],
    [Sp, "return", None],
]

O_table = [
    [O, "EOF", None],
    [O, "INCLUDE", None],
    [O, "LEFT_PARENTHESIS", [T, Op]],
    [O, "RIGHT_PARENTHESIS", None],
    [O, "LEFT_BLOCK", None],
    [O, "RIGHT_BLOCK", None],
    [O, "INSTRUCTION_END", None],
    [O, "COMMA", None],
    [O, "EQUAL", None],
    [O, "LESS_THAN", None],
    [O, "GREATER_THAN", None],
    [O, "PLUS", None],
    [O, "MINUS", None],
    [O, "TIMES", None],
    [O, "DIVIDE", None],
    [O, "IDENTIFIER", [T, Op]],
    [O, "CHAR_DEFINITION", None],
    [O, "NUMBER", [T, Op]],
    [O, "STRING_DEFINITION", None],
    [O, "IF", None],
    [O, "ELSE", None],
    [O, "COMMENT", None],
    [O, "STRING", None],
    [O, "CHAR", None],
    [O, "INT", None],
    [O, "FLOAT", None],
    [O, "PRINTF", None],
    [O, "SCANF", None],
    [O, "WHILE", None],
    [O, "return", None],
]

Op_table = [
    [Op, "EOF", None],
    [Op, "INCLUDE", None],
    [Op, "LEFT_PARENTHESIS", None],
    [Op, "RIGHT_PARENTHESIS", ["VACIA"]],
    [Op, "LEFT_BLOCK", None],
    [Op, "RIGHT_BLOCK", None],
    [Op, "INSTRUCTION_END", ["VACIA"]],
    [Op, "COMMA", ["VACIA"]],
    [Op, "EQUAL", ["VACIA"]],
    [Op, "LESS_THAN", ["VACIA"]],
    [Op, "GREATER_THAN", ["VACIA"]],
    [Op, "PLUS", ["PLUS", T, Op]],
    [Op, "MINUS", ["MINUS", T, Op]],
    [Op, "TIMES", None],
    [Op, "DIVIDE", None],
    [Op, "IDENTIFIER", None],
    [Op, "CHAR_DEFINITION", None],
    [Op, "NUMBER", None],
    [Op, "STRING_DEFINITION", None],
    [Op, "IF", None],
    [Op, "ELSE", None],
    [Op, "COMMENT", None],
    [Op, "STRING", None],
    [Op, "CHAR", None],
    [Op, "INT", None],
    [Op, "FLOAT", None],
    [Op, "PRINTF", None],
    [Op, "SCANF", None],
    [Op, "WHILE", None],
    [Op, "return", None],
]

T_table = [
    [T, "EOF", None],
    [T, "INCLUDE", None],
    [T, "LEFT_PARENTHESIS", [Ov, Tp]],
    [T, "RIGHT_PARENTHESIS", None],
    [T, "LEFT_BLOCK", None],
    [T, "RIGHT_BLOCK", None],
    [T, "INSTRUCTION_END", None],
    [T, "COMMA", None],
    [T, "EQUAL", None],
    [T, "LESS_THAN", None],
    [T, "GREATER_THAN", None],
    [T, "PLUS", None],
    [T, "MINUS", None],
    [T, "TIMES", None],
    [T, "DIVIDE", None],
    [T, "IDENTIFIER", [Ov, Tp]],
    [T, "CHAR_DEFINITION", None],
    [T, "NUMBER", [Ov, Tp]],
    [T, "STRING_DEFINITION", None],
    [T, "IF", None],
    [T, "ELSE", None],
    [T, "COMMENT", None],
    [T, "STRING", None],
    [T, "CHAR", None],
    [T, "INT", None],
    [T, "FLOAT", None],
    [T, "PRINTF", None],
    [T, "SCANF", None],
    [T, "WHILE", None],
    [T, "return", None],
]

Tp_table = [
    [Tp, "EOF", None],
    [Tp, "INCLUDE", None],
    [Tp, "LEFT_PARENTHESIS", None],
    [Tp, "RIGHT_PARENTHESIS", ["VACIA"]],
    [Tp, "LEFT_BLOCK", None],
    [Tp, "RIGHT_BLOCK", None],
    [Tp, "INSTRUCTION_END", ["VACIA"]],
    [Tp, "COMMA", ["VACIA"]],
    [Tp, "EQUAL", ["VACIA"]],
    [Tp, "LESS_THAN", ["VACIA"]],
    [Tp, "GREATER_THAN", ["VACIA"]],
    [Tp, "PLUS", ["VACIA"]],
    [Tp, "MINUS", ["VACIA"]],
    [Tp, "TIMES", ["TIMES", Ov, Tp]],
    [Tp, "DIVIDE", ["DIVIDE", Ov, Tp]],
    [Tp, "IDENTIFIER", None],
    [Tp, "CHAR_DEFINITION", None],
    [Tp, "NUMBER", None],
    [Tp, "STRING_DEFINITION", None],
    [Tp, "IF", None],
    [Tp, "ELSE", None],
    [Tp, "COMMENT", None],
    [Tp, "STRING", None],
    [Tp, "CHAR", None],
    [Tp, "INT", None],
    [Tp, "FLOAT", None],
    [Tp, "PRINTF", None],
    [Tp, "SCANF", None],
    [Tp, "WHILE", None],
    [Tp, "return", None],
]

Ov_table = [
    [Ov, "EOF", None],
    [Ov, "INCLUDE", None],
    [Ov, "LEFT_PARENTHESIS", ["LEFT_PARENTHESIS", O, "RIGHT_PARENTHESIS"]],
    [Ov, "RIGHT_PARENTHESIS", None],
    [Ov, "LEFT_BLOCK", None],
    [Ov, "RIGHT_BLOCK", None],
    [Ov, "INSTRUCTION_END", None],
    [Ov, "COMMA", None],
    [Ov, "EQUAL", None],
    [Ov, "LESS_THAN", None],
    [Ov, "GREATER_THAN", None],
    [Ov, "PLUS", None],
    [Ov, "MINUS", None],
    [Ov, "TIMES", None],
    [Ov, "DIVIDE", None],
    [Ov, "IDENTIFIER", None],
    [Ov, "CHAR_DEFINITION", None],
    [Ov, "NUMBER", None],
    [Ov, "STRING_DEFINITION", None],
    [Ov, "IF", None],
    [Ov, "ELSE", None],
    [Ov, "COMMENT", None],
    [Ov, "STRING", None],
    [Ov, "CHAR", None],
    [Ov, "INT", None],
    [Ov, "FLOAT", None],
    [Ov, "PRINTF", None],
    [Ov, "SCANF", None],
    [Ov, "WHILE", None],
    [Ov, "return", None],
]

general_table = [
    [S, "EOF", None],
    [S, "#INCLUDE", ["#INCLUDE", "LESS_THAN", "IDENTIFIER", "GREATER_THAN", Sp]],
    [S, "LEFT_PARENTHESIS", None],
    [S, "RIGHT_PARENTHESIS", None],
    [S, "COMMENT", ["#INCLUDE", "LESS_THAN", "IDENTIFIER", "GREATER_THAN", Sp]],
]


template = [
    [O, "EOF", None],
    [O, "INCLUDE", None],
    [O, "LEFT_PARENTHESIS", None],
    [O, "RIGHT_PARENTHESIS", None],
    [O, "LEFT_BLOCK", None],
    [O, "RIGHT_BLOCK", None],
    [O, "INSTRUCTION_END", None],
    [O, "COMMA", None],
    [O, "EQUAL", None],
    [O, "LESS_THAN", None],
    [O, "GREATER_THAN", None],
    [O, "PLUS", None],
    [O, "MINUS", None],
    [O, "TIMES", None],
    [O, "DIVIDE", None],
    [O, "IDENTIFIER", None],
    [O, "CHAR_DEFINITION", None],
    [O, "NUMBER", None],
    [O, "STRING_DEFINITION", None],
    [O, "IF", None],
    [O, "ELSE", None],
    [O, "COMMENT", None],
    [O, "STRING", None],
    [O, "CHAR", None],
    [O, "INT", None],
    [O, "FLOAT", None],
    [O, "PRINTF", None],
    [O, "SCANF", None],
    [O, "WHILE", None],
    [O, "return", None],
]
