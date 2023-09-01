import bme680
import RPi.GPIO as GPIO
import blynklib
import time
import requests
import threading
from gpiozero import Buzzer
from gpiozero import LED 
import beep
from payload import *
from AQIScoring import *
from AQIStatus import *
import AQIStatus
from RPi_GPIO_i2c_LCD import lcd
from mqtt_upload import publish_to_mqtt
from Blynk_controller import *
temperature = 0
humidity = 0
pressure = 0
gas_resistance = 0
IAQ_text = ""
AQI_score = 0
i2c_address = 0x27
lcdDisplay = lcd.HD44780(i2c_address)

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# Fungsi untuk menampilkan data di LCD display
def display_data_on_lcd():
    while True:
        if sensor.data.heat_stable:
            lcdDisplay.set("Temp: {}  C        ".format(temperature), 1)
            lcdDisplay.set("Hum : {} %        ".format(humidity), 2)
            time.sleep(4)
            lcdDisplay.set("Press:{:.0f}  hPa      ".format(pressure), 1)
            if gas_resistance:
                lcdDisplay.set("Gas :{:.0f} Ohms    ".format(gas_resistance), 2)
            time.sleep(4)
            lcdDisplay.set(IAQ_text + "                ", 1)
            lcdDisplay.set("AQI: {:.3f}         ".format(AQI_score), 2)
        time.sleep(4)  # Tampilkan data setiap 1 detik

# Buat thread untuk tampilan LCD display
lcd_thread = threading.Thread(target=display_data_on_lcd)
lcd_thread.daemon = True
lcd_thread.start()
def bip_thread():
    time.sleep(2)
    while True:
        score = IAQ_score(AQI_score)
        if score >= 301:
            bip()
        elif 201 <= score <= 300:
            bip()
        time.sleep(1)
bip_threading = threading.Thread(target=bip_thread)
bip_threading.daemon = True
bip_threading.start()
# def Blynk():
#     try:
#         while True:
#             if check_internet_connection():
#                 send_to_blynk(AQI_score, IAQ_text, gas_resistance, pressure, temperature, humidity)
#             time.sleep(1)
#     except:
#         pass
# Blynk_threading = threading.Thread(target=Blynk())
# Blynk_threading.daemon = True
# Blynk_threading.start()
print('Calibration data:')
for name in dir(sensor.calibration_data):
    if not name.startswith('_'):
        value = getattr(sensor.calibration_data, name)
        if isinstance(value, int):
            print('{}: {}'.format(name, value))

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

print('\n\nInitial reading:')
for name in dir(sensor.data):
    value = getattr(sensor.data, name)
    
    if not name.startswith('_'):
        print('{}: {}'.format(name, value))

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# Fungsi untuk memeriksa koneksi internet
def check_internet_connection():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        if response.status_code == 200:
            return True
    except:
        pass
    return False

print('\n\nPolling:')
try:
    while True:
        if sensor.get_sensor_data():
            temperature = sensor.data.temperature
            pressure = sensor.data.pressure
            humidity = sensor.data.humidity
            output = '\ntemperature : {0:.2f} C \npressure : {1:.2f} hPa \nhumidity: {2:.2f} %'.format(
                temperature,
                pressure,
                humidity)
            gas_resistance = sensor.data.gas_resistance
            get_gas_reference(gas_resistance)
            hum_score = humidity_score(humidity)
            gas_score = get_gas_score()
            AQI_score = hum_score + gas_score
            IAQ_text = calculate_IAQ(AQI_score)
            print('Humidity score :', hum_score)
            print('Gas score :', gas_score)
            print('Air quality score :', AQI_score)
            print('Air quality in room is ' + IAQ_text)
            print('{0} \n gas resistance : {1}  Ohms'.format(
                    output,
                    gas_resistance))
                
            payload = {
                    "temperature": temperature,
                    "humidity": humidity,
                    "pressure": pressure,
                    "gas": gas_resistance,
                    "air_quality_score": AQI_score
                }
            if check_internet_connection():
                send_to_ubidots(payload)
                blynk_main(AQI_score, IAQ_text, gas_resistance, pressure, temperature,humidity)
                # publish_to_mqtt("SIC/ZUTEMANU/AQI", AQI_score)
                # publish_to_mqtt("SIC/ZUTEMANU/TEMP", temperature)
                # publish_to_mqtt("SIC/ZUTEMANU/HUMIDITY", humidity)
                # publish_to_mqtt("SIC/ZUTEMANU/PRESSURE", pressure)
                # publish_to_mqtt("SIC/ZUTEMANU/GAS_RESISTANCE", gas_resistance)
                # publish_to_mqtt("SIC/ZUTEMANU/AQI_TEXT", IAQ_text)
            else:
                pass
        time.sleep(0.5)
except KeyboardInterrupt:
    beep.buzzer.off()
    AQIStatus.green.off()
    AQIStatus.red.off()
    AQIStatus.yellow.off()
    lcdDisplay.clear()

