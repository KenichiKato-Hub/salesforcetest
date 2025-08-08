"""
Salesforce接続テスト用 FastAPI アプリケーション
Vercel上で動作するAPIサーバー
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any
import os

from salesforce_service import SalesforceService, SalesforceCredentials, SalesforceTestResult

# FastAPIアプリケーションの初期化
app = FastAPI(
    title="Salesforce接続テストAPI",
    description="Salesforceへの接続テストを実行するAPIサーバー",
    version="1.0.0",
    docs_url="/",  # Swagger UIをルートパスで表示
    redoc_url="/redoc"
)

# Salesforceサービスのインスタンス
sf_service = SalesforceService()


class SOQLQueryRequest(BaseModel):
    """SOQLクエリリクエストのモデル"""
    query: str
    credentials: SalesforceCredentials


@app.get("/health")
async def health_check():
    """ヘルスチェック用エンドポイント"""
    return {"status": "OK", "message": "APIサーバーは正常に動作しています"}


@app.post("/salesforce/test-connection", response_model=SalesforceTestResult)
async def test_salesforce_connection(credentials: SalesforceCredentials):
    """
    Salesforceへの接続テストを実行
    
    Args:
        credentials: Salesforce認証情報
        
    Returns:
        SalesforceTestResult: 接続テストの結果
    """
    try:
        result = sf_service.connect(credentials)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"接続テストの実行中にエラーが発生しました: {str(e)}")


@app.post("/salesforce/api-limits")
async def get_api_limits(credentials: SalesforceCredentials):
    """
    SalesforceのAPI制限情報を取得
    
    Args:
        credentials: Salesforce認証情報
        
    Returns:
        Dict: API制限情報
    """
    try:
        # まず接続テストを実行
        connection_result = sf_service.connect(credentials)
        if not connection_result.success:
            raise HTTPException(status_code=400, detail=connection_result.message)
        
        # API制限情報を取得
        limits_info = sf_service.test_api_limits()
        return {
            "success": True,
            "data": limits_info
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"API制限情報の取得中にエラーが発生しました: {str(e)}")


@app.post("/salesforce/execute-soql")
async def execute_soql_query(request: SOQLQueryRequest):
    """
    SOQLクエリを実行
    
    Args:
        request: SOQLクエリリクエスト
        
    Returns:
        Dict: クエリ実行結果
    """
    try:
        # まず接続テストを実行
        connection_result = sf_service.connect(request.credentials)
        if not connection_result.success:
            raise HTTPException(status_code=400, detail=connection_result.message)
        
        # SOQLクエリを実行
        query_result = sf_service.test_soql_query(request.query)
        return {
            "success": True,
            "query": request.query,
            "result": query_result
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SOQLクエリの実行中にエラーが発生しました: {str(e)}")


@app.get("/salesforce/sample-queries")
async def get_sample_queries():
    """
    サンプルSOQLクエリを返す
    
    Returns:
        Dict: サンプルクエリのリスト
    """
    return {
        "sample_queries": [
            {
                "name": "ユーザー情報取得",
                "query": "SELECT Id, Name, Email, Username FROM User LIMIT 5",
                "description": "システム内のユーザー情報を取得します"
            },
            {
                "name": "アカウント情報取得",
                "query": "SELECT Id, Name, Type, Industry FROM Account LIMIT 10",
                "description": "アカウント（会社）情報を取得します"
            },
            {
                "name": "商談情報取得",
                "query": "SELECT Id, Name, StageName, Amount, CloseDate FROM Opportunity WHERE Amount > 0 LIMIT 10",
                "description": "商談情報を取得します"
            },
            {
                "name": "組織情報取得",
                "query": "SELECT Id, Name, OrganizationType, InstanceName FROM Organization",
                "description": "組織の基本情報を取得します"
            }
        ]
    }


@app.get("/")
async def root():
    """ルートエンドポイント - Swagger UIにリダイレクト"""
    return {
        "message": "Salesforce接続テストAPIへようこそ！",
        "swagger_ui": "/docs",
        "api_documentation": "/redoc",
        "endpoints": {
            "health_check": "/health",
            "test_connection": "/salesforce/test-connection",
            "api_limits": "/salesforce/api-limits", 
            "execute_soql": "/salesforce/execute-soql",
            "sample_queries": "/salesforce/sample-queries"
        }
    }


# Vercel用のハンドラ（必要に応じて）
handler = app
