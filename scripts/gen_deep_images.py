"""Generate all architecture diagrams for the deep technical article."""
import json, base64, time
from pathlib import Path
import openai

cfg = json.loads((Path.home() / ".gpt_image_studio" / "config.json").read_text("utf-8"))
client = openai.OpenAI(api_key=cfg["api_key"], base_url=cfg["base_url"])
out_dir = Path("F:/workspace/git/python/get-gpt-image")

IMAGES = [
    (
        "deep_oauth_pkce.png",
        """白底技术架构图，极简专业风格，浅灰色背景，深色字体，清晰易读。

        图题：「Sub2API 获取 ChatGPT Token 的完整流程（OAuth 2.0 PKCE）」

        从上到下的流程图，8个步骤，每步骤用圆角矩形框：

        步骤1：用户/运营方 → 触发授权请求
        步骤2：Sub2API生成 code_verifier + code_challenge（SHA256哈希）
        步骤3：跳转 accounts.google.com/o/oauth2/authorize（附带 client_id, scope, redirect_uri, code_challenge）
        步骤4：Google授权服务 → 返回 authorization_code
        步骤5：Sub2API 用 code + code_verifier 换取 token（POST https://auth0.openai.com/oauth/token）
        步骤6：OpenAI Auth服务 → 返回 access_token（1小时有效）+ refresh_token（长期有效）
        步骤7：Sub2API 缓存 token，存入账号池（最长30分钟缓存）
        步骤8：token到期前3分钟自动刷新，循环维持可用状态

        右侧注释框：
        - 「这是标准 OAuth 2.0 协议，不是破解或者假冒登录」
        - 「和你用Google账号登录第三方App完全相同的机制」

        底部标注：授权代码来源 openai_oauth_service.go lines 48-108

        整体配色：白底，蓝色流程箭头，步骤框浅蓝色填充，注释框浅黄色，字体黑色，无渐变，扁平风格。4K画质，专业排版。"""
    ),
    (
        "deep_request_transform.png",
        """白底技术架构图，极简专业风格，浅灰色背景，深色字体，清晰易读。

        图题：「Sub2API 请求转换：Images API → Responses API 工具调用」

        左右对比布局，中间有粗箭头和「Sub2API转换层」标签：

        左侧框（标题：「你发送的请求（Images API格式）」，蓝色边框）：
        POST /v1/images/generations
        {
          "model": "gpt-image-2",
          "prompt": "一只猫",
          "size": "1024x1024",
          "n": 4,
          "quality": "high",
          "background": "transparent",
          "output_format": "png"
        }

        中间：大箭头 →，箭头上方标注「Sub2API重构请求」，下方3行注释：
        ❌ n=4 → n=1（强制）
        ❌ background=transparent → 502
        ❌ 非标准尺寸 → 502

        右侧框（标题：「实际发出的请求（Responses API格式）」，橙色边框）：
        POST /v1/responses
        Authorization: Bearer {oauth_token}
        {
          "model": "gpt-image-2",
          "stream": true,
          "tools": [{
            "type": "image_generation",
            "size": "1024x1024",
            "quality": "high",
            "background": "auto"  // transparent被过滤
          }],
          "input": [{
            "type": "message",
            "role": "user",
            "content": [{"type":"text","text":"一只猫"}]
          }]
        }

        底部注释：「源码：openai_images_responses.go lines 220-301」

        整体配色：白底，左蓝右橙，代码区浅灰背景，等宽字体，字体黑色，无渐变，扁平风格。4K画质。"""
    ),
    (
        "deep_account_pool.png",
        """白底技术架构图，极简专业风格，浅灰色背景，深色字体，清晰易读。

        图题：「Sub2API 账号池调度与故障转移机制」

        整体布局从上到下：

        第一层（顶部）：「用户请求」方块

        第二层：「账号选择器（3级策略）」长方框，内含三行：
        策略1：Sticky Session → 优先使用上次请求的账号（会话粘性）
        策略2：Top-K 负载均衡 → 选最近20个成功账号中评分最高的
        策略3：随机兜底 → Top-K无可用时随机选一个

        第三层：3个并排的账号图标（Account A / Account B / Account C），每个图标下方显示「Plus订阅」标签

        第四层：「故障转移（Failover）」红色框，内含：
        当账号返回错误 → 标记账号为不可用 → 切换到下一个账号 → 最多重试3次

        右侧注释框（浅黄色）：
        - 账号池大小：运营方购买的订阅数量
        - 每个账号对应一个OAuth Token
        - 账号被封 = 服务直接中断

        底部：「源码：openai_account_scheduler.go + openai_images.go lines 140-250」

        整体配色：白底，绿色成功路径箭头，红色故障转移箭头，账号图标蓝色，字体黑色，扁平风格。4K画质。"""
    ),
    (
        "deep_full_arch.png",
        """白底技术全景架构图，极简专业风格，浅灰色背景，深色字体，清晰易读。

        图题：「Sub2API 完整运作架构图」

        三列布局（从左到右）：

        左列（用户侧）：
        - 「开发者」人形图标
        - 向下箭头
        - 「OpenAI SDK 调用」代码框：client.images.generate(model, prompt, size, n, background)

        中列（Sub2API层）, 从上到下多个模块用虚线框包围，标题「Sub2API 代理服务」：
        模块1（蓝色）：「请求接收层」- 解析 Images API 格式，参数校验
        模块2（橙色）：「Token 管理层」- OAuth Token获取/刷新/缓存（30min）
        模块3（红色）：「账号池调度层」- Sticky→Top-K→Random，故障转移
        模块4（紫色）：「请求转换层」- 重构为 Responses API 工具调用格式
        模块5（绿色）：「响应解析层」- 从 Responses 流式结果中提取图片URL/base64

        右列（OpenAI 侧）两条路径：
        上方路径（API Key账号，绿色箭头）：/v1/images/generations → 完整参数支持
        下方路径（OAuth账号，橙色箭头）：/v1/responses → 参数受限

        底部横向对比注释栏（3列）：
        「API Key路径」| 「OAuth路径（代理）」| 「ChatGPT网页」
        ✅ n支持 | ❌ n=1强制 | N/A
        ✅ transparent | ❌ 502 | N/A
        ✅ 任意尺寸 | ❌ 计费层级限制 | N/A

        整体配色：白底，各模块不同颜色，箭头清晰，扁平专业风格。4K画质。"""
    ),
    (
        "deep_cover.png",
        """专业技术文章封面图，白色背景，现代简洁设计风格。

        中央大标题（黑色粗体，最大字号）：「GPT-Image 代理站」
        副标题（深灰色，中等字号）：「原理深度解析 · 避坑实测指南」

        下方两个并排的对比卡片（圆角矩形）：
        左卡片（浅蓝色边框）：「官方 API Key」，内含✅图标和文字「完整8参数，直连模型」
        右卡片（浅橙色边框）：「Sub2API 代理」，内含⚠️图标和文字「OAuth受限，n=1，透明背景502」

        底部标签行：「基于 Sub2API 源码分析 + 25组API实测」

        整体风格：白底，商务简洁，无多余装饰，字体清晰，适合微信公众号封面。4K画质，宽幅横向构图（16:9比例）。"""
    ),
]

def gen(fname, prompt):
    print(f"[GEN] {fname} ...", flush=True)
    t0 = time.time()
    try:
        resp = client.images.generate(
            model="gpt-image-2",
            prompt=prompt,
            size="3840x2160",
            quality="high",
            output_format="png",
            n=1,
        )
        data = resp.data[0]
        if data.b64_json:
            raw = base64.b64decode(data.b64_json)
        else:
            import requests as rq
            raw = rq.get(data.url, timeout=120).content
        p = out_dir / fname
        p.write_bytes(raw)
        elapsed = round(time.time() - t0, 1)
        kb = len(raw) // 1024
        print(f"  -> saved {fname}  {kb}KB  {elapsed}s", flush=True)
        return True
    except Exception as e:
        print(f"  -> ERROR: {e}", flush=True)
        return False

for fname, prompt in IMAGES:
    ok = gen(fname, prompt)
    if not ok:
        print(f"  [SKIP] {fname}", flush=True)
    time.sleep(3)

print("\n[ALL DONE]")
