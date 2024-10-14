import requests, pandas,time, copy, numpy, discord
from datetime import datetime

td = requests.get('https://taxas-tesouro.com/page-data/index/page-data.json')

if td.status_code ==200:
    td = td.json()
    
    tdcompra = td['result']['data']['dataJson']['compra']
    tdcompra = pandas.DataFrame(tdcompra)
    tdcompra['id'] = numpy.arange(len(tdcompra))
    tdcompra = tdcompra[['name','rate','maturity_at','str_price','net_change','str_min_amount','hist','id']]
    
    tdvenda = td['result']['data']['dataJson']['venda']
    tdvenda = pandas.DataFrame(tdvenda)
    tdvenda['id'] = numpy.arange(len(tdvenda))
    tdvenda = tdvenda[['name', 'rate','maturity_at','str_price','id']]

    listcompra = []
    tesouro = input('Digite o título publico:').title()
    
    try:
        numero = int(tesouro)
        numero = tdcompra.loc[tdcompra['id']==numero,'name'].values[0]
        if numero in tdcompra['name'].values:
            listcompra.append(numero)
        else:
            print('Título não encontrado')
    except ValueError:
        if tesouro in tdcompra['name'].values:
            listcompra.append(tesouro)
        else:
            print('Título não encontrado')
    except IndexError:
        print('Titulo fora de ar')

    def tempo(z):
        hist = tdcompra['hist']
        copiar = copy.copy(hist[z][0])
        tempo = copiar['ts']
        tempo = pandas.to_datetime(tempo)
        dia = tempo.strftime("%d/%m/%Y")
        horario = tempo.strftime("%H:%M")
        return horario
    def last_rate(y):
        hist = tdcompra['hist']
        copiar = copy.copy(hist[y][1])
        rate = copiar['rate']
        rate = rate.replace('.', ',')
        return rate
    
    id = tdcompra.loc[tdcompra['name'].isin(listcompra),['id']]
    lista_id = id['id'].tolist()

    idvenda = tdvenda.loc[tdvenda['name'].isin(listcompra),['id']]
    lista_idvenda = idvenda['id'].tolist()

    for i in lista_id:
        dia = tempo(i)
        taxa = last_rate(i)
        tdcompra['Taxa anterior']= taxa
        tdcompra['Última att:'] = dia
        compra = tdcompra.loc[i,['name','rate','str_price','str_min_amount','net_change'] + [ 'Última att:']+['Taxa anterior']]
        compra = compra.rename({'name' : 'Nome:', 'maturity_at' : 'Vencimento:', 'str_price' : 'P.U.:', 'str_min_amount' : 'P.U. minimo:', 'rate':'Taxa:', 'net_change':'Variação:'})
        print(compra)
         
    for o in lista_idvenda:
        venda = tdvenda.loc[o,['name', 'rate','maturity_at','str_price']]
        print(venda)

else:
    print(f'Fora de ar{td}')
