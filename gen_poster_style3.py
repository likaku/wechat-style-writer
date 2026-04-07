#!/usr/bin/env python3
"""
WorkBuddy Poster - Style 3: Warm Systems (有机系统·温暖协作)
3:4 ratio poster, 900x1200px
"""
from PIL import Image, ImageDraw, ImageFont
import os
import math

FONT_DIR = "/Users/kaku/.workbuddy/skills/canvas-design/canvas-fonts"
OUTPUT = "/Users/kaku/WorkBuddy/20260407113700/workbuddy_poster_style3.png"

W, H = 900, 1200

# Warm editorial palette
IVORY    = (252, 248, 240)      # warm background
AMBER    = (220, 140, 40)       # warm amber accent
PLUM     = (72, 30, 58)         # deep plum (main text)
TERRA    = (188, 80, 46)        # terracotta
SAGE     = (88, 126, 100)       # sage green
CREAM    = (244, 236, 218)      # cream panel
SAND     = (230, 210, 180)      # sandy divider
TAN_DIM  = (180, 155, 120)      # dim tan
PLUM_LT  = (140, 90, 120)       # light plum

img = Image.new("RGB", (W, H), IVORY)
draw = ImageDraw.Draw(img)

# ── Load fonts ─────────────────────────────────────────────────────────────
def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

f_serif_h  = font("YoungSerif-Regular.ttf",        88)
f_serif_m  = font("YoungSerif-Regular.ttf",         32)
f_serif_s  = font("YoungSerif-Regular.ttf",         20)
f_sans     = font("InstrumentSans-Regular.ttf",     16)
f_sans_b   = font("InstrumentSans-Bold.ttf",        16)
f_sans_it  = font("InstrumentSans-Italic.ttf",      15)
f_label    = font("InstrumentSans-Bold.ttf",        11)
f_script   = font("Italiana-Regular.ttf",           28)
f_crim     = font("CrimsonPro-Regular.ttf",         18)
f_crim_b   = font("CrimsonPro-Bold.ttf",            19)
f_crim_i   = font("CrimsonPro-Italic.ttf",          18)
f_big_num  = font("Lora-Bold.ttf",                  96)
f_cta      = font("InstrumentSans-Bold.ttf",        20)

# ── Large amber top bar ───────────────────────────────────────────────────
draw.rectangle([0, 0, W, 10], fill=AMBER)

# ── Warm header band ─────────────────────────────────────────────────────
draw.rectangle([0, 10, W, 90], fill=CREAM)
# Thin bottom rule of header
draw.rectangle([0, 90, W, 92], fill=SAND)

# Header content
draw.text((54, 30), "TENCENT  ·  WORKBUDDY  ·  2026", font=f_label, fill=TAN_DIM)
draw.text((W-54, 30), "腾讯内测版", font=f_label, fill=AMBER, anchor="ra")
draw.text((W-54, 48), "Beta Open", font=f_label, fill=TAN_DIM, anchor="ra")

# ── Main title area ───────────────────────────────────────────────────────
title_y = 108
# Large serif title
draw.text((54, title_y), "Work", font=f_serif_h, fill=PLUM)
w1 = draw.textlength("Work", font=f_serif_h)
draw.text((54 + w1, title_y), "Buddy", font=f_serif_h, fill=AMBER)

# Elegant italic subtitle
sub_y = title_y + 98
draw.text((54, sub_y), "你的全场景 AI 职场同事", font=f_script, fill=PLUM_LT)

# Thin amber rule
rul_y = sub_y + 40
draw.rectangle([54, rul_y, W-54, rul_y+2], fill=AMBER)
draw.rectangle([54, rul_y+4, 200, rul_y+5], fill=SAND)

