# 同步上游更新指南

## 核心概念

### 翻译任务派发机制

```
┌─────────────────────────────────────────────────────────────┐
│  你 (主会话)                                                  │
│         │                                                    │
│         ▼                                                    │
│  运行 auto-dispatch.py                                       │
│         │                                                    │
│         ▼                                                    │
│  sessions_spawn (派发任务)                                    │
│         │                                                    │
│    ┌────┴────┐  ┌────┴────┐  ┌────┴────┐                    │
│    │ 子代理 1 │  │ 子代理 2 │  │ 子代理 3 │  ...             │
│    │ 翻译中  │  │ 翻译中  │  │ 翻译中  │                    │
│    └────┬────┘  └────┬────┘  └────┬────┘                    │
│         │            │            │                          │
│         └────────────┴────────────┘                          │
│                      │                                       │
│                      ▼                                       │
│         完成后自动通知主会话 (System Message)                    │
└─────────────────────────────────────────────────────────────┘
```

**关键点：**
- `sessions_spawn` 必须在 **OpenClaw 会话内** 运行
- 子代理完成后通过 **System Message** 自动通知
- 无法通过 cron/GitHub Actions 直接调用

---

## 同步方式对比

| 方式 | 可行性 | 说明 |
|------|--------|------|
| 手动运行脚本 | ✅ 推荐 | 完全可控，实时处理 |
| GitHub Actions 自动翻译 | ❌ 不可行 | Actions 无法调用本地 Claude |
| GitHub Actions + Issue 通知 | ✅ 可行 | Actions 检测更新，创建 Issue 通知你 |
| 本地 cron | ❌ 不可行 | cron 无法在 OpenClaw 会话内运行 |
| 本地 cron + 通知 | ⚠️ 复杂 | 需要额外服务，不推荐 |

---

## 推荐工作流程

### 方案 A: 完全手动（最简单）

```bash
# 当你想检查更新时
cd /Volumes/myDisk/workplace/awesome-openclaw-skills-zh
./scripts/sync-upstream.sh
```

**优点：**
- 简单直接
- 完全可控
- 无需额外配置

**缺点：**
- 需要记得手动执行

---

### 方案 B: GitHub Actions 检测 + 手动翻译

**工作流程：**

```
上游仓库更新
    ↓
GitHub Actions 检测到 (每天 18:00)
    ↓
创建 Issue 通知你
    ↓
你看到通知后手动运行同步脚本
```

**配置：**

1. GitHub Actions 工作流已创建：`.github/workflows/sync-and-translate.yml`

2. Actions 会：
   - 每天检查上游更新
   - 发现变更时创建 Issue
   - Issue 标题：`[同步通知] 上游仓库有更新需要重新翻译`

3. 你收到通知后：
   ```bash
   ./scripts/sync-upstream.sh
   ```

**优点：**
- 不会错过更新
- 翻译仍由你控制
- 无需本地定时任务

**缺点：**
- 仍需手动执行翻译

---

### 方案 C: 完全自动化（不推荐）

理论上可以实现，但需要：
- 本地运行 HTTP 服务接收 Webhook
- 服务调用 OpenClaw API
- 配置复杂，安全性考虑多

**不推荐普通用户使用。**

---

## 实际操作步骤

### 初次设置

```bash
# 1. 克隆仓库
cd /Volumes/myDisk/workplace
git clone https://github.com/Rito-w/awesome-openclaw-skills-zh.git
cd awesome-openclaw-skills-zh

# 2. 添加上游远程仓库
git remote add upstream https://github.com/VoltAgent/awesome-openclaw-skills.git

# 3. 测试同步脚本
./scripts/sync-upstream.sh --status
```

### 日常同步（推荐频率：每周 1-2 次）

```bash
# 1. 检查并同步
./scripts/sync-upstream.sh

# 2. 查看翻译状态
python3 scripts/auto-dispatch.py --status

# 3. 等待翻译完成（子代理完成后会自动通知）

# 4. 提交翻译结果
git add -A
git commit -m "feat: 同步上游更新 $(date +%Y-%m-%d)"
git push
```

### 查看翻译进度

```bash
# 查看哪些文件已翻译
ls -la categories/*.zh.md | wc -l

# 查看状态
python3 scripts/auto-dispatch.py --status
```

---

## 常见问题

### Q: 为什么不能用 cron 自动翻译？

**A:** `sessions_spawn` 需要在 OpenClaw 会话内运行，而 cron 是系统级任务调度器，无法访问 OpenClaw 会话上下文。

### Q: GitHub Actions 能直接翻译吗？

**A:** 不能。GitHub Actions 运行在 GitHub 的服务器上，无法访问你本地的 Claude Code。

### Q: 如何确保不错过更新？

**A:** 启用 GitHub Actions 的 Issue 通知功能，或设置 GitHub 的"Watch"通知。

### Q: 翻译任务失败怎么办？

**A:** 
```bash
# 重新翻译单个文件
rm categories/git-and-github.zh.md
python3 scripts/auto-dispatch.py --all  # 会跳过已完成的
```

---

## 总结

**推荐方案：** 

1. **GitHub Watch** 上游仓库，收到更新通知
2. **每周手动运行一次** `./scripts/sync-upstream.sh`
3. **等待子代理完成翻译**（自动通知）
4. **提交并推送** 翻译结果

这样既保证了翻译质量（由本地 Claude 处理），又不会错过重要更新。

---

*最后更新：2026-03-02*
