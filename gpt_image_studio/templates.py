from .paths import TEMPLATE_DIR

GENERAL_CATEGORY = "通用创意 / General Creative"

GENERAL_TEMPLATES = [
    {"title": "霓虹产品海报", "category": GENERAL_CATEGORY, "image": TEMPLATE_DIR / "template_1.png", "prompt": "futuristic glass perfume bottle on reflective surface, cyan purple neon rim light, commercial product photography, premium advertising poster, ultra clean composition"},
    {"title": "温暖等距小屋", "category": GENERAL_CATEGORY, "image": TEMPLATE_DIR / "template_2.png", "prompt": "cozy isometric 3D room, tiny desk, warm lamp, soft pastel colors, miniature world, clean details, soft global illumination"},
    {"title": "赛博雨夜街景", "category": GENERAL_CATEGORY, "image": TEMPLATE_DIR / "template_3.png", "prompt": "cinematic cyberpunk rainy street in Tokyo, neon signs, reflections, wide angle, high detail, atmospheric lighting"},
    {"title": "可爱贴纸角色", "category": GENERAL_CATEGORY, "image": TEMPLATE_DIR / "template_4.png", "prompt": "cute mascot sticker, white border, expressive character, clean flat illustration, soft shadows, playful brand mascot"},
    {"title": "杂志级人像", "category": GENERAL_CATEGORY, "image": TEMPLATE_DIR / "template_5.png", "prompt": "editorial fashion portrait, dramatic studio lighting, elegant styling, magazine cover quality, sharp focus, refined color grading"},
    {"title": "AI 工具界面", "category": GENERAL_CATEGORY, "image": TEMPLATE_DIR / "template_6.png", "prompt": "clean landing page hero mockup for AI design tool, glassmorphism panels, blue purple gradient, modern UI, premium SaaS website"},
    {"title": "建筑空间", "category": GENERAL_CATEGORY, "image": TEMPLATE_DIR / "template_7.png", "prompt": "modern architectural interior, warm natural light, concrete and wood materials, editorial architecture photography, clean composition"},
    {"title": "美食摄影", "category": GENERAL_CATEGORY, "image": TEMPLATE_DIR / "template_8.png", "prompt": "premium food photography, steaming ramen bowl, dark ceramic table, soft studio light, appetizing commercial shot, shallow depth of field"},
    {"title": "国风插画", "category": GENERAL_CATEGORY, "image": TEMPLATE_DIR / "template_9.png", "prompt": "Chinese fantasy ink illustration, elegant heroine standing near misty mountains, flowing silk, gold accents, cinematic composition"},
    {"title": "像素游戏", "category": GENERAL_CATEGORY, "image": TEMPLATE_DIR / "template_10.png", "prompt": "pixel art game scene, cozy village at night, tiny characters, glowing windows, rich details, 16-bit style"},
    {"title": "电影海报", "category": GENERAL_CATEGORY, "image": TEMPLATE_DIR / "template_11.png", "prompt": "dramatic movie poster, lone astronaut walking through desert storm, bold title space, cinematic lighting, high contrast"},
    {"title": "包装设计", "category": GENERAL_CATEGORY, "image": TEMPLATE_DIR / "template_12.png", "prompt": "premium cosmetic packaging design mockup, frosted glass jar and box, elegant typography, soft shadows, clean studio background"},
    {"title": "儿童绘本", "category": GENERAL_CATEGORY, "image": TEMPLATE_DIR / "template_13.png", "prompt": "children picture book illustration, small fox reading under a tree, soft watercolor texture, warm colors, gentle dreamy atmosphere"},
    {"title": "机械概念", "category": GENERAL_CATEGORY, "image": TEMPLATE_DIR / "template_14.png", "prompt": "hard surface sci-fi robot concept art, white armor panels, blue light accents, industrial background, detailed design sheet"},
    {"title": "电商主图", "category": GENERAL_CATEGORY, "image": TEMPLATE_DIR / "template_15.png", "prompt": "clean ecommerce hero image, wireless headphones floating, white and blue background, crisp product lighting, commercial layout"},
    {"title": "自然风景", "category": GENERAL_CATEGORY, "image": TEMPLATE_DIR / "template_16.png", "prompt": "epic landscape photography, alpine lake at golden hour, dramatic clouds, mirror reflection, ultra wide angle, natural colors"},
    {"title": "字体海报", "category": GENERAL_CATEGORY, "image": TEMPLATE_DIR / "template_17.png", "prompt": "bold typography poster, huge 3D letters, black background, magenta blue gradient lighting, modern graphic design"},
    {"title": "App 图标", "category": GENERAL_CATEGORY, "image": TEMPLATE_DIR / "template_18.png", "prompt": "premium app icon, abstract 3D gradient shape, glossy material, dark background, minimal and recognizable, no text"},
]

