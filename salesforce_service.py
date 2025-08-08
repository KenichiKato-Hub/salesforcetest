"""
Salesforce接続テスト用のサービスクラス
"""
import os
from typing import Dict, Any, Optional
from simple_salesforce import Salesforce
import requests
from pydantic import BaseModel


class SalesforceCredentials(BaseModel):
    """Salesforce認証情報のモデル"""
    username: str
    password: str
    security_token: str
    domain: str = "login"  # 'login' or 'test'


class SalesforceTestResult(BaseModel):
    """Salesforce接続テスト結果のモデル"""
    success: bool
    message: str
    user_info: Optional[Dict[str, Any]] = None
    org_info: Optional[Dict[str, Any]] = None


class SalesforceService:
    """Salesforce接続とテスト用のサービスクラス"""
    
    def __init__(self):
        self.sf_client: Optional[Salesforce] = None
    
    def connect(self, credentials: SalesforceCredentials) -> SalesforceTestResult:
        """
        Salesforceに接続してテストを実行
        
        Args:
            credentials: Salesforce認証情報
            
        Returns:
            SalesforceTestResult: 接続テストの結果
        """
        try:
            # Salesforceクライアントを作成
            self.sf_client = Salesforce(
                username=credentials.username,
                password=credentials.password,
                security_token=credentials.security_token,
                domain=credentials.domain
            )
            
            # 基本的な情報を取得してテスト
            user_info = self._get_user_info()
            org_info = self._get_org_info()
            
            return SalesforceTestResult(
                success=True,
                message="Salesforceへの接続に成功しました",
                user_info=user_info,
                org_info=org_info
            )
            
        except Exception as e:
            return SalesforceTestResult(
                success=False,
                message=f"Salesforceへの接続に失敗しました: {str(e)}"
            )
    
    def _get_user_info(self) -> Dict[str, Any]:
        """現在のユーザー情報を取得"""
        try:
            if not self.sf_client:
                return {}
            
            # 現在のユーザー情報を取得
            user = self.sf_client.query("SELECT Id, Name, Email, Username FROM User WHERE Id = UserInfo.getUserId()")
            if user['records']:
                return {
                    'id': user['records'][0]['Id'],
                    'name': user['records'][0]['Name'],
                    'email': user['records'][0]['Email'],
                    'username': user['records'][0]['Username']
                }
            return {}
        except Exception as e:
            return {'error': str(e)}
    
    def _get_org_info(self) -> Dict[str, Any]:
        """組織情報を取得"""
        try:
            if not self.sf_client:
                return {}
            
            # 組織情報を取得
            org = self.sf_client.query("SELECT Id, Name, OrganizationType FROM Organization LIMIT 1")
            if org['records']:
                return {
                    'id': org['records'][0]['Id'],
                    'name': org['records'][0]['Name'],
                    'type': org['records'][0]['OrganizationType']
                }
            return {}
        except Exception as e:
            return {'error': str(e)}
    
    def test_api_limits(self) -> Dict[str, Any]:
        """API制限情報をテスト"""
        try:
            if not self.sf_client:
                return {'error': 'Salesforceクライアントが初期化されていません'}
            
            # API制限情報を取得
            limits_url = f"{self.sf_client.base_url}limits/"
            headers = {'Authorization': f'Bearer {self.sf_client.session_id}'}
            
            response = requests.get(limits_url, headers=headers)
            if response.status_code == 200:
                limits_data = response.json()
                return {
                    'daily_api_requests': limits_data.get('DailyApiRequests', {}),
                    'hourly_api_requests': limits_data.get('HourlyApiRequests', {}),
                    'data_storage_mb': limits_data.get('DataStorageMB', {}),
                    'file_storage_mb': limits_data.get('FileStorageMB', {})
                }
            else:
                return {'error': f'API制限情報の取得に失敗: {response.status_code}'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def test_soql_query(self, query: str) -> Dict[str, Any]:
        """SOQLクエリのテスト実行"""
        try:
            if not self.sf_client:
                return {'error': 'Salesforceクライアントが初期化されていません'}
            
            result = self.sf_client.query(query)
            return {
                'total_size': result['totalSize'],
                'done': result['done'],
                'records_count': len(result['records']),
                'records': result['records'][:5]  # 最初の5件のみ返す
            }
            
        except Exception as e:
            return {'error': str(e)}
