"""
https://github.com/yt-dlp/yt-dlp#embedding-yt-dlp
"""
import re
from typing import Any
from pathlib import Path

import typer
import yt_dlp

YT_DLP_CACHE_DIR: str = "/tmp/.cache/yt-dlp"

def get_info(url: str, fps: int, file_extension: str, resolution: str) -> tuple[str, str]:
    ydl_opts: dict[str, Any] = {"cachedir": YT_DLP_CACHE_DIR}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info: dict[str, str] = ydl.extract_info(url, download=False)  # type: ignore
        # print(json.dumps(ydl.sanitize_info(info), indent=2))

        formats: list[dict[str, Any]] = info.get("formats", [])  # type: ignore
        for format in formats:
            print(f"FPS={format.get('fps')}, Extension={format.get('ext')}, Resolution:{format.get('resolution')}")

        for format in formats:
            if (
                format.get("fps") == int(fps)
                and format.get("ext") == file_extension
                and format.get("resolution") == resolution
            ):
                return format.get("url", ""), info.get("title", "")

    raise ValueError("Unable to get video. Try different arguments.")


def download_video(url: str, title: str, file_extension: str, output_dir: Path) -> None:
    filename: str = f"{title}.{file_extension}"
    filename = filename.replace(" ", "_")
    regex = re.compile("[^a-zA-Z0-9-_.]")
    filename = regex.sub("", filename)

    ydl_opts: dict[str, Any] = {
        "cachedir": YT_DLP_CACHE_DIR,
        "paths": {"home": output_dir},
        "outtmpl": {"default": filename},
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code: int = ydl.download([url])
        print(f"{error_code=}")


def main(
    url: str = "https://www.youtube.com/watch?v=yp6WuHFhYCo",
    fps: int = 30,
    file_extension="mp4",
    resolution: str = "1280x720",
    output_dir=Path("downloads"),
) -> None:
    video_url: str
    video_title: str
    video_url, video_title = get_info(url, fps, file_extension, resolution)
    print(f"{video_url=}, {video_title=}")

    download_video(video_url, video_title, file_extension, output_dir)


if __name__ == "__main__":
    typer.run(main)
