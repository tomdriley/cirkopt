import pyparsing as pp

from src.file_io import IFile
from pyparsing import pyparsing_common as ppc


class LibertyParser():

    def __init__(self):
        # Basic tokens/types
        LPAREN, RPAREN, LBRACE, RBRACE, COLON, SEMI = map(pp.Suppress, "(){}:;")
        string = pp.Word(pp.alphanums + '_' + '.')
        dblQuotesString = pp.dblQuotedString().setParseAction(pp.removeQuotes)
        real = ppc.real().setParseAction(ppc.convertToFloat)
        integer = ppc.integer().setParseAction(ppc.convertToInteger)

        # Statement
        statement = pp.Forward().setName("statement")

        # Simple Attribute
        simple_attribute = pp.Forward().setName("simple_attribute")
        attribute_value = pp.Forward().setName("attribute_value")
        attribute_name = string

        attribute_value << (real | integer | string | dblQuotesString)
        simple_attribute << pp.Group(attribute_name + COLON + attribute_value + SEMI)

        # Group Statement
        group_statement = pp.Forward().setName("group_statement")
        group_name = string
        name = string
        group_statement << pp.Group(
            group_name + LPAREN + pp.Optional(name) + RPAREN + LBRACE + pp.Dict(pp.ZeroOrMore(statement)) + RBRACE
        )
        group_statement.ignore(pp.cppStyleComment)

        # Statement Def
        statement <<= (group_statement | simple_attribute)

        # Root liberty object
        liberty_object = pp.Forward().setName("liberty_object")
        liberty_object <<= statement
        # liberty_object.ignore(pp.cppStyleComment)

        self.liberty_object = liberty_object

    def parse(self, file: IFile):
        return self.liberty_object.parseString(file.read())