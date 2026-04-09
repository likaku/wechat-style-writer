#!/usr/bin/env python3
"""
重绘两张参考图：
1. ref_retail_stages.png  — 零售四阶段演变流程图
2. ref_ai_framework.png   — AI-Driven Retail Transformation 八大启示框架图

风格：与原图一致的蓝色系商务图表风格
"""
from PIL import Image, ImageDraw, ImageFont
import os, math

# ── 字体 ────────────────────────────────────────────────────────────────────
FONT_DIR = "/Users/kaku/.workbuddy/skills/canvas-design/canvas-fonts"
PINGFANG = "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/86ba2c91f017a3749571a82f2c6d890ac7ffb2fb.asset/AssetData/PingFang.ttc"

def ef(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

def cf(size, index=0):
    return ImageFont.truetype(PINGFANG, size, index=index)

OUT_DIR = "/Users/kaku/WorkBuddy/20260407113700"

# ── 配色 ────────────────────────────────────────────────────────────────────
NAVY      = (5, 28, 55)
DARK_BLUE = (15, 52, 96)
MID_BLUE  = (30, 90, 150)
LIGHT_BLUE = (70, 140, 200)
SKY_BLUE  = (120, 180, 230)
PALE_BLUE = (200, 220, 240)
WHITE     = (255, 255, 255)
GRAY_BG   = (245, 247, 250)
GRAY_TEXT = (100, 110, 125)
ORANGE    = (230, 140, 50)
TEAL      = (0, 178, 180)
GREEN     = (60, 170, 100)
CORAL     = (220, 90, 80)
PURPLE    = (120, 80, 170)


# ═══════════════════════════════════════════════════════════════════════════
# 图1：零售四阶段演变流程图
# ═══════════════════════════════════════════════════════════════════════════

def draw_retail_stages():
    W, H = 670, 520
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # 标题
    title_font = cf(22, index=3)
    sub_font = cf(14)
    d.text((W // 2, 28), "技术驱动零售四阶段演变", font=title_font, fill=NAVY, anchor="mm")
    d.text((W // 2, 54), "Technology-Driven Retail Evolution", font=ef("BricolageGrotesque-Regular.ttf", 13), fill=GRAY_TEXT, anchor="mm")

    # ── 四个阶段 ─────────────────────────────────────────────────────────
    stages = [
        {
            "title_zh": "线下零售",
            "title_en": "Traditional\nRetail",
            "period": "~2003",
            "color": MID_BLUE,
            "items": ["国有百货垄断", "物理购物文化", "有限竞争"],
            "tech": "3G 终结",
            "icon": "🏬",
        },
        {
            "title_zh": "货架电商",
            "title_en": "Shelf\nE-Commerce",
            "period": "2003-2015",
            "color": LIGHT_BLUE,
            "items": ["淘宝京东崛起", "支付宝信任体系", "CAGR 47%"],
            "tech": "5G 终结",
            "icon": "🖥️",
        },
        {
            "title_zh": "兴趣电商",
            "title_en": "Interest\nE-Commerce",
            "period": "2016-2025",
            "color": TEAL,
            "items": ["抖音快手小红书", "算法+直播", "GMV占比35%"],
            "tech": "AI 终结",
            "icon": "📱",
        },
        {
            "title_zh": "Agent 商业",
            "title_en": "Agentic\nDTC",
            "period": "2026+",
            "color": NAVY,
            "items": ["AI替代人决策", "Skill/API接口", "80%价值链重塑"],
            "tech": "NOW →",
            "icon": "🤖",
        },
    ]

    card_w = 140
    card_h = 310
    gap = 12
    total_w = len(stages) * card_w + (len(stages) - 1) * gap
    start_x = (W - total_w) // 2
    top_y = 80

    for i, st in enumerate(stages):
        cx = start_x + i * (card_w + gap)

        # 卡片背景
        d.rounded_rectangle(
            [cx, top_y, cx + card_w, top_y + card_h],
            radius=10,
            fill=st["color"],
        )

        # 时间标签
        period_font = ef("BricolageGrotesque-Bold.ttf", 12)
        d.text((cx + card_w // 2, top_y + 16), st["period"],
               font=period_font, fill=WHITE, anchor="mm")

        # Icon circle
        circle_y = top_y + 46
        circle_r = 24
        d.ellipse(
            [cx + card_w // 2 - circle_r, circle_y - circle_r,
             cx + card_w // 2 + circle_r, circle_y + circle_r],
            fill=(255, 255, 255, 60),
            outline=WHITE,
            width=2,
        )
        icon_font = cf(26)
        d.text((cx + card_w // 2, circle_y), st["icon"],
               font=icon_font, fill=WHITE, anchor="mm")

        # 中文标题
        zh_font = cf(17, index=3)
        d.text((cx + card_w // 2, circle_y + 38), st["title_zh"],
               font=zh_font, fill=WHITE, anchor="mm")

        # 英文标题
        en_font = ef("BricolageGrotesque-Regular.ttf", 11)
        en_lines = st["title_en"].split("\n")
        for j, line in enumerate(en_lines):
            d.text((cx + card_w // 2, circle_y + 58 + j * 14), line,
                   font=en_font, fill=(200, 220, 240), anchor="mm")

        # 分隔细线
        sep_y = circle_y + 58 + len(en_lines) * 14 + 8
        d.rectangle([cx + 20, sep_y, cx + card_w - 20, sep_y + 1],
                     fill=(255, 255, 255, 80))

        # 关键数据 items
        item_font = cf(12)
        item_y = sep_y + 12
        for item in st["items"]:
            d.text((cx + 16, item_y), f"· {item}",
                   font=item_font, fill=(220, 230, 240))
            item_y += 20

        # 底部技术标签
        tech_y = top_y + card_h - 30
        tech_font = ef("BricolageGrotesque-Bold.ttf", 11)
        if st["tech"] == "NOW →":
            # 高亮当前
            d.rounded_rectangle(
                [cx + 15, tech_y - 4, cx + card_w - 15, tech_y + 16],
                radius=8,
                fill=ORANGE,
            )
            d.text((cx + card_w // 2, tech_y + 6), "NOW →",
                   font=tech_font, fill=WHITE, anchor="mm")
        else:
            d.text((cx + card_w // 2, tech_y + 6), st["tech"],
                   font=tech_font, fill=(180, 200, 220), anchor="mm")

        # 箭头连接（除最后一个）
        if i < len(stages) - 1:
            arrow_x = cx + card_w + 1
            arrow_y = top_y + card_h // 2
            # 三角形箭头
            d.polygon(
                [(arrow_x, arrow_y - 6), (arrow_x + gap - 2, arrow_y), (arrow_x, arrow_y + 6)],
                fill=GRAY_TEXT,
            )

    # ── 底部时间轴 ────────────────────────────────────────────────────────
    timeline_y = top_y + card_h + 24
    d.rectangle([start_x, timeline_y, start_x + total_w, timeline_y + 2], fill=PALE_BLUE)

    milestones = [
        (0.0, "2003"),
        (0.33, "2015"),
        (0.55, "2016"),
        (0.78, "2025"),
        (1.0, "2026+"),
    ]
    ms_font = ef("BricolageGrotesque-Regular.ttf", 11)
    for pct, label in milestones:
        mx = start_x + int(total_w * pct)
        d.ellipse([mx - 3, timeline_y - 3, mx + 3, timeline_y + 5], fill=MID_BLUE)
        d.text((mx, timeline_y + 12), label, font=ms_font, fill=GRAY_TEXT, anchor="mm")

    # ── 底部说明 ──────────────────────────────────────────────────────────
    note_font = cf(11)
    d.text((W // 2, H - 20),
           "每一次零售变革，推手都不是零售人自己——是技术",
           font=note_font, fill=GRAY_TEXT, anchor="mm")

    # 签名
    sig_font = ef("NothingYouCouldDo-Regular.ttf", 14)
    d.text((W - 50, H - 18), "kaku", font=sig_font, fill=(190, 190, 190))

    out = os.path.join(OUT_DIR, "ref_retail_stages.png")
    img.save(out, "PNG", dpi=(150, 150))
    print(f"✅ Saved: {out} ({W}×{H})")
    return out


# ═══════════════════════════════════════════════════════════════════════════
# 图2：AI-Driven Retail Transformation 八大启示框架图
# ═══════════════════════════════════════════════════════════════════════════

def draw_ai_framework():
    W, H = 670, 620
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # 标题
    title_font = cf(22, index=3)
    d.text((W // 2, 28), "AI-Driven 零售转型八大启示",
           font=title_font, fill=NAVY, anchor="mm")
    d.text((W // 2, 54), "8 Imperatives for Agentic Retail Transformation",
           font=ef("BricolageGrotesque-Regular.ttf", 12), fill=GRAY_TEXT, anchor="mm")

    # ── 八个模块 ─────────────────────────────────────────────────────────
    modules = [
        {
            "num": "01",
            "title": "SEO → GEO",
            "desc": "优化 AI 搜索\n心智占位",
            "color": NAVY,
            "icon": "🔍",
        },
        {
            "num": "02",
            "title": "Agentic Insights",
            "desc": "数字孪生模拟\n360°消费预测",
            "color": DARK_BLUE,
            "icon": "📊",
        },
        {
            "num": "03",
            "title": "即时研发",
            "desc": "Agent汇聚需求\n按需C2M",
            "color": MID_BLUE,
            "icon": "⚡",
        },
        {
            "num": "04",
            "title": "AI 购买黑箱",
            "desc": "破解Agent\n筛选评分逻辑",
            "color": LIGHT_BLUE,
            "icon": "🔓",
        },
        {
            "num": "05",
            "title": "智能接口",
            "desc": "渠道→Skill/API\n被Agent调用",
            "color": TEAL,
            "icon": "🔌",
        },
        {
            "num": "06",
            "title": "机器营销",
            "desc": "Bot-to-Bot经济\n结构化说服",
            "color": GREEN,
            "icon": "🤝",
        },
        {
            "num": "07",
            "title": "仿生组织",
            "desc": "AI执行+人类创意\n重新分工",
            "color": PURPLE,
            "icon": "🧬",
        },
        {
            "num": "08",
            "title": "认知骨架",
            "desc": "数据中台→\n认知基础设施",
            "color": CORAL,
            "icon": "🧠",
        },
    ]

    # 布局：4×2 网格
    cols = 4
    rows = 2
    card_w = 142
    card_h = 195
    gap_x = 10
    gap_y = 14
    total_grid_w = cols * card_w + (cols - 1) * gap_x
    total_grid_h = rows * card_h + (rows - 1) * gap_y
    grid_x0 = (W - total_grid_w) // 2
    grid_y0 = 78

    for idx, mod in enumerate(modules):
        row = idx // cols
        col = idx % cols
        cx = grid_x0 + col * (card_w + gap_x)
        cy = grid_y0 + row * (card_h + gap_y)

        # 卡片圆角
        d.rounded_rectangle(
            [cx, cy, cx + card_w, cy + card_h],
            radius=10,
            fill=mod["color"],
        )

        # 序号
        num_font = ef("BricolageGrotesque-Bold.ttf", 28)
        d.text((cx + 14, cy + 10), mod["num"],
               font=num_font, fill=(255, 255, 255, 60))

        # Icon
        icon_y = cy + 52
        icon_font = cf(30)
        d.text((cx + card_w // 2, icon_y), mod["icon"],
               font=icon_font, fill=WHITE, anchor="mm")

        # 标题
        t_font = cf(15, index=3)
        d.text((cx + card_w // 2, icon_y + 32), mod["title"],
               font=t_font, fill=WHITE, anchor="mm")

        # 分隔线
        sep_y = icon_y + 50
        d.rectangle([cx + 20, sep_y, cx + card_w - 20, sep_y + 1],
                     fill=(255, 255, 255, 60))

        # 描述
        desc_font = cf(11)
        desc_lines = mod["desc"].split("\n")
        for j, line in enumerate(desc_lines):
            d.text((cx + card_w // 2, sep_y + 14 + j * 17), line,
                   font=desc_font, fill=(210, 225, 240), anchor="mm")

    # ── 底部总结条 ────────────────────────────────────────────────────────
    bar_y = grid_y0 + total_grid_h + 22
    d.rounded_rectangle(
        [grid_x0, bar_y, grid_x0 + total_grid_w, bar_y + 60],
        radius=8,
        fill=GRAY_BG,
    )

    # 中心标题
    bar_title = cf(15, index=3)
    d.text((W // 2, bar_y + 16), "核心逻辑：从「人找货」到「Agent 代理一切」",
           font=bar_title, fill=NAVY, anchor="mm")
    bar_sub = cf(12)
    d.text((W // 2, bar_y + 40),
           "品牌的竞争力 = 被 Agent 发现 × 被 Agent 理解 × 被 Agent 信任",
           font=bar_sub, fill=GRAY_TEXT, anchor="mm")

    # ── 底部来源 ──────────────────────────────────────────────────────────
    src_font = cf(10)
    d.text((W // 2, H - 22),
           "Source: Gartner 2025, McKinsey Retail Report, 作者分析",
           font=src_font, fill=(170, 175, 185), anchor="mm")

    # 签名
    sig_font = ef("NothingYouCouldDo-Regular.ttf", 14)
    d.text((W - 50, H - 20), "kaku", font=sig_font, fill=(190, 190, 190))

    out = os.path.join(OUT_DIR, "ref_ai_framework.png")
    img.save(out, "PNG", dpi=(150, 150))
    print(f"✅ Saved: {out} ({W}×{H})")
    return out


if __name__ == "__main__":
    draw_retail_stages()
    draw_ai_framework()
