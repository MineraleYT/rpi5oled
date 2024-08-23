# Originally Created by: Michael Klements
# Modified by MinerAle
import time
import psutil as PS
import socket
import board
import digitalio
import adafruit_ssd1306
import gpiod
from PIL import Image, ImageDraw, ImageFont
import sys

# Constants
KB = 1024
MB = KB * 1024
GB = MB * 1024
WIDTH = 128
HEIGHT = 64
FONTSIZE = 16
LOOPTIME = 1.0

# GPIO Setup
chip = gpiod.Chip('gpiochip0')
reset_line = chip.get_line(17)  # Update this to a pin that is free

def get_ipv4_from_interface(interfacename):
    """Get IPv4 address from a specified network interface."""
    try:
        iface = PS.net_if_addrs().get(interfacename, [])
        for addr in iface:
            if addr.family == socket.AF_INET:
                return f"IP {addr.address}"
    except Exception as e:
        print(f"Error getting IP from {interfacename}: {e}")
    return "IP ?"

def signal_handler(sig, frame):
    """Handle signals to ensure proper cleanup."""
    print("Signal received, cleaning up...")
    cleanup()
    sys.exit(0)

def get_ipv4():
    """Get the first non-loopback IPv4 address."""
    for iface_name, iface_addrs in PS.net_if_addrs().items():
        if iface_name != "lo":  # Ignore loopback interface
            for addr in iface_addrs:
                if addr.family == socket.AF_INET:
                    return f"IP {addr.address}"
    return "IP ?"

def turn_off_display():
    """Turn off the display."""
    oled.fill(0)
    oled.show()

def cleanup_gpio():
    """Clean up GPIO resources."""
    reset_line.release()

def cleanup():
    """Clean up display and GPIO before exit."""
    turn_off_display()
    cleanup_gpio()

def signal_handler(sig, frame):
    """Handle signals to ensure proper cleanup."""
    cleanup()
    sys.exit(0)

# Setup I2C and OLED display
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

# Create blank image for drawing
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype('Caramel-Regular.otf', FONTSIZE)

try:
    while True:
        # Clear the image
        draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

        # Get system information
        IP = get_ipv4()
        CPU = f"CPU {PS.cpu_percent():.1f}%"
        
        # Handling temperature data
        temps = PS.sensors_temperatures().get('cpu_thermal', [])
        TEMP = "TEMP ?°C"
        if temps:
            cpu_temp = temps[0]
            TEMP = f"{cpu_temp.current:.1f}°C" if hasattr(cpu_temp, 'current') else "TEMP ?°C"
        
        mem = PS.virtual_memory()
        MemUsage = f"Mem {mem.used // MB:5}/{mem.total // MB:5}MB"
        root = PS.disk_usage("/")
        Disk = f"Disk {root.used // GB:4}/{root.total // GB:4}GB"

        # Draw text on the display
        draw.text((0, 0), IP, font=font, fill=255)
        draw.text((0, FONTSIZE), CPU, font=font, fill=255)
        draw.text((80, FONTSIZE), TEMP, font=font, fill=255)
        draw.text((0, 2 * FONTSIZE), MemUsage, font=font, fill=255)
        draw.text((0, 3 * FONTSIZE), Disk, font=font, fill=255)

        # Update display
        oled.image(image)
        oled.show()
        time.sleep(LOOPTIME)

except KeyboardInterrupt:
    cleanup()