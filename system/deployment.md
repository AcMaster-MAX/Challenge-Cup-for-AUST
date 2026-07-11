# 部署说明

## 环境要求

- Python 3.10+
- uv / pip
- ArbiterOS 官方仓库：https://github.com/cure-lab/ArbiterOS

## 部署步骤

1. 克隆本仓库和 ArbiterOS 官方仓库：

```bash
git clone https://github.com/YangYu-NUAA/Challenge-Cup-for-AUST.git
git clone https://github.com/cure-lab/ArbiterOS.git
```

2. 安装 ArbiterOS 依赖（参考官方 README）：

```bash
cd ArbiterOS/ArbiterOS-Kernel
uv sync
```

3. 配置环境变量：

```bash
cp .env.example .env
# 编辑 .env 填入必要的 API key、Langfuse 配置等
```

4. 将本项目 `data/block-01-redteam-rewrite/processed/rewritten_cases/` 中的 case 复制到 ArbiterOS redteam 目录并运行：

```bash
cd ../ArbiterOS
uv run python redteam/_automation/run_cases.py --case-id gov-email-phishing-001 --analyze-failures
```

5. 查看运行结果：

```bash
ls redteam/_automation/runs/
```

## 后续工作

- 集成 Block 03 的 skills 到 ArbiterOS 的 policy 注册表。
- 根据 Block 04 风险分级结果配置不同等级的响应策略。
- 构建前端展示界面（可选）。
