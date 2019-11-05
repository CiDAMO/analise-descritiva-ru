
#df = dataframe
#num = decide as linhas que estarão presentes na tabela preparada (num = 1 -> não remove nenhuma linha)

def preparatabela(df,num = 1):
    
    tabela = []
    for x in range(df.shape[0]):
        if x%num == 0:
            row = df.iloc[x]
            tabela.append(row)

    df['Datetime'] = pd.to_datetime(df['Datetime'])
    tabela = pd.DataFrame(tabela)
    tabela.drop([0],axis=0, inplace = True)
    tabela['hora'] = df['Datetime'].apply(lambda x: x.hour)
    tabela['minuto'] = df['Datetime'].apply(lambda x: x.minute)
    return tabela  
