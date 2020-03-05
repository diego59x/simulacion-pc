# Diego Alvarez 19498
# Simulacion de un sistema operativo

import simpy
import random
import statistics
# Variables
prom = 0 # promedio
desvest = 0 #desviacion estandar
env = simpy.Environment() #ambiente de simulación
RAM = simpy.Container(env, init=100, capacity=100)#cantidad de ram
cpus = simpy.Resource(env,capacity = 2)#Cantidad de CPU
tiempototal = 0


def pc(num,instr,env,tiempo_llegada,RAM,cpus):
    global listiempos #tiempo por proceso
    global tiempototal #tiempo total
    random_ram = 0 # ram para cada proceso
    instrN = 0 # instrucciones despues de pasar por el proceso
    yield env.timeout(tiempo_llegada)
    # momento en el que llega a la pc
    horaLlegada = env.now 
    
    #---------------- New ----------------  
    
    #---------------- Ready ---------------- 
    # simular que necesita RAM para ejecutarse.
    if RAM.level < random_ram:
            # Debe esperar va la cola de para asignar ram
            print('proceso %s Esperando por ram... ' % num)
            #yield env.timeout(10)  # Verificar cada 10 segundos
    else:
        random_ram = random.randint(1,1)
    
    tiempoEje = random_ram
    # Se verifica que exista memoria ram para llevarse acabo
    
    
    print ('proceso %s necesita %d de ram para ejecutarse' % (num,tiempoEje))
    
    
    #---------------- Running ---------------- 
    # ahora se dirige a la pc,
    # pero si hay otros procesos, debe hacer cola 
    with RAM.get(random_ram) as turno:
        yield turno      #ya llego al pc
        yield env.timeout(tiempoEje) #se esta ejecutando
        
        instrN = instr - 3
        with cpus.request() as simular:
            yield simular
            # si hay instrucciones menores a 3 se obtendria un numero negativo
            # por eso se hace que se haga cero
            if(instrN <= 0):
                instrN = 0
            yield env.timeout(1)
            print("proceso %s tiempo de ejecucion %f" % (num,env.now))
            #---------------- Waiting ---------------- 
            io = random.randint(1,2)
            if(io == 2):
                yield env.timeout(1)
         #Si se tienen menos de tres       
        if instrN<3:
            yield env.timeout(1)
        RAM.put(random_ram)#Se regresa a la ram lo utilizado
        print ('proceso %s entra con %f instrucciones sale de la pc con %d instrucciones' % (num, instr, instrN))

    
    # se guarda el tiempo total del proceso
    tiempoTotal = env.now - horaLlegada
    # se guarda cada tiempo para calcular la desviacion estandar luego
    listiempos = list()
    listiempos.append(tiempoTotal)
    print ('proceso %s se tardo %f en ejecutarse' % (num, tiempoTotal))
    # se guarda el tiempo total de la simulacion 
    tiempototal = tiempototal + tiempoTotal

  
    
# ---------------------------
# Simulacion
numprocesos = 200
for i in range(numprocesos):
    env.process(pc(i,random.randint(1,10),env,random.expovariate(1.0/1),RAM,cpus))
env.run()  #correr la simulación hasta que termine
# se calcula el promedio
prom = tiempototal/numprocesos
print ("tiempo promedio por proceso es: ", prom)
# se calcula la desviacion estandar 
for i in listiempos:
    desvest = ((i-prom)*(i-prom))/numprocesos
print ("desviacion estandar es: ", desvest)




