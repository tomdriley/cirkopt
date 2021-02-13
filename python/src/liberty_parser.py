import pyparsing as pp

from pyparsing import pyparsing_common as ppc
from src.file_io import IFile


class LibertyParser:

    def __init__(self):
        # Basic tokens/types
        lparen, rparen, lbrace, rbrace, colon, semi, dblquote = map(pp.Suppress, "(){}:;\"")
        string = pp.Word(pp.alphanums + '_' + '.')
        dbl_quotes_string = pp.dblQuotedString().setParseAction(pp.removeQuotes)
        real = ppc.real().setParseAction(ppc.convertToFloat)
        integer = ppc.integer().setParseAction(ppc.convertToInteger)

        # Statement
        statement = pp.Forward().setName("statement")

        # Simple Attribute
        simple_attribute = pp.Forward().setName("simple_attribute")
        attribute_value = pp.Forward().setName("attribute_value")
        attribute_name = string

        attribute_value <<= (real | integer | string | dbl_quotes_string)
        simple_attribute <<= pp.Group(attribute_name + colon + attribute_value + semi)

        # Complex Attribute
        complex_attribute = pp.Forward().setName("complex_attribute")
        parameter_list = pp.Group(dblquote + pp.delimitedList(attribute_value) + dblquote)
        parameter = (parameter_list | attribute_value)
        parameters = pp.delimitedList(parameter)
        complex_attribute <<= pp.Group(attribute_name + lparen + parameters + rparen + semi)

        # Group Statement
        group_statement = pp.Forward().setName("group_statement")
        group_name = string
        name = string
        group_statement <<= pp.Group(
            group_name +
            lparen +
            pp.Optional(name) +
            rparen +
            lbrace +
            pp.Dict(pp.ZeroOrMore(statement)) +
            rbrace
        )
        group_statement.ignore(pp.cppStyleComment)

        # Statement Def
        statement <<= (group_statement | simple_attribute | complex_attribute)

        # Root liberty object
        liberty_object = pp.Forward().setName("liberty_object")
        liberty_object <<= statement

        self.liberty_object = liberty_object

    def parse(self, file: IFile):
        return self.liberty_object.parseString(file.read())
