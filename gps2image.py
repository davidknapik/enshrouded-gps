from PIL import Image, ImageDraw
import os

# --- CONFIGURATION ---
INPUT_FILE = 'gps.txt'
OUTPUT_FILE = 'map_overlay.png'
MAP_SIZE = 10240
DOT_SIZE = 5

# --- COLOR GRADIENT CONFIGURATION ---
COLOR_STOPS = [
    (0.0, (0, 51, 204)),    # Dark Blue (Low elevation)
    (0.25, (204, 0, 204)),  # Purple/Pink (Mid elevation)
    (0.5, (0, 153, 51)),    # Green (Mid elevation)
    (0.75, (255, 165, 0)),  # Orange (Mid elevation)
    (1.0, (204, 0, 0))      # Red (High elevation)
]

def get_z_bounds(filename):
    """Reads the file once to determine the actual Min and Max Z values."""
    min_z = float('inf')
    max_z = float('-inf')
    found_data = False

    if not os.path.exists(filename):
        return None, None

    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 3:
                try:
                    z = float(parts[2])
                    if z < min_z: min_z = z
                    if z > max_z: max_z = z
                    found_data = True
                except ValueError:
                    continue
    
    if not found_data:
        return None, None
    
    return min_z, max_z

def get_color_from_z(z, z_min, z_max):
    """Interpolates between color stops based on dynamic Z bounds."""
    # Prevent division by zero if all Z values are the same
    if z_max == z_min:
        val = 0.5
    else:
        val = (z - z_min) / (z_max - z_min)
    
    val = max(0, min(1, val)) # Clamp between 0 and 1

    for i in range(len(COLOR_STOPS) - 1):
        stop1, color1 = COLOR_STOPS[i]
        stop2, color2 = COLOR_STOPS[i+1]
        
        if stop1 <= val <= stop2:
            local_val = (val - stop1) / (stop2 - stop1)
            r = int(color1[0] + (color2[0] - color1[0]) * local_val)
            g = int(color1[1] + (color2[1] - color1[1]) * local_val)
            b = int(color1[2] + (color2[2] - color1[2]) * local_val)
            return (r, g, b, 255)
            
    return (COLOR_STOPS[-1][1] + (255,))

def create_overlay():
    # 1. Determine dynamic Z bounds
    print(f"Scanning {INPUT_FILE} for elevation range...")
    z_min, z_max = get_z_bounds(INPUT_FILE)

    if z_min is None:
        print("Error: No valid Z data found in file.")
        return

    print(f"Detected Z-Range: Min={z_min}, Max={z_max}")

    # 2. Create a blank transparent image
    img = Image.new('RGBA', (MAP_SIZE, MAP_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    print(f"Drawing points...")
    count = 0
    with open(INPUT_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            
            try:
                parts = line.split(',')
                x = float(parts[0])
                y = float(parts[1])
                z = float(parts[2])

                # Coordinate Transformation (Origin Bottom-Left)
                img_x = x
                img_y = MAP_SIZE - y

                # Get Color based on dynamic range
                dot_color = get_color_from_z(z, z_min, z_max)

                # Draw the dot
                if DOT_SIZE <= 1:
                    draw.point((img_x, img_y), fill=dot_color)
                else:
                    r = DOT_SIZE / 2
                    draw.ellipse([img_x - r, img_y - r, img_x + r, img_y + r], 
                                 fill=dot_color)
                
                count += 1
            except (ValueError, IndexError):
                continue

    # 3. Save the image
    print(f"Drawing complete. Saving {count} points to {OUTPUT_FILE}...")
    img.save(OUTPUT_FILE, "PNG")
    print("Done.")

if __name__ == "__main__":
    create_overlay()