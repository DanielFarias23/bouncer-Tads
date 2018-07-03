import sys, pygame, os
pygame.init()

size = largura, altura = 600, 400
tela = pygame.display.set_mode(size)
black = 0, 0, 0
pygame.font.init()
fonte = pygame.font.get_default_font()
jogo_fonte = pygame.font.SysFont(fonte,50)
perdeu = jogo_fonte.render('PERDEU',1,(255,255,255))


class Bouncer(pygame.sprite.Sprite):
    """classe para a barrinha"""
    def __init__(self, startpos):
        pygame.sprite.Sprite.__init__(self)
        self.direction = 1
        self.image, self.rect = load_image('bouncer.gif')
        self.rect.centerx = startpos[0]
        self.rect.centery = startpos[1]
    
    def update(self):
        self.rect.move_ip((self.direction*3,0))
        if self.rect.left < 0:
            self.direction = 1
        elif self.rect.right > largura:
            self.direction = -1

class Ball(pygame.sprite.Sprite):
    """classe para o sanduiche"""
    def __init__(self, startpos):
        pygame.sprite.Sprite.__init__(self)
        self.speed = [2,2]
        self.image, self.rect = load_image('ball.gif')
        self.rect.centerx = startpos[0]
        self.rect.centery = startpos[1]
        self.init_pos = startpos
    
    def update(self):
        self.rect.move_ip(self.speed)
        if self.rect.left < 0 or self.rect.right > largura:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0: 
            self.speed[1] = -self.speed[1]
        if self.rect.bottom > altura:
            tela.blit(perdeu,(0,0))
            self.rect.centerx = self.init_pos[0]
            self.rect.centery = self.init_pos[1]

def load_image(name):
    #carrega uma imagem, e retorna a imagem e o seu rect (retangulo)"""
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print ('Não é possivel carregar a imagem:'), fullname
        raise sys.exit
    return image, image.get_rect()

def main():
    #cria os nossos objetos (sanduiche e bouncer)
    sanduiche = Ball([100,100])
    barra = Bouncer([20,395])
    pygame.display.set_caption('Bouncer Sandwich')
    clock = pygame.time.Clock()




    while 1:
        #o programa nao vai rodar a mais que 120fps
        clock.tick(120)

        #checando eventos de teclado
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
               sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    barra.direction = -1
                if event.key == pygame.K_RIGHT:
                    barra.direction = 1
        
        #checa se sanduiche colidiu na barra, e caso sim inverte a direcao vertical do sanduiche
        if barra.rect.colliderect(sanduiche.rect):
           if sanduiche.speed[1] > 0:
              sanduiche.speed[1] = -sanduiche.speed[1]


        #atualiza os objetos
        sanduiche.update()
        barra.update()
    
        #redesenha a tela
        tela.fill(black)
        tela.blit(sanduiche.image, sanduiche.rect)
        tela.blit(barra.image, barra.rect)
        pygame.display.flip()
    
if __name__ == "__main__":
    main()