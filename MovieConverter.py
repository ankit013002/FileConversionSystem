import subprocess
import os
from colorama import Fore, init


def movie_converter(input_path, debug_enabled):
    if input_path == "":
        input_path = input("Please enter the path to the video file: ")

    output_path = os.path.splitext(input_path)[0] + ".mp4"

    vf_string = (
        "tonemap=tonemap=reinhard:param=0.2:peak=300:desat=0,"
        "format=yuv420p"
    )

    # Construct ffmpeg command
    command = [
        "ffmpeg",
        "-i", input_path,
        "-vf", vf_string,
        "-c:v", "libx264",
        "-crf", "18",
        "-preset", "slow",
        "-c:a", "aac",
        "-b:a", "192k",
        output_path
    ]
    try:
        print(Fore.CYAN + f"Converting video {input_path} to {output_path}")
        subprocess.run(command, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if debug_enabled:
            print(Fore.GREEN +
                  f"Conversion successful! Saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print("Conversion failed:", e)

    return output_path
