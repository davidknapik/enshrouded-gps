
# GPS Logger & Map Visualizer

A two-part toolset designed to extract real-time coordinate data from a running process and visualize it as a high-resolution, color-coded map overlay.

## 📋 Table of Contents
1. [Overview](#-overview)
2. [Setup: Data Logger (Lua)](#1-data-logger-lua)
3. [Setup: Map Renderer (Python)](#2-map-renderer-python)
4. [Coordinate System](#-coordinate-system)
5. [Configuration](#-configuration)

---

## 🔍 Overview
This project provides a workflow for mapping game worlds or software environments:
1.  **Logger (Cheat Engine/Lua):** Hooks into process memory to track X, Y, and Z coordinates. Outputs data to `gps.txt` with a toggleable hotkey.
2.  **Renderer (Python/Pillow):** Processes the raw text data into a 10240x10240 transparent PNG. It uses a **Magma-style color gradient** to represent elevation (Z), designed to contrast against common map colors (browns, cyans, and greys).

---

## 🛠 1. Data Logger (Lua)
The logger runs inside **Cheat Engine**. It monitors specific memory addresses and logs coordinates every *n* seconds.

### Installation
1. Open **Cheat Engine** and attach to your target process.
2. Open file enshrouded.ct in **Cheat Engine**

### Usage
- **Hotkey (F5):** Toggle logging on/off.
- **Output:** Progress is printed to the Lua console and saved to `gps.txt`.

---

## 🐍 2. Map Renderer (Python)
The renderer takes the `gps.txt` file and generates a layered map overlay.

### Prerequisites
Install the required image processing library:
```bash
pip install Pillow
```

### Usage
Place your `gps.txt` in the same directory as the script and run:
```bash
python gps2image.py
```

### Visual Features
- **Transparency:** The output `map_overlay.png` is transparent, allowing it to be layered directly over an existing game map.
- **Elevation Gradient:** Points are colored based on their Z-value (0–2500):
  - **Low:** Dark Blue
  - **Low/Mid:** Purple/Pink
  - **Mid:** Green
  - **Mid/High:** Orange
  - **High:** Red

---

## 📍 Coordinate System
The scripts are calibrated for a **Bottom-Left Origin** system:
- **X-axis:** Positive to the right.
- **Y-axis:** Positive moving up.
- **Z-axis:** Represented by color intensity.

*Note: The Python script automatically handles the flip between mathematical coordinates (bottom-left) and image pixel coordinates (top-left).*

---

## ⚙️ Configuration

### Lua Logger
Modify these variables at the top of the script to match your memory addresses:
```lua
local Xaddr = "enshrouded.exe+1D2C574"
local Zaddr = "enshrouded.exe+1D2C57C"
local Yaddr = "enshrouded.exe+1D2C584"
```

You can also change the capture interval and enable/disable hotkey
```lua
local interval = 2000 -- 2 seconds
local toggleKey = VK_F5 -- Change to VK_INSERT, VK_F1, etc.
```

*Note:
If the game version changes the above address offsets will probably change.
The easist way to find the new offsets is to fast travel to the cinder vault and scan for 3695.

The Cinder Vault coordinates are:
Xcoord: 3695
Ycoord: 1216
Zcoord: 902
*

### Python Renderer
Adjust the visual output by changing these constants:
```python
MAP_SIZE = 10240        # Resolution of the background map
DOT_SIZE = 5            # Thickness of the GPS trail
Z_MIN = 500            # The lowest expected elevation for the gradient
Z_MAX = 1800            # The highest expected elevation for the gradient
```

## 📜 License
This project is licensed under the MIT License - see the LICENSE file for details.