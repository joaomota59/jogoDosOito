#pip install PyQt5 + pptree + numpy + tkinter + copy + ete3
import numpy as np
from tkinter import * #importamos o pacote tkinter
import tkinter.ttk as ttk
from tkinter import messagebox
from copy import deepcopy
from ete3 import Tree, TreeStyle, Tree, TextFace, add_face_to_node
import time
import threading
from threading import Thread
from random import shuffle

##Funções##

class Arvore: #classe para exibir a arvore
    def __init__(self):
        pass
    def stringArvore(self,listaFilhos=[],pai="",kw=""):#retorna a árvore em uma string 
         aux="("#abre para fazer a tupla de filhos
         for i in listaFilhos:
              aux+= str(i).replace("], [","*").replace("[","").replace("]","").replace(",",' ')+"," #colocar estrela pois não dá crto se colocar \n quando passar na instância Tree()
         aux=aux[:-1]#tira a vírgula do final do ultimo filho
         aux+=")"
         pai = pai.replace("], [","*").replace("[","").replace("]","").replace(",",' ')
         if kw=="": #se for o nó raiz e seus filhos
              return aux+pai+";"
         posPai = kw.index(pai) #possição do nó pai na string
         return kw[:posPai] +aux+ kw[posPai:]#escreve os filhos na string do pai correspondente

    def nivelDoNo(self,pai,k=""):#retorna o nível do nó dada a string de árvore k
        if k=="":
            return 0 #nível 0
        pai = str(pai).replace("], [","*").replace("[","").replace("]","").replace(",",' ')
        posPai = k.find(pai)#econtra a posicao do pai na string
        return k[posPai:].count(")") - k[posPai:].count("(") 
        
    def mostraArvore(self,ks=";"):#passa todos as arestas para exibir a árvore
        t = Tree(ks,format=1)
        ts = TreeStyle()
        ts.show_leaf_name = False
        def my_layout(node): #coloca o nome em cada nó
                node.name
                F = TextFace(node.name.replace("*","\n"), tight_text=True)#substitui onde tem estrela p quebra de linha
                add_face_to_node(F, node, column=0, position="branch-right")
                F.rotation = -90#rotação do nome no nó
            
        ts.layout_fn = my_layout
        ts.rotation = 90#exibir árvore na vertical
        t.show(tree_style=ts)#mostra árvore

def encontraParidade(matrix):#retorna a paridade da matrix(se é possível ou não resolvê-la)
    k=""
    for i in matrix:#coloca tds numeros da matrix em uma string
        for j in i:
            if j!='':
                k+=j
    somatorioParidade = 0
    for i in range(8):#8 é a quantidade de números no jogo dos oito
        for j in range(i+1,8):
            if(int(k[i])>int(k[j])):#se ouver números menores após o número que está em analise então soma mais 1
                somatorioParidade+=1
    return (somatorioParidade%2 == 0)
        

def encontraPosicao(matrix,value = ''):#retorna a posicao(linha,coluna) de um valor na matriz
    return [(index, row.index(value)) for index, row in enumerate(matrix) if value in row][0]

def filhosPossiveis(matrix): #retorna todos os filhos possiveis do estado em branco
    indice = encontraPosicao(matrix) #retorna o indice do espaço em branco na matrix (linha,coluna)
    NosFilhos = [] #vetor que guarda todos filhos possiveis(matrizes)
    if(indice[1]-1>=0):#tenta mover o espaço branco p coluna anterior
        c = deepcopy(matrix)
        c[indice[0]][indice[1]-1] = ''
        c[indice[0]][indice[1]] = matrix[indice[0]][indice[1]-1]
        NosFilhos.append(c)
    if(indice[1]+1<=2):#tenta mover o espaço branco p coluna sucessora
        d = deepcopy(matrix)
        d[indice[0]][indice[1]+1] = ''
        d[indice[0]][indice[1]] = matrix[indice[0]][indice[1]+1]
        NosFilhos.append(d)
    if(indice[0]-1>=0):#tenta mover o espaço branco p linha anterior
        a = deepcopy(matrix) #copia a matriz original para a variável w
        a[indice[0]-1][indice[1]] = ''
        a[indice[0]][indice[1]] = matrix[indice[0]-1][indice[1]]
        NosFilhos.append(a)
    if(indice[0]+1<=2):#tenta mover o espaço branco p linha sucessora
        b = deepcopy(matrix)
        b[indice[0]+1][indice[1]] = ''
        b[indice[0]][indice[1]] = matrix[indice[0]+1][indice[1]]
        NosFilhos.append(b)
    return NosFilhos
    


