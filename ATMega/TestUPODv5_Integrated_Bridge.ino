#include <SPI.h>
#include <Wire.h>
#include <SoftwareSerial.h>
#include <Bridge.h>
#include <SFE_BMP180.h>
#include <RTC_DS3231.h>
#include <mcp3424.h>
#include <Adafruit_ADS1015.h>

SoftwareSerial GPS(8, 9);
RTC_DS3231 RTC;

//On-Board ADC instances and variables
Adafruit_ADS1115 ads1;
Adafruit_ADS1115 ads2(B1001001);
int ADC1;

//Quadstat ADC instances and variables
mcp3424 alpha_one;
mcp3424 alpha_two;
float alpha_value;

//BMP Temp and Pressure Variables
SFE_BMP180 BMP;

//SHT2 Temp and Humidity Variables
unsigned int temperature_board, humidity_board;

//Interrupt for GPS
void useInterrupt(boolean); // Func prototype keeps Arduino 0023 happy
uint32_t timer = millis();
String gps_data;
bool gps_available = false;

//Wind direction sensor(Potentiometer) on analog pin 0
const byte WDIR = A0;

//Wind speed variables
long lastWindCheck = 0;
volatile long lastWindIRQ = 0;
volatile byte windClicks = 0;

//Data delimieter for Bridge string
String delimiter = "#";

// Function called anemometer interrupt (2 ticks per rotation), attached to input D4
void wspeedIRQ()
{
  if (millis() - lastWindIRQ > 10) // Ignore switch-bounce glitches less than 10ms (142MPH max reading) after the reed switch closes
  {
    lastWindIRQ = millis(); //Grab the current time
    windClicks++; //There is 1.492MPH for each click per second.
  }
}

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
  attachInterrupt(4, wspeedIRQ, FALLING); //anemometer reed switch on pin 7--> interrupt# 4
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
  } else {
    // do not call the interrupt function COMPA anymore
    TIMSK0 &= ~_BV(OCIE0A);
  }
}

// Interrupt is called once a millisecond, looks for any new GPS data, and stores it
SIGNAL(TIMER0_COMPA_vect) {
  if (GPS.available()) {
    char c = GPS.read();
    //    Serial.print(c);
    if (!gps_available) {
      gps_data += c;
      if (c == '\n') gps_available = true;
    }
  }
}

void loop() {
  String data;

  //Get time from RTC
  DateTime now = RTC.now();


  //Get SHT data
  const byte temp_command = B11100011;
  const byte hum_command = B11100101;
  temperature_board = read_wire(temp_command);
  humidity_board = read_wire(hum_command);
  float humidity_SHT = ((125 * (float)humidity_board) / (65536)) - 6.00;
  float temperature_SHT = ((175.72 * (float)temperature_board) / (65536)) - 46.85;

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

  data += String(now.unixtime()) + delimiter + T + delimiter + P + delimiter +
          temperature_SHT + delimiter + humidity_SHT + delimiter +
          String(getS300CO2()) + delimiter + String(get_wind_speed()) +
          delimiter + String(analogRead(A0)) + delimiter;
          
  //Read ADCs on-board and on-Quadstat
  for (int i = 1; i <= 16; i++) {
    if (i <= 4) data += alpha_one.GetValue(i) + delimiter;
    else if (i <= 8) data += alpha_two.GetValue(i - 4) + delimiter;
    else if (i <= 12) data += ads1.readADC_SingleEnded(i - 9) + delimiter;
    else if (i <= 16) data += ads2.readADC_SingleEnded(i - 13) + delimiter;
  }
  
  //Get GPS data
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

  //DEBUG Serial print and send data to Atheros over Bridge
  Serial.println(data);
  Bridge.put("TX-channel", data);
  //QuadStat takes 11 seconds to sample. No need for delay in main loop
}

float getS300CO2()
{
  int i = 1;
  long reading;
  //float CO2val;
  wire_setup(0x31, 0x52, 7);

  while (Wire.available())
  {
    byte val = Wire.read();
    if (i == 2)
    {
      reading = val;
      reading = reading << 8;
    }
    if (i == 3)
    {
      reading = reading | val;
    }
    i = i + 1;
  }

  //Shift Calculation to Atheros
  //    CO2val = reading / 4095.0 * 5000.0;
  //    CO2val = reading;
  return reading;
}

void wire_setup(int address, byte cmd, int from) {
  Wire.beginTransmission(address);
  Wire.write(cmd);
  Wire.endTransmission();
  Wire.requestFrom(address, from);
}

unsigned int read_wire(byte cmd) {
  const int SHT2x_address = 64;
  const byte mask = B11111100;
  byte byte1, byte2, byte3;

  wire_setup(SHT2x_address, cmd, 3);

  byte1 = Wire.read();
  byte2 = Wire.read();
  byte3 = Wire.read();

  //HUM_byte1 shifted left by 1 byte, (|) bitwise inclusize OR operator
  return ( (byte1 << 8) | (byte2) & mask );
}

//Returns the instataneous wind speed
float get_wind_speed()//Will be modified from Sparkfun's Example
{
  float deltaTime = millis() - lastWindCheck; //750ms

  deltaTime /= 1000.0; //Covert to seconds

  float windSpeed = (float)windClicks / deltaTime; //3 / 0.750s = 4

  windClicks = 0; //Reset and start watching for new wind
  lastWindCheck = millis();

  windSpeed *= 1.492; //4 * 1.492 = 5.968MPH

  return (windSpeed);
}
