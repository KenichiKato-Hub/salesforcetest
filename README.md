# Salesforce接続テストAPI

Vercel上で動作するFastAPIベースのSalesforce接続テストアプリケーションです。simple-salesforceライブラリを使用してSalesforceとの連携をテストできます。

## 機能

- ✅ Salesforceへの接続テスト
- ✅ ユーザー情報・組織情報の取得
- ✅ API制限情報の確認
- ✅ SOQLクエリの実行とテスト
- ✅ Swagger UIによる直感的なAPI操作

## 必要な依存関係

- FastAPI
- simple-salesforce
- requests
- uvicorn
- python-dotenv
- pydantic

## ローカル開発環境のセットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. アプリケーションの起動

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. APIの確認

ブラウザで以下のURLにアクセス：
- Swagger UI: http://localhost:8000/
- API Documentation: http://localhost:8000/redoc

## Vercelへのデプロイ

### 1. Vercelアカウントとプロジェクトの準備

1. [Vercel](https://vercel.com/)にアカウントを作成
2. GitHubリポジトリをVercelに接続

### 2. 自動デプロイ

GitHubにプッシュすると自動的にデプロイされます。

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

## API エンドポイント

### ヘルスチェック
- `GET /health` - APIサーバーの状態確認

### Salesforce接続テスト
- `POST /salesforce/test-connection` - Salesforceへの接続テスト

### API制限情報
- `POST /salesforce/api-limits` - SalesforceのAPI制限情報を取得

### SOQLクエリ実行
- `POST /salesforce/execute-soql` - SOQLクエリの実行

### サンプルクエリ
- `GET /salesforce/sample-queries` - サンプルSOQLクエリの一覧

## 使用方法

### 1. Salesforce接続情報の準備

Salesforceの接続に必要な情報：
- `username`: Salesforceのユーザー名
- `password`: Salesforceのパスワード
- `security_token`: セキュリティトークン
- `domain`: "login"（本番環境）または "test"（Sandbox環境）

### 2. Swagger UIでのテスト

1. デプロイされたURLまたはローカルのSwagger UIにアクセス
2. `/salesforce/test-connection` エンドポイントを選択
3. 認証情報を入力してテスト実行

### 3. セキュリティトークンの取得方法

1. Salesforceにログイン
2. 右上のプロフィールアイコン → 設定
3. 私の個人情報 → セキュリティトークンのリセット
4. メールで送信されたトークンを使用

## プロジェクト構成

```
salesforcetest/
├── main.py                 # FastAPIメインアプリケーション
├── salesforce_service.py   # Salesforce接続サービス
├── requirements.txt        # Python依存関係
├── vercel.json            # Vercelデプロイ設定
└── README.md              # このファイル
```

## 注意事項

- Salesforceの認証情報は安全に管理してください
- API制限に注意してテストを実行してください
- セキュリティトークンは定期的に更新することを推奨します

## トラブルシューティング

### 接続エラーが発生する場合

1. ユーザー名、パスワード、セキュリティトークンが正しいか確認
2. IPアドレス制限がかかっていないか確認
3. Salesforceの組織設定でAPI接続が許可されているか確認

### デプロイエラーが発生する場合

1. `requirements.txt`の依存関係が正しいか確認
2. `vercel.json`の設定が正しいか確認
3. Vercelのログを確認してエラー内容を特定

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。
