from pyparsing import Forward, Word, alphas, Suppress, Optional, Group, Literal


def tag(name):
    def tagfn(tokens):
        tklist = tokens.asList()
        if name == 'expr' and len(tklist) == 1:
            return tklist
        return tuple([name] + tklist)

    return tagfn


def get_parser():
    LPAR = Suppress("(")
    RPAR = Suppress(")")
    COMMA = Suppress(",")
    OR = Literal("OR")
    AND = Literal("AND")
    ANDNOT = Literal("ANDNOT")
    OP = (ANDNOT | AND | OR)
    word = Word(alphas)

    OPRET = Forward()
    EXPR = Forward()

    RET = (Literal("RET") + Group(LPAR + word + RPAR)).setParseAction(
        tag('fncall'))
    OPRET << (OP + Group(LPAR + EXPR + COMMA + EXPR + RPAR)).setParseAction(
        tag('fncall'))
    EXPR << (OPRET | RET)

    return EXPR
