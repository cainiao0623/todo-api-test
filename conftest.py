import pytest
import requests

BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="session")
def base_url():
    """全局base地址"""
    return BASE_URL

@pytest.fixture(scope="session")
def auth_token(base_url):
    """登录一次，整个测试会话复用token"""
    resp = requests.post(
        f"{base_url}/api/login",
        params={"username": "admin", "password": "123456"}
    )
    return resp.json()["token"]

@pytest.fixture
def headers(auth_token):
    """带鉴权的请求头"""
    return {"token": auth_token}

@pytest.fixture(autouse=True)
def reset_data(base_url, headers):
    """每条用例执行前重置测试数据（自动执行）"""
    # 先创建3条基础数据
    for i in range(1, 4):
        requests.post(
            f"{base_url}/api/todos",
            json={"title": f"预置任务{i}", "priority": i},
            headers=headers
        )
    yield  # 这里执行测试用例
    # 用例执行后可以做清理（可选）
