#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
#     "pillow>=10.0.0",
#     "requests>=2.31.0",
# ]
# ///
"""
Nano Banana Unified Image Generator.
Combines Google Gemini 3 Pro Image (direct GenAI SDK), AI Gateway, and Kie.ai fallback.
Supports photorealistic text-to-image, JSON parameterization, and multi-image composition (up to 14 images).

Usage:
    python3 generate_image.py --prompt "a cybernetic falcon in neon rain" --filename "output.png"
    python3 generate_image.py --json-prompt examples/portrait_dense.json --filename "output.png"
    python3 generate_image.py --prompt "merge styles" --filename "output.png" -i img1.png -i img2.png
"""

import argparse
import base64
from io import BytesIO
import json
import os
from pathlib import Path
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

REALISTIC_POSITIVE_SUFFIX = (
    " Highly detailed photograph, authentic documentary realism. "
    "Visible natural skin pores, peach fuzz, subtle imperfections, natural asymmetric features. "
    "Shot on 85mm lens, f/1.8, ISO 200, realistic lighting with natural specular falloff. "
    "Unretouched raw photograph, no beauty filters, no digital smoothing."
)

DEFAULT_NEGATIVE_STACK = (
    "blurry, low resolution, distorted face, extra fingers, malformed hands, overexposed, "
    "heavy makeup, unrealistic skin, cartoon, CGI, 3D render, oversaturated colors, "
    "anatomy normalization, datasets-average body, plastic skin, airbrushed, wax figure, "
    "beautified, perfectly symmetrical face, stock photo look"
)


def load_env_files():
    """Load environment variables from nearest .env or config/.env files."""
    script_dir = Path(__file__).resolve().parent
    candidates = [
        script_dir.parent / "config" / ".env",
        script_dir.parent / ".env",
        Path.cwd() / ".env",
        Path("/Users/asmadey/AntiGravity/PersonalOS/skills/nano-banana/config/.env"),
    ]
    for env_path in candidates:
        if env_path.is_file():
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            k = k.strip()
                            v = v.strip().strip("'\"")
                            if k and k not in os.environ:
                                os.environ[k] = v
            except Exception:
                pass


load_env_files()


def get_credentials(
    cli_key: Optional[str], preferred_provider: str
) -> Tuple[str, str]:
    """
    Resolve (provider, api_key).
    Provider can be: 'ai-gateway', 'gemini', 'kie'.
    """
    if cli_key:
        if preferred_provider != "auto":
            return preferred_provider, cli_key
        return "gemini", cli_key

    ai_gateway_key = os.environ.get("AI_GATEWAY_API_KEY")
    gemini_key = os.environ.get("GEMINI_API_KEY")
    kie_key = os.environ.get("KIE_API_KEY")

    if preferred_provider == "ai-gateway":
        if not ai_gateway_key:
            raise ValueError("AI_GATEWAY_API_KEY not found in environment.")
        return "ai-gateway", ai_gateway_key

    if preferred_provider == "gemini":
        if not gemini_key:
            raise ValueError("GEMINI_API_KEY not found in environment.")
        return "gemini", gemini_key

    if preferred_provider == "kie":
        if not kie_key:
            raise ValueError("KIE_API_KEY not found in environment.")
        return "kie", kie_key

    # Auto priority:
    # 1. AI Gateway if key exists
    if ai_gateway_key:
        return "ai-gateway", ai_gateway_key
    # 2. Direct Gemini GenAI
    if gemini_key:
        return "gemini", gemini_key
    # 3. Kie.ai fallback
    if kie_key:
        return "kie", kie_key

    raise ValueError(
        "No API key found. Please set GEMINI_API_KEY, AI_GATEWAY_API_KEY, or KIE_API_KEY in config/.env."
    )


