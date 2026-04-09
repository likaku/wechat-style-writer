#!/usr/bin/env python3
"""
零售行业变革 — 长图 Poster + Word 文档同步渲染
文章：饺子馆的 Skill，和零售业的下一个二十年
输出：retail_poster.png + retail_poster.docx
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from md_to_image_v2 import *
from word_renderer import WordRenderer

# ═══════════════════════════════════════════════════════════════════════════════
#  插图路径
# ═══════════════════════════════════════════════════════════════════════════════
IMG_COVER = os.path.join(IMG_DIR, "Editorial_cartoon__medieval_fa_2026-04-08T11-17-30.png")  # 封面：饺子馆 + Skill
IMG1 = os.path.join(IMG_DIR, "Editorial_cartoon__medieval_fa_2026-04-08T11-17-40.png")       # 购物实验：混乱 vs 一句话
IMG2 = os.path.join(IMG_DIR, "Editorial_cartoon__medieval_fa_2026-04-08T11-17-45.png")       # 零售四阶段
IMG3 = os.path.join(IMG_DIR, "Editorial_cartoon__medieval_fa_2026-04-08T11-17-37.png")       # 人货场重构
IMG4 = os.path.join(IMG_DIR, "Editorial_cartoon__medieval_fa_2026-04-08T11-17-50.png")       # 企业八大启示
IMG5 = os.path.join(IMG_DIR, "Editorial_cartoon__medieval_fa_2026-04-08T11-17-52.png")       # 结尾：饺子馆在未来城市

# 参考图（用户原图）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REF_STAGES = os.path.join(BASE_DIR, "ref_retail_stages.png")      # 零售四阶段流程图
REF_FRAMEWORK = os.path.join(BASE_DIR, "ref_ai_framework.png")    # AI 八大启示框架图


# ═══════════════════════════════════════════════════════════════════════════════
#  内容渲染函数（同时渲染 PNG 长图 + Word 文档）
# ═══════════════════════════════════════════════════════════════════════════════

def render_content(r, w):
    """
    双通道渲染：r=CardRenderer (PNG), w=WordRenderer (DOCX)
    同一份内容，同步输出两种格式
    """

    # ═══════════════════════════════════════════════════════════════════
    #  封面
    # ═══════════════════════════════════════════════════════════════════
    r.render_h1("饺子馆的 Skill")
    w.render_h1("饺子馆的 Skill")

    r.render_body("**和零售业的下一个二十年**")
    w.render_body("**和零售业的下一个二十年**")

    r.y += 4
    w.add_spacer(4)

    r.render_body(
        "四月七日深夜十一点五十六分，一个叫金谷园饺子馆的公众号推送了一条消息。"
        "正文开头写着：正常每年 4 条的推送规律，今天打乱了节奏。"
    )
    w.render_body(
        "四月七日深夜十一点五十六分，一个叫金谷园饺子馆的公众号推送了一条消息。"
        "正文开头写着：正常每年 4 条的推送规律，今天打乱了节奏。"
    )

    r.render_body(
        "这家以手工大馅鲅鱼饺子闻名的北京餐厅，发布了自己的 AI Skill。"
        "不是 App。不是小程序。是一个可以被任何 AI 助手调用的 Skill。"
    )
    w.render_body(
        "这家以手工大馅鲅鱼饺子闻名的北京餐厅，发布了自己的 AI Skill。"
        "不是 App。不是小程序。是一个可以被任何 AI 助手调用的 Skill。"
    )

    r.render_callout(
        "先记住一条，金谷园是做饺子的，无他。"
        "但是，餐厅面向 AI 的信息接口也会成为必要的基础设施。"
    )
    w.render_callout(
        "先记住一条，金谷园是做饺子的，无他。"
        "但是，餐厅面向 AI 的信息接口也会成为必要的基础设施。"
    )

    r.render_body(
        "一家饺子馆，正在为一个它不完全理解的未来下注。"
        "它下注的逻辑很朴素：如果明天所有人都通过 AI 助手来决定去哪吃饭，"
        "那没有 Skill 的餐厅，就像没有电话的餐厅。"
    )
    w.render_body(
        "一家饺子馆，正在为一个它不完全理解的未来下注。"
        "它下注的逻辑很朴素：如果明天所有人都通过 AI 助手来决定去哪吃饭，"
        "那没有 Skill 的餐厅，就像没有电话的餐厅。"
    )

    r.render_body("这不是科幻。这是 2026 年 4 月 8 日正在发生的事。")
    w.render_body("这不是科幻。这是 2026 年 4 月 8 日正在发生的事。")

    # 封面图
    r.render_image(IMG_COVER, caption="当一家饺子馆开始为 AI 写接口")
    w.render_image(IMG_COVER, caption="当一家饺子馆开始为 AI 写接口")

    r.render_separator()
    w.render_separator()

    # ═══════════════════════════════════════════════════════════════════
    #  第一章：一次购物实验
    # ═══════════════════════════════════════════════════════════════════
    r.render_h2(1, "一次购物实验")
    w.render_h2(1, "一次购物实验")

    r.render_body(
        "就在金谷园发布 Skill 的同一周，淘宝桌面客户端更新到了 2.5 版本，"
        "首次开放了 MCP 协议的 AI 工具支持。"
        "简单说，你的 AI Agent 现在可以直接在淘宝上帮你买东西了。"
    )
    w.render_body(
        "就在金谷园发布 Skill 的同一周，淘宝桌面客户端更新到了 2.5 版本，"
        "首次开放了 MCP 协议的 AI 工具支持。"
        "简单说，你的 AI Agent 现在可以直接在淘宝上帮你买东西了。"
    )

    r.render_body("我第一时间做了一个实验。")
    w.render_body("我第一时间做了一个实验。")

    r.render_body(
        "需求很简单——买一个洗车水枪。但条件很刁钻："
        "**要质量好，要能适配我的车型，要能接上我现有的洗车设备，"
        "店铺信誉要过关，价格要有竞争力，最好还能发顺丰。**"
    )
    w.render_body(
        "需求很简单——买一个洗车水枪。但条件很刁钻："
        "**要质量好，要能适配我的车型，要能接上我现有的洗车设备，"
        "店铺信誉要过关，价格要有竞争力，最好还能发顺丰。**"
    )

    r.render_body(
        "如果是传统方式，这大概需要：打开淘宝、搜索、翻五六页、"
        "一个一个点进去看参数、对比评价、问客服能不能发顺丰、再对比价格、下单。"
        "整个过程少说二十分钟，多则一个小时。"
    )
    w.render_body(
        "如果是传统方式，这大概需要：打开淘宝、搜索、翻五六页、"
        "一个一个点进去看参数、对比评价、问客服能不能发顺丰、再对比价格、下单。"
        "整个过程少说二十分钟，多则一个小时。"
    )

    r.render_body("我对 Agent 说了一句话。")
    w.render_body("我对 Agent 说了一句话。")

    r.render_body(
        "它搜索了。它筛选了。它比对了参数、评价、店铺评分、物流选项。"
        "然后它告诉我：这一款，满足你所有条件。要下单吗？"
    )
    w.render_body(
        "它搜索了。它筛选了。它比对了参数、评价、店铺评分、物流选项。"
        "然后它告诉我：这一款，满足你所有条件。要下单吗？"
    )

    r.render_callout("整个过程不到两分钟。")
    w.render_callout("整个过程不到两分钟。")

    r.render_body(
        "这不是效率提升。这是交互范式的替换。"
        "我没有逛淘宝。我甚至没有打开淘宝的界面。"
        "我只是说了我想要什么，然后得到了我想要的。"
    )
    w.render_body(
        "这不是效率提升。这是交互范式的替换。"
        "我没有逛淘宝。我甚至没有打开淘宝的界面。"
        "我只是说了我想要什么，然后得到了我想要的。"
    )

    r.render_body(
        "跟我想的一样，零售行业的\u201c场\u201d，正在被重新定义。只是来得更快一些。"
    )
    w.render_body(
        "跟我想的一样，零售行业的\u201c场\u201d，正在被重新定义。只是来得更快一些。"
    )

    r.render_image(IMG1, caption="六家店的混乱 vs 一句话搞定")
    w.render_image(IMG1, caption="六家店的混乱 vs 一句话搞定")

    r.render_separator()
    w.render_separator()

    # ═══════════════════════════════════════════════════════════════════
    #  第二章：是谁在推动变革？
    # ═══════════════════════════════════════════════════════════════════
    r.render_h2(2, "是谁在推动变革？")
    w.render_h2(2, "是谁在推动变革？")

    r.render_body(
        "中国零售业在过去二十年经历了四次范式转换。"
        "每一次的推动力，都不是零售业自己——**是技术。**"
    )
    w.render_body(
        "中国零售业在过去二十年经历了四次范式转换。"
        "每一次的推动力，都不是零售业自己——**是技术。**"
    )

    r.render_h3("线下零售（2003 年以前）")
    w.render_h3("线下零售（2003 年以前）")

    r.render_body(
        "国有百货垄断、物理购物文化、有限的竞争。"
        "这个阶段的终结者不是更好的百货商场，而是 3G 网络和互联网的普及。"
        "到 2003 年，20% 的线下门店已经关闭。"
    )
    w.render_body(
        "国有百货垄断、物理购物文化、有限的竞争。"
        "这个阶段的终结者不是更好的百货商场，而是 3G 网络和互联网的普及。"
        "到 2003 年，20% 的线下门店已经关闭。"
    )

    r.render_h3("货架电商（2003-2015）")
    w.render_h3("货架电商（2003-2015）")

    r.render_body(
        "淘宝、京东崛起。支付宝解决了信任问题。年复合增长率达到 47%。"
        "但终结它的也不是更好的电商平台——是 5G 技术催生了短视频文化。"
    )
    w.render_body(
        "淘宝、京东崛起。支付宝解决了信任问题。年复合增长率达到 47%。"
        "但终结它的也不是更好的电商平台——是 5G 技术催生了短视频文化。"
    )

    r.render_h3("兴趣电商（2016 至今）")
    w.render_h3("兴趣电商（2016 至今）")

    r.render_body(
        "抖音、快手、小红书。算法 + 直播重新定义了发现和购买的关系。"
        "2021 年直播电商 GMV 占比 35%，2023 年已有 25% 的交易通过直播完成。"
    )
    w.render_body(
        "抖音、快手、小红书。算法 + 直播重新定义了发现和购买的关系。"
        "2021 年直播电商 GMV 占比 35%，2023 年已有 25% 的交易通过直播完成。"
    )

    r.render_h3("Agentic Commerce（2026 年之后）")
    w.render_h3("Agentic Commerce（2026 年之后）")

    r.render_body(
        "AI 直播成本只有真人的 10%。15-30% 的平台流量份额正在被 Agent 渠道分走。"
        "预计到 2030 年，AI 和 Agent 将重塑全球 80% 的电商价值链。"
    )
    w.render_body(
        "AI 直播成本只有真人的 10%。15-30% 的平台流量份额正在被 Agent 渠道分走。"
        "预计到 2030 年，AI 和 Agent 将重塑全球 80% 的电商价值链。"
    )

    r.render_callout(
        "每一次零售变革，推手都不是零售人自己。"
        "是 3G 催生了电商，是 5G 催生了直播，是 AI 催生了 Agent。"
    )
    w.render_callout(
        "每一次零售变革，推手都不是零售人自己。"
        "是 3G 催生了电商，是 5G 催生了直播，是 AI 催生了 Agent。"
    )

    # 数据展示
    r.y += 6
    w.add_spacer(6)

    data_rows = [
        ('线下零售', '→ 3G 终结', False),
        ('货架电商 CAGR', '47%（2010-2016）', True),
        ('直播电商 GMV 占比', '35%（2021）', True),
        ('Agent 渠道占比', '15-30%（2026）', True),
        ('AI 重塑电商价值链', '80%（2030 预测）', True),
    ]
    for label, value, hl in data_rows:
        r.render_data_row(label, value, highlight=hl)
        w.render_data_row(label, value, highlight=hl)

    r.y += 6
    w.add_spacer(6)

    r.render_image(IMG2, caption="技术驱动零售四阶段演变")
    w.render_image(IMG2, caption="技术驱动零售四阶段演变")

    r.y += 8
    w.add_spacer(8)

    r.render_image(REF_STAGES, caption="零售四阶段演变 — 结构化视图")
    w.render_image(REF_STAGES, caption="零售四阶段演变 — 结构化视图")

    r.render_separator()
    w.render_separator()

    # ═══════════════════════════════════════════════════════════════════
    #  第三章：人货场的第四次重构
    # ═══════════════════════════════════════════════════════════════════
    r.render_h2(3, "人货场的第四次重构")
    w.render_h2(3, "人货场的第四次重构")

    r.render_body(
        "传统零售：**人**到**场**去找**货**。"
        "电商：**人**在**场**里搜索**货**。"
        "兴趣电商：**货**通过**场**找到**人**。"
    )
    w.render_body(
        "传统零售：**人**到**场**去找**货**。"
        "电商：**人**在**场**里搜索**货**。"
        "兴趣电商：**货**通过**场**找到**人**。"
    )

    r.render_callout(
        "Agent 时代：Agent 代替人，直接和货对话。场，从平台变成了协议。"
    )
    w.render_callout(
        "Agent 时代：Agent 代替人，直接和货对话。场，从平台变成了协议。"
    )

    r.render_h3("人：从注意力争夺到 Agent 信任")
    w.render_h3("人：从注意力争夺到 Agent 信任")

    r.render_body(
        "过去品牌在争夺人的注意力——更好的广告、更精准的推荐、更吸引眼球的直播间。"
        "Agent 时代，品牌需要争夺的是 Agent 的信任。"
        "Agent 不会被主播的话术打动。它会看参数、看评价、看价格、看物流。"
        "**产品力回归中心位。**"
    )
    w.render_body(
        "过去品牌在争夺人的注意力——更好的广告、更精准的推荐、更吸引眼球的直播间。"
        "Agent 时代，品牌需要争夺的是 Agent 的信任。"
        "Agent 不会被主播的话术打动。它会看参数、看评价、看价格、看物流。"
        "**产品力回归中心位。**"
    )

    r.render_h3("货：从标准品到超个性化")
    w.render_h3("货：从标准品到超个性化")

    r.render_body(
        "当 Agent 理解用户的所有偏好——车型、设备兼容性、价格敏感度、品牌偏好——"
        "货的匹配精度会提升一个数量级。"
        "当 C2M 被 Agent 驱动，即时研发不再是概念。"
    )
    w.render_body(
        "当 Agent 理解用户的所有偏好——车型、设备兼容性、价格敏感度、品牌偏好——"
        "货的匹配精度会提升一个数量级。"
        "当 C2M 被 Agent 驱动，即时研发不再是概念。"
    )

    r.render_h3("场：从平台到智能接口")
    w.render_h3("场：从平台到智能接口")

    r.render_body(
        "过去的场是淘宝、京东、抖音——巨大的流量池，品牌在池子里花钱买位置。"
        "Agent 时代的场不再是一个你要走进去的地方。"
        "它是一个协议层——品牌把信息、价格、库存、物流封装成 Skill 或 API，"
        "Agent 在需要的时候调用。**就像金谷园饺子馆做的那样。**"
    )
    w.render_body(
        "过去的场是淘宝、京东、抖音——巨大的流量池，品牌在池子里花钱买位置。"
        "Agent 时代的场不再是一个你要走进去的地方。"
        "它是一个协议层——品牌把信息、价格、库存、物流封装成 Skill 或 API，"
        "Agent 在需要的时候调用。**就像金谷园饺子馆做的那样。**"
    )

    r.render_callout(
        "未来的渠道不是一个地方，而是一种能力——"
        "被 Agent 发现、被 Agent 理解、被 Agent 信任的能力。"
    )
    w.render_callout(
        "未来的渠道不是一个地方，而是一种能力——"
        "被 Agent 发现、被 Agent 理解、被 Agent 信任的能力。"
    )

    r.render_image(IMG3, caption="人货场的第四次重构")
    w.render_image(IMG3, caption="人货场的第四次重构")

    r.y += 8
    w.add_spacer(8)

    r.render_image(REF_FRAMEWORK, caption="AI-Driven 零售转型八大启示 — 结构化框架")
    w.render_image(REF_FRAMEWORK, caption="AI-Driven 零售转型八大启示 — 结构化框架")

    r.render_separator()
    w.render_separator()

    # ═══════════════════════════════════════════════════════════════════
    #  第四章：对企业的八个启示
    # ═══════════════════════════════════════════════════════════════════
    r.render_h2(4, "对企业的八个启示")
    w.render_h2(4, "对企业的八个启示")

    items = [
        ('从 SEO 到 GEO', '优化 AI 搜索中的心智占位，让品牌出现在 Agent 的答案里'),
        ('从仪表盘到 Agentic Insights', '用数字孪生模拟和预测 360° 消费者行为，不是月报，是实时'),
        ('即时研发，按需生产', 'Agent 汇聚需求信号，供应链实时响应，大规模定制不再是口号'),
        ('破解 AI 购买的黑箱', '理解 Agent 怎么筛选、怎么评分、怎么推荐，这是全新的学科'),
        ('渠道变成智能接口', '你还需要一个 Skill、一个 API、一个能被 Agent 直接调用的接口'),
        ('为机器设计营销', 'Bot-to-Bot 经济正在形成，产品描述要结构化、参数要标准化'),
        ('仿生组织', 'AI 驱动高频执行，人类主导战略创意，不是裁员，是重新分工'),
        ('认知骨架', 'IT 从数据中台进化为认知骨架——模块化数据 + 可扩展 AI 执行'),
    ]
    for t, d in items:
        bullet_text = f"**{t}**：{d}"
        r.render_bullet(bullet_text)
        w.render_bullet(bullet_text)

    r.y += 4
    w.add_spacer(4)

    r.render_image(IMG4, caption="八个启示——Agent 不是在进攻，它们是在购物")
    w.render_image(IMG4, caption="八个启示——Agent 不是在进攻，它们是在购物")

    r.render_separator()
    w.render_separator()

    # ═══════════════════════════════════════════════════════════════════
    #  第五章：变革的速度
    # ═══════════════════════════════════════════════════════════════════
    r.render_h2(5, "变革的速度")
    w.render_h2(5, "变革的速度")

    r.render_body(
        "App 替代 PC 软件用了 7 年，因为要等 iPhone 普及。"
        "SaaS 替代本地部署用了 15 年，因为要等云计算成熟。"
    )
    w.render_body(
        "App 替代 PC 软件用了 7 年，因为要等 iPhone 普及。"
        "SaaS 替代本地部署用了 15 年，因为要等云计算成熟。"
    )

    r.render_body(
        "Agent 替代 App 需要等什么？"
        "**什么都不需要等。**硬件已经在那里，网络已经在那里，"
        "模型每隔几个月自动升级一次。"
    )
    w.render_body(
        "Agent 替代 App 需要等什么？"
        "**什么都不需要等。**硬件已经在那里，网络已经在那里，"
        "模型每隔几个月自动升级一次。"
    )

    r.y += 6
    w.add_spacer(6)

    speed_data = [
        ('2025 年企业 AI 渗透率', '< 5%', True),
        ('2026 年预测渗透率', '40%', True),
        ('增长倍数', '8× 一年', True),
    ]
    for label, value, hl in speed_data:
        r.render_data_row(label, value, highlight=hl)
        w.render_data_row(label, value, highlight=hl)

    r.y += 6
    w.add_spacer(6)

    r.render_callout(
        "当一家饺子馆都在做 Skill 的时候，这个信号已经够清楚了。"
    )
    w.render_callout(
        "当一家饺子馆都在做 Skill 的时候，这个信号已经够清楚了。"
    )

    r.render_body(
        "金谷园饺子馆的那条公众号推送，到我写这篇文章的时候，已经有 73 个人听过了。"
        "七十三个人。一家饺子馆的一条推送。"
    )
    w.render_body(
        "金谷园饺子馆的那条公众号推送，到我写这篇文章的时候，已经有 73 个人听过了。"
        "七十三个人。一家饺子馆的一条推送。"
    )

    r.render_body(
        "但这七十三个人知道了一件事：未来的顾客不会打开大众点评搜附近饺子。"
        "他们会对 AI 说一句话。而金谷园，已经准备好了回答。"
    )
    w.render_body(
        "但这七十三个人知道了一件事：未来的顾客不会打开大众点评搜附近饺子。"
        "他们会对 AI 说一句话。而金谷园，已经准备好了回答。"
    )

    r.render_callout("你呢？")
    w.render_callout("你呢？")

    # 结尾图
    r.render_image(IMG5, caption="小小饺子馆，连接着整个未来")
    w.render_image(IMG5, caption="小小饺子馆，连接着整个未来")

    # ── Footer ─────────────────────────────────────────────────────────
    r.render_footer("饺子馆的 Skill · 零售业的下一个二十年 · Kaku")
    w.render_footer("饺子馆的 Skill · 零售业的下一个二十年 · Kaku")


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # PNG 长图渲染器
    r = CardRenderer(width=750)

    # Word 文档渲染器
    w = WordRenderer()

    # 双通道同步渲染
    render_content(r, w)

    # ── 保存 PNG ────────────────────────────────────────────────────────
    png_out = os.path.join(base_dir, "retail_poster.png")
    r.save(png_out)

    # ── 保存 Word ───────────────────────────────────────────────────────
    docx_out = os.path.join(base_dir, "retail_poster.docx")
    w.save(docx_out)


if __name__ == "__main__":
    main()
