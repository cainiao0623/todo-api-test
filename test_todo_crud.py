import requests

class TestTodoCreate:
    """创建Todo接口测试"""
    
    def test_create_success(self, base_url, headers):
        """正常创建：传对参数，应该返回201"""
        # 1. 准备数据
        payload = {"title": "我的第一个测试任务", "priority": 2}
        
        # 2. 发请求
        resp = requests.post(
            f"{base_url}/api/todos",
            json=payload,
            headers=headers
        )
        
        # 3. 断言（验证结果对不对）
        assert resp.status_code == 201  # 状态码对不对
        body = resp.json()
        assert body["code"] == 201
        assert body["data"]["title"] == "我的第一个测试任务"
        assert body["data"]["priority"] == 2
        assert body["data"]["completed"] == False  # 默认应该是未完成
    
    def test_create_without_title(self, base_url, headers):
        """异常场景：不传title，应该报错422"""
        payload = {"priority": 2}  # 故意不传必填的title
        resp = requests.post(
            f"{base_url}/api/todos",
            json=payload,
            headers=headers
        )
        assert resp.status_code == 422  # FastAPI参数校验失败返回422
import pytest
import requests

class TestTodoQuery:
    """查询接口测试"""
    
    def test_get_list(self, base_url, headers):
        """查询列表，应该至少有3条预置数据"""
        resp = requests.get(f"{base_url}/api/todos", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["total"] >= 3
    
    def test_get_by_id(self, base_url, headers):
        """查询单个存在的Todo"""
        resp = requests.get(f"{base_url}/api/todos/1", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["data"]["id"] == 1
    
    def test_get_not_exist(self, base_url, headers):
        """查询不存在的id，返回404"""
        resp = requests.get(f"{base_url}/api/todos/9999", headers=headers)
        assert resp.status_code == 404
        assert "不存在" in resp.json()["detail"]

class TestTodoUpdate:
    """更新接口测试"""
    
    def test_update_title(self, base_url, headers):
        """更新标题"""
        resp = requests.put(
            f"{base_url}/api/todos/1",
            json={"title": "更新后的标题"},
            headers=headers
        )
        assert resp.status_code == 200
        assert resp.json()["data"]["title"] == "更新后的标题"
    
    def test_mark_completed(self, base_url, headers):
        """标记为已完成"""
        resp = requests.put(
            f"{base_url}/api/todos/1",
            json={"completed": True},
            headers=headers
        )
        assert resp.status_code == 200
        assert resp.json()["data"]["completed"] == True

class TestTodoDelete:
    """删除接口测试"""
    
    def test_delete_success(self, base_url, headers):
        """删除成功后再查应该404"""
        # 先删
        del_resp = requests.delete(f"{base_url}/api/todos/2", headers=headers)
        assert del_resp.status_code == 204
        # 再查，确认删掉了
        get_resp = requests.get(f"{base_url}/api/todos/2", headers=headers)
        assert get_resp.status_code == 404
class TestTodoBoundary:
    """边界值测试"""
    
    @pytest.mark.parametrize("priority, expected_code", [
        (1, 201),    # 正常值
        (3, 201),    # 正常值
        (0, 201),    # 边界值
        (999, 201),  # 极大值
        (-1, 201),   # 负值
    ])
    def test_priority_boundary(self, base_url, headers, priority, expected_code):
        """优先级边界值测试"""
        payload = {"title": f"优先级{priority}测试", "priority": priority}
        resp = requests.post(
            f"{base_url}/api/todos",
            json=payload,
            headers=headers
        )
        assert resp.status_code == expected_code
