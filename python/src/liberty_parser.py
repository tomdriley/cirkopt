from dataclasses import dataclass
from typing import Any, Dict, List

import pyparsing as pp
from pyparsing import pyparsing_common as ppc

from src.file_io import IFile


@dataclass(frozen=True)
class Group:
    def __init__(self, adict: Dict):
        self.__dict__.update(adict)


# pylint: disable=unused-argument
def _to_multi_dict(input_string: str, location: int, toks: List[Any]) -> List[Any]:
    tokens = toks[0]
    group = dict()
    # Should be [group name, name, [members]]
    assert len(tokens) == 3

    group['group_name'] = tokens[0]
    group['name'] = tokens[1]

    for members in tokens[-1]:
        # Simple and complex attributes are [key, value]
        if len(members) == 2:
            group[members[0]] = members[1]
        # Grouped statements are [group name, name, dict of members]
        elif len(members) == 3:
            if members[0] in group:
                group[members[0]].append(members[2])
            else:
                group[members[0]] = [members[2]]
    toks[0][-1] = group
    return toks


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
        parameter_list = dblquote + pp.Group(pp.delimitedList(attribute_value)) + dblquote
        parameter = (parameter_list | attribute_value)
        parameters = pp.Group(pp.delimitedList(parameter))
        complex_attribute <<= pp.Group(attribute_name + lparen + parameters + rparen + semi)

        # Group Statement
        group_statement = pp.Forward().setName("group_statement")
        group_name = string
        name = string
        group_statement <<= pp.Group(
            group_name +
            lparen +
            pp.Optional(name, default='') +
            rparen +
            lbrace +
            pp.Group(pp.ZeroOrMore(statement)) +
            rbrace
        ).setParseAction(_to_multi_dict)
        group_statement.ignore(pp.cppStyleComment)

        # Statement Def
        statement <<= (group_statement | simple_attribute | complex_attribute)

        # Root liberty object
        liberty_object = pp.Forward().setName("liberty_object")
        liberty_object <<= statement

        self.liberty_object = liberty_object

    def parse(self, file: IFile):
        def dict_to_group(adict: Dict) -> Group:
            def handle_value(val: Any) -> Any:
                if isinstance(val, pp.ParseResults):
                    return val.asList()
                if isinstance(val, list):
                    return [dict_to_group(d) for d in val]
                if isinstance(val, dict):
                    return Group(val)
                return val

            return Group({key: handle_value(val) for key, val in adict.items()})

        root = self.liberty_object.parseString(file.read())[0][2]
        result = dict_to_group(root)
        return result
