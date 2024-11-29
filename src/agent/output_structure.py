from typing import Optional

from pydantic import BaseModel, Field


# ================
# Copy Generation
# ================
class Copy(BaseModel):
    """コピー"""

    title: str = Field(description="タイトル(例:案1, 案2, ..)")
    reason: str = Field(description="回答の理由")
    copy_text: str = Field(description="キャッチコピー")


class Copies(BaseModel):
    """コピーの出力形式"""

    copies: list[Copy] = Field(description="キャッチコピーのリスト")


# ================
# Reflect
# ================
class ReflectDetails(BaseModel):
    """ユーザーからのフィードバック情報"""

    reason: str = Field(description="回答の理由")
    improvement_point: str = Field(description="改善点")
    additional_info: Optional[str] = Field(
        default=None,
        description="ユーザーに求める追加情報の内容(体言止め)",
    )
