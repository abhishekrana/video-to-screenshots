from pathlib import Path

import cv2
import numpy as np
import typer
from cv2.typing import MatLike


def similarity_mse(frame1: MatLike, frame2: MatLike, similarity_threshold: float) -> bool:
    # Convert frames to grayscale for better accuracy
    gray_frame1: MatLike = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray_frame2: MatLike = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Calculate the Mean Squared Error (MSE) between the two frames
    mse = np.mean((gray_frame1 - gray_frame2) ** 2) # type: ignore

    # Return True if frames are similar (MSE is below the threshold), False otherwise
    return mse < similarity_threshold


def generate_video_frames(
    video_path: Path,
    output_path: Path,
    similarity_threshold: float,
    frame_width: int,
    jpeg_quality: int,
    skip_frames: int,
) -> None:
    if not video_path.exists():
        raise IOError(f"Video does not exist. {video_path=}")

    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)

    # Open the video file
    cap = cv2.VideoCapture(str(video_path))

    ret: bool
    prev_frame: MatLike
    current_frame: MatLike

    # Read the first frame
    ret, prev_frame = cap.read()

    count = 0
    similar_count: int = 0

    while True:
        # Read the next frame
        ret, current_frame = cap.read()
        if ret is False:
            break

        if skip_frames != 0 and skip_frames != 1 and (count % skip_frames) == 0:
            count += 1
            continue

        # Compare the current frame with the previous frame
        similar: bool = similarity_mse(prev_frame, current_frame, similarity_threshold)
        if similar:
            similar_count += 1
        else:
            if similar_count > 0:
                path: str = f"{output_path}/{video_path.stem}_frame_{count:06d}.jpg"

                height, width, _ = prev_frame.shape
                new_height = int((frame_width / width) * height)
                resized_image: MatLike = cv2.resize(prev_frame, (frame_width, new_height))

                cv2.imwrite(path, resized_image, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])

                similar_count = 0
                print(f"Saved snapshot. {count=} {similar_count=}, {path}")

        prev_frame = current_frame
        count += 1


def main(
    video_path: Path = Path("downloads/Keynote_Speaker_-_Guido_van_Rossum.mp4"),
    similarity_threshold: float = 3.0,
    output_dir: Path = Path("screenshots"),
    skip_frames: int = 2,
    image_width: int = 720,  # resolution
    jpeg_quality: int = 50,  # 0-100
) -> None:
    generate_video_frames(
        video_path=video_path,
        output_path=output_dir,
        similarity_threshold=similarity_threshold,
        frame_width=image_width,
        jpeg_quality=jpeg_quality,
        skip_frames=skip_frames,
    )


if __name__ == "__main__":
    typer.run(main)
