#Lenguaje para Computación Cuántica
#Enrique Cingolani - 24/11/2019 - 2023

#20/02/2021 agregada función qubit_bloch()
#02/04/22 agregada funcion medir()
#03/04/22 agregada funcion graficar()
#11/04/22 agregada funcion fase()
#14/04/22 modificada graficar() para agregar fases
#15/04/22 agregada medirEnsamble() para realizar n mediciones de un sistema
#30/04/22 agregada normalizar()
#22/05/22 agregada colapsar()
#22/06/22 agregada groverUs()
#06/07/22 agregada reset()
#11/09/22 agregada cxNqubit()
#07/02/23 agregada graf3D()


from .matrices import *
import math
import random
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

ver = vermatrizf

#Qubits |0> y |1> en la base z
ket0 = [[1],[0]]
ket1 = [[0],[1]]

bra0 = [[1,0]]
bra1 = [[0,1]]

#Sistemas de 2 qubits
ket00 = tensorial(ket0,ket0)
ket01 = tensorial(ket0,ket1)
ket10 = tensorial(ket1,ket0)
ket11 = tensorial(ket1,ket1)

bra00 = trasponer(ket00)
bra01 = trasponer(ket01)
bra10 = trasponer(ket10)
bra11 = trasponer(ket11)

#Compuerta Reset (irreversible) pone qubits |0> o |1> en estado |0>
Rst=[[1,1],[0,0]]

#Clifford Group
  #Matriz Identidad
I=[[1,0],[0,1]]

  #Matrices de Pauli
X=[[0,1],[1,0]]
Y=[[0,complex(0,-1)],[complex(0,1),0]]
Z=[[1,0],[0,-1]]

  #Operador de Hadamard
H=[[2**(-0.5),2**(-0.5)],[2**(-0.5),-2**(-0.5)]]

  #Rotacion pi/2 alrededor del eje z
S=[[1,0],[0,complex(0,1)]]
Sdg=[[1,0],[0,complex(0,-1)]]

 #Rotacion pi/4 alrededor del eje z
T=[[1,0],[0,math.e**complex(0,math.pi/4)]]
Tdg=[[1,0],[0,math.e**complex(0,-math.pi/4)]]

 #CNOT o Controlled NOT o XOR
Cx=[[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]]

 #I-CNOT Controlled NOT Invertida Controlada por el 2do.qubit
Xc=[[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]]

 #Oraculos cuánticos (Matrices asociadas a las 4 funciones boleanas f de 1 entrada)
    # f(0)=0 , f(1)=0
U00 = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

    # f(0)=0 , f(1)=1
U01 = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]

    # f(0)=1 , f(1)=0
