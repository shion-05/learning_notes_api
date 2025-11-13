from fastapi import FastAPI, HTTPException
from models.entry_model import LearningEntry, EntryCreate
from datetime import datetime
from typing import Optional,List
from collections import Counter

app = FastAPI()
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")

# 実際のアプリの「簡易データベース」的なものとして使うリスト
entries: List[LearningEntry] = []
"""
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
"""

@app.get("/entries")
def get_entries(tag: Optional[str] = None):#/entries?tag 型ヒント:str/none　ここでクエリパラメータがなくてもよくしている
    """
    登録されている全ての学習ノートを取得する．
    tag クエリパラメータが指定されていれば，そのタグを含むノートだけ返す．
    """
    # tag が指定されていない場合：全件返す
    if tag is None:
        return [entry.model_dump() for entry in entries] #[式 for 変数 in リスト (if 条件)]

    # tag が指定されている場合：タグでフィルタ
    filtered = [
        entry
        for entry in entries
        if tag in entry.tags  # tags に指定された tag が含まれているかどうか
    ]
    return [entry.model_dump() for entry in filtered]

#検索機能の文字列一致確認
def _contains(text: Optional[str], needle: str) -> bool:
    if text is None:
        return False
    return needle.lower() in text.lower()

@app.get("/entries/search")
def search_entries(keyword: Optional[str] = None, tag: Optional[str] = None):
    """
    ノート検索する
    - keyword: term / short_description / detail に部分一致（大文字小文字無視）
    - tag: tags に完全一致
    どちらか片方だけでもOK。両方指定時は AND 条件。
    """
    # 条件が何もないときは空配列を返す（無制限で全件返さない方針）
    if keyword is None and tag is None:
        return []

    result = []
    for entry in entries:
        ok_keyword = True  # デフォルト通過
        ok_tag = True      # デフォルト通過

        if keyword is not None:
            ok_keyword = (
                _contains(entry.term, keyword) or
                _contains(entry.short_description, keyword) or
                _contains(entry.detail, keyword)
            )

        if tag is not None:
            ok_tag = (tag in (entry.tags or []))

        if ok_keyword and ok_tag:
            result.append(entry.model_dump())

    return result

@app.post("/entries")
def create_entry(payload: EntryCreate):
    """
    新しい学習ノートを追加する
    """
    # 新しいIDを決める
    new_id = len(entries) + 1
    now = datetime.now()

    # EntryCreate から LearningEntry を作成
    entry = LearningEntry(
        id=new_id,
        created_at=now,
        updated_at=now,
        **payload.model_dump()  # term, short_description, detail, tags, source を展開
    )

    # リストに追加
    entries.append(entry)

    # 作成したノートをそのまま返す
    return entry.model_dump()

@app.get("/entries/{entry_id:int}")
def get_entry(entry_id: int):
    """
    指定されたIDの学習ノートを1件だけ返す
    見つからなければ 404 を返す
    """
    # entries の中から id が一致するものを探す
    for entry in entries:
        if entry.id == entry_id:
            return entry.model_dump()

    # ループを全部見ても見つからなかった場合
    raise HTTPException(status_code=404, detail=f"Entry with id={entry_id} not found")

@app.delete("/entries/{entry_id:int}")
def delete_entry(entry_id: int):
    """
    指定されたIDの学習ノートを削除するAPI
    削除したノートの内容を返す
    見つからなければ 404 を返す
    """
    for index, entry in enumerate(entries):
        if entry.id == entry_id:
            # 見つかった位置から要素を削除し，削除したものを取得
            deleted = entries.pop(index)
            return deleted.model_dump()

    # 見つからなかった場合
    raise HTTPException(status_code=404, detail=f"Entry with id={entry_id} not found")

@app.put("/entries/{entry_id:int}")
def update_entry(entry_id: int, payload: EntryCreate):
    """
    指定IDの学習ノートを更新する（PUT）
    - id と created_at は保持
    - updated_at は現在時刻に更新
    - 404: 見つからないとき
    - 422: 必須項目が欠けているとき（Pydanticが判定）
    """
    for idx, existing in enumerate(entries):
        if existing.id == entry_id:
            # Pydantic v2 の model_copy(update=...) で上書き
            updated = existing.model_copy(update={ #.model_copyで内容のコピー 引数にupdate=を付けるとフィールドの上書きが可能
                **payload.model_dump(),     # term / short_description / detail / tags / sourceを更新,**は辞書の展開
                "updated_at": datetime.now()
            })
            entries[idx] = updated
            return updated.model_dump()

    # 見つからなかったとき
    raise HTTPException(status_code=404, detail=f"Entry with id={entry_id} not found")

#タグ一覧表示
@app.get("/tags")
def list_tags():
    counter = Counter()
    for e in entries:
        for t in (e.tags or []):
            counter[t] += 1
    # 件数の多い順に並べて返す
    return [{"name": name, "count": count} for name, count in counter.most_common()]

