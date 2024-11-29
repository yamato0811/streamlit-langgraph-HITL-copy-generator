from typing import Annotated, List

from PIL import Image
from typing_extensions import TypedDict


class DisplayMessageDict(TypedDict):
    title: Annotated[str, "表示用のタイトル"]
    icon: Annotated[str, "アイコン"]
    message_text: Annotated[str, "表示用のメッセージ"]


class State(TypedDict):
    # ================
    # Input
    # ================
    # Initial
    product_info: Annotated[str, "商品情報"]

    # Stremlit上でのuser input
    additional_info_input: Annotated[str, "入力された追加情報"]
    selected_copy: Annotated[dict, "選択されたキャッチコピー"]

    # ================
    # Output
    # ================
    # Copy
    copies: Annotated[list[dict], "キャッチコピーのリスト"]

    # Common
    is_additional_info_needed: Annotated[bool, "追加情報が必要か"]
    additional_info: Annotated[str, "必要な追加情報"]
    is_rethink: Annotated[bool, "再検討を行うか"]

    # ================
    # 処理用State
    # ================
    iteration_count: Annotated[int, "現在の反復回数"]
    is_finish: Annotated[bool, "終了判定フラグ"]
    display_message_dict: Annotated[DisplayMessageDict, "表示用のメッセージ"]

    # 履歴管理用
    messages: Annotated[list, "会話履歴のリスト"]
