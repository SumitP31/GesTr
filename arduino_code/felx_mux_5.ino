#include <Wire.h>
#include <Arduino_LSM6DS3.h>
#include <light_CD74HC4067.h>

// BOARD CONFIG
const int BAUDRATE = 9600;
const int DELAY_MS = 10;

// MUX CONFIG
const int N_FLEX = 5;
const int SIG_PIN = A0;

// MUX selector pins
const int S0 = 4;
const int S1 = 5;
const int S2 = 6;
const int S3 = 7;

// MUX enable pin (active LOW)
const int NOT_EN = 3;

CD74HC4067 mux(S0, S1, S2, S3);

// ---------------------------
// FILTERING VARIABLES
// ---------------------------
float lpf[N_FLEX] = {0};        // low-pass filtered value
float baseline[N_FLEX] = {0};   // drift baseline
bool initialized = false;

// PARAMETERS
const int OVERSAMPLE_COUNT = 8;
const float ALPHA = 0.12;          // low-pass smoothing
const float DRIFT_ALPHA = 0.003;   // slow drift removal


// ---------------------------
// FLEX SENSOR READ FUNCTION
// ---------------------------
float readFlexFiltered(int ch) {

  mux.channel(ch);
  delayMicroseconds(10);  // allow MUX to settle

  // -------- 1. OVERSAMPLING --------
  long sum = 0;
  for (int i = 0; i < OVERSAMPLE_COUNT; i++) {
    sum += analogRead(SIG_PIN);
  }
  float raw = sum / (float)OVERSAMPLE_COUNT;

  // Init first values
  if (!initialized) {
    lpf[ch] = raw;
    baseline[ch] = raw;
  }

  // -------- 2. LOW-PASS FILTER --------
  lpf[ch] = ALPHA * raw + (1 - ALPHA) * lpf[ch];

  // -------- 3. DRIFT REMOVAL --------
  baseline[ch] = (1 - DRIFT_ALPHA) * baseline[ch] + DRIFT_ALPHA * lpf[ch];

  // Return drift-corrected signal
  return lpf[ch] - baseline[ch];
}


void setup() {
  Serial.begin(BAUDRATE);
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  pinMode(SIG_PIN, INPUT);
  pinMode(NOT_EN, OUTPUT);
  digitalWrite(NOT_EN, LOW);   // enable MUX

  initialized = false;
}


void loop() {
  float x, y, z;

  if (IMU.accelerationAvailable()) {

    // ---------------------------
    // READ ALL FLEX CHANNELS
    // ---------------------------
    for (int ch = 0; ch < N_FLEX; ch++) {
      float flexValue = readFlexFiltered(ch);
      Serial.print(flexValue, 4);
      Serial.print(" ");
    }

    // ---------------------------
    // READ IMU
    // ---------------------------
    IMU.readAcceleration(x, y, z);

    Serial.print(x);
    Serial.print(" ");
    Serial.print(y);
    Serial.print(" ");

    Serial.println();

    initialized = true;
    delay(DELAY_MS);
  }
}
