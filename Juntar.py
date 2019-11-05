def juntar(vet_c, data = 0): 
    #vet_c é um vetor com a quantidade de dados em todos os clusters
        
    tipos, quantidade = np.unique(vet_c, return_counts=True)
    #'tipos' é um vetor com cada dado diferente
    #'quantidade' é um vetor de quantos dados de cada tipo existe em vet
    
    #Criando a matriz para usar no DataFrame:
    d = []
    for k in range(len(quantidade)): 
        d.append([k,quantidade[k]])
    if data == 0: #Retorna o gráfico
        return pd.DataFrame(d, columns = 'Tipo Quantidade'.split()).plot('Tipo')
    #Se não,Retorna o DataFrame
    return pd.DataFrame(d, columns = 'Tipo Quantidade'.split())
