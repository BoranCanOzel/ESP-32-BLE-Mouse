#include <Arduino.h>
#include "crc.h"
#include <BleMouse.h>
#include <esp_bt.h>
#include <esp_gap_ble_api.h>


BleMouse bleMouse("Logitech Wireless", "BLE Mouse", 100);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(3000000);

  bleMouse.begin();
  // Set the MAC address
  uint8_t logitechMacAddress[6] = {0x00, 0x0d, 0xb5, 0x78, 0x12, 0x34};
  esp_base_mac_addr_set(logitechMacAddress);
  Serial.println("bluetooth router started");

}

void loop() {

  if (GetData() == 1)
  {
    //Serial.println("Mouse event is generated");
    if (bleMouse.isConnected())
    {
      uint8_t command = rf_buf[1] & 0x03;
      short x = (rf_buf[2] << 8 ) |  rf_buf[3];
      short y = (rf_buf[4] << 8 ) |  rf_buf[5];
      if (command == 0x01) // button event
      {
          int buttonEvent = (rf_buf[1] >> 6);
          if (buttonEvent == 0)  // right button is released
          {
            Serial.println("right button is released");
            bleMouse.release(MOUSE_RIGHT);
          }
          else if (buttonEvent == 2)  // right button is pressed
          {
              Serial.println("right button is pressed");
              bleMouse.press(MOUSE_RIGHT);
          }
          else if (buttonEvent == 1)  // left button is released
          {
              Serial.println("left button is released");
              bleMouse.release(MOUSE_LEFT);

          }          
          else if (buttonEvent == 3)  // left button is pressed
          {
              Serial.println("left button is pressed");
              bleMouse.press(MOUSE_LEFT);
          }
      }
      else if (command == 0x02) // wheel event
      {
          //short delta = (rf_buf[2] << 8 ) |  rf_buf[3];
          //Serial.println(delta);
          bleMouse.move(0,0, x, y);
          
      }
      else if (command == 0x03) // mouse move event     
      {
          //short x = (rf_buf[3] << 8 ) |  rf_buf[4];
          //short y = (rf_buf[5] << 8 ) |  rf_buf[6];
          // int8_t x = rf_buf[2];
          // int8_t y = rf_buf[3];

          // // Serial.println(x);
          // // Serial.println(y);
          
          bleMouse.move(x,y);
          
      }
    }
  }
}