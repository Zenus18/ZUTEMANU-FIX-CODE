from gpiozero import Buzzer
buzzer = Buzzer(23)
import time
def bip():
        buzzer.on()
        time.sleep(1)  # Waktu nyala buzzer (suara "beeb")
        buzzer.off()
        time.sleep(1) 