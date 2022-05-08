from signal import signal, SIGTERM, SIGHUP, pause       #Librería para pantalla LCD
from rpi_lcd import LCD                                 #Librería para Pantalla LCD
from time import sleep                                  #Librería para delay
from w1thermsensor import W1ThermSensor                 #Librería Sensor Temperatura db18b20
import board, busio                                     #Librería para definir pines placa
import adafruit_ads1x15.ads1015 as ADS                  #Librería adafruit para ADS
from adafruit_ads1x15.analog_in import AnalogIn         #Librería adafruit para entrada Análoga

lcd = LCD()                                             #Pantalla LCD

def safe_exit(signum, frame):
    exit(1)

def PantallaLCD(Temp, pH):                              #Función para escribir en pantalla LCD
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)
        lcd.text("T°: " + Temp, 1)                      #Escribe en fila 1 Pantalla
        lcd.text("pH:" + pH, 2)                         #Escribe en fila 2 Pantalla
        pause()
    except KeyboardInterrupt:
        pass
    finally:
        lcd.clear()

#Sensor Temperatura
sensorT = W1ThermSensor()
def Temperatura():                                      #Función que retorna la T° del agua
    TWater = sensorT.get_temperature()
    #print("The temperature is %s celsius" % TWater)
    return TWater

#Conversor ADC
i2c = busio.I2C(board.SCL, board.SDA)                   #Crea bus I2C
ads = ADS.ADS1015(i2c)                                  #Crea el objeto ADC usando I2C
chan1 = AnalogIn(ads, ADS.P0)                           #Crea la entrada Sensor en canal 1
chan2 = AnalogIn(ads, ADS.P1)                           #Crea la entrada Sensor en canal 2

#Sensor pH
def pHSensor():
    print ("Channel0: " + str(chan1.value) + "  "  + str(chan1.voltage))

def ECSensor():
    print ("Channel1: " + str(chan2.value) + "  "  + str(chan2.voltage))

while True:                                             #Bucle
    DatoT = str(Temperatura())                          #Adquiere dato T°
    print("Temperatura: " + DatoT)                      #Imprime dato T°
    pHSensor()                              
    ECSensor()
    #PantallaLCD(Temperatura, "10")                     #Muestra en pantalla los datos de los sensores

