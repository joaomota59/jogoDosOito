from pptree import *
import numpy as np
from tkinter import * #importamos o pacote tkinter
from copy import deepcopy

##Funções e Classes##

def encontraPosicao(matrix,value = ''):#retorna a posicao(linha,coluna) de um valor na matriz
    return [(index, row.index(value)) for index, row in enumerate(matrix) if value in row][0]

class Arvore:
    def __init__(self,matrizInicial):#construtor
        self.raiz = Node(matrizInicial)
    def printArvore(self):# printa a árvore atual
        print_tree(self.raiz, horizontal=False)
    #def criaAresta(no1,no2)


########
#k = Arvore(matrix)
#k.printArvore()

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

def buscaEmProfundidade(mat):#incompleto
    if(np.array_equal(mat,[['1','2','3'],['4','5','6'],['7','8','']])): #Compara a matriz atual com a matriz de estado final
        return True
    
    
    
    
def buscaEmLargura(mat):#incompleto
    return
def BuscaHeuristica(mat):#incompleto
    return
def A(mat):#incompleto
    return

def start():
    matrix = [[entrada.get(),entrada2.get(),entrada3.get()],[entrada4.get(),entrada5.get(),entrada6.get()],[entrada7.get(),entrada8.get(),entrada9.get()]]
    print(matrix)
    raiz = Arvore(matrix)
    
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
botao = Button(window, text="Começar", command=start)
botao.pack()

window.mainloop()


##########
