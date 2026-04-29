# AI Bug Buster v2: Executable & Closed-Loop Debugging

## 🚀 Overview
AI Bug Buster v2 is an upgraded, execution-driven framework designed to solve the "whack-a-mole" problem in AI-assisted coding. Unlike passive methodologies, v2 provides a suite of scripts to **run tests, classify errors, inject telemetry logs, and enforce hard resets** when a bug persists beyond 3 rounds.

## 🛠 Components
- `src/bug_cracker.py`: Core CLI for test execution, error classification, and log injection.
- `src/runner.py`: Isolated execution environment for verifying code snippets.
- `rules/ide_rules.md`: Enforced protocol for Cursor/VS Code AI.
- `docs/system_prompt_template.md`: Closed-loop system prompt for AI assistants.

## 🔄 The v2 Workflow
1. **Trigger**: Same error after 2 attempts.
2. **Execution**: AI runs `run_tests` to capture the real stack trace.
3. **Telemetry**: AI uses `inject_logs` to insert debug prints and gather runtime variable states.
4. **MVF**: AI proposes a single, evidence-based fix.
5. **Reset**: If it fails 3 times, AI generates a "Reset Prompt" for a fresh session.

## 📦 Installation
```bash
git clone https://github.com/shenlian19831109/ai_bug_buster.git
cd ai_bug_buster
chmod +x install.sh
./install.sh
```

## 📖 Documentation
- [中文说明 (Chinese README)](README_zh-CN.md)
- [System Prompt Template](docs/system_prompt_template.md)
- [IDE Rules (.cursorrules)](rules/ide_rules.md)

---

# AI Bug Buster v2：可执行与闭环验证调试框架

## 🚀 概述
AI Bug Buster v2 是一个升级版的、以执行为驱动的框架，旨在解决 AI 辅助编程中的“打地鼠”困境。与被动的方法论不同，v2 提供了一套脚本，用于**运行测试、分类错误、注入调试日志，并在 Bug 持续超过 3 轮时强制执行硬重置**。

## 🛠 组件
- `src/bug_cracker.py`：用于测试执行、错误分类和日志注入的核心 CLI。
- `src/runner.py`：用于验证代码片段的隔离执行环境。
- `rules/ide_rules.md`：针对 Cursor/VS Code AI 的强制执行协议。
- `docs/system_prompt_template.md`：AI 助手的闭环系统提示词。

## 🔄 v2 工作流
1. **触发**：2 次尝试后错误依然存在。
2. **执行**：AI 运行 `run_tests` 捕获真实的堆栈跟踪。
3. **追踪**：AI 使用 `inject_logs` 插入调试打印，收集运行时变量状态。
4. **最小修复 (MVF)**：AI 根据运行时证据提出单一修复方案。
5. **重置**：如果失败 3 次，AI 生成“重置提示词”以开启全新会话。

## 📦 安装
```bash
git clone https://github.com/shenlian19831109/ai_bug_buster.git
cd ai_bug_buster
chmod +x install.sh
./install.sh
```
