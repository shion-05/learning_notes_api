from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

  #学んだ内容（辞書項目）を表す
class LearningEntry(BaseModel):

    id: int = Field(..., description="一意のID（自動採番）")
    term: str = Field(..., min_length=1, description="用語・トピック名")
    short_description: str = Field(..., min_length=3, description="短い説明")
    detail: Optional[str] = Field(None, description="詳細な説明・ノート")
    tags: Optional[List[str]] = Field(default_factory=list, description="関連タグ")
    source: Optional[str] = Field(None, description="出典や参考URL")
    created_at: datetime = Field(default_factory=datetime.now, description="作成日時")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新日時")
