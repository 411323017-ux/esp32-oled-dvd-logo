# ESP32 MicroPython OLED DVD Logo

This project runs MicroPython on an ESP32 and shows a bouncing DVD-style logo on an I2C SSD1306 OLED.

## Wiring

- OLED VCC -> 3.3V
- OLED GND -> GND
- OLED SCL -> GPIO22
- OLED SDA -> GPIO21

GPIO16 is still used as a small status LED heartbeat if you keep the previous LED wiring:

- GPIO16 -> resistor -> LED anode
- LED cathode -> GND

## Run without saving to flash

```bash
mpremote connect <PORT> run main.py
```

## Upload to ESP32 flash

```bash
mpremote connect <PORT> cp boot.py :boot.py
mpremote connect <PORT> cp ssd1306.py :ssd1306.py
mpremote connect <PORT> cp main.py :main.py
mpremote connect <PORT> reset
```

Replace `<PORT>` with your ESP32 port, such as `COM3`.
