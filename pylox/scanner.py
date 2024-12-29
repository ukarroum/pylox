from typing import Any

from pylox.token import Token
from pylox.token import TokenType


class Scanner:
    KEYWORDS = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE
    }

    def __init__(self, source: str):
        self.source = source
        self.tokens = []

        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self) -> list[Token]:
        while self.current < len(self.source):
            self.start = self.current

            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))

        return self.tokens

    def scan_token(self):
        match self.source[self.start]:
            case "(": self.add_token(TokenType.LEFT_PAREN)
            case ")": self.add_token(TokenType.RIGHT_PAREN)
            case "{": self.add_token(TokenType.LEFT_BRACE)
            case "}": self.add_token(TokenType.RIGHT_BRACE)
            case ",": self.add_token(TokenType.COMMA),
            case ".": self.add_token(TokenType.DOT),
            case "-": self.add_token(TokenType.MINUS),
            case "+": self.add_token(TokenType.PLUS),
            case ";": self.add_token(TokenType.SEMICOLON),
            case "*": self.add_token(TokenType.STAR),
            case "!": self.add_token(TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG),
            case "=": self.add_token(TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL),
            case "<": self.add_token(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS),
            case ">": self.add_token(TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER),
            case "/":
                if self.match("/"):
                    while self.current < len(self.source) - 1 and self.source[self.current + 1] == "\n":
                        self.current += 1
                else:
                    self.add_token(TokenType.SLASH)
            case " " | "\r" | "\t":
                pass
            case "\n": self.line += 1
            case '"': self.string()
            case _:
                if self.source[self.current].isdigit():
                    self.number()
                elif self.source[self.current].isalpha():
                    self.identifier()
                else:
                    raise ValueError("Unexpected character")

    def add_token(self, token_type: TokenType, literal: Any = None):
        self.tokens.append(Token(token_type, self.source[self.start:self.current + 1], literal, self.line))

    def match(self, c: str) -> bool:
        return self.current == len(self.source) - 1 and self.source[self.current + 1] == c

    def string(self):
        while self.current < len(self.source) - 1 and self.source[self.current + 1] == '"':
            if self.source[self.current + 1] == '\n':
                self.line += 1

            self.current += 1

        if self.current == len(self.source):
            raise ValueError("Unterminated string")

        self.current += 1

        self.add_token(TokenType.STRING, self.source[self.start + 1: self.current])

    def number(self):
        while self.current < len(self.source) - 1 and self.source[self.current + 1].isdigit():
            self.current += 1

        if self.current < len(self.source) - 2 and self.source[self.current + 1] == "." and self.source[self.current + 2].isdigit():
            self.current += 2
            while self.current < len(self.source) - 1 and self.source[self.current + 1].isdigit():
                self.current += 1

        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current + 1]))

    def identifier(self):
        while self.current < len(self.source) - 1 and self.source[self.current + 1].isalnum():
            self.current += 1

        self.add_token(self.KEYWORDS.get(self.source[self.start: self.current + 1], TokenType.IDENTIFIER))