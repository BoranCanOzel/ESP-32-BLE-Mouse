
# 🖱️ ESP32 Bluetooth Mouse

This repository contains the code to turn an ESP32 into a Bluetooth mouse. The ESP32 reads data via serial communication, processes it, and uses BLE (Bluetooth Low Energy) to act as a mouse. A Python program is used to forward mouse actions from a second PC to the ESP32.

## 🔧 Functionality

### ESP32

The ESP32 firmware reads mouse data from a serial port, processes the data, and sends corresponding mouse actions via Bluetooth to a connected device. The key functionalities include:

- **Mouse Movement**: Move the mouse cursor based on received x and y coordinates.
- **Button Events**: Simulate mouse button presses and releases (left and right buttons).
- **Wheel Events**: Simulate mouse wheel scrolling.

### Python Program

A Python program running on a second PC captures mouse actions and forwards them to the ESP32 via serial communication. The program includes:

- **Mouse Movement Capture**: Captures and forwards mouse movement.
- **Button Press Capture**: Captures and forwards mouse button press and release events.
- **Wheel Event Capture**: Captures and forwards mouse wheel scroll events.

## 📂 Files

- **main.cpp**: The main entry point of the ESP32 firmware. Initializes the BLE mouse and processes incoming serial data.
- **crc.cpp**: Contains the CRC (Cyclic Redundancy Check) functions used for validating the integrity of the received data.
- **crc.h**: Header file for `crc.cpp`.
- **window.py**: Handles window creation and mouse event hooking.
- **Comm.py**: Manages serial communication and data transfer.
- **constants.py**: Defines various constants used throughout the program.
- **devices.py**: Manages device registration and raw input handling.
- **SoftwareMouse.py**: Implements the SoftwareMouse class for mouse actions.
- **structures.py**: Defines various data structures used for raw input and device information.

## 📜 Code Snippets

### `main.cpp`
```cpp
#include <Arduino.h>
#include "crc.h"
#include <BleMouse.h>
#include <esp_bt.h>
#include <esp_gap_ble_api.h>

BleMouse bleMouse("Logitech Wireless", "BLE Mouse", 100);

void setup() {
  Serial.begin(3000000);
  bleMouse.begin();
  uint8_t logitechMacAddress[6] = {0x00, 0x0d, 0xb5, 0x78, 0x12, 0x34};
  esp_base_mac_addr_set(logitechMacAddress);
  Serial.println("Bluetooth router started");
}

void loop() {
  if (GetData() == 1) {
    if (bleMouse.isConnected()) {
      uint8_t command = rf_buf[1] & 0x03;
      short x = (rf_buf[2] << 8 ) |  rf_buf[3];
      short y = (rf_buf[4] << 8 ) |  rf_buf[5];
      if (command == 0x01) { // button event
        int buttonEvent = (rf_buf[1] >> 6);
        if (buttonEvent == 0) bleMouse.release(MOUSE_RIGHT);
        else if (buttonEvent == 2) bleMouse.press(MOUSE_RIGHT);
        else if (buttonEvent == 1) bleMouse.release(MOUSE_LEFT);
        else if (buttonEvent == 3) bleMouse.press(MOUSE_LEFT);
      }
      else if (command == 0x02) { // wheel event
        bleMouse.move(0, 0, x, y);
      }
      else if (command == 0x03) { // mouse move event     
        bleMouse.move(x, y);
      }
    }
  }
}
```

### `crc.cpp`
```cpp
#include <Arduino.h>

enum REC_STATUS {
    DEV_ADD,
    REG_ADD,
    REC_DATA,
    REC_CHECK1,
    REC_CHECK2,
};

enum REC_STATUS recStatus = DEV_ADD;
uint8_t rf_buf[20];
uint8_t rf_RecCnt = 0;

unsigned int CRC16_2(unsigned char *buf, int len) {  
    unsigned int crc = 0xFFFF;
    for (int pos = 0; pos < len; pos++) {
        crc ^= (unsigned int)buf[pos];
        for (int i = len - 1; i >= 0; i--) {
            if ((crc & 0x0001) != 0) {
                crc >>= 1;
                crc ^= 0xA001;
            }
            else crc >>= 1;
        }
    }
    return crc;
}

unsigned char CRC16_1(unsigned char *buf, int len) {  
    unsigned char crc = 0xFF;
    for (int pos = 0; pos < len; pos++) {
        crc ^= buf[pos];
    }
    return crc;
}

uint8_t GetData() {
    while (Serial.available()) {
        uint8_t c = Serial.read();
        switch (recStatus) {
            case DEV_ADD:
                if (c == 0x0F) {
                    rf_buf[0] = c;
                    recStatus = REC_DATA;
                    rf_RecCnt = 0;
                }
                break;
            case REC_DATA:
                rf_buf[1 + rf_RecCnt] = c;
                rf_RecCnt++;
                if (rf_RecCnt >= 5) recStatus = REC_CHECK2;
                break;
            case REC_CHECK2:
                rf_buf[6] = c;
                recStatus = DEV_ADD;
                unsigned char crc = CRC16_1(rf_buf, 6);
                if (crc == rf_buf[6]) return 1;
                break;           
        }
    }
    return 0;
}
```