def matrizNaTelaUpdate(mat):
    entrada.delete(0, END) #deleta o valor atual da entrada
    entrada2.delete(0, END) #deleta o valor atual da entrada
    entrada3.delete(0, END) #deleta o valor atual da entrada
    entrada4.delete(0, END) #deleta o valor atual da entrada
    entrada5.delete(0, END) #deleta o valor atual da entrada
    entrada6.delete(0, END) #deleta o valor atual da entrada
    entrada7.delete(0, END) #deleta o valor atual da entrada
    entrada8.delete(0, END) #deleta o valor atual da entrada
    entrada9.delete(0, END) #deleta o valor atual da entrada
    entrada.insert(0,mat[0][0])
    entrada2.insert(0,mat[0][1])
    entrada3.insert(0,mat[0][2])
    entrada4.insert(0,mat[1][0])
    entrada5.insert(0,mat[1][1])
    entrada6.insert(0,mat[1][2])
    entrada7.insert(0,mat[2][0])
    entrada8.insert(0,mat[2][1])
    entrada9.insert(0,mat[2][2])
    time.sleep(0.01)#para o programa nessa linha por 1,5 segundos

def somatorioMatriz(mat,matFinal=[['1','2','3'],['4','','5'],['6','7','8']]):#retorna o valor do somatorio da distancia relativa das peças para sua posição correta
    somatorio = 0
    for i in mat:
        for j in i:
            if not (j==''):#não considera a movimentação da pedra branca
                posAtual = encontraPosicao(mat,j)#(x,y) do pai atual
                posCerta = encontraPosicao(matFinal,j)#(x,y) da matriz final
                distDaPosicaoCerta = abs(posAtual[0]-posCerta[0]) + abs(posAtual[1]-posCerta[1])#Distância de Manhattan
                somatorio+=distDaPosicaoCerta
    return somatorio

def menorSomatorio(filhos=[]):#vê qual filho tem o menor somatório local(método guloso)
    distanciasDosFilhos = []
    for i in filhos:
        distanciasDosFilhos.append(somatorioMatriz(i))
    posVet = distanciasDosFilhos.index(min(distanciasDosFilhos))
    return filhos[posVet] #retorna o filho que tem a menor distancia das peças


def printaMatriz(matrix):#printa a matriz que foi passada
    for i in matrix:
        print(i)
    print()

