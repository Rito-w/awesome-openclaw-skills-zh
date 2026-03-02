# Awesome OpenClaw Skills 中文版 - 项目文档

## 项目概述

本项目是 [VoltAgent/awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills) 的中文翻译版本，旨在帮助中文用户发现和使用 OpenClaw 技能。

## 项目结构

```
awesome-openclaw-skills-zh/
├── README.md                    # 中文版主 README
├── categories/                  # 分类目录
│   ├── *.zh.md                 # 翻译后的分类文件
│   └── *.md                    # 原始英文文件（从上游同步）
├── scripts/                     # 自动化脚本
│   ├── sync-from-upstream.sh   # 从上游同步更新
│   ├── translate-category.sh   # 翻译分类文件
│   └── translate.py            # Python 翻译工具
└── .github/workflows/
    └── sync-daily.yml          # GitHub Actions 每日同步
```

## 已完成工作

### ✅ 阶段 1：项目初始化
- [x] 创建项目目录
- [x] 初始化 Git 仓库
- [x] 配置远程仓库（https://github.com/Rito-w/awesome-openclaw-skills-zh）

### ✅ 阶段 2：核心翻译
- [x] 翻译 README.md（标题、介绍、安装说明、安全提示、目录）
- [x] 翻译 30 个分类文件（保留英文技能列表确保链接准确）

### ✅ 阶段 3：自动化工具
- [x] 创建 `sync-from-upstream.sh` - 从上游识别变更
- [x] 创建 `translate-category.sh` - 批量翻译分类
- [x] 创建 GitHub Actions 工作流 - 每日自动检查更新

### ✅ 阶段 4：发布
- [x] 首次提交到 GitHub
- [x] 仓库公开可见

## 使用方法

### 手动同步上游更新

```bash
cd /Volumes/myDisk/workplace/awesome-openclaw-skills-zh
./scripts/sync-from-upstream.sh
```

### 翻译单个分类

```bash
./scripts/translate-category.sh categories/git-and-github.md
```

### 批量翻译所有分类

```bash
for f in categories/*.md; do
  ./scripts/translate-category.sh "$f"
done
```

## 自动同步流程

1. **GitHub Actions** 每天 18:00（北京时间）自动检查上游更新
2. 发现变更时自动创建 Issue 通知
3. 运行 `sync-from-upstream.sh` 识别需要翻译的文件
4. 使用 `translate-category.sh` 翻译新增/修改的分类
5. 提交翻译结果并推送

## 下一步建议

### 短期
- [ ] 完善 README 中的分类链接指向中文版
- [ ] 添加翻译贡献指南
- [ ] 设置 Issue 模板

### 中期
- [ ] 翻译技能描述的元数据（标题、简短描述）
- [ ] 添加搜索功能
- [ ] 创建技能索引（按中文名搜索）

### 长期
- [ ] 建立翻译审核流程
- [ ] 社区协作翻译平台
- [ ] 定期质量审查

## 统计信息

| 项目 | 数量 |
|------|------|
| 分类文件 | 30 个 |
| 技能总数 | 5,494 个 |
| 已翻译分类 | 30 个 (100%) |
| 技能描述翻译 | 待处理 |

## 相关仓库

- **上游仓库**: https://github.com/VoltAgent/awesome-openclaw-skills
- **本仓库**: https://github.com/Rito-w/awesome-openclaw-skills-zh
- **OpenClaw**: https://github.com/openclaw/openclaw
- **ClawHub**: https://www.clawhub.ai/

## 许可证

本项目遵循上游仓库的许可证（MIT）。

---

*最后更新：2026-03-02*
*维护者：@Rito-w*
