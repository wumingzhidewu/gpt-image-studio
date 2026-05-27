<div align="center">
  <img src="assets/app_logo.png" width="120" alt="GPT-Image Studio Logo" />
  <h1>GPT-Image Studio</h1>
  <p><strong>本地 GPT-Image-2 图像生成、编辑与小红书图文工作台</strong></p>
  <p>
    <a href="README.md">简体中文</a> | <a href="README_EN.md">English</a>
  </p>
</div>

---

GPT-Image Studio 是一个本地桌面端图像生成工具，用来调用 GPT-Image 系列模型生成、编辑和管理图片。

它的目标不是做一个复杂的在线平台，而是把日常生图里最常用的几件事放到一个本地工作台里：写提示词、选模型参数、上传参考图、保存历史、复用模板，以及一键生成小红书图文海报。

## 功能特性

- 支持 `gpt-image-2`、`gpt-image-1.5`、`gpt-image-1`
- 默认使用 `gpt-image-2`、`2K`、`png`
- 根据「画面比例 + 分辨率」明确计算 API `size`，避免界面选择和实际请求不一致
- 支持普通图像生成和参考图编辑模式
- 支持上传参考图继续编辑已有图片
- 独立的灵感模板页，内置多种提示词模板和本地预览图
- 独立的小红书图文页，按分类选择模板，一步生成图文海报
- 独立的历史生成页，生成记录和图片保存在本地
- 支持深色 / 浅色主题切换
- 支持中文 / English 界面切换
- 支持 OpenAI 官方接口或 OpenAI 兼容代理
- Windows 可打包为免安装 `.exe`

## 小红书图文模式

小红书图文不是普通配图，而是完整的图文海报提示词模板。

当前内置 6 个分类，每个分类 3 个模板：

- 健康养生
- 家居生活
- 美食饮品
- 美妆护肤
- 穿搭时尚
- 本地生活

使用流程：

1. 打开左侧 **小红书图文**
2. 选择分类
3. 选择一个模板
4. 按需要修改提示词
5. 点击生成，得到一张 3:4 竖版图文海报

模板提示词包含标题、副标题、三条内容、底部提醒、画面背景和排版要求，目标是直接生成可发布风格的图文海报，而不是编辑器截图或空白信息卡。

## 下载 Windows 免安装版

正式版本会在 GitHub Releases 中提供 Windows 免安装文件：

```text
GPT-Image-Studio-<version>.exe
```

下载后双击即可启动，不需要安装。

## 从源码运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动应用

```bash
python main.py
```

也支持包模式启动：

```bash
python -m gpt_image_studio
```

Windows 下也可以双击：

```bat
run.bat
```

## 配置 API

首次启动后，点击左下角 **API 设置**，填写：

- `API Key`：OpenAI API Key 或兼容代理 Token
- `Base URL`：OpenAI 兼容接口地址，例如 `https://api.openai.com/v1` 或你的代理地址
- `默认模型`：默认使用的图像生成模型

配置文件保存在本地：

```text
~/.gpt_image_studio/config.json
```

示例：

```json
{
  "api_key": "sk-...",
  "base_url": "https://api.openai.com/v1",
  "model": "gpt-image-2",
  "language": "zh",
  "default_aspect": "方形 1:1",
  "default_resolution": "2K",
  "default_quality": "auto",
  "default_format": "png"
}
```

生成图片和历史记录保存在：

```text
~/.gpt_image_studio/images/
~/.gpt_image_studio/sessions/
```

## 典型使用场景

- 给公众号、博客、产品文档生成配图
- 给开源项目生成 logo、封面图、宣传图
- 使用 GPT-Image-2 批量测试不同提示词风格
- 基于参考图继续编辑图片
- 快速生成小红书封面或图文海报
- 管理本地生成历史，方便回看和继续编辑

## 项目结构

```text
.
├── main.py                  # 启动入口
├── gpt_image_studio/        # 应用主包
│   ├── app.py               # QApplication 启动逻辑
│   ├── models.py            # 模型、比例、分辨率和 size 映射
│   ├── config.py            # 本地配置读写
│   ├── sessions.py          # 本地历史记录
│   ├── templates.py         # 灵感模板和小红书模板
│   ├── workers/             # 后台 API 调用线程
│   └── ui/                  # PyQt6 界面组件
├── assets/                  # 应用图标和模板预览图
│   └── templates/
├── docs/                    # 文档和文章
├── scripts/                 # 开发辅助脚本
├── tests/                   # 轻量测试
├── requirements.txt
├── requirements-build.txt
├── run.bat
└── README.md
```

## 自测

```bash
python -m compileall -q main.py gpt_image_studio tests scripts
python tests/test_param_mapping.py
```

## 本地构建 Windows 免安装 exe

在 Windows 上执行：

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-build.txt
python -m compileall -q main.py gpt_image_studio tests scripts
python tests/test_param_mapping.py
pyinstaller --clean --noconfirm GPT-Image-Studio.spec
```

生成文件位置：

```text
dist/GPT-Image-Studio.exe
```

## 发布流程

维护者推送版本标签即可触发 GitHub Actions 自动构建和发布：

```bash
git tag v0.1.0
git push origin v0.1.0
```

匹配 `v*` 的标签会触发 Windows 构建流程：运行源码检查，使用 PyInstaller 构建免安装 exe，并把 `.exe` 上传到 GitHub Release。

## 代理说明

如果使用 OpenAI 兼容代理，代理行为可能和官方 API 不完全一致。例如：

- `n` 可能被限制为 1
- 透明背景可能不支持
- 部分尺寸可能不支持
- 返回格式可能和官方接口略有差异

应用会记录界面参数和最终 API 请求参数，方便排查界面选择和实际请求是否一致。