def call_ai_gateway(
    api_key: str,
    prompt: str,
    input_images: List[Any],
    resolution: str,
) -> bytes:
    """Call AI Gateway endpoint."""
    import requests

    api_base = "https://ai-gateway.happycapy.ai/api/v1"
    gateway_url = f"{api_base}/images/generations"

    payload = {
        "model": "google/gemini-3-pro-image-preview",
        "prompt": prompt,
        "response_format": "url",
        "n": 1,
    }

    if input_images:
        print("Warning: AI Gateway images endpoint does not support input images.")
        print("Generating from prompt text only.")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "Origin": "https://trickle.so",
        "User-Agent": "Mozilla/5.0 (compatible; Nano-Banana/1.0)",
    }

    print(f"Calling AI Gateway ({gateway_url})...")
    res = requests.post(gateway_url, json=payload, headers=headers, timeout=120)
    if res.status_code != 200:
        raise RuntimeError(f"AI Gateway error ({res.status_code}): {res.text}")

    data = res.json()
    items = data.get("data", [])
    if not items:
        raise RuntimeError(f"No image data returned from AI Gateway: {data}")

    first = items[0]
    if "b64_json" in first:
        return base64.b64decode(first["b64_json"])
    elif "url" in first:
        img_url = first["url"]
        dl = requests.get(img_url, timeout=60)
        if dl.status_code == 200:
            return dl.content
        raise RuntimeError(f"Failed to download image from URL ({dl.status_code})")
    raise RuntimeError(f"Unknown image payload: {first}")


