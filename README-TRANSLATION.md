# 翻译自动化 - 使用说明

## 核心概念

### ⚠️ 重要：sessions_spawn 的限制

`sessions_spawn` **必须在 OpenClaw 会话内运行**，无法通过：
- ❌ cron 定时任务
- ❌ GitHub Actions
- ❌ 外部脚本直接调用

**原因：** `sessions_spawn` 需要访问 OpenClaw 会话上下文，这是外部进程无法提供的。

---

## 正确的工作流程

### 流程图解

```
┌─────────────────────────────────────────────────────────────┐
│ 1. 检查更新                                                  │
│    ./scripts/sync-upstream.sh                               │
│         │                                                    │
│         ▼                                                    │
│    发现上游有 5 个分类更新                                      │
│         │                                                    │
└─────────┼────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. 生成翻译任务提示词                                         │
│    python3 scripts/auto-dispatch.py --next 5                │
│         │                                                    │
│         ▼                                                    │
│    输出 5 个任务的完整提示词                                     │
│         │                                                    │
└─────────┼────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. 在 OpenClaw 会话中派发任务                                 │
│    复制提示词 → sessions_spawn(task="""...""")              │
│         │                                                    │
│         ▼                                                    │
│    创建 5 个子代理会话                                          │
│         │                                                    │
└─────────┼────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. 等待完成（自动通知）                                       │
│    [System Message] 翻译任务完成！                            │
│         │                                                    │
│         ▼                                                    │
│    检查 categories/*.zh.md                                   │
│         │                                                    │
└─────────┼────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. 提交并推送                                                │
│    git add -A && git commit && git push                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 具体操作步骤

### 步骤 1: 检查并同步上游更新

```bash
cd /Volumes/myDisk/workplace/awesome-openclaw-skills-zh

# 检查上游是否有更新
./scripts/sync-upstream.sh --check

# 如果有更新，同步并删除旧的翻译文件
./scripts/sync-upstream.sh
```

**输出示例：**
```
[2026-03-02 14:00:00] 📥 检查上游仓库更新...
[2026-03-02 14:00:01] 📊 本地提交：abc123
[2026-03-02 14:00:01] 📊 上游提交：def456
[2026-03-02 14:00:02] 📝 发现变更的分类文件:
[2026-03-02 14:00:02]   - categories/git-and-github.md
[2026-03-02 14:00:02]   - categories/ai-and-llms.md
[2026-03-02 14:00:02] 🗑️  删除旧版：git-and-github.zh.md
[2026-03-02 14:00:02] 🗑️  删除旧版：ai-and-llms.zh.md
```

---

### 步骤 2: 生成翻译任务提示词

```bash
# 查看还有哪些文件待翻译
python3 scripts/auto-dispatch.py --status

# 生成接下来 5 个任务的提示词
python3 scripts/auto-dispatch.py --next 5
```

**输出示例：**
```
=== 待翻译任务：5 个 ===

💡 使用方法：
1. 复制下面的提示词
2. 在 OpenClaw 会话中运行：sessions_spawn(task="""...提示词...""")
3. 子代理完成后会自动通知你

======================================================================

### 任务 1/5: browser-and-automation
======================================================================
请翻译此 OpenClaw Skills 分类文件为中文。

【任务】
- 输入：/Volumes/myDisk/workplace/awesome-openclaw-skills/categories/browser-and-automation.md
- 输出：/Volumes/myDisk/workplace/awesome-openclaw-skills-zh/categories/browser-and-automation.zh.md

【翻译规则】
1. 完整翻译所有内容，包括每个技能的描述
2. 保持技能名称为英文（如 git-helper）
3. 保留所有链接、代码块、图片、HTML 标签不变
4. 移除所有赞助商相关内容（Gold/Silver/Bronze Sponsor 段落）
5. 在文件末尾添加来源标注

【来源标注格式】
---
*翻译自：https://github.com/VoltAgent/awesome-openclaw-skills/blob/main/categories/browser-and-automation.md*
*翻译时间：2026-03-02*

请读取输入文件，翻译后写入输出文件。完成后回复"✅ 完成：browser-and-automation.zh.md"。

--- 任务 1 结束 ---

