# 翻译自动化脚本使用指南

## 概述

本项目使用 **sessions_spawn** 派发翻译任务给子代理，实现批量自动化翻译。

## 核心脚本

### 1. `auto-dispatch.py` - 自动派发翻译任务

**功能：** 使用 sessions_spawn 批量派发翻译任务

```bash
# 查看所有待翻译文件
python3 scripts/auto-dispatch.py --status

# 派发所有待翻译任务
python3 scripts/auto-dispatch.py --all

# 派发指定数量的任务（如 5 个）
python3 scripts/auto-dispatch.py --dispatch 5

# 同步上游更新并派发新任务
python3 scripts/auto-dispatch.py --sync
```

**工作原理：**
1. 检查哪些分类文件尚未翻译
2. 为每个待翻译文件创建翻译提示词
3. 使用 `openclaw sessions_spawn` 派发任务给子代理
4. 记录任务状态到 `dispatch-state.json`

### 2. `sync-upstream.sh` - 同步上游更新

**功能：** 检查上游仓库变更，重新翻译更新的文件

```bash
# 查看翻译状态
./scripts/sync-upstream.sh --status

# 检查并同步上游更新
./scripts/sync-upstream.sh

# 强制重新翻译所有文件
./scripts/sync-upstream.sh --force

# 仅检查变更（不执行翻译）
./scripts/sync-upstream.sh --check
```

**工作流程：**
1. 从上游仓库 (`VoltAgent/awesome-openclaw-skills`) 获取最新提交
2. 比较本地与上游的差异
3. 识别变更的分类文件
4. 删除旧的中文翻译
5. 调用 `auto-dispatch.py` 重新翻译

### 3. `translate-direct.py` - 直接翻译（备用）

**功能：** 使用 subprocess 调用 claude 命令直接翻译

```bash
# 翻译单个分类
python3 scripts/translate-direct.py git-and-github

# 翻译所有分类
python3 scripts/translate-direct.py --all

# 查看状态
python3 scripts/translate-direct.py --status
```

## 完整工作流程

### 初次翻译

```bash
cd /Volumes/myDisk/workplace/awesome-openclaw-skills-zh

# 1. 查看所有待翻译文件
python3 scripts/auto-dispatch.py --status

# 2. 派发所有翻译任务
python3 scripts/auto-dispatch.py --all

# 3. 等待任务完成（子代理完成后会自动通知）

# 4. 检查翻译结果
ls -la categories/*.zh.md

# 5. 提交到 Git
git add -A
git commit -m "feat: 批量翻译所有分类"
git push
```

### 日常同步上游更新

```bash
# 每天执行一次
./scripts/sync-upstream.sh

# 或手动检查
python3 scripts/auto-dispatch.py --sync
```

### GitHub Actions 自动同步

项目包含两个工作流：

1. `.github/workflows/sync-daily.yml` - 每日检查上游更新
2. `.github/workflows/sync-and-translate.yml` - 同步并自动翻译

## 任务派发机制

### sessions_spawn 原理

```python
# auto-dispatch.py 中的核心代码
result = subprocess.run(
    ['openclaw', 'sessions_spawn', 
     '--mode', 'run', 
     '--label', f'translate-{category}', 
     '--task', prompt],
    capture_output=True,
    text=True
)
```

每个任务：
- 独立运行在子代理会话中
- 完成后自动通知主会话
- 失败不影响其他任务

### 任务状态追踪

状态保存在 `scripts/dispatch-state.json`:

```json
{
  "dispatched": [
    {
      "status": "dispatched",
      "session_key": "agent:main:subagent:xxx",
      "category": "ai-and-llms",
      "timestamp": "2026-03-02T13:33:00"
    }
  ],
  "completed": ["git-and-github", "ai-and-llms"],
  "last_update": "2026-03-02T13:33:00"
}
```

## 翻译规则

每个翻译任务遵循以下规则：

1. **完整翻译** - 包括所有技能描述
2. **保留格式** - Markdown 结构、链接、代码块不变
3. **技能名称** - 保持英文（如 `git-helper`）
4. **移除赞助商** - 删除 Gold/Silver/Bronze Sponsor 段落
5. **添加标注** - 文件末尾添加翻译来源信息

## 故障排除

### 任务派发失败

```bash
# 检查 openclaw 命令是否可用
openclaw --version

# 手动测试单个任务
python3 scripts/translate-direct.py git-and-github
```

### 翻译结果异常

```bash
# 查看任务日志
cat scripts/dispatch-state.json

# 重新翻译单个文件
rm categories/git-and-github.zh.md
python3 scripts/auto-dispatch.py --dispatch 1
```

### 同步冲突

```bash
# 强制重新翻译所有
./scripts/sync-upstream.sh --force

# 或手动清理
rm categories/*.zh.md
python3 scripts/auto-dispatch.py --all
```

## 最佳实践

1. **批量派发** - 一次派发所有待翻译任务，让子代理并行处理
2. **定期检查** - 每天运行一次同步脚本
3. **及时提交** - 翻译完成后尽快提交到 Git
4. **监控状态** - 使用 `--status` 查看进度

## 扩展

可以添加的功能：

- [ ] 翻译进度实时监控
- [ ] 翻译质量自动检查
- [ ] 失败任务自动重试
- [ ] 翻译统计报告
- [ ] 多语言支持

---

*最后更新：2026-03-02*
