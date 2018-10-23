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

parser.add_argument('-a', '--host', action='store', dest='host', help='Adres hosta')

parser.add_argument('-c', '--port', action='store', dest='port', help='Port')

parser.add_argument('-u', '--unit', nargs='*', dest='units', type=int, help='Tablica adresow urzadzen')

parser.add_argument('-s', '--start', action='store', dest='reg_start', type=int, help='Start zapytania')

parser.add_argument('-l', '--len', action='store', dest='reg_lenght', type=int, help='Długość zapytania')

parser.add_argument('-rh', '--holding', action='store_const', dest='reg_type', const='holding', help='Rejetry holding')

parser.add_argument('-ri', '--input', action='store_const', dest='reg_type', const='input', help='Rejetry input')

parser.add_argument('-i', '--int', action='store_const', dest='data_type', const='int', help='Rejetry typu int')

parser.add_argument('-f', '--float', action='store_const', dest='data_type', const='float', help='Rejetry typu float')

parser.add_argument('-q', '--qty', action='store', dest='qty', default=3, type=int, help='Ilosc powtorzen def: 3')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

actions = vars(parser.parse_args())  # pobranie wartosci akcji z namespace parasera w postaci slownika
print("Dane wejsciowe: ", actions)
if actions['reg_type'] == None or actions['data_type'] == None:
    print('\n!!! Trzeba wprowadzic typ rejetsru ( holding ?) oraz typ danych w rejestrach (int ?) !!!')
    sys.exit(1)

master = Master(actions['host'], actions['port'])
master.masterDoc()
for c, v in enumerate(range(0, actions['qty']), 1):
    print('Pomiar ', c)
    for u in actions['units']:
        master.read_register(u, actions['reg_start'], actions['reg_lenght'], actions['reg_type'], actions['data_type'])
