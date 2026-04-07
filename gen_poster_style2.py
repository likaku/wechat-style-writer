#!/usr/bin/env python3
"""
WorkBuddy Poster - Style 2: Neon Archaeology (赛博朋克·数字律动)
3:4 ratio poster, 900x1200px
"""
from PIL import Image, ImageDraw, ImageFont
import os
import math

FONT_DIR = "/Users/kaku/.workbuddy/skills/canvas-design/canvas-fonts"
OUTPUT = "/Users/kaku/WorkBuddy/20260407113700/workbuddy_poster_style2.png"

W, H = 900, 1200

# Color palette — dark field, neon signals
BG_DARK  = (6, 8, 18)          # near-black space
BG_MID   = (10, 14, 30)        # panel dark
NAVY_MID = (14, 22, 52)        # mid-layer
NEON_G   = (0, 255, 180)       # plasma green-teal
NEON_B   = (80, 180, 255)      # electric blue
NEON_DIM = (0, 120, 90)        # dim neon
DIM_BLUE = (30, 70, 130)       # dim blue
GRID_C   = (18, 28, 60)        # grid lines
WHITE    = (245, 248, 255)
GRAY_DIM = (60, 75, 110)

img = Image.new("RGB", (W, H), BG_DARK)
draw = ImageDraw.Draw(img)

# ── Load fonts ─────────────────────────────────────────────────────────────
def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

f_huge   = font("BigShoulders-Bold.ttf",    160)
f_title  = font("Tektur-Medium.ttf",         52)
f_sub    = font("Tektur-Regular.ttf",         18)
f_mono   = font("JetBrainsMono-Regular.ttf",  12)
f_mono_b = font("JetBrainsMono-Bold.ttf",     13)
f_body   = font("GeistMono-Regular.ttf",      14)
f_body_b = font("GeistMono-Bold.ttf",         15)
f_label  = font("IBMPlexMono-Bold.ttf",       11)
f_cta    = font("Tektur-Medium.ttf",          22)
f_num    = font("BigShoulders-Bold.ttf",      72)

# ── Background grid overlay ───────────────────────────────────────────────
# Horizontal grid lines
for y in range(0, H, 40):
    draw.line([(0, y), (W, y)], fill=GRID_C, width=1)
# Vertical grid lines
for x in range(0, W, 40):
    draw.line([(x, 0), (x, H)], fill=GRID_C, width=1)

# ── Circuit trace lines (decorative horizontal) ───────────────────────────
# Top circuit band
draw.rectangle([0, 0, W, 180], fill=BG_MID)
# circuit traces in top band
for i, (y, color, w) in enumerate([
    (30, DIM_BLUE, 1), (44, NEON_DIM, 1), (58, DIM_BLUE, 1),
    (72, NEON_G, 2), (86, DIM_BLUE, 1),
]):
    draw.line([(60, y), (W-60, y)], fill=color, width=w)
    # small node dots
    for x in range(120, W-60, 80):
        r = 3 if color == NEON_G else 2
        draw.ellipse([x-r, y-r, x+r, y+r], fill=color)

# Bottom circuit band
draw.rectangle([0, H-160, W, H], fill=BG_MID)
for i, (y, color, w) in enumerate([
    (H-30, DIM_BLUE, 1), (H-44, NEON_DIM, 1), (H-58, DIM_BLUE, 1),
    (H-72, NEON_G, 2), (H-86, DIM_BLUE, 1),
]):
    draw.line([(60, y), (W-60, y)], fill=color, width=w)
    for x in range(120, W-60, 80):
        r = 3 if color == NEON_G else 2
        draw.ellipse([x-r, y-r, x+r, y+r], fill=color)

# ── Left vertical circuit column ─────────────────────────────────────────
draw.rectangle([0, 0, 54, H], fill=BG_MID)
# vertical trace
draw.line([(26, 0), (26, H)], fill=NEON_DIM, width=2)
draw.line([(36, 0), (36, H)], fill=DIM_BLUE, width=1)
# node dots on vertical trace
for y in range(100, H-100, 60):
    draw.ellipse([23, y-3, 29, y+3], fill=NEON_G)

# Right vertical strip
draw.rectangle([W-4, 0, W, H], fill=NEON_G)

# ── System header text ────────────────────────────────────────────────────
draw.text((74, 14), "SYS:WORKBUDDY", font=f_mono_b, fill=NEON_G)
draw.text((74, 30), "BUILD:2026.01.19  STATUS:ACTIVE  USERS:15000+", font=f_mono, fill=GRAY_DIM)

# Right side status
status_x = W - 64
draw.text((status_x, 14), "● ONLINE", font=f_mono_b, fill=NEON_G, anchor="ra")
draw.text((status_x, 30), "TENCENT AI", font=f_mono, fill=GRAY_DIM, anchor="ra")

