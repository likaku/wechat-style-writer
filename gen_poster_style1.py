#!/usr/bin/env python3
"""
WorkBuddy Poster - Style 1: Chromatic Silence (极简主义·科技冷感)
3:4 ratio poster, 900x1200px
"""
from PIL import Image, ImageDraw, ImageFont
import os

FONT_DIR = "/Users/kaku/.workbuddy/skills/canvas-design/canvas-fonts"
OUTPUT = "/Users/kaku/WorkBuddy/20260407113700/workbuddy_poster_style1.png"

W, H = 900, 1200

# Color palette
BG = (248, 248, 246)        # near-white warm paper
NAVY = (8, 18, 42)          # deep navy
TEAL = (0, 178, 180)        # electric teal accent
GRAY_LIGHT = (200, 205, 210)
GRAY_MED = (130, 138, 148)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# ── Load fonts ───────────────────────────────────────────────────────────────
def font(name, size):
    path = os.path.join(FONT_DIR, name)
    return ImageFont.truetype(path, size)

f_title    = font("BricolageGrotesque-Bold.ttf",   96)
f_sub      = font("BricolageGrotesque-Regular.ttf", 22)
f_tag      = font("Jura-Light.ttf",                 14)
f_label    = font("Jura-Medium.ttf",                16)
f_body     = font("InstrumentSans-Regular.ttf",     17)
f_body_b   = font("InstrumentSans-Bold.ttf",        17)
f_mono     = font("JetBrainsMono-Regular.ttf",      12)
f_mono_b   = font("JetBrainsMono-Bold.ttf",         13)
f_large_num= font("BigShoulders-Bold.ttf",          200)
f_cta      = font("InstrumentSans-Bold.ttf",        18)

# ── Background structural elements ──────────────────────────────────────────
# Top horizontal rule (full width, navy, 2px)
draw.rectangle([0, 80, W, 82], fill=NAVY)

# Bottom horizontal rule
draw.rectangle([0, H-80, W, H-78], fill=NAVY)

# Thin teal accent vertical strip (far right edge)
draw.rectangle([W-4, 0, W, H], fill=TEAL)

