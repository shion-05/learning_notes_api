from fastapi import FastAPI
from models.entry_model import LearningEntry
from datetime import datetime
from typing import Optional

app = FastAPI()

# ダミーデータ
dummy_entries = [
    LearningEntry(
        id=1,
        term="FastAPI",
        short_description="Pythonの軽量なWebフレームワーク",
        detail="型ヒントを使った宣言的なAPI開発が特徴。",
        tags=["Python", "Web", "FastAPI"],
        source="Qiita: https://qiita.com/miyakiyo/items/6cc9024d96c7f56f8321",
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    LearningEntry(
        id=2,
        term="機械学習",
        short_description="データから学習して予測や分類を行う技術",
        tags=["AI", "データサイエンス"],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
]


@app.get("/entries")
def get_entries(tag: Optional[str] = None):#/entries?tag 型ヒント:str/none　ここでクエリパラメータがなくてもよくしている
    """
    登録されている全ての学習ノートを取得する．
    tag クエリパラメータが指定されていれば，そのタグを含むノートだけ返す．
    """
    # tag が指定されていない場合：全件返す
    if tag is None:
        return [entry.model_dump() for entry in dummy_entries] #[式 for 変数 in リスト (if 条件)]

    # tag が指定されている場合：タグでフィルタ
    filtered = [
        entry
        for entry in dummy_entries
        if tag in entry.tags  # tags に指定された tag が含まれているかどうか
    ]
    return [entry.model_dump() for entry in filtered]
