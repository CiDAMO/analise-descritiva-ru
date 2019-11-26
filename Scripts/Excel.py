#!/usr/bin/env python3

# Criando DataFrame com os arquivos
files = os.listdir("..")
arquivos = pd.DataFrame()
for i in range(0,len(files)):
    if RepresentsInt(files[i]):
        arquivos[files[i]] = []
for l in arquivos.columns:
    files = os.listdir("../" + l)
    for i in range(0,len(files)):
        if files[i].split(".")[-1] == "xlsx":
            arquivos = arquivos.append({l: files[i]}, ignore_index=True)

ano = arquivos.columns.tolist()
for ano_i in range(0,len(ano)):
    l = arquivos[str(ano[ano_i])].dropna().tolist()
    for arquivos_i in range(0,len(l)):
        xls_file = pd.ExcelFile("../" + str(ano[ano_i]) + "/" + l[arquivos_i])
        df = xls_file.parse(xls_file.sheet_names[0])
        data = ano[ano_i] + "-" + gera_data(l[arquivos_i])
        tabela = gera_tabela()
        r,c = df.shape
        maior = 0
        
        # Criando tabela csv
        for i in range(0,r):
            for j in range(0,c):
                if type(df.iloc[i,j]) == int:
                    if df.iloc[i,j] > maior:
                        Itens = []
                        for k in range(1,13):
                            Itens += [df.iloc[i+k,j]]
                        for u,k in [("Cafe da Manha",[0,1])]:
                            organizado = False
                            for v in k:
                                while not organizado:
                                    w = copy.copy(ordena(Itens[v],u,False))
                                    if Itens[v] == Itens[w]:
                                        organizado = True
                                    else:
                                        Itens[v],Itens[w] = Itens[w],Itens[v]
                        tabela.loc[data + "-" + str(df.iloc[i,j])] = Itens
                        maior = df.iloc[i,j]
        
        # Reordenando a tabela
        for i,k in [("Cafe da Manha",[0,1]),("Almoco",[3,4,5,6,7]),("Jantar",[8,9,10,11])]:
            for j in k:
                a = copy.copy(tabela.iloc[:,j])
                b = copy.copy(tabela.iloc[:,ordena(a,i,True)])
                tabela.iloc[:,j],tabela.iloc[:,ordena(a,i,True)] = copy.copy(b),copy.copy(a)
        
        # Criando pasta e arquivo csv
        newpath = "../" + str(ano[ano_i]) + "_csv"
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        tabela.to_csv(newpath + "/" + data + ".csv")
