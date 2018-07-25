
'''
author: George Nunes de Moura Filho, 
2018, Computer Engineering Student at Federal University of Paraiba (UFPB), João Pessoa, Brazil.
e-mail: georgenmoura@gmail.com
'''
from copy import deepcopy
from math import ceil
from random import randint

alpha = 0.5
iteracoes_grasp = 50

#função que carrega as matrizes de distancia e fluxo
def carrega_matriz(distancia, fluxo):

    #carrega os arquivos
    distancia_input = open(distancia, "r")
    fluxo_input = open(fluxo, "r")

    #executa a leitura das linhas
    distancia = distancia_input.readlines()
    fluxo = fluxo_input.readlines()

    '''a primeira linha dos arquivos é sempre um número inteiro
    informando a quantidade de nós do grafo'''
    qtdDistancia = int(distancia[0])
    qtdFluxo = int(fluxo[0])

    #aloca duas matrizes com a quantidade de nós dita no arquivo
    distancia_matrix = [[0]]*(qtdDistancia)
    fluxo_matrix = [[0]]*(qtdFluxo)

    ''' quebra a string de cada linha de entrada em uma lista de numeros
    e armazena na matriz criada anteriormente'''
    for i in range(0, int(qtdDistancia)):
        distancia_matrix[i] = list(map(int, distancia[i+1].split()))

    for i in range(0, int(qtdFluxo)):
        fluxo_matrix[i] = list(map(int, fluxo[i+1].split()))

    
    # retorna uma cópia das duas matrizes
    return distancia_matrix.copy(), fluxo_matrix.copy(), qtdDistancia, qtdFluxo


#essa função verifica se uma tupla existe dentro de uma dada solução, retorna um booleano
def exists_in(x, y):
    for i in y:
        if(i[0]==x[0] and (i[1][0]==x[1][1] and i[1][1]==x[1][0])):
            return True
    return False

