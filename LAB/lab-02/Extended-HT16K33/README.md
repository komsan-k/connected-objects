# Lab 02 Extention: Interfacing HT16K33 with ESP32 to Control an 8x8 LED Dot Matrix

## Lab Objective

The goal of this lab is to interface the HT16K33 LED driver with the
ESP32 to control an 8x8 LED dot matrix display. By the end of this lab,
you will understand how to use the I²C protocol to communicate with the
HT16K33 and control the individual LEDs on the matrix to display
characters, patterns, and scrolling text.

## Learning Objectives

1.  Understand how to set up and configure the HT16K33 driver for LED
    control.
2.  Learn how to use the I²C communication protocol to send data from
    the ESP32 to the HT16K33.
3.  Control an 8x8 LED matrix display using the HT16K33.
4.  Display static text and simple animations on the LED matrix.
5.  Implement brightness control and LED matrix clearing functions.

## Required Components

-   ESP32 Development Board
-   HT16K33 LED driver
-   8x8 LED dot matrix display
-   Breadboard and jumper wires
-   USB cable for programming the ESP32

## Pre-requisite Knowledge

-   Basic knowledge of I²C communication protocol.
-   Familiarity with Arduino IDE and programming the ESP32.
-   Understanding of how to use libraries like Adafruit GFX for
    graphical display.

## Hardware Setup

1.  **Connections for I²C Communication (HT16K33 to ESP32):**
    -   VCC → 3.3V on ESP32
    -   GND → GND on ESP32
    -   SCL → GPIO 22 on ESP32
    -   SDA → GPIO 21 on ESP32
2.  Connect the LED matrix to the HT16K33 according to its pin layout.
    The HT16K33 handles multiplexing for the LED matrix.

## Procedure

### Step 1: Install Required Libraries

Install the following libraries in Arduino IDE: - Adafruit GFX Library -
Adafruit LED Backpack Library

To install: 1. Open Arduino IDE. 2. Go to **Sketch \> Include Library \>
Manage Libraries**. 3. Search and install: - "Adafruit GFX Library" -
"Adafruit LED Backpack Library"

### Step 2: Example Code

``` cpp
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_LEDBackpack.h>

Adafruit_8x8matrix matrix = Adafruit_8x8matrix();

void setup() {
  Serial.begin(115200);
  matrix.begin(0x70);  
  matrix.setBrightness(10);  
  matrix.clear();
  matrix.writeDisplay();

  matrix.drawPixel(0, 0, LED_ON);
  matrix.drawPixel(7, 0, LED_ON);
  matrix.drawPixel(0, 7, LED_ON);
  matrix.drawPixel(7, 7, LED_ON);
  matrix.writeDisplay();

  delay(2000);
  matrix.clear();
  matrix.writeDisplay();
}

void loop() {
  for (int i = 0; i < 8; i++) {
    matrix.clear();
    matrix.drawLine(0, i, 7, i, LED_ON);
    matrix.writeDisplay();
    delay(500);
  }

  matrix.clear();
  matrix.setCursor(1, 0);
  matrix.print('A');
  matrix.writeDisplay();
  delay(2000);
}
```

### Code Explanation

-   `matrix.begin(0x70)`: Initializes the matrix at I²C address 0x70.\
-   `matrix.setBrightness(10)`: Sets brightness (0--15).\
-   `matrix.drawPixel(x, y, LED_ON)`: Lights a specific pixel.\
-   `matrix.writeDisplay()`: Updates the physical display.\
-   `matrix.clear()`: Clears the display.\
-   `matrix.drawLine()`: Draws a row.\
-   `matrix.print('A')`: Displays a character.

### Step 3: Upload and Test

1.  Connect ESP32 via USB.\
2.  Select correct board and port.\
3.  Upload code.\
4.  Observe LED matrix patterns and characters.

## Lab Experiment

### Experiment 1: Static Text Display

-   Modify code to display a custom character (e.g., initials).\
-   Change brightness using `setBrightness()`.

### Experiment 2: Scrolling Text

-   Modify code for scrolling text using `setCursor()` and `print()`.\
-   Example: scroll your name.

## Lab Assignment

1.  **Custom Patterns**
    -   Use `drawPixel()` to create shapes (e.g., smiley face).
2.  **Display Temperature Data**
    -   Integrate LM35/DHT11 and display readings.
3.  **8x16 Matrix Expansion**
    -   Use two HT16K33 + LED matrices.\
    -   Implement scrolling text across 8x16 display.

------------------------------------------------------------------------

By completing this lab, you will understand interfacing the HT16K33 LED
driver with ESP32, practical I²C communication, brightness control, and
text/animation display on LED matrices.

