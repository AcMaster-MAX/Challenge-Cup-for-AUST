# src/system

本目录存放系统设计与部署相关的代码、脚本和配置。

## 文件清单

- `deployment_scripts/`：部署脚本（安装依赖、启动服务等）
- `integration/`：与 ArbiterOS 内核集成的适配代码
- `frontend/`：可选的前端展示代码
- `README.md`：本文件

## 开发规范

- 所有代码遵循 Python 3.10+ 语法。
- 与 ArbiterOS 集成时，优先使用官方 CLI/API，避免修改内核源码。
- 配置项使用环境变量或 YAML，不提交敏感信息到仓库。
