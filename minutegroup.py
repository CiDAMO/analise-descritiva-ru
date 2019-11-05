#df  = dataframe
#num = agrupamento em minutos do número de pessoas
def minutegroup(df,num):
    tabela = preparatabela(df,num).drop(['hora', 'minuto'], axis=1)
    for i in range(num,int(df.shape[0])-num,num):
        if (i%num != 0):
            continue
        if (df.loc[i]['Refeição'] != df.loc[i-num]['Refeição']):
            continue
        soma = 0
        for j in range(0,num):
            soma += int(df.iloc[i-j,df.columns.get_loc('Num_pessoas')])
        tabela.at[i,'Num_pessoas'] = soma
    return tabela
