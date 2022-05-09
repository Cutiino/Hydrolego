from signal import signal, SIGTERM, SIGHUP, pause
from telnetlib import EC                                #Librería para pantalla LCD
from rpi_lcd import LCD                                 #Librería para Pantalla LCD
from time import sleep                                  #Librería para delay
from time import time                                   #Librería para obtener tiempo en Epoch
from w1thermsensor import W1ThermSensor                 #Librería Sensor Temperatura db18b20
import board, busio                                     #Librería para definir pines placa
import adafruit_ads1x15.ads1015 as ADS                  #Librería adafruit para ADS
from adafruit_ads1x15.analog_in import AnalogIn         #Librería adafruit para entrada Análoga

#Pantalla LCD
lcd = LCD()                                             #Define variable pantalla LCD                  

def safe_exit(signum, frame):
    exit(1)

Pantalla = False
def PantallaLCD(Temp, pH, EC):                          #Función para escribir en pantalla LCD
    global Pantalla
    if (Pantalla == True):
        print("Mostrando datos en pantalla")
        tiempoPantalla = tiempo
        TempP = str(round(Temp, 2))
        pHP = str(round(pH, 2))
        ECP = str(round(EC, 2))
        try:
            signal(SIGTERM, safe_exit)
            signal(SIGHUP, safe_exit)
            lcd.text("T:" + TempP + " EC:" + ECP, 1)     #Escribe en fila 1 Pantalla            
            lcd.text("pH:" + pHP, 2)                     #Escribe en fila 2 Pantalla
            Pantalla = False
        except:
            print("Error en pantalla LCD")
            lcd.clear()

#Sensor Temperatura
sensorT = W1ThermSensor()
def Temperatura():                                      #Función que retorna la T° del agua
    TWater = sensorT.get_temperature()
    #TWater = round(TWater, 2)                           #Redondea T° a la centesima
    print("Temperatura: " + str(TWater))
    return TWater

#Conversor ADC
i2c = busio.I2C(board.SCL, board.SDA)                   #Crea bus I2C
ads = ADS.ADS1015(i2c)                                  #Crea el objeto ADC usando I2C
chan0 = AnalogIn(ads, ADS.P0)                           #Crea la entrada Sensor en canal 1
chan1 = AnalogIn(ads, ADS.P1)                           #Crea la entrada Sensor en canal 2

def ECSensor():
    EcVoltage = chan0.voltage                           #Obtiene valor voltage sensor EC
    #EcMuestra = round(EcMuestra, 2)                     #Redondea valor voltage a la centesima
    print ("Channel 0: " + str(EcVoltage)  + "[V]")
    ECMuestra = EcVoltage*7594.04 - 29.8676             #Ecuación para pasar de [V] a [us/cm]       
    print ("EC: " + str(ECMuestra)  + "[us/cm]")
    return ECMuestra

#Sensor pH
def pHSensor():
    pHVoltage = chan1.voltage                           #Obtine valor voltage sensor EC
    #pHMuestra = round(pHMuestra, 2)                     #Redondea valor voltage a la centesima
    print ("Channel 1: " + str(pHVoltage) + "[V]")
    pHMuestra = pHVoltage*-5.859 + 15.99                #Ecuación para pasar voltage a pH
    print ("pH: " + str(pHMuestra))
    return pHMuestra

#Promedios
borrarProm = True
def promSensores(Temp, pH, EC, tiempoProm):             #Función para adquirir promedio datos en un tiempo
    global muestras, tiempoSensores, promT              #Defincion variables globales
    global promEC, prompH, Pantalla, borrarProm         #Defincion variables globales
    promedioDatos = [0, 0, 0]                           #Creación lista para retornar promedios valores
    if (borrarProm == True):                            #Inicialización de valores prom
        muestras = 0
        promT = 0
        promEC = 0
        prompH = 0
        borrarProm = False
        tiempoSensores = tiempoProm
    Intervalo = 15                                      #Variable de tiempo para obtener las muestras en seg
    if (tiempoProm - tiempoSensores < 15):              
        promT = promT + Temp                            #Suma cada muestra de Temperatura
        promEC = promEC + EC                            #Suma cada muestra de EC
        prompH = prompH + pH                            #Suma cada muestra de pH
        muestras = muestras + 1                         #Lleva la cantidad de muestras que se han obtenido
    else:
        promT = promT/muestras                          #Calcula promedio Temperatura
        prompH = prompH/muestras                        #Calcula promedio pH
        promEC = promEC/muestras                        #Calcula promedio EC
        borrarProm = True                               #Habilita que variables se reinicien para siguiente intervalo
        Pantalla = True                                 #Habilita datos se muestren en Pantalla
        promedioDatos [0] = promT                       #Se meten en una lista promedio Temperatura
        promedioDatos [1] = prompH                      #Se meten en una lista promedio pH
        promedioDatos [2] = promEC                      #Se meten en una lista promedio EC
        print("\nPromedio T: " + str(promT))
        print("Promedio pH: " + str(prompH))
        print("Promedio EC: " + str(promEC) + "\n")
    return promedioDatos                                #Retorna en una lista los promedios

while True:                                             #Bucle
    tiempo = time()
    datoT = Temperatura()                               #Adquiere dato T°
    datoEC = ECSensor()                                 #Adquiere dato EC
    datopH = pHSensor()                                 #Adquiere dato pH
    media = promSensores(datoT, datopH, datoEC, tiempo) #Saca promedio datos cada 15s
    #media = [Temperatura, pH, EC]
    PantallaLCD(media[0], media[1], media[2])           #Muestra en pantalla los datos de los sensores
    
