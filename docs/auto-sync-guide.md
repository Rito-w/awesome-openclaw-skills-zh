# 🦞 Awesome OpenClaw Skills 翻译同步 - 自动化方案

## 📋 项目说明

- **本地仓库**: `/Volumes/myDisk/workplace/awesome-openclaw-skills-zh`
- **上游仓库**: `https://github.com/VoltAgent/awesome-openclaw-skills.git`
- **同步方式**: OpenClaw Cron 自动检测 → 派发子任务翻译 → 自动提交推送

---

## 🕐 Cron 任务配置

| 项目 | 值 |
|------|-----|
| **任务 ID** | `c41403b8-985f-41ae-ac31-8bd86e3da17d` |
| **任务名称** | Awesome OpenClaw Skills 自动翻译同步 |
| **执行时间** | 每周二、四、六 上午 10:00 (Asia/Shanghai) |
| **下次运行** | 约 2 天后 |
| **运行模式** | 隔离会话 + 子任务派发 |

---

## 🔄 自动化流程

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Cron 触发 (每周二、四、六 10:00)                           │
│    进入项目目录，检查上游更新                                 │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
                    ┌─────────────┐
                    │ 有变更文件？ │
                    └──────┬──────┘
                           │
              ┌────────────┴────────────┐
              │                         │
             是                        否
              │                         │
              ▼                         ▼
    ┌─────────────────┐       ┌─────────────────┐
    │ 2. 拉取英文原文  │       │ 回复            │
    │    git checkout │       │ "无需同步"      │
    └────────┬────────┘       └─────────────────┘
             │
             ▼
    ┌─────────────────────────────────────────┐
    │ 3. 为每个文件派发翻译子任务              │
    │    sessions_spawn (mode: run)           │
    │    ┌───────┐ ┌───────┐ ┌───────┐       │
    │    │ 子任务│ │ 子任务│ │ 子任务│  ...  │
    │    │ 翻译  │ │ 翻译  │ │ 翻译  │       │
    │    └───────┘ └───────┘ └───────┘       │
    └─────────────────┬───────────────────────┘
                      │
                      ▼
    ┌─────────────────────────────────────────┐
    │ 4. 所有翻译完成后提交推送                │
    │    git add → commit → push              │
    └─────────────────┬───────────────────────┘
                      │
                      ▼
    ┌─────────────────────────────────────────┐
    │ 5. 报告完成                              │
    │    同步文件数 + 列表                     │
    └─────────────────────────────────────────┘
```

---

## 📊 当前状态

### 已完成
- ✅ 30 个英文原文件已同步 (2026-03-05)
- ✅ 1 个文件已翻译：`ai-and-llms.zh.md`
- ✅ Cron 任务已配置

### 待翻译 (29 个文件)
- apple-apps-and-services.zh.md
- browser-and-automation.zh.md
- calendar-and-scheduling.zh.md
- clawdbot-tools.zh.md
- cli-utilities.zh.md
- coding-agents-and-ides.zh.md
- communication.zh.md
- data-and-analytics.zh.md
- devops-and-cloud.zh.md
- gaming.zh.md
- git-and-github.zh.md
- health-and-fitness.zh.md
- image-and-video-generation.zh.md
- ios-and-macos-development.zh.md
- marketing-and-sales.zh.md
- media-and-streaming.zh.md
- moltbook.zh.md
- notes-and-pkm.zh.md
- pdf-and-documents.zh.md
- personal-development.zh.md
- productivity-and-tasks.zh.md
- search-and-research.zh.md
- security-and-passwords.zh.md
- self-hosted-and-automation.zh.md
- shopping-and-e-commerce.zh.md
- smart-home-and-iot.zh.md
- speech-and-transcription.zh.md
- transportation.zh.md
- web-and-frontend-development.zh.md

---

## 🛠️ 管理命令

```bash
# 查看 Cron 任务
openclaw cron list

# 手动触发同步
openclaw cron run c41403b8-985f-41ae-ac31-8bd86e3da17d

# 查看运行历史
openclaw cron runs --id c41403b8-985f-41ae-ac31-8bd86e3da17d --limit 5

# 修改执行频率
# 改为每天执行
openclaw cron edit c41403b8-985f-41ae-ac31-8bd86e3da17d --cron "0 10 * * *"

# 删除任务
openclaw cron remove c41403b8-985f-41ae-ac31-8bd86e3da17d
```

---

## 📝 翻译规则

| 规则 | 说明 |
|------|------|
| **标题和描述** | 全部翻译成中文 |
| **技能名称** | 保持英文（如 git-helper, claude-code） |
| **链接/代码块** | 保持原样不变 |
| **图片/HTML** | 保持原样不变 |
| **赞助内容** | 删除 Gold/Silver/Bronze Sponsor 段落 |
| **来源标注** | 文件末尾添加翻译来源链接 |

### 来源标注格式

```markdown
---
*翻译自：https://github.com/VoltAgent/awesome-openclaw-skills/blob/main/categories/xxx.md*
*翻译时间：2026-03-05*
```

---

## ⚠️ 注意事项

### 1. 翻译时间
- 每个文件约需 2-5 分钟
- 30 个文件全部翻译约需 1-2 小时
- 建议分批执行或等待 Cron 自动处理

### 2. Git 配置
确保已配置 git 用户信息：
```bash
git config --global user.name "wrt"
git config --global user.email "your@email.com"
```

### 3. 推送权限
确保有 GitHub 仓库写入权限：
```bash
# 测试推送
git push origin main
```

### 4. 失败处理
如果任务失败，查看运行历史：
```bash
openclaw cron runs --id c41403b8-985f-41ae-ac31-8bd86e3da17d --limit 5
```

---

## 📈 与旧方案对比

| 特性 | 旧方案 (GitHub Actions) | 新方案 (OpenClaw Cron) |
|------|------------------------|------------------------|
| 检测更新 | ✅ | ✅ |
| 自动翻译 | ❌ | ✅ (派发子任务) |
| 自动提交 | ❌ | ✅ |
| 自动推送 | ❌ | ✅ |
| 需要手动操作 | ✅ | ❌ |
| 使用 Claude | ❌ | ✅ (子任务) |

---

## 🚀 立即翻译剩余文件

如果想立即翻译剩余 29 个文件，可以手动触发：

```bash
openclaw cron run c41403b8-985f-41ae-ac31-8bd86e3da17d
```

或者分批派发子任务：

```bash
# 在 OpenClaw 会话中
sessions_spawn(task="翻译 categories/browser-and-automation.md 为中文...", label="translate-1")
sessions_spawn(task="翻译 categories/calendar-and-scheduling.md 为中文...", label="translate-2")
# ...
```

---

*创建时间：2026-03-05*
*最后更新：2026-03-05 11:20*
