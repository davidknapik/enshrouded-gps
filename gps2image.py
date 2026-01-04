from PIL import Image, ImageDraw
import os

# --- CONFIGURATION ---
INPUT_FILE = 'gps.txt'
OUTPUT_FILE = 'map_overlay.png'
MAP_SIZE = 10240        # 10240 x 10240
DOT_SIZE = 5            # Change this to make dots bigger or smaller
DOT_COLOR = (255, 0, 0, 255) # Red (R, G, B, Alpha)

def create_overlay():
    # 1. Create a blank transparent image (RGBA)
    # (0, 0, 0, 0) means Black with 0 Alpha (fully transparent)
    img = Image.new('RGBA', (MAP_SIZE, MAP_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return

    print(f"Processing {INPUT_FILE}...")
    
    count = 0
    with open(INPUT_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or ',' not in line:
                continue
            
            try:
                # Parse coordinates
                x_raw, y_raw = line.split(',')
                x = float(x_raw)
                y = float(y_raw)

                # 2. Coordinate Transformation
                # Origin bottom-left: 
                # Image X is same as Coordinate X
                # Image Y is ImageHeight - Coordinate Y (because Image 0,0 is top-left)
                img_x = x
                img_y = MAP_SIZE - y

                # 3. Draw the dot
                if DOT_SIZE <= 1:
                    draw.point((img_x, img_y), fill=DOT_COLOR)
                else:
                    # Draw a circle centered on the coordinate
                    r = DOT_SIZE / 2
                    draw.ellipse([img_x - r, img_y - r, img_x + r, img_y + r], 
                                 fill=DOT_COLOR, outline=DOT_COLOR)
                
                count += 1
            except ValueError:
                print(f"Skipping invalid line: {line}")

    # 4. Save the image
    print(f"Drawing complete. Saving {count} points to {OUTPUT_FILE}...")
    img.save(OUTPUT_FILE, "PNG")
    print("Done.")

if __name__ == "__main__":
    create_overlay()