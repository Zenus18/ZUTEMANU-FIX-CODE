from gpiozero import LED 
from beep import bip
import beep
red = LED(26)
yellow = LED(19)
green = LED(13)
def IAQ_score(score):
    score = (100 - score) * 5
    return score

def calculate_IAQ(score):
    IAQ_text = ""
    score = (100 - score) * 5

    if score >= 301:
        IAQ_text += "Hazardous"
        red.on()
        yellow.off()
        green.off()
    elif 201 <= score <= 300:
        IAQ_text += "Very Unhealthy"
        red.on()
        yellow.off()
        green.off()
    elif 176 <= score <= 200:
        IAQ_text += "Unhealthy"
        red.off()
        yellow.on()
        green.off()
        beep.buzzer.off()
    elif 151 <= score <= 175:
        IAQ_text += "Almost Unhealthy"
        red.off()
        yellow.on()
        green.off()
        beep.buzzer.off()
    elif 51 <= score <= 150:
        IAQ_text += "Moderate"
        red.off()
        yellow.off()
        green.on()
        beep.buzzer.off()
    elif 0 <= score <= 50:
        IAQ_text += "Good"
        red.off()
        yellow.off()
        green.on()
        beep.buzzer.off()
    return IAQ_text