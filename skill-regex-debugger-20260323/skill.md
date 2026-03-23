---
name: regex-debugger
description: "Build, test, debug, and explain regular expressions. Use when working with regex patterns, fixing regex bugs, optimizing regex performance, explaining regex to others, or converting between regex dialects (PCRE/JavaScript/Python/Go). Triggers on: regex not working, fix my regex, explain this regex, optimize regex, build a regex for X, regex performance, convert regex."
---

# Regex Debugger

Build, test, debug, and explain regular expressions across languages and dialects.

## Regex Testing Workflow

### Step 1: Identify the Goal

Ask: What pattern am I trying to match?
- Exact string match
- Pattern with wildcards
- Validation (email, phone, URL, etc.)
- Extraction (capture groups)
- Replacement/substitution

### Step 2: Build Incrementally

Build regex piece by piece, testing each part:
```
Start simple → Add complexity → Verify each step
```

### Step 3: Test with Edge Cases

Always test against:
- **Positive cases** — strings that SHOULD match
- **Negative cases** — strings that should NOT match
- **Edge cases** — empty strings, special characters, Unicode

### Step 4: Optimize Last

Don't optimize prematurely. Get it working first, then profile.

## Common Patterns Cheat Sheet

### Validation

```
Email:     ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
Phone:     ^\+?[1-9]\d{1,14}$          (E.164)
URL:       ^https?:\/\/[^\s/$.?#].[^\s]*$
IPv4:      ^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$
IPv6:      ^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$
Date:      ^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])$
Time:      ^(?:[01][0-9]|2[0-3]):[0-5][0-9](?::[0-5][0-9])?$
```

### Extraction

```
HTML tag:        <([a-z]+)([^>]*)>(.*?)<\/\1>
JSON key-value:  "(\w+)":\s*(".*?"|\d+|true|false|null)
Log line:        ^(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+(\w+)\s+(.*)$
```

### Text Cleaning

```
Multiple spaces:  \s{2,}
Leading/trailing: ^\s+|\s+$
HTML entities:    &[a-z]+;|&#\d+;
```

## Debugging Broken Regex

### Checklist

- [ ] Escape special chars inside character classes: `[.]` not `.`
- [ ] Use non-greedy quantifiers: `.*?` instead of `.*` when extracting
- [ ] Anchor appropriately: `^` and `$` for full match, no anchors for partial
- [ ] Check for missing groups: `(...)` vs `(?:...)`
- [ ] Verify lookahead/lookbehind syntax: `(?=...)` `(?<=...)`
- [ ] Test with multiline mode if using `^`/`$` across lines
- [ ] Beware of catastrophic backtracking: `(a+)+` patterns

### Catastrophic Backtracking Warning Signs

These patterns can freeze or timeout:
```
(a+)+    (a*)+
(a|a)+
(.*a){n}  for n > 1
```

**Fix:** Use atomic groups, possessive quantifiers, or rewrite to linear regex.

## Dialect Differences

| Feature | PCRE | JavaScript | Python | Go |
|---------|------|------------|--------|-----|
| Named groups | `(?<name>...)` | `(?<name>...)` | `(?P<name>...)` | `(?P<name>...)` |
| Lookahead | `(?=...)` | `(?=...)` | `(?=...)` | `(?=...)` |
| Lookbehind | `(?<=...)` | `(?<=...)` ES2018+ | `(?<=...)` | `(?<=...)` |
| Non-greedy | `??` `*?` `+?` | `??` `*?` `+?` | `??` `*?` `+?` | Only `?` after `*`/`+` |
| Dot-all | `(?s)` | `.` doesn't match `\n` | `(?s)` | `(?s)` |
| Unicode | `\u{...}` | `\u{...}` | `\u{...}` | `\p{L}` |

## Performance Tips

1. **Use character classes over alternation:** `[abc]` faster than `(a|b|c)`
2. **Anchor literals:** `^hello` faster than `hello`
3. **Avoid `.*` at start:** Use negated character class like `[^"]*`
4. **Use lazy quantifiers appropriately:** `.*?` vs `[^"]*`
5. **Compile when reusing:** Most engines cache or allow pre-compilation

## Tools

- [regex101.com](https://regex101.com) — Interactive tester with explanation
- [regexr.com](https://regexr.com) — Visual regex tool
- [debuggex.com](https://www.debuggex.com) — Railroad diagram visualizer
- PCRE: `pcregrep` or online testers
- Python: `re.DEBUG` flag for pattern analysis
- JavaScript: Chrome DevTools or Node.js `regex` object
- See `references/common-patterns.md` for curated pattern library
