#pip install PyQt5 + pptree + numpy + tkinter + copy + ete3
from pptree import *
import numpy as np
from tkinter import * #importamos o pacote tkinter
import tkinter.ttk as ttk
from copy import deepcopy
from ete3 import Tree, TreeStyle, Tree, TextFace, add_face_to_node

##Funções e Classes##

class Arvore:
    def __init__(self,matrizInicial):#construtor
        self.raiz = Node(matrizInicial)
        self.dicio = {}#guarda tds estados visitados
        self.dicio[str(matrizInicial)] = self.raiz #guarda a pos na memoria da raiz
        self.arestas = []
    def printArvore(self):# printa a árvore atual    
        print_tree(self.raiz, horizontal=False)
    def criaAresta(self,no2,no1):#no2 = nó pai no1= nó filho
        self.arestas.append((str(no2.name),str(no1)))
        self.dicio[str(no1)] = Node(str(no1),no2)

def encontraPosicao(matrix,value = ''):#retorna a posicao(linha,coluna) de um valor na matriz
    return [(index, row.index(value)) for index, row in enumerate(matrix) if value in row][0]

def filhosPossiveis(matrix): #retorna todos os filhos possiveis do estado em branco
    indice = encontraPosicao(matrix) #retorna o indice do espaço em branco na matrix (linha,coluna)
    NosFilhos = [] #vetor que guarda todos filhos possiveis(matrizes)
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
    return NosFilhos

def mostraArvore(arestas=[]):#passa todos as arestas para exibir a árvore
    for i in range(len(arestas)):
        arestas[i] = list(arestas[i])
        arestas[i][0] = arestas[i][0].replace("], [","\n").replace("[","").replace("]","")
        arestas[i][1] = arestas[i][1].replace("], [","\n").replace("[","").replace("]","")
        arestas[i] = tuple(arestas[i])
    t = Tree.from_parent_child_table(arestas)
    ts = TreeStyle()
    ts.show_leaf_name = False
    def my_layout(node): #coloca o nome em cada nó
            F = TextFace(node.name, tight_text=True)
            add_face_to_node(F, node, column=0, position="branch-right")
            F.rotation = -90#rotação do nome no nó
        
    ts.layout_fn = my_layout
    ts.rotation = 90#exibir árvore na vertical
    t.show(tree_style=ts)#mostra árvore


def buscaEmProfundidade(mat):#incompleto
    arvore = Arvore(mat) #Instancia a classe e já cria o nó raiz
    noNaoVisitado = [mat] #pilha já começa com o nó raiz
    while(len(noNaoVisitado)>0):
        pai = noNaoVisitado.pop()#viu que matriz não era solução então tira da pilha
        mat = pai
        #for i in pai: #printa o nó em que o algoritmo está no momento
        #    print(i)
        #print("\n\n")
        if(np.array_equal(mat,[['1','2','3'],['4','5','6'],['7','8','']])): #Compara a matriz atual com a matriz de estado final
            print("ACHOU A SOLUÇÃO")
            print("Quantidade na Pilha:",len(noNaoVisitado))
            #print(arvore.arestas[0])
            return
        for i in filhosPossiveis(mat)[::-1]:#percore os nós filhos de trás para frente
            try:
                arvore.dicio[str(i)] #verifica se o filho está no dicionário
            except:#se não tiver no dicionario(filho visitado) então adiciona ao dicionario
                arvore.criaAresta(arvore.dicio[str(pai)],i)
                noNaoVisitado.append(i)#add todos nós filhos
        if len(noNaoVisitado)==100: #mostra a arvore quando tem 100 nós na pilha
            mostraArvore(arvore.arestas)
        #print(arvore.arestas[0])
    raise OverflowError
    
    
    
def buscaEmLargura(mat):#incompleto
    return
def BuscaHeuristica(mat):#incompleto
    return
def A(mat):#incompleto
    return

def start():
    matrix = [[entrada.get(),entrada2.get(),entrada3.get()],[entrada4.get(),entrada5.get(),entrada6.get()],[entrada7.get(),entrada8.get(),entrada9.get()]]
    #print(matrix)
    print("Aguarde o resultado final!\n")
    if(str(escolha.get())=='profundidade'):
        buscaEmProfundidade(matrix)
    elif(str(escolha.get())=='largura'):
        buscaEmLargura(matrix)
    elif(str(escolha.get())=='heuristica'):
        buscaHeuristica(matrix)
    elif(str(escolha.get())=='A'):
        A(mat)
        
    

###main####

window = Tk()#instanciamos a classe tk
window.title("IA - Jogo dos Oito")
window.geometry("300x300+200+100")#largura x altura + pos_x + posy

mensagem = Label(window, text="Insira o estado Inicial", font="impact 20 bold")
mensagem.pack()
jogoDosOito = Frame(window)
jogoDosOito.pack()
entrada = Entry(jogoDosOito, font="arial 15 bold",width=5)
entrada.grid(row=0,column=0)
entrada2 = Entry(jogoDosOito, font="arial 15 bold",width=5)
entrada2.grid(row=0,column=1)
entrada3 = Entry(jogoDosOito, font="arial 15 bold",width=5)
entrada3.grid(row=0,column=2)
entrada4 = Entry(jogoDosOito, font="arial 15 bold",width=5)
entrada4.grid(row=1,column=0)
entrada5 = Entry(jogoDosOito, font="arial 15 bold",width=5)
entrada5.grid(row=1,column=1)
entrada6 = Entry(jogoDosOito, font="arial 15 bold",width=5)
entrada6.grid(row=1,column=2)
entrada7 = Entry(jogoDosOito, font="arial 15 bold",width=5)
entrada7.grid(row=2,column=0)
entrada8 = Entry(jogoDosOito, font="arial 15 bold",width=5)
entrada8.grid(row=2,column=1)
entrada9 = Entry(jogoDosOito, font="arial 15 bold",width=5)
entrada9.grid(row=2,column=2)

#radioButtons:
escolha = StringVar()#Guarda o valor escolhido
escolha1 = Radiobutton(window,text='Busca em Profundidade', value='profundidade', tristatevalue=0,variable = escolha)
escolha2= Radiobutton(window,text='Busca em Largura', value='largura', tristatevalue=0,variable = escolha)
escolha3 = Radiobutton(window,text='Busca Heurística', value='heuristica', tristatevalue=0,variable = escolha)
escolha4 = Radiobutton(window,text='Busca A*', value='A', tristatevalue=0,variable = escolha)
escolha1.pack()
escolha2.pack()
escolha3.pack()
escolha4.pack()
botao = ttk.Button(window, text="Começar", command=start,cursor="hand2")
botao.pack()

window.mainloop()


##########
