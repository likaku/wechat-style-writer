#!/usr/bin/env python3
"""
Word 渲染器 — 与 CardRenderer v2 (md_to_image_v2.py) 完全一致的排版
输出 .docx 文件，方便上传公众号编辑器

视觉映射：
  H1        → 顶部 NAVY 装饰线 + BricolageGrotesque-Bold 56pt 标题 + TEAL 底线
  H2        → 浅灰序号 + PingFang SC Semibold 38pt 标题 + TEAL 短线
  H3        → "— " 前缀 + PingFang SC Semibold 29pt
  Body      → PingFang SC 28pt，加粗用 Semibold，颜色 #2D2D2D / NAVY
  Callout   → 左侧 TEAL 竖线 + 浅灰背景块 + Semibold 加粗文字
  Bullet    → TEAL 圆点 ● + 缩进正文
  Separator → 居中 "— · —" 分隔符
  Image     → 居中插图 + caption
  Data Row  → 左标签 + 右数值
  Footer    → 灰线 + 居中文字
"""
from docx import Document
from docx.shared import Pt, Cm, Emu, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import os
import re


# ═══════════════════════════════════════════════════════════════════════════════
# 配色常量（与 md_to_image_v2.py 一致）
# ═══════════════════════════════════════════════════════════════════════════════
NAVY_RGB   = RGBColor(8, 18, 42)
TEAL_RGB   = RGBColor(0, 178, 180)
TEAL_DK    = RGBColor(0, 130, 132)
GRAY_L_RGB = RGBColor(210, 215, 218)
GRAY_M_RGB = RGBColor(130, 138, 148)
GRAY_D_RGB = RGBColor(80, 90, 105)
BODY_RGB   = RGBColor(45, 45, 45)
WHITE_RGB  = RGBColor(255, 255, 255)


# ═══════════════════════════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════════════════════════

def clean_text(text):
    """清除 Unicode 占位符和中文间多余空格"""
    text = re.sub(r'[\u330c\u330d]+', '', text)
    text = re.sub(r'(?<=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]) +(?=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])', '', text)
    return text


def parse_inline(text):
    """解析 **bold** 行内标记，返回 [(text, is_bold), ...]"""
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


def set_run_font(run, size_pt, bold=False, color=None, font_name='PingFang SC',
                 font_name_east='PingFang SC'):
    """设置 run 的字体属性"""
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    if color:
        run.font.color.rgb = color
    run.font.name = font_name
    # 设置东亚字体
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:eastAsia="{font_name_east}"/>')
        rPr.insert(0, rFonts)
    else:
        rFonts.set(qn('w:eastAsia'), font_name_east)


def add_shading(paragraph, color_hex="FAFAF9"):
    """给段落添加底纹背景色"""
    pPr = paragraph._element.get_or_add_pPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}" w:val="clear"/>')
    pPr.append(shd)


def add_left_border(paragraph, color_hex="00B2B4", width_pt=5):
    """给段落添加左侧彩色边框（模拟 callout 竖线）"""
    pPr = paragraph._element.get_or_add_pPr()
    # 左边框
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:left w:val="single" w:sz="{int(width_pt * 8)}" w:space="8" w:color="{color_hex}"/>'
        f'</w:pBdr>'
    )
    pPr.append(pBdr)


def add_top_bottom_border(paragraph, color_hex="051C2C", position="top", width_pt=1.5):
    """给段落添加顶部或底部边框线"""
    pPr = paragraph._element.get_or_add_pPr()
    sz = int(width_pt * 8)
    tag = f'w:{position}'
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <{tag} w:val="single" w:sz="{sz}" w:space="1" w:color="{color_hex}"/>'
        f'</w:pBdr>'
    )
    pPr.append(pBdr)


def set_paragraph_spacing(paragraph, before_pt=0, after_pt=0, line_spacing=None):
    """设置段落间距"""
    pf = paragraph.paragraph_format
    pf.space_before = Pt(before_pt)
    pf.space_after = Pt(after_pt)
    if line_spacing:
        pf.line_spacing = Pt(line_spacing)


# ═══════════════════════════════════════════════════════════════════════════════
# Word 渲染器
# ═══════════════════════════════════════════════════════════════════════════════