def buscaEmProfundidade(mat,threadKill=False):#Completo (não guarda estados visitados)
    if not(encontraParidade(mat)): #verifica se a matriz não pode ser resolvida
        messagebox.showwarning('Impossível','Impossível Resolver.\nTente com outra entrada!')
        if(questao2):
                pb.destroy()
        return
    k="" #arvore em string
    nivel = 0 #guarda o nível atual da árvore
    arvore = Arvore() #Instancia a classe
    noNaoVisitado = [mat] #pilha já começa com o nó raiz
    flag = False #flag para exibir a árvore só uma vez
    custoDeEspaco = 0 #numero de filhos não expandidos
    while(len(noNaoVisitado)>0): #Enquanto tiver nós na pilha
        try:
            if(threadKill.wait(1)):
                break
        except:
            pass
        pai = noNaoVisitado.pop()#viu que matriz não era solução então tira da pilha
        if(questao2):
            matrizNaTelaUpdate(pai)
        if(np.array_equal(pai,[['1','2','3'],['4','','5'],['6','7','8']])): #Compara a matriz atual com a matriz de estado final
            messagebox.showinfo('Busca em Profundidade - Solução Encontrada',"A solução foi encontrada!\n"+
                                 "Custo do Caminho: "+str(nivel)+"\n"+
                                 "Custo de Espaço: "+str(custoDeEspaco)+"\n"+
                                 "Custo de Tempo: "+str(nivel+1)) #nivel + 1 pois conta com o nó raiz
            if(questao2):
                pb.destroy()
            elif(not flag and questao1):#se a árvore ainda não foi exibida
                arvore.mostraArvore(k)
            return
        nivel+=1
        vetPossiveis = filhosPossiveis(pai) #retorna os filhos possíveis do pai atual
        custoDeEspaco+= len(vetPossiveis)-1 #todos os filhos gerados tirando o filho que vai ser expandido
        shuffle(vetPossiveis)#embaralha os filhos
        if(questao1):
            k=arvore.stringArvore(vetPossiveis,str(pai),k)#função que auxilia para criar a arvore (cria todas aresta possíveis com o nó pai)
        noNaoVisitado.append(vetPossiveis[0])#add nó filhos na pilha 
        if nivel==50 and not flag and questao1: #mostra a arvore quando tá no nível 50
            flag=True
            arvore.mostraArvore(k)


def buscaEmLargura(pai,threadKill=False):#incompleto falta arrumar nível
    if not(encontraParidade(pai)): #verifica se a matriz não pode ser resolvida
        messagebox.showwarning('Impossível','Impossível Resolver.\nTente com outra entrada!')
        if(questao2):
                pb.destroy()
        return
    arvore = Arvore() #Instancia a classe e já cria o nó raiz
    visitados = [pai]#estados visitados
    noNaoVisitado = [pai] #fila já começa com o nó raiz
    flag = False #exibe a árvore só uma vez
    k=""
    custoTempo = 0
    while(len(noNaoVisitado)>0):#percorre a fila
        try:
            if(threadKill.wait(1)):
                break
        except:
            pass

        pai = noNaoVisitado[0]#primeiro da fila
        nivel = arvore.nivelDoNo(pai,k) #nível atual do nó corrente
        if(questao2):
            matrizNaTelaUpdate(pai)
        if(np.array_equal(pai,[['1','2','3'],['4','','5'],['6','7','8']])): #Compara a matriz atual com a matriz de estado final
            nivelNo = arvore.nivelDoNo(pai,k)
            messagebox.showinfo('Busca em Largura - Solução Encontrada',"A solução foi encontrada!\n"+
                                 "Custo do Caminho: "+str(nivelNo)+"\n"+
                                 "Custo de Espaço: "+str(len(noNaoVisitado))+"\n"+
                                 "Custo de Tempo: "+str(custoTempo)) #caminho: quant de nós até a solucao #tempo: quantidade de nós expandidos(pais)
            if(questao2):
                pb.destroy()
            elif(not flag and questao1):#se a árvore ainda não foi exibida
                arvore.mostraArvore(k)
            return
        #printaMatriz(pai)
        custoTempo+=1
        del(noNaoVisitado[0])#tira o nó pai da fila
        vetPossiveis = []  #retorna os filhos possíveis do nó pai
        for b in filhosPossiveis(pai)[::-1]:
            try:
                visitados.index(b)
                
            except ValueError:#se não foi visitado
                vetPossiveis.append(b)#filhos não repetidos
                noNaoVisitado.append(b)#add os filhos não visitados na fila
                visitados.append(b)
                if len(noNaoVisitado)==150 and not flag and questao1: #mostra a arvore quando tem 100 nós na fila
                    flag=True
                    arvore.mostraArvore(k)
        if (len(vetPossiveis)!=0): #se tiver filho para adicionar na árvore então...
            k=arvore.stringArvore(vetPossiveis,str(pai),k)#função que auxilia para criar a arvore (cria todas aresta possíveis com o nó pai)
    return