def call_gemini_direct(
    api_key: str,
    prompt: str,
    input_images: List[Any],
    resolution: str,
    aspect_ratio: Optional[str] = None,
) -> bytes:
    """Call Google Gemini 3 Pro directly via GenAI SDK."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    contents: Any
    if input_images:
        contents = [*input_images, prompt]
    else:
        contents = prompt

    print(f"Calling Gemini 3 Pro (gemini-3-pro-image-preview, resolution: {resolution})...")
    
    # Supported image sizes in Gemini Image Config: '1K', '2K', '4K'
    image_config_args = {"image_size": resolution}
    if aspect_ratio and aspect_ratio != "auto":
        image_config_args["aspect_ratio"] = aspect_ratio

    try:
        image_cfg = types.ImageConfig(**image_config_args)
    except Exception:
        image_cfg = types.ImageConfig(image_size=resolution)

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=image_cfg,
        ),
    )

    for part in response.parts:
        if part.inline_data is not None:
            raw = part.inline_data.data
            if isinstance(raw, str):
                return base64.b64decode(raw)
            return raw
        elif part.text is not None:
            print(f"Model note: {part.text}")

    raise RuntimeError("Gemini API response did not contain image data.")


def call_kie_ai(
    api_key: str,
    prompt: str,
    aspect_ratio: str,
    resolution: str,
) -> bytes:
    """Call Kie.ai task API as fallback."""
    import requests

    create_url = "https://api.kie.ai/api/v1/jobs/createTask"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    payload = {
        "model": "nano-banana-2",
        "input": {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio if aspect_ratio != "auto" else "1:1",
            "resolution": resolution,
            "output_format": "png",
        },
    }

    print("Submitting task to Kie.ai API...")
    res = requests.post(create_url, headers=headers, json=payload, timeout=30)
    res.raise_for_status()
    task_id = res.json().get("data", {}).get("taskId")
    if not task_id:
        raise RuntimeError(f"Kie.ai did not return taskId: {res.text}")

    print(f"Task created (ID: {task_id}). Polling status...")
    poll_url = "https://api.kie.ai/api/v1/jobs/recordInfo"

    attempts = 0
    while attempts < 60:
        time.sleep(4)
        attempts += 1
        poll_res = requests.get(
            poll_url, headers=headers, params={"taskId": task_id}, timeout=15
        )
        if poll_res.status_code != 200:
            continue
        data = poll_res.json().get("data", {})
        state = data.get("state")
        if state in ("success", "completed"):
            result_json_str = data.get("resultJson", "{}")
            try:
                r_json = json.loads(result_json_str)
            except Exception:
                r_json = {}
            urls = r_json.get("resultUrls", [])
            if urls:
                dl = requests.get(urls[0], timeout=30)
                dl.raise_for_status()
                return dl.content
            raise RuntimeError(f"No resultUrls in Kie.ai result: {data}")
        elif state in ("failed", "error"):
            raise RuntimeError(f"Kie.ai task failed: {data}")

    raise TimeoutError("Timed out waiting for Kie.ai job completion.")


def parse_prompt_input(
    prompt_arg: Optional[str],
    json_prompt_arg: Optional[str],
    force_realistic: bool,
    custom_negative: Optional[str],
) -> Tuple[str, Dict[str, Any]]:
    """Resolve prompt text, negative constraints and settings."""
    metadata: Dict[str, Any] = {}
    base_prompt = ""
    neg_prompt = custom_negative or ""

    if json_prompt_arg:
        p_path = Path(json_prompt_arg)
        if not p_path.is_file():
            raise FileNotFoundError(f"JSON prompt file not found: {json_prompt_arg}")
        with open(p_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, dict):
            base_prompt = data.get("prompt", "")
            json_neg = data.get("negative_prompt", "")
            if json_neg:
                neg_prompt = f"{neg_prompt}, {json_neg}" if neg_prompt else json_neg
            settings = data.get("settings") or data.get("api_parameters") or {}
            if isinstance(settings, dict):
                metadata.update(settings)
        else:
            base_prompt = str(data)

    if prompt_arg:
        base_prompt = f"{base_prompt} {prompt_arg}".strip() if base_prompt else prompt_arg

    if not base_prompt:
        raise ValueError("No prompt provided. Specify --prompt or --json-prompt.")

    if force_realistic:
        base_prompt = f"{base_prompt.rstrip('.')}.{REALISTIC_POSITIVE_SUFFIX}"
        if not neg_prompt:
            neg_prompt = DEFAULT_NEGATIVE_STACK
        else:
            neg_prompt = f"{neg_prompt}, {DEFAULT_NEGATIVE_STACK}"

    if neg_prompt:
        full_prompt = f"{base_prompt}\n\nNegative Constraints (DO NOT INCLUDE): {neg_prompt}"
    else:
        full_prompt = base_prompt

    return full_prompt, metadata


def main():
    parser = argparse.ArgumentParser(
        description="Nano Banana Unified Image Generator (Gemini 3 Pro / AI Gateway / Kie.ai)"
    )
    parser.add_argument(
        "--prompt", "-p",
        help="Image description/prompt text"
    )
    parser.add_argument(
        "--json-prompt", "-j",
        help="Path to JSON prompt file (following master schema)"
    )
    parser.add_argument(
        "--filename", "-f",
        required=True,
        help="Output image path (e.g. output/photo.png)"
    )
    parser.add_argument(
        "--input-image", "-i",
        action="append",
        dest="input_images",
        metavar="IMAGE",
        help="Input image for editing or multi-image composition (can specify up to 14 times)"
    )
    parser.add_argument(
        "--resolution", "-r",
        choices=["1K", "2K", "4K"],
        default="1K",
        help="Resolution tier: 1K (default), 2K, 4K"
    )
    parser.add_argument(
        "--aspect-ratio", "-a",
        default="auto",
        help="Aspect ratio (e.g. 1:1, 16:9, 9:16, 4:5, 3:4, 4:3, auto)"
    )
    parser.add_argument(
        "--realistic",
        action="store_true",
        help="Automatically apply 13 photorealism rules, camera physics, and anti-plastic negative stack"
    )
    parser.add_argument(
        "--negative-prompt",
        help="Explicit negative prompt / elements to avoid"
    )
    parser.add_argument(
        "--provider",
        choices=["auto", "gemini", "ai-gateway", "kie"],
        default="auto",
        help="Provider choice (default: auto priority)"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="Explicit API key override"
    )

    args = parser.parse_args()

    # 1. Parse prompt & settings
    prompt_text, meta_settings = parse_prompt_input(
        prompt_arg=args.prompt,
        json_prompt_arg=args.json_prompt,
        force_realistic=args.realistic,
        custom_negative=args.negative_prompt,
    )

    # Resolution precedence: CLI arg > JSON settings > default
    resolution = meta_settings.get("resolution", args.resolution)
    aspect_ratio = meta_settings.get("aspect_ratio", args.aspect_ratio)

    # 2. Resolve credentials & provider
    try:
        provider, api_key = get_credentials(args.api_key, args.provider)
    except ValueError as e:
        print(f"Authentication Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Provider: {provider}")

    # 3. Load input images (PIL)
    from PIL import Image as PILImage

    loaded_images = []
    if args.input_images:
        if len(args.input_images) > 14:
            print("Error: Maximum 14 input images allowed.", file=sys.stderr)
            sys.exit(1)

        max_dim = 0
        for p in args.input_images:
            if not os.path.exists(p):
                print(f"Error: Input image not found: {p}", file=sys.stderr)
                sys.exit(1)
            img = PILImage.open(p)
            loaded_images.append(img)
            max_dim = max(max_dim, img.size[0], img.size[1])

        # Auto resolution promotion if default 1K was left
        if args.resolution == "1K" and max_dim >= 2000:
            resolution = "2K"
            print(f"Auto-promoted resolution to 2K based on input image dimensions ({max_dim}px)")

    # 4. Generate image
    image_bytes: Optional[bytes] = None
    try:
        if provider == "ai-gateway":
            image_bytes = call_ai_gateway(api_key, prompt_text, loaded_images, resolution)
        elif provider == "gemini":
            image_bytes = call_gemini_direct(
                api_key, prompt_text, loaded_images, resolution, aspect_ratio
            )
        elif provider == "kie":
            image_bytes = call_kie_ai(api_key, prompt_text, aspect_ratio, resolution)
    except Exception as e:
        print(f"Primary provider '{provider}' failed: {e}", file=sys.stderr)
        # Try fallbacks in auto mode
        if args.provider == "auto":
            # 1. If not Gemini, try Gemini
            if provider != "gemini" and os.environ.get("GEMINI_API_KEY") and not image_bytes:
                print("Attempting fallback to direct Gemini API...")
                try:
                    image_bytes = call_gemini_direct(
                        os.environ["GEMINI_API_KEY"], prompt_text, loaded_images, resolution, aspect_ratio
                    )
                except Exception as fb_err:
                    print(f"Fallback to Gemini failed: {fb_err}", file=sys.stderr)

            # 2. If not Kie, try Kie.ai
            if provider != "kie" and os.environ.get("KIE_API_KEY") and not image_bytes:
                print("Attempting fallback to Kie.ai...")
                try:
                    image_bytes = call_kie_ai(
                        os.environ["KIE_API_KEY"], prompt_text, aspect_ratio, resolution
                    )
                except Exception as fb_err:
                    print(f"Fallback to Kie.ai failed: {fb_err}", file=sys.stderr)

            # 3. If not AI Gateway, try AI Gateway
            if provider != "ai-gateway" and os.environ.get("AI_GATEWAY_API_KEY") and not image_bytes:
                print("Attempting fallback to AI Gateway...")
                try:
                    image_bytes = call_ai_gateway(
                        os.environ["AI_GATEWAY_API_KEY"], prompt_text, loaded_images, resolution
                    )
                except Exception as fb_err:
                    print(f"Fallback to AI Gateway failed: {fb_err}", file=sys.stderr)

    if not image_bytes:
        print("Error: Failed to generate image from any available provider.", file=sys.stderr)
        sys.exit(1)

    # 5. Save output file
    output_path = Path(args.filename).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    img = PILImage.open(BytesIO(image_bytes))

    if output_path.suffix.lower() in [".jpg", ".jpeg"]:
        if img.mode in ("RGBA", "P"):
            rgb = PILImage.new("RGB", img.size, (255, 255, 255))
            if img.mode == "RGBA":
                rgb.paste(img, mask=img.split()[3])
            else:
                rgb.paste(img.convert("RGBA"))
            rgb.save(str(output_path), "JPEG", quality=95)
        else:
            img.convert("RGB").save(str(output_path), "JPEG", quality=95)
    else:
        # Default PNG
        if img.mode == "RGBA":
            # Clean composite with white background if PNG
            rgb = PILImage.new("RGB", img.size, (255, 255, 255))
            rgb.paste(img, mask=img.split()[3])
            rgb.save(str(output_path), "PNG")
        elif img.mode == "RGB":
            img.save(str(output_path), "PNG")
        else:
            img.convert("RGB").save(str(output_path), "PNG")

    print(f"\n✅ Image successfully saved: {output_path}")
    print(f"MEDIA: {output_path}")


if __name__ == "__main__":
    main()
