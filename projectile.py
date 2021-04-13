import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class bcolors:
    FAIL = '\033[91m'
    ENDC = '\033[0m'

print("Symulator rzutu poziomego")
print("Proszę podać następujące parametry:")
# Pobieranie danych
v = float(input('Prędkość początkową (m/s): '))
ang = float(input('Kąt wyrzutu (stopnie): '))
h = float(input('Wysokość wyrzutu (m): '))
M = float(input('Masę wyrzucanego obiektu (kg): '))
B = float(input('Współczynnik proporcjonalności siły oporu (kg/m): '))
if v<=0 or abs(ang)>90 or M<0 or h<0 or B<0:
    print(f"{bcolors.FAIL}Błędna wartość jednego lub kilku parametrów.{bcolors.ENDC}"'''
Podana prędkość, masa i wysokość początkowa powinny być większe 
od zera, a kąt wyrzutu mieścić się w przedziale ]0,90[.''')
else:   
    # zamiana kąta na radiany
    angrad = ang/180 * np.pi
    # Stałe
    g = 9.8
    # listy na współrzędne
    t = [0]  
    x = [0]  
    y = [0+h]
    # Początkowe wartości - prędkość i przyspieszenie
    vx = [v * np.cos(angrad)] 
    vy = [v * np.sin(angrad)]
    ax = [-(B * (v ** 2) * np.cos(angrad)) / M]
    ay = [-g - (B * (v ** 2) * np.sin(angrad)) / M]
    # Krok
    dt = 0.01
    #czas lotu
    vterm = np.sqrt(2*M*g/B)
    t_max = vterm/g * np.arctan(v/vterm)
    t_lot = 2 * t_max
    #'''
    # Rysunek
    history_len=500
    f1 = plt.figure()
    ax1 = f1.add_subplot()
    ax1.grid()
    line, = ax1.plot([], [], '-', lw=2)

    # Dane do animacji
    # Próbowałem tutaj dodać jakąś pętlę z warunkiem y[i] >= 0, czyli żeby 
    # pętla przestała się wykonywać gdy y<0. 
    # Jednak gdy animacja dochodziła do tego punktu to pojawiał się błąd: IndexError: list index out of range
    #
    # Z kolei bez pętli wykres nie przestanie się tworzyć, więc też nie jest to najlepsza sytuacja...
    #
    def animate(counter):
        #Kolejne chwile
        t.append(t[counter] + dt) 
        #Nowa prędkość
        vx.append(vx[counter] + dt * ax[counter])
        vy.append(vy[counter] + dt * ay[counter])
        vel = np.sqrt(vx[-1] ** 2 + vy[-1] ** 2)
        #Nowe położenie
        x.append(x[counter] + dt * vx[counter])
        y.append(y[counter] + dt * vy[counter])
        #Nowe przyspieszenie
        ax.append(- (B * vel * vx[-1] / M))
        ay.append(- g - (B * vel * vy[-1] / M))
        #Ślad
        line.set_xdata(x[:-1])
        line.set_ydata(y[:-1])

    #Paramtery wykresu
    print("Tworzę animację...")
    ax1.set_title("Rzut ukośny")
    ax1.set_ylabel("Wysokość [m]")
    ax1.set_xlabel("Odległość od miejsca wyrzutu [m]")
    xmin = 0 
    xmax = vterm**2/(g) * np.log((vterm**2+g*(v * np.cos(angrad))*t_lot)/(vterm**2)) 
    ymax = np.sin(angrad)*(vterm**2)/(2*g) * np.log((v**2+vterm**2)/(vterm**2)) + h
    ymin = 0 
    maxxy = max(ymax, xmax)
    plt.xlim(xmin, maxxy)
    plt.ylim(ymin, maxxy)
    #Animowanie. Próbowałem uzależnić jakoś liczbę 'frames' od czasu lotu
    #ale skutek był taki, że wszystkie punkty wyrysowywały się dobrze, lecz
    #ostatni łączył się z pierwszym
    ani = animation.FuncAnimation(f1, animate, interval=dt*500)
    plt.show()
'''
#DRUGA WERSJA
#Początek ten sam:

# Pobieranie danych
v = float(input('Podaj prędkość początkową (m/s): '))
ang = float(input('Podaj kąt wyrzutu (stopnie): '))
h = float(input('Podaj wysokość wyrzutu (m): '))
M = float(input('Podaj masę wyrzucanego obiektu (kg): '))
B = float(input('Podaj współczynnik proporcjonalności siły oporu (kg/m): '))
# zamiana kąta na radiany
angrad = ang/180 * np.pi
# Stałe
g = 9.8
# listy na współrzędne
t = [0]  
x = [0]  
y = [0+h]
# Początkowe wartości - prędkość i przyspieszenie
vx = [v * np.cos(angrad)] 
vy = [v * np.sin(angrad)]
ax = [-(B * (v ** 2) * np.cos(angrad)) / M]
ay = [-g - (B * (v ** 2) * np.sin(angrad)) / M]
# Krok
dt = 0.01
f1 = plt.figure()
ax1 = f1.add_subplot(111)
ax1.grid()
line, = ax1.plot([], [], '-', lw=2)
# Tutaj jakoś wstawiłem pętlę, ale efekt nie jest najlepszy
# Co prawda wykres się wyrysowuje i kończy dla y[i]<0, lecz to chyba nie animacja, tylko statyczny orbaz
def animate(i):
    y = [0]
    x = [0]
    vx = [v*np.cos(angrad)]
    vy = [v*np.sin(angrad)]
    ax = [-(B * v ** 2 * np.cos(angrad)) / M]
    ay = [-g - (B * v ** 2 * np.sin(angrad) / M)]
    dt = 0.01
    i = 0
    while (y[i] >= 0):
        x += [0]
        y += [0]
        vx += [0]
        vy += [0]
        ax += [0]
        ay += [0]
        #Nowe położenie
        x[i+1] = x[i] + dt * vx[i]
        y[i+1] =  y[i] + dt * vy[i]
        #Nowa prędkosć
        vx[i+1] = vx[i] + dt * ax[i]
        vy[i+1] = vy[i] + dt * ay[i]
        vel = np.sqrt(vx[i+1] ** 2 + vy[i+1] ** 2)
        #Nowe przyspieszenie
        ax[i+1] = -(B * vel * vx[i+1]) / M
        ay[i+1] = -g - (B * vel * vy[i+1]) / M
        line.set_xdata(x[:-1])
        line.set_ydata(y[:-1])
        i = i + 1
    return line, 

#Wykres statyczny wyrysowuje się poprawny
#plt.plot(x,y)
#plt.xlabel("x [m]")
#plt.ylabel("y [m]")
#plt.show()   


ax1.set_xlabel("x [m]")
ax1.set_ylabel("y [m]")
xmin = 0
xmax = 10
ymax = 10
ymin = 0 
ax1.set_xlim(xmin, xmax)
ax1.set_ylim(0, ymax)
ani = animation.FuncAnimation(f1, animate, interval=dt*1000)
plt.show()
'''