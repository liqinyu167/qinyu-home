# AIGC 导航生态树更新候选 2026-05-17 20:33

## 摘要

- Grok 原始输出：`/home/ubuntu/qinyu-home/.hermes/curation/20260517-2032-ecosystem-grok-raw.json`
- 标准化候选 JSON：`/home/ubuntu/qinyu-home/.hermes/curation/20260517-2033-ecosystem-proposal.json`
- 建议新增：10
- 已剔除 Grok 重复建议：`veo`, `imagen`（站内已存在）
- 状态：仅 proposal，未写入 `data/sites.json`，未部署。


## 生态树视角

### chatgpt
- 已有下游：['sora', 'openai-api', 'codex']

- 建议补充：`gpt-image` GPT Image / DALL·E，upstream=['chatgpt', 'openai-api']，parent updates=['chatgpt', 'openai-api']

- 建议补充：`whisper` Whisper，upstream=['openai-api', 'chatgpt']，parent updates=['openai-api', 'chatgpt']

### gemini
- 已有下游：['aistudio', 'flow', 'notebooklm', 'gemini-api']

- 建议补充：暂无

### claude
- 已有下游：['anthropic-api', 'claude-design']

- 建议补充：`claude-code` Claude Code，upstream=['claude', 'anthropic-api']，parent updates=['claude', 'anthropic-api']

### grok
- 已有下游：['aurora', 'grok-api']

- 建议补充：`grok-imagine` Grok Imagine，upstream=['grok', 'aurora']，parent updates=['grok', 'aurora', 'grok-api']

### doubao
- 已有下游：['jimeng', 'coze', 'ark']

- 建议补充：`seedance` Seedance，upstream=['doubao', 'jimeng']，parent updates=['jimeng', 'doubao']

### jimeng
- 已有下游：无/新塔尖

- 建议补充：暂无

### runway
- 已有下游：无/新塔尖

- 建议补充：`runway` Runway，upstream=[]，parent updates=[]

### midjourney
- 已有下游：无/新塔尖

- 建议补充：`midjourney` Midjourney，upstream=[]，parent updates=[]


## 建议新增明细

### GPT Image / DALL·E (`gpt-image`)
- URL: https://openai.com/dall-e-3
- 所属塔尖: chatgpt
- primarySection: `image-gen`；sections=['image-gen']
- upstream: ['chatgpt', 'openai-api']
- 需要更新父节点 downstream/products: ['chatgpt', 'openai-api']
- 能力: ['image-gen']
- 标签: ['订阅制', 'API', '图像生成', 'OpenAI', '子站']
- 加入理由: OpenAI/ChatGPT 生态下的核心图像生成能力，补齐 ChatGPT 金字塔中图像生成节点。
- 注意: Grok 给了 official-labs secondary，已按规则移除；不作为塔尖。

### Whisper (`whisper`)
- URL: https://openai.com/research/whisper
- 所属塔尖: chatgpt
- primarySection: `audio-gen`；sections=['audio-gen', 'compute-api']
- upstream: ['openai-api', 'chatgpt']
- 需要更新父节点 downstream/products: ['openai-api', 'chatgpt']
- 能力: ['audio-gen']
- 标签: ['开源', 'API', '音频生成', 'OpenAI', '模型']
- 加入理由: OpenAI 语音识别/转写基础模型，作为 OpenAI API 生态下游补齐音频侧能力。
- 注意: 更偏 STT/模型能力，是否放 audio-gen 需确认。

### Claude Code (`claude-code`)
- URL: https://www.anthropic.com/claude-code
- 所属塔尖: claude
- primarySection: `code-dev`；sections=['code-dev']
- upstream: ['claude', 'anthropic-api']
- 需要更新父节点 downstream/products: ['claude', 'anthropic-api']
- 能力: ['code']
- 标签: ['订阅制', '编程开发', 'Anthropic', '子站']
- 加入理由: Anthropic/Claude 生态下的官方代码代理工具，补齐 Claude 金字塔的开发工具节点。
- 注意: 当前已有 claude-design，Claude Code 应单独作为 code-dev 下游。

