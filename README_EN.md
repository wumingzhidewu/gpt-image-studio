<div align="center">
  <img src="assets/app_logo.png" width="120" alt="GPT-Image Studio Logo" />
  <h1>GPT-Image Studio</h1>
  <p><strong>A local GPT-Image-2 workspace for image generation, editing, and Xiaohongshu graphic posts</strong></p>
  <p>
    <a href="README.md">简体中文</a> | <a href="README_EN.md">English</a>
  </p>
</div>

---

GPT-Image Studio is a local desktop app for generating, editing, and managing images with GPT-Image models.

It is not designed to be a heavy online design platform. Instead, it focuses on the daily workflow around image generation: writing prompts, choosing model parameters, uploading reference images, saving history, reusing templates, and quickly creating Xiaohongshu-style graphic posters.

## Features

- Supports `gpt-image-2`, `gpt-image-1.5`, and `gpt-image-1`
- Defaults to `gpt-image-2`, `2K`, and `png`
- Explicit API `size` mapping from aspect ratio + resolution, so UI choices match the final request payload
- Supports both new image generation and reference-image editing workflows
- Upload reference images and continue editing existing outputs
- Dedicated inspiration template page with local thumbnails
- Dedicated Xiaohongshu graphic-post page with categorized templates
- Dedicated local history page for generated sessions
- Dark / light theme toggle
- Chinese / English UI toggle
- Supports official OpenAI endpoints and OpenAI-compatible proxies
- Can be packaged as a standalone Windows `.exe`

## Xiaohongshu Graphic-Post Mode

The Xiaohongshu mode is not just a generic image prompt collection. It provides complete graphic-poster prompts.

The current version includes 6 categories, with 3 templates per category:

- Wellness
- Home
- Food
- Beauty
- Fashion
- Local Life

Workflow:

1. Open **Xiaohongshu** from the left sidebar
2. Pick a category
3. Select a template
4. Edit the prompt if needed
5. Generate one 3:4 vertical graphic poster

Each template includes a title, subtitle, three content points, a footer reminder, background description, and layout requirements. The goal is to generate a finished poster-like image, not an editor screenshot or blank information card.

## Download Windows Standalone Build

Tagged releases provide a standalone Windows executable from GitHub Releases:

```text
GPT-Image-Studio-<version>.exe
```

Download and double-click to launch. No installer is required.

## Run from Source

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the app

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

## API Configuration

On first launch, open **API Settings** and configure:

- `API Key`: your OpenAI API key or proxy token
- `Base URL`: an OpenAI-compatible endpoint, such as `https://api.openai.com/v1` or your proxy URL
- `Default model`: the default image generation model

The local configuration file is stored at:

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

## Typical Use Cases

- Generate illustrations for WeChat articles, blogs, and product docs
- Create logos, covers, and promotional graphics for open-source projects
- Test different prompt styles with GPT-Image-2
- Continue editing from a reference image
- Quickly create Xiaohongshu covers or graphic-post posters
- Manage local generation history and continue previous work

## Project Structure

```text
.
├── main.py                  # App entry point
├── gpt_image_studio/        # Application package
│   ├── app.py               # QApplication bootstrap
│   ├── models.py            # Models, aspect ratios, resolutions, and size mapping
│   ├── config.py            # Local config persistence
│   ├── sessions.py          # Local generation history
│   ├── templates.py         # Inspiration and Xiaohongshu templates
│   ├── workers/             # Background API worker threads
│   └── ui/                  # PyQt6 UI components
├── assets/                  # App logo and template thumbnails
│   └── templates/
├── docs/                    # Docs and articles
├── scripts/                 # Development helper scripts
├── tests/                   # Lightweight tests
├── requirements.txt
├── requirements-build.txt
├── run.bat
└── README.md
```

## Test

```bash
python -m compileall -q main.py gpt_image_studio tests scripts
python tests/test_param_mapping.py
```

## Build a Standalone Windows Executable Locally

On Windows:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-build.txt
python -m compileall -q main.py gpt_image_studio tests scripts
python tests/test_param_mapping.py
pyinstaller --clean --noconfirm GPT-Image-Studio.spec
```

The executable is written to:

```text
dist/GPT-Image-Studio.exe
```

## Release Process

Maintainers can publish a release by pushing a version tag:

```bash
git tag v0.1.0
git push origin v0.1.0
```

Tags matching `v*` trigger the GitHub Actions workflow. The workflow runs source checks, builds the standalone Windows executable with PyInstaller, creates a GitHub Release, and uploads the `.exe` file.

## Proxy Notes

If you use an OpenAI-compatible proxy, behavior may differ from the official API. For example:

- `n` may be capped to 1
- Transparent background may not be supported
- Some sizes may be rejected
- Response formats may differ slightly from the official API

The app logs both UI parameters and final API request parameters to help verify what is actually sent.
