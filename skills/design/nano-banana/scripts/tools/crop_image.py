#!/usr/bin/env python3
import os
import sys
from PIL import Image

def run():
    if len(sys.argv) < 3:
        print("Usage: python crop_image.py <input_img> <output_img> [aspect_ratio]")
        print("Supported ratios: 4:5, 16:9, 1:1, 9:16, 3:4, 4:3")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    ratio_str = sys.argv[3] if len(sys.argv) > 3 else "4:5"
    
    if not os.path.exists(input_file):
        print(f"ERROR: {input_file} not found")
        sys.exit(1)
        
    try:
        img = Image.open(input_file)
        w, h = img.size
        
        try:
            rw, rh = map(int, ratio_str.split(':'))
            target_ratio = rw / rh
        except Exception:
            print("Invalid ratio format. Use 'W:H'")
            sys.exit(1)
            
        current_ratio = w / h
        
        if current_ratio > target_ratio:
            # Too wide, crop sides
            new_w = int(h * target_ratio)
            left = (w - new_w) / 2
            img = img.crop((left, 0, left + new_w, h))
        else:
            # Too tall, crop top/bottom
            new_h = int(w / target_ratio)
            top = (h - new_h) / 2
            img = img.crop((0, top, w, top + new_h))
            
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        img.save(output_file, quality=95)
        print(f"Successfully cropped to {ratio_str} and saved to {output_file}")
        
    except Exception as e:
        print(f"ERROR cropping image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
