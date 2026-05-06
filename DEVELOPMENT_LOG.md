# Development Log

Date: 2026-05-06

## Project

ESP32 MicroPython project with:

- GPIO16 LED blink / heartbeat output
- SSD1306 I2C OLED display
- Bouncing DVD-style logo animation
- VS Code + uv + mpremote development workflow
- GitHub repository upload

Repository:

https://github.com/411323017-ux/esp32-oled-dvd-logo

## What We Did

### 1. Reviewed the Original Plan

We started from `plan.md`, which described setting up an ESP32 MicroPython development environment with VS Code and uv.

Findings:

- The overall direction was correct.
- The original file mixed conversation text, Python code, and Markdown content.
- Some Markdown code fences were not closed properly.
- Some wording around VS Code MicroPython extensions was too specific and could be misleading.

Result:

- Created a cleaned-up setup guide: `ESP32_MicroPython_Setup_Guide.md`.

### 2. Built the ESP32 MicroPython Project

Created a working MicroPython project under the `esp` folder.

Files added:

- `boot.py`
- `main.py`
- `.vscode/settings.json`
- `README.md`
- `.gitignore`

Environment setup:

- Installed `uv`.
- Created a project virtual environment at `.venv`.
- Installed development tools into `.venv`:
  - `mpremote`
  - `esptool`
  - `micropython-esp32-stubs`

### 3. Implemented GPIO16 LED Blinking

The first device test made GPIO16 output a blinking signal.

Behavior:

- GPIO16 toggled every 500 ms.
- This allowed an external LED to blink.

Wiring used:

```text
GPIO16 -> resistor -> LED anode
LED cathode -> GND
```

Device result:

- ESP32 was detected on `COM7`.
- `mpremote` confirmed the board was running MicroPython.
- `main.py` was uploaded to flash.
- The LED blink worked correctly.

### 4. Implemented OLED DVD Logo Animation

Next, we changed the project from simple LED blink to an OLED animation project.

OLED wiring:

```text
OLED VCC -> 3.3V
OLED GND -> GND
OLED SCL -> GPIO22
OLED SDA -> GPIO21
```

Notes:

- The user described the data pin as `sck` on GPIO21.
- For a typical I2C OLED, this was implemented as `SDA=GPIO21` and `SCL=GPIO22`.

I2C verification:

```text
I2C scan result: 0x3c
```

Implementation:

- Added `ssd1306.py` driver.
- Updated `main.py` to draw a bouncing DVD-style logo on a 128x64 OLED.
- Kept GPIO16 as a small heartbeat status LED.

Current animation behavior:

- OLED shows a `DVD` logo.
- Logo bounces around the display.
- Logo inverts style after hitting an edge.
- GPIO16 toggles every 500 ms as a status heartbeat.

### 5. Uploaded the Program to the ESP32

Uploaded these files to the ESP32 flash:

```text
boot.py
main.py
ssd1306.py
```

Confirmed ESP32 filesystem contents:

```text
boot.py
main.py
ssd1306.py
```

Then reset the board so the OLED animation starts automatically.

### 6. Created and Pushed the GitHub Repository

Initialized a local git repository in the `esp` folder.

Commit created:

```text
Initial ESP32 OLED DVD logo project
```

Remote repository:

```text
https://github.com/411323017-ux/esp32-oled-dvd-logo.git
```

Pushed branch:

```text
main -> origin/main
```

Verified that GitHub contains the project files, including `README.md` and `main.py`.

## Current File Overview

- `README.md`: Project usage and wiring instructions.
- `ESP32_MicroPython_Setup_Guide.md`: Full setup guide for ESP32 MicroPython with VS Code and uv.
- `boot.py`: Minimal boot file.
- `main.py`: OLED DVD logo animation and GPIO16 heartbeat.
- `ssd1306.py`: SSD1306 OLED display driver.
- `.vscode/settings.json`: VS Code Python settings.
- `.gitignore`: Excludes `.venv` and Python cache files.
- `plan.md`: Original plan/reference file.

## Current Hardware Configuration

```text
ESP32 GPIO22 -> OLED SCL
ESP32 GPIO21 -> OLED SDA
ESP32 GPIO16 -> status LED output
OLED address  -> 0x3c
Board port    -> COM7
```

## Useful Commands

Run locally without saving to flash:

```bash
mpremote connect COM7 run main.py
```

Upload to ESP32 flash:

```bash
mpremote connect COM7 cp boot.py :boot.py
mpremote connect COM7 cp ssd1306.py :ssd1306.py
mpremote connect COM7 cp main.py :main.py
mpremote connect COM7 reset
```

Check OLED I2C address:

```bash
mpremote connect COM7 exec "from machine import Pin,I2C; i2c=I2C(0,scl=Pin(22),sda=Pin(21),freq=400000); print([hex(x) for x in i2c.scan()])"
```

## Final Status

The ESP32 project is working and pushed to GitHub.

Current result:

- GPIO16 LED heartbeat works.
- OLED on GPIO22/GPIO21 is detected at `0x3c`.
- The OLED displays the bouncing DVD-style logo animation.
- Project source code is available on GitHub.
