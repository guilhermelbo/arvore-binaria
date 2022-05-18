class Arvore:
    def __init__(self):
        self.raiz = None
        self.altura = 0
        self.multiplicadordistancia = 0
        
    def insert_node(self, numero):
        #insere os nós na árvore
        if not self.raiz:
            #se não existir nenhum nó
            self.altura = 1
            self.raiz = self.Node(numero, nivel=0)
            return self.raiz
        atual = self.raiz
        while True:
            if numero > atual.conteudo:
                #se o número a ser inserido é maior que o número do nó atual
                if atual.direita:
                    #enquanto o nó atual tiver filho a sua direita ele continuar indo para a direita
                    atual = atual.direita
                    continue
                if atual.nivel+2 > self.altura:
                    self.altura = atual.nivel+2
                #quando o número for maior que o nó atual e o nó atual não tiver mais filho a sua direita ele criará um novo nó
                atual.direita = self.Node(numero, pai=atual, orientacao='direita', nivel=atual.nivel+1)
                return atual.direita
            if numero < atual.conteudo:
                #se o número a ser inserido é menor que o número do nó atual
                if atual.esquerda:
                    #enquanto o nó atual tiver filho a sua esquerda ele vai continuar indo para a esquerda
                    atual = atual.esquerda
                    continue
                if atual.nivel+2 > self.altura:
                    self.altura = atual.nivel+2
                #quando o número for menor que o nó atual e o nó atual não tiver mais filho a sua esquerda ele criará um novo nó
                atual.esquerda = self.Node(numero, pai=atual, orientacao='esquerda', nivel=atual.nivel+1)
                return atual.esquerda
            #retornará falso sempre que o número a ser inserido for igual a algum já inserido
            return False
        
    def remove_node(self, numero):
        #remove os nós na árvore
        if self.raiz:
            substituto = None
            node = self.procurar_node(numero, self.raiz)
            if node:
                #se o nó existe
                if node.direita:
                    #se o nó tem filho a direita
                    substituto = self.sucessor_node(node.direita)
                    if node.direita == substituto:
                        #se o filho da direita é igual ao nó substituto
                        substituto.esquerda = node.esquerda
                        self.transfere_info_basicas(node, substituto)
                    elif substituto.direita:
                        #caso o filho da direita não seja igual ao substituto e o substituto tenha filho a sua direita
                        substituto.direita.pai = substituto.pai
                        substituto.pai.esquerda = substituto.direita
                        substituto.direita.orientacao = 'esquerda'
                        node.direita.pai = substituto
                        substituto.direita = node.direita
                        substituto.esquerda = node.esquerda
                        self.transfere_info_basicas(node, substituto)
                    else:
                        #caso o filho da direita não seja igual ao substituto e o substituto não tenha filho a sua direita
                        substituto.pai.esquerda = None
                        node.direita.pai = substituto
                        substituto.direita = node.direita
                        substituto.esquerda = node.esquerda
                        self.transfere_info_basicas(node, substituto)
                    if node.esquerda:
                        #se o nó tem filho a esquerda
                        node.esquerda.pai = substituto
                    
                elif node.esquerda:
                    #se o nó não tenha filho a sua direita e tenha a sua esquerda
                    substituto = self.antecessor_node(node.esquerda)
                    if node.esquerda == substituto:
                        #se o filho a esquerda do nó seja igual ao nó substituto
                        self.transfere_info_basicas(node, substituto)
                    elif substituto.esquerda:
                        #caso o filho a esquerda do nó não seja igual ao nó substituto e o nó substituto tenha filho a sua esquerda
                        substituto.pai.direita = substituto.esquerda
                        substituto.esquerda.pai = substituto.pai
                        substituto.esquerda.orientacao = 'direita'
                        node.esquerda.pai = substituto
                        substituto.esquerda = node.esquerda
                        self.transfere_info_basicas(node, substituto)
                    else:
                        #caso o filho a esquerda do nó não seja igual ao nó substituto e o nó substituto não tenha filho a sua esquerda
                        substituto.pai.direita = None
                        node.esquerda.pai = substituto
                        substituto.esquerda = node.esquerda
                        self.transfere_info_basicas(node, substituto)
                        
                else:
                    #se o nó é folha
                    if node == self.raiz:
                        #se o nó é folha e é a raiz
                        self.raiz = None
                    else:
                        #se o nó é folha mas não é a raiz
                        if node.orientacao == 'direita':
                            node.pai.direita = None
                        else:
                            node.pai.esquerda = None
                            
                if node == self.raiz:
                    #se o nó é raiz e tem substituto
                    if substituto:
                        self.raiz = substituto
                else:
                    #se o nó não é raiz e tem substituto
                    if substituto:
                        if substituto.orientacao == 'direita':
                            substituto.pai.direita = substituto
                        else:
                            substituto.pai.esquerda = substituto
                
                self.corrige_nivel(substituto)
                self.corrige_x_y(substituto)
                self.altura = self.calcula_altura(self.raiz)
                
                #retorna o nó removido e o nó substituto
                return node, substituto
        #retorna None,None sempre que a árvore estiver vazia ou quando o número não existir 
        return None,None
    
    def calcula_altura(self, node):
        #função que retorna a altura da árvore
        if node:
            esquerda = self.calcula_altura(node.esquerda)
            direita = self.calcula_altura(node.direita)
            if esquerda > direita:
                return esquerda + 1
            else:
                return direita + 1
        return 0
    
    def corrige_nivel(self, node):
        #função que percorre todos os nós a partir do nó passado e corrige o seu nível em relação ao nível de seu pai
        #caso o nó não tenha pai significa que ele é a raiz e o seu nível já foi ajustado anteriormente para 0
        if node:
            if node.nivel != 0:
                node.nivel = node.pai.nivel+1
            self.corrige_nivel(node.esquerda)
            self.corrige_nivel(node.direita)
    
    def corrige_x_y(self, node):
        #função que percorre todo os nós a partir do nó passado e corrige as suas coordenadas x e y em relação as coordenadas de seu pai
        #caso o nó não tenha pai significa que ele é a raiz e as suas coordenadas já foram ajustadas anteriormente
        if node:
            if node.pai:
                mdistanciatemp = self.multiplicadordistancia-node.nivel+1
                if mdistanciatemp < 0:
                    mdistanciatemp = 0
                node.y = node.pai.y+80
                if node.orientacao == 'direita':
                    node.x = node.pai.x + (2**mdistanciatemp)*80
                else:
                    node.x = node.pai.x - (2**mdistanciatemp)*80
            self.corrige_x_y(node.esquerda)
            self.corrige_x_y(node.direita)
    
    def transfere_info_basicas(self, node, substituto):
        #função que transfere algumas informações básicas de um nó para outro quando é feita a remoção de algum nó
        substituto.x = node.x
        substituto.y = node.y
        substituto.orientacao = node.orientacao
        substituto.nivel = node.nivel
        substituto.pai = node.pai
    
    def sucessor_node(self, node):
        #função que retorna o menor nó a direita do nó passado
        if node.esquerda:
            return self.sucessor_node(node.esquerda)
        return node
        
    def antecessor_node(self, node):
        #função que retorna o maior nó a esquerda do nó passado 
        if node.direita:
            return self.antecessor_node(node.direita)
        return node
        
    def procurar_node(self, numero, atual):
        #função que procura e retorna um nó caso ele exista 
        if atual:
            if numero == atual.conteudo:
                return atual
            elif numero > atual.conteudo:
                return self.procurar_node(numero, atual.direita)
            else: 
                return self.procurar_node(numero, atual.esquerda)
        return None
            
    class Node:
        def __init__(self, numero, pai=None, orientacao=None, nivel=None):
            self.conteudo = numero
            self.esquerda = None
            self.direita = None
            self.x = None
            self.y = None
            self.orientacao = orientacao
            self.nivel = nivel
            self.pai = pai
            self.idcircle = None
            self.idtext = None
            self.idline = None