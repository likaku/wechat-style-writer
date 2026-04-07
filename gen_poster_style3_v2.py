#!/usr/bin/env python3
"""
WorkBuddy Poster - Style 3 REFINED: Warm Systems (有机系统·温暖协作)
3:4 ratio, 900x1200px — with proper CJK font support
"""
from PIL import Image, ImageDraw, ImageFont
import os

FONT_DIR = "/Users/kaku/.workbuddy/skills/canvas-design/canvas-fonts"
PINGFANG = "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/86ba2c91f017a3749571a82f2c6d890ac7ffb2fb.asset/AssetData/PingFang.ttc"
OUTPUT = "/Users/kaku/WorkBuddy/20260407113700/workbuddy_poster_style3.png"

W, H = 900, 1200

IVORY   = (252, 248, 240)
AMBER   = (210, 130, 30)
PLUM    = (62,  24,  52)
TERRA   = (180, 72,  40)
SAGE    = (78,  116, 90)
CREAM   = (244, 236, 218)
SAND    = (218, 196, 162)
TAN_DIM = (170, 148, 112)
PLUM_LT = (130, 84,  114)

img = Image.new("RGB", (W, H), IVORY)
draw = ImageDraw.Draw(img)

def ef(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
def cf(size, index=0):
    return ImageFont.truetype(PINGFANG, size, index=index)

f_serif_h = ef("YoungSerif-Regular.ttf",       92)
f_serif_s = ef("YoungSerif-Regular.ttf",       22)
f_script  = ef("Italiana-Regular.ttf",          28)
f_sans    = cf(16)
f_sans_b  = cf(16, index=3)
f_tag     = cf(13)
f_label   = ef("InstrumentSans-Bold.ttf",       11)
f_crim    = ef("CrimsonPro-Regular.ttf",        18)
f_crim_b  = ef("CrimsonPro-Bold.ttf",           19)
f_bignum  = ef("Lora-Bold.ttf",                 92)
f_cta     = cf(20, index=3)
f_mono    = ef("JetBrainsMono-Regular.ttf",     11)

# ── Top amber bar ─────────────────────────────────────────────────────────
draw.rectangle([0, 0, W, 8], fill=AMBER)

# ── Header band ───────────────────────────────────────────────────────────
draw.rectangle([0, 8, W, 88], fill=CREAM)
draw.rectangle([0, 88, W, 90], fill=SAND)
draw.text((54, 30), "TENCENT  ·  WORKBUDDY  ·  2026", font=f_label, fill=TAN_DIM)
draw.text((W-54, 30), "腾讯内测版", font=f_tag, fill=AMBER, anchor="ra")
draw.text((W-54, 48), "Beta Open", font=f_label, fill=TAN_DIM, anchor="ra")

# ── Main title ────────────────────────────────────────────────────────────
ty = 102
draw.text((54, ty), "Work", font=f_serif_h, fill=PLUM)
ww = draw.textlength("Work", font=f_serif_h)
draw.text((54 + ww, ty), "Buddy", font=f_serif_h, fill=AMBER)

# ── Italic tagline ────────────────────────────────────────────────────────
draw.text((54, ty + 100), "你的全场景 AI 职场同事", font=cf(26), fill=PLUM_LT)

# Amber rule
rul_y = ty + 140
draw.rectangle([54, rul_y, W-54, rul_y+2], fill=AMBER)
draw.rectangle([54, rul_y+4, 200, rul_y+5], fill=SAND)

# ── Three circles ─────────────────────────────────────────────────────────
circ_y = rul_y + 32
circ_r = 54
cx_list = [54 + (W-108)//6, 54 + (W-108)//2, 54 + 5*(W-108)//6]
cy_c = circ_y + circ_r + 4

circles_data = [
    (PLUM,  "执行任务", "自动规划\n复杂多步"),
    (TERRA, "内容创作", "文档/PPT\n报告表格"),
    (SAGE,  "深度分析", "数据洞察\n行业调研"),
]
for cx, (color, lbl, desc) in zip(cx_list, circles_data):
    draw.ellipse([cx-circ_r, cy_c-circ_r, cx+circ_r, cy_c+circ_r], fill=color)
    draw.text((cx, cy_c-12), lbl, font=f_tag, fill=IVORY, anchor="mm")
    for j, line in enumerate(desc.split("\n")):
        draw.text((cx, cy_c+6+j*17), line, font=f_tag, fill=IVORY, anchor="mm")

# Connecting lines
for i in range(len(cx_list)-1):
    x1 = cx_list[i] + circ_r + 4
    x2 = cx_list[i+1] - circ_r - 4
    draw.line([(x1, cy_c), (x2, cy_c)], fill=SAND, width=2)

# ── Tagline ───────────────────────────────────────────────────────────────
tgy = circ_y + circ_r*2 + 28
draw.text((54, tgy), "听懂自然语言  ·  带脑子思考  ·  真能操作本地文件", font=f_sans_b, fill=PLUM)
draw.text((54, tgy + 26), "一句话描述需求  →  自主规划并执行  →  交付可验收结果", font=f_sans, fill=PLUM_LT)

# ── Problem block ─────────────────────────────────────────────────────────
pb_y = tgy + 62
draw.rectangle([54, pb_y, W-54, pb_y+152], fill=CREAM)
draw.rectangle([54, pb_y, 58, pb_y+152], fill=AMBER)
draw.text((72, pb_y+16), "为什么需要 WorkBuddy ?", font=cf(22, index=3), fill=PLUM)
draw.rectangle([72, pb_y+46, W-70, pb_y+47], fill=SAND)
prob = [
    "腾讯内部 85% 非技术用户被高门槛 AI 工具拒之门外——",
    "不懂编程语言、IDE 开发环境与计算机专业知识，",
    "但他们同样有强烈的办公场景 AI 提效需求。",
    "WorkBuddy 正是为此而生：零门槛，真能干活。",
]
for j, line in enumerate(prob):
    clr = PLUM if j < 3 else AMBER
    f   = f_sans_b if j == 3 else f_sans
    draw.text((72, pb_y+56+j*22), line, font=f, fill=clr)

# ── Differentiator strip ──────────────────────────────────────────────────
diff_y = pb_y + 170
draw.rectangle([0, diff_y, W, diff_y+48], fill=PLUM)
# Use cf for Chinese
diff1 = "不同于 ChatGPT 等聊天机器人只能"
diff2 = "对话"
diff3 = "，WorkBuddy 是真正执行任务的 AI 同事"
total_w = (draw.textlength(diff1, font=f_sans) +
           draw.textlength(diff2, font=f_sans_b) +
           draw.textlength(diff3, font=f_sans))
sx = (W - int(total_w)) // 2
ey = diff_y + 24
draw.text((sx, ey), diff1, font=f_sans, fill=IVORY)
sx += int(draw.textlength(diff1, font=f_sans))
draw.text((sx, ey), diff2, font=f_sans_b, fill=AMBER)
sx += int(draw.textlength(diff2, font=f_sans_b))
draw.text((sx, ey), diff3, font=f_sans, fill=IVORY)

# ── Stats ─────────────────────────────────────────────────────────────────
stat_y = diff_y + 66
draw.text((54, stat_y), "15,000", font=f_bignum, fill=AMBER)
plus_x = 54 + int(draw.textlength("15,000", font=f_bignum))
draw.text((plus_x+4, stat_y+10), "+", font=f_serif_s, fill=TERRA)
draw.text((54, stat_y+90), "腾讯内部 Beta 用户，获一致好评", font=f_sans, fill=PLUM_LT)

# Launch badge
bx, by = W-54-200, stat_y+14
draw.rectangle([bx, by, bx+200, by+76], fill=CREAM)
draw.rectangle([bx, by, bx+4, by+76], fill=TERRA)
draw.text((bx+14, by+10), "发布日期", font=f_tag, fill=TAN_DIM)
draw.text((bx+14, by+30), "2026.01.19", font=f_sans_b, fill=PLUM)
draw.text((bx+14, by+56), "腾讯内部正式上线", font=f_tag, fill=TAN_DIM)

# ── Features list ─────────────────────────────────────────────────────────
feat_y = stat_y + 126
draw.rectangle([54, feat_y, W-54, feat_y+1], fill=SAND)
feat_y += 18
draw.text((54, feat_y), "核心能力", font=cf(22, index=3), fill=PLUM)
feat_y += 34

feats_list = [
    ("自动批量处理文件",      PLUM,    "生成文档 / 表格 / PPT",     TERRA),
    ("多模态内容创作",        SAGE,    "数据深度分析与行业调研",    PLUM_LT),
    ("多任务 Agent 并行处理", AMBER,   "内置多模型 & 主流 MCP Skills", PLUM),
]
for row in feats_list:
    left_t, left_c, right_t, right_c = row
    draw.text((54, feat_y), "✦  " + left_t, font=f_sans, fill=left_c)
    draw.text((54 + (W-108)//2, feat_y), "✦  " + right_t, font=f_sans, fill=right_c)
    feat_y += 26

# ── Bottom CTA ────────────────────────────────────────────────────────────
cta_bg_y = H - 118
draw.rectangle([0, cta_bg_y, W, H], fill=PLUM)
draw.rectangle([0, cta_bg_y, W, cta_bg_y+2], fill=AMBER)

cta_text = "内测开放中  ·  欢迎体验"
tw3 = int(draw.textlength(cta_text, font=f_cta))
draw.text((W//2, cta_bg_y+30), cta_text, font=f_cta, fill=IVORY, anchor="mm")

draw.text((54, cta_bg_y+54), "workbuddy.tencent.com", font=f_mono, fill=TAN_DIM)
draw.text((54, cta_bg_y+72), "Powered by Tencent", font=f_mono, fill=PLUM_LT)
draw.text((130, cta_bg_y+72), "  ·  全角色 · 全场景 · 全能力", font=cf(11), fill=PLUM_LT)
draw.text((W-54, cta_bg_y+66), "2026", font=f_sans_b, fill=AMBER, anchor="ra")

draw.rectangle([0, H-4, W, H], fill=AMBER)

img.save(OUTPUT, "PNG", dpi=(150, 150))
print(f"Saved: {OUTPUT}")
