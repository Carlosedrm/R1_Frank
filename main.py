# Alunos: Arthur Przygocki, Henrique Tetilha, Carlos Mello

import re
import sys

# Tokens possíveis
TOKENS = {
    '\\neg': 'OP_UNARIO',
    '\\wedge': 'OP_BINARIO',
    '\\vee': 'OP_BINARIO',
    '\\rightarrow': 'OP_BINARIO',
    '\\leftrightarrow': 'OP_BINARIO',
    'true': 'CONSTANTE',
    'false': 'CONSTANTE',
    '(': 'ABREPAREN',
    ')': 'FECHAPAREN'
}

# Expressão regular para proposições
PROP_REGEX = re.compile(r'[0-9][0-9a-z]*')

class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor})"

def lexer(expressao):
    tokens = []
    i = 0
    while i < len(expressao):
        if expressao[i].isspace():
            i += 1
            continue

        match = False
        for tk in sorted(TOKENS.keys(), key=lambda x: -len(x)):
            if expressao.startswith(tk, i):
                tokens.append(Token(TOKENS[tk], tk))
                i += len(tk)
                match = True
                break

        if match:
            continue

        prop_match = PROP_REGEX.match(expressao[i:])
        if prop_match:
            valor = prop_match.group(0)
            tokens.append(Token('PROPOSICAO', valor))
            i += len(valor)
            continue

        # Token inválido
        return None

    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def eat(self, tipo):
        if self.current() and self.current().tipo == tipo:
            self.pos += 1
            return True
        return False

    def parse(self):
        return self.formula() and self.pos == len(self.tokens)

    def formula(self):
        tok = self.current()
        if not tok:
            return False
        if tok.tipo == 'CONSTANTE':
            return self.eat('CONSTANTE')
        if tok.tipo == 'PROPOSICAO':
            return self.eat('PROPOSICAO')
        if self.eat('ABREPAREN'):
            if self.current() and self.current().tipo == 'OP_UNARIO':
                self.eat('OP_UNARIO')
                if self.formula():
                    return self.eat('FECHAPAREN')
                return False
            elif self.current() and self.current().tipo == 'OP_BINARIO':
                self.eat('OP_BINARIO')
                if self.formula() and self.formula():
                    return self.eat('FECHAPAREN')
                return False
            return False
        return False

def validar_expressao(expr):
    tokens = lexer(expr)
    if tokens is None:
        return False
    parser = Parser(tokens)
    return parser.parse()

def main():
    if len(sys.argv) != 2:
        print("Use: python main.py arquivo.txt")
        return

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        linhas = [linha.strip() for linha in f.readlines() if linha.strip()]

    try:
        n = int(linhas[0])
        expressoes = linhas[1:]
        if len(expressoes) != n:
            print("Número de expressões não corresponde ao informado.")
            return
    except:
        print("Erro ao ler o arquivo.")
        return

    for expr in expressoes:
        print("valida" if validar_expressao(expr) else "inválida")

if __name__ == "__main__":
    main()
