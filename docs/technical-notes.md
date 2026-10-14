# 技术核对与编辑记录

核对日期：2026-10-14。

1. Prefill 最后位置的 logits 用于采样首个输出；后续 Decode 处理刚采样的位置。输出 G 个 Token 后、末 Token 未回送时，缓存通常为 T + G − 1，而不是无条件等于 T + G。
2. Decode 新位置仍计算 Q/K/V、Attention、FFN；历史 Q 不需复用，历史 K/V 需读取。RoPE 通常作用于各层 Q/K，不是简单的 Embedding 相加。
3. Prefill 并行受到因果掩码约束；层与层仍有依赖。标准稠密 Prefill 注意力算术量关于长度为二次，KV 缓存为线性；这些不是全部模型运算的复杂度表达式。
4. KV 公式使用 KV 头数而非一律 Query 头数。固定 80 层、8 KV 头、128 维、BF16，每 Token 327,680 字节（320 KiB），10,000 Token 为 3.0517578125 GiB。本文不用含混的“10K”替代 10,000 或 10,240。
5. KV 公式不含模型权重、激活、工作区、元数据、分块余量、共享与复制；不是所有架构通用，更不是 GPU 服务容量保证。
6. 本轮 Token 预算与已驻留 KV 总量分开解释。常规解码每轮每请求一个新位置；连续批处理在请求间并行，不消除单请求依赖。
7. PagedAttention 为 KV 分块组织与 Kernel 访问设计；不等于 OS 自动换页，不自动减少完整注意力的数学工作量。现代 GPU 分配器未必符合简单酒店连续分配模型。
8. Block Size 16、40 个位置需要 3 块，分配 48，尾空 8。第 20 个 Token 零基下标为 19，逻辑块 1、偏移 3，映射表 [7,2,11] 对应物理块 2。
9. Prefix Cache 需要相同前缀与兼容上下文，语义相似不够；主要减少重复 Prefill，不是答案缓存。空闲引用与缓存数据保留是不同状态。
10. TPOT 定义为首个输出之后的平均间隔，N_out > 1；总时长近似 TTFT + (N_out − 1) × TPOT。排队与网络计时边界必须一致。
11. Little 定律用于稳态长期平均，不能把在途请求数直接当作 GPU Batch Size，也不能直接推出 GPU 数量。
12. 原 PNG 含“仅生成 Q”等简化，正文附校注。A4 SVG 修正缓存长度近似与耗时公式，但仍为概念复习图，不是特定实现结构图。

依据：

- https://arxiv.org/abs/1706.03762
- https://arxiv.org/abs/2309.06180
- https://docs.vllm.ai/en/stable/configuration/optimization/
- https://docs.vllm.ai/en/stable/features/automatic_prefix_caching/
- https://github.com/vllm-project/vllm/blob/main/docs/design/prefix_caching.md

官方文档可能随版本变化；本文没有承诺具体版本默认值，也未使用论文中的吞吐倍数作为普遍收益。
