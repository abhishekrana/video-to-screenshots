#!/bin/bash

set -e

. .venv/bin/activate

# Download video
python3 src/download_video.py --url https://www.youtube.com/watch?v=yp6WuHFhYCo

# Generate screenshots
python3 src/generate_screenshots.py --video-path downloads/Keynote_Speaker_-_Guido_van_Rossum.mp4

