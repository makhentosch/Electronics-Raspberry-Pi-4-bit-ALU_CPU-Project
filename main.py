import RPi.GPIO as GPIO
import time
from smbus2 import SMBus
from RPLCD.i2c import CharLCD

# --- GPIO Setup ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pin mappings
bit_buttons = [16, 26, 19, 13]  # Bit 0 to Bit 3
enter_button = 21
left_button = 12
right_button = 6

all_buttons = bit_buttons + [enter_button, left_button, right_button]

# Setup button pins
for pin in all_buttons:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# LCD setup
lcd = CharLCD('PCF8574', 0x27)
lcd.clear()

# Utility functions
def read_buttons_state(bits):
    """Returns 4-bit integer from bit button states."""
    binary = [bits[i] for i in range(4)]
    return int(''.join(str(b) for b in binary), 2)

def wait_for_press(pin):
    while GPIO.input(pin) == GPIO.LOW:
        time.sleep(0.01)
    time.sleep(0.2)  # Debounce

def wait_for_release(pin):
    while GPIO.input(pin) == GPIO.HIGH:
        time.sleep(0.01)

def get_4bit_input(label):
    bits = [0, 0, 0, 0]
    lcd.clear()
    lcd.write_string(f"Input {label}:")
    lcd.crlf()
    lcd.write_string("0000 = 0")

    while True:
        # Display current input
        binary_str = ''.join(str(b) for b in bits)
        dec_val = read_buttons_state(bits)
        lcd.cursor_pos = (1, 0)
        lcd.write_string(f"{binary_str} = {dec_val:<3}    ")

        # Check bit toggle buttons
        for i, pin in enumerate(bit_buttons):
            if GPIO.input(pin) == GPIO.HIGH:
                bits[i] ^= 1
                wait_for_release(pin)

        # Check for enter
        if GPIO.input(enter_button) == GPIO.HIGH:
            wait_for_release(enter_button)
            return bits

        time.sleep(0.05)

def select_mode():
    modes = ['ADD', 'SUB', 'AND', 'OR', 'XOR']
    index = 0

    lcd.clear()
    lcd.write_string("Select Mode:")
    lcd.crlf()
    lcd.write_string(f"> {modes[index]}   ")

    while True:
        if GPIO.input(left_button) == GPIO.HIGH:
            index = (index - 1) % len(modes)
            lcd.cursor_pos = (1, 0)
            lcd.write_string(f"> {modes[index]}   ")
            wait_for_release(left_button)

        if GPIO.input(right_button) == GPIO.HIGH:
            index = (index + 1) % len(modes)
            lcd.cursor_pos = (1, 0)
            lcd.write_string(f"> {modes[index]}   ")
            wait_for_release(right_button)

        if GPIO.input(enter_button) == GPIO.HIGH:
            wait_for_release(enter_button)
            return index

        time.sleep(0.05)

def choose_display_format():
    formats = ['BIN', 'OCT', 'HEX']
    index = 0

    lcd.clear()
    lcd.write_string("Output Format:")
    lcd.crlf()
    lcd.write_string(f"> {formats[index]}   ")

    while True:
        if GPIO.input(left_button) == GPIO.HIGH:
            index = (index - 1) % len(formats)
            lcd.cursor_pos = (1, 0)
            lcd.write_string(f"> {formats[index]}   ")
            wait_for_release(left_button)

        if GPIO.input(right_button) == GPIO.HIGH:
            index = (index + 1) % len(formats)
            lcd.cursor_pos = (1, 0)
            lcd.write_string(f"> {formats[index]}   ")
            wait_for_release(right_button)

        if GPIO.input(enter_button) == GPIO.HIGH:
            wait_for_release(enter_button)
            return index

        time.sleep(0.05)

def perform_operation(a_bits, b_bits, mode):
    a = int(''.join(str(b) for b in a_bits), 2)
    b = int(''.join(str(b) for b in b_bits), 2)

    if mode == 0:  # ADD
        result = a + b
    elif mode == 1:  # SUB
        result = (a - b) % 32  # simulate 5-bit wrap-around
    elif mode == 2:  # AND
        result = a & b
    elif mode == 3:  # OR
        result = a | b
    elif mode == 4:  # XOR
        result = a ^ b
    else:
        result = 0

    return result

def display_result(result, format_index):
    lcd.clear()
    lcd.write_string("Result:")

    if format_index == 0:  # BIN
        formatted = f"{result:05b} = {result}"
    elif format_index == 1:  # OCT
        formatted = f"{oct(result)} = {result}"
    elif format_index == 2:  # HEX
        formatted = f"{hex(result)} = {result}"
    else:
        formatted = str(result)

    lcd.crlf()
    lcd.write_string(formatted)
    time.sleep(10)


# --- Main Execution ---
try:
    while True:
        a_bits = get_4bit_input("A")
        b_bits = get_4bit_input("B")
        mode = select_mode()
        result = perform_operation(a_bits, b_bits, mode)
        format_index = choose_display_format()
        display_result(result, format_index)


except KeyboardInterrupt:
    pass

finally:
    lcd.clear()
    GPIO.cleanup()

