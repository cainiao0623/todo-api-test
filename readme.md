# Todo API 自动化测试项目

## 项目介绍
基于 pytest + requests 搭建的接口自动化测试框架，针对 Todo 管理系统 API 进行全量接口测试，覆盖正常场景、异常场景和边界值验证。

## 技术栈
- Python 3.x
- pytest 测试框架
- requests 接口请求库
- pytest-html 可视化测试报告
- GitHub Actions 持续集成

## 覆盖范围
- 登录鉴权接口
- Todo 增删改查接口
- 正常场景 + 异常场景 + 边界值
- 核心接口自动化覆盖率 100%

## 本地运行
1. 启动被测服务：`uvicorn main:app --port 8000`
2. 执行测试：`pytest tests/`
3. 查看报告：打开 `reports/report.html`

## CI 持续集成
- 代码提交自动触发测试
- 每日凌晨定时执行回归测试
- 测试报告可下载追溯