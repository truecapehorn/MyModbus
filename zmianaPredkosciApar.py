from modbus_rtu_v5 import Master
import time




def unitCheck(start, stop, speed):
    '''

    :param start: adres urzadzenia poczatek
    :param stop: aders urzadzenia koniec
    :param speed: predkosc polaczenia
    :return: zwraca tablice z adresami urzadzen z którymi nawiazal połączenie
    '''
    units = []
    apar = Master(port='com3', speed=speed)
    while apar.connection == True:
        for unit in range(start, stop + 1):
            conn = apar.read_register(unit, 29, 1)
            print(conn)
            if conn != False:
                units.append(unit)
            if unit == stop:
                break
        break
    print("ODCZYTANE URZADZENIA: ", units)
    return units


def speed_change(units, speedOld, speedNew):
    '''

    :param units: tablica adresow urzadzen
    :param speedOld: stara predkosc np. 2400
    :param speedNew: nowa predkosc np. 9600
    :return: zmienia adres 29 rejestru apar
    '''

    '''
    Tabela predkosci i odpowiadajcym mu wartosi rejestru 29. 
    115,2k  -   9
    57,6k   -   8
    38,4k   -   7
    19,2k   -   6
    14,4k   -   5
    9,6k    -   4
    4,8k    -   3
    2,4k    -   2
    1,2k    -   1
    0,6k    -   0
    '''

    speedTab = {0: 600, 1: 1200, 2: 2400, 3: 4800, 4: 9600, 5: 14400, 6: 19200, 7: 38400, 8: 57600,
                9: 115200}  # tabela z predkosciami

    def checkConnection(apar, unit):

        '''

        :param apar: obejekt z polaczeniem modbus
        :param unit: adres urzadzenia
        :return: zwraca wartosc rejetrow lub wartosc False
        '''
        print("Odczytanie rejestrow z unit nr:", unit)
        connection = apar.read_register(unit, 29, 1)
        time.sleep(0.5)
        return connection

    def speedTable(speedTab):

        '''
        :param speedTab: slownik z wartosciami rejetru i odpowiadajacymi im predkosciami
        :return: wartosc rejestru
        '''
        for k, v in speedTab.items():
            if v == speedNew:
                regVal = k
                print("{} = {}".format(v, k))
                return regVal
            else:
                pass

    def apparSpeedChange(speedOld, speedNew):

        '''

        :param speedOld: stara wartosc predkosci
        :param speedNew: nowa wartosc predkosci
        :return: zwraca False kiedy urzytkownik nie zdecyduje zmieniac predkosci
        '''

        testVar = input("\t!!! Czy chcesz zmienic adres z {} na {} ( t/n).".format(speedOld, speedNew))
        if testVar != "t":
            print("Wyjscie z programu")
            return False
        else:
            print("Zmiana adresu na ", speedNew)
            # przypisanie nowej wartosci rejestru
            regVal = speedTable(speedTab)  # przeskanowanie tabali i zwrocenie wartosci rej. odpowiadajacej predkosci
            print("Nowa Wartosc ", regVal)
            time.sleep(0.5)
            apar1.write_register(29, regVal, unit)
            time.sleep(0.5)

    for unit in units:

        apar1 = Master(port='com3', speed=speedOld)
        if apar1.connection == True:
            print(160 * "=")
            reg = checkConnection(apar1, unit)
            if reg != False:
                change = apparSpeedChange(speedOld, speedNew)
                if change != False:
                    print("Sprawdzenie połaczenia:")
                    apar2 = Master(port='com3', speed=speedNew)
                    if apar2.connection == True:
                        checkConnection(apar2, unit)
                        time.sleep(1)


units = unitCheck(17, 23, 2400)
speed_change(units, 2400, 2400)
