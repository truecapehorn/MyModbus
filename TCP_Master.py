from src.modbus_tcp_v1 import Master
import argparse
import textwrap
import sys

parser = argparse.ArgumentParser(
    prog='MasterTCP',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''\
        Main program do osblugi Api dla modbasa tcp.
        --------------------------------------------------------

        --------------------------------------------------------
        '''))

parser.add_argument('-a', '--host', action='store', dest='host', type=str, help='Adres hosta')

parser.add_argument('-c', '--port', nargs='*', dest='port', type=int, help='Port')

parser.add_argument('-u', '--units', nargs='*', dest='units', type=int, help='Tablica adresow urzadzen')

parser.add_argument('-s', '--start', action='store', dest='reg_start', type=int, help='Start zapytania')

parser.add_argument('-l', '--len', action='store', dest='reg_lenght', type=int, help='Długość zapytania')

parser.add_argument('-rh', '--holding', action='store_const', dest='reg_type', const='holding', help='Rejetry holding')

parser.add_argument('-ri', '--input', action='store_const', dest='reg_type', const='input', help='Rejetry input')

parser.add_argument('-i', '--int', action='store_const', dest='data_type', const='int', help='Rejetry typu int')

parser.add_argument('-f', '--float', action='store_const', dest='data_type', const='float', help='Rejetry typu float')

parser.add_argument('-t', '--transpozycja', action='store_const', dest='transp', const='transp',
                    help='Czy trasnpozycja rejestrow w tabicy float?')

parser.add_argument('-q', '--qty', action='store', dest='qty', default=1, type=int, help='Ilosc powtorzen def: 1')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

actions = vars(parser.parse_args())  # pobranie wartosci akcji z namespace parasera w postaci slownika
print("Dane wejsciowe: ", actions)

if actions['reg_type'] == None or actions['data_type'] == None:
    print('\n!!! Trzeba wprowadzic typ rejetsru ( holding ?) oraz typ danych w rejestrach (int ?) !!!')
    sys.exit(1)
elif actions['data_type'] != 'int' and actions['reg_lenght']%2!=0:
    print( '!!! Dlugosc zapytania MUSI byc parzysta !!!')
    sys.exit(1)

reg={}

for port in actions['port']:
    master = Master(actions['host'], port)
    master.masterDoc()
    if master.connection == True:
        for c, v in enumerate(range(0, actions['qty']), 1):
            print(100 * '=')
            print('Pomiar TCP ', c)
            for u in actions['units']:
                print(100 * '+')
                # odczytanie rejestrow i wpisanie ich w slownik "reg"
                reg = master.read_register(u, actions['reg_start'], actions['reg_lenght'], actions['reg_type'],
                                     actions['data_type'], actions['transp'])
            print(100 * '=')
    else:
        print('\n!!! Połaczenie z adresem {} na porcie {} nie udane !!!'.format(actions['host'], port))
        continue

# actions={'host': '192.168.0.35', 'port': [502], 'units': [1], 'reg_start': 0, 'reg_lenght': 10, 'reg_type': 'holding','data_type': 'int', 'qty': 1}



for k,v in reg[0].items():
    print('{} - {}'.format(k,v))
print(reg[1])