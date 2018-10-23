from src.zmianaPredkosciApar import *

import argparse
import textwrap
import time


def str2bool(v):
    if v.lower() in ('yes', 'true', 'on', 'y', '1'):
        return 1
    elif v.lower() in ('no', 'false', 'off', 'n', '0'):
        return 0
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


parser = argparse.ArgumentParser(prog='Appar Speed Change',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description=textwrap.dedent(
                                     '''Main program do osblugi zmiany spredkosci w appr.\nRejestr 29 w tablicy'''))

parser.add_argument('-c', action='store', dest='port', default='com3', type=str,
                    help='Port')

parser.add_argument('-o', action='store', dest='speed_old', default=2400, type=int,
                    help='Predkość połączenia.Defaulut: 2400')

parser.add_argument('-n', action='store', dest='speed_new', default=9600, type=int,
                    help='Nowa wartosc predkosci. Defaulut: 9600')

parser.add_argument('-p', '--start', action='store', dest='reg_start', type=int,
                    help='Start zapytania')

parser.add_argument('-k', '--stop', action='store', dest='reg_stop', type=int,
                    help='Stop zapytania')

parser.add_argument('-u', nargs='*', dest='units', type=int, help='tablica adresow urzadzen')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

actions = vars(parser.parse_args())  # pobranie wartosci akcji z namespace parasera w postaci slownika
print("Dane wejsciowe: ", actions)


units = unitCheck(actions['units'], actions["reg_start"], actions["reg_stop"], actions["speed_old"], actions["port"])
speed_change(units, actions["speed_old"], actions["speed_new"])