class WordRenderer:
    """
    与 CardRenderer v2 完全一致的 Word 文档渲染器
    输出格式：.docx（A4 纵向，窄边距）
    """

    def __init__(self, output_path=None):
        self.doc = Document()
        self.output_path = output_path

        # 页面设置：A4 纵向，窄边距（模拟 750px 手机宽度）
        section = self.doc.sections[0]
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)

        # 设置默认字体
        style = self.doc.styles['Normal']
        style.font.name = 'PingFang SC'
        style.font.size = Pt(14)
        style.font.color.rgb = BODY_RGB
        style._element.rPr.rFonts.set(qn('w:eastAsia'), 'PingFang SC')
        style.paragraph_format.line_spacing = Pt(28)

    def render_h1(self, text):
        """一级标题：顶部 NAVY 装饰线 + 大标题 + TEAL 底线"""
        text = clean_text(text)

        # 顶部装饰线（用段落顶部边框模拟）
        line_p = self.doc.add_paragraph()
        line_p.paragraph_format.space_before = Pt(8)
        line_p.paragraph_format.space_after = Pt(12)
        add_top_bottom_border(line_p, "051C2C", "top", width_pt=3)
        # 占位 run
        run = line_p.add_run(" ")
        set_run_font(run, 2, color=NAVY_RGB)

        # 主标题
        title_p = self.doc.add_paragraph()
        title_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        title_p.paragraph_format.space_before = Pt(4)
        title_p.paragraph_format.space_after = Pt(6)
        title_p.paragraph_format.line_spacing = Pt(60)

        run = title_p.add_run(text)
        set_run_font(run, 28, bold=True, color=NAVY_RGB, font_name='Bricolage Grotesque Bold',
                     font_name_east='PingFang SC Semibold')

        # TEAL 底线（用段落底部边框模拟）
        teal_line = self.doc.add_paragraph()
        teal_line.paragraph_format.space_before = Pt(0)
        teal_line.paragraph_format.space_after = Pt(16)
        add_top_bottom_border(teal_line, "00B2B4", "bottom", width_pt=2)
        # 缩短线宽（左缩进）
        teal_line.paragraph_format.left_indent = Cm(0)
        run = teal_line.add_run(" ")
        set_run_font(run, 2, color=TEAL_RGB)

    def render_h2(self, number, text):
        """二级标题：浅灰序号 + 标题 + TEAL 短线"""
        text = clean_text(text)

        # 序号行
        num_p = self.doc.add_paragraph()
        num_p.paragraph_format.space_before = Pt(20)
        num_p.paragraph_format.space_after = Pt(2)
        num_p.paragraph_format.line_spacing = Pt(36)

        run = num_p.add_run(f"{number:02d}")
        set_run_font(run, 18, bold=True, color=GRAY_L_RGB,
                     font_name='Bricolage Grotesque Bold', font_name_east='Bricolage Grotesque Bold')

        # 标题行
        title_p = self.doc.add_paragraph()
        title_p.paragraph_format.space_before = Pt(2)
        title_p.paragraph_format.space_after = Pt(4)
        title_p.paragraph_format.line_spacing = Pt(44)

        run = title_p.add_run(text)
        set_run_font(run, 19, bold=True, color=NAVY_RGB,
                     font_name='PingFang SC Semibold', font_name_east='PingFang SC Semibold')

        # TEAL 短线
        teal_p = self.doc.add_paragraph()
        teal_p.paragraph_format.space_before = Pt(0)
        teal_p.paragraph_format.space_after = Pt(14)
        add_top_bottom_border(teal_p, "00B2B4", "bottom", width_pt=2)
        teal_p.paragraph_format.right_indent = Cm(14)  # 短线效果
        run = teal_p.add_run(" ")
        set_run_font(run, 2, color=TEAL_RGB)

    def render_h3(self, text):
        """三级标题："— " 前缀 + Semibold"""
        text = clean_text(text)

        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.line_spacing = Pt(34)

        # 前缀 "— "
        run_prefix = p.add_run("— ")
        set_run_font(run_prefix, 14.5, color=GRAY_L_RGB,
                     font_name='PingFang SC', font_name_east='PingFang SC')

        # 标题文字
        run_text = p.add_run(text)
        set_run_font(run_text, 14.5, bold=True, color=NAVY_RGB,
                     font_name='PingFang SC Semibold', font_name_east='PingFang SC Semibold')

    def render_body(self, text):
        """正文段落（支持 **加粗**）"""
        text = clean_text(text)
        parts = parse_inline(text)

        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = Pt(28)

        for txt, bold in parts:
            run = p.add_run(txt)
            color = NAVY_RGB if bold else BODY_RGB
            set_run_font(run, 14, bold=bold, color=color,
                         font_name='PingFang SC Semibold' if bold else 'PingFang SC',
                         font_name_east='PingFang SC Semibold' if bold else 'PingFang SC')

    def render_callout(self, text):
        """金句 callout：左侧 TEAL 竖线 + 浅灰底纹 + 加粗文字"""
        text = clean_text(text)

        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(12)
        p.paragraph_format.line_spacing = Pt(30)
        p.paragraph_format.left_indent = Cm(0.3)
        p.paragraph_format.right_indent = Cm(0)

        # 底纹 + 左边框
        add_shading(p, "FAFAF9")
        add_left_border(p, "00B2B4", width_pt=6)

        # 文字（全部加粗，NAVY 色）
        run = p.add_run(text)
        set_run_font(run, 14, bold=True, color=NAVY_RGB,
                     font_name='PingFang SC Semibold', font_name_east='PingFang SC Semibold')

    def render_quote(self, text):
        """引用块：左侧细灰竖线 + 浅灰底纹"""
        text = clean_text(text)

        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(12)
        p.paragraph_format.line_spacing = Pt(26)
        p.paragraph_format.left_indent = Cm(0.3)

        add_shading(p, "FAFAF8")
        add_left_border(p, "828A94", width_pt=3)

        run = p.add_run(text)
        set_run_font(run, 12.5, color=GRAY_D_RGB,
                     font_name='PingFang SC', font_name_east='PingFang SC')

    def render_bullet(self, text, dot="●"):
        """无序列表项"""
        text = clean_text(text)
        parts = parse_inline(text)

        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = Pt(28)
        p.paragraph_format.left_indent = Cm(0.8)
        p.paragraph_format.first_line_indent = Cm(-0.5)

        # 圆点
        dot_run = p.add_run(f"{dot} ")
        set_run_font(dot_run, 14, color=TEAL_RGB,
                     font_name='PingFang SC', font_name_east='PingFang SC')

        # 内容
        for txt, bold in parts:
            run = p.add_run(txt)
            color = NAVY_RGB if bold else BODY_RGB
            set_run_font(run, 14, bold=bold, color=color,
                         font_name='PingFang SC Semibold' if bold else 'PingFang SC',
                         font_name_east='PingFang SC Semibold' if bold else 'PingFang SC')

    def render_separator(self):
        """分隔线：居中 "— · —" """
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(12)

        run = p.add_run("— · —")
        set_run_font(run, 10.5, color=GRAY_L_RGB,
                     font_name='PingFang SC', font_name_east='PingFang SC')

    def render_image(self, img_path, caption=None):
        """插入图片 + 可选 caption"""
        if not os.path.exists(img_path):
            print(f"⚠️ Image not found: {img_path}")
            return

        # 图片段落
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        # 关键：行间距设为 single（1.0 倍），让图片完整显示不被裁切
        p.paragraph_format.line_spacing = None  # 清除固定行距
        from docx.enum.text import WD_LINE_SPACING
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE

        # 计算图片宽度（适配页面内容区宽度）
        section = self.doc.sections[0]
        content_width = section.page_width - section.left_margin - section.right_margin
        # 限制最大宽度
        img_width = min(content_width, Cm(16.0))

        run = p.add_run()
        run.add_picture(img_path, width=img_width)

        # Caption
        if caption:
            cap_p = self.doc.add_paragraph()
            cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cap_p.paragraph_format.space_before = Pt(2)
            cap_p.paragraph_format.space_after = Pt(8)

            run = cap_p.add_run(caption)
            set_run_font(run, 10, color=GRAY_M_RGB,
                         font_name='PingFang SC', font_name_east='PingFang SC')

    def render_data_row(self, label, value, highlight=False):
        """数据行：左标签 + 右数值"""
        label = clean_text(label)
        value = clean_text(value)

        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = Pt(28)

        # 左侧标签
        lbl_color = TEAL_RGB if highlight else GRAY_D_RGB
        lbl_bold = highlight
        lbl_run = p.add_run(label + "  ")
        set_run_font(lbl_run, 14, bold=lbl_bold, color=lbl_color,
                     font_name='PingFang SC Semibold' if lbl_bold else 'PingFang SC',
                     font_name_east='PingFang SC Semibold' if lbl_bold else 'PingFang SC')

        # 右侧数值（用 tab 分隔模拟右对齐）
        val_color = NAVY_RGB if highlight else GRAY_D_RGB
        val_run = p.add_run(value)
        set_run_font(val_run, 14, bold=highlight, color=val_color,
                     font_name='PingFang SC Semibold' if highlight else 'PingFang SC',
                     font_name_east='PingFang SC Semibold' if highlight else 'PingFang SC')

    def render_footer(self, text="— END —"):
        """底部结尾"""
        text = clean_text(text)

        # 灰色分隔线
        line_p = self.doc.add_paragraph()
        line_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        line_p.paragraph_format.space_before = Pt(20)
        line_p.paragraph_format.space_after = Pt(10)
        add_top_bottom_border(line_p, "D2D7DA", "top", width_pt=1)
        run = line_p.add_run(" ")
        set_run_font(run, 2, color=GRAY_L_RGB)

        # 文字
        text_p = self.doc.add_paragraph()
        text_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        text_p.paragraph_format.space_before = Pt(4)
        text_p.paragraph_format.space_after = Pt(20)

        run = text_p.add_run(text)
        set_run_font(run, 10.5, color=GRAY_M_RGB,
                     font_name='PingFang SC', font_name_east='PingFang SC')

    def add_spacer(self, pt=12):
        """添加空白间距"""
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(pt)
        run = p.add_run(" ")
        set_run_font(run, 2)

    def save(self, path=None):
        """保存 Word 文件"""
        save_path = path or self.output_path
        if not save_path:
            raise ValueError("No output path specified")
        self.doc.save(save_path)
        print(f"✅ Word saved: {save_path}")
        return save_path
