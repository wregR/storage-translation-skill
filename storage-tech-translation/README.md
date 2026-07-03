---
name: storage-tech-translation
description: Translate, explain, and terminology-check Minecraft storage technology documents, redstone storage discussions, shulker-box storage notes, sorter/splitter/loader documentation, and related English technical community text into natural Chinese. Use for reading storage-tech documents with a local glossary/literature table and optional Minecraft Wiki verification for official game names.
---

# Storage Tech Translation

## Overview

Use this skill to read, translate, and explain Minecraft storage technology material in Chinese. Prioritize storage-tech meaning, mechanism, and community wording over literal English translation.

This skill is intentionally focused on document reading and terminology assistance. Do not use it as a video subtitle workflow.

## Core Workflow

1. Identify the text domain: storage technology, general redstone, computational redstone, official Minecraft content, or mixed.
2. Query the local glossary for storage-tech terms, abbreviations, slang, design names, and community-specific wording.
3. Use Minecraft Wiki lookup only for official game terms such as blocks, items, entities, effects, enchantments, structures, biomes, and commands.
4. Translate by mechanism and context rather than word-by-word.
5. Prefer natural Chinese wording used by storage-tech players.
6. Preserve code, commands, coordinates, item counts, lists, Markdown structure, links, file names, and schematic names.
7. Keep unstable abbreviations and design names in English unless the glossary gives a stable Chinese form.
8. If a term is uncertain, keep the English term and explain the likely meaning instead of inventing a confident translation.

## Required References

Read only the relevant reference files:

- `references/translation-style.md`: Read before translating substantial prose or when the user asks for natural Chinese wording.
- `references/ambiguity-rules.md`: Read when the text contains storage-tech terms that are easy to mistranslate.
- `references/glossary.csv`: Query with `scripts/query_glossary.py`; do not load the whole CSV unless needed.

## Local Glossary

Use the local glossary before choosing Chinese terms for storage technology. Prefer:

```bash
python scripts/query_glossary.py "toggle buffer"
python scripts/query_glossary.py "bulk box" --format json
```

For longer text, use glossary lookup on the suspicious terms first. Do not rely on fuzzy matching alone for short words or abbreviations.

## Minecraft Wiki Verification

Use `scripts/query_minecraft_wiki.py` only for official Minecraft names, not storage-tech community jargon.

Examples:

```bash
python scripts/query_minecraft_wiki.py --term "Hopper" --language zh
python scripts/query_minecraft_wiki.py --term "Dispenser" --language zh --format json
```

If network access is unavailable or lookup fails, continue with the best known term and state that the official name was not verified.

## Output Style

For direct translation requests, output the translation first. Add terminology notes only when they clarify choices or uncertainty.

For document-reading requests, summarize the mechanism, then translate or explain the relevant passage.

For messy chat logs, remove UI noise such as reaction prompts, duplicated quoted messages, timestamps that are not meaningful, and platform controls before translating.

## Do Not

- Do not copy a general Minecraft translation workflow when the task is storage-tech specific.
- Do not use Minecraft Wiki as authority for storage-tech slang.
- Do not force every English technical term into Chinese.
- Do not translate design names or abbreviations just because they contain ordinary English words.
- Do not add video subtitle processing unless the user explicitly expands the skill scope later.
