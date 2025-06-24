# 🔢 Raspberry Pi 4-bit ALU with I2C LCD & GPIO Buttons

This project demonstrates a low-level binary calculator built using a **Raspberry Pi**, **I2C LCD display**, and **7 GPIO buttons**, emulating basic ALU (Arithmetic Logic Unit) operations in real-time.

---

## 📌 Features

- ✅ Input 4-bit binary numbers using toggle buttons
- ✅ Real-time binary + decimal preview on LCD
- ✅ Choose operation: `ADD`, `SUB`, `AND`, `OR`, `XOR` via navigation buttons
- ✅ View result in `Binary`, `Octal`, or `Hex` (with Decimal shown alongside)
- ✅ Designed for educational use: demonstrates how basic binary operations work at the bit level

---

## 🧰 Hardware Required

| Component           | Quantity | Notes                            |
|--------------------|----------|----------------------------------|
| Raspberry Pi (any) | 1        | GPIO header required             |
| Push Buttons        | 7        | For 4-bit input + navigation     |
| I2C 16x2 LCD        | 1        | With PCF8574 backpack module     |
| Resistors (10kΩ)    | 7        | Pull-down for buttons (optional) |
| Jumper wires        | ~20      | Male-to-female for GPIO header   |
| Breadboard          | 1        | For easy prototyping             |

---

## 🖥️ GPIO Pin Assignments

| Function         | GPIO Pin | Physical Pin |
|------------------|----------|--------------|
| Enter Button      | 21       | 40           |
| Left Button       | 20       | 38           |
| Right Button      | 6        | 31           |
| Bit 0 Button      | 16       | 36           |
| Bit 1 Button      | 26       | 37           |
| Bit 2 Button      | 19       | 35           |
| Bit 3 Button      | 13       | 33           |
| LCD SDA           | 2        | 3 (I2C SDA)  |
| LCD SCL           | 3        | 5 (I2C SCL)  |

---

## ⚙️ How It Works

### 1️⃣ Input Stage
- The user sets 4 bits (A and B) using 4 dedicated toggle buttons.
- Bit state is displayed on the LCD in real-time as binary and decimal.
- Pressing the **Enter** button locks in the input.

### 2️⃣ Operation Selection
- The user navigates through `ADD`, `SUB`, `AND`, `OR`, `XOR` using **Left** and **Right** buttons.
- The **Enter** button confirms the selected operation.

### 3️⃣ Format Selection
- The user chooses how the result is displayed:
  - **BIN**: Binary (with decimal shown)
  - **OCT**: Octal (with decimal shown)
  - **HEX**: Hexadecimal (with decimal shown)

### 4️⃣ Result Display
- The selected operation is performed.
- Result is shown for 10 seconds on the LCD in the selected format **+ decimal** (e.g., `0x15 = 21`).

---

## 💡 Bit-Level Logic

- Each button press toggles a bit between 0 and 1.
- Operations are done in **5-bit logic** to support overflow results (e.g., `15 + 15 = 30`).
- Subtraction wraps using:  
  ```python
  result = (a - b) % 32