def buscaHeuristica(pai,threadKill=False):#completo #recebe o nó raiz primeiramente
    if not(encontraParidade(pai)): #verifica se a matriz não pode ser resolvida
        messagebox.showwarning('Impossível','Impossível Resolver.\nTente com outra entrada!')
        if(questao2):
                pb.destroy()
        return
    custoDeEspaco = 0 #numero de filhos não expandidos
    arvore = Arvore() #Instancia a classe e já cria o nó raiz
    k=""
    visitados = [pai]
    nivel = 0 #mostra o nível da árvore
    
    while(True):
        try:
            if(threadKill.wait(1)):
                break
        except:
            pass
        #printaMatriz(pai)
        if(np.array_equal(pai,[['1','2','3'],['4','','5'],['6','7','8']])): #Compara a matriz atual com a matriz de estado final
            messagebox.showinfo('Busca Gulosa - Solução Encontrada',"A solução foi encontrada!\n"+
                                 "Custo do Caminho: "+str(nivel)+"\n"+
                                 "Custo de Espaço: "+str(custoDeEspaco)+"\n"+
                                 "Custo de Tempo: "+str(nivel+1)) #nivel + 1 pois conta com o nó raiz
            if(questao2):
                pb.destroy()
            elif(questao1):#exibe a árvore somente no quando acha a resposta
                arvore.mostraArvore(k)
            return
        nivel+=1
        vetPossiveis = []
        for filho in filhosPossiveis(pai):
            try:
                visitados.index(filho)
            except ValueError:
                vetPossiveis.append(filho)
                visitados.append(filho)
        custoDeEspaco+= len(vetPossiveis)-1 #todos os filhos gerados tirando o filho que vai ser expandido
        if(vetPossiveis == []):
            messagebox.showwarning('Solução Inválida', 'Não foi encontrada uma solução para a matriz de entrada')
            return
        if(questao1):
            k=arvore.stringArvore(vetPossiveis,str(pai),k)#função que auxilia para criar a arvore (cria todas aresta possíveis com o nó pai)
        pai = menorSomatorio(vetPossiveis) #retorna o filho com as peças menos distantes da matriz correta e atribui como pai da vez
        if(questao2):
            matrizNaTelaUpdate(pai)


    

