#!/usr/bin/env python3
"""
YouTube Video Downloader
Downloads videos from YouTube with customizable quality and format options.
"""

import argparse
import sys
import subprocess
import json
import os

def check_yt_dlp():
    """Check if yt-dlp is installed, install if not."""
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("yt-dlp not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", "yt-dlp"], check=True)

def get_video_info(url):
    """Get information about the video without downloading."""
    check_yt_dlp()
    cmd = ["yt-dlp", "--dump-json", "--no-playlist", url]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(result.stdout)

def download_video(url, output_path=None, quality="best", format_type="mp4", audio_only=False):
    """
    Download a YouTube video.
    
    Args:
        url: YouTube video URL
        output_path: Directory to save the video. Defaults to /mnt/user-data/outputs or current dir.
        quality: Quality setting (best, 1080p, 720p, 480p, 360p, worst)
        format_type: Output format (mp4, webm, mkv, etc.)
        audio_only: Download only audio (mp3)
    """
    check_yt_dlp()
    
    # Determine output path
    if output_path is None:
        # Default fallback logic
        if os.path.isdir("/mnt/user-data/outputs"):
            output_path = "/mnt/user-data/outputs"
        else:
            output_path = os.getcwd()
            
    # Ensure output directory exists
    if not os.path.exists(output_path):
        try:
            os.makedirs(output_path)
        except OSError as e:
            print(f"Error creating output directory: {e}")
            return False

    cmd = ["yt-dlp"]
    
    if audio_only:
        cmd.extend([
            "-x",  # Extract audio
            "--audio-format", "mp3",
            "--audio-quality", "0",  # Best quality
        ])
    else:
        # Video quality settings
        if quality == "best":
            # Just use best available that matches our container preference
            # If format_type is mp4, we want best video+best audio that merges to mp4
            format_string = f"bestvideo+bestaudio/best"
        elif quality == "worst":
            format_string = "worstvideo+worstaudio/worst"
        else:
            # Specific resolution (e.g., 1080p, 720p)
            height = quality.replace("p", "")
            # Try to get exact height, fallback to best under that height
            format_string = f"bestvideo[height<={height}]+bestaudio/best[height<={height}]"
        
        cmd.extend([
            "-f", format_string,
            "--merge-output-format", format_type,
        ])
    
    # Output template
    cmd.extend([
        "-o", os.path.join(output_path, "%(title)s.%(ext)s"),
        "--no-playlist",  # Don't download playlists by default
    ])
    
    cmd.append(url)
    
    print(f"Downloading from: {url}")
    print(f"Quality: {quality}")
    print(f"Format: {'mp3 (audio only)' if audio_only else format_type}")
    print(f"Output: {output_path}")
    
    try:
        # Get video info first for nice logging
        print("\nFetching video info...")
        info = get_video_info(url)
        title = info.get('title', 'Unknown')
        duration = info.get('duration', 0)
        uploader = info.get('uploader', 'Unknown')
        
        print(f"Title: {title}")
        print(f"Duration: {duration // 60}:{duration % 60:02d}")
        print(f"Uploader: {uploader}\n")
        
        # Download the video
        subprocess.run(cmd, check=True)
        print(f"\n✅ Download complete!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error downloading video: {e}")
        # If it failed, maybe because of format selection issues, try generic best
        if quality != "best" and not audio_only:
            print("Retrying with default 'best' quality settings...")
            return download_video(url, output_path, "best", format_type, audio_only)
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Download YouTube videos with customizable quality and format"
    )
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Output directory (default: /mnt/user-data/outputs or current dir)"
    )
    parser.add_argument(
        "-q", "--quality",
        default="best",
        choices=["best", "1080p", "720p", "480p", "360p", "worst"],
        help="Video quality (default: best)"
    )
    parser.add_argument(
        "-f", "--format",
        default="mp4",
        choices=["mp4", "webm", "mkv"],
        help="Video format (default: mp4)"
    )
    parser.add_argument(
        "-a", "--audio-only",
        action="store_true",
        help="Download only audio as MP3"
    )
    
    args = parser.parse_args()
    
    success = download_video(
        url=args.url,
        output_path=args.output,
        quality=args.quality,
        format_type=args.format,
        audio_only=args.audio_only
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
