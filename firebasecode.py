import adafruit_dht
import RPi.GPIO as GPIO
import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import pyrebase
from time import sleep

# Firebase configuration
firebase_config = {
    "apiKey": "YOUR_API_KEY",
    "authDomain": "YOUR_AUTH_DOMAIN",
    "databaseURL": "YOUR_DATABASE_URL",
    "projectId": "YOUR_PROJECT_ID",
    "storageBucket": "YOUR_STORAGE_BUCKET",
    "messagingSenderId": "YOUR_MESSAGING_SENDER_ID",
    "appId": "YOUR_APP_ID"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

# Define pin for LDR
LDR_PIN = 27

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Initialize DHT11 sensor
dht11 = adafruit_dht.DHT11(board.D17)

# Initialize I2C bus and ADC
i2c = board.I2C()
ads = ADS.ADS1115(i2c, address=0x48)

# Define analog input channel for LDR sensor
LDR_SENSOR_CHANNEL = 1
ldr_sensor = AnalogIn(ads, LDR_SENSOR_CHANNEL)

# Define analog input channel for rain sensor
RAIN_SENSOR_CHANNEL = 0
rain_sensor = AnalogIn(ads, RAIN_SENSOR_CHANNEL)

# Function to read sensor data
def read_sensor_data():
    try:
        temperature = dht11.temperature
        humidity = dht11.humidity
        ldr_value = ldr_sensor.value
        rain_sensor_value = rain_sensor.value
        return temperature, humidity, ldr_value, rain_sensor_value
    except Exception as e:
        print("Error reading sensor data:", e)
        return None, None, None, None

while True:
    try:
        temperature, humidity, ldr_value, rain_sensor_value = read_sensor_data()
        if temperature is not None:
            print("Temperature: {:.1f}°C".format(temperature))
        if humidity is not None:
            print("Humidity: {:.1f}%".format(humidity))
        if ldr_value is not None:
            print("LDR Sensor Value: {}".format(ldr_value))
        if rain_sensor_value is not None:
            print("Rain Sensor Value: {}".format(rain_sensor_value))

        # Upload data to Firebase
        data = {
            "temperature": temperature,
            "humidity": humidity,
            "ldr_value": ldr_value,
            "rain_sensor_value": rain_sensor_value
        }
        db.child("sensor_data").set(data)
        
        sleep(1)
    except Exception as e:
        print("Error:", e)