def A(pai,threadKill=False):#completo
    if not(encontraParidade(pai)): #verifica se a matriz não pode ser resolvida
        messagebox.showwarning('Impossível','Impossível Resolver.\nTente com outra entrada!')
        if(questao2):
                pb.destroy()
        return
    raiz = pai #raiz é a primeira matriz recebida
    arvore = Arvore() #Instancia a classe e já cria o nó raiz
    k=""
    quantNos = 0#quantidade de nós expandidos
    aberto = {}
    fechado = {0 + somatorioMatriz(pai) : [pai]}#matriz : matriz,f(n) = g(n)+h(n) #guarda os nós já expandidos
    custoDeEspaco = 0#quantidade de nós abertos
    while(True):
        try:
            if(threadKill.wait(1)):
                break
        except:
            pass
        #printaMatriz(pai)
        if(np.array_equal(pai,[['1','2','3'],['4','','5'],['6','7','8']])): #Compara a matriz atual com a matriz de estado final
            messagebox.showinfo('Busca A* Solução Encontrada',"Custo do Caminho: "+str(g)+"\n"+
                                "Custo do espaço:"+str(custoDeEspaco)+"\n"+
                                "Custo do tempo: "+str(quantNos+1))
            if(questao2):
                pb.destroy()
            elif(questao1):#exibe a árvore somente no quando acha a resposta
                arvore.mostraArvore(k)
            return
        quantNos+=1#quantidade na lista fechada
        vetPossiveis = []#são os filhos possiveis, não repetidos, que podem colocar como arestas com seu nó pai
        auxFilhos = filhosPossiveis(pai)
        g = arvore.nivelDoNo(pai,k)+1
        for filho in auxFilhos:
            if( str(aberto.values()).find(str(filho))==-1 and str(fechado.values()).find(str(filho))==-1):#verifica se o filho não está em aberto e nem em fechado
                    vetPossiveis.append(filho)
                    f = g + somatorioMatriz(filho) #manhatham do filho para a raiz + manhatham do filho para o objetivo
                    try:
                        aberto[f].append(filho) # se for a primeira matriz para aquela chave(f(n))
                    except:
                        aberto[f] = [filho]
        custoDeEspaco+= len(vetPossiveis)-1 #todos os filhos gerados tirando o filho que vai ser expandido
        if(len(vetPossiveis)!=0):#se tiver vetor para adicionar na arvore
            k=arvore.stringArvore(vetPossiveis[::-1],str(pai),k)#função que auxilia para criar a arvore (cria todas aresta possíveis com o nó pai)
        menorGlobal = min(aberto)
        pai = aberto[menorGlobal][0] #pega os filhos que tem os menores valores globais e escolhe o primeiro filho, dentre estes, para expandir
        del(aberto[menorGlobal][0])
        if(aberto[menorGlobal]==[]): # se ficar vazio então excluí a key do dicionário
            aberto.pop(menorGlobal,None)
        try:
            fechado[menorGlobal].append(pai) # se for a primeira matriz para aquela chave(f(n))
        except:
            fechado[menorGlobal] = [pai]
        if(questao2):
            matrizNaTelaUpdate(pai)
        

def start():
    global questao1,questao2,threadKill,thread
    mensagemProcessando["text"] = "Processando..."
    questao1 = messagebox.askyesno('Escolha','Deseja ver a árvore?\nObs: A árvore é exibida até certo nível!')#pergunta se sim ou não
    questao2 = False
    if not(questao1):
        questao2 = messagebox.askyesno('Escolha','Deseja ver a animação?')#pergunta se sim ou não
    matrix = [[entrada.get(),entrada2.get(),entrada3.get()],[entrada4.get(),entrada5.get(),entrada6.get()],[entrada7.get(),entrada8.get(),entrada9.get()]]
    print("Aguarde o resultado final!\n")
    if(str(escolha.get())=='profundidade'):
        if(questao2):
            mensagemProcessando["text"] = ""
            threadKill = threading.Event()
            thread=Thread(target=buscaEmProfundidade,args=(matrix,threadKill))#passa os parametros e a função para a thread
            thread.start()
            loadingStatus()
            return
        buscaEmProfundidade(matrix)
        mensagemProcessando["text"] = ""
    elif(str(escolha.get())=='largura'):
        if(questao2):
            mensagemProcessando["text"] = ""
            threadKill = threading.Event()
            thread=Thread(target=buscaEmLargura,args=(matrix,threadKill))#passa os parametros e a função para a thread
            thread.start()
            loadingStatus()
            return
        buscaEmLargura(matrix)
        mensagemProcessando["text"] = ""
    elif(str(escolha.get())=='heuristica'):
        if(questao2):
            mensagemProcessando["text"] = ""
            threadKill = threading.Event()
            thread=Thread(target=buscaHeuristica,args=(matrix,threadKill))#passa os parametros e a função para a thread
            thread.start()
            loadingStatus()
            return
        buscaHeuristica(matrix)
        mensagemProcessando["text"] = ""
    elif(str(escolha.get())=='A'):
        if(questao2):
            mensagemProcessando["text"] = ""
            threadKill = threading.Event()
            thread=Thread(target=A,args=(matrix,threadKill))#passa os parametros e a função para a thread
            thread.start()
            loadingStatus()
            return
        A(matrix)
        mensagemProcessando["text"] = ""
    else:
        messagebox.showinfo('Algoritmo não selecionado.',"Escolha um método de busca antes de iniciar!")
        


