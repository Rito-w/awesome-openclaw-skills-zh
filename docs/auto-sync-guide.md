# 🦞 Awesome OpenClaw Skills 翻译同步 - 完全自动化方案

## 📋 项目说明

- **本地仓库**: `/Volumes/myDisk/workplace/awesome-openclaw-skills-zh`
- **上游仓库**: `https://github.com/VoltAgent/awesome-openclaw-skills.git`
- **同步方式**: OpenClaw Cron 自动检测 + 自动翻译 + 自动提交

---

## ✅ 已删除的无效工作流

以下 GitHub Actions 工作流已删除（无法调用本地 Claude）：

- ❌ `sync-notify.yml` - 只能检测更新，无法翻译
- ❌ `sync-daily.yml` - 同上
- ❌ `sync-and-translate.yml` - 同上

---

## 🕐 新的自动化方案

### OpenClaw Cron 任务

| 项目 | 值 |
|------|-----|
| **任务 ID** | `981bf530-0559-4431-81f0-4fc5aed5f326` |
| **任务名称** | Awesome OpenClaw Skills 自动翻译同步 |
| **执行时间** | 每周二、四、六 上午 10:00 (Asia/Shanghai) |
| **运行模式** | 隔离会话 (isolated) |
| **消息投递** | 完成后发送到当前频道 |

### Cron 表达式

```
0 10 * * 2,4,6
│  │  │ │  └──── 星期 (2=周二，4=周四，6=周六)
│  │  │ └─────── 月份
│  │  └───────── 日期
│  └──────────── 小时 (10 点)
└─────────────── 分钟 (0 分)
```

---

## 🔄 自动化工作流程

```
┌─────────────────────────────────────────────────────────────┐
│ 定时任务触发 (每周二、四、六 10:00)                           │
│ OpenClaw Cron → 隔离 AI 会话                                   │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. 检查上游更新                                               │
│    cd /Volumes/myDisk/workplace/awesome-openclaw-skills-zh  │
│    git fetch upstream main                                   │
│    git diff --name-only HEAD..upstream/main                 │
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
    │ 2. 自动翻译      │       │ 回复            │
    │                 │       │ "无需同步"      │
    │ 读取英文原文     │       └─────────────────┘
    │ AI 翻译为中文    │
    │ 写入 .zh.md     │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────────────────────────────┐
    │ 3. 拉取上游变更 + 提交 + 推送              │
    │    git pull upstream main               │
    │    git add -A                           │
    │    git commit -m "feat: 同步翻译更新"    │
    │    git push origin main                 │
    └────────┬────────────────────────────────┘
             │
             ▼
    ┌─────────────────────────────────────────┐
    │ 4. 报告完成                              │
    │ - 同步了几个文件                         │
    │ - 每个文件的翻译统计                     │
    └─────────────────────────────────────────┘
```

---

## 🛠️ 管理命令

```bash
# 查看所有定时任务
openclaw cron list

# 手动触发测试（立即执行）
openclaw cron run 981bf530-0559-4431-81f0-4fc5aed5f326 --force

# 查看运行历史
openclaw cron runs --id 981bf530-0559-4431-81f0-4fc5aed5f326 --limit 10

# 修改执行频率
# 改为每天执行
openclaw cron edit 981bf530-0559-4431-81f0-4fc5aed5f326 --cron "0 10 * * *"

# 改为每周一、三、五
openclaw cron edit 981bf530-0559-4431-81f0-4fc5aed5f326 --cron "0 10 * * 1,3,5"

# 删除任务
openclaw cron remove 981bf530-0559-4431-81f0-4fc5aed5f326
```

---

## 📝 翻译规则

AI 翻译时遵循以下规则：

| 规则 | 说明 |
|------|------|
| **技能名称** | 保持英文（如 `git-helper`） |
| **链接/代码块** | 保留不变 |
| **图片/HTML** | 保留不变 |
| **赞助内容** | 移除 Gold/Silver/Bronze Sponsor 段落 |
| **来源标注** | 文件末尾添加翻译来源链接 |

### 来源标注格式

```markdown
---
*翻译自：https://github.com/VoltAgent/awesome-openclaw-skills/blob/main/categories/xxx.md*
*翻译时间：2026-03-05*
```

---

## 📊 查看翻译状态

```bash
cd /Volumes/myDisk/workplace/awesome-openclaw-skills-zh

# 查看已翻译文件数量
ls -la categories/*.zh.md | wc -l

# 查看翻译状态
python3 scripts/auto-dispatch.py --status

# 检查上游更新
git remote add upstream https://github.com/VoltAgent/awesome-openclaw-skills.git 2>/dev/null || true
git fetch upstream main --depth=1
git diff --name-only HEAD..upstream/main | grep "^categories/" | grep "\.md$" | grep -v "\.zh\.md$"
```

---

## ⚠️ 注意事项

### 1. Git 配置

确保已配置 git 用户信息：

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### 2. GitHub Token

如果需要推送，确保有写入权限：

- 方案 A: 使用 SSH key（推荐）
- 方案 B: 使用 Personal Access Token

### 3. 翻译质量

- AI 翻译可能不完美，建议定期人工 review
- 如有错误，手动修正后 commit 即可

### 4. 失败处理

如果任务失败，查看运行历史：

```bash
openclaw cron runs --id 981bf530-0559-4431-81f0-4fc5aed5f326 --limit 5
```

---

## 🔔 通知方式

任务完成后会自动发送消息到当前频道，包含：

- ✅/❌ 执行状态
- 📊 同步文件数量
- 📝 翻译统计

---

## 📈 与旧方案对比

| 特性 | 旧方案 (GitHub Actions) | 新方案 (OpenClaw Cron) |
|------|------------------------|------------------------|
| 检测更新 | ✅ | ✅ |
| 自动翻译 | ❌ | ✅ |
| 自动提交 | ❌ | ✅ |
| 自动推送 | ❌ | ✅ |
| 需要手动操作 | ✅ | ❌ |
| 调用本地 Claude | ❌ | ✅ |

---

*创建时间：2026-03-05*
*最后更新：2026-03-05*
