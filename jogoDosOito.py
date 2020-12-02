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
         posPai = kw.find(pai)
         return kw[:posPai] +aux+ kw[posPai:] #escreve os filhos na string pai correspondente


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
    time.sleep(1)#para o programa nessa linha por 1,5 segundos

def buscaEmProfundidade(mat,threadKill=False):#Completo (guardando estados visitados)
    k="" #arvore em string
    arvore = Arvore() #Instancia a classe
    noNaoVisitado = [mat] #pilha já começa com o nó raiz
    flag = False #flag para exibir a árvore só uma vez
    while(len(noNaoVisitado)>0): #Enquanto tiver nós na pilha
        try:
            if(threadKill.wait(1)):
                break
        except:
            pass
        pai = noNaoVisitado.pop()#viu que matriz não era solução então tira da pilha
        if(np.array_equal(pai,[['1','2','3'],['4','','5'],['6','7','8']])): #Compara a matriz atual com a matriz de estado final
            print("ACHOU A SOLUÇÃO")
            print("Quantidade na Pilha:",len(noNaoVisitado))
            print("Quant de nós visitados",len(arvore.dicio))
            if(questao2):
                pb.destroy()
            elif(not flag and questao1):#se a árvore ainda não foi exibida
                arvore.mostraArvore(k)
            return
        vetPossiveis = filhosPossiveis(pai) #retorna os filhos possíveis da raiz
        shuffle(vetPossiveis)#embaralha os filhos
        k=arvore.stringArvore(vetPossiveis,str(pai),k)#função que auxilia para criar a arvore (cria todas aresta possíveis com o nó pai)
        #print(k)
        for i in vetPossiveis:#percore os nós filhos de trás para frente
            noNaoVisitado.append(i)#add todos nós filhos    
            if len(noNaoVisitado)==250 and not flag and questao1: #mostra a arvore quando tem 250 nós na pilha
                flag=True
                arvore.mostraArvore(k)
            if len(noNaoVisitado)>=42000:#se der mais de 42.000 nós na pilha já gera exception pois o programa vai travar e fechar
                pb.destroy()
                messagebox.showerror('Erro', 'Estouro de Pilha')
                raise OverflowError
                return
        if(questao2):
            matrizNaTelaUpdate(pai)
def buscaEmLargura(mat):#incompleto
    arvore = Arvore(mat) #Instancia a classe e já cria o nó raiz
    noNaoVisitado = [mat] #pilha já começa com o nó raiz
    flag = False #exibe a árvore só uma vez
    k=""
    while(len(noNaoVisitado)>0):
        if(np.array_equal(mat,[['1','2','3'],['4','','5'],['6','7','8']])): #Compara a matriz atual com a matriz de estado final
            print("ACHOU A SOLUÇÃO")
            print("Quantidade na Pilha:",len(noNaoVisitado))
            print("Quant de nós visitados",len(arvore.dicio))
            if not(flag):#se a árvore ainda não foi exibida
                mostraArvore(k)
            return     
    return
def buscaHeuristica(mat):#incompleto
    return
def A(mat):#incompleto
    return

def start():
    global questao1,questao2,threadKill,thread
    questao1 = messagebox.askyesno('Escolha','Deseja ver a árvore?')#pergunta se sim ou não
    questao2 = False
    if not(questao1):
        questao2 = messagebox.askyesno('Escolha','Deseja ver a animação?')#pergunta se sim ou não
    matrix = [[entrada.get(),entrada2.get(),entrada3.get()],[entrada4.get(),entrada5.get(),entrada6.get()],[entrada7.get(),entrada8.get(),entrada9.get()]]
    print("Aguarde o resultado final!\n")
    if(str(escolha.get())=='profundidade'):
        if(questao2):
            threadKill = threading.Event()
            thread=Thread(target=buscaEmProfundidade,args=(matrix,threadKill))#passa os parametros e a função para a thread
            thread.start()
            loadingStatus()
            return
        buscaEmProfundidade(matrix)
    elif(str(escolha.get())=='largura'):
        buscaEmLargura(matrix)
    elif(str(escolha.get())=='heuristica'):
        buscaHeuristica(matrix)
    elif(str(escolha.get())=='A'):
        A(matrix)
        
    

###main####
def telaHome():
    apagaJanela()
    global entrada,entrada1,entrada2,entrada3,entrada4,entrada5,entrada6,entrada7,entrada8,entrada9,escolha
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
    mensagem = Label(window, text="Selecione um algoritmo de busca: ", font="arial 12 bold")
    mensagem.pack()
    escolha = StringVar()#Guarda o valor escolhido
    escolha.set(1)
    escolha1 = ttk.Radiobutton(window,text='Busca em Profundidade', value='profundidade' ,cursor="hand2",variable = escolha)
    escolha2= ttk.Radiobutton(window,text='Busca em Largura', value='largura', cursor="hand2",variable = escolha)
    escolha3 = ttk.Radiobutton(window,text='Busca Heurística', value='heuristica', cursor="hand2",variable = escolha)
    escolha4 = ttk.Radiobutton(window,text='Busca A*', value='A', cursor="hand2",variable = escolha)
    escolha1.pack(padx=(0,0))
    escolha2.pack(padx=(0,33))
    escolha3.pack(padx=(0,39))
    escolha4.pack(padx=(0,79))
    botao = ttk.Button(window, text="Começar", command=start,cursor="hand2")
    botao.pack()

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
        
if __name__ == "__main__":  
    window = Tk()#instanciamos a classe tk
    window.title("IA - Jogo dos Oito")
    window.geometry("300x300+200+100")#largura x altura + pos_x + posy
    menu = Menu(window)
    window.config(menu=menu)
    menu.add_cascade(label='Resetar',command=telaHome)
    telaHome()
    window.mainloop()


##########