XHS_POSTER_STYLE = (
    "生成一张最终可发布的小红书图文海报图片，不是编辑器界面、不是白底卡片截图、不是提示词说明。"
    "画面比例 3:4 竖版，整张图是完整设计海报：有主题化背景图、插画元素或生活场景，上面叠加清晰准确的中文标题和内容。"
    "标题要大、黑色粗体、位于上半部分；副标题紧跟标题下方；中下部排版 3 条编号要点，每条有彩色圆形数字、emoji 图标、加粗小标题和一句解释。"
    "底部用半透明色块写一句收藏/行动提醒；整体像小红书博主发布的封面图文，色彩明亮、留白舒适、移动端可读。"
    "不要出现『配图建议』，不要 UI 输入框，不要滚动条，不要网页窗口，不要水印，不要英文乱码，不要把提示词本身画出来。"
)


def xhs_poster_prompt(title: str, subtitle: str, points: list[tuple[str, str, str]], footer: str, scene: str) -> str:
    point_text = "\n".join(f"{i}. {emoji} {heading}：{desc}" for i, (emoji, heading, desc) in enumerate(points, 1))
    return (
        f"{XHS_POSTER_STYLE}\n"
        f"背景画面：{scene}\n"
        "把下面中文文案作为海报上的真实可读文字，不要遗漏，不要改成英文：\n"
        f"主标题：{title}\n"
        f"副标题：{subtitle}\n"
        f"三条内容：\n{point_text}\n"
        f"底部提醒：{footer}\n"
        "设计要求：文字区域可以用柔和半透明白色或浅色蒙层保证可读；标题最大最醒目；编号 1/2/3 使用红、橙、绿圆点；整体是成品海报图片，不是白底信息卡。"
    )

