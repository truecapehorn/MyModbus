from src.modbus_tcp_v1 import Master

master = Master('192.168.0.35', 502)

mw255 = master.read_coils(0, 255, unit=1)

mw = master.read_coils(2000, 2000, unit=1)
dic_val = {'M{}'.format(nr): {'val': v, 'comment': None} for nr, v in enumerate(mw)}

print(dic_val)


# for k,v in dic_val.items():
#     print('{} - {} '.format(k,v))

# {M0:{'name':'coś tam " 'value'=true},M1:{'name':'LAMPA2 " 'value'=FLASE}....


def maping():
    F = open('komentarze_fatek_biuro.csv', 'r')
    lista = []
    for line in F.readlines():
        parts = line.split(';')
        part = [x.strip() for x in parts]
        lista.append(part)
    F.close()
    slownik = {}
    for i in lista:
        slownik.update({i[0]: {'comment': i[1]}})
    return slownik


fatek = maping()

print(fatek)

for item, value in dic_val.items():  # {'M0': False, 'M1': False,..}
    for zmienna, wartosc in fatek.items():  # {'X0': {'komentarz': 'jarzeniówki kory',...}
        if zmienna == item:
            dic_val[item]['comment'] = wartosc['comment']
print(dic_val)
for k, v in dic_val.items():
    if v['comment'] != None:
        print(v['comment'], '\t', v['val'])
