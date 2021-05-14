import numpy as np
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import repeat

#Automat komórkowy z trzema możliwymi stanami.
#Stan danej komórki został uzależniony od stanów dwóch lewych i dwóch prawych komórek 
#sąsiadujących z tą komórką.

#W związku z tą modyfikacją użyto piątek a nie trójek liczb, co powoduje zwiększenie 
#się liczby możliwych stanów danej grupy do 3^5, czyli 243. 
#Liczba możliwych funkcji ewolucji to w tym przypadku 5^243, czyli... dość dużo:
#70747492803333690371164994460060873286582274985462017106114178827621104051506602458
#90258946844498515198400343200685804418658385057244730731440540694165974855422973632
#8125, w przybliżeniu: 7*10^106.

#Program wymaga podania trzech zmiennych: funkcji ewolucji, stanu początkowego oraz
#długości ewolucji.

#Jako, że każda komórka posiada czy możliwe stany to łańcuchy określające stany będą
#odpowiadały liczbom w systemie trójkowym.
# 
# Zapewne jest o wiele prostszy i bardziej efektywny sposób zamiany liczb na system
#trójowy niż to... 
def tr(dec):
    x = dec//3
    y = dec%3
    if dec == 0:
        return '0'
    elif x == 0:
        return str(y)
    else:
        return tr(x) + str(y)
#Ustalamy listę wszystkich możliwych stanów
for i in range(243):
    quint = tr(i).zfill(5) #zfill użyte po to aby liczby miały jednorodną postać.

def funkn(quint):
    #Stan komórki ma zależeć od czterech najbliższych sąsiadujących z nią komórek:
    L2, L1, C, R1, R2 = quint 
    #Takie skakanie między systemami nie jest szczytem efektywności, szczególnie przy
    #bardzo długich łańcuchów stanów, ale nie miałem już siły zastanawiać się jak
    #możnaby to usprawnić. 
    n = 242 - (81*L1 + 27*L2 + 9*C + 3*R1 + R2)
    return int(n)

#Funkcja update oblicza stan n na podstawie n-1 (no i początkowego)
#init oznacza stan początkowy; n - liczba etapów ewolucji; no - numer reguły/funkcji
def update(init, n, no):
    #Przeliczenie numeru funkcji na system trójkowy z wyrównaniem.
    ruletr = tr(no).zfill(243)
    #Zamiana int na str
    rule = np.array([int(bit) for bit in ruletr])
    state = np.zeros((n, len(init)))
    state[0, :] = init
    #Generowanie kolejnych stanów
    for i in range(1, n):
        prstate = state[i - 1, :] #Stan poprzedzający stan i
        #Obliczanie stanu na podstawie poprzedniego stanu danej komórki i cztererch sąsiadów
        T = []
        for j in range(3,-2,-1):
            T.append(np.roll(prstate, j))
            all_quints = np.stack(T)

        state[i, :] = rule[np.apply_along_axis(funkn, 0, all_quints)]

    return state
#Funkcja wyrusowująca "wykres" ewolucji komórek automatu.
def plot(init, n, no):
    data = update(init, n, no)
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.matshow(data)
    ax.axes.get_xaxis().set_visible(False)
    ax.set_frame_on(False)
    ax.set_ylabel('Krok ewolucji')
    plt.show()

#Opis witający użytkownika wraz z instrukcją. 

#Trochę nadprogramowo dodałem oprócz możliwości samego wpisania wartości także losowanie
#tych paramterów, wraz z dwoma opcjami sczególnymi, które pokazują ewolucję dla funkcji
#0 oraz 5^243. 
hello = (
'''
---------------------------------Automat komórkowy---------------------------------
Oto jednowymiarowy automat komórkowy. Przedstawia on ewolucję podanego stanu począ-
tkowego zgodnie z algorytmem, uzwględniającym stan komórek i ich sąsiadów - dwóch z 
każdej ze stron.

Ciekawsze lecz nadal chaotyczne wzory pojawiają się dla funkcji rzędu 10^20. Począ-
tkowe zaś niemal natychmiast się stabilizują. Jest to związane z uzgadnianiem stanu 
każdej komórki do jej czterech najbliższych sąsiadów.

Aby uruchomić program możesz nacisnąć "r" - wówczas program sam wylosuje potrzebne 
parametry lub nacisnąć klawisz "p", aby wpisać własne wartości.

Aby móc łatwo zobaczyć zmiany stanów komórek dla minimalnej funkcji ewolucji wciśnij 
"n", zaś dla funkcji maksymalnej - klawisz "m" dla 5^243.
''')
Q = 5**243
print(hello)
kl = input('Wybierz opcję wpisująć odpowiednią literę: ')
#Warunki pozwalające wybrać użytkownikowi jedną z czterech opcji
#Opcja główna, w której użytkownik dobiera paramtery.
if kl == 'p':
    try:
        rule = int(input('Podaj liczbę całkowitą: '))
        initial = list(map(int, (input('Podaj stan początkowy: '))))
        steps = int(input('Podaj liczbę kroków ewolucji do wykonania: '))
        #Warunki na błedy
        if 0>=rule or rule>=Q:
            raise ValueError("Podana funkcja ewolucji jest nieprawidłowa!")
        if 0>=steps or steps>=10000:
            #Zamiast takiego ograniczenia możnaby zaimplementować jakiś rodzaj 
            #czasowego ograniczenia na wykonywanie się tej grafiki
            raise ValueError("Podana liczba kroków jest nieprawidłowa!")
        if False in [a==0 or a==1 or a==2 for a in initial]:
            #Chodzi o to czy użytkownik nie poda czegoś np. w systemie dziesiętnym
            raise ValueError("Podano błedy stan początkowy!")
    except ValueError as ver:
        print(ver)
    else:
        plot(initial, steps, rule)
#opcja (niemal) zupełnie zrandomizowana
elif kl == 'r':
    sp = np.random.randint(0, 3, 250)
    st = 300
    ru = np.random.randint(0,2**63)**5 
    #Muszę przyznać, że to rozwiązanie jest, delikatnie mówiąc, niezbyt ładne, ale
    #mniej-więcej działa. Nie przewidziałem, że funkcja ma ograniczenie do 
    #64 bitów.  
    plot(sp, st, ru)
#opcja "minimalna"
elif kl == 'n':
    sp = np.random.randint(0, 3, 250)
    plot(sp, 300, 0)
#opcja "maksymalna"
elif kl == 'm':
    sp = np.random.randint(0, 3, 250)
    st = 300
    ru = Q - 1
    plot(sp, st, ru)
else:
    print("Nie wybrano żadnej z dostępnych opcji") #Nie wiedziałem jak dodać tutaj możliwość żeby po błędnym wpisaniu program wyświetlił ponownie komendę 'Wybierz opcję...'. Pewnie pętlą while, ale coś mi nie wychodziło.

#Teraz jak na to patrzę, to myślę że zasadne byłoby użycie klas, a nie takie chałupnicze pętle