def telaHome():#reset
    apagaJanela()
    global entrada,entrada1,entrada2,entrada3,entrada4,entrada5,entrada6,entrada7,entrada8,entrada9,escolha,mensagemProcessando
    mensagem = Label(window, text="Insira o estado Inicial", font="impact 20 normal")
    mensagem.pack()
    jogoDosOito = Frame(window)
    jogoDosOito.pack()
    entrada = ttk.Entry(jogoDosOito, font="arial 15 bold",width=5)
    entrada.grid(row=0,column=0)
    entrada2 = ttk.Entry(jogoDosOito, font="arial 15 bold",width=5)
    entrada2.grid(row=0,column=1)
    entrada3 = ttk.Entry(jogoDosOito, font="arial 15 bold",width=5)
    entrada3.grid(row=0,column=2)
    entrada4 = ttk.Entry(jogoDosOito, font="arial 15 bold",width=5)
    entrada4.grid(row=1,column=0)
    entrada5 = ttk.Entry(jogoDosOito, font="arial 15 bold",width=5)
    entrada5.grid(row=1,column=1)
    entrada6 = ttk.Entry(jogoDosOito, font="arial 15 bold",width=5)
    entrada6.grid(row=1,column=2)
    entrada7 = ttk.Entry(jogoDosOito, font="arial 15 bold",width=5)
    entrada7.grid(row=2,column=0)
    entrada8 = ttk.Entry(jogoDosOito, font="arial 15 bold",width=5)
    entrada8.grid(row=2,column=1)
    entrada9 = ttk.Entry(jogoDosOito, font="arial 15 bold",width=5)
    entrada9.grid(row=2,column=2)
    
    #radioButtons:
    mensagemAlg = Label(window, text="Selecione um algoritmo de busca: ", font="arial 12 bold")
    mensagemAlg.pack()
    escolha = StringVar()#Guarda o valor escolhido
    escolha.set(1)
    escolha1 = ttk.Radiobutton(window,text='Busca em Profundidade', value='profundidade' ,cursor="hand2",variable = escolha)
    escolha2= ttk.Radiobutton(window,text='Busca em Largura', value='largura', cursor="hand2",variable = escolha)
    escolha3 = ttk.Radiobutton(window,text='Busca Heurística - Alg. Guloso', value='heuristica', cursor="hand2",variable = escolha)
    escolha4 = ttk.Radiobutton(window,text='Busca A*', value='A', cursor="hand2",variable = escolha)
    escolha1.pack(padx=(0,0))
    escolha2.pack(padx=(0,33))
    escolha3.pack(padx=(33,0))
    escolha4.pack(padx=(0,79))
    botao = ttk.Button(window, text="Começar", command=start,cursor="hand2")
    botao.pack()

    mensagemProcessando = Label(window, text="", font="Arial 10 normal")
    mensagemProcessando.pack()
def loadingStatus():
    frame = ttk.Frame()
    global pb
    pb = ttk.Progressbar(frame, length=300, mode='indeterminate')
    frame.pack()
    pb.pack()
    pb.start(10)#velocidade da barra
    
def all_children (window) :
    _list = window.winfo_children()
    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())
    return _list

def apagaJanela():
    try:
        if(thread.isAlive()):#se tiver alguma thread em execução então para ela
             threadKill.set()
    except:
        pass
    widget_list = all_children(window)
    for item in widget_list:
        item.pack_forget()


###main####        
if __name__ == "__main__":  
    window = Tk()#instanciamos a classe tk
    window.title("IA - Jogo dos Oito")
    window.geometry("300x320+200+100")#largura x altura + pos_x + posy
    menu = Menu(window)
    window.config(menu=menu)
    menu.add_cascade(label='Resetar',command=telaHome)
    telaHome()
    window.mainloop()


##########
