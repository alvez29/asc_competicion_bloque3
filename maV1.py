# 0 > n > 1
# m = 2
# p = 30
import math
import numpy as np
import random
from deap import benchmarks

#Inicializa los vectores peso
def inicializa_vectores_peso(n):
    i = 0
    j = n-1
    lista_vectores = []
    for i in range(n):
        e1 = i * (1/(n-1))
        e2 = j * (1/(n-1))
        j = j - 1
        v = [e1, e2]
        lista_vectores.append(v)
    return lista_vectores

#Calcula la distancia euclidea entre dos vectores
def calcular_distancia_euclidea(v1, v2):
    dist = math.sqrt(((v2[0]-v1[0]) ** 2) + ((v2[1]-v1[1]) ** 2))
    return dist

#Devuelve un diccionario que vincula cada elemento de la lista de vectores con la distancia a todos sus vectores vecinos
def calcular_distancias(vector):
    res = {}
    for i in range(len(vector)):
        res[i] = []
        for j in range(len(vector)):
            res[i].append(calcular_distancia_euclidea(vector[i], vector[j]))
    return res

#Calcula el conjunto B con los T vectores mas cercanos a los vectores peso
def calcular_conjunto_b(vectores_peso,distancias, t):
    n = len(distancias.keys())
    b_set = []
    for i in range(n):
        idx = np.array(distancias[i]).argsort()[:t]
        aux = []
        for j in range(len(idx)):
            aux.append(idx[j])
        b_set.append(aux)

    return b_set        
        
def funct():
    return benchmarks.zdt3([1,1,1,1,1,0.5])

#Calcular la poblacion
def inicializar_poblacion(n, seed):
    random.seed(seed)
    poblacion = []
    for i in range(n):
        individuo = []
        for j in range(30):
            aux = random.random()
            individuo.append(aux)
        poblacion.append(individuo)
    return poblacion

#Evalua la poblacion con la funcion zdt3
def evaluar_poblacion(poblacion):
    res = []
    for i in range(len(poblacion)):
        individuo_eval = evaluar_individuo(poblacion[i])
        res.append(individuo_eval)
    return res

def evaluar_individuo(individuo):
    return benchmarks.zdt3(individuo)

def calcular_z(evaluaciones):
    res = []
    menor_1 = 100
    menor_2 = 100
    for i in range(len(evaluaciones)):
        x = evaluaciones[i][0]
        y = evaluaciones[i][1]
        if x < menor_1:
            menor_1 = x
        if y < menor_2:
            menor_2 = y
    res.append(menor_1)
    res.append(menor_2)
    return res

def actualizar_z(eval_hijo, z_actual):

    res = z_actual

    if eval_hijo[0]<res[0]:
        res[0] = eval_hijo[0]
    if eval_hijo[1]<res[1]:
        res[1] = eval_hijo[1]
    
    return res

#Calcula el valor gte para un individuo
def gte(individuo, peso, z):
    evaluado = evaluar_individuo(individuo)
    val1 = peso[0] * abs(evaluado[0] - z[0])
    val2 = peso[1] * abs(evaluado[1] - z[1])

    return np.amax([val1, val2])

def algoritmo_total(n, g, porcentaje_t, xl, xu, seed):
    t = int(porcentaje_t * n)
    print('Inicialización del algoritmo:')
    print('T es '+ str(t)+'\n')
    print('Calculando los vectores pesos iniciales...')
    vectores_peso = inicializa_vectores_peso(n)
    print('Vectores peso calculados.')
    print('Calculando las distancias de los vectores y sus vecinos...')
    distancias = calcular_distancias(vectores_peso)
    print('Distancias calculadas. \n')
    print('Calculando vector B...')
    conjunto_b = calcular_conjunto_b(vectores_peso,distancias, t)
    print('Vector B calculado.')
    print('Inicializando población...')
    poblacion = inicializar_poblacion(n, seed)
    print('Población inicializada')
    print('Evaluando población inicial...')
    evaluaciones = evaluar_poblacion(poblacion)
    print('Evaluaciones calculadas.')
    z = calcular_z(evaluaciones)
    print('El punto Z de referencia es: ' + str(z))

    f = open('ma_all_p'+str(n)+'g'+str(g)+'_seed'+str(float(seed)).replace('.','')+'.out', 'w')

    for generacion in range(g):
        for i in range(n):
            individuo = poblacion[i]
            hijo = []

            #Mutación

            indice_vecinos_aleatorios = random.sample(conjunto_b[i], 3)
            vecinos_aleatorios = []
            
            for indice in indice_vecinos_aleatorios:
                vecinos_aleatorios.append(poblacion[indice])
            
            vector_mutante = np.array(vecinos_aleatorios[0]) + 0.5 * (np.array(vecinos_aleatorios[1]) - np.array(vecinos_aleatorios[2]))
            vector_mutante = vector_mutante.tolist()
            
            #Recortamos los limites
            for vm in range(len(vector_mutante)):
                if vector_mutante[vm] > xu:
                    vector_mutante[vm] = xu
                if vector_mutante[vm] < xl:
                    vector_mutante[vm] = xl

            #Cruce
            delta = random.randint(0, len(individuo))
            for u in range(len(individuo)):
                aleatorio = random.random()
                if aleatorio<=0.5 or u == delta:
                    hijo.append(vector_mutante[u])
                elif aleatorio>0.5:
                    hijo.append(individuo[u])

            #Evaluación del hijo
            eval_hijo = evaluar_individuo(hijo)

            #Actualización de z
            z = actualizar_z(eval_hijo, z)

            indice_vecinos = conjunto_b[i]

            for indice_del_vecino in indice_vecinos:
                gte_hijo = gte(hijo,vectores_peso[indice_del_vecino],z)
                gte_vecino = gte(poblacion[indice_del_vecino], vectores_peso[indice_del_vecino], z)
                if gte_hijo <= gte_vecino:
                    poblacion[indice_del_vecino] = hijo

        
        for individuo in poblacion:
            punto = evaluar_individuo(individuo)
            f.write(str(punto[0]) + ' ' + str(punto[1]) + ' 0.0' +'\n')

    f.close()    

    f2 = open('ma_plot_p'+str(n)+'g'+str(g)+'_seed'+str(float(seed)).replace('.','')+'.out', 'w')
    for evaluacion_final in evaluar_poblacion(poblacion):
        f2.write(str(evaluacion_final[0]) +' '+ str(evaluacion_final[1])+'\n')
    f2.close()
    return poblacion

#Realiza el algoritmo para todas las semillas con paso 0.1
wi = 0.0
while i <= 1 :
    if(wi.__round__(1) == 1):
        algoritmo_total(49, 100 , 0.2, 0, 1, 0.99)
    else:
        algoritmo_total(40, 100 , 0.2, 0, 1, wi.__round__(1))

    wi = wi+0.1

