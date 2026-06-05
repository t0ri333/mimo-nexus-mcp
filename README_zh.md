# MiMo-Nexus

<p align="center">
  <strong>轻量级 MCP 智能网关，为 AI 编程节省 Token 消耗</strong>
</p>

<p align="center">
  <a href="#安装">安装</a> •
  <a href="#快速开始">快速开始</a> •
  <a href="#功能特性">功能特性</a> •
  <a href="#api-参考">API 参考</a> •
  <a href="README.md">English</a> •
  <a href="README_ja.md">日本語</a>
</p>

---

## 概述

MiMo-Nexus 是一个轻量级的 MCP（Model Context Protocol）智能网关，能够拦截来自 AI 编程助手（Claude Code、Cursor 等）的大型代码库分析请求，并将其卸载到小米 MiMo 2.5 Pro API。

**问题所在：** 当 AI 助手读取大型项目时，会消耗大量 Token，导致高昂的 API 账单和上下文溢出。

**解决方案：** MiMo-Nexus 充当智能代理 - 它扫描本地代码，高效打包，发送到 MiMo 2.5 Pro 的 1M 上下文窗口（约 $1/M Token），并将简洁的分析结果返回给 AI 助手。

**效果：** 节省 60-95% 的 Token 成本，同时获得更深入的代码分析。

## 功能特性

- **Token 高效分析** - 将整个代码库分析卸载到 MiMo 2.5 Pro 的 1M 上下文窗口
- **OpenAI 兼容 API** - 使用标准 OpenAI SDK 实现无缝集成
- **思维模型支持** - 通过 Gemini 格式访问 MiMo 2.5 Omni 的推理链
- **语音反馈** - 使用 MiMo TTS 生成语音构建通知
- **智能文件过滤** - 自动跳过 .git、node_modules、二进制文件等无关文件
- **MCP 协议** - 开箱即用，兼容所有支持 MCP 的 AI 助手

## 安装

### 前置要求

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) 包管理器
- MiMo API 密钥，从 [platform.xiaomimimo.com](https://platform.xiaomimimo.com) 获取

### 使用 uv 安装（推荐）

```bash
# 克隆仓库
git clone https://github.com/t0ri333/mimo-nexus-mcp.git
cd mimo-nexus-mcp

# 安装依赖
uv sync

# 复制环境模板
cp .env.example .env

# 编辑 .env 并添加 API 密钥
# XIAOMI_MIMO_API_KEY=your_key_here
```

### 从 PyPI 安装（发布后）

```bash
pip install mimo-nexus-mcp
```

## 快速开始

### 1. 配置 API 密钥

```bash
# 复制环境模板
cp .env.example .env

# 编辑 .env 并添加 API 密钥
# 从 https://platform.xiaomimimo.com 获取密钥
XIAOMI_MIMO_API_KEY=your_key_here
```

### 2. 注册到 Claude Code

```bash
# 全局注册 MCP 服务器
claude mcp add \
  --env XIAOMI_MIMO_API_KEY=$XIAOMI_MIMO_API_KEY \
  --transport stdio \
  mimo-nexus \
  -- uv run server.py
```

### 3. 在工作流中使用

在 Claude Code 中，直接提问：

```
分析这个项目的认证模块，并识别潜在的安全漏洞。
```

Claude Code 会自动调用 MiMo-Nexus，它会：
1. 扫描本地源文件
2. 打包成结构化载荷
3. 发送到 MiMo 2.5 Pro 进行深度分析
4. 返回简洁报告（节省数千 Token）

## API 参考

### MCP 工具

#### `mimo_global_repo_analyzer`

通过卸载到 MiMo 2.5 Pro 的 1M 上下文来分析整个代码库。

**参数：**
- `directory_path` (str)：项目目录的绝对路径
- `architectural_query` (str)：分析的具体问题或焦点
- `model` (str, 可选)：模型 ID（默认：`mimo-v2.5-pro`）
- `use_thinking` (bool, 可选)：为 `mimo-v2.5-omni` 启用思维模式

**返回：** 详细的分析报告，包含文件引用和具体建议。

#### `mimo_code_query`

快速查询代码库，无需完整分析。

**参数：**
- `question` (str)：关于代码的具体问题
- `directory_path` (str, 可选)：项目根目录（默认：`.`）
- `model` (str, 可选)：模型 ID（默认：`mimo-v2.5-pro`）

**返回：** 基于项目结构的简洁回答。

#### `mimo_voice_broadcaster`

使用 MiMo TTS 生成语音反馈。

**参数：**
- `report_text` (str)：要转换为语音的文本内容
- `vibe_style` (str, 可选)：情绪基调预设
  - `professional_engineer`：冷静、精准的高级工程师
  - `urgent_warning`：焦虑的系统管理员警告
  - `calm_success`：构建成功后的温暖满足感
  - `hacker_cyberpunk`：快速说话的赛博朋克黑客

**返回：** 包含 `audio_path`（本地文件路径）和 `metadata` 的字典。

## 支持的模型

| 模型 | ID | 格式 | 上下文 | 用途 |
|------|-----|------|--------|------|
| MiMo 2.5 Pro | `mimo-v2.5-pro` | OpenAI | 1M Token | 代码分析、架构审查 |
| MiMo 2.5 | `mimo-v2.5` | OpenAI | 1M Token | 轻量级查询 |
| MiMo 2.5 Omni | `mimo-v2.5-omni` | OpenAI / Gemini | 1M Token | 思维模式，带推理链 |

## 配置

### 环境变量

| 变量 | 必需 | 描述 |
|------|------|------|
| `XIAOMI_MIMO_API_KEY` | 是 | MiMo API 密钥 |

### 推理参数

网关使用 MiMo 官方推荐的优化参数：

| 参数 | 标准模型 | 思维模型 |
|------|----------|----------|
| Temperature | 0.3 | 1.0 |
| Top P | 0.95 | 0.95 |

## 架构

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Claude Code    │────▶│  MiMo-Nexus      │────▶│  MiMo 2.5 Pro   │
│  (本地 AI)      │◀────│  MCP 网关        │◀────│  API (云端)     │
└─────────────────┘     └──────────────────┘     └─────────────────┘
        │                        │
        │                   ┌────┴────┐
        │                   │ 本地    │
        │                   │ 文件    │
        │                   └─────────┘
        ▼
  简洁结果 (300 Token)
  而非原始代码 (80,000 Token)
```

## 贡献

欢迎贡献！请先阅读我们的[贡献指南](CONTRIBUTING.md)。

## 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE)。

## 致谢

- 使用 [FastMCP](https://github.com/jlowin/fastmcp) 处理 MCP 协议
- 由 [Xiaomi MiMo 2.5 Pro](https://platform.xiaomimimo.com) 提供云端推理支持
- 灵感来自 [headroom](https://github.com/anthropics/headroom) 的 Token 优化概念
