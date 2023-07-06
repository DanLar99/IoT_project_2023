from time import sleep
from machine import Pin
from functions import *
import time
import dht

LED_Pin_Red = Pin(0, Pin.OUT)
LED_Pin_Green = Pin(1, Pin.OUT)
LED_Pin_Blue = Pin(2, Pin.OUT)
push_button = Pin(22, Pin.IN, Pin.PULL_UP)
temp_hum_time_start = time.time()
water_time_start = time.time()
tempSensor = dht.DHT11(Pin(27))
drinks = 0
LED_Pin_Red.value(0)
LED_Pin_Green.value(0)
LED_Pin_Blue.value(0)

while True:
    temp_hum_time_end = time.time()
    water_time_end = time.time()
    button_state = push_button.value()

    # Drinking water logic
    if water_time_end - water_time_start > 3600:
        LED_Pin_Red.value(0)
        LED_Pin_Green.value(0)
        LED_Pin_Blue.value(1)
        while button_state == True:
            print("Get up, do some stretching, and drink a glass of water! Press the button when you're done.")
            button_state = push_button.value()
            sleep(0.1)
        
        LED_Pin_Blue.value(0)
        water_time_start = time.time()
        drinks += 1
        while button_state == False:
            print("Let go of the button!")
            button_state = push_button.value()
            sleep(0.1)
        
        returnValue = sendData("my-first-device", "Drinks", drinks)

    # Temperature & humidity logic
    if temp_hum_time_end - temp_hum_time_start > 300:
        temp_hum_time_start = time.time()
        tempSensor.measure()
        temperature = tempSensor.temperature()
        humidity = tempSensor.humidity()
        print("Temperature is {} degrees Celsius and Humidity is {}%".format(temperature, humidity))
        returnValue = sendData("my-first-device", "Temperature", temperature)
        returnValue = sendData("my-first-device", "Humidity", humidity)

        if temperature >= 23 or (temperature >= 20 and humidity >= 55):
            LED_Pin_Red.value(1)
            LED_Pin_Green.value(0)
            LED_Pin_Blue.value(0)
            while button_state == True:
                print("It's getting hot in here, turn on the fan! Press the button when you're done.")
                button_state = push_button.value()
                sleep(0.1)
        
            LED_Pin_Red.value(0)
            while button_state == False:
                print("Let go of the button!")
                button_state = push_button.value()
                sleep(0.1)

    sleep(0.1)