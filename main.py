from fastapi import FastAPI

# FastAPI アプリ本体を作成
app = FastAPI()

# 動作確認用エンドポイント
@app.get("/health")
def health_check():
    return {"status": "ok"}
