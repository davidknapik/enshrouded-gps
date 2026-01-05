from PIL import Image, ImageDraw
import os

# --- CONFIGURATION ---
INPUT_FILE = 'gps.txt'
OUTPUT_FILE = 'map_overlay.png'
MAP_SIZE = 10240
DOT_SIZE = 5            # Increased default size for better visibility
Z_MIN = 500               # Minimum expected elevation
Z_MAX = 1800            # Maximum expected elevation

# --- COLOR GRADIENT CONFIGURATION ---
# We define a "Magma-style" gradient to contrast against browns and cyans.
# Format: (Stop_Value_0_to_1, (R, G, B))
COLOR_STOPS = [
    # (0.0, (45, 0, 75)),    # Deep Purple (Low elevation)
    # (0.5, (220, 20, 60)),  # Crimson/Pink (Mid elevation)
    # (1.0, (255, 165, 0))   # Bright Orange (High elevation)
    (0.0, (0, 51, 204)),    # Dark Blue (Low elevation)
    (0.25, (204, 0, 204)),  # Purple/Pink (Mid elevation)
    (0.5, (0, 153, 51)),  # Green (Mid elevation)
    (0.75, (255, 165, 0)),  # Orange (Mid elevation)
    (1.0, (204, 0, 0))   # Red (High elevation)
]

def get_color_from_z(z):
    """Interpolates between color stops based on Z value."""
    # Normalize Z to a 0.0 - 1.0 range
    val = (z - Z_MIN) / (Z_MAX - Z_MIN)
    val = max(0, min(1, val)) # Clamp between 0 and 1

    # Find the two stops to interpolate between
    for i in range(len(COLOR_STOPS) - 1):
        stop1, color1 = COLOR_STOPS[i]
        stop2, color2 = COLOR_STOPS[i+1]
        
        if stop1 <= val <= stop2:
            # Calculate local interpolation factor
            local_val = (val - stop1) / (stop2 - stop1)
            
            # Linear interpolation for R, G, and B
            r = int(color1[0] + (color2[0] - color1[0]) * local_val)
            g = int(color1[1] + (color2[1] - color1[1]) * local_val)
            b = int(color1[2] + (color2[2] - color1[2]) * local_val)
            return (r, g, b, 255) # Return with full Alpha
            
    return (COLOR_STOPS[-1][1] + (255,))

def create_overlay():
    # 1. Create a blank transparent image
    img = Image.new('RGBA', (MAP_SIZE, MAP_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return

    print(f"Processing {INPUT_FILE} with Z-Gradient...")
    
    count = 0
    with open(INPUT_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            
            try:
                # Parse x, y, z
                parts = line.split(',')
                x = float(parts[0])
                y = float(parts[1])
                z = float(parts[2])

                # 2. Coordinate Transformation (Origin Bottom-Left)
                img_x = x
                img_y = MAP_SIZE - y

                # 3. Get Color based on Z
                dot_color = get_color_from_z(z)

                # 4. Draw the dot
                if DOT_SIZE <= 1:
                    draw.point((img_x, img_y), fill=dot_color)
                else:
                    r = DOT_SIZE / 2
                    draw.ellipse([img_x - r, img_y - r, img_x + r, img_y + r], 
                                 fill=dot_color)
                
                count += 1
            except (ValueError, IndexError):
                print(f"Skipping invalid line: {line}")

    # 5. Save the image
    print(f"Drawing complete. Saving {count} points to {OUTPUT_FILE}...")
    img.save(OUTPUT_FILE, "PNG")
    print("Done. Ready to layer onto your map.")

if __name__ == "__main__":
    create_overlay()