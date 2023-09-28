# video-to-screenshots

Convert video to screenshots

## Setup

```bash
./bootstrap.sh
```

## With Docker

```bash
task run
```

## Without Docker

```bash
# Setup virtual environment
task setup-venv
source .venv/bin/activate

# Download video
python3 src/download_video.py \
    --url https://www.youtube.com/watch?v=yp6WuHFhYCo

# Generate screenshots
python3 src/generate_screenshots.py \
    --video-path downloads/Keynote_Speaker_-_Guido_van_Rossum.mp4 \
    --similarity-threshold 3.0
```
