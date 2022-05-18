from tkinter import *
from arvore import Arvore

class Application():
    def __init__(self):
        self.arvore = Arvore()
        
        self.root = Tk()
        self.tela()
        self.create_frames()
        self.create_canvas()
        self.create_menu()
        self.root.mainloop()
    
    def tela(self):
        #função que determina o tamanho da tela do programa e coloca um título
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f'{int(self.screen_width*0.78)}x{int(self.screen_height*0.78)}+{10}+{10}')
        self.root.title('Arvore binária')
    
    def create_frames(self):
        #função que cria dois frames, um para o menu e outro para o canvas
        self.framemenu = Frame(self.root, bg='#fff')
        self.framemenu.place(relx=0, rely=0, relwidth=0.2, relheight=1)
        self.framecanvas = Frame(self.root)
        self.framecanvas.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)
        
    def create_canvas(self):
        #função que cria o canvas com as barras de rolagem vertical e horizontal
        self.canvas = Canvas(self.framecanvas, bg='#fff')
        self.canvas.place(relx=0, rely=0, relwidth=0.9823, relheight=0.975)
        self.scroll_x = Scrollbar(self.framecanvas, orient="horizontal", command=self.canvas.xview)
        self.scroll_x.place(relx=0, rely=0.975, relwidth=0.9823, relheight=0.025)
        self.scroll_y = Scrollbar(self.framecanvas, orient="vertical", command=self.canvas.yview)
        self.scroll_y.place(relx=0.9823, rely=0, relwidth=0.0177, relheight=1)
        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        
    def create_menu(self):
        #função que cria o menu
        self.entrada = Entry(self.framemenu, font=('arial',25), justify='center')
        self.entrada.place(relx=0, rely=0, relwidth=1, relheight=0.05)
        self.entrada.focus()
        
        self.adicionar = Button(self.framemenu, text='Adicionar', font=('arial', 15), command=self.adicionar_node)
        self.adicionar.place(relx=0, rely=0.05, relwidth=0.5, relheight=0.05)
        self.root.bind('<Return>',self.adicionar_node)
        
        self.remover = Button(self.framemenu, text='Remover', font=('arial', 15), command=self.remover_node)
        self.remover.place(relx=0.5, rely=0.05, relwidth=0.5, relheight=0.05)
        
        self.resetar = Button(self.framemenu, text='Resetar', font=('arial', 15), command=self.resetar_canvas)
        self.resetar.place(relx=0, rely=0.1, relwidth=1, relheight=0.05)
        
        self.entradaprocurar = Entry(self.framemenu, font=('arial',25), justify='center')
        self.entradaprocurar.place(relx=0, rely=0.25, relwidth=1, relheight=0.05)
        
        self.botaoprocurar = Button(self.framemenu, text='Procurar nó', font=('arial', 15), command=self.buscar_node_mostrar_info)
        self.botaoprocurar.place(relx=0, rely=0.3, relwidth=1, relheight=0.05)
        
        self.areainfo = Text(self.framemenu, font=('arial', 15))
    
    def buscar_node_mostrar_info(self):
        #função que mostra as informações de um nó caso ele exista
        numero = self.entradaprocurar.get()
        if numero.lstrip('-').isnumeric():
            numero = int(numero)
            node = self.arvore.procurar_node(numero, self.arvore.raiz)
            if node:
                self.areainfo.place(relx=0, rely=0.35, relwidth=1, relheight=0.15)
                self.areainfo.delete('1.0', END)
                eraiz = 'Não' if node.pai else 'Sim'
                efolha = 'Não' if node.esquerda or node.direita else 'Sim'
                self.areainfo.insert(INSERT, f'Valor: {node.conteudo}\n'
                                             f'Nível: {node.nivel}\n'
                                             f'É raiz? {eraiz}\n'
                                             f'É folha? {efolha}\n'
                                             f'Altura da árvore: {self.arvore.altura}')
            else:
                self.areainfo.place(relx=0, rely=0.35, relwidth=1, relheight=0.15)
                self.areainfo.delete('1.0', END)
                self.areainfo.insert(INSERT, 'Nó não encontrado')
    
    def resetar_canvas(self):
        #função que limpa o canvas e cria uma nova instancia de Arvore
        self.arvore = Arvore()
        self.canvas.delete('all')
        self.areainfo.delete('1.0', END)
        self.areainfo.place_forget()
    
    def remover_node(self):
        #função responsável por remover e ajustar os nós graficamente
        numero = self.entrada.get()
        if numero.lstrip('-').isnumeric():
            numero = int(numero)
            node = self.arvore.remove_node(numero)
            if node[0]:
                #se algum nó foi removido 
                if node[1] == None:
                    #se o nó removido era folha
                    self.canvas.delete(node[0].idtext, node[0].idcircle, node[0].idline)
                    if node[0].pai:
                        #se o nó removido tem pai
                        if node[0].pai != self.arvore.raiz and not node[0].pai.esquerda and not node[0].pai.direita:
                            #se o pai do nó removido é diferente da raiz e pai do nó removido é folha
                            self.canvas.itemconfig(node[0].pai.idcircle, fill='green')
                    return
                self.canvas.delete(node[0].idtext, node[0].idcircle, node[0].idline)
                self.redesenhar_nodes(node[1], node[0])
    
    def redesenhar_nodes(self, node, nodeexcluido):
        #função que exclui e desenha novamente todos os nós abaixo do nó removido
        if node:
            self.canvas.delete(node.idtext, node.idcircle, node.idline)
            if node == self.arvore.raiz:
                #se o nó substituto é a raiz ele vai receber a cor preta
                node.idcircle = self.canvas.create_oval(node.x, node.y, node.x+80, node.y+80, fill='black')
                node.idtext = self.canvas.create_text(node.x+40, node.y+40, text=str(node.conteudo), fill="white", font=(f'Arial 25 bold'))
            else:
                #se o nó substituto não é a raiz
                node.idline = self.canvas.create_line(node.pai.x+40, node.pai.y+40, node.x+40, node.y+40, width=5)
                self.canvas.tag_lower(node.idline, node.pai.idcircle)
                if node.esquerda or node.direita:
                    #se o nó substituto tiver filho ele vai receber a cor marrom
                    node.idcircle = self.canvas.create_oval(node.x, node.y, node.x+80, node.y+80, fill='brown')
                else:
                    #se o nó substituto for folha ele vai receber a cor verde
                    node.idcircle = self.canvas.create_oval(node.x, node.y, node.x+80, node.y+80, fill='green')
                node.idtext = self.canvas.create_text(node.x+40, node.y+40, text=str(node.conteudo), fill="white", font=(f'Arial 25 bold'))
            self.redesenhar_nodes(node.esquerda, nodeexcluido)
            self.redesenhar_nodes(node.direita, nodeexcluido)
    
    def adicionar_node(self, event=None):
        #função que adiciona o nó graficamente
        numero = self.entrada.get()
        if numero.lstrip('-').isnumeric():
            numero = int(numero)
            if not self.arvore.raiz:
                #se a árvora ainda não tem nenhum elemento
                node = self.arvore.insert_node(numero)
                if node:
                    xbola = int((self.screen_width*0.78*0.9823*0.8)/2-40)
                    node.x = xbola
                    node.y = 10
                    node.idcircle = self.canvas.create_oval(node.x, node.y, node.x+80, node.y+80, fill='black')
                    node.idtext = self.canvas.create_text(node.x+40, node.y+40, text=str(node.conteudo), fill="white", font=(f'Arial 25 bold'))
                return
            node = self.arvore.insert_node(numero)
            if node:
                if node.pai != self.arvore.raiz:
                    #se o pai do nó adicionado não é a raiz ele recebe a cor marrom
                    self.canvas.itemconfig(node.pai.idcircle, fill='brown')
                mdistanciatemp = self.arvore.multiplicadordistancia-node.nivel+1
                if mdistanciatemp < 0:
                    mdistanciatemp = 0
                node.y = node.pai.y+80
                if node.orientacao == 'direita':
                    node.x = node.pai.x + (2**mdistanciatemp)*80
                else:
                    node.x = node.pai.x - (2**mdistanciatemp)*80
                node.idline = self.canvas.create_line(node.pai.x+40, node.pai.y+40, node.x+40, node.y+40, width=5)
                self.canvas.tag_lower(node.idline, node.pai.idcircle)
                node.idcircle = self.canvas.create_oval(node.x, node.y, node.x+80, node.y+80, fill='green')
                node.idtext = self.canvas.create_text(node.x+40, node.y+40, text=str(node.conteudo), fill="white", font=(f'Arial 25 bold'))
                if self.verifica_colisao(node, self.arvore.raiz):
                    #depois de inserido o novo nó se houver colisão com outro nó o espaço entre os nós será aumentado
                    self.arvore.multiplicadordistancia = node.nivel-1
                    self.aumentar_distancia(self.arvore.multiplicadordistancia+1, self.arvore.raiz)
                self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def aumentar_distancia(self, multiplicadordistancia, atual):
        #função que percorre os nós desde a raiz aumentando a distância entre eles de acordo com o fator multiplicadordistancia
        if atual:
            if atual.pai:
                if multiplicadordistancia < 0:
                    multiplicadordistancia = 0
                if atual.orientacao == 'direita':
                    xrelativo = atual.x
                    atual.x = atual.pai.x + (2**multiplicadordistancia)*80
                    xrelativo = atual.x - xrelativo 
                else:
                    xrelativo = atual.x
                    atual.x = atual.pai.x - (2**multiplicadordistancia)*80
                    xrelativo = atual.x - xrelativo
                self.canvas.move(atual.idcircle, xrelativo, 0)
                self.canvas.move(atual.idtext, xrelativo, 0)
                self.canvas.delete(atual.idline)
                atual.idline = self.canvas.create_line(atual.pai.x+40, atual.pai.y+40, atual.x+40, atual.y+40, width=5)
                self.canvas.tag_lower(atual.idline, atual.pai.idcircle)
            self.aumentar_distancia(multiplicadordistancia-1, atual.esquerda)
            self.aumentar_distancia(multiplicadordistancia-1, atual.direita)
    
    def verifica_colisao(self, node, atual):
        #função que verifica se um nó colidiu com o outro retornando True se colidiu e False caso contrário
        if not atual:
            return False
        if self.verifica_colisao(node, atual.esquerda):
            return True
        if self.verifica_colisao(node, atual.direita):
            return True
        if atual.nivel == node.nivel:
            if atual.x == node.x and atual.idcircle != node.idcircle:
                return True
        return False

Application()
