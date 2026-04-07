#!/usr/bin/env python3
"""
WorkBuddy Poster - Style 2 REFINED: Neon Archaeology (赛博朋克·数字律动)
3:4 ratio, 900x1200px — with proper CJK font support
"""
from PIL import Image, ImageDraw, ImageFont
import os

FONT_DIR = "/Users/kaku/.workbuddy/skills/canvas-design/canvas-fonts"
PINGFANG = "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/86ba2c91f017a3749571a82f2c6d890ac7ffb2fb.asset/AssetData/PingFang.ttc"
OUTPUT = "/Users/kaku/WorkBuddy/20260407113700/workbuddy_poster_style2.png"

W, H = 900, 1200

BG_DARK  = (6, 8, 18)
BG_MID   = (10, 14, 30)
NAVY_MID = (14, 22, 52)
NEON_G   = (0, 255, 180)
NEON_B   = (80, 180, 255)
NEON_DIM = (0, 110, 85)
DIM_BLUE = (28, 65, 120)
GRID_C   = (14, 24, 56)
WHITE    = (240, 244, 255)
GRAY_DIM = (55, 72, 108)

img = Image.new("RGB", (W, H), BG_DARK)
draw = ImageDraw.Draw(img)

def ef(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
def cf(size, index=0):
    return ImageFont.truetype(PINGFANG, size, index=index)

f_title  = ef("Tektur-Medium.ttf",          56)
f_sub    = cf(20, index=3)
f_mono   = ef("JetBrainsMono-Regular.ttf",  11)
f_mono_b = ef("JetBrainsMono-Bold.ttf",     12)
f_body   = cf(15)
f_body_b = cf(15, index=3)
f_label  = ef("IBMPlexMono-Bold.ttf",       10)
f_cta    = cf(22, index=3)
f_num    = ef("BigShoulders-Bold.ttf",      74)
f_tag    = cf(13)
f_huge   = ef("BigShoulders-Bold.ttf",     200)

# ── Background grid ────────────────────────────────────────────────────────
for y in range(0, H, 40):
    draw.line([(0, y), (W, y)], fill=GRID_C, width=1)
for x in range(0, W, 40):
    draw.line([(x, 0), (x, H)], fill=GRID_C, width=1)

# ── Ghost "AI" ────────────────────────────────────────────────────────────
ghost = (12, 20, 46)
draw.text((W//2, H//2 - 20), "AI", font=f_huge, fill=ghost, anchor="mm")

# ── Top circuit band ─────────────────────────────────────────────────────
draw.rectangle([0, 0, W, 190], fill=BG_MID)
for y, color, w in [(30, DIM_BLUE, 1), (46, NEON_DIM, 1), (62, DIM_BLUE, 1),
                     (78, NEON_G, 2), (94, DIM_BLUE, 1)]:
    draw.line([(60, y), (W-60, y)], fill=color, width=w)
    for x in range(120, W-60, 80):
        r = 3 if color == NEON_G else 2
        draw.ellipse([x-r, y-r, x+r, y+r], fill=color)

# ── Left column ──────────────────────────────────────────────────────────
draw.rectangle([0, 0, 54, H], fill=BG_MID)
draw.line([(26, 0), (26, H)], fill=NEON_DIM, width=2)
draw.line([(38, 0), (38, H)], fill=DIM_BLUE, width=1)
for y in range(100, H-100, 60):
    draw.ellipse([23, y-3, 29, y+3], fill=NEON_G)

# Right neon strip
draw.rectangle([W-4, 0, W, H], fill=NEON_G)

# ── Top header ────────────────────────────────────────────────────────────
draw.text((74, 16), "SYS:WORKBUDDY", font=f_mono_b, fill=NEON_G)
draw.text((74, 32), "BUILD:2026.01.19  STATUS:ACTIVE  USERS:15000+", font=f_mono, fill=GRAY_DIM)
draw.text((W-64, 16), "● ONLINE", font=f_mono_b, fill=NEON_G, anchor="ra")
draw.text((W-64, 32), "TENCENT AI", font=f_mono, fill=GRAY_DIM, anchor="ra")

# ── Main title ────────────────────────────────────────────────────────────
draw.text((74, 196), "WORK", font=f_title, fill=WHITE)
ww = draw.textlength("WORK", font=f_title)
draw.text((74 + ww + 8, 196), "BUDDY", font=f_title, fill=NEON_G)

# Subtitle
draw.text((74, 262), "全场景职场 AI 智能体  ·  桌面工作台", font=f_sub, fill=NEON_B)

# Underline
draw.rectangle([74, 294, 74+480, 295], fill=NEON_DIM)

# Taglines
draw.text((74, 306), ">  听懂自然语言", font=f_mono_b, fill=NEON_G)
draw.text((74+230, 306), ">  带脑子思考", font=f_mono_b, fill=NEON_G)
draw.text((74+450, 306), ">  真能操作本地文件", font=f_mono_b, fill=NEON_G)

# ── Feature grid ─────────────────────────────────────────────────────────
gy = 340
cw = (W - 108 - 30) // 3
feats = [
    ("/EXECUTE", "AGENT", "自动规划·执行\n复杂多步骤任务"),
    ("/CREATE",  "OUTPUT","生成文档/PPT\n表格·深度分析"),
    ("/DELIVER", "RESULT","交付可验收成果\n像真正的 AI 同事"),
]
for i, (cmd, tag, desc) in enumerate(feats):
    cx = 74 + i * (cw + 15)
    draw.rectangle([cx, gy, cx+cw, gy+122], fill=NAVY_MID)
    draw.rectangle([cx, gy, cx+cw, gy+2], fill=NEON_G)
    draw.text((cx+10, gy+10), cmd, font=f_mono_b, fill=NEON_G)
    draw.text((cx+10, gy+28), tag, font=f_label, fill=GRAY_DIM)
    draw.rectangle([cx+10, gy+44, cx+cw-10, gy+45], fill=DIM_BLUE)
    for j, line in enumerate(desc.split("\n")):
        draw.text((cx+10, gy+54+j*24), line, font=f_body, fill=WHITE)

# ── Problem panel ─────────────────────────────────────────────────────────
py = gy + 140
draw.rectangle([74, py, W-54, py+138], fill=BG_MID)
draw.rectangle([74, py, 76, py+138], fill=NEON_G)
draw.text((90, py+12), "PROBLEM.STATEMENT:", font=f_mono_b, fill=GRAY_DIM)
lines = [
    "腾讯内 85% 非技术用户被 AI 工具高门槛挡在门外",
    "不懂编程、IDE、专业知识  →  望而却步",
    "WorkBuddy 正是在此背景下诞生",
]
for j, line in enumerate(lines):
    c = NEON_G if j == 2 else WHITE
    draw.text((90, py+34+j*28), line, font=f_body_b if j==2 else f_body, fill=c)

# ── Diff analysis ────────────────────────────────────────────────────────
dy2 = py + 158
draw.text((74, dy2), "DIFF.ANALYSIS:", font=f_mono_b, fill=GRAY_DIM)
dy2 += 22
diffs_data = [
    ("ChatGPT / Claude", "仅对话·建议", "WorkBuddy", "直接执行·交付"),
    ("需要专业操作",     "高门槛学习成本", "一句话描述", "零门槛上手"),
]
for left_l, left_v, right_l, right_v in diffs_data:
    # Draw label in mono (ASCII only)
    prefix = "[ "
    draw.text((74, dy2), prefix, font=f_mono, fill=GRAY_DIM)
    px2 = 74 + int(draw.textlength(prefix, font=f_mono))
    draw.text((px2, dy2), left_l, font=f_tag, fill=GRAY_DIM)
    px2 += int(draw.textlength(left_l, font=f_tag))
    draw.text((px2, dy2), ": ", font=f_mono, fill=GRAY_DIM)
    px2 += int(draw.textlength(": ", font=f_mono))
    draw.text((px2, dy2), left_v, font=f_tag, fill=GRAY_DIM)
    px2 += int(draw.textlength(left_v, font=f_tag))
    draw.text((px2, dy2), " ]", font=f_mono, fill=GRAY_DIM)
    px2 += int(draw.textlength(" ]", font=f_mono)) + 8
    draw.text((px2, dy2), "->", font=f_mono_b, fill=NEON_G)
    px2 += int(draw.textlength("->", font=f_mono_b)) + 8
    draw.text((px2, dy2), "[ ", font=f_mono, fill=NEON_G)
    px2 += int(draw.textlength("[ ", font=f_mono))
    draw.text((px2, dy2), right_l, font=f_tag, fill=NEON_G)
    px2 += int(draw.textlength(right_l, font=f_tag))
    draw.text((px2, dy2), ": ", font=f_mono, fill=NEON_G)
    px2 += int(draw.textlength(": ", font=f_mono))
    draw.text((px2, dy2), right_v, font=f_tag, fill=NEON_G)
    px2 += int(draw.textlength(right_v, font=f_tag))
    draw.text((px2, dy2), " ]", font=f_mono, fill=NEON_G)
    dy2 += 24

# ── Stats blocks ─────────────────────────────────────────────────────────
sy = dy2 + 30
draw.rectangle([74, sy, 310, sy+90], fill=NAVY_MID)
draw.rectangle([74, sy, 76, sy+90], fill=NEON_G)
draw.text((92, sy+6), "15,000+", font=f_num, fill=NEON_G)
draw.text((92, sy+72), "TENCENT INTERNAL BETA USERS", font=f_label, fill=GRAY_DIM)

draw.rectangle([328, sy, 600, sy+90], fill=NAVY_MID)
draw.rectangle([328, sy, 330, sy+90], fill=NEON_B)
draw.text((346, sy+6), "2026.01", font=f_num, fill=NEON_B)
draw.text((346, sy+72), "INTERNAL LAUNCH DATE", font=f_label, fill=GRAY_DIM)

# ── Capability tags ──────────────────────────────────────────────────────
tag_y = sy + 108
tags = ["批量处理文件", "多模态创作", "深度分析", "行业调研", "Agent并行", "MCP Skills", "内置多模型"]
tx = 74
for t in tags:
    tw = int(draw.textlength(t, font=f_tag)) + 16
    draw.rectangle([tx, tag_y, tx+tw, tag_y+22], outline=NEON_DIM, width=1)
    draw.text((tx+tw//2, tag_y+11), t, font=f_tag, fill=NEON_G, anchor="mm")
    tx += tw + 8

# ── Bottom circuit band ──────────────────────────────────────────────────
draw.rectangle([0, H-180, W, H], fill=BG_MID)
for y, color, w in [(H-30, DIM_BLUE, 1), (H-46, NEON_DIM, 1),
                     (H-62, DIM_BLUE, 1), (H-78, NEON_G, 2), (H-94, DIM_BLUE, 1)]:
    draw.line([(60, y), (W-60, y)], fill=color, width=w)
    for x in range(120, W-60, 80):
        r = 3 if color == NEON_G else 2
        draw.ellipse([x-r, y-r, x+r, y+r], fill=color)

# ── CTA button ───────────────────────────────────────────────────────────
cta_y = H - 162
draw.rectangle([74, cta_y, W-54, cta_y+50], fill=NEON_G)
cta_text = "内测开放中  ·  欢迎参与体验"
tw2 = draw.textlength(cta_text, font=f_cta)
draw.text((74 + (W-128-int(tw2))//2, cta_y+13), cta_text, font=f_cta, fill=BG_DARK)

# Footer
draw.text((74, H - 104), "workbuddy.tencent.com", font=f_mono, fill=GRAY_DIM)
draw.text((74, H - 88), "Powered by Tencent  ·  Built for Everyone", font=f_mono, fill=GRAY_DIM)
draw.text((W-64, H - 88), "v2026", font=f_mono, fill=NEON_DIM, anchor="ra")

img.save(OUTPUT, "PNG", dpi=(150, 150))
print(f"Saved: {OUTPUT}")
