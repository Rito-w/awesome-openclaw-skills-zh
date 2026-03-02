# 自动化翻译方案

## 问题解答

### Q1: 怎么派发的翻译任务？

**答：** 使用 `sessions_spawn` 将每个文件的翻译任务派发给独立的子代理会话。

**派发方式：**
```python
# 核心代码示例
import subprocess

prompt = """请翻译此 OpenClaw Skills 分类文件为中文..."""

result = subprocess.run(
    ['openclaw', 'sessions_spawn', 
     '--mode', 'run', 
     '--label', 'translate-category', 
     '--task', prompt],
    capture_output=True,
    text=True
)
```

每个任务：
- 独立运行在子代理中
- 完成后自动通知主会话
- 并行处理，互不阻塞

### Q2: 可以写个脚本循环派发吗？

**答：** 可以！已创建以下脚本：

#### `scripts/dispatch-all.py` - 批量派发脚本

```bash
# 查看所有待翻译任务
python3 scripts/dispatch-all.py --list

# 输出接下来 5 个任务的完整提示词
python3 scripts/dispatch-all.py --next 5

# 输出所有待翻译任务（可直接复制使用）
python3 scripts/dispatch-all.py
```

#### `scripts/auto-dispatch.py` - 自动派发脚本

```bash
# 查看翻译状态
python3 scripts/auto-dispatch.py --status

# 派发所有待翻译任务
python3 scripts/auto-dispatch.py --all

# 同步上游并派发新任务
python3 scripts/auto-dispatch.py --sync
```

### Q3: 后续要同步原仓库更新怎么做？

**答：** 有三种方式：

#### 方式 1: 手动同步（推荐）

```bash
cd /Volumes/myDisk/workplace/awesome-openclaw-skills-zh

# 检查并同步上游更新
./scripts/sync-upstream.sh

# 或
python3 scripts/auto-dispatch.py --sync
```

**工作流程：**
1. 从上游仓库 (`VoltAgent/awesome-openclaw-skills`) 获取最新提交
2. 识别变更的分类文件
3. 删除旧的中文翻译
4. 自动派发重新翻译任务

#### 方式 2: GitHub Actions 自动同步

项目包含自动同步工作流：

- `.github/workflows/sync-and-translate.yml` - 每天 18:00 检查更新
- 发现变更时自动创建 Issue 通知
- 可选择自动重新翻译

#### 方式 3: 本地 cron 定时任务

```bash
# 添加到 crontab (每天 18:00 执行)
0 18 * * * cd /Volumes/myDisk/workplace/awesome-openclaw-skills-zh && ./scripts/sync-upstream.sh
```

## 完整工作流程

### 初次翻译

```bash
# 1. 查看状态
python3 scripts/auto-dispatch.py --status

# 2. 派发所有翻译任务
python3 scripts/auto-dispatch.py --all

# 3. 等待任务完成（子代理完成后会自动通知）

# 4. 检查结果
ls -la categories/*.zh.md

# 5. 提交到 Git
git add -A
git commit -m "feat: 批量翻译所有分类"
git push origin main
```

### 日常同步

```bash
# 每天执行一次
./scripts/sync-upstream.sh

# 或手动检查
python3 scripts/auto-dispatch.py --sync
```

## 脚本说明

| 脚本 | 功能 | 用法 |
|------|------|------|
| `dispatch-all.py` | 输出待翻译任务提示词 | `python3 dispatch-all.py --next 5` |
| `auto-dispatch.py` | 自动派发翻译任务 | `python3 auto-dispatch.py --all` |
| `sync-upstream.sh` | 同步上游更新 | `./sync-upstream.sh` |
| `translate-direct.py` | 直接翻译（备用） | `python3 translate-direct.py --all` |

## 翻译规则

所有翻译任务遵循以下规则：

1. ✅ **完整翻译** - 包括所有技能描述
2. ✅ **保留格式** - Markdown 结构、链接、代码块不变
3. ✅ **技能名称** - 保持英文（如 `git-helper`）
4. ✅ **移除赞助商** - 删除 Gold/Silver/Bronze Sponsor 段落
5. ✅ **添加标注** - 文件末尾添加翻译来源信息

## 当前状态

```
总计：30 个分类
已完成：2 个 (git-and-github, ai-and-llms)
待翻译：28 个
```

## 扩展建议

可以添加的功能：

- [ ] 翻译进度实时监控面板
- [ ] 失败任务自动重试机制
- [ ] 翻译质量自动检查（术语一致性等）
- [ ] 翻译统计报告生成
- [ ] 多语言支持（日语、韩语等）

---

*最后更新：2026-03-02*