# ── Ghost huge "AI" in background ────────────────────────────────────────
ghost = (12, 22, 50)
draw.text((W//2, H//2 - 60), "AI", font=f_huge, fill=ghost, anchor="mm")

# ── Main title ────────────────────────────────────────────────────────────
title_y = 188
# "WORK" in white
draw.text((74, title_y), "WORK", font=f_title, fill=WHITE)
w1 = draw.textlength("WORK", font=f_title)
# "BUDDY" in neon
draw.text((74 + w1 + 8, title_y), "BUDDY", font=f_title, fill=NEON_G)

# Subtitle
sub_y = title_y + 64
draw.text((74, sub_y), "全场景职场 AI 智能体 · 桌面工作台", font=f_sub, fill=NEON_B)

# Glowing underline
ul_y = sub_y + 30
draw.rectangle([74, ul_y, 74+480, ul_y+1], fill=NEON_DIM)
draw.rectangle([74, ul_y+2, 74+480, ul_y+3], fill=GRID_C)

# ── Core tagline ──────────────────────────────────────────────────────────
tag_y = ul_y + 24
draw.text((74, tag_y), "> 听懂自然语言  >  带脑子思考  >  真能操作本地文件", font=f_mono_b, fill=NEON_G)

# ── Feature grid — 3 columns ──────────────────────────────────────────────
grid_y = tag_y + 52
cell_w = (W - 108 - 30) // 3
features = [
    ("EXECUTE", "AGENT", "自动规划·执行\n复杂多步骤任务"),
    ("CREATE", "OUTPUT", "生成文档/PPT\n表格·深度分析"),
    ("DELIVER", "RESULT", "交付可验收成果\n像真正的 AI 同事"),
]
for i, (cmd, tag, desc) in enumerate(features):
    cx = 74 + i * (cell_w + 15)
    # Cell background
    draw.rectangle([cx, grid_y, cx+cell_w, grid_y+120], fill=NAVY_MID)
    # Neon top border
    draw.rectangle([cx, grid_y, cx+cell_w, grid_y+2], fill=NEON_G)
    # Command label
    draw.text((cx+10, grid_y+10), f"/{cmd}", font=f_mono_b, fill=NEON_G)
    draw.text((cx+10, grid_y+28), tag, font=f_label, fill=GRAY_DIM)
    # Separator
    draw.rectangle([cx+10, grid_y+44, cx+cell_w-10, grid_y+45], fill=DIM_BLUE)
    # Description
    for j, line in enumerate(desc.split("\n")):
        draw.text((cx+10, grid_y+54+j*22), line, font=f_body, fill=WHITE)

# ── Problem definition panel ──────────────────────────────────────────────
prob_y = grid_y + 138
draw.rectangle([74, prob_y, W-54, prob_y+130], fill=BG_MID)
draw.rectangle([74, prob_y, 76, prob_y+130], fill=NEON_G)  # left accent bar

draw.text((88, prob_y+12), "PROBLEM.STATEMENT:", font=f_mono_b, fill=GRAY_DIM)

problem_lines = [
    "腾讯内 85% 非技术用户被 AI 工具高门槛挡在门外",
    "不懂编程、IDE、专业知识 → 望而却步",
    "WorkBuddy 正是在此背景下诞生",
]
for j, line in enumerate(problem_lines):
    draw.text((88, prob_y+32+j*26), f"  {line}", font=f_body, fill=WHITE if j < 2 else NEON_G)

# ── Differentiator ────────────────────────────────────────────────────────
diff_y = prob_y + 150
draw.text((74, diff_y), "DIFF.ANALYSIS:", font=f_mono_b, fill=GRAY_DIM)
diff_y += 22
diffs = [
    ("ChatGPT / Claude", "只能对话·建议", "WorkBuddy", "直接执行·交付"),
    ("需要专业操作",      "高门槛学习成本", "一句话描述", "零门槛上手"),
]
for left_label, left_val, right_label, right_val in diffs:
    draw.text((74, diff_y), f"[ {left_label}: {left_val} ]", font=f_mono, fill=GRAY_DIM)
    arrow_x = 74 + draw.textlength(f"[ {left_label}: {left_val} ]", font=f_mono) + 10
    draw.text((arrow_x, diff_y), "→", font=f_mono_b, fill=NEON_G)
    draw.text((arrow_x+22, diff_y), f"[ {right_label}: {right_val} ]", font=f_mono_b, fill=NEON_G)
    diff_y += 24

# ── Statistics highlight ──────────────────────────────────────────────────
stat_y = diff_y + 32
# Big number block
draw.rectangle([74, stat_y, 320, stat_y+90], fill=NAVY_MID)
draw.rectangle([74, stat_y, 76, stat_y+90], fill=NEON_G)
draw.text((90, stat_y+8), "15,000+", font=f_num, fill=NEON_G)
draw.text((90, stat_y+72), "TENCENT INTERNAL BETA USERS", font=f_label, fill=GRAY_DIM)

# Side stat
draw.rectangle([336, stat_y, 600, stat_y+90], fill=NAVY_MID)
draw.rectangle([336, stat_y, 338, stat_y+90], fill=NEON_B)
draw.text((352, stat_y+8), "2026.01", font=f_num, fill=NEON_B)
draw.text((352, stat_y+72), "INTERNAL LAUNCH DATE", font=f_label, fill=GRAY_DIM)

# ── CTA bottom ────────────────────────────────────────────────────────────
cta_y = H - 144
draw.rectangle([74, cta_y, W-54, cta_y+50], fill=NEON_G)
cta_text = "内测开放中  ·  欢迎参与体验"
tw = draw.textlength(cta_text, font=f_cta)
draw.text((74 + (W-128-tw)//2, cta_y+14), cta_text, font=f_cta, fill=BG_DARK)

# Bottom labels
draw.text((74, H-78), "workbuddy.tencent.com", font=f_mono, fill=GRAY_DIM)
draw.text((74, H-60), "Powered by Tencent  ·  Built for Everyone", font=f_mono, fill=GRAY_DIM)
draw.text((W-64, H-60), "v2026", font=f_mono, fill=NEON_DIM, anchor="ra")

img.save(OUTPUT, "PNG", dpi=(150, 150))
print(f"Saved: {OUTPUT}")
