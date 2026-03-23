# Common Regex Patterns Library

## Identity & Contact

```
Username:     ^[a-zA-Z][a-zA-Z0-9_-]{2,15}$
Password:     ^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$
Email:        ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
Phone (US):   ^\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$
Postal (US):  ^\d{5}(-\d{4})?$
```

## Web & URLs

```
HTTP(S) URL:  ^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$
Markdown URL: \[([^\]]+)\]\(([^)]+)\)
HTML tag:     <([a-z][a-z0-9]*)\b[^>]*>(.*?)<\/\1>
HTML comment: <!--[\s\S]*?-->
CSS class:    \.-?[_a-zA-Z]+[_a-zA-Z0-9-]*
CSS id:       #[a-zA-Z][_a-zA-Z0-9-]*
```

## Code & Programming

```
Variable name (JS):    ^[a-zA-Z_$][a-zA-Z0-9_$]*$
Function name (camel): ^[a-z][a-zA-Z0-9]*$
Class name (Pascal):  ^[A-Z][a-zA-Z0-9]*$
Hex color:             ^#?([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$
UUID:                  ^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$
Semver:                ^\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?(\+[a-zA-Z0-9]+)?$
```

## Numbers & Formatting

```
Integer:       ^-?\d+$
Positive int:  ^\d+$
Float:         ^-?\d+\.?\d*$
Currency ($):  ^\$?\d{1,3}(,\d{3})*(\.\d{2})?$
Percentage:    ^\d+\.?\d*%$
Scientific:    ^[+-]?\d+\.?\d*([eE][+-]?\d+)?$
Binary:        ^[01]+$
Hex:           ^0x[0-9a-fA-F]+$
```

## Date & Time

```
ISO 8601 date:       ^\d{4}-\d{2}-\d{2}$
ISO 8601 datetime:   ^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})?$
US date (MM/DD/YYYY):^(0[1-9]|1[0-2])\/(0[1-9]|[12]\d|3[01])\/\d{4}$
EU date (DD/MM/YYYY):^(0[1-9]|[12]\d|3[01])\/(0[1-9]|1[0-2])\/\d{4}$
Time 24h:            ^([01]\d|2[0-3]):([0-5]\d)(:([0-5]\d))?$
Time 12h:            ^(0?[1-9]|1[0-2]):([0-5]\d)\s?(AM|PM|am|pm)$
```

## Text Cleaning

```
Trim whitespace:  ^\s+|\s+$
Collapse spaces:  \s{2,}
Line breaks:      \r\n|\r|\n
Multiple newlines: \n{3,}
HTML tags:        <[^>]+>
HTML entities:    &[a-zA-Z]+;|&#\d+;
```

## Security

```
JWT:                ^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]*$
AWS Access Key:     ^AKIA[0-9A-Z]{16}$
AWS Secret Key:     ^[A-Za-z0-9/+=]{40}$
Private key header:-----BEGIN (RSA |EC |DSA |OPENSSH )PRIVATE KEY-----
Credit card:        ^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})$
SSN:                ^\d{3}-\d{2}-\d{4}$
```

## Logs & Structured Text

```
IP address (v4):    ^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$
IP address (v6):    ^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$
MAC address:        ^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$
Log level:          \b(DEBUG|INFO|WARN|ERROR|FATAL|TRACE)\b
ISO timestamp:      \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}
```
