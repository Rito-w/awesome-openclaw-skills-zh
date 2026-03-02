<div align="center">

<a href="https://github.com/VoltAgent/voltagent">
<img width="1500" height="500" alt="social" src="https://github.com/user-attachments/assets/a6f310af-8fed-4766-9649-b190575b399d" />
</a>

<br/>
<br/>

<div align="center">
    <strong>探索 5494 个社区构建的 OpenClaw 技能，按分类组织。
    </strong>
    <br />
    <br />
</div>

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
<a href="https://github.com/VoltAgent/voltagent">
  <img alt="VoltAgent" src="https://cdn.voltagent.dev/website/logo/logo-2-svg.svg" height="20" />
</a> 

[![AI Agent Papers](https://img.shields.io/badge/AI%20Agent-研究论文-b31b1b)](https://github.com/VoltAgent/awesome-ai-agent-papers)
[![Skills Count](https://img.shields.io/badge/技能数 -5494-blue?style=flat-square)](#目录)
[![Last Update](https://img.shields.io/github/last-commit/VoltAgent/awesome-clawdbot-skills?label=最后更新&style=flat-square)](https://github.com/VoltAgent/awesome-clawdbot-skills/pulls?q=is%3Apr+is%3Amerged+sort%3Aupdated-desc)
[![Discord](https://img.shields.io/discord/1361559153780195478.svg?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2)](https://s.voltagent.dev/discord)
[![GitHub forks](https://img.shields.io/github/forks/VoltAgent/awesome-clawdbot-skills?style=social)](https://github.com/VoltAgent/awesome-clawdbot-skills/network/members)
</div>

# Awesome OpenClaw Skills 中文版

OpenClaw（曾用名 Moltbot，最初叫 Clawdbot... 身份危机包括在内，不额外收费）是一个在本地运行的 AI 助手，直接在你的机器上操作。技能扩展了它的能力，使其能够与外部服务交互、自动化工作流并执行 specialized 任务。这个集合帮助你发现和安装适合你需求的技能。

本列表中的技能来源于 [ClawHub](https://www.clawhub.ai/)（OpenClaw 的公共技能注册中心），并经过分类以便更容易发现。

## 安装

### ClawHub CLI

> **注意：** 正如你可能知道的，他们一直在改名。这反映了当前的官方文档。当他们再次改名时我们会更新。

```bash
npx clawhub@latest install <skill-slug>
```

### 手动安装

将技能文件夹复制到以下位置之一：

| 位置 | 路径 |
|----------|------|
| 全局 | `~/.openclaw/skills/` |
| 工作区 | `<project>/skills/` |

优先级：工作区 > 本地 > 捆绑

### 替代方案

你也可以将技能的 GitHub 仓库链接直接粘贴到你的助手的聊天中，并要求它使用它。助手将在后台自动处理设置。

## 为什么这个列表存在？

截至 2026 年 2 月 28 日，OpenClaw 的公共注册中心（ClawHub）托管了 **13,729 个社区构建的技能**。这个 awesome 列表包含 **5,494 个技能**。以下是我们过滤掉的内容：

| 过滤条件 | 排除数量 |
|--------|----------|
| 可能垃圾 — 批量账户、机器人账户、测试/垃圾 | 4,065 |
| 重复/相似名称 | 1,040 |
| 非英文 — 描述不是英文 | 604 |
| 加密货币/区块链/金融/交易 | 573 |
| 恶意 — 由研究人员发布的安全审计识别（不包括 VirusTotal） | 373 |
| 无或不充分的描述 — 版本号、元数据、少于 3 个词 | 247 |
| ERC / x402 / a2a 协议技能 | 38 |
| **未从 OpenClaw 官方技能注册中心采用的总数** | **6,940** |

## 安全提示

本列表中的技能经过**精选，但未审计**。它们可能在添加后随时被原始维护者更新、修改或替换。

在安装或使用任何 Agent Skill 之前，请自行审查潜在的安全风险并验证来源。OpenClaw 与 **VirusTotal** 合作，为技能提供安全扫描，访问 ClawHub 上技能的页面并查看 VirusTotal 报告，看看它是否被标记为有风险。

**推荐工具：**

- [Snyk Skill Security Scanner](https://github.com/snyk/agent-scan)
- [Agent Trust Hub](https://ai.gendigital.com/agent-trust-hub)

> Agent 技能可能包括提示注入、工具中毒、隐藏恶意软件负载或不安全的数据处理模式。在安装前务必审查源代码，并自行决定使用技能。

**想要添加技能？** 本列表仅包含**已发布**在 `github.com/openclaw/skills` 仓库中的技能。我们不接受个人仓库、gist 或任何其他外部来源的链接。如果你的技能还未在 OpenClaw 技能仓库中，请先在那里发布。详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

如果你认为本列表中的某个技能应该被标记或有安全问题，请 [提交 issue](https://github.com/VoltAgent/awesome-clawdbot-skills/issues) 以便我们审查。

## 目录

| | | |
|---|---|---|
| [Git & GitHub](#git--github) (170) | [Marketing & Sales](#marketing--sales) (104) | [Communication](#communication) (149) |
| [Coding Agents & IDEs](#coding-agents--ides) (1222) | [Productivity & Tasks](#productivity--tasks) (206) | [Speech & Transcription](#speech--transcription) (45) |
| [Browser & Automation](#browser--automation) (335) | [AI & LLMs](#ai--llms) (196) | [Smart Home & IoT](#smart-home--iot) (43) |
| [Web & Frontend Development](#web--frontend-development) (938) | [Data & Analytics](#data--analytics) (28) | [Shopping & E-commerce](#shopping--e-commerce) (55) |
| [DevOps & Cloud](#devops--cloud) (408) | [Finance](#finance) (21) | [Calendar & Scheduling](#calendar--scheduling) (61) |
| [Image & Video Generation](#image--video-generation) (169) | [Media & Streaming](#media--streaming) (85) | [PDF & Documents](#pdf--documents) (111) |
| [Apple Apps & Services](#apple-apps--services) (44) | [Notes & PKM](#notes--pkm) (71) | [Self-Hosted & Automation](#self-hosted--automation) (32) |
| [Search & Research](#search--research) (350) | [iOS & macOS Development](#ios--macos-development) (29) | [Security & Passwords](#security--passwords) (53) |
| [Clawdbot Tools](#clawdbot-tools) (35) | [Transportation](#transportation) (109) | [Moltbook](#moltbook) (29) |
| [CLI Utilities](#cli-utilities) (186) | [Personal Development](#personal-development) (51) | [Gaming](#gaming) (36) |
| [Health & Fitness](#health--fitness) (88) | [Agent-to-Agent Protocols](#agent-to-agent-protocols) (17) | |

## OpenClaw 部署技术栈

OpenClaw 代理的设置、托管和部署提供商。

**赞助位置保留为服务 OpenClaw 开发者和用户的托管、部署和设置提供商。**

📩 赞助咨询请联系：necati@voltagent.dev

<br/>

<div align="center">

<a href="#your-link-here">
<img src="https://placehold.co/800x120/1a1a2e/FFD700?text=金牌赞助 +&font=montserrat" alt="Gold Sponsor" width="800" height="120" />
</a>

<sub>你的产品描述在此 — 用一句话介绍你为 OpenClaw 开发者提供的服务。</sub>

<br/>

<a href="#your-link-here"><img src="https://placehold.co/380x90/1a1a2e/C0C0C0?text=银牌赞助&font=montserrat" alt="Silver Sponsor" width="380" height="90" /></a>&nbsp;&nbsp;&nbsp;<a href="#your-link-here"><img src="https://placehold.co/380x90/1a1a2e/C0C0C0?text=银牌赞助&font=montserrat" alt="Silver Sponsor" width="380" height="90" /></a>

<sub>简短描述在此。</sub>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<sub>简短描述在此。</sub>

<br/>

<a href="#your-link-here"><img src="https://placehold.co/220x60/1a1a2e/CD7F32?text=铜牌赞助&font=montserrat" alt="Bronze Sponsor" width="220" height="60" /></a>&nbsp;&nbsp;<a href="#your-link-here"><img src="https://placehold.co/220x60/1a1a2e/CD7F32?text=铜牌赞助&font=montserrat" alt="Bronze Sponsor" width="220" height="60" /></a>&nbsp;&nbsp;<a href="#your-link-here"><img src="https://placehold.co/220x60/1a1a2e/CD7F32?text=铜牌赞助&font=montserrat" alt="Bronze Sponsor" width="220" height="60" /></a>

</div>

<br/>

---

## 技能分类详情

> 以下分类文件已翻译，点击查看详情：

| 分类 | 技能数 | 翻译状态 |
|------|--------|----------|
| Git & GitHub | 170 | ✅ 已翻译 |
| Coding Agents & IDEs | 1222 | ✅ 已翻译 |
| Browser & Automation | 335 | ✅ 已翻译 |
| Web & Frontend Development | 938 | ✅ 已翻译 |
| DevOps & Cloud | 408 | ✅ 已翻译 |
| AI & LLMs | 196 | ✅ 已翻译 |
| ... | ... | 进行中 |

---

## 自动同步状态

- **最后同步时间:** 2026-03-02 13:08 CST
- **上游仓库:** https://github.com/VoltAgent/awesome-openclaw-skills
- **本仓库:** https://github.com/Rito-w/awesome-openclaw-skills-zh

---

## 贡献

欢迎提交 Issue 和 Pull Request 来改进翻译质量或添加新的分类翻译！

---

*本中文版由社区维护，旨在帮助中文用户发现和使用 OpenClaw 技能。*
