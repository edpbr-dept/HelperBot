import pandas as pd

def torezaniBot_locations(name, loc=None, filename='torezaniBot_locations.csv'):
    df = pd.read_csv(filename, sep=';')

    if loc is None:
        df = df[df.desc.str.contains(name.upper())]
    else:
        df = df[(df.desc.str.contains(name.upper())) & (df.categ == loc)]

    msg_list = []
    msg = 'Cód.: {}\nDesc.: {}\n'

    for i in df.index:
        cod, desc, _ = df.loc[i]
        msg_list.append(msg.format(cod, desc))

    return '\n'.join(msg_list) 

def medidores(name, loc=None, filename='medidores.csv'):
    df = pd.read_csv(filename, sep=';')

    df = df[df.desc.str.contains(name.upper())]

    msg_list = []
    msg = 'Local.: {}\nTrafo.: {}\nInstalação: {}\n'

    for i in df.index:
        desc0, trafo, inst = df.loc[i]
        msg_list.append(msg.format(desc0, trafo, inst))

    return '\n'.join(msg_list) 
