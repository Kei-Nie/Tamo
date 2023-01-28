import pygame
class MainGame():
    window= None
    screenheight=500
    screenwidth=800
    color=pygame.Color(30,30,30)
    fontcolor=pygame.Color(255,0,0)
    tankp1=None


    def __init__(self):
        pass
    def startgame(self):
        pygame.display.init()
        MainGame.window=pygame.display.set_mode([MainGame.screenwidth,MainGame.screenheight])
        MainGame.tankp1=Tank(250,250)
        pygame.display.set_caption("Tank War V1.03")
        while True:
            MainGame.window.fill(MainGame.color)
            self.getevent()
            MainGame.window.blit(self.gettextsurface("the remaining tank number is %d"%5),(5,5))
            MainGame.tankp1.displaytank()
            pygame.display.update()
    def endgame(self):
        print("thanks for playing")
        exit()
    def getevent(self):
        eventlist = pygame.event.get()
        for event in eventlist:
            if event.type == pygame.QUIT:
                self.endgame()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    print("the tank moves to the left")
                elif event.key==pygame.K_RIGHT:
                    print("the tank moves to the right")
                elif event.key==pygame.K_UP:
                    print("the tank moves to the up")
                elif event.key==pygame.K_DOWN:
                    print("the tank moves to the down")
                elif event.key==pygame.K_SPACE:
                    print("the tank is going to shot")
    def gettextsurface(self,text):
        pygame.font.init()
        font=pygame.font.SysFont("laoui",18)
        textsurface=font.render(text,True,MainGame.fontcolor)
        return textsurface




class Tank():
    def __init__(self,left,top):
        self.images = {
            "U":pygame.image.load('tankimages/tankup.jpg'),
            "D":pygame.image.load('tankimages/tankdown.jpg'),
            "L":pygame.image.load('tankimages/tankleft.jpg'),
            "R":pygame.image.load('tankimages/tankright.jpg')
            }
        self.direction = "U"
        self.image =self.images[self.direction]
        self.rect=self.image.get_rect()
        self.rect.left=left
        self.rect.top=top

    def move(self):
        pass
    def shot(self):
        pass
    def displaytank(self):
        self.image = self.images[self.direction]
        MainGame.window.blit(self.image,self.rect)
class Mytank(Tank):
    def __init__(self):
        pass


class EnemyTank(Tank):
    def __init__(self):
        pass
class Bullet():
    def __init__(self):
        pass
    def move(self):
        pass
    def displaybullet(self):
        pass
class Explode():
    def __init__(self):
        pass
    def displayexplode(self):
        pass
class Wall():
    def __init__(self):
        pass
    def displaywall(self):
        pass
class Music():
    def __init__(self):
        pass
    def play(self):
        pass
a=MainGame()
a.startgame()
