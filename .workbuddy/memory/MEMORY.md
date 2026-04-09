# MEMORY.md — 长期记忆

## 工具链
- **CardRenderer v2** (`md_to_image_v2.py`)：750px 宽长图渲染器，Pillow + PingFang SC 字体，Chromatic Silence 设计风格
- **WordRenderer** (`word_renderer.py`)：基于 python-docx 的 Word 渲染器，API 与 CardRenderer v2 完全对应，支持同步输出 .docx
- **wechat-style-writer**：公众号写作 Skill（~/.workbuddy/skills/wechat-style-writer/）
- **gen_ref_diagrams.py**：Pillow 重绘参考图脚本

## 设计规范
- 长图宽度：750px（手机阅读优化）
- 配色：NAVY(#051C2C) / TEAL(#00B2B4) / BODY(#2D2D2D) / 纯白背景
- 字体：PingFang SC（正文 28pt / Semibold 加粗）+ Bricolage Grotesque Bold（英文标题）
- 行高：1.75 倍；段后间距：GAP_S=12 / GAP_M=20 / GAP_L=30
- 插图上的 "kaku" 签名已去掉（2026-04-08）

## 工作流
- 文字草稿 → 确认 → 生成插图 → 双通道渲染（PNG + DOCX）
- 双通道渲染：`render_content(r, w)` 同时输出 CardRenderer 和 WordRenderer

## 已知 Bug 修复
- Unicode 占位符码点错误：`\u334c\u334d` → `\u330c\u330d`（已修复并同步到 skill）

## 用户偏好
- 原图原样贴入，不要 AI 重新演绎
- 沟通简洁高效，由 AI 主导流程