U10 = [[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

    # f(0)=1 , f(1)=1
U11 = [[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
    #se construye haciendo: U11=sumar(
    #sumar(multiplicar(ket00,bra01),multiplicar(ket01,bra00)),
    #sumar(multiplicar(ket10,bra11),multiplicar(ket11,bra10)) )

 #Oraculo cuántico (Matriz asociada a la función f AND de 2 entradas)
    # f(0,0)=0, f(0,1)=0, f(1,0)=0, f(1,1)=1 ; NO balanceada
Uand2 = [[1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 0]]

 #Oraculo cuántico (Matriz asociada a la función f XOR de 2 entradas)
    # f(0,0)=0, f(0,1)=1, f(1,0)=1, f(1,1)=0 ; Balanceada
Uxor2 = [[1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 1]]

 #Oraculo cuántico (Matriz asociada a la función f constante=1 de 2 entradas)
    # f(0,0)=1, f(0,1)=1, f(1,0)=1, f(1,1)=1 ; Constante (siempre=1)
Ucte2 = [[0, 1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 0]]

## Funciones ##

def h(v):
    return(multiplicar(H, v))

def x(v):
    return(multiplicar(X, v))

def y(v):
    return(multiplicar(Y, v))

def z(v):
    return(multiplicar(Z, v))

def s(v):
    return(multiplicar(S, v))

def sdg(v):
    return(multiplicar(Sdg, v))

def t(v):
    return(multiplicar(T, v))

def tdg(v):
    return(multiplicar(Tdg, v))

def cx(v0, v1):
    R = multiplicar(Cx, tensorial(v0,v1))
    return(R)

def xc(v0, v1):
    R = multiplicar(Xc, tensorial(v0,v1))
    return(R)


def cxNqubit(cantqubits, control, target): # Retorna compuerta Controled Not del qubit control al qubit target
                                           # para un nqubit, q0,q1,....q(cantqubits-1)
    if (cantqubits < 2 or control >= cantqubits or target >=cantqubits or control==target): #chequea si hay errores
        return(0)
    filas=int(2**cantqubits)
    R = I                      # Matriz Identidad 2x2
    for j in range (cantqubits-1):
        R = tensorial(I, R)    #  Matriz Identidad 2^cantqubits x 2^cantqubits
    for f in range (filas):
        b = format(f,"b").zfill(cantqubits) # arma código binario ('000...' a '111...'
        if(b[control]=="1"):   # si qubit control == 1
            valort = eval(b[target]) ^ 1 # b[target] XOR 1
            columna = 0
            for j in range(cantqubits):
                if j != target:
                    columna += eval(b[j]) * 2**(cantqubits-1-j)
            columna += valort * (2**(cantqubits-1-target)) #columna con un 1 en la fila
            for c in range (filas):
                if c==columna:
                    R[f][c]=1
                else:
                    R[f][c]=0
    return(R)


def proba(M):   #Matriz de probabilidades
    R=[]
    for i in range (len(M)):
        R.append([])
        for j in range (len(M[0])):
            modulo = M[i][j]*M[i][j].conjugate()
            R[i].append(modulo.real)
    return(R)

def rotar(radianes):  #Matriz de rotacion de radianes alrededor del eje z (Phase gate P)
    R=[[1,0],[0,math.e**complex(0,radianes)]]
    return(R)

def f(radianes, vector):  #Phase shift (rotar vector alrededor de Z)
	return(multiplicar(rotar(radianes),vector))

def medir(qubit):   #Operador de medición de un n-qubit
    posicion=[]
    probas = proba(trasponer(qubit))[0] #array de probas (peso) de cada estado
    for i in range (len(qubit)):
        posicion.append(i)      #array con posiciones numericas de cada estado (0 a n-1)
    m = random.choices(posicion, weights=probas)[0] #elige estado random según peso
    q=[]
    for i in range (len(qubit)):        #rearma qubit del estado medido
        q.append([])
        if i == m:
            q[i].append(1)
        else:
            q[i].append(0)
    return(q)

def medirEnsamble(nqubit, repeticiones): #Mide repeticiones veces para estadística
    mediciones=[]  #Vector para sumar los resultados de cada medición
    for i in range (len(nqubit)):  #inicializa en 0
        mediciones.append([])
        mediciones[i].append(0)
    for i in range (repeticiones):  #Mide y suma el resultado a mediciones
        mediciones = sumar(mediciones, medir(nqubit))
    return(mediciones)      #Retorna vector suma de mediciones para cada estado


def fase(vector):   #Calcula las fases de cada componente de un vector de estado
    if (len(vector[0]) > 1): #si no es vector columna retorna 0 y termina
        return(0)
    f=[]
    for i in range (len(vector)):   #rearma qubit del estado medido
        f.append([])
        f[i].append(math.degrees(math.atan2(vector[i][0].imag,vector[i][0].real)))
    return(f)

def normalizar(vector):   #Normaliza amplitudes de un vector para convertirlo en un qubit
    if (len(vector[0]) > 1): #si no es vector columna retorna 0 y termina
        return(0)
    q = []
    p = proba(vector)
    norma = 0
    for i in range (len(p)):
        norma += p[i][0]
    norma = math.sqrt(norma)        #raiz cuadrada de la suma de las probas de c/estado
    if(norma > 0):              #si la norma > 0
        for i in range (len(vector)):   #rearma qubit correspondiente al vector de entrada
            q.append([])
            q[i].append(vector[i][0]/norma)
    else:                       #si la norma==0 no puede normalizar vector
        q = 0                   #y retorna 0 (error)
    return(q)


def colapsar(vector, qubitNro, valor):   #Retorna qubit resultante después de medir qubitNro con valor 0 o 1
    if (len(vector[0]) != 1): #si no es vector columna retorna 0 y termina
        return(0)
    digitos=int(math.log(len(vector),2))
    q=[]
    for i in range (len(vector)):   # para cada elemento del vector de entrada
        ib=format(i,"b").zfill(digitos) # arma código binario ('000...' a '111...')
        q.append([])
        if(eval(ib[qubitNro])==valor):  # pasa estados que correspondan
            q[i].append(vector[i][0])   # con su valor de amplitud
        else:
            q[i].append(0)              # y el resto los deja con amplitud 0
    return(normalizar(q))           # Retorna qubit resultante normalizado


def reset(vector, qubitNro):    #Retorna qubit resultante después de resetear qubitNro a estado |0>
                            #OJO Funciona MAL para estados con fases negativas pq Rst no los reseta, por ejemplo al |->
    cantqubits=int(math.log(len(vector),2)) #cantidad de qubits del vector
    if ((len(vector[0]) != 1) or (qubitNro >= cantqubits)): #si no es vector columna o qubitNro fuera de rango retorna 0 y termina
        return(0)
    Rn = Rst                    #matriz para resetear un 1qubit a estado |0>
    for i in range (cantqubits):  #arma la matriz para resetear el qubitNro del vector
        if(i<qubitNro):
            Rn = tensorial(I,Rn)
        elif(i>qubitNro):
            Rn = tensorial(Rn,I)
    q = normalizar(multiplicar(Rn, vector)) #resetea el qubitNro del vector y normaliza
    return(q)                               #retorna el nuevo vector con el qubitNro en estado |0>
    

def graficar(nqubit):   #Grafica nqubit (amplitudes vector de estado, probas y fases)
    if (len(nqubit[0]) > 1): #si no es vector columna retorna 0 y termina
        return(0)
    digitos=int(math.log(len(nqubit),2))
    eje_x = []
    eje_y1 = trasponer(nqubit)[0]
    eje_y2 = trasponer(proba(nqubit))[0]
    eje_y3 = trasponer(fase(nqubit))[0]
    for i in range (len(nqubit)):
        ib=format(i,"b").zfill(digitos)
        eje_x.append(ib)
        eje_y1[i]=((eje_y1[i]*eje_y1[i].conjugate())**0.5).real

    fig, (w1, w2, w3) = plt.subplots(3,1)  #Figura con 3 gráficos en 3 filas 1 columna
    fig.suptitle("Vector de estado del qubit")

    #fila 1 columna 1 Ventana 1
    p1 = w1.bar(eje_x, eje_y1, label="Amplitudes", color="blue")
    w1.legend(loc='best')
    w1.set_ylim(0, 1.1)
    w1.bar_label(p1, label_type='center')
    
    #fila 2 columna 1 Ventana 2
    p2 = w2.bar(eje_x, eje_y2, label="Probabilidades", color="orange")
    w2.legend(loc='best')
    w2.set_ylim(0, 1.1)
    w2.bar_label(p2, label_type='center')

    #fila 3 columna 1 Ventana 3
    p3 = w3.bar(eje_x, eje_y3, label="Fases", color="red")
    w3.legend(loc='best')
    w3.set_ylim(-190, 190)
    w3.axhline(0, color='grey', linewidth=1)
    w3.bar_label(p3, label_type='center')

    plt.show()
    return


def graf3D(matriz, titulo="Elementos de la Matriz"):   #Grafica amplitudes de matriz (parte real) en 3D
    filas = len(matriz)
    columnas = len(matriz[0])
    if (filas < 1 or columnas < 1): #si no es matriz o vector retorna 0 y termina
        return(0)
    eje_x = []
    eje_y = []
    eje_z = []
    dx = []
    dy = []
    dz = []
    for f in range (filas):
        for c in range (columnas):
            eje_x.append(f) #posiciones de las base de las barras
            eje_y.append(c)
            eje_z.append(0)
            dx.append(1)    #ancho, profundidad y altura de barras
            dy.append(1)
            dz.append(matriz[f][c].real) #grafica valores reales

    fig = plt.figure()
    fig.suptitle(titulo)
    ax1 = fig.add_subplot(111, projection='3d')
    ax1.bar3d(eje_x, eje_y, eje_z, dx, dy, dz)
    ax1.set_xlabel("Fila")
    ax1.set_ylabel("Columna")
    
    plt.show()
    return


def deutsch(Uf, q1=ket0, q2=ket1):  #Algoritmo de DEUTSCH (debe ser q12=ket01)
    q12=tensorial(q1, q2)   #Uf = oraculo booleano U00, U01, U10 o U11
    H2=tensorial(H, H)
    HI=tensorial(H, I)
    vermatrizf(multiplicar(HI, multiplicar(Uf, multiplicar(H2,q12))))
    return

def djozsa(Ufn):  #Algoritmo de DEUTSCH-JOSZA de n entradas (n + ket1 auxiliar)
                #Ufn = matriz 2^(n+1)*2^(n+1) (oraculo función booleana de n entradas)
    if (len(Ufn)==len(Ufn[0])):
        q = ket1
        Hn = H
        n = int(math.log2(len(Ufn)))-1
        for i in range(n):   # CUIDADO! se trabaja con matrices de 2^(n+1)*2^(n+1)
            q = tensorial(ket0, q)
            HmI = tensorial(Hn, I)  # HmI = Hn ant x I
            Hn = tensorial(H, Hn)   # H x Hn ant
        vermatrizf(multiplicar(HmI, multiplicar(Ufn, multiplicar(Hn,q))))
        return
    else:
        return(0)

def groverUs(n_qubits):         #Arma la compuerta Us = 2|s><s|-I (Difusor de Grover)
    if(n_qubits < 2):           #para un sistema de n_qubits (N=2**n_qubits estados)
        return(0)               #mínimo 2 qubits (sino retorna 0)
    In = I                      #Matriz Identidad
    supn = h(ket0)              #Superposición |+>
    for n in range (n_qubits - 1):
        In = tensorial(I, In)           #Matriz Identidad N x N
        supn = tensorial(supn, h(ket0)) #Estado de superposición |+> de n_qubits
    Usn = sumar(escalar(multiplicar(supn,conjugar(trasponer(supn))),2),escalar(In, -1))
    return(Usn)


#Para un qubit q=[[a],[b]], encuentra su punto [x, y, z] en la esfera de Bloch
def qubit_bloch(q):
    bloch = [0, 0, 0]           #Inicializa con el centro de esfera de Bloch
    
    ar = q[0][0].real           #a=(ar + j ai)
    ai = q[0][0].imag
    br = q[1][0].real           #b=(br + j bi)
    bi = q[1][0].imag
    r1 = (ar**2 + ai**2)**0.5   #módulo r1 de a
    r2 = (br**2 + bi**2)**0.5   #módulo r2 de b

#    print("a=", ar, ai, "b=", br, bi, "r1=", r1 , "r2=", r2)

    if(ar==ai==0):              #argumento tita1 de a
        tita1 = 0
    elif(ar==0):
        tita1 = math.pi/2
        if(ai < 0):
            tita1 = tita1 + math.pi
    elif(ai==0):
        tita1 = 0
        if(ar < 0):
            tita1 = math.pi
    else:
        tita1 = math.atan(ai/ar)
        if(ai<0 and ar<0):
            tita1 = tita1 + math.pi
        elif(ai>0 and ar<0):
            tita1 = math.pi - tita1
        elif(ai<0 and ar>0):
            tita1 = 2*math.pi - tita1

#    print("tita1=", tita1)
        
    if(br==bi==0):              #argumento tita2 de b
        tita2 = 0
    elif(br==0):
        tita2 = math.pi/2
        if(bi < 0):
            tita2 = tita2 + math.pi
    elif(bi==0):
        tita2 = 0
        if(br < 0):
            tita2 = math.pi
    else:
        tita2 = math.atan(bi/br)
        if(bi<0 and br<0):
            tita2 = tita2 + math.pi
        elif(bi>0 and br<0):
            tita2 = math.pi - tita2
        elif(bi<0 and br>0):
            tita2 = 2*math.pi - tita2

#    print("tita2=", tita2)

    if(r1==r2==0):              #si r1=r2=0 error qubit nulo, retorna centro
        return(bloch)
    elif(r1==0):
        phi = math.pi
    else:    
        phi = 2*math.atan(r2/r1)

    tita = tita2-tita1
    if(tita < 0):
        tita = tita + (2*math.pi)

    bloch[0] = math.sin(phi)*math.cos(tita)
    bloch[1] = math.sin(phi)*math.sin(tita)
    bloch[2] = math.cos(phi)
    print("({:1.3f}, {:1.3f}, {:1.3f})".format(bloch[0], bloch[1], bloch[2]))
    print("phi={:.3f} rad , tita={:.3f} rad".format(phi, tita))
    return(bloch)


def matrizDens(nqubits, probas): #Arma la Matriz de Densidad para un vector de nqubits
                                 #asociados a un vector de probabilidades respectivas
                    #pasar la lista asi: [nqubit1,...,nqubitn] y [probas1,...,probasn]
                    #ejemplo: D = matrizDens([ket0, ket1],[0.5, 0.5])
    if(len(nqubits) != len(probas)): #cantidad de nqubits (estados mixtos del sistema)
       return(0)                     #cada uno con su respectiva probabilidad, sino termina
    n = len(nqubits[0])              #Tamaño Matriz Dens según la n de cada nqubit
    Dens = np.zeros((n, n))          #Llena matriz Dens con 0s
    for i in range(len(nqubits)):
        Dens = sumar(Dens,escalar(multiplicar(nqubits[i],conjugar(trasponer(nqubits[i]))),probas[i]))
    return(Dens)


def shannon(probas):    #Calcula la Entropia de Shannon para un alfabeto de n letras,
    n = len(probas)     #donde probas=[p1,p2,...,pn] las probabilidades de cada letra
    Ss = 0
    for i in range(n):
        if (probas[i] != 0):
            Ss = Ss - probas[i] * math.log(probas[i],2)
    return(Ss)
    
    
def vonNeumann(matrizDensidad): #Calcula la Entropia de von Neumann para un sistema
                                #de nqubits con determinada matriz de Densidad
    autoval, autovec = np.linalg.eigh(matrizDensidad)
    Sv = 0
    for i in range(len(autoval)):
        if (autoval[i] != 0):
            Sv = Sv - autoval[i] * math.log(autoval[i],2)
    return(Sv)