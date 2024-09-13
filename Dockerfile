# 使用するPythonのベースイメージ
FROM python:3.11-slim

# 作業ディレクトリの設定
WORKDIR /app

# 必要なパッケージをインストールするためにrequirements.txtをコピー
COPY requirements.txt .

# 依存関係のインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコードをコンテナにコピー
COPY . .

# Uvicornをインストールする
RUN pip install uvicorn

# コンテナが起動する際に実行するコマンドを指定
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
