"""
Quick Start Guide for ECB Tool (Alpha Version)

## Installation

1. Create virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -e .
# Or with dev dependencies:
pip install -e ".[dev]"
```

## Running the Application

```bash
# New way (recommended)
python -m ecb_tool.main

# Or use the entry point:
ecb-tool

# Legacy way (still works):
python main.py
```

## Running Tests

```bash
# All tests
pytest

# Only unit tests
pytest tests/unit

# With coverage
pytest --cov=ecb_tool --cov-report=html
```

## Project Structure

```
ecb_tool/              # Main package
  ├── core/           # Core utilities (paths, config)
  ├── features/       # Business features
  │   ├── conversion/ # Video conversion
  │   ├── upload/     # YouTube upload
  │   ├── settings/   # Settings management
  │   └── ui/         # UI components
  └── main.py         # Entry point

tests/                # Test suite
  ├── unit/          # Unit tests
  └── integration/   # Integration tests

workspace/            # Working files
  ├── beats/         # Audio input
  ├── covers/        # Image input
  └── videos/        # Video output
```

## Using the New Paths System

```python
from ecb_tool.core.paths import get_paths

paths = get_paths()

# Access any path directly:
print(paths.beats)      # workspace/beats
print(paths.videos)     # workspace/videos
print(paths.app_log)    # data/app.log
```

## Using Features

```python
from ecb_tool.features.conversion import VideoConverter, ConversionConfig
from ecb_tool.features.upload import VideoUploader, UploadConfig
from ecb_tool.core.paths import get_paths

paths = get_paths()

# Setup conversion
config = ConversionConfig(
    beats_dir=paths.beats,
    covers_dir=paths.covers,
    videos_dir=paths.videos,
)

converter = VideoConverter(config)
beats = converter.list_beats()
```

## Development

```bash
# Format code
black ecb_tool/

# Type checking
mypy ecb_tool/

# Linting
flake8 ecb_tool/
```

## Next Steps

1. Add beats to `workspace/beats/`
2. Add covers to `workspace/covers/`
3. Configure settings in `config/`
4. Run the application
5. Check `NUEVA_ESTRUCTURA.md` for details

## Troubleshooting

### Import errors
```bash
pip install -e .
```

### FFmpeg not found
Ensure `ffmpeg/bin/ffmpeg.exe` exists

### Tests fail
```bash
pip install pytest pytest-qt
pytest -v
```

---

Version: 1.0.0-alpha