... (任务 2-5)
```

---

### 步骤 3: 在 OpenClaw 会话中派发任务

**复制步骤 2 输出的提示词**，然后在 OpenClaw 会话中运行：

```
sessions_spawn(task="""请翻译此 OpenClaw Skills 分类文件为中文。

【任务】
- 输入：/Volumes/myDisk/workplace/awesome-openclaw-skills/categories/browser-and-automation.md
- 输出：/Volumes/myDisk/workplace/awesome-openclaw-skills-zh/categories/browser-and-automation.zh.md

【翻译规则】
1. 完整翻译所有内容，包括每个技能的描述
2. 保持技能名称为英文（如 git-helper）
3. 保留所有链接、代码块、图片、HTML 标签不变
4. 移除所有赞助商相关内容（Gold/Silver/Bronze Sponsor 段落）
5. 在文件末尾添加来源标注

【来源标注格式】
---
*翻译自：https://github.com/VoltAgent/awesome-openclaw-skills/blob/main/categories/browser-and-automation.md*
*翻译时间：2026-03-02*

请读取输入文件，翻译后写入输出文件。完成后回复"✅ 完成：browser-and-automation.zh.md"。""", label="translate-browser-automation")
```

**或者批量派发（一次一个）：**

```
# 任务 1
sessions_spawn(task="""...任务 1 提示词...""", label="translate-1")

# 任务 2
sessions_spawn(task="""...任务 2 提示词...""", label="translate-2")

# ...
```

---

### 步骤 4: 等待完成（自动通知）

派发任务后，**子代理会在后台运行**，完成后你会收到自动通知：

```
[System Message] [sessionId: xxx] A subagent task "translate-browser-automation" just completed successfully.

Result:
✅ 完成：browser-and-automation.zh.md

Stats: runtime 2m15s • tokens 85.3k (in 72.1k / out 13.2k)
```

---

### 步骤 5: 检查并提交

```bash
# 检查翻译结果
ls -la categories/*.zh.md

# 查看新翻译的文件
git status

# 提交
git add -A
git commit -m "feat: 翻译更新 5 个分类 (2026-03-02)"
git push origin main
```

---

## 快速参考

### 常用命令

```bash
# 查看翻译状态
python3 scripts/auto-dispatch.py --status

# 生成接下来 N 个任务的提示词
python3 scripts/auto-dispatch.py --next 3

# 生成所有待翻译任务的提示词
python3 scripts/auto-dispatch.py --all

# 检查上游更新
./scripts/sync-upstream.sh --check

# 同步上游并删除旧翻译
./scripts/sync-upstream.sh

# 强制重新翻译所有
./scripts/sync-upstream.sh --force
```

### 任务派发模板

```
sessions_spawn(task="""请翻译此 OpenClaw Skills 分类文件为中文。

【任务】
- 输入：/Volumes/myDisk/workplace/awesome-openclaw-skills/categories/<分类名>.md
- 输出：/Volumes/myDisk/workplace/awesome-openclaw-skills-zh/categories/<分类名>.zh.md

【翻译规则】
1. 完整翻译所有内容，包括每个技能的描述
2. 保持技能名称为英文
3. 保留所有链接、代码块、图片、HTML 标签不变
4. 移除所有赞助商相关内容
5. 在文件末尾添加来源标注

请读取输入文件，翻译后写入输出文件。""", label="translate-<分类名>")
```

---

## GitHub Actions 通知

项目配置了 GitHub Actions，每周一 18:00 自动检查上游更新：

- **工作流文件：** `.github/workflows/sync-notify.yml`
- **触发条件：** 每周一 10:00 UTC (18:00 北京时间)
- **动作：** 发现更新时创建 Issue 通知你

**收到 Issue 后：**
1. 打开 Issue 查看变更文件列表
2. 在本地运行 `./scripts/sync-upstream.sh`
3. 继续上述步骤 2-5

---

## 常见问题

### Q: 为什么不能自动派发任务？

**A:** `sessions_spawn` 必须在 OpenClaw 会话内运行，外部脚本无法直接调用。这是 OpenClaw 的安全设计。

### Q: 可以一次性派发多个任务吗？

**A:** 可以！复制多个提示词，依次运行多个 `sessions_spawn` 命令。每个任务会创建独立的子代理会话，并行处理。

### Q: 任务失败怎么办？

**A:** 
1. 检查错误信息
2. 删除对应的 `.zh.md` 文件
3. 重新生成提示词并派发

### Q: 如何知道哪些任务完成了？

**A:** 
- 查看 `categories/*.zh.md` 文件
- 运行 `python3 scripts/auto-dispatch.py --status`
- 等待 System Message 通知

---

*最后更新：2026-03-02*