### Grok Imagine (`grok-imagine`)
- URL: https://x.ai/grok
- 所属塔尖: grok
- primarySection: `video-gen`；sections=['video-gen', 'image-gen']
- upstream: ['grok', 'aurora']
- 需要更新父节点 downstream/products: ['grok', 'aurora', 'grok-api']
- 能力: ['image-gen', 'video-gen']
- 标签: ['订阅制', '图像生成', '视频生成', 'xAI', '子站']
- 加入理由: xAI/Grok 生态的图像/视频创作能力，可作为 Aurora 向多模态创作的下游延展。
- 注意: 产品 URL/公开独立入口需人工再核实。

### Seedance (`seedance`)
- URL: https://seed.bytedance.com/
- 所属塔尖: doubao
- primarySection: `video-gen`；sections=['video-gen']
- upstream: ['doubao', 'jimeng']
- 需要更新父节点 downstream/products: ['jimeng', 'doubao']
- 能力: ['video-gen']
- 标签: ['视频生成', '字节跳动', '模型', '子站']
- 加入理由: 字节视频生成模型能力，作为豆包/即梦视觉创作链路的下游/模型节点。
- 注意: 入口 URL 与是否适合导航展示需确认；可能更适合作为即梦能力说明而非独立卡片。

### Runway (`runway`)
- URL: https://runwayml.com/
- 所属塔尖: runway
- primarySection: `video-gen`；sections=['video-gen', 'image-gen']
- upstream: []
- 需要更新父节点 downstream/products: []
- 能力: ['video-gen', 'image-gen']
- 标签: ['免费', '订阅制', '视频生成', '图像生成']
- 加入理由: 独立视频创作塔尖，可与 Sora/Veo/即梦构成视频生成主干竞品。
- 注意: 因为无上游母站，加入后它本身可作为新的塔尖。

### Midjourney (`midjourney`)
- URL: https://www.midjourney.com/
- 所属塔尖: midjourney
- primarySection: `image-gen`；sections=['image-gen']
- upstream: []
- 需要更新父节点 downstream/products: []
- 能力: ['image-gen']
- 标签: ['订阅制', '图像生成', '英文']
- 加入理由: 独立图像生成塔尖，可与 Imagen/GPT Image/即梦/Flux 构成图像生成主干竞品。
- 注意: 加入后它本身可作为新的塔尖。

### Luma Dream Machine (`luma-dream-machine`)
- URL: https://lumalabs.ai/dream-machine
- 所属塔尖: luma
- primarySection: `video-gen`；sections=['video-gen']
- upstream: []
- 需要更新父节点 downstream/products: []
- 能力: ['video-gen']
- 标签: ['免费', '订阅制', '视频生成']
- 加入理由: 独立视频生成工具，可作为 Sora/Veo/Runway/Kling 的同类替代。
- 注意: 非现有塔尖下游，先作为 alternatives。

### Kling AI (`kling`)
- URL: https://klingai.com
- 所属塔尖: kuaishou
- primarySection: `video-gen`；sections=['video-gen', 'image-gen']
- upstream: []
- 需要更新父节点 downstream/products: []
- 能力: ['video-gen', 'image-gen']
- 标签: ['免费', '订阅制', '中文', '视频生成', '快手']
- 加入理由: 快手系视频生成入口，适合补充中文视频生成主干竞品。
- 注意: 不挂到豆包/即梦下游；它是竞品。

### Pika (`pika`)
- URL: https://pika.art
- 所属塔尖: pika
- primarySection: `video-gen`；sections=['video-gen', 'image-gen']
- upstream: []
- 需要更新父节点 downstream/products: []
- 能力: ['video-gen', 'image-gen']
- 标签: ['免费', '订阅制', '视频生成', '英文']
- 加入理由: 短视频特效和图生视频工具，作为视频生成生态的补充/竞品。
- 注意: 非主站下游，作为 alternatives/complements。


## 关系更新原则
- 有 upstream 的节点：同时把该节点补到父节点 `downstream`；如果是官方子产品，再补到父节点 `products`。
- Runway / Midjourney / Luma / Kling / Pika 这类独立产品：不要挂到 OpenAI/Google 等上游，只与 Sora/Veo/即梦等做 `alternatives`。
- `official-labs` 不新增；这批全部按功能分类进入下层。


## 待你确认
1. 是否认可“先补塔尖生态下游，再补独立竞品塔尖”的方向？
2. Seedance / Whisper 这种模型能力是否要做成独立卡片，还是只写进父产品描述？
3. 确认后我再写入 `data/sites.json`、补双向关系和 favicon。
