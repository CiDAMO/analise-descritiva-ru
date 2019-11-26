#!/usr/bin/env python3

# Coletando o texto
text = textract.process("../2019/Cardápio fevereiro 2019 versão final REVISADA BLUME com breves descrições.doc")
text = text.decode("utf-8") 
text = "SEGUNDA\nTERÇA\nQUARTA\nQUINTA\nSEXTA\nSÁBADO\nDOMINGO\n25\nChá de erva cidreira\nPão hot dog com margarina\nMaçã\n26\nChá de camomila\nPão francês com presunto\nMelancia\n27\nChá Maçã\nPão hot dog c/ doce de abóbora\nLaranja\n28\nChá de morango\nPão francês com patê de frango\nBanana\n01\nChá de erva doce\nPão hot dog com margarina\nAbacaxi\n02\nChá de hortelã\nPão francês com queijo\nMamão\n03\nChá de erva cidreira\nPão francês com presunto\nBanana\nBisteca ao m. do cheff (molho escuro com batata salsa)\nQuirera com costelinha\nLaranja\nAlface americana e beterraba ralada\nSoja refogada\nBife de panela\nMacarrão com brócolis\nMelão\nAcelga e cenoura ralada\nFeijão cavalo ao alho e óleo\nFilé de frango à milanesa\nAbobrinha refogada\nCreme de abacaxi\nAlmeirão e tomate\nTorre de berinjela (com ervilha seca)\nCarne moída ao sugo\nPurê prático\nSagu de vinho\nRepolho e beterraba ralada\nTrigo em grão c/ PTS ao sugo\nFrango assado/frito\nQuibebe\nGelatina miscelânea\nRadite e Berinjela ao vinagrete\nHambúrguer de soja\nTirinhas de carne ao molho oriental\nLegumes refogado\nBanana\nAlface e brócolis\nBolinho de lentilha\nChurrasco\nFarofa úmida\nGelflan\nAgrião e maionese de legumes\nTorre de berinjela\nPicadinho especial (molho com cenoura, tomate e milho)\nSopa Califórnia (frango, batata, cenoura e abobrinha)\nAcelga e tomate\nCharutinho de repolho com lentilha\nFilé de frango ao molho de limão\nSopa leve (paleta bovina, batata cenoura e arroz)\nAlmeirão e Natural\nHamb g-bico c/ abóbora\nPanqueca de carne moída\nSopa de legumes com arroz\nRepolho bicolor e vagem\nPanqueca de triguilho\nFrango à paulista (molho escuro com bacon, tomate e pimentão verde)\nSopa de mandioca\nRadite e cenoura ralada\nPimentão recheado com grão-de-bico\nStrogonoff de carne\nBatata chips\nAlface e chuchu com milho verde\nStrogonoff de feijão branco\nRocambole de carne\nCanja (frango, batata, cenoura, arroz)\nAgrião e abobrinha cozida\nPolpeta de PTS recheada c/ cenoura e vagem\nFrango americano\nCreme rio branco (creme de batata salsa com couve)\nEscarola e brócolis c/ c-flor\nCroquete de trigo em grão"
text = text.split("\n")

# Gerando dataframe
dias = []
for i in range(0,7):
    dias += [text[i]]
dias
df = pd.DataFrame([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]],columns=dias)
for i in [0,1,2,3,4,5,6]:
    for j in [1,2,3,4]:
        df.iloc[j-1,i] = text[6+(i*4)+j]
        df.iloc[j-1+4,i] = text[34+(i*5)+j]
        df.iloc[j-1+9,i] = text[69+(i*4)+j]
    df.iloc[5-1+4,i] = text[34+(i*5)+5]

data = "2019-02"
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
newpath = "../2019_csv"
if not os.path.exists(newpath):
    os.makedirs(newpath)
tabela.to_csv(newpath + "/" + data + ".csv")
