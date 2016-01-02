#include <SPI.h>
#include <Wire.h>
#include <SoftwareSerial.h>
#include <Bridge.h>
#include <SFE_BMP180.h>
#include <RTC_DS3231.h>
#include <mcp3424.h>
#include <Adafruit_ADS1015.h>

#define DEBUG


SoftwareSerial GPS(8, 9);
RTC_DS3231 RTC;

Adafruit_ADS1115 ads1;
Adafruit_ADS1115 ads2(B1001001);

//Quadstat ADC instances and variables
mcp3424 alpha_one;
mcp3424 alpha_two;
float alpha_value;

//BMP Temp and PreGPSure Variables
SFE_BMP180 BMP;

//SHT2 Temp and Humidity Variables
unsigned int temperature_board, humidity_board;
String delimiter = "|";


boolean usingInterrupt = false;
void useInterrupt(boolean); // Func prototype keeps Arduino 0023 happy
uint32_t timer = millis();

void setup() {
  Serial.begin(9600);
  GPS.begin(4800);
  Bridge.begin();
  Wire.begin();
  SPI.begin();
  RTC.begin();
  BMP.begin();
  ads1.begin();
  ads2.begin();
  alpha_one.GetAddress('G', 'F'); //user defined address for the alphasense pstat array (4-stat)
  alpha_two.GetAddress('H', 'H') ;

  useInterrupt(true);
  
  GPS.println("$PTNLSNM,0001,02"); //AddreGPS for GGA outputs. $PTNLSNM,0021,02 for GGA and ZDA
  delay(500);
  GPS.println("$PTNLSNM,0001,02");//AddreGPS for RMC and GGA outputs. "$PTNLSNM,0101,02"
}

void useInterrupt(boolean v) {
  if (v) {
    // Timer0 is already used for millis() - we'll just interrupt somewhere
    // in the middle and call the "Compare A" function above
    OCR0A = 0xAF;
    TIMSK0 |= _BV(OCIE0A);
    usingInterrupt = true;
  } else {
    // do not call the interrupt function COMPA anymore
    TIMSK0 &= ~_BV(OCIE0A);
    usingInterrupt = false;
  }
}

String gps_data;
bool gps_available = false;

// Interrupt is called once a millisecond, looks for any new GPS data, and stores it
SIGNAL(TIMER0_COMPA_vect) {
  if (GPS.available()) {
    char c = GPS.read();
    Serial.print(c);
    if (!gps_available) {
      gps_data += c;
      if (c == '\n') {
        gps_available = true;
      }
    }
  }
}

void loop() {
  String data;
  //Get time from RTC
  DateTime now = RTC.now();
  //Get Quadstat data
  alpha_value = alpha_one.GetValue(1);
  data += alpha_value + delimiter;
  alpha_value = alpha_one.GetValue(2);
  data += alpha_value + delimiter;
  alpha_value = alpha_one.GetValue(3);
  data += alpha_value + delimiter;
  alpha_value = alpha_one.GetValue(4);
  data += alpha_value + delimiter;
  alpha_value = alpha_two.GetValue(1);
  data += alpha_value + delimiter;
  alpha_value = alpha_two.GetValue(2);
  data += alpha_value + delimiter;
  alpha_value = alpha_two.GetValue(3);
  data += alpha_value + delimiter;
  alpha_value = alpha_two.GetValue(4);
  data += alpha_value + delimiter;

  //Get SHT data
  get_SHT2x();

  //Get BMP data
  double T, P;
  char status;
  status = BMP.startTemperature();
  if (status != 0)
  {
    //Serial.println(status);
    delay(status);
    status = BMP.getTemperature(T);
    status = BMP.startPressure(3);
    if (status != 0)
    {
      delay(status);
      status = BMP.getPressure(P, T);
    }
    else //if good temp; but can't compute P
    {
      P = -99;
    }
  }
  else //if bad temp; then can't compute temp or preGPSure
  {
    T = -99;
    P = -99;
  }
  
  data += T + delimiter + P + delimiter + String(now.unixtime()) + delimiter +
          temperature_board + delimiter + humidity_board + delimiter;

  // if millis() or timer wraps around, we'll just reset it
  if (timer > millis())  timer = millis();
  if (millis() - timer > 2000) {
    timer = millis();
    if (gps_available) {
      data += gps_data;
      gps_data = "";
      gps_available = false;
    }
  }
  Serial.println(data);
  Bridge.put("TX-channel", data);
  delay(500);
}

void get_SHT2x()
{
  const int SHT2x_address = 64;
  const byte mask = B11111100;
  const byte temp_command = B11100011;
  const byte hum_command = B11100101;
  byte TEMP_byte1, TEMP_byte2, TEMP_byte3;
  byte HUM_byte1, HUM_byte2, HUM_byte3;
  byte check1, check2;

  Wire.beginTransmission(SHT2x_address);
  Wire.write(temp_command);
  check1 = Wire.endTransmission();

  Wire.requestFrom(SHT2x_address, 3);

  TEMP_byte1 = Wire.read();
  TEMP_byte2 = Wire.read();
  TEMP_byte3 = Wire.read();

  Wire.beginTransmission(SHT2x_address);
  Wire.write(hum_command);
  check2 = Wire.endTransmission();

  Wire.requestFrom(SHT2x_address, 3);
  HUM_byte1 = Wire.read();
  HUM_byte2 = Wire.read();
  HUM_byte3 = Wire.read();

  humidity_board = ( (HUM_byte1 << 8) | (HUM_byte2) & mask ); //HUM_byte1 shifted left by 1 byte, (|) bitwise inclusize OR operator
  temperature_board = ( (TEMP_byte1 << 8) | (TEMP_byte2) & mask );
  //  humidity_SHT = ((125 * (float)humidity_board) / (65536)) - 6.00;
  //  temperature_SHT = ((175.72 * (float)temperature_board) / (65536)) - 46.85;
}
