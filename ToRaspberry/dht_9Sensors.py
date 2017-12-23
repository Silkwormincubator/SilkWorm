# SISTEMA DE MONITOREO TEMPERATURA Y HUMEDAD, PARA UNA ENCUBADORA DE GUSANOS DE SEDA
# Maestria en Ingenieria Telematica
# Universidad del Cauca, Colombia
# Descripcion  : Programa que permite obtener la lectura de un sensor DHT22
# Lenguaje     : Python
# Autor        : Alejandra Duque Torres

# Importa las librerias necesarias

# Importa las librerias necesarias 
import time
import datetime
import Adafruit_DHT
import subprocess
import apds9301

# Importa la configuracion
sensor=22
pins= [5,6,13,19,26,21,20,16,12]
log_path = "/home/pi/pi-timolo/GoogleDrive/data/"

# Escribe un archivo log en log_path con el nombre en el formato yyyy-mm-dd_dht.log
def write_log(promedios,luxes):
   text = ""     
   for item in promedios:
           text += str(item)+"; "
   if not luxes == None:
      text += str(luxes)
   else:
      text += "0 "
   print text
   log = open(log_path + datetime.datetime.now().strftime("%Y-%m-%d") + "_dht.txt","a")
   line = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " ; " + text + "\n"
   log.write(line)
   log.close()
   subprocess.call(["gdrive push -quiet /home/pi/pi-timolo/GoogleDrive"],shell = True)
   

# Intenta ejecutar las siguientes instrucciones, si falla va a la instruccion except
humedad = [None]*9 
temperatura = [None]*9
promedios = [0.0]*18
retardo = 1 #segudos de retardo
tpromedio = 5*60  #promedio cada 5 minutos
tiempo = 0
nmuestras = 0

try:
   
   # Ciclo principal infinito
   while True:
      # Obtiene la humedad y la temperatura desde el sensor
      startime = time.time()
      for i in range(9):
                        hum, temp = Adafruit_DHT.read_retry(sensor, pins[i])
                        # Si obtiene una lectura del sensor la registra en el archivo log
                        if hum is not None and temp is not None:
                                humedad[i] = hum
                                temperatura[i] = temp
                                print "lectura de sensor "+ str(i)+" "+str(humedad[i])+" % "+ str(temperatura[i])+" c"
                                
                        else:
           
                                print "Error "
                                
        
      # Duerme n segundos
      stoptime = time.time()
      time.sleep(retardo)
      tiempo = tiempo + retardo + (stoptime - startime)
      luxes = 0
      try:
         light = apds9301.adps9300()
         luxes = light.read_lux()
      except:
         print "notligth"
         
      print str(tiempo)+ " Segundos "+str(luxes) + " lux"
      if tiempo >= tpromedio:
              tiempo = tiempo - tpromedio 
              for i in range(18):
                      promedios[i] = promedios[i]/nmuestras
              write_log(promedios,luxes)
              for i in range(18):
                      promedios[i] = 0
              nmuestras = 0
      else:
              nmuestras = nmuestras+1
              for i in range(9):
                      promedios[i] = promedios[i]+temperatura[i]
                      promedios[i+9] = promedios[i+9]+humedad[i]
      

      

# Se ejecuta en caso de que falle alguna instruccion dentro del try
except Exception,e:
   # Registra el error en el archivo log y termina la ejecucion
   print str(e)
   #write_log(str(e))