#complexidade da heuristica: O(n*logn*n²)
def heuristica(distancia, fluxo, qtdAntenas, qtdInstalacoes):
    
    '''
        A ideia da aleatóriedade do grasp é determinar qual a porcentagem do array solução que será gulosa e qual
        será randômica, isso é feito alterando o valor da variável de iteração da heuristica gulosa, diminuimos ela
        multiplicando-a pelo alpha, o que fará com que o vetor seja formado apenas até a posição determinada por este
        cálculo (arrendodamento pra cima). Em seguida, adicionamos aleatóriamente nós à solução, a partir do pool de nós
        do grafo que ainda não foram adicionados de maneira gulosa. Nós só mexemos no grafo de localidades,
        pois mesmo que o grafo de antenas seja feito de maneira totalmente gulosa, alterar os nós localidades é tão ou mais
        impactante que apenas rotacionar antenas nos nós de localidade escolhidos.
    '''
    greedy = ceil(qtdAntenas * alpha)
    iterador = greedy
    resto = qtdAntenas - iterador

    distancia_arestas = []
    fluxo_arestas = []
    visitados = [False] * qtdInstalacoes
    #criamos o pool de nós do grafo, a medida que a heuristica gulosa adicionar nós, os retiraremos do pool
    pool_resto_distancia = [i for i in range(qtdInstalacoes)]
    solucao_inicial = []
    pool_distancia = []
    
    '''Esse loop vai adicionar à tupla [peso_aresta, (nó_ligado1, nó_ligado2), aresta_visitada(true ou false)]
    no vetor 'distancia_arestas', percorrendo toda a matriz de adjacência'''
    a = 0
    for linha in distancia:
        b = 0
        for coluna in linha:
            if(a!=b):
                distancia_arestas.append([coluna, (a,b), False])
            b = b + 1
        a = a + 1
    
    a = 0
    for linha in fluxo:
        b = 0
        for coluna in linha:
            if(a!=b):
                fluxo_arestas.append([coluna, (a,b), False])
            b = b + 1
        a = a + 1
    
    #executamos a ordenação das arestas baseado no peso delas
    distancia_arestas.sort()
    fluxo_arestas.sort()

    for i in range(0,len(distancia_arestas)):

        if(iterador == 0):
            break
            
        for j in distancia_arestas:
            
            if(exists_in(j, solucao_inicial)):
                j[2] = True
            
            #na primeira interação do loop, o primeiro elemento do vetor ordenado deve sempre ser escolhido
            if(iterador == greedy):
                
                '''
                Esse if é pro caso do cálculo do alpha resultar em 1, se isso acontecer apenas 1 nó deverá ser visitado,
                em qualquer outro caso, como estamos tratando de arestas, visitaríamos 2 nós
                '''
                if(iterador==1):
                    solucao_inicial.append(j)
                    pool_distancia.append(j[1][0])
                    pool_resto_distancia.remove(j[1][0])
                    visitados[j[1][0]] = True
                    j[2] = True
                    iterador = iterador - 1
                else:
                    solucao_inicial.append(j)

                    pool_distancia.append(j[1][0])
                    pool_distancia.append(j[1][1])

                    if(j[1][0] in pool_resto_distancia):
                        pool_resto_distancia.remove(j[1][0])
                    if(j[1][1] in pool_resto_distancia):
                        pool_resto_distancia.remove(j[1][1])

                    visitados[j[1][0]] = True
                    visitados[j[1][1]] = True
                    j[2] = True
                    iterador = iterador - 1
                break
            
            
            #quando o iterador é 1, chega a hora de escolher uma aresta de modo a fechar o cíclo da solução inicial
            if(iterador == 1):
                #esse if verifica qual aresta deve ser escolhida
                if((visitados[j[1][0]]==True and visitados[j[1][1]]==True) and j[2]==False):
                    
                    solucao_inicial.append(j)
                    if(j[1][0] not in pool_distancia):
                        pool_distancia.append(j[1][0])
                    if(j[1][1] not in pool_distancia):
                        pool_distancia.append(j[1][1])
                        
                    if(j[1][0] in pool_resto_distancia):
                        pool_resto_distancia.remove(j[1][0])
                    if(j[1][1] in pool_resto_distancia):
                        pool_resto_distancia.remove(j[1][1])

                    j[2] = True
                    iterador = iterador - 1
                else:
                    continue
                break
            
            
            
            #esse if garante que sempre escolheremos uma aresta que ligue um nó visitado a outro não visitado
            if( (visitados[j[1][1]]==True and visitados[j[1][0]]==False) or 
                (visitados[j[1][1]]==False and visitados[j[1][0]]==True) ):
                
                solucao_inicial.append(j)
                if(j[1][0] not in pool_distancia):
                    pool_distancia.append(j[1][0])
                if(j[1][1] not in pool_distancia):
                    pool_distancia.append(j[1][1])
                
                if(j[1][0] in pool_resto_distancia):
                    pool_resto_distancia.remove(j[1][0])
                if(j[1][1] in pool_resto_distancia):
                    pool_resto_distancia.remove(j[1][1])

                visitados[j[1][0]] = True
                visitados[j[1][1]] = True
                j[2] = True
                iterador = iterador - 1
                break
    

    '''Agora vamos determinar de maneira gulosa a distribuição de antenas sobre as localidaddes, como os dois vetores
    estão ordenados, simplesmente alocamos os indexes de nós de ambos os grafos respeitando a ordem de percorrimento
    de ambos os vetores'''

    pool_fluxo = []
    rand = 0

    #Esse for adiciona aleatoriamente nós à solução, a quantidade de nós aleatórios é também baseado no parâmetro alpha
    for i in range(resto):
        rand = randint(0, len(pool_resto_distancia)-1)
        pool_distancia.append(pool_resto_distancia[rand])
        pool_resto_distancia.remove(pool_resto_distancia[rand])
    
    for i in range(0, len(fluxo_arestas), 2):
        if(fluxo_arestas[i][1][0] not in pool_fluxo):
            pool_fluxo.append(fluxo_arestas[i][1][0])
        if(fluxo_arestas[i][1][1] not in pool_fluxo):
            pool_fluxo.append(fluxo_arestas[i][1][1])
    
    '''o retorno da heuristica é uma lista que contém dois indexes, onde o primeiro é a lista referente as localidades
    e o segundo é a lista referente as antenas, a ordem de qual antena fica em qual localidade é respeitada pelos indexes
    de ambas as lista, ou seja, o index [0] da segunda lista em cima do index [0] da primeira e assim sucessivamente'''
    return [pool_distancia, pool_fluxo]

