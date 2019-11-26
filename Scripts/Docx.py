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
        if files[i].split(".")[-1] == "docx":
            arquivos = arquivos.append({l: files[i]}, ignore_index=True)

ano = arquivos.columns.tolist()
for ano_i in range(0,len(ano)):
    l = arquivos[str(ano[ano_i])].dropna().tolist()
    bb = []
    for arquivos_i in range(0,len(l)):
        df = read_docx_tables("../" + ano[ano_i] + "/" + l[arquivos_i])
        if len(df) == 1:
            df = df[0]
        elif len(df) == 2:
            df = df[0].append(df[1],ignore_index=True)
            df = df[["SEGUNDA","TERÇA","QUARTA","QUINTA","SEXTA","SÁBADO","DOMINGO"]]
        df = Insert_row(0,df,df.columns)
        aa = {}
        for k in range(0,len(df.index)):
            c = []
            for i in range(0,len(df.columns)):
                a = df.iloc[k,i]
                if type(a) == str:
                    a = a.split("\n")
                    b = []
                    for j in range(0,len(a)):
                        if a[j] != "" and a[j] != " ":
                            b += [a[j]]
                    c += [len(b)]
                    c1 = pd.DataFrame(pd.DataFrame(c)[0].value_counts())
                    c1 = c1[c1[0] == max(c1[0])].index[0]
            if len(list(set(c))) > 1:
                c = pd.DataFrame(c)[pd.DataFrame(c)[0] != c1]
                for j in range(0,len(c.index)):
                    aa[k,c.index[j-1]] = c.iloc[j,0],c1
        df = casos_particulares(df,l[arquivos_i])
        k = 0
        while k <= df.index[-1]:
            ii = df.index[-1]
            for i in range(0,len(df.columns)):
                a = df.iloc[k,i]
                if RepresentsStr(a):
                    a = a.split("\n")
                    b = []
                    for j in range(0,len(a)):
                        if a[j] != "":
                            b += [a[j]]
            for i in range(ii + 1,ii + len(b)):
                df.loc[i,:] = 0
            for i in range(ii,k,-1):
                df.loc[i+len(b)-1,:] = df.loc[i,:]
            for i in range(1,len(b)):
                df.loc[k+i,:] = 0

            for i in range(0,len(df.columns)):
                a = df.iloc[k,i]
                if RepresentsStr(a):
                    a = a.split("\n")
                    b = []
                    for j in range(0,len(a)):
                        if a[j] != "":
                            b += [a[j]]
                    df.iloc[k:k+len(b),i] = b
            k += len(b)
        data = ano[ano_i] + "-" + gera_data(l[arquivos_i])
        tabela = gera_tabela()
        r,c = df.shape
        maior = 0
        # Criando tabela csv
        for i in range(0,r):
            for j in range(0,c):
                if RepresentsInt(df.iloc[i,j]):
                    if int(df.iloc[i,j]) > maior:
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
                        maior = int(df.iloc[i,j])

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
