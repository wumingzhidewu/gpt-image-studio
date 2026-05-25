# GPT-Image Studio

A local desktop workspace for generating and editing images with GPT-Image models. It provides a polished PyQt6 interface, reusable inspiration templates, generation history, and OpenAI-compatible proxy configuration.

## Features

- GPT-Image generation with `gpt-image-2`, `gpt-image-1.5`, and `gpt-image-1`
- Default options: `gpt-image-2`, `2K`, `png`
- Explicit size mapping from aspect ratio + resolution, so selected UI options match API payloads
- Image edit workflow using a selected reference image
- Left sidebar history with resizable layout
- Separate Generate and Templates pages
- Built-in inspiration template gallery with local thumbnails
- Chinese / English UI toggle
- Local config and image storage under `~/.gpt_image_studio/`

## Requirements

- Python 3.10+
- PyQt6
- OpenAI Python SDK
- Pillow
- requests

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

Package mode is also supported:

```bash
python -m gpt_image_studio
```

On Windows, you can also double-click:

```bat
run.bat
```

## Configuration

On first launch, open **API Settings** and configure:

- `API Key`: your OpenAI API key or proxy token
- `Base URL`: OpenAI-compatible endpoint, for example `https://api.openai.com/v1` or a local proxy URL
- `Default model`: default generation model

The app stores local configuration at:

```text
~/.gpt_image_studio/config.json
```

Example:

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

Generated images and sessions are saved locally under:

```text
~/.gpt_image_studio/images/
~/.gpt_image_studio/sessions/
```

## Project Structure

```text
.
├── main.py                  # Thin compatibility launcher
├── gpt_image_studio/        # Application package
│   ├── app.py               # QApplication bootstrap
│   ├── models.py            # GPT-Image options and size mapping
│   ├── config.py            # Local config persistence
│   ├── sessions.py          # Local generation history
│   ├── workers/             # Background API workers
│   └── ui/                  # PyQt6 windows, dialogs, and widgets
├── assets/                  # App logo and template thumbnails
│   └── templates/
├── docs/                    # Articles, diagrams, and research notes
├── scripts/                 # Development and research helper scripts
├── tests/                   # Lightweight parameter mapping tests
├── requirements.txt
├── run.bat
└── README.md
```

## Test

```bash
python -m compileall -q main.py gpt_image_studio tests
python tests/test_param_mapping.py
```

## Proxy Notes

If you use an OpenAI-compatible proxy, behavior may differ from the official API. Some proxies cap `n` to 1, reject transparent background requests, or only support a subset of sizes. The app logs both UI parameters and final API request parameters to help verify what is actually sent.

---

# GPT-Image Studio（中文）

一个本地 GPT-Image 桌面工作台，用于生成、编辑和管理图片。应用基于 PyQt6，支持灵感模板、左侧历史记录、可调整侧边栏、图像编辑模式，以及 OpenAI 兼容代理配置。

## 功能

- 支持 `gpt-image-2`、`gpt-image-1.5`、`gpt-image-1`
- 默认选项：`gpt-image-2`、`2K`、`png`
- 根据「比例 + 分辨率」计算明确的 `size`，确保界面选择和实际 API 请求一致
- 选择参考图后进入图片编辑工作流
- 左侧历史记录与可拖动布局
- `图像生成` 和 `灵感模板` 是两个独立页面
- 内置灵感模板图库和本地缩略图
- 支持中文 / English 切换
- 配置、图片和历史记录都保存在本地

## 安装

```bash
pip install -r requirements.txt
```

## 启动

```bash
python main.py
```

也支持包模式启动：

```bash
python -m gpt_image_studio
```

Windows 也可以双击：

```bat
run.bat
```

## 配置

首次启动后，在 **API 设置** 中填写：

- `API Key`：OpenAI API Key 或代理 Token
- `Base URL`：OpenAI 兼容接口地址，例如 `https://api.openai.com/v1` 或本地代理地址
- `默认模型`：默认使用的生成模型

配置文件位置：

```text
~/.gpt_image_studio/config.json
```

生成图片与历史记录位置：

```text
~/.gpt_image_studio/images/
~/.gpt_image_studio/sessions/
```

## 自测

```bash
python -m compileall -q main.py gpt_image_studio tests
python tests/test_param_mapping.py
```

## 代理说明

如果使用 OpenAI 兼容代理，代理行为可能和官方 API 不完全一致。例如 `n` 可能被限制为 1，透明背景可能不支持，部分非标准尺寸可能失败。应用会记录 UI 参数和最终 API 请求参数，便于排查界面选择和实际请求是否一致。
