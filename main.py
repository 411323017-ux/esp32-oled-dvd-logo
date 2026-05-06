import machine
import time

import ssd1306


OLED_WIDTH = 128
OLED_HEIGHT = 64
I2C_SCL_PIN = 22
I2C_SDA_PIN = 21
I2C_FREQ = 400_000

STATUS_LED_PIN = 16
OLED_ADDRESS = 0x3C
FRAME_DELAY_MS = 35

LOGO_WIDTH = 44
LOGO_HEIGHT = 20


i2c = machine.I2C(
    0,
    scl=machine.Pin(I2C_SCL_PIN),
    sda=machine.Pin(I2C_SDA_PIN),
    freq=I2C_FREQ,
)

devices = i2c.scan()
if devices:
    OLED_ADDRESS = devices[0]

display = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, OLED_ADDRESS)
status_led = machine.Pin(STATUS_LED_PIN, machine.Pin.OUT)


def draw_dvd_logo(x, y, inverted):
    color = 0 if inverted else 1
    background = 1 if inverted else 0

    display.fill_rect(x, y, LOGO_WIDTH, LOGO_HEIGHT, background)
    display.text("DVD", x + 9, y + 2, color)
    display.hline(x + 8, y + 13, 28, color)
    display.hline(x + 11, y + 15, 22, color)
    display.hline(x + 16, y + 17, 12, color)

    display.pixel(x + 6, y + 14, color)
    display.pixel(x + 37, y + 14, color)
    display.pixel(x + 9, y + 16, color)
    display.pixel(x + 34, y + 16, color)


x = 7
y = 5
dx = 2
dy = 1
inverted = False
last_led_tick = time.ticks_ms()
led_state = 0

display.fill(0)
display.show()

while True:
    display.fill(0)
    draw_dvd_logo(x, y, inverted)
    display.show()

    x += dx
    y += dy

    bounced = False
    if x <= 0:
        x = 0
        dx = abs(dx)
        bounced = True
    elif x >= OLED_WIDTH - LOGO_WIDTH:
        x = OLED_WIDTH - LOGO_WIDTH
        dx = -abs(dx)
        bounced = True

    if y <= 0:
        y = 0
        dy = abs(dy)
        bounced = True
    elif y >= OLED_HEIGHT - LOGO_HEIGHT:
        y = OLED_HEIGHT - LOGO_HEIGHT
        dy = -abs(dy)
        bounced = True

    if bounced:
        inverted = not inverted

    now = time.ticks_ms()
    if time.ticks_diff(now, last_led_tick) >= 500:
        led_state = 0 if led_state else 1
        status_led.value(led_state)
        last_led_tick = now

    time.sleep_ms(FRAME_DELAY_MS)
