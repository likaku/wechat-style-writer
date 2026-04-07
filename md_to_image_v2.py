#!/usr/bin/env python3
"""
md_to_image v2 — 公众号图片化输出引擎
用风格一（Chromatic Silence）设计语言，将 Markdown 文本渲染为细长图片卡片。
支持：标题/正文/加粗/Callout/引用/列表/分隔线/插图

用法:
    python3 md_to_image_v2.py
"""
from PIL import Image, ImageDraw, ImageFont
import os
import re

# ── 字体 ───────────────────────────────────────────────────────────────────────
FONT_DIR = "/Users/kaku/.workbuddy/skills/canvas-design/canvas-fonts"
PINGFANG = "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/86ba2c91f017a3749571a82f2c6d890ac7ffb2fb.asset/AssetData/PingFang.ttc"

def ef(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

def cf(size, index=0):
    return ImageFont.truetype(PINGFANG, size, index=index)

# ── 风格一配色（纯白背景版）─────────────────────────────────────────────────
BG      = (255, 255, 255)   # 纯白背景
NAVY    = (8,  18, 42)
TEAL    = (0,  178, 180)
TEAL_DK = (0,  130, 132)
GRAY_L  = (210, 215, 218)
GRAY_M  = (130, 138, 148)
GRAY_D  = (80,  90, 105)
WHITE   = (255, 255, 255)

# ── 细长版：750px 宽度（手机阅读优化）───────────────────────────────────────
W = 750

# ── 字体实例（750px 细长版，字号+32%）──────────────────────────────────────
F_H1     = ef("BricolageGrotesque-Bold.ttf", 45)
F_H2     = cf(30, index=3)       # PingFang SC Semibold
F_H3     = cf(23, index=3)
F_BODY   = cf(22)                # 正文
F_BODY_B = cf(22, index=3)
F_QUOTE  = cf(20)                # 引用稍小
F_TAG    = cf(17)                # 标签/标注
F_MONO   = ef("JetBrainsMono-Regular.ttf", 16)
F_CAPTION = cf(16)
F_SIG    = ef("NothingYouCouldDo-Regular.ttf", 21)  # 草书签名

# ── 布局参数 ───────────────────────────────────────────────────────────────────
MARGIN_X = 40                    # 左右边距
CONTENT_W = W - MARGIN_X * 2     # 内容区宽度
LINE_HEIGHT = 1.75               # 行内行高倍率
# 统一段后间距（同一层次元素之间的标准距离）
GAP_S     = 10   # 小间距：正文→正文、列表项之间  
GAP_M     = 16   # 中间距：正文→callout、正文→引用、callout→正文
GAP_L     = 24   # 大间距：章节标题→第一个正文、分隔线前后、插图前后

# ── 插图目录 ───────────────────────────────────────────────────────────────────
IMG_DIR = "/Users/kaku/WorkBuddy/20260407113700/generated-images"


# ═══════════════════════════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════════════════════════

def split_text_by_script(text):
    """将文本按 CJK / ASCII 脚本分段"""
    segments = []
    current = ""
    current_is_cjk = None
    
    for char in text:
        is_cjk = '\u4e00' <= char <= '\u9fff' or '\u3000' <= char <= '\u303f' or '\uff00' <= char <= '\uffef'
        if current_is_cjk is None:
            current = char
            current_is_cjk = is_cjk
        elif is_cjk == current_is_cjk:
            current += char
        else:
            segments.append((current, current_is_cjk))
            current = char
            current_is_cjk = is_cjk
    
    if current:
        segments.append((current, current_is_cjk))
    return segments


def draw_mixed_text(draw, xy, text, font_cjk, font_ascii, fill, anchor="lt"):
    """绘制混合中英文文本。CJK 用 font_cjk，ASCII 用 font_ascii。"""
    x, y = xy
    segments = split_text_by_script(text)
    
    if anchor in ("mm", "ra") and len(segments) == 1:
        draw.text((x, y), text, 
                  font=font_cjk if segments[0][1] else font_ascii, 
                  fill=fill, anchor=anchor)
        return
    
    for seg_text, is_cjk in segments:
        font = font_cjk if is_cjk else font_ascii
        draw.text((x, y), seg_text, font=font, fill=fill)
        x += font.getlength(seg_text)


def parse_inline(text):
    """简单行内 Markdown 解析，处理 **bold**"""
    parts = []
    pattern = re.compile(r'(\*\*.*?\*\*)')
    last_end = 0
    
    for m in pattern.finditer(text):
        if m.start() > last_end:
            parts.append((text[last_end:m.start()], False))
        parts.append((m.group()[2:-2], True))
        last_end = m.end()
    
    if last_end < len(text):
        parts.append((text[last_end:], False))
    
    if not parts:
        parts.append((text, False))
    
    return parts


def render_paragraph_with_inline(draw, xy, text, font_normal, font_bold,
                                  max_width, color_normal=(45,45,45),
                                  color_bold=None, line_spacing=LINE_HEIGHT,
                                  margin_x=MARGIN_X, after=GAP_S):
    """渲染包含行内 **bold** 的段落。返回 (final_y, total_height)"""
    if color_bold is None:
        color_bold = NAVY

    runs = parse_inline(text)
    x, y = xy
    line_start_y = y
    max_h = font_normal.size * line_spacing

    i = 0
    while i < len(runs):
        txt, bold = runs[i]
        remaining = txt
        while remaining:
            f = font_bold if bold else font_normal
            available = max_width - (x - margin_x)

            if f.getlength(remaining) <= available:
                color = color_bold if bold else color_normal
                draw_mixed_text(draw, (x, y), remaining,
                               cf(f.size, index=3 if bold else 0),
                               f, color)
                x += f.getlength(remaining)
                break
            else:
                cut = len(remaining)
                while cut > 0 and f.getlength(remaining[:cut]) > available:
                    cut -= 1
                if cut == 0:
                    cut = 1

                color = color_bold if bold else color_normal
                draw_mixed_text(draw, (x, y), remaining[:cut],
                               cf(font_normal.size, index=3 if bold else 0),
                               f, color)

                y += int(max_h)
                x = margin_x
                remaining = remaining[cut:]

        i += 1

    # 统一：段落内容高度 + 段后间距 after
    content_h = (y - line_start_y) + max_h if y > line_start_y else max_h
    return y + max_h + after, int(content_h)


def text_wrap(text, font, max_width):
    """中文自动换行。返回行列表。"""
    if not text.strip():
        return []
    
    lines = []
    paragraphs = text.split('\n')
    
    for para in paragraphs:
        if para.strip() == '':
            continue
            
        current_line = ""
        for char in para:
            test_line = current_line + char
            if font.getlength(test_line) > max_width and current_line:
                lines.append(current_line)
                current_line = char
            else:
                current_line = test_line
        if current_line:
            lines.append(current_line)
    
    return lines


# ═══════════════════════════════════════════════════════════════════════════════
# 渲染器
# ═══════════════════════════════════════════════════════════════════════════════

class CardRenderer:
    """
    细长版图片卡片渲染器（750px 宽度）
    支持文字 + 插图混排
    """
    
    def __init__(self, width=W, bg=BG):
        self.W = width
        self.bg = bg
        self.MX = MARGIN_X
        self.CW = CONTENT_W
        self.y = 0
        self.H = 1200
        self.img = Image.new("RGB", (self.W, self.H), self.bg)
        self.draw = ImageDraw.Draw(self.img)
        
    def _ensure_height(self, needed_y, extra_bottom=80):
        """确保画布高度足够"""
        if needed_y + extra_bottom > self.H:
            new_h = int((needed_y + extra_bottom) * 1.3)
            new_img = Image.new("RGB", (self.W, new_h), self.bg)
            new_img.paste(self.img, (0, 0))
            self.img = new_img
            self.H = new_h
            self.draw = ImageDraw.Draw(self.img)
    
    def render_h1(self, text):
        """一级标题"""
        self._ensure_height(self.y + 80)
        y = self.y + 8
        
        # 顶部装饰线
        self.draw.rectangle([0, y, self.W, y+3], fill=NAVY)
        y += 14
        
        # 混排绘制
        draw_mixed_text(self.draw, (self.MX, y), text, 
                       cf(36, index=3), F_H1,   
                       NAVY)
        y += F_H1.size + 8
        
        # 底部装饰线
        self.draw.rectangle([self.MX, y, self.MX + 60, y+2], fill=TEAL)
        
        self.y = y + 18
        return self.y
    
    def render_h2(self, number, text):
        """二级标题：序号 + 文字"""
        self._ensure_height(self.y + 70)
        
        self.y += 22
        
        # 序号（大号浅灰）
        num_y = self.y
        self.draw.text((self.MX, num_y), f"{number:02d}", 
                       font=ef("BricolageGrotesque-Bold.ttf", 28), 
                       fill=GRAY_L)
        
        # 标题
        title_y = num_y + 30
        self.draw.text((self.MX, title_y), text, font=F_H2, fill=NAVY)
        
        # 装饰短线
        under_y = title_y + F_H2.size + 6
        self.draw.rectangle([self.MX, under_y, self.MX + 32, under_y+2], fill=TEAL)
        
        self.y = under_y + 18
        return self.y
    
    def render_h3(self, text):
        """三级标题"""
        self._ensure_height(self.y + 40)
        self.y += 14
        prefix = "— "
        self.draw.text((self.MX, self.y), prefix, font=F_H3, fill=GRAY_L)
        prefix_w = self.draw.textlength(prefix, font=F_H3)
        self.draw.text((self.MX + prefix_w, self.y), text, font=F_H3, fill=NAVY)
        self.y += int(F_H3.size * LINE_HEIGHT) + GAP_S
        return self.y
    
    def render_body(self, text):
        """正文段落（支持 **加粗**）"""
        self._ensure_height(self.y + 40)
        new_y, _h = render_paragraph_with_inline(
            self.draw, (self.MX, self.y), text,
            F_BODY, F_BODY_B,
            max_width=self.CW,
            color_normal=(45, 45, 45),
            color_bold=NAVY,
            after=GAP_S
        )
        self.y = new_y
        return self.y
    
    def render_bullet(self, text, dot="●"):
        """无序列表项"""
        self._ensure_height(self.y + 40)

        dot_y = self.y + 5
        self.draw.text((self.MX, dot_y), dot, font=F_BODY, fill=TEAL)

        new_y, _h = render_paragraph_with_inline(
            self.draw, (self.MX + 22, self.y), text,
            F_BODY, F_BODY_B,
            max_width=self.CW - 22,
            color_normal=(45, 45, 45),
            color_bold=NAVY,
            margin_x=self.MX + 22,
            after=GAP_S
        )
        self.y = new_y
        return self.y
    
    def render_callout(self, text):
        """金句 callout：左侧竖线 + 底纹"""
        lines = text_wrap(text, F_BODY_B, self.CW - 32)
        if not lines:
            return self.y

        line_h = int(F_BODY_B.size * LINE_HEIGHT)
        pad_v = 12          # 上下内边距
        block_h = len(lines) * line_h + pad_v * 2
        self._ensure_height(self.y + block_h + GAP_M)

        block_top = self.y + 4
        block_bottom = self.y + block_h - 4

        # 背景
        self.draw.rectangle(
            [self.MX, block_top, self.W - self.MX, block_bottom],
            fill=(250, 250, 249)
        )
        # 左侧竖线
        self.draw.rectangle([self.MX, block_top, self.MX+4, block_bottom], fill=TEAL)

        for i, line in enumerate(lines):
            ly = block_top + pad_v + i * line_h
            self.draw.text((self.MX + 20, ly), line, font=F_BODY_B, fill=NAVY)

        self.y = block_bottom + GAP_M
        return self.y
    
    def render_quote(self, text):
        """引用块：细竖线 + 浅灰底纹"""
        lines = text_wrap(text, F_QUOTE, self.CW - 28)
        if not lines:
            return self.y

        line_h = int(F_QUOTE.size * LINE_HEIGHT)
        pad_v = 10
        block_h = len(lines) * line_h + pad_v * 2
        self._ensure_height(self.y + block_h + GAP_M)

        block_top = self.y + 3
        block_bottom = self.y + block_h - 3

        # 底纹
        self.draw.rectangle(
            [self.MX, block_top, self.W - self.MX, block_bottom],
            fill=(250, 250, 248)
        )
        # 细竖线
        self.draw.rectangle([self.MX, block_top, self.MX+2, block_bottom], fill=GRAY_M)

        for i, line in enumerate(lines):
            ly = block_top + pad_v + i * line_h
            self.draw.text((self.MX + 16, ly), line, font=F_QUOTE, fill=GRAY_D)

        self.y = block_bottom + GAP_M
        return self.y
    
    def render_separator(self):
        """分隔线"""
        self._ensure_height(self.y + 32)
        self.y += 12
        cx = self.W // 2
        self.draw.text((cx, self.y), "— · —", font=F_TAG, fill=GRAY_L, anchor="mm")
        self.y += 24
        return self.y
    
    def render_image(self, img_path, caption=None):
        """
        插入一张插图。
        图片自适应宽度（最大 W-2*MX），保持比例。
        可选 caption 在图下方居中显示。
        """
        if not os.path.exists(img_path):
            print(f"⚠️ Image not found: {img_path}")
            return self.y
        
        img = Image.open(img_path).convert("RGBA")
        
        # 自适应宽度
        max_w = self.W - 2 * self.MX
        orig_w, orig_h = img.size
        scale = min(max_w / orig_w, 1.0)  # 不放大，只缩小
        new_w = int(orig_w * scale)
        new_h = int(orig_h * scale)
        
        if scale < 1.0:
            img = img.resize((new_w, new_h), Image.LANCZOS)
        
        # 居中位置 + 预估总高度（加更多余量）
        x_offset = (self.W - new_w) // 2
        total_h = new_h + (32 if caption else 22)
        
        # 关键：先扩展画布，再粘贴！
        self._ensure_height(self.y + total_h + 20)
        
        # 上留白
        self.y += 12
        
        # 粘贴图片：RGBA → RGB 合成到白色背景
        rgb_img = Image.new("RGB", img.size, (255, 255, 255))
        rgb_img.paste(img, mask=img.split()[3])
        
        # 右下角草书签名
        sig = ImageDraw.Draw(rgb_img)
        sig.text((new_w - 64, new_h - 18), "kaku", font=F_SIG, fill=(170, 170, 170))
        
        self.img.paste(rgb_img, (x_offset, int(self.y)))
        
        # 重要：_ensure_height 可能重建了画布，需要重新获取 draw 对象
        self.draw = ImageDraw.Draw(self.img)
        
        self.y += new_h + 8
        
        # Caption
        if caption:
            cap_lines = text_wrap(caption, F_CAPTION, self.CW)
            for line in cap_lines:
                cw = self.draw.textlength(line, font=F_CAPTION)
                cx = (self.W - cw) // 2
                self.draw.text((cx, self.y), line, font=F_CAPTION, fill=GRAY_M)
                self.y += int(F_CAPTION.size * LINE_HEIGHT)
        else:
            self.y += 8

        print(f"  🖼 Inserted image: {os.path.basename(img_path)} ({new_w}×{new_h}) at y={self.y}")
        return self.y
    
    def render_data_row(self, label, value, highlight=False):
        """数据行：左标签 + 右数值"""
        self._ensure_height(self.y + 28)
        self.y += 4
        
        lbl_color = TEAL if highlight else GRAY_D
        val_color = NAVY if highlight else GRAY_D
        lbl_font = F_BODY_B if highlight else F_BODY
        val_font = F_BODY_B if highlight else F_BODY
        
        self.draw.text((self.MX, self.y), label, font=lbl_font, fill=lbl_color)
        
        # 右对齐数值
        val_w = self.draw.textlength(value, font=val_font)
        self.draw.text((self.W - MARGIN_X - val_w, self.y), value, font=val_font, fill=val_color)
        
        self.y += int(F_BODY.size * LINE_HEIGHT) + 2
        return self.y
    
    def render_footer(self, text="— END —"):
        """底部结尾"""
        self._ensure_height(self.y + 60)
        self.y += 24
        
        # 线
        self.draw.rectangle([self.MX, self.y, self.W - self.MX, self.y+1], fill=GRAY_L)
        self.y += 12
        
        # 结束文字
        tw = self.draw.textlength(text, font=F_TAG)
        self.draw.text(((self.W - tw)//2, self.y), text, font=F_TAG, fill=GRAY_M)
        self.y += 30
        return self.y
    
    def get_image(self):
        """裁剪到实际内容高度"""
        final = self.img.crop((0, 0, self.W, self.y + 30))
        return final
    
    def save(self, path):
        result = self.get_image()
        result.save(path, "PNG", dpi=(150, 150))
        print(f"✅ Saved: {path} ({result.width}×{result.height}px)")
        return path


# ═══════════════════════════════════════════════════════════════════════════════
# Skill vs APP 完整文章内容
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    r = CardRenderer(width=750)
    
    # ═══════════════════════════════════════════════════════════════════
    #  Skill 替代 App：一场比你想象中更快的范式革命
    # ═══════════════════════════════════════════════════════════════════
    
    # ── H1 封面标题 ───────────────────────────────────────────────────────────
    r.render_h1("Skill 替代 App")
    r.render_body("**一场比你想象中更快的范式革命**")
    r.y += 4
    r.render_body("当你还在纠结下载哪个 App 的时候，Skill 已经开始替你做决定了。")
    
    # ── 分隔线 ─────────────────────────────────────────────────────────────────
    r.render_separator()
    
    # ═══════════════════════════════════════════════════════════════════
    #  第一章：引子 — 2850 亿美元的恐慌
    # ═══════════════════════════════════════════════════════════════════
    
    r.render_h2(1, "引子：2850 亿美元的恐慌")
    
    r.render_body(
        "2026 年 1 月 30 日，Anthropic 发布了 Claude Plugins。" +
        "这不是什么新产品发布会，没有大屏幕，没有「One more thing」。" +
        "只是一个技术博客帖子，宣布 AI 可以通过「插件」直接操控第三方软件——" +
        "订机票、写合同、管项目、做报表，中间不需要打开任何一个 App。"
    )
    
    r.render_body(
        "当天，全球软件股市值蒸发了 **2850 亿美元**。"
    )
    
    r.render_callout(
        "如果用户可以用一句话完成任务，他们为什么还需要打开你的 App？"
    )
    
    r.render_body(
        "几乎同一时间，淘宝上线了 AI 购物助手，用户不再需要搜索、筛选、比价、下单。" +
        "OpenAI 开始在 ChatGPT 里测试商务功能和广告。" +
        "Google 发布了通用商务协议（UCP），Shopify 第一个接入。"
    )
    
    r.render_callout(
        "AI Skill 正在替代传统 App。不是「未来可能」，是「正在发生」。"
    )
    
    # ── 插图 1：手机监狱 ─────────────────────────────────────────────────────
    r.render_image(
        os.path.join(IMG_DIR, "A_satirical_cartoon_in_the_sty_2026-04-07T10-32-55.png"),
        caption="App 是一座座牢房，Skill 是那把钥匙"
    )
    
    # ── 分隔线 ─────────────────────────────────────────────────────────────────
    r.render_separator()
    
    # ═══════════════════════════════════════════════════════════════════
    #  第二章：第一性原理 — 为什么是两个物种
    # ═══════════════════════════════════════════════════════════════════
    
    r.render_h2(2, "第一性原理：两个物种")
    
    r.render_body("**App 的本质是什么？**")
    r.render_body(
        "是人用 CPU 写的确定性逻辑。每一个按钮的位置、每一个流程的分支、" +
        "每一个交互的反馈，都是程序员一行一行写出来的。" +
        "产品经理画原型，设计师出 UI，开发者写代码，测试走流程。" +
        "升级靠人力，迭代靠版本号。这套体系运转了 15 年，非常成熟。"
    )
    
    r.render_body("**Skill 的本质是什么？**")
    r.render_body(
        "是大模型上的概率性推理。它不需要人写每一步逻辑，而是理解你的意图，" +
        "拆解任务，调用工具，完成目标。没有 UI 需要学习，没有流程需要走，" +
        "没有版本号需要更新。"
    )
    
    # 最关键区别
    items = [
        ("App 升级", "靠人写代码 → 线性进化"),
        ("Skill 升级", "靠模型进化 → 指数进化"),
    ]
    for t, d in items:
        r.render_bullet(f"**{t}**：{d}")
    
    r.y += 4
    
    r.render_callout(
        "一个在走路，一个在搭火箭。这就是根本差异。"
    )
    
    # ── 插图 2：乌龟 vs 火箭 ─────────────────────────────────────────────────
    r.render_image(
        os.path.join(IMG_DIR, "A_satirical_cartoon_in_the_sty_2026-04-07T10-34-01.png"),
        caption="背着版本号的 App 乌龟 vs Skill 火箭"
    )
    
    r.render_quote(
        "Skill 的下限低但上限高，App 的下限高但上限固定。" +
        "时间站在 Skill 这边。"
    )
    
    # ── 分隔线 ─────────────────────────────────────────────────────────────────
    r.render_separator()
    
    # ═══════════════════════════════════════════════════════════════════
    #  第三章：历史镜鉴 & 数据说话
    # ═══════════════════════════════════════════════════════════════════
    
    r.render_h2(3, "历史不会说谎")
    
    r.render_h3("移动 App 替代 PC 软件（2008-2015）")
    r.render_body(
        "2007 年 iPhone 发布时，诺基亚高管说「触屏手机不适合商务人士」。" +
        "但手机 App 开辟了全新的体验维度：随时随地、触控、摄像头、GPS。" +
        "到 2015 年，移动端流量超过 PC 端。不是更强，而是更方便。"
    )
    
    r.render_h3("SaaS 替代本地部署（2005-2020）")
    r.render_body(
        "Salesforce 刚出来被嘲笑「功能简陋」「数据不安全」。" +
        "但 SaaS 的优势在于不需要安装、不需要维护、随时升级。" +
        "到 2020 年，全球 SaaS 市场超过 1500 亿美元。"
    )
    
    r.render_callout(
        "新范式从来不是在旧范式的赛道上赢的。它另起炉灶，用旧范式给不了的东西来赢。"
    )
    
    r.render_h3("数据说话：一年涨 8 倍")
    r.render_body(
        "**Gartner 2025.8 正式报告**："
    )
    
    # 数据展示
    r.y += 6
    r.render_data_row("2025 年企业 AI 渗透率", "< 5%", highlight=True)
    r.render_data_row("2026 年预测渗透率", "40%", highlight=True)
    r.render_data_row("增长倍数", "8× 一年", highlight=True)
    r.render_data_row("2035 年预期市场规模", "$4500 亿", highlight=True)
    r.y += 6
    
    r.render_body(
        "**为什么这么快？因为不需要换硬件。**" +
        "App 替代 PC 需要等 iPhone 普及；SaaS 需要等云计算成熟；" +
        "Skill 替代 App 只需要模型升级——每隔几个月自动发生。"
    )
    
    # ── 插图 3：6 个手机的人 vs Done 的人 ────────────────────────────────────
    r.render_image(
        os.path.join(IMG_DIR, "A_satirical_cartoon_in_the_sty_2026-04-07T10-34-39.png"),
        caption="10 步变 1 步 —— 不是效率提升，是交互范式的消灭"
    )
    
    # ── 分隔线 ─────────────────────────────────────────────────────────────────
    r.render_separator()
    
    # ═══════════════════════════════════════════════════════════════════
    #  第四章：渗透地图 — 谁先被吃掉？
    # ═══════════════════════════════════════════════════════════════════
    
    r.render_h2(4, "谁最先被吃掉？")
    
    r.render_h3("第一波：跨 App 流程型场景（已在发生）")
    r.render_body(
        "旅行预订、金融操作、电商购物、医疗预约。" +
        "这些场景的共同特点：用户需要**打开 6 个以上的 App** 才能完成一件事。" +
        "搜航班一个 App、订酒店一个 App、叫车一个 App……一个 Skill 说一句话就搞定。"
    )
    
    r.render_h3("第二波：工具型 App")
    r.render_body(
        "计算器、格式转换、翻译、单位换算、文件处理、OCR。" +
        "功能明确、不需要强视觉、结果导向。Skill 天然就是干这个的。"
    )
    
    r.render_h3("第三波：高认知创作型")
    r.render_body(
        "写作、编程、设计、数据分析。" +
        "GitHub Copilot 辅助全球数百万开发者写代码；" +
        "Cursor 把 AI 直接嵌进编辑器。这一波正在发生。"
    )
    
    r.render_h3("最难替代的：强交互 + 强视觉")
    r.render_body(
        "社交、游戏、短视频。核心价值是**体验本身**而非「完成任务」。" +
        "你打开抖音不是为了完成一个任务，是为了消磨时间、获得多巴胺。" +
        "但也不要低估变化——当 Skill 能给你情绪价值的时候，某些社交场景也会被重新定义。"
    )
    
    r.render_callout(
        "未来的 Skill 不是工具，是伙伴。谁能做出让用户有情感依赖的 Skill，谁就有了最深的护城河。"
    )
    
    # ── 插图 4：一面墙的 APP vs 一句话搞定 ────────────────────────────────────
    r.render_image(
        os.path.join(IMG_DIR, "Satirical_cartoon__New_Yorker__2026-04-07T10-54-41.png"),
        caption="10 个 App 的混乱 → 1 句话搞定"
    )
    
    # ── 分隔线 ─────────────────────────────────────────────────────────────────
    r.render_separator()
    
    # ═══════════════════════════════════════════════════════════════════
    #  第五章：你应该怎么办？
    # ═══════════════════════════════════════════════════════════════════
    
    r.render_h2(5, "你应该怎么办？")
    
    r.render_body("如果你是 **App 开发者**：",)
    r.render_body(
        "不要等 Skill 来替代你，主动把 AI Agent 嵌进你的产品。" +
        "63% 的零售商认为不做 Agent 两年内就会落后。"
    )
    
    r.render_body("如果你是**领域专家**（不会写代码也没关系）：")
    r.render_body(
        "把你的方法论做成 Skill。护城河不是技术，是知识。" +
        "现在开始做，你就是 2008 年第一批进 App Store 的人。"
    )
    
    r.render_body("如果你是**普通用户**：")
    r.render_body(
        "开始尝试用 Skill 替代你手机上的一些 App。" +
        "很多你以为需要打开 App 才能做的事情，说一句话就够了。"
    )
    
    r.render_callout(
        "对个人开发者来说，现在正是 2008 年 App Store 刚开的那个时刻——起跑线上没有大厂，只有先知。窗口不会一直开着。"
    )
    
    # ── 插图 5：躺椅上的人 vs AI 机器人 ───────────────────────────────────────
    r.render_image(
        os.path.join(IMG_DIR, "Satirical_cartoon__New_Yorker__2026-04-07T10-52-10.png"),
        caption='"Book me a flight to Tokyo." — "Certainly!"'
    )
    
    # ── 结语数据总结 ──────────────────────────────────────────────────────────
    r.y += 8
    r.render_separator()
    
    r.render_body("**数据不会说谎：**")
    data_items = [
        ("一年 8× 企业渗透率", "Gartner"),
        ("$4500 亿市场预期", "Gartner, 2035"),
        ("$2850 亿股市即时反应", "2026.1.30"),
        ("70 万+ Skill 生态规模", "2026"),
        ("1/3 消费者愿通过 Agent 购买", "Gen Z: 32%"),
    ]
    for val, src in data_items:
        r.render_bullet(f"**{val}**（{src}）")
    
    r.y += 8
    r.render_callout(
        "Skill 替代 App 不是「如果」的问题，而是「你准备好了没有」的问题。"
    )
    
    # ── Footer ─────────────────────────────────────────────────────────────────
    r.render_footer("Skill 替代 App · 范式革命进行时")
    
    # ── 保存 ───────────────────────────────────────────────────────────────────
    out = "/Users/kaku/WorkBuddy/20260407113700/skill_vs_app_full.png"
    r.save(out)


if __name__ == "__main__":
    main()
