# Internationalization (i18n) Structure

This project uses a directory-based i18n structure for managing translations of The Rust Programming Language book.

## Structure

```
src/
├── *.md                    # English source files
└── fi/
    └── *.md               # Finnish translations
```

## Building the Book

### English Version
```bash
mdbook build --open
```

### Finnish Version
```bash
mdbook build -d book-fi.toml --open
```

Or use the provided scripts:
```bash
python tools/translation-manager.py status
```

## Translation Management

The `tools/translation-manager.py` script helps manage translations:

- `python tools/translation-manager.py status` - Show translation status
- `python tools/translation-manager.py missing` - List missing files
- `python tools/translation-manager.py template <file>` - Create translation template

## Adding New Translations

1. Create a new directory under `src/` for your language code (e.g., `src/sv/` for Swedish)
2. Copy `book-fi.toml` and create `book-<lang>.toml` with appropriate settings
3. Update the `src` path in the book configuration
4. Start translating files from `src/` to `src/<lang>/`

## Notes

- Keep file names identical between languages
- Maintain the same directory structure
- Update `SUMMARY.md` in each language directory to reflect translated titles
- Code examples and technical terms may remain in English where appropriate