XIAOHONGSHU_TEMPLATES = [
    {
        "title": "夏日养生海报",
        "category": "健康养生 / Wellness",
        "image": TEMPLATE_DIR / "xiaohongshu_wellness_1.png",
        "prompt": xhs_poster_prompt(
            "🧢 女生夏天自救养生指南 🌿",
            "拒绝冷饮病！3 个小习惯养出好气色 ✨",
            [("🥤", "热饮替冷饮", "三豆汤、生脉饮、姜枣茶更适合空调房"), ("🧦", "护住脚踝", "办公室备薄袜，别让冷风直吹关节"), ("🛁", "睡前泡脚", "温水 15 分钟，放松身体更好睡")],
            "先收藏，今晚就从一杯温热饮开始。",
            "清爽夏日养生氛围，浅绿色和奶油白渐变背景，草本植物、温热饮品、阳光、冰块和空调风的柔和插画元素，干净治愈。",
        ),
        "tags": ["养生", "夏天", "女性健康"],
    },
    {
        "title": "熬夜恢复海报",
        "category": "健康养生 / Wellness",
        "image": TEMPLATE_DIR / "xiaohongshu_wellness_2.png",
        "prompt": xhs_poster_prompt(
            "😴 熬夜后别硬扛！这样补回来",
            "第二天没精神，先做这 3 件小事",
            [("💧", "先补温水", "起床先喝一杯，别立刻猛灌咖啡"), ("☀️", "晒 10 分钟太阳", "让身体重新找回白天节律"), ("🥣", "早餐加蛋白", "鸡蛋、牛奶、豆腐都能稳住状态")],
            "收藏起来，下次熬夜后照着做。",
            "晨光卧室和早餐桌生活场景，温水杯、鸡蛋牛奶、窗边阳光、柔软被子和绿植，浅黄色治愈氛围。",
        ),
        "tags": ["熬夜", "恢复", "养生"],
    },
    {
        "title": "办公室养生海报",
        "category": "健康养生 / Wellness",
        "image": TEMPLATE_DIR / "xiaohongshu_wellness_3.png",
        "prompt": xhs_poster_prompt(
            "💻 打工人办公室养生 3 件套",
            "久坐不舒服，先从这些小动作开始",
            [("🧘", "每小时站一站", "起身 2 分钟，比一直坐着舒服很多"), ("👀", "眼睛看远处", "盯屏幕久了，记得望向窗外"), ("🍵", "下午喝温茶", "少点冰饮，身体负担更小")],
            "不用大改生活，先改 3 个办公习惯。",
            "现代办公室桌面海报背景，电脑、保温杯、护眼绿植、便签、窗外阳光和简洁工位，清爽蓝绿色。",
        ),
        "tags": ["办公室", "久坐", "养生"],
    },
    {
        "title": "家居收纳海报",
        "category": "家居生活 / Home",
        "image": TEMPLATE_DIR / "xiaohongshu_home_1.png",
        "prompt": xhs_poster_prompt(
            "🏠 小家越住越乱？先改这 3 个收纳习惯",
            "不是柜子不够，是动线和分类没做好",
            [("📦", "高频放伸手区", "每天用的东西别藏太深，减少翻找"), ("🏷️", "同类只留一个家", "纸巾、药品、工具分别固定位置"), ("✨", "透明盒加标签", "一眼看见库存，补货和整理都更轻松")],
            "照这 3 步整理，小户型也能越住越清爽。",
            "明亮小户型客厅和收纳角的温柔插画背景，白色收纳盒、标签、木质小柜、绿植和自然光，奶油色系。",
        ),
        "tags": ["收纳", "家居", "小户型"],
    },
    {
        "title": "出租屋改造海报",
        "category": "家居生活 / Home",
        "image": TEMPLATE_DIR / "xiaohongshu_home_2.png",
        "prompt": xhs_poster_prompt(
            "🛋️ 出租屋不砸墙，也能变温柔小家",
            "低预算改造，先动这 3 个地方",
            [("💡", "换暖光灯", "氛围感马上提升，晚上更舒服"), ("🧺", "统一收纳色", "米白、木色、透明色最不容易乱"), ("🖼️", "墙面加软装", "挂布、海报、照片让空间有性格")],
            "不用大装修，小变化也能住得开心。",
            "温馨出租屋卧室客厅一角，暖光落地灯、米白床品、木质小桌、布艺挂画、收纳篮和绿植，胶片感。",
        ),
        "tags": ["出租屋", "改造", "软装"],
    },
    {
        "title": "清洁流程海报",
        "category": "家居生活 / Home",
        "image": TEMPLATE_DIR / "xiaohongshu_home_3.png",
        "prompt": xhs_poster_prompt(
            "🧹 周末大扫除别乱干！照这个顺序来",
            "省力又干净，家务效率直接翻倍",
            [("🪟", "先高后低", "先擦柜顶和窗台，最后再拖地"), ("🧽", "先干后湿", "先扫灰尘毛发，再用湿巾清洁"), ("🧴", "分区收尾", "厨房、浴室、客厅各留 10 分钟检查")],
            "按顺序做，打扫不再越做越崩溃。",
            "明亮家务清洁场景，阳光客厅、清洁喷雾、抹布、拖把、收纳桶、干净地板和清爽白绿色背景。",
        ),
        "tags": ["清洁", "家务", "周末"],
    },
    {
        "title": "夏日饮品海报",
        "category": "美食饮品 / Food",
        "image": TEMPLATE_DIR / "xiaohongshu_food_1.png",
        "prompt": xhs_poster_prompt(
            "🥤 冰镇饮料退退退！换成这三杯神仙饮",
            "夏天出汗多，别再猛灌冰水啦",
            [("🫘", "三豆汤", "解暑不伤脾，适合下午喝"), ("🌿", "生脉饮", "补气又清热，空调房很友好"), ("🍵", "姜枣茶", "早晨一杯，暖胃又舒服")],
            "把冷饮换成温和饮品，身体真的会轻松很多。",
            "日系夏日饮品海报背景，三杯不同颜色茶饮、玻璃杯、草本材料、便签、阳光桌面，清爽浅蓝和奶白色。",
        ),
        "tags": ["饮品", "测评", "夏日"],
    },
    {
        "title": "快手早餐海报",
        "category": "美食饮品 / Food",
        "image": TEMPLATE_DIR / "xiaohongshu_food_2.png",
        "prompt": xhs_poster_prompt(
            "🍳 早八人 10 分钟早餐公式",
            "不用早起很久，也能吃得像样",
            [("🥚", "蛋白质打底", "鸡蛋、酸奶、豆浆任选一个"), ("🍞", "主食别省", "全麦面包、燕麦、饭团都可以"), ("🍓", "加一份水果", "补充清爽口感，拍照也更好看")],
            "照公式搭配，早餐不再随便糊弄。",
            "明亮厨房早餐桌场景，煎蛋、吐司、酸奶、水果、咖啡杯、晨光和木质餐盘，清新食谱海报感。",
        ),
        "tags": ["早餐", "快手", "食谱"],
    },
    {
        "title": "周末甜品海报",
        "category": "美食饮品 / Food",
        "image": TEMPLATE_DIR / "xiaohongshu_food_3.png",
        "prompt": xhs_poster_prompt(
            "🍰 周末在家做甜品，氛围感拉满",
            "新手也能成功的 3 个小技巧",
            [("🍓", "水果选鲜艳", "草莓、蓝莓、芒果最容易出片"), ("🥣", "奶油少量多次", "慢慢调整口感，不容易太腻"), ("📸", "自然光拍照", "靠窗摆盘，比顶灯更柔和")],
            "甜品好吃，也要拍得好看。",
            "温柔下午茶甜品桌，草莓蛋糕、奶油碗、蓝莓、陶瓷盘、蕾丝桌布、窗边阳光，粉白色甜美海报。",
        ),
        "tags": ["甜品", "周末", "烘焙"],
    },
    {
        "title": "护肤避坑海报",
        "category": "美妆护肤 / Beauty",
        "image": TEMPLATE_DIR / "xiaohongshu_beauty_1.png",
        "prompt": xhs_poster_prompt(
            "🧴 皮肤越护越差？新手先避开这 3 个坑",
            "别急着叠产品，先把基础护肤做对",
            [("🫧", "少洗少搓", "别过度清洁，屏障比干净更重要"), ("☀️", "防晒别偷懒", "每天出门前都要认真涂够量"), ("🌙", "别乱叠猛药", "早 C 晚 A 先从低频低浓度开始")],
            "护肤先求稳，再谈进阶。",
            "干净浴室洗手台和护肤品插画背景，温和奶油白、淡粉色、镜面柔光、毛巾和瓶罐元素，清爽专业。",
        ),
        "tags": ["护肤", "避坑", "新手"],
    },
    {
        "title": "夏日底妆海报",
        "category": "美妆护肤 / Beauty",
        "image": TEMPLATE_DIR / "xiaohongshu_beauty_2.png",
        "prompt": xhs_poster_prompt(
            "💄 夏天底妆不斑驳，记住这 3 步",
            "出门 8 小时，也能保持清爽干净",
            [("🧊", "妆前先降温", "用湿敷或冷毛巾，让皮肤状态稳定"), ("🧴", "少量多次上妆", "底妆越薄越服帖，不要一次涂太厚"), ("🌫️", "分区定妆", "T 区重点控油，脸颊保留光泽")],
            "夏天底妆重点不是厚，是轻薄稳。",
            "夏日化妆台场景，粉底液、粉扑、散粉刷、镜子、冰感蓝色元素、阳光和清透水光质感，精致海报。",
        ),
        "tags": ["底妆", "夏天", "化妆"],
    },
    {
        "title": "空瓶复盘海报",
        "category": "美妆护肤 / Beauty",
        "image": TEMPLATE_DIR / "xiaohongshu_beauty_3.png",
        "prompt": xhs_poster_prompt(
            "🧾 护肤空瓶复盘：真正值得回购的 3 类",
            "别被种草带跑，先看自己皮肤需要什么",
            [("💧", "保湿精华", "干皮和屏障期都更容易用得上"), ("☀️", "通勤防晒", "肤感舒服，才会每天坚持涂"), ("🧼", "温和洁面", "洗完不紧绷，比洗得很干净更重要")],
            "理性回购，比盲买新品更省钱。",
            "美妆空瓶陈列海报背景，护肤瓶罐、购物小票、便签评分、淡粉色桌面和柔和灯光，测评博主风。",
        ),
        "tags": ["空瓶", "回购", "护肤测评"],
    },
    {
        "title": "通勤穿搭海报",
        "category": "穿搭时尚 / Fashion",
        "image": TEMPLATE_DIR / "xiaohongshu_fashion_1.png",
        "prompt": xhs_poster_prompt(
            "👗 普通人通勤穿搭，照这 3 个公式就够了",
            "不追爆款，也能穿出干净高级感",
            [("👕", "短上衣 + 高腰裤", "拉高比例，适合小个子"), ("👚", "衬衫 + 半裙", "温柔利落，约会通勤都能穿"), ("🧥", "西装 + 直筒裤", "线条干净，显高又有气场")],
            "统一色系 + 少量配饰，比堆单品更显贵。",
            "米色衣橱和穿搭灵感板背景，三套通勤 outfit 平铺、包包鞋子配饰、布料纹理，温柔高级的杂志海报感。",
        ),
        "tags": ["穿搭", "通勤", "公式"],
    },
    {
        "title": "小个子显高海报",
        "category": "穿搭时尚 / Fashion",
        "image": TEMPLATE_DIR / "xiaohongshu_fashion_2.png",
        "prompt": xhs_poster_prompt(
            "🧥 小个子显高穿搭，别只会穿厚底鞋",
            "比例对了，基础款也很显高",
            [("📏", "腰线往上提", "短外套和高腰裤最直接"), ("🎨", "上下同色系", "减少截断感，视觉更连贯"), ("👟", "鞋头选轻巧", "尖头、窄鞋型比笨重鞋更利落")],
            "显高不是堆单品，是调整比例。",
            "时尚穿搭海报背景，小个子模特剪影、衣架、鞋包配饰、全身镜、米白和浅咖色杂志排版氛围。",
        ),
        "tags": ["小个子", "显高", "穿搭"],
    },
    {
        "title": "衣橱断舍离海报",
        "category": "穿搭时尚 / Fashion",
        "image": TEMPLATE_DIR / "xiaohongshu_fashion_3.png",
        "prompt": xhs_poster_prompt(
            "👚 衣柜爆满还没衣服穿？先丢这 3 类",
            "整理完你会更清楚自己适合什么",
            [("📦", "一年没穿的", "不要等幻想场合，先给衣柜腾空间"), ("🪡", "版型不舒服的", "再好看也会降低穿出门概率"), ("🎯", "风格不匹配的", "和日常生活不搭，就很难反复穿")],
            "衣橱变少，搭配反而更轻松。",
            "整洁衣帽间海报背景，挂衣区、折叠衣物、收纳箱、标签、全身镜和柔和暖光，干净高级。",
        ),
        "tags": ["衣橱", "断舍离", "整理"],
    },
    {
        "title": "City Walk 海报",
        "category": "本地生活 / Local Life",
        "image": TEMPLATE_DIR / "xiaohongshu_local_1.png",
        "prompt": xhs_poster_prompt(
            "📍 周末 City Walk 路线，照着走就很出片",
            "咖啡店、街角小店、老建筑，一次安排好",
            [("☕", "上午咖啡店", "先点一杯拿铁，拍窗边自然光"), ("🏪", "中午逛小店", "找有招牌和街角感的位置"), ("🌇", "傍晚老街散步", "逆光拍照，氛围感直接拉满")],
            "不想远行，就在本地换个心情。",
            "城市街区旅行海报背景，手绘地图、咖啡杯、票根、手账本、街角小店和暖色阳光，轻松出片氛围。",
        ),
        "tags": ["本地生活", "city walk", "攻略"],
    },
    {
        "title": "周末探店海报",
        "category": "本地生活 / Local Life",
        "image": TEMPLATE_DIR / "xiaohongshu_local_2.png",
        "prompt": xhs_poster_prompt(
            "☕ 周末探店别只拍咖啡，记住这 3 张",
            "朋友圈和小红书都更有氛围感",
            [("🚪", "门头照", "招牌和入口最能交代地点"), ("🪑", "座位角落", "桌椅、窗景、灯光拍出环境感"), ("🥐", "食物特写", "饮品甜点靠近窗边更好看")],
            "下次探店，照这个清单拍就够。",
            "精品咖啡店探店海报背景，门头招牌、拿铁、可颂、窗边座位、票根贴纸和暖棕色街景，生活方式杂志感。",
        ),
        "tags": ["探店", "咖啡", "拍照"],
    },
    {
        "title": "短途旅行海报",
        "category": "本地生活 / Local Life",
        "image": TEMPLATE_DIR / "xiaohongshu_local_3.png",
        "prompt": xhs_poster_prompt(
            "🚄 1 天短途旅行，这样安排不累还出片",
            "适合不想请假、又想换心情的人",
            [("🎒", "轻装出发", "只带小包和充电宝，行动更自由"), ("📍", "少排景点", "一天 2-3 个点就够，不要赶路"), ("🌅", "留日落时间", "傍晚光线最好，照片更有故事感")],
            "周末不远行，也能拥有旅行感。",
            "短途旅行海报背景，高铁车票、小背包、城市地标、日落街道、相机和手绘路线图，轻松明亮。",
        ),
        "tags": ["旅行", "周末", "攻略"],
    },
]

TEMPLATE_CATEGORIES = [GENERAL_CATEGORY] + list(dict.fromkeys(t["category"] for t in XIAOHONGSHU_TEMPLATES))
TEMPLATES = GENERAL_TEMPLATES + XIAOHONGSHU_TEMPLATES
