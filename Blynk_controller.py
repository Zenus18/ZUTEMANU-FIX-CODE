import BlynkLib
import time
from AQIStatus import IAQ_score

# Inisialisasi koneksi ke server Blynk
BLYNK_AUTH = 'Ndbjz_ixYUFhE1Xid1t9wO6FmlTCwoTK'
blynk = BlynkLib.Blynk(BLYNK_AUTH, server="blynk.cloud", port=80)

# Fungsi untuk mengirim data ke Blynk
def send_to_blynk(AQI, AQI_STATUS, GAS_RESISTANCE, PRESSURE, TEMPERATURE, HUMIDITY):
    try:
        score = IAQ_score(AQI)
        if score >= 201:
            blynk.log_event("very_bad_aqi")
        elif 151 <= score <= 200:
            blynk.log_event("bad_aqi")
        blynk.virtual_write(1, AQI)
        blynk.virtual_write(2, AQI_STATUS)
        blynk.virtual_write(3, HUMIDITY)
        blynk.virtual_write(4, TEMPERATURE)
        blynk.virtual_write(5, PRESSURE)
        blynk.virtual_write(6, GAS_RESISTANCE) 
        print("Data berhasil diunggah ke Blynk")
    except Exception as e:
        print("Terjadi kesalahan:")
        print(e)
        pass
def blynk_main(AQI, AQI_STATUS, GAS_RESISTANCE, PRESSURE, TEMPERATURE, HUMIDITY):
    blynk.run()
    send_to_blynk(AQI, AQI_STATUS, GAS_RESISTANCE, PRESSURE, TEMPERATURE, HUMIDITY)

