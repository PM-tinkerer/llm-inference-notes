# -*- coding: utf-8 -*-
"""Regenerate static pages with Python standard library only."""
from pathlib import Path
import json, re, html
ROOT = Path(__file__).resolve().parents[1]
titles = json.loads((ROOT/'content/curriculum.json').read_text())
groups = [(1,'大模型单次推理原理'),(2,'高并发推理与 KV Cache 管理'),(4,'GPU 硬件与推理计算性能'),(7,'大模型推理引擎架构'),(11,'分布式推理与大规模部署'),(15,'推理性能优化与容量规划'),(20,'2026 前沿推理技术'),(23,'生产级推理服务架构')]
available_chapters = {n for n in range(1,25) if (ROOT/f'content/chapter-{n:02}.html').exists()}
count = len(available_chapters)
intros = ['理解一个请求从输入到输出的完整计算过程。','理解一块 GPU 如何组织大量长度各异的请求。','理解有限显存中的 KV 分配、寻址、共享与回收。']
def nav(current):
    out='<a class="nav-home" href="index.html">⌂ 课程总览</a><label class="search-label" for="nav-search">查找章节</label><input type="search" id="nav-search" placeholder="章节名称 / 关键词">'
    for start,group in groups:
        end=next((x[0] for x in groups if x[0]>start),25)
        out+=f'<div class="nav-group"><p>{group}</p>'
        for n in range(start,end):
            out+=f'<a class="chapter-link {"current" if current==n else ""}" {"aria-current=page" if current==n else ""} href="chapter-{n:02}.html"><span>{n:02}</span><span>{html.escape(titles[n-1])}<small>{"已收录" if n in available_chapters else "待学习"}</small></span></a>'
        out+='</div>'
    return out+'<p id="search-empty" hidden>没有匹配章节</p>'
