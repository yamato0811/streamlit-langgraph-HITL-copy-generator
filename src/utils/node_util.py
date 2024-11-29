from typing import Any

from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel


def filter_key_from_list(
    input_list: list[dict[str, Any]], key_to_remove: str
) -> list[dict[str, Any]]:
    """
    指定されたキーをリスト内の各辞書から削除し、新しいリストを生成する
    """
    return [
        {key: value for key, value in item.items() if key != key_to_remove}
        for item in input_list
    ]


def get_output_format_instructions(model: BaseModel) -> str:
    parser = PydanticOutputParser(pydantic_object=model)
    output_format_instruction = parser.get_format_instructions()
    return output_format_instruction
