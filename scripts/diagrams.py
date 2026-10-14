# -*- coding: utf-8 -*-
from pathlib import Path
from html import escape
P=Path(__file__).resolve().parents[1]/'assets'
def text(x,y,s,size=15,color='#193f36'):
 return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}">{escape(s)}</text>'
def box(x,y,w,h,title,sub='',fill='#fff'):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{fill}" stroke="#b4c6b2"/>'+text(x+15,y+29,title,17)+text(x+15,y+53,sub,12,'#61756c')
def arrow(x,y,xx,yy):
 return f'<path d="M{x} {y} L{xx} {yy}" stroke="#7d987a" stroke-width="2" fill="none" marker-end="url(#a)"/>'
def save(name,height,title,desc,body):
 (P/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 {height}" role="img" aria-labelledby="title desc"><title id="title">{title}</title><desc id="desc">{desc}</desc><defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10" fill="none" stroke="#7d987a"/></marker></defs><g font-family="PingFang SC,Microsoft YaHei,sans-serif">{body}</g></svg>')
s=text(15,25,'01 / 从输入到首 Token，再进入生成循环',17)
s+=box(15,50,195,75,'Tokenizer → Embedding','文本 → ID → 向量')+arrow(210,88,245,88)+box(250,50,210,75,'Prefill · 处理输入','每层建立输入位置的 KV')+arrow(460,88,495,88)+box(500,50,205,75,'LM Head → 采样','得到第一个输出 Token', '#f8ead8')
s+=arrow(603,125,603,177)+box(430,185,275,80,'Decode · 处理刚生成的 Token','每层计算新 Q/K/V，读取历史 KV')+arrow(430,224,390,224)+box(140,185,245,80,'LM Head → 下一次采样','继续生成，或满足停止条件')
s+=f'<path d="M260 265 V300 H650 V265" fill="none" stroke="#7d987a" stroke-width="2" marker-end="url(#a)"/>'+text(335,324,'未结束：回送刚生成的 Token',13)
s+=box(15,360,690,72,'每层 KV Cache：保留历史 K/V，按处理进度追加','Decode 不重算历史位置的 FFN；仍需访问历史 K/V。','#e4ecdf')
save('pipeline.svg',452,'Prefill 与 Decode 流程','先处理已知输入，采样首Token；后续循环处理刚采样的Token，并追加KV。',s)
s=text(15,25,'02 / 连续批处理：在轮次边界重新组批',17)
for row,(tokens,note) in enumerate([(['A','B','C'],'B 完成 → D 加入'),(['A','C','D'],'C 完成 → E 加入'),(['A','D','E'],'A 完成 → F 加入'),(['D','E','F'],'下一轮继续调度')]):
 y=55+row*68;s+=text(15,y+29,f'轮次 {row+1}',13)
 for j,t in enumerate(tokens):s+=box(100+j*112,y,96,52,t,'', '#e2ebde' if t in ['A','B','C'] else '#f8ead8')
 s+=text(460,y+30,note,14)
s+=text(15,355,'示意前提：仅画 Decode 槽位；每个请求已完成 Prefill。',13)
save('batching.svg',380,'连续批处理轮次','第一轮ABC，第二轮ACD，第三轮ADE，第四轮DEF。',s)
s=text(15,25,'03 / Block Table：逻辑位置 → 物理地址',17)
for j,(phy,subtitle) in enumerate([(7,'Token 1—16 · 16/16'),(2,'Token 17—32 · 16/16'),(11,'Token 33—40 · 8/16')]):
 y=60+j*98;s+=box(15,y,220,72,f'逻辑块 {j}',subtitle)+arrow(235,y+35,290,y+35)+box(295,y,110,72,f'{j} → {phy}','映射表','#f8ead8')+arrow(405,y+35,465,y+35)+box(470,y,235,72,f'物理块 {phy}', '保存各层对应位置的 K/V','#e2ebde')
s+=text(15,390,'第 20 个 Token：i = 19 → 逻辑块 1 → 物理块 2 → 偏移 3',15)
save('blocks.svg',425,'KV块表映射','逻辑块0映射7，1映射2，2映射11；块大小16。',s)
s=text(15,25,'04 / 相同前缀共享，后续内容独立',17)+box(15,130,245,90,'共享前缀 KV','相同 Token 与兼容上下文','#e2ebde')
s+=arrow(260,157,370,87)+arrow(260,194,370,274)+box(380,50,325,85,'请求 A · 私有后缀','共享前缀 → 问题 A → 生成 A','#f8ead8')+box(380,235,325,85,'请求 B · 私有后缀','共享前缀 → 问题 B → 生成 B','#f8ead8')
s+=text(15,369,'A 结束：释放 A 的引用；B 仍在使用时，公共块不可被覆盖。',14)
save('prefix.svg',400,'前缀KV共享','请求A和B读取共享前缀KV，分别追加自己的后缀。',s)
# Revise the editable A4 illustration already in this workspace; original PNG remains intact.
p=P/'inference-a4.svg';s=p.read_text()
s=s.replace('L_KV = L_input + L_generated','L_KV ≈ L_input + L_generated')
s=s.replace('总耗时 ≈ TTFT + 输出 token 数 × TPOT','总耗时 ≈ TTFT + (输出数 − 1) × TPOT')
s=s.replace('RoPE：注入相对位置','RoPE：各层旋转 Q、K')
s=s.replace('生成速度（TPOT）越来越受 KV 读取和显存带宽限制。','小批量 Decode 常受带宽限制；瓶颈随批量和模型变化。')
s=s.replace('避免互相抢资源','隔离计算，增加 KV 传输')
s=s.replace('最后一层 hidden state → LM Head → logits → Sampling','Prefill 末位 → LM Head → 采样首 Token；随后循环 Decode')
s=s.replace('每一层追加 K_t 和 V_t','已处理的位置才写入 K/V')
s=s.replace('class="title" font-size="77" fill="#fff"','class="title" font-size="77" style="fill:#fff"')
s=s.replace('class="title" font-size="30" fill="#fff"','class="title" font-size="30" style="fill:#fff"')
p.write_text(s)
print('Four SVG diagrams generated; A4 corrected.')