def shell(title,content,current=0,toc=''):
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="大模型推理学习知识库：24章路线，前三章涵盖Transformer、并发调度与KV缓存管理。"><meta name="theme-color" content="#153d35"><title>{title} · 推理手册</title><link rel="stylesheet" href="assets/style.css"><script defer src="assets/app.js"></script></head><body><a class="skip" href="#main">跳到正文</a><header class="topbar"><a class="brand" href="index.html"><span class="brand-icon">推</span><span>推理手册<small>LLM INFERENCE FIELD NOTES</small></span></a><div class="top-actions"><span class="edition">学习笔记 · VOL. 01</span><button id="menu-toggle" aria-controls="sidebar" aria-expanded="false">课程目录</button><button id="print" class="secondary">打印 / PDF</button></div></header><div class="layout"><aside class="sidebar" id="sidebar" aria-label="课程目录"><div class="progress-label"><b>课程收录</b><span>{count:02} / 24</span></div><div class="progress"><i style="width:{count/24*100:.3f}%"></i></div>{nav(current)}</aside><main id="main" tabindex="-1">{content}<footer>专业知识海洋 · 大模型推理技术体系<br>基于已完成的前三章学习记录整理 · 技术核对 2026-10-14<br><a href="index.html#sources">资料与编辑说明</a></footer></main><aside class="toc" aria-label="本页导航">{toc}</aside></div></body></html>'''
for n,title in enumerate(titles,1):
    path=ROOT/f'content/chapter-{n:02}.html'
    available=path.exists()
    # Adding chapters is an explicit editorial action: a content file is required.
    body=path.read_text() if available else '<div class="pending"><span class="pending-number">'+f'{n:02}'+'</span><h2>这一章，留给下一次探索。</h2><p>待学习 · 当前仅保留课程目录。</p><p>确认完成本章学习后，再补充正文、图解与复习记录。</p><a class="button" href="index.html#roadmap">返回完整课程路线 →</a></div>'
    body=re.sub(r'<figure><img src="([^"]+)"([^>]*)>', lambda m: f'<figure><a href="{m[1]}" target="_blank" rel="noopener" title="打开原尺寸技术图"><img src="{m[1]}"{m[2]}></a>',body)
    body=body.replace('</figcaption>', ' · 点击图可放大</figcaption>')
    sections=re.findall(r'<section id="([^"]+)"><h2>(.*?)</h2>',body)
    toc='<p class="eyebrow">本章导航</p>'+''.join(f'<a href="#{id}">{text}</a>' for id,text in sections)
    lead=intros[n-1] if n<=3 else '课程路线 / 待学习'
    content=f'<div class="breadcrumb"><a href="index.html">课程总览</a> / 第 {n:02} 章</div><header class="chapter-head"><span class="eyebrow">CHAPTER {n:02} <span class="badge">{"已学习 · 已收录" if available else "待学习"}</span></span><h1>{title}</h1><p>{lead}</p></header><article>{body}</article><nav class="page-turn" aria-label="章节翻页">'
    content+=f'<a href="chapter-{n-1:02}.html">← 第 {n-1} 章</a>' if n>1 else '<a href="index.html">← 课程总览</a>'
    content+=f'<a href="chapter-{n+1:02}.html">第 {n+1} 章 →</a>' if n<24 else '<a href="index.html">课程总览 →</a>'
    content+='</nav>'
    (ROOT/f'chapter-{n:02}.html').write_text(shell(title,content,n,toc))
roadmap=''
for j,(start,group) in enumerate(groups,1):
    end=next((x[0] for x in groups if x[0]>start),25)
    roadmap+=f'<div class="roadmap-group"><div class="part">PART {j:02}</div><h3>{group}</h3><div>'
    for n in range(start,end):
        roadmap+=f'<a href="chapter-{n:02}.html"><span class="chapter-num">{n:02}</span><span>{titles[n-1]}</span><small>{"已收录 ↗" if n in available_chapters else "待学习"}</small></a>'
    roadmap+='</div></div>'
home='''<section class="hero"><div class="hero-copy"><span class="eyebrow">从一个 TOKEN，到一套推理系统</span><h1>看懂大模型，<br>如何一步步<br><em>生成答案。</em></h1><p>把计算、调度与显存连成一条线。<br>一份持续生长的中文推理技术学习手册。</p><a class="button" href="chapter-01.html">从第一章开始阅读 <span>↗</span></a><a class="text-link" href="#roadmap">浏览课程路线 ↓</a></div><div class="hero-visual"><div class="visual-label">THE INFERENCE LOOP <span>01—03</span></div><div class="token-line"><span>输入</span><i>→</i><span>Token</span><i>→</i><span>向量</span></div><div class="engine-box"><span class="eyebrow">01 / COMPUTE</span><h3>Transformer</h3><div><span>Prefill</span><b>→</b><span>Decode ↻</span></div></div><div class="connector">↓ 读写历史 KV</div><div class="cache-box"><span class="eyebrow">03 / MEMORY</span><h3>KV Cache</h3><div class="mini-blocks"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div><p>按块存储 · 按表寻址</p></div><div class="scheduler-tag">02 / Scheduler · 决定每一轮服务谁</div></div></section><div class="stats"><div><b>24</b><span>核心章节</span></div><div><b>08</b><span>学习篇章</span></div><div><b>03</b><span>已完成并收录</span></div><p>先理解单次推理，<br>再走向高并发 Serving。</p></div><section id="start"><div class="section-heading"><div><span class="eyebrow">YOUR FIRST THREE CHAPTERS</span><h2>三步，建立推理全局观</h2></div><span class="muted">原理 → 调度 → 内存</span></div><div class="chapter-cards"><a href="chapter-01.html"><span class="card-number">01 / 计算</span><h3>一个答案<br>是怎样生成的？</h3><p>Transformer · Attention<br>Prefill / Decode · KV Cache</p><span class="card-link">进入第一章 ↗</span></a><a href="chapter-02.html"><span class="card-number">02 / 调度</span><h3>一块 GPU<br>如何服务多人？</h3><p>Batching · Scheduler<br>Continuous / Chunked Prefill</p><span class="card-link">进入第二章 ↗</span></a><a href="chapter-03.html"><span class="card-number">03 / 内存</span><h3>不断增长的历史，<br>应该存在哪里？</h3><p>PagedAttention · KV Block<br>Block Table · Prefix Cache</p><span class="card-link">进入第三章 ↗</span></a></div></section><section id="roadmap"><div class="section-heading"><div><span class="eyebrow">THE COMPLETE LEARNING PATH</span><h2>完整课程路线</h2></div><span class="badge">3 / 24 已收录</span></div><p class="muted">沿用原对话的 8 篇、24 章规划。待学习章节仅保留标题；确认学完后逐章更新。</p>'''+roadmap+'''</section><section id="sources" class="sources"><span class="eyebrow">SOURCES & EDITORIAL NOTES</span><h2>学习记录与技术依据</h2><p>正文基于原会话《大模型推理体系》前三章重编，保留厨房、餐厅与酒店类比。新增 SVG 为概念示意；交互例子是教学计算，不是性能基准。技术口径以常见 Decoder-only、完整注意力、常规自回归解码为主。</p><ul><li><a href="https://arxiv.org/abs/1706.03762">Attention Is All You Need</a>：缩放点积注意力的基础。</li><li><a href="https://arxiv.org/abs/2309.06180">PagedAttention / vLLM 论文</a>：块式 KV 管理与共享设计。</li><li><a href="https://docs.vllm.ai/en/stable/configuration/optimization/">vLLM Optimization and Tuning</a>：调度、抢占与 Chunked Prefill 的性能权衡。</li><li><a href="https://docs.vllm.ai/en/stable/features/automatic_prefix_caching/">vLLM Automatic Prefix Caching</a>：前缀复用的收益与限制。</li><li><a href="https://github.com/vllm-project/vllm/blob/main/docs/design/prefix_caching.md">vLLM Prefix Cache Design</a>：块哈希、引用与生命周期。</li></ul><p>核对日期：2026-10-14。框架文档会更新；站内不把默认配置或特定硬件吞吐当作通用结论。原配图在第一章附录保留，易误读表述已加校注。</p><a href="assets/inference-a4.svg">A4 单次推理复习图 ↗</a></section>'''
home=home.replace('<b>03</b><span>已完成并收录</span>',f'<b>{count:02}</b><span>已完成并收录</span>').replace('3 / 24 已收录',f'{count} / 24 已收录')
(ROOT/'index.html').write_text(shell('大模型推理技术知识库',home,toc='<p class="eyebrow">本页导航</p><a href="#start">开始阅读</a><a href="#roadmap">24 章路线</a><a href="#sources">参考资料</a>'))
print('Generated index + 24 chapter pages.')
