# AIGC 导航网站入口更新候选 2026-05-17 20:46

## 这版采用的新规则
- 模型/能力节点先不做独立卡片。
- 只看能打开使用的网站/产品入口。
- 独立工具如果有自研模型，可作为 `official-labs` 候选；没有则进功能分类或 misc。
- 仍然只是候选，未写入 `data/sites.json`，未部署。


- Grok 原始评估：`/home/ubuntu/qinyu-home/.hermes/curation/20260517-2045-product-entry-grok-raw.json`
- 标准化候选 JSON：`/home/ubuntu/qinyu-home/.hermes/curation/20260517-2046-product-entry-proposal.json`
- 本轮建议新增网站入口：9


## 建议进入 `official-labs` 的独立模型/工具站候选

### Runway (`runway`)
- URL: https://runwayml.com/
- 自研模型判断: yes — Gen-3, Gen-4 video models developed in-house; research-focused company building their own generative video and image tech.
- 建议 primarySection: `official-labs`；功能分类: `video-gen`；sections=['official-labs', 'video-gen', 'image-gen']
- capabilities: ['video-gen']
- alternatives: ['sora', 'veo']
- 加入理由: Popular independent AI video platform with direct web/app access and self-developed core models.

### Midjourney (`midjourney`)
- URL: https://www.midjourney.com/
- 自研模型判断: yes — Proprietary image generation models (V6, V7 etc.) built by their research lab.
- 建议 primarySection: `official-labs`；功能分类: `image-gen`；sections=['official-labs', 'image-gen']
- capabilities: ['image-gen']
- alternatives: ['jimeng']
- 加入理由: Major standalone image gen product with web access and self-funded independent models.

### Luma Dream Machine (`luma-dream-machine`)
- URL: https://dream-machine.lumalabs.ai/
- 自研模型判断: yes — Dream Machine video model developed by Luma AI.
- 建议 primarySection: `official-labs`；功能分类: `video-gen`；sections=['official-labs', 'video-gen', 'image-gen']
- capabilities: ['video-gen']
- alternatives: ['sora']
- 加入理由: Direct product entry for Luma's AI video generation tools.

### Pika (`pika`)
- URL: https://pika.art/
- 自研模型判断: yes — Pikaformance and other video models developed in-house.
- 建议 primarySection: `official-labs`；功能分类: `video-gen`；sections=['official-labs', 'video-gen']
- capabilities: ['video-gen']
- alternatives: []
- 加入理由: Independent video creation platform with direct access.

### Ideogram (`ideogram`)
- URL: https://ideogram.ai/
- 自研模型判断: yes — Ideogram text-to-image models (v2, v3) developed by the company.
- 建议 primarySection: `official-labs`；功能分类: `image-gen`；sections=['official-labs', 'image-gen']
- capabilities: ['image-gen']
- alternatives: ['jimeng']
- 加入理由: Strong independent image gen product focused on text rendering.

### Black Forest Labs FLUX (`flux`)
- URL: https://bfl.ai/
- 自研模型判断: yes — FLUX.1 / FLUX.2 family of models developed by BFL.
- 建议 primarySection: `official-labs`；功能分类: `image-gen`；sections=['official-labs', 'image-gen']
- capabilities: ['image-gen', 'code']
- alternatives: []
- 加入理由: Direct access via playground/API for their advanced open and pro models.

### Suno (`suno`)
- URL: https://suno.com/
- 自研模型判断: yes — Proprietary AI music generation models.
- 建议 primarySection: `official-labs`；功能分类: `audio-gen`；sections=['official-labs', 'audio-gen']
- capabilities: ['audio-gen']
- alternatives: ['musicfx']
- 加入理由: Leading independent AI music creation platform.

### ElevenLabs (`elevenlabs`)
- URL: https://elevenlabs.io/
- 自研模型判断: yes — Voice synthesis and audio models developed in-house.
- 建议 primarySection: `official-labs`；功能分类: `audio-gen`；sections=['official-labs', 'audio-gen']
- capabilities: ['audio-gen', 'voice']
- alternatives: []
- 加入理由: Premier AI voice platform with direct product access and self-developed tech.


## 不进 `official-labs`，按功能分类加入

### Kling AI (`kling`)
- URL: https://kling.ai/
- 原因: 虽有产品入口，但不作为 official-labs 候选；建议 primarySection=`video-gen`
- 自研模型判断: yes — Kling video generation models developed by Kuaishou.
- sections=['video-gen', 'image-gen']
- alternatives: ['sora', 'veo']


## 本轮明确暂不处理
- Whisper：模型/能力节点，先不做独立卡片。
- Seedance：模型/能力节点，先不做独立卡片；后续可放进即梦/豆包描述或模型层设计。
- 其它纯模型页/论文页/benchmark 页：暂缓。


## 待你确认
如果你认可这版规则，我建议优先写入这些“网站入口”：Runway、Midjourney、Luma Dream Machine、Pika、Ideogram、FLUX、Suno、ElevenLabs。Kling AI 我放在功能分类候选，因为它虽是快手自研模型，但更像快手系产品入口，是否进 `official-labs` 你来定。
