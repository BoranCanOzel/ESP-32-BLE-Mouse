#include <Arduino.h>


enum REC_STATUS
{
    DEV_ADD ,
    REG_ADD ,
    REC_DATA,
    REC_CHECK1,
    REC_CHECK2,
};

enum REC_STATUS  recStatus = DEV_ADD;
uint8_t rf_buf[20];
uint8_t rf_RecCnt = 0;

unsigned int CRC16_2(unsigned char *buf, int len)
{  
    unsigned int crc = 0xFFFF;
    for (int pos = 0; pos < len; pos++)
    {
        crc ^= (unsigned int)buf[pos];    // XOR byte into least sig. byte of crc

        for (int i = len-1; i >= 0; i--)
        {    // Loop over each bit
            if ((crc & 0x0001) != 0) {      // If the LSB is set
                crc >>= 1;                    // Shift right and XOR 0xA001
                crc ^= 0xA001;
            }
            else                            // Else LSB is not set
                crc >>= 1;                    // Just shift right
        }
    }

  return crc;


}

unsigned char CRC16_1(unsigned char *buf, int len)
{  
    unsigned char crc = 0xFF;
    for (int pos = 0; pos < len; pos++)
    {
        crc ^= buf[pos];    // XOR byte into least sig. byte of crc

    }

  return crc;


}

uint8_t GetData()
{
    while (Serial.available()) 
    {
        uint8_t c = Serial.read();
        //Serial.print(c);
        switch (recStatus){
            case DEV_ADD:
                if (c == 0x0F)
                {
                    rf_buf[0] = c;
                    recStatus = REC_DATA;
                    rf_RecCnt = 0;
                }
                //Serial.print("test1");
                break;
            case REC_DATA:
                rf_buf[1 + rf_RecCnt] = c;
                rf_RecCnt ++;
                if (rf_RecCnt >=5)
                    recStatus = REC_CHECK2;
//                    recStatus = REC_CHECK1;

                break;
            case REC_CHECK2:
                rf_buf[6] = c;
                recStatus = DEV_ADD;
                unsigned char crc = CRC16_1(rf_buf, 6);
                
                //Serial.println(crc);
                // Serial.println(high_byte);
                if (crc == rf_buf[6])
                {
                    //Serial.println("checksum is ok");
                    return 1;
                }
                
                break;           
        }
    }

    return 0;
}



