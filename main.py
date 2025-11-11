from fastapi import FastAPI
from models.entry_model import LearningEntry
from datetime import datetime

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
def get_entries():
    #登録されている全ての学習ノートを取得する
    return [entry.model_dump() for entry in dummy_entries]
