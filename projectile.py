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
    ball, = ax1.plot([], [], 'og', ms=10)
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
        ball.set_data(x[counter], y[counter])
        return line, ball,

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
    ani = animation.FuncAnimation(f1, animate, interval=dt*500, blit=True)
    plt.show()