#Essa função executa o cálculo do custo de uma dada solução, consultando as matrizes
def soma_local(distancia, fluxo, solucao_local, size):
    soma = 0
    aux = deepcopy(solucao_local)
    aux[0].append(aux[0][0])
    aux[1].append(aux[1][0])
    for i in range(size):
        multiplicacao = distancia[aux[0][i]][aux[0][i+1]] * fluxo[aux[1][i]][aux[1][i+1]]
        soma = soma + multiplicacao
    return soma

def movimentacao_local(solucao_inicial):
    size = len(solucao_inicial[1])
    valor_inicial = solucao_inicial[1][0]
    for i in range(size):
        if(i==(size-1)):
            solucao_inicial[1][i] = valor_inicial
        else:
            solucao_inicial[1][i] = solucao_inicial[1][i+1]
    return solucao_inicial

#A movimentação global se dá pela troca de uma localidade por outra de maneira aleatória
def movimentacao_global(solucao_inicial, distancia):
    pool = []
    if(len(distancia) == len(solucao_inicial[0])):
        pool = solucao_inicial[0]
    else:
        for i in range(len(distancia)):
            if(i not in solucao_inicial[0]):
                pool.append(i)     
    change_from = randint(0, len(solucao_inicial[0])-1)
    change_to = randint(0, len(pool)-1)
    solucao_inicial[0][change_from] = pool[change_to]
    
    return solucao_inicial

'''O VND implementa a busca pela solução ótima através de movimentações locais e globais, movimentamos localmente enquanto
isso estiver melhorando a solução, temos um parâmetro 'stop_local' que contabiliza quantas vezes a movimentação
local pode errar, quando esse valor é atingido, movimentamos globalmente para tentar a melhoria da solução, até que o valor
de K seja atingido. Quando atingimos o K, paremos de procurar e consideramos a solução encontrada até então como a melhor.'''

def VND(solucao_parcial, distancia, fluxo, qtdInstalacoes, qtdAntenas):
    
    #iniciamos o VND setando a solução inicial a partir da nossa heuristica
    melhor_soma = soma_local(distancia, fluxo, solucao_parcial, qtdAntenas)
    melhor_solucao = deepcopy(solucao_parcial)
    soma = 0
    k = 0
    stop_local = 4
    
    while(k<5):
        
        if(k<stop_local):
            solucao_parcial = movimentacao_local(solucao_parcial)
        else:
            solucao_parcial = movimentacao_global(solucao_parcial, distancia)
        
        soma = soma_local(distancia, fluxo, solucao_parcial, qtdAntenas)
        
        #se melhorou, atualize a melhor solução e zere o parâmetro K
        if(soma < melhor_soma):
            melhor_soma = soma
            melhor_solucao = deepcopy(solucao_parcial)
            k = 0
        else:
            k = k + 1
    
    #essa solução retornada contém a melhor soma encontrada para o espectro de soluções buscadas
    return melhor_solucao


def main():

    distancia, fluxo, qtdInstalacoes, qtdAntenas = carrega_matriz("INST2ELE1.txt", "INST1ELE1.txt")
    
    melhor_solucao = []
    solucao = []
    melhor_soma = 0
    soma = 0
    
    for i in range(iteracoes_grasp):
        
        if(i==0):
            melhor_solucao = heuristica(distancia, fluxo, qtdAntenas, qtdInstalacoes)
            melhor_soma = soma_local(distancia, fluxo, melhor_solucao, qtdAntenas)
            continue

        solucao = heuristica(distancia, fluxo, qtdAntenas, qtdInstalacoes)
        solucao = VND(solucao, distancia, fluxo, qtdInstalacoes, qtdAntenas)
        soma = soma_local(distancia, fluxo, solucao, qtdAntenas)
        
        if(soma < melhor_soma):
            melhor_soma = soma
            melhor_solucao = solucao
            print("Melhorou. soma: " + str(melhor_soma))
            print(melhor_solucao)
        
    print("######################")
    print("\nScore da melhor solucao encontrada pelo GRASP: " + str(melhor_soma))
    print(melhor_solucao)

main()