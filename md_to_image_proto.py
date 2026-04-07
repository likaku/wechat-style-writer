#!/usr/bin/env python3
"""
md_to_image.py — 最小原型 v0.1
用风格一（Chromatic Silence）设计语言，将 Markdown 文本渲染为图片卡片。
公众号图片化输出方案验证。

目标：
  - 验证 PIL 渲染中文长文的可行性
  - 验证风格一配色/字体在正文场景的效果
  - 验证动态高度自适应布局

用法:
    python3 md_to_image_proto.py
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

# ── 风格一配色（Chromatic Silence）───────────────────────────────────────────
BG      = (248, 248, 246)
NAVY    = (8,  18, 42)
TEAL    = (0,  178, 180)
TEAL_DK = (0,  130, 132)
GRAY_L  = (210, 215, 218)
GRAY_M  = (130, 138, 148)
GRAY_D  = (80,  90, 105)
WHITE   = (255, 255, 255)

# 公众号图片宽度：900px（更细长，适合手机阅读）
W = 900

# ── 字体实例（适配 900px 细长版）──────────────────────────────────────────────
F_H1     = ef("BricolageGrotesque-Bold.ttf", 42)
F_H2     = cf(26, index=3)       # PingFang SC Semibold
F_H3     = cf(20, index=3)
F_BODY   = cf(18)                # 正文
F_BODY_B = cf(18, index=3)
F_QUOTE  = cf(17)                # 引用稍小
F_TAG    = cf(15)                # 标签/标注
F_MONO   = ef("JetBrainsMono-Regular.ttf", 13)
F_CAPTION = cf(13)

# ── 布局参数 ───────────────────────────────────────────────────────────────────
MARGIN_X = 50                    # 左右边距（窄图稍收窄）
CONTENT_W = W - MARGIN_X * 2     # 内容区宽度
LINE_HEIGHT = 1.85               # 行高倍率
PARA_SPACE = 20                  # 段间距


# ═══════════════════════════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════════════════════════

def split_text_by_script(text):
    """
    将文本按 CJK / ASCII 脚本分段。
    返回 [(segment_text, is_cjk), ...]
    用于混排英文+中文时分别用不同字体。
    """
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
    """
    绘制混合中英文文本。CJK 用 font_cjk，ASCII 用 font_ascii。
    自动逐段切换字体，保持 x 坐标连续。
    """
    x, y = xy
    segments = split_text_by_script(text)
    
    if anchor in ("mm", "ra") and len(segments) == 1:
        # 单段特殊锚点
        draw.text((x, y), text, 
                  font=font_cjk if segments[0][1] else font_ascii, 
                  fill=fill, anchor=anchor)
        return
    
    for seg_text, is_cjk in segments:
        font = font_cjk if is_cjk else font_ascii
        draw.text((x, y), seg_text, font=font, fill=fill)
        w = font.getlength(seg_text)
        # 对于最后一个字符如果是 CJK，需要额外加一点间距
        x += w


def parse_inline(text):
    """
    简单行内 Markdown 解析。
    返回 [(display_text, is_bold), ...]
    只处理 **bold** 标记。
    """
    parts = []
    # 匹配 **...**
    pattern = re.compile(r'(\*\*.*?\*\*)')
    last_end = 0
    
    for m in pattern.finditer(text):
        # 前面的普通文本
        if m.start() > last_end:
            parts.append((text[last_end:m.start()], False))
        # 加粗部分（去掉 **）
        parts.append((m.group()[2:-2], True))
        last_end = m.end()
    
    # 剩余文本
    if last_end < len(text):
        parts.append((text[last_end:], False))
    
    if not parts:
        parts.append((text, False))
    
    return parts


def render_paragraph_with_inline(draw, xy, text, font_normal, font_bold, 
                                  max_width, color_normal=(45,45,45), 
                                  color_bold=None, line_spacing=LINE_HEIGHT,
                                  margin_x=MARGIN_X):
    """
    渲染包含行内 **bold** 的段落。
    处理换行时需要考虑每个 run 的宽度。
    返回 (final_y, total_height)
    """
    if color_bold is None:
        color_bold = NAVY
    
    runs = parse_inline(text)
    x, y = xy
    line_start_y = y
    max_h = font_normal.size * line_spacing
    
    def measure_run(txt, bold):
        f = font_bold if bold else font_normal
        return f.getlength(txt)
    
    i = 0
    while i < len(runs):
        txt, bold = runs[i]
        
        # 如果 run 太长需要跨行
        remaining = txt
        while remaining:
            f = font_bold if bold else font_normal
            available = max_width - (x - margin_x)
            
            if f.getlength(remaining) <= available:
                # 整个剩余部分放得下
                color = color_bold if bold else color_normal
                draw_mixed_text(draw, (x, y), remaining, 
                               f if not any('\u4e00'<=c<='\u9fff' for c in remaining) else cf(f.size, index=3 if bold else 0),
                               f, color)
                x += f.getlength(remaining)
                break
            else:
                # 需要截断换行
                # 逐步找到能放下的字符数
                cut = len(remaining)
                while cut > 0 and f.getlength(remaining[:cut]) > available:
                    cut -= 1
                if cut == 0:
                    cut = 1  # 至少放一个字符
                
                color = color_bold if bold else color_normal
                draw_mixed_text(draw, (x, y), remaining[:cut],
                               cf(font_normal.size, index=3 if bold else 0),
                               f, color)
                
                # 换行
                y += int(max_h)
                x = margin_x
                remaining = remaining[cut:]
        
        i += 1
    
    total_h = (y - line_start_y) + max_h if y > line_start_y else max_h
    return y + int(max_h * 0.2) + PARA_SPACE, int(total_h)


def text_wrap(text, font, max_width):
    """
    中文自动换行。返回行列表。
    PIL 的 textlength() 可以正确计算 CJK 字符宽度。
    """
    if not text.strip():
        return []
    
    lines = []
    # 先按原始换行符分割段落
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


def measure_text_height(text_lines, font, line_spacing=LINE_HEIGHT):
    """计算多行文本渲染高度"""
    if not text_lines:
        return 0
    line_h = font.size * line_spacing
    # 最后一行不加行距（或者也加？这里统一加）
    return len(text_lines) * line_h


def measure_block_height(text, font, max_width, line_spacing=LINE_HEIGHT, para_space=PARA_SPACE):
    """测量一段文字（可能多段）的总高度"""
    lines = text_wrap(text, font, max_width)
    h = measure_text_height(lines, font, line_spacing)
    return int(h) + para_space


# ═══════════════════════════════════════════════════════════════════════════════
# 渲染器 — 每种元素类型一个函数，返回占用的高度
# ═══════════════════════════════════════════════════════════════════════════════

class CardRenderer:
    """
    图片卡片渲染器。
    维护当前 Y 坐标，每个 render_* 方法绘制内容并返回新 Y 坐标。
    最终可以获取总高度和图片对象。
    """
    
    def __init__(self, width=W, bg=BG):
        self.W = width
        self.bg = bg
        self.MX = MARGIN_X
        self.CW = CONTENT_W
        self.y = 0
        # 初始高度先给个最小值，后面会动态扩展
        self.H = 800
        self.img = Image.new("RGB", (self.W, self.H), self.bg)
        self.draw = ImageDraw.Draw(self.img)
        
    def _ensure_height(self, needed_y, extra_bottom=60):
        """确保画布高度足够，不够就扩"""
        if needed_y + extra_bottom > self.H:
            new_h = int((needed_y + extra_bottom) * 1.3)
            new_img = Image.new("RGB", (self.W, new_h), self.bg)
            new_img.paste(self.img, (0, 0))
            self.img = new_img
            self.H = new_h
            self.draw = ImageDraw.Draw(self.img)
    
    def render_h1(self, text):
        """一级标题 — 中英文混排"""
        self._ensure_height(self.y + 100)
        y = self.y + 10
        
        # 顶部装饰线
        self.draw.rectangle([0, y, self.W, y+4], fill=NAVY)
        y += 20
        
        # 混排绘制：中文用 PingFang，英文/数字用 BricolageGrotesque
        draw_mixed_text(self.draw, (self.MX, y), text, 
                       cf(48, index=3), F_H1,   # font_cjk=PingFang, font_ascii=Bricolage
                       NAVY)
        y += F_H1.size + 12
        
        # 底部装饰线
        self.draw.rectangle([self.MX, y, self.MX + 80, y+2], fill=TEAL)
        
        self.y = y + 24
        return self.y
    
    def render_h2(self, number, text):
        """二级标题：大号序号 + 标题文字"""
        self._ensure_height(self.y + 90)
        
        # 上留白
        self.y += 28
        
        # 序号
        num_y = self.y
        self.draw.text((self.MX, num_y), f"{number:02d}", 
                       font=ef("BricolageGrotesque-Bold.ttf", 36), 
                       fill=GRAY_L)
        
        # 标题
        title_y = num_y + 38
        self.draw.text((self.MX, title_y), text, font=F_H2, fill=NAVY)
        
        # 装饰短线
        under_y = title_y + F_H2.size + 8
        self.draw.rectangle([self.MX, under_y, self.MX + 40, under_y+2], fill=TEAL)
        
        self.y = under_y + 22
        return self.y
    
    def render_h3(self, text):
        """三级标题"""
        self._ensure_height(self.y + 50)
        self.y += 18
        prefix = "— "
        self.draw.text((self.MX, self.y), prefix, font=F_H3, fill=GRAY_L)
        prefix_w = self.draw.textlength(prefix, font=F_H3)
        self.draw.text((self.MX + prefix_w, self.y), text, font=F_H3, fill=NAVY)
        self.y += int(F_H3.size * LINE_HEIGHT) + 8
        return self.y
    
    def render_body(self, text):
        """正文段落（支持行内 **加粗**）"""
        self._ensure_height(self.y + 40)
        new_y, _h = render_paragraph_with_inline(
            self.draw, (self.MX, self.y), text,
            F_BODY, F_BODY_B,
            max_width=self.CW,
            color_normal=(45, 45, 45),
            color_bold=NAVY
        )
        self.y = new_y
        return self.y
    
    def render_bullet(self, text, dot="●"):
        """无序列表项（支持行内 **加粗**）"""
        self._ensure_height(self.y + 40)
        
        # 绘制圆点
        dot_y = self.y + 4
        self.draw.text((self.MX, dot_y), dot, font=F_BODY, fill=TEAL)
        
        # 缩进渲染文字
        new_y, _h = render_paragraph_with_inline(
            self.draw, (self.MX + 28, self.y), text,
            F_BODY, F_BODY_B,
            max_width=self.CW - 28,
            color_normal=(45, 45, 45),
            color_bold=NAVY,
            margin_x=self.MX + 28
        )
        self.y = new_y
        return self.y
    
    def render_callout(self, text):
        """金句 callout：左侧竖线 + 底纹"""
        lines = text_wrap(text, F_BODY_B, self.CW - 40)
        if not lines:
            return self.y
        
        line_h = int(F_BODY_B.size * 1.7)
        block_h = len(lines) * line_h + 32
        self._ensure_height(self.y + block_h)
        
        block_top = self.y + 6
        block_bottom = self.y + block_h - 6
        
        # 背景
        self.draw.rectangle(
            [self.MX, block_top, self.W - self.MX, block_bottom], 
            fill=(245, 245, 244)
        )
        # 左侧竖线
        self.draw.rectangle([self.MX, block_top, self.MX+5, block_bottom], fill=TEAL)
        
        # 文字
        for i, line in enumerate(lines):
            ly = block_top + 12 + i * line_h
            self.draw.text((self.MX + 24, ly), line, font=F_BODY_B, fill=NAVY)
        
        self.y += block_h + 8
        return self.y
    
    def render_quote(self, text):
        """引用块：细竖线 + 浅灰底纹"""
        lines = text_wrap(text, F_QUOTE, self.CW - 36)
        if not lines:
            return self.y
        
        line_h = int(F_QUOTE.size * 1.75)
        block_h = len(lines) * line_h + 28
        self._ensure_height(self.y + block_h)
        
        block_top = self.y + 4
        block_bottom = self.y + block_h - 4
        
        # 底纹
        self.draw.rectangle(
            [self.MX, block_top, self.W - self.MX, block_bottom],
            fill=(250, 250, 248)
        )
        # 细竖线
        self.draw.rectangle([self.MX, block_top, self.MX+3, block_bottom], fill=GRAY_M)
        
        for i, line in enumerate(lines):
            ly = block_top + 10 + i * line_h
            self.draw.text((self.MX + 20, ly), line, font=F_QUOTE, fill=GRAY_D)
        
        self.y += block_h + 6
        return self.y
    
    def render_separator(self):
        """分隔线"""
        self._ensure_height(self.y + 40)
        self.y += 16
        cx = self.W // 2
        sep_w = 80
        self.draw.text((cx - sep_w//2, self.y), "— · —", font=F_TAG, fill=GRAY_L, anchor="mm")
        self.y += 30
        return self.y
    
    def render_footer(self, text="— END —"):
        """底部结尾"""
        self._ensure_height(self.y + 80)
        self.y += 30
        
        # 线
        self.draw.rectangle([self.MX, self.y, self.W - self.MX, self.y+1], fill=GRAY_L)
        self.y += 16
        
        # 结束文字
        tw = self.draw.textlength(text, font=F_TAG)
        self.draw.text(((self.W - tw)//2, self.y), text, font=F_TAG, fill=GRAY_M)
        self.y += 40
        return self.y
    
    def get_image(self):
        """裁剪到实际内容高度，返回图片"""
        # 裁掉多余空白
        final = self.img.crop((0, 0, self.W, self.y + 40))
        return final
    
    def save(self, path):
        result = self.get_image()
        result.save(path, "PNG", dpi=(150, 150))
        print(f"✅ Saved: {path} ({result.width}×{result.height}px)")
        return path


# ═══════════════════════════════════════════════════════════════════════════════
# 示例内容 & 渲染测试
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    r = CardRenderer(width=900)
    
    # ═══════════════════════════════════════════════════════════════════
    #  Skill vs APP：两种 AI 产品形态的深度对比
    # ═══════════════════════════════════════════════════════════════════
    
    # ── H1 标题 ───────────────────────────────────────────────────────────────
    r.render_h1("Skill vs APP：AI 产品的两条路")
    
    # ── 导语 ───────────────────────────────────────────────────────────────────
    r.render_body(
        "当我们在谈论 AI 产品时，实际上在说两件完全不同的事。" +
        "一种是 **APP**，一种是 **Skill**。它们看起来相似，但底层逻辑天差地别。"
    )
    r.y += 8
    
    # ── H2 第一章：什么是 APP ──────────────────────────────────────────────────
    r.render_h2(1, "APP：一个封闭的花园")
    
    r.render_body(
        "APP 是我们最熟悉的形态。你打开微信、打开抖音、打开 ChatGPT，" +
        "进入的是一个**预设好的功能边界**。开发者决定了你能做什么、不能做什么。"
    )
    
    r.render_body(
        "APP 的本质是**「我给你什么，你用什么」**。" +
        "它像一个精心设计的主题公园——路线规划好了，项目固定了，" +
        "你的体验被限定在围墙之内。"
    )
    
    # ── Callout ────────────────────────────────────────────────────────────────
    r.render_callout(
        "APP 的边界就是能力的边界。" +
        "用户想要围墙外的功能？等下一个版本吧。"
    )
    
    # ── 分隔线 ─────────────────────────────────────────────────────────────────
    r.render_separator()
    
    # ── H2 第二章：什么是 Skill ───────────────────────────────────────────────
    r.render_h2(2, "Skill：一把万能钥匙")
    
    r.render_body(
        "Skill 是另一种思路。它不是一个独立的应用，而是一种**能力插件**——" +
        "可以嵌入到任何工具、任何场景、任何工作流中。"
    )
    
    r.render_body(
        "Skill 的本质是**「你需要什么，我就变成什么」**。" +
        "它不像一个公园，更像一套工具箱。你拿锤子钉钉子，拿螺丝刀拧螺丝，" +
        "工具随场景而变，但能力始终在线。"
    )
    
    # ── 列表对比 ───────────────────────────────────────────────────────────────
    items = [
        ("使用场景", "APP 固定入口，Skill 随处调用"),
        ("能力边界", "APP 功能预置，Skill 按需扩展"),
        ("用户体验", "APP 学习成本高，Skill 自然语言驱动"),
        ("迭代速度", "APP 发版周期长，Skill 实时更新"),
    ]
    for title_text, desc in items:
        r.render_bullet(f"**{title_text}**：{desc}")
    
    r.y += 8
    
    # ── 引用块 ─────────────────────────────────────────────────────────────────
    r.render_quote(
        "APP 问：你要不要用我的功能？" +
        "Skill 问：你想解决什么问题？——这是两种完全不同的产品哲学。"
    )
    
    # ── H2 第三章：为什么 Skill 是未来 ───────────────────────────────────────
    r.render_h2(3, "为什么 Skill 是未来")
    
    r.render_body(
        "**AI 的终极形态不是超级 APP，而是无所不在的能力层。**" +
        "未来的工作流不是在十个 APP 之间来回切换，" +
        "而是 AI 能力像水电一样——需要时就在那里。"
    )
    
    r.render_body(
        "WorkBuddy 走的就是这条路。它不希望你「打开一个 AI 应用」," +
        "而是让你在任何需要的地方直接召唤 AI 能力。" +
        "写报告时在 Word 里调用，分析数据时在 Excel 里调用，" +
        "做 PPT 时在幻灯片里调用。"
    )
    
    # ── Callout ────────────────────────────────────────────────────────────────
    r.render_callout(
        "最好的 AI 不是让你离开工作去用 AI，" +
        "而是让 AI 来到你的工作中。"
    )
    
    # ── Footer ─────────────────────────────────────────────────────────────────
    r.render_footer("Skill vs APP  ·  AI 产品的下一站")
    
    # ── 保存 ───────────────────────────────────────────────────────────────────
    out = "/Users/kaku/WorkBuddy/20260407113700/proto_card_v01.png"
    r.save(out)


if __name__ == "__main__":
    main()
