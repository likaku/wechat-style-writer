#!/usr/bin/env python3
"""
WorkBuddy Poster - Style 1 REFINED: Chromatic Silence (极简主义·科技冷感)
3:4 ratio, 900x1200px — with proper CJK font support
"""
from PIL import Image, ImageDraw, ImageFont
import os

FONT_DIR = "/Users/kaku/.workbuddy/skills/canvas-design/canvas-fonts"
PINGFANG = "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/86ba2c91f017a3749571a82f2c6d890ac7ffb2fb.asset/AssetData/PingFang.ttc"
OUTPUT = "/Users/kaku/WorkBuddy/20260407113700/workbuddy_poster_style1.png"

W, H = 900, 1200

BG      = (248, 248, 246)
NAVY    = (8,  18,  42)
TEAL    = (0,  178, 180)
TEAL_DK = (0,  130, 132)
GRAY_L  = (210, 215, 218)
GRAY_M  = (130, 138, 148)
GRAY_D  = (80,  90,  105)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

def ef(name, size):  # english font
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
def cf(size, index=0):  # chinese font (PingFang)
    return ImageFont.truetype(PINGFANG, size, index=index)

# Fonts
f_title  = ef("BricolageGrotesque-Bold.ttf",     104)
f_title2 = ef("BricolageGrotesque-Bold.ttf",     104)
f_sub    = cf(22)
f_sub_b  = cf(22, index=3)   # semibold
f_tag    = cf(13)
f_label  = ef("Jura-Medium.ttf",                  13)
f_body   = cf(16)
f_body_b = cf(16, index=3)
f_mono   = ef("JetBrainsMono-Regular.ttf",        11)
f_mono_b = ef("JetBrainsMono-Bold.ttf",           12)
f_cmd    = ef("JetBrainsMono-Bold.ttf",           13)
f_num    = ef("BigShoulders-Bold.ttf",            220)
f_cta    = cf(20, index=3)

# ── Structural lines ──────────────────────────────────────────────────────────
draw.rectangle([0, 0, W, 3], fill=NAVY)          # very top
draw.rectangle([0, H-3, W, H], fill=TEAL)        # very bottom
draw.rectangle([W-5, 0, W, H], fill=TEAL)        # right edge strip

