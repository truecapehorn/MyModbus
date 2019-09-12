# MyModbus
API Modbus RTU/TCP

## Description

API do odczytu rejstrow Modbus RTU/TCP.

* Odczyt rejstrów holding,
* Odczyt rejestrow input
* Odczyt rejstrow coil
* Odczyt Rejestrow discrete input
* Zapis do rejstru holding

## Use

    staski = TCP_Client('192.168.1.100', 502)
    print("host:",staski.client.host)
    print("time out:",staski.client.timeout)

    conn = Master(staski.client)
    try:
        reg = conn.read_register(1, 101, 10, reg_type='holding', data_type='int')
        print(reg)
    except Exception as e:
        print(e)

## Doc

    class TCP_Client(builtins.object)
        TCP_Client(host, port)
    
    Obsłoga Modbus TCP
    
    Methods defined here:
    
    __init__(self, host, port)
        Initialize self.  See help(type(self)) for accurate signature.
    
    ----------------------------------------------------------------------
 
     class RTU_Client(builtins.object)
        RTU_Client(speed, rs_port, method='rtu', stopbits=1, parity='N', bytesize=8, timeout=1)
    
    Obsłoga Modbus RTU
    
    Methods defined here:
    
    __init__(self, speed, rs_port, method='rtu', stopbits=1, parity='N', bytesize=8, timeout=1)
        Initialize self.  See help(type(self)) for accurate signature.
    
    ----------------------------------------------------------------------

------------------------------------------------------------------------
    class Master(builtins.object)
        Master(client)
    
    Methods defined here:
    
    __init__(self, client)
        Initialize self.  See help(type(self)) for accurate signature.
    
    assercion(self, operation)
        :param operation: Metoda klienta. Sprawdza czy sciagnelo dane.
        :return: Status False to OK or True to chujowo.
    
    choise_data_type(self, data)
        Sprawdza czy trzeba zamienic miejscami rejstry i koduje do opowiedniego formatu.
        :param data: Pobrana lista rejestrow
        :return: Lista w formacie danych jaki jest potrzebny. int, int32 lub float.
    
    data_check(self, data)
        Sprawdza czy obiekt jest iterowalny.
        :param data: Pobrana lista rejestrow.
        :return: True to OK ,False to chujowo.
    
    data_to_dict(self, data)
        Wrzuca ponumerowane rejestry do slownika
        :param data: Lista z pobranymi rejestrami
        :return: Slownik.
    
    read_bool(self, unit, reg_start, reg_lenght, reg_type='coil')
        Odczytanie rejestrow binarnych.
        :param unit: Adres urzadznia.
        :param reg_start: Rejestr początkowy.
        :param reg_lenght: Dlugosc zapytania.
        :param reg_type: Typ rejestru.
        :return: Slownik
    
    read_holding(self)
        Funkcja pomocnicza
        :return:holding reg
    
    read_input(self)
        Funkcja pomocnicza
        :return:
    
    read_multipe_discrete_inputs(self)
        Funkcja pomocnicza
        :return:
    
    read_multiple_colis(self)
        Funkcja pomocnicza
        :return:
    
    read_register(self, unit, reg_start, reg_lenght, reg_type='holding', data_type='int', transp=False)
        :param unit: Adres urzadznia.
        :param reg_start: Rejestr początkowy.
        :param reg_lenght: Dlugosc zapytania.
        :param reg_type: Typ rejestru. ('holding','input','coil','disc_input')
        :param data_type: Typ danych ('int','int32','float')
        :param transp: odwrócenie rejestrow.
        :return: Slownik
    
    write_register(self, reg_add, val, unit)
        Nie przetestowane
    
    write_single(self)
        Funkcja pomocnicza
        :return:
    
    ----------------------------------------------------------------------


## Note

Nie przetestowany zapis wartosci do rejestru. 

W przygotowaniu reszta reszta metod. 