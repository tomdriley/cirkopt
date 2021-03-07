from dataclasses import dataclass
from typing import Any, Dict, List
from logging import info

import pyparsing as pp  # type: ignore
from pyparsing import pyparsing_common as ppc

from src.file_io import IFile


@dataclass(frozen=True)
class Group:
    def __init__(self, adict: Dict):
        self.__dict__.update(adict)


LibertyResult = Group  # Alias for use outside module

# pylint: disable=unused-argument
def _to_multi_dict(input_string: str, location: int, toks: List[Any]) -> List[Any]:
    tokens = toks[0]
    group = dict()
    # Should be [group name, name, [member]]
    assert len(tokens) == 3

    group["group_name"] = tokens[0]
    group["name"] = tokens[1]

    duplicate_attribute_names = set()
    for member in tokens[-1]:
        member_name = member[0]
        existing_member = group[member_name] if member_name in group else None

        is_attribute = len(member) == 2
        is_group = len(member) == 3
        existing_member_is_list_of_dicts = (
            existing_member is not None
            and isinstance(existing_member, list)
            and isinstance(existing_member[-1], dict)
        )

        # Error if attribute's name has already been defined group name
        if is_attribute and existing_member_is_list_of_dicts:
            raise Exception(
                f"Member name '{member_name}' already defined as group name"
            )

        # Error if group name has already been defined by an attribute
        if (
            is_group
            and existing_member is not None
            and not existing_member_is_list_of_dicts
        ):
            raise Exception(
                f"Group with group name '{member_name}' already defined as attribute"
            )

        if is_attribute and existing_member is not None:
            # If there are duplicate attribute-value mappings,
            # store the values as an array in order of first appearance
            if member_name in duplicate_attribute_names:
                existing_member.append(member[1])
            else:
                group[member_name] = [existing_member, member[1]]
                duplicate_attribute_names.add(member_name)
        elif is_attribute:
            group[member_name] = member[1]
        elif is_group and existing_member is not None:
            group[member_name].append(member[2])
        elif is_group:
            group[member_name] = [member[2]]
        else:
            raise Exception(f"Unexpected tokens in group: {toks}")

    toks[0][-1] = group
    return toks


class LibertyParser:

    # pylint: disable=too-many-locals
    def __init__(self):
        # Basic tokens/types
        lparen, rparen, lbrace, rbrace, colon, semi, dblquote = map(
            pp.Suppress, '(){}:;"'
        )
        string = pp.Word(pp.alphanums + "_" + ".")
        dbl_quotes_string = pp.dblQuotedString().setParseAction(pp.removeQuotes)
        real = ppc.sci_real().setParseAction(ppc.convertToFloat)
        integer = ppc.integer().setParseAction(ppc.convertToInteger)

        # Statement
        statement = pp.Forward().setName("statement")

        # Simple Attribute
        simple_attribute = pp.Forward().setName("simple_attribute")
        attribute_value = pp.Forward().setName("attribute_value")
        attribute_name = string

        attribute_value <<= real | integer | string | dbl_quotes_string
        simple_attribute <<= pp.Group(attribute_name + colon + attribute_value + semi)

        # Complex Attribute
        complex_attribute = pp.Forward().setName("complex_attribute")
        parameter_list = (
            dblquote + pp.Group(pp.delimitedList(attribute_value)) + dblquote
        )
        parameter = parameter_list | attribute_value
        parameters = pp.Group(pp.delimitedList(parameter))
        complex_attribute <<= pp.Group(
            attribute_name + lparen + parameters + rparen + semi
        )

        # Group Statement
        group_statement = pp.Forward().setName("group_statement")
        group_name = string
        name = string
        group_statement <<= pp.Group(
            group_name
            + lparen
            + pp.Optional(name, default="")
            + rparen
            + lbrace
            + pp.Group(pp.ZeroOrMore(statement))
            + rbrace
        ).setParseAction(_to_multi_dict)

        # Statement Def
        statement <<= group_statement | simple_attribute | complex_attribute

        # Root liberty object
        liberty_object = pp.Forward().setName("liberty_object")
        liberty_object <<= statement
        liberty_object.ignore(pp.cppStyleComment)
        liberty_object.ignore("\\")

        self.liberty_object = liberty_object

    def parse(self, file: IFile) -> LibertyResult:
        info("Parsing LDB library.")

        def handle_value(val: Any) -> Any:
            if isinstance(val, pp.ParseResults):
                return tuple(handle_value(v) for v in val.asList())
            if isinstance(val, list) and isinstance(val[-1], dict):
                return tuple(dict_to_group(d) for d in val)
            if isinstance(val, list):
                return tuple(handle_value(v) for v in val)
            if isinstance(val, dict):
                return Group(val)
            return val

        def dict_to_group(adict: Dict) -> Group:
            return Group({key: handle_value(val) for key, val in adict.items()})

        root = self.liberty_object.parseString(file.read())[0][2]
        result: LibertyResult = dict_to_group(root)
        return result