# ── Large ghost number – visual texture ─────────────────────────────────────
# "15K" as ghosted element (大字背景纹理)
ghost_color = (220, 222, 220)
draw.text((W//2-140, H//2-60), "AI", font=f_large_num, fill=ghost_color, anchor="mm")

# ── Top section: system label + tag line ────────────────────────────────────
# System tag
draw.text((54, 52), "TENCENT WORKBUDDY  ·  v2026", font=f_mono, fill=GRAY_MED)

# ── Main title block ─────────────────────────────────────────────────────────
# "Work" in navy, "Buddy" with teal dot
title_y = 108
draw.text((54, title_y), "Work", font=f_title, fill=NAVY)
title_w = draw.textlength("Work", font=f_title)
draw.text((54 + title_w, title_y), "Buddy", font=f_title, fill=TEAL)

# Subtitle line under title
sub_y = title_y + 106
draw.text((54, sub_y), "全场景职场 AI 智能体桌面工作台", font=f_sub, fill=NAVY)

# Thin separator under subtitle
sep_y = sub_y + 36
draw.rectangle([54, sep_y, W-54, sep_y+1], fill=GRAY_LIGHT)

# ── Core identity statement ──────────────────────────────────────────────────
id_y = sep_y + 26
taglines = [
    "听懂自然语言  ·  带脑子思考  ·  真能操作本地文件",
]
for t in taglines:
    draw.text((54, id_y), t, font=f_label, fill=GRAY_MED)
    id_y += 26

# ── Three-column feature grid ─────────────────────────────────────────────────
grid_y = id_y + 42
cols = [
    ("EXECUTE", "自动规划并执行\n复杂多步骤任务"),
    ("CREATE", "生成文档 / PPT\n表格 · 深度分析"),
    ("DELIVER", "交付可验收结果\n像真正的同事"),
]
col_w = (W - 108) // 3
for i, (label, desc) in enumerate(cols):
    cx = 54 + i * col_w
    # Column header
    draw.text((cx, grid_y), label, font=f_mono_b, fill=TEAL)
    # Thin rule under label
    draw.rectangle([cx, grid_y+22, cx+col_w-16, grid_y+23], fill=TEAL)
    # Description
    for j, line in enumerate(desc.split("\n")):
        draw.text((cx, grid_y + 34 + j * 24), line, font=f_body, fill=NAVY)

# ── Divider rule ─────────────────────────────────────────────────────────────
div_y = grid_y + 110
draw.rectangle([54, div_y, W-54, div_y+1], fill=GRAY_LIGHT)

# ── Problem / solution statement ─────────────────────────────────────────────
ps_y = div_y + 28

# Side label
draw.text((54, ps_y), "WHY WORKBUDDY", font=f_mono, fill=GRAY_MED)

ps_y += 26

statement_lines = [
    "腾讯内部 85% 非技术用户",
    "被 AI 工具的高门槛挡在门外——",
    "WorkBuddy 为他们而生。",
]
for line in statement_lines:
    draw.text((54, ps_y), line, font=f_body_b, fill=NAVY)
    ps_y += 28

# ── Data proof line ───────────────────────────────────────────────────────────
ps_y += 16
proof_parts = [
    ("15,000+", True),
    ("  腾讯内测用户  ", False),
    ("·  ", False),
    ("自 2026.01.19 起运营", False),
]
x = 54
for text, bold in proof_parts:
    f = f_body_b if bold else f_body
    color = TEAL if bold else GRAY_MED
    draw.text((x, ps_y), text, font=f, fill=color)
    x += draw.textlength(text, font=f)

# ── Differentiator block ──────────────────────────────────────────────────────
diff_y = ps_y + 52
draw.rectangle([54, diff_y, W-54, diff_y+1], fill=GRAY_LIGHT)
diff_y += 24

draw.text((54, diff_y), "VS CHATGPT / CLAUDE", font=f_mono, fill=GRAY_MED)
diff_y += 26

diffs = [
    ("对话机器人", "职场 AI 同事"),
    ("只能建议", "真正执行任务"),
    ("需要专业操作", "一句话描述需求"),
]
for left, right in diffs:
    draw.text((54, diff_y), left, font=f_body, fill=GRAY_MED)
    arrow_x = 54 + 180
    draw.text((arrow_x, diff_y), "→", font=f_body, fill=TEAL)
    draw.text((arrow_x + 30, diff_y), right, font=f_body_b, fill=NAVY)
    diff_y += 27

# ── Bottom CTA section ────────────────────────────────────────────────────────
cta_y = H - 148
draw.rectangle([54, cta_y, W-54, cta_y+1], fill=NAVY)
cta_y += 20

draw.text((54, cta_y), "内测开放中  ·  欢迎体验", font=f_cta, fill=NAVY)

# Small mono tag bottom right
draw.text((W-54, H-52), "workbuddy.tencent.com", font=f_mono, fill=GRAY_MED, anchor="ra")
draw.text((W-54, H-34), "AI ASSISTANT  ·  DESKTOP  ·  2026", font=f_mono, fill=GRAY_LIGHT, anchor="ra")

# Bottom left
draw.text((54, H-52), "全角色  ·  全场景  ·  全能力", font=f_mono, fill=NAVY)
draw.text((54, H-34), "Powered by Tencent", font=f_mono, fill=GRAY_MED)

# ── Teal accent bottom bar ────────────────────────────────────────────────────
draw.rectangle([0, H-6, W, H], fill=TEAL)

# ── Save ─────────────────────────────────────────────────────────────────────
img.save(OUTPUT, "PNG", dpi=(150, 150))
print(f"Saved: {OUTPUT}")
