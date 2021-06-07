from pyparsing import Forward, Word, alphas, Suppress, Optional, Group


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
    OR = Word("OR")
    AND = Word("AND")
    ANDNOT = Word("ANDNOT")
    OP = OR | AND | ANDNOT
    word = Word(alphas)

    OPRET = Forward()
    EXPR = Forward()

    RET = (Word("RET") + Group(LPAR + word + RPAR)).setParseAction(
        tag('fncall'))
    OPRET << (OP + Group(LPAR + EXPR + COMMA + EXPR + RPAR)).setParseAction(
        tag('fncall'))
    EXPR << (OPRET | RET)

    return EXPR
