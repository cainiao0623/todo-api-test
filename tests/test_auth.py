import requests

class TestLogin:
    """登录接口测试"""
    
    def test_login_success(self, base_url):
        """正确账号密码登录成功"""
        resp = requests.post(
            f"{base_url}/api/login",
            params={"username": "admin", "password": "123456"}
        )
        assert resp.status_code == 200
        assert "token" in resp.json()
    
    def test_login_wrong_password(self, base_url):
        """密码错误"""
        resp = requests.post(
            f"{base_url}/api/login",
            params={"username": "admin", "password": "wrong"}
        )
        assert resp.status_code == 400

class TestPermission:
    """权限测试"""
    
    def test_no_token(self, base_url):
        """不带token访问，401"""
        resp = requests.get(f"{base_url}/api/todos")
        assert resp.status_code == 401
    
    def test_wrong_token(self, base_url):
        """token错误，401"""
        resp = requests.get(
            f"{base_url}/api/todos",
            headers={"token": "fake-token"}
        )
        assert resp.status_code == 401
