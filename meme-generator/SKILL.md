---
name: meme-generator
description: Generate memes and viral images using AI image generation tools. Use when user wants to create memes, reaction images, viral content, or funny images. Supports caption-based memes, image remixing with custom text overlays, viral template selection, and style transfer for meme aesthetics. Triggers on requests like "make a meme", "生成表情包", "create meme", "梗图", "表情包生成", or any request involving meme creation.
---

# Meme Generator

## Overview

This skill enables AI agents to generate memes using AI image generation tools. It provides workflows for caption-based memes, image remixing, and viral template customization.

## Quick Start

### Prerequisites

- Use the available AI image generation skills/tools:
  - `antigravity-image-gen` - Google Antigravity API
  - `qwen-image-skill` - Alibaba Qwen image generation
  - `volcengine-ai-image-generation` - ByteDance Volcano Engine

### Basic Workflow

1. **Identify the meme type** the user wants
2. **Select the appropriate generation method**
3. **Generate and deliver** the image

## Meme Types & Generation Methods

### 1. Caption-Based Memes (Classic Format)

Traditional "top text + bottom text" memes.

**Prompt template:**
```
[Scene description], classic meme format, top text: "[upper text]", bottom text: "[lower text]", white Arial text, Impact font style, yellow caption bars, humorous, viral meme aesthetic
```

**Example:**
User wants: "when the code works on first try but you don't know why"

Generate with prompt: "developer celebrating at computer,confused but happy expression, classic meme format, top text: 'WHEN THE CODE', bottom text: 'WORKS ON FIRST TRY', white Arial text, Impact font style, yellow caption bars, funny meme"

### 2. Custom Text Overlay Memes

Text anywhere on the image.

**Prompt template:**
```
[Scene description], meme style, text overlay: "[text]", [position], [font style], viral meme aesthetic
```

### 3. Viral Template Memes

Use popular meme templates by describing them:

**Common templates:**
- Distracted Boyfriend: "man looking at another woman while holding girlfriend's hand, meme format"
- Drake Hotline Bling: "two panels, left: [normal thing], right: [better thing], drake meme format"
- Woman Yelling at Cat: "woman pointing at camera, confused white cat at table, meme format"

### 4. Reaction/Emotional Memes

**Prompt template:**
```
[Character/emotion description], reaction meme face, exaggerated expression, [emotion], meme format, popular meme template style
```

## Best Practices

1. **Be specific with scenes** - Describe what should be in the image
2. **Include "meme format" or "meme style"** - Helps the AI understand the target aesthetic
3. **Use popular meme keywords** - "viral", "classic meme", "reaction image"
4. **Keep text simple** - AI image generators handle short, clear text better
5. **Iterate if needed** - If first attempt isn't right, refine the prompt

## Example Requests

| User Request | Generation Approach |
|--------------|---------------------|
| "帮我做个表情包，关于程序员" | Caption-based: describe programmer scenario + caption |
| "make a meme about AI taking over" | Custom text overlay with robot/AI imagery |
| "生成一个梗图" | Viral template or caption-based depending on context |

## Workflow Decision Tree

```
User wants meme
├── Has specific image in mind → Describe scene + text in prompt
├── Wants classic caption format → Top/bottom text template
├── References viral template → Describe template by name
└── Just says "meme" → Ask for more details or suggest popular formats
```

## Tools Reference

When generating images, use these tools appropriately:

- **For complex scenes**: volcengine-ai-image-generation or qwen-image-skill
- **For simple memes with text**: antigravity-image-gen
- **For style transfer**: qwen-image-skill with style parameters