# ── Ghost "AI" texture ────────────────────────────────────────────────────────
ghost = (230, 232, 230)
draw.text((W//2, H//2 - 20), "AI", font=f_num, fill=ghost, anchor="mm")

# ── Top area ──────────────────────────────────────────────────────────────────
draw.rectangle([0, 3, W, 88], fill=BG)
draw.rectangle([0, 88, W, 90], fill=NAVY)

draw.text((54, 32), "TENCENT  WORKBUDDY", font=f_mono_b, fill=NAVY)
draw.text((54, 52), "v2026  ·  INTERNAL BETA", font=f_mono, fill=GRAY_M)
draw.text((W-58, 32), "● ACTIVE", font=f_mono_b, fill=TEAL, anchor="ra")
draw.text((W-58, 52), "15,000+ users", font=f_mono, fill=GRAY_M, anchor="ra")

# ── Main title ────────────────────────────────────────────────────────────────
ty = 98
draw.text((54, ty), "Work", font=f_title, fill=NAVY)
ww = draw.textlength("Work", font=f_title)
draw.text((54 + ww, ty), "Buddy", font=f_title2, fill=TEAL)

# ── Subtitle ──────────────────────────────────────────────────────────────────
sy = ty + 112
draw.text((54, sy), "全场景职场 AI 智能体桌面工作台", font=f_sub_b, fill=NAVY)

# tagline
ty2 = sy + 34
draw.text((54, ty2), "听懂自然语言  ·  带脑子思考  ·  真能操作本地文件", font=f_tag, fill=GRAY_M)

# thin separator
sep = ty2 + 26
draw.rectangle([54, sep, W-54, sep+1], fill=GRAY_L)

# ── Feature 3-column grid ─────────────────────────────────────────────────────
gy = sep + 32
cw = (W - 108 - 32) // 3
feats = [
    ("EXECUTE", "自动规划并执行\n复杂多步骤任务"),
    ("CREATE",  "生成文档 / PPT\n表格 · 深度分析"),
    ("DELIVER", "交付可验收结果\n像真正的 AI 同事"),
]
for i, (cmd, desc) in enumerate(feats):
    cx = 54 + i * (cw + 16)
    draw.text((cx, gy), cmd, font=f_cmd, fill=TEAL)
    draw.rectangle([cx, gy + 20, cx + cw - 8, gy + 21], fill=TEAL)
    for j, line in enumerate(desc.split("\n")):
        draw.text((cx, gy + 30 + j * 24), line, font=f_body, fill=NAVY)

# ── Separator ─────────────────────────────────────────────────────────────────
sep2 = gy + 100
draw.rectangle([54, sep2, W-54, sep2+1], fill=GRAY_L)

# ── Problem statement ─────────────────────────────────────────────────────────
py = sep2 + 26

draw.text((54, py), "WHY WORKBUDDY", font=f_label, fill=GRAY_M)
py += 24

problem = [
    ("腾讯内部 85% 非技术用户", False),
    ("被 AI 工具的高门槛挡在门外——", False),
    ("WorkBuddy 正是为此而生。", True),
]
for text, accent in problem:
    color = TEAL if accent else NAVY
    f = f_body_b if accent else f_body_b
    draw.text((54, py), text, font=f, fill=color)
    py += 28

# ── Stats row ─────────────────────────────────────────────────────────────────
py += 12
sx = 54
# 15,000+ label
draw.text((sx, py), "15,000+", font=ef("BigShoulders-Bold.ttf", 60), fill=TEAL)
tw = draw.textlength("15,000+", font=ef("BigShoulders-Bold.ttf", 60))
draw.text((sx + tw + 14, py + 14), "腾讯内部内测用户", font=f_body, fill=GRAY_M)
draw.text((sx + tw + 14, py + 38), "自 2026.01.19 起开放内测", font=f_tag, fill=GRAY_L)

# ── Separator ─────────────────────────────────────────────────────────────────
sep3 = py + 82
draw.rectangle([54, sep3, W-54, sep3+1], fill=GRAY_L)

# ── VS block ──────────────────────────────────────────────────────────────────
vsy = sep3 + 24
draw.text((54, vsy), "VS  CHATGPT  /  CLAUDE", font=f_label, fill=GRAY_M)
vsy += 24

diffs = [
    ("只能对话·建议",   "直接执行·交付结果"),
    ("需要专业操作",   "一句话描述，零门槛"),
    ("无法操作本地文件", "读取授权文件夹，自动处理"),
]
for left, right in diffs:
    draw.text((54, vsy), left, font=f_body, fill=GRAY_D)
    ax = 54 + 220
    draw.text((ax, vsy), "→", font=f_mono_b, fill=TEAL)
    draw.text((ax + 24, vsy), right, font=f_body_b, fill=NAVY)
    vsy += 28

# ── Capability pills row ────────────────────────────────────────────────────
pill_y = vsy + 24
pills = ["批量处理文件", "多模态创作", "行业调研", "Agent并行", "MCP Skills", "内置多模型"]
px = 54
for pill in pills:
    pw = int(draw.textlength(pill, font=f_tag)) + 20
    draw.rectangle([px, pill_y, px+pw, pill_y+22], outline=TEAL, width=1)
    draw.text((px + pw//2, pill_y+11), pill, font=f_tag, fill=NAVY, anchor="mm")
    px += pw + 10

# ── Full-width navy band (mission statement) ─────────────────────────────────
band_y = pill_y + 50
draw.rectangle([0, band_y, W, band_y+68], fill=NAVY)
mission = "一句话描述需求，WorkBuddy 自主规划、执行、交付——真正像同事一样工作"
draw.text((W//2, band_y+34), mission, font=cf(16, index=3), fill=TEAL, anchor="mm")

# ── Tall decorative grid section ─────────────────────────────────────────────
deco_y = band_y + 84
# Draw a grid of small teal dots – visual system diagram feel
dot_rows = 4
dot_cols = 18
dot_sp_x = (W - 108) // (dot_cols - 1)
dot_sp_y = 28
for r in range(dot_rows):
    for c in range(dot_cols):
        dx = 54 + c * dot_sp_x
        dy = deco_y + r * dot_sp_y
        dr = 2 if (r + c) % 3 == 0 else 1
        col = TEAL if (r + c) % 4 == 0 else GRAY_L
        draw.ellipse([dx-dr, dy-dr, dx+dr, dy+dr], fill=col)

# Horizontal lines through dots
for r in range(dot_rows):
    dy = deco_y + r * dot_sp_y
    draw.line([(54, dy), (W-54, dy)], fill=GRAY_L, width=1)

# ── CTA block ─────────────────────────────────────────────────────────────────
cta_y = deco_y + dot_rows * dot_sp_y + 28
draw.rectangle([54, cta_y, W-54, cta_y+1], fill=NAVY)
cta_y += 18
draw.text((54, cta_y), "内测开放中  ·  欢迎参与体验", font=f_cta, fill=NAVY)

# ── Footer (fixed to bottom) ─────────────────────────────────────────────────
foot_y = H - 60
draw.rectangle([0, foot_y - 8, W, foot_y - 7], fill=GRAY_L)
draw.text((54, foot_y - 2), "全角色  ·  全场景  ·  全能力", font=f_mono_b, fill=NAVY)
draw.text((54, foot_y + 16), "Powered by Tencent", font=f_mono, fill=GRAY_M)
draw.text((W-58, foot_y - 2), "workbuddy.tencent.com", font=f_mono, fill=GRAY_M, anchor="ra")
draw.text((W-58, foot_y + 16), "AI  ·  DESKTOP  ·  2026", font=f_mono, fill=GRAY_L, anchor="ra")

img.save(OUTPUT, "PNG", dpi=(150, 150))
print(f"Saved: {OUTPUT}")