# ── Three organic feature circles ────────────────────────────────────────
circ_y = rul_y + 36
circ_r = 52
circ_centers = [
    (54 + circ_r, circ_y + circ_r),
    (54 + circ_r*2 + 14 + circ_r + 14 + circ_r, circ_y + circ_r),  # placeholder
    (54 + circ_r*2 + 14 + circ_r, circ_y + circ_r),
]
# Recalculate evenly
spacing = (W - 108 - circ_r*2*3) // 2
c1x = 54 + circ_r
c2x = 54 + circ_r*2 + spacing + circ_r
c3x = 54 + circ_r*2 + spacing*2 + circ_r*2 + spacing - spacing//2 + circ_r
# simpler: 3 evenly
cx_list = [54 + (W-108)//6, 54 + (W-108)//2, 54 + 5*(W-108)//6]
cy = circ_y + circ_r

circles = [
    (PLUM, "执行任务", "自动规划\n复杂多步"),
    (TERRA, "内容创作", "文档/PPT\n报告表格"),
    (SAGE, "深度分析", "数据洞察\n行业调研"),
]
for cx, (color, label, desc) in zip(cx_list, circles):
    # Outer ring
    draw.ellipse([cx-circ_r, cy-circ_r, cx+circ_r, cy+circ_r], fill=color)
    # Inner text
    draw.text((cx, cy-14), label, font=f_label, fill=IVORY, anchor="mm")
    for j, line in enumerate(desc.split("\n")):
        draw.text((cx, cy+6+j*16), line, font=f_label, fill=IVORY, anchor="mm")

# Connecting lines between circles
for i in range(len(cx_list)-1):
    x1 = cx_list[i] + circ_r + 4
    x2 = cx_list[i+1] - circ_r - 4
    draw.line([(x1, cy), (x2, cy)], fill=SAND, width=2)

# ── Tagline block ────────────────────────────────────────────────────────
tag_y = circ_y + circ_r*2 + 28
draw.text((54, tag_y), "听懂自然语言  ·  带脑子思考  ·  真能操作本地文件", font=f_sans_b, fill=PLUM)
tag_y += 26
draw.text((54, tag_y), "一句话描述需求 → 自主规划并执行 → 交付可验收结果", font=f_crim_i, fill=PLUM_LT)

# ── Warm cream problem block ─────────────────────────────────────────────
pb_y = tag_y + 42
draw.rectangle([54, pb_y, W-54, pb_y+148], fill=CREAM)
draw.rectangle([54, pb_y, 58, pb_y+148], fill=AMBER)   # left amber bar

draw.text((72, pb_y+16), "为什么需要 WorkBuddy ?", font=f_serif_s, fill=PLUM)
draw.rectangle([72, pb_y+44, W-70, pb_y+45], fill=SAND)

prob_lines = [
    "腾讯内 85% 非技术用户被高门槛 AI 工具拒之门外——",
    "不懂编程语言、IDE 开发环境与计算机专业知识，",
    "但他们同样有强烈的办公场景 AI 提效需求。",
    "WorkBuddy 正是为此而生：零门槛，真能干活。",
]
for j, line in enumerate(prob_lines):
    clr = PLUM if j < 3 else AMBER
    f   = f_crim if j < 3 else f_crim_b
    draw.text((72, pb_y+54+j*22), line, font=f, fill=clr)

# ── Differentiator strip ─────────────────────────────────────────────────
diff_y = pb_y + 166
draw.rectangle([0, diff_y, W, diff_y+44], fill=PLUM)
diff_text = "\u4e0d\u540c\u4e8e ChatGPT \u7b49\u804a\u5929\u673a\u5668\u4eba\u53ea\u80fd\u300c\u5bf9\u8bdd\u300d\uff0cWorkBuddy \u662f\u771f\u6b63\u6267\u884c\u4efb\u52a1\u7684 AI \u540c\u4e8b"
draw.text((W//2, diff_y+22), diff_text, font=f_sans, fill=IVORY, anchor="mm")

# ── Statistics section ────────────────────────────────────────────────────
stat_y = diff_y + 60
# Left: big number
draw.text((54, stat_y), "15,000", font=f_big_num, fill=AMBER)
plus_x = 54 + draw.textlength("15,000", font=f_big_num)
draw.text((plus_x+4, stat_y+8), "+", font=f_serif_m, fill=TERRA)
draw.text((54, stat_y+90), "腾讯内部 Beta 用户，一致好评", font=f_sans, fill=PLUM_LT)

# Right: launch date badge
badge_x, badge_y = W-54-200, stat_y+14
draw.rectangle([badge_x, badge_y, badge_x+200, badge_y+72], fill=CREAM)
draw.rectangle([badge_x, badge_y, badge_x+4, badge_y+72], fill=TERRA)
draw.text((badge_x+14, badge_y+10), "发布日期", font=f_label, fill=TAN_DIM)
draw.text((badge_x+14, badge_y+28), "2026.01.19", font=f_sans_b, fill=PLUM)
draw.text((badge_x+14, badge_y+50), "腾讯内部上线", font=f_label, fill=TAN_DIM)

# ── Features text list ────────────────────────────────────────────────────
feat_y = stat_y + 122
draw.rectangle([54, feat_y, W-54, feat_y+1], fill=SAND)
feat_y += 18

draw.text((54, feat_y), "核心能力", font=f_serif_s, fill=PLUM)
feat_y += 32

features = [
    ("✦ 自动批量处理文件", PLUM),
    ("✦ 生成文档 / 表格 / PPT", TERRA),
    ("✦ 多模态内容创作", SAGE),
    ("✦ 数据深度分析与行业调研", PLUM_LT),
    ("✦ 多任务 Agent 并行处理", AMBER),
    ("✦ 内置多种模型 & 主流 MCP Skills", PLUM),
]
col_h = len(features) // 2
for i, (text, color) in enumerate(features):
    col = i % 2
    row = i // 2
    fx = 54 + col * ((W-108)//2)
    fy = feat_y + row * 26
    draw.text((fx, fy), text, font=f_crim, fill=color)

# ── Bottom CTA area ───────────────────────────────────────────────────────
cta_y = H - 130
draw.rectangle([0, cta_y, W, H], fill=PLUM)
draw.rectangle([0, cta_y, W, cta_y+2], fill=AMBER)

cta_text = "内测开放中  ·  欢迎体验"
tw = draw.textlength(cta_text, font=f_cta)
draw.text((W//2, cta_y+28), cta_text, font=f_cta, fill=IVORY, anchor="mm")

draw.text((54, cta_y+56), "workbuddy.tencent.com", font=f_sans, fill=TAN_DIM)
draw.text((54, cta_y+76), "Powered by Tencent  ·  全角色 · 全场景 · 全能力", font=f_label, fill=PLUM_LT)
draw.text((W-54, cta_y+68), "2026", font=f_sans_b, fill=AMBER, anchor="ra")

# ── Bottom amber strip ────────────────────────────────────────────────────
draw.rectangle([0, H-4, W, H], fill=AMBER)

img.save(OUTPUT, "PNG", dpi=(150, 150))
print(f"Saved: {OUTPUT}")
