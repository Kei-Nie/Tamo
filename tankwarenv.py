import pygame
import random
import numpy as np

class MainGame():
    window= None
    screenheight=600
    screenwidth=800
    color=pygame.Color(0,0,0)
    fontcolor=pygame.Color(255,0,0)
    tankp1=None
    enemytank_list=[]
    enemytank_count=10
    Bullet_list=[]
    enemybullet_list=[]
    explode_list=[]
    wall_list=[]
    sensor_b=None
    sensor_s=None
    sensor_r=None
    sensor_l=None
    def __init__(self):
        pygame.display.init()
        MainGame.window=pygame.display.set_mode([MainGame.screenwidth,MainGame.screenheight])
        self.reset()
        music = Music("tankimages/music.mp3")
        #music.play(-1)
        pygame.display.set_caption("TAMO V1.0")


#divide between init and play step
    def play_step(self,action):
        self.frame_iteration+=1
        self.getevent()
        MainGame.window.fill(MainGame.color)
        MainGame.window.blit(self.gettextsurface("the remaining tank number is %d"%len(MainGame.enemytank_list)),(5,5))
        self.blitwalls()
        self.blitmytank()
        self.blitsensors()
        MainGame.tankp1.move(action)
        self.blitenemytank()
        self.score = 10 - len(MainGame.enemytank_list)
        reward=0
        game_over=False
        self.blitbullet()
        self.blitenemybullet()
        self.displayexplodes()
        if len(MainGame.enemytank_list)==0:
            game_over=True
        for ebullet in MainGame.enemybullet_list:
            if ebullet.hitmytank():
                game_over=True
                reward=-10
                return reward,game_over,self.score
        for bullet in MainGame.Bullet_list:
            if bullet.hitenemytank():
                reward=10
        pygame.display.update()
        return reward,game_over,self.score





    def reset(self):
        for etank in MainGame.enemytank_list:
            etank.live = False
        for walls in MainGame.wall_list:
            walls.live = False
        for enemybullet in MainGame.enemybullet_list:
            enemybullet.live= False
        self.create_mytank()
        self.create_enemytank()
        self.create_walls()
        self.score=0
        self.frame_iteration = 0
        self.create_sensors()




    def create_enemytank(self):
        top=100
        for i in range(MainGame.enemytank_count):
            speed = random.randint(3, 6)
            left = random.randint(100, 700)
            etank=EnemyTank(left,top,speed)
            MainGame.enemytank_list.append(etank)
    def create_walls(self):
        for i in range(1,7):
            wall=Wall(120*i,300)
            MainGame.wall_list.append(wall)
    def create_sensors(self):
        MainGame.sensor_b=Sensor_back()
        MainGame.sensor_s=Sensor_straight()
        MainGame.sensor_r=Sensor_right()
        MainGame.sensor_l=Sensor_left()

    def blitwalls(self):
        for wall in MainGame.wall_list:
            if wall.live:
                wall.displaywall()
            else:
                MainGame.wall_list.remove(wall)
    def blitmytank(self):
        if MainGame.tankp1 and MainGame.tankp1.live:
            MainGame.tankp1.displaytank()
            MainGame.tankp1.hitwalls()
            MainGame.tankp1.hitenemytank()
            bullet=Bullet(MainGame.tankp1)
            if len(MainGame.Bullet_list) < 5:
                MainGame.Bullet_list.append(bullet)
        else:
            del MainGame.tankp1
            MainGame.tankp1=None
    def create_mytank(self):
        MainGame.tankp1 = Mytank(600, 200)
        #music=Music('tankimages/music.mp3')
        #music.play()

    def blitenemytank(self):
        for etank in MainGame.enemytank_list:
            if etank.live:
                etank.displaytank()
                etank.randmove()
                etank.hitwalls()
                etank.hitmytank()
                ebullet=etank.shot()
                if ebullet and len(MainGame.enemybullet_list)<5*self.enemytank_count:
                    MainGame.enemybullet_list.append(ebullet)
            else:
                MainGame.enemytank_list.remove(etank)
    def blitbullet(self):
        for bullet in MainGame.Bullet_list:
            if bullet.live:
                bullet.displaybullet()
                bullet.bulletmove()
                bullet.hitenemytank()
                bullet.hitwalls()
            else:
                MainGame.Bullet_list.remove(bullet)
    def blitenemybullet(self):
        for ebullet in MainGame.enemybullet_list:
            if ebullet.live:
                ebullet.displaybullet()
                ebullet.bulletmove()
                ebullet.hitwalls()
                #ebullet.hitsensors()
                if MainGame.tankp1 and MainGame.tankp1.live:
                    ebullet.hitmytank()
            else:
                MainGame.enemybullet_list.remove(ebullet)
    def displayexplodes(self):
        for explode in MainGame.explode_list:
            if explode.live:
                explode.displayexplode()
            else:
                MainGame.explode_list.remove(explode)

    def blitsensors(self):
        MainGame.sensor_b.displaysensor()
        MainGame.sensor_l.displaysensor()
        MainGame.sensor_r.displaysensor()
        MainGame.sensor_s.displaysensor()

    def is_collision_stright(self):
        if len(MainGame.enemybullet_list) >= 1:
            for enemy_bullet in MainGame.enemybullet_list:
                if pygame.sprite.collide_rect(MainGame.sensor_s, enemy_bullet):
                    return True
        return False

    def is_collision_back(self):
        if len(MainGame.enemybullet_list) >= 1:
            for enemy_bullet in MainGame.enemybullet_list:
                if pygame.sprite.collide_rect(MainGame.sensor_b, enemy_bullet):
                    return True
        return False

    def is_collision_left(self):
        if len(MainGame.enemybullet_list)>=1:
            for enemy_bullet in MainGame.enemybullet_list:
                if pygame.sprite.collide_rect(MainGame.sensor_l, enemy_bullet):
                    return True
        return False

    def is_collision_right(self):
        if len(MainGame.enemybullet_list) >= 1:
            for enemy_bullet in MainGame.enemybullet_list:
                if pygame.sprite.collide_rect(MainGame.sensor_r, enemy_bullet):
                    return True
        return False

    def determine_enemy_up(self):
        if len(MainGame.enemytank_list) >= 1:
            for etank in MainGame.enemytank_list:
                if etank.rect.top>MainGame.tankp1.rect.top:
                    return True
        return False

    def determine_enemy_down(self):
        if len(MainGame.enemytank_list) >= 1:
            for etank in MainGame.enemytank_list:
                if etank.rect.top<MainGame.tankp1.rect.top:
                    return True
        return False

    def determine_enemy_left(self):
        if len(MainGame.enemytank_list)>=1:
            for etank in MainGame.enemytank_list:
                if etank.rect.left<MainGame.tankp1.rect.left:
                    return True
        return False

    def determine_enemy_right(self):
        if len(MainGame.enemytank_list) >= 1:
            for etank in MainGame.enemytank_list:
                if etank.rect.left>MainGame.tankp1.rect.left:
                    return True
        return False
    def endgame(self):
        print("thanks for playing")
        exit()
    def getevent(self):
        eventlist = pygame.event.get()
        for event in eventlist:
            if event.type == pygame.QUIT:
                self.endgame()

    def gettextsurface(self,text):
        pygame.font.init()
        font=pygame.font.SysFont("laoui",18)
        textsurface=font.render(text,True,MainGame.fontcolor)
        return textsurface
class Baseitem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__()




class Tank(Baseitem):
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
        self.speed=5
        self.stop=True
        self.live=True
        self.oldleft=self.rect.left
        self.oldtop=self.rect.top


    def move(self,action):
        self.oldleft = self.rect.left
        self.oldtop = self.rect.top
        clock_wise = ["R", "D", "L", "U"]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn r -> d -> l -> u
        elif np.array_equal(action, [0, 0, 1, 0]):
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn r -> u -> l -> d
        elif np.array_equal(action, [0, 0, 0, 1]):
            next_idx = (idx + 2) % 4
            new_dir = clock_wise[next_idx]

        self.direction = new_dir
        if self.direction=="L":
            if self.rect.left>0:
                self.rect.left-=self.speed
        elif self.direction=="R":
            if self.rect.left+self.rect.height<MainGame.screenwidth:
                self.rect.left+=self.speed
        elif self.direction=="U":
            if self.rect.top>0:
                self.rect.top-=self.speed
        elif self.direction=="D":
            if self.rect.top+self.rect.height<MainGame.screenheight:
                self.rect.top+=self.speed
    def stay(self):
        self.rect.left=self.oldleft
        self.rect.top=self.oldtop
    def hitwalls(self):
        for wall in MainGame.wall_list:
            if pygame.sprite.collide_rect(wall,self):
                self.stay()


    def shot(self):
        num=random.randint(1,100)
        if num>=10:
            return Bullet(self)
    def displaytank(self):
        self.image = self.images[self.direction]
        MainGame.window.blit(self.image,self.rect)

class Mytank(Tank):
    def __init__(self,left,top):
        super(Mytank,self).__init__(left,top)
    def hitenemytank(self):
        for etank in MainGame.enemytank_list:
            if pygame.sprite.collide_rect(etank,self):
                self.stay()


class Sensor_straight():
    def __init__(self):
        self.direction=MainGame.tankp1.direction
        self.sensorimages={
            "U":pygame.image.load('tankimages/36x216.png'),
            "D":pygame.image.load('tankimages/36x216.png'),
            "L":pygame.image.load('tankimages/210x35.png'),
            "R":pygame.image.load('tankimages/210x35.png')
        }
        self.sensorimage = self.sensorimages[self.direction]
        self.rect = self.sensorimage.get_rect()

    def displaysensor(self):
        if self.direction=="L":
            self.rect.left=MainGame.tankp1.rect.left-210
            self.rect.top=MainGame.tankp1.rect.top
        elif self.direction=="R":
            self.rect.left = MainGame.tankp1.rect.left + 36
            self.rect.top = MainGame.tankp1.rect.top
        elif self.direction=="U":
            self.rect.left = MainGame.tankp1.rect.left
            self.rect.top = MainGame.tankp1.rect.top-216
        else:
            self.rect.left = MainGame.tankp1.rect.left
            self.rect.top = MainGame.tankp1.rect.top +38
        MainGame.window.blit(self.sensorimage, self.rect)




class Sensor_back():
    def __init__(self):
        self.direction = MainGame.tankp1.direction
        self.sensorimages = {
            "U": pygame.image.load('tankimages/36x216.png'),
            "D": pygame.image.load('tankimages/36x216.png'),
            "L": pygame.image.load('tankimages/210x35.png'),
            "R": pygame.image.load('tankimages/210x35.png')
        }
        self.sensorimage = self.sensorimages[self.direction]
        self.rect = self.sensorimage.get_rect()


    def displaysensor(self):
        if self.direction=="L":
            self.rect.left=MainGame.tankp1.rect.left+36
            self.rect.top=MainGame.tankp1.rect.top
        elif self.direction=="R":
            self.rect.left = MainGame.tankp1.rect.left - 210
            self.rect.top = MainGame.tankp1.rect.top
        elif self.direction=="U":
            self.rect.left = MainGame.tankp1.rect.left
            self.rect.top = MainGame.tankp1.rect.top+38
        else:
            self.rect.left = MainGame.tankp1.rect.left
            self.rect.top = MainGame.tankp1.rect.top -216
        MainGame.window.blit(self.sensorimage, self.rect)

class Sensor_left():
    def __init__(self):
        self.direction = MainGame.tankp1.direction
        self.sensorimages = {
            "U": pygame.image.load('tankimages/228x38.png'),
            "D": pygame.image.load('tankimages/228x38.png'),
            "L": pygame.image.load('tankimages/36x216.png'),
            "R": pygame.image.load('tankimages/36x216.png')
        }
        self.sensorimage = self.sensorimages[self.direction]
        self.rect = self.sensorimage.get_rect()


    def displaysensor(self):
        if self.direction == "L":
            self.rect.left = MainGame.tankp1.rect.left
            self.rect.top = MainGame.tankp1.rect.top - 35
        elif self.direction == "R":
            self.rect.left = MainGame.tankp1.rect.left
            self.rect.top = MainGame.tankp1.rect.top + 216
        elif self.direction == "U":
            self.rect.left = MainGame.tankp1.rect.left + 228
            self.rect.top = MainGame.tankp1.rect.top
        else:
            self.rect.left = MainGame.tankp1.rect.left - 36
            self.rect.top = MainGame.tankp1.rect.top
            MainGame.window.blit(self.sensorimage, self.rect)

class Sensor_right():
    def __init__(self):
        self.direction = MainGame.tankp1.direction
        self.sensorimages = {
            "U": pygame.image.load('tankimages/228x38.png'),
            "D": pygame.image.load('tankimages/228x38.png'),
            "L": pygame.image.load('tankimages/36x216.png'),
            "R": pygame.image.load('tankimages/36x216.png')
        }
        self.sensorimage = self.sensorimages[self.direction]
        self.rect = self.sensorimage.get_rect()

    def displaysensor(self):
        if self.direction == "L":
            self.rect.left = MainGame.tankp1.rect.left
            self.rect.top = MainGame.tankp1.rect.top + 216
        elif self.direction == "R":
            self.rect.left = MainGame.tankp1.rect.left
            self.rect.top = MainGame.tankp1.rect.top - 35
        elif self.direction == "U":
            self.rect.left = MainGame.tankp1.rect.left - 36
            self.rect.top = MainGame.tankp1.rect.top
        else:
            self.rect.left = MainGame.tankp1.rect.left + 228
            self.rect.top = MainGame.tankp1.rect.top
            MainGame.window.blit(self.sensorimage, self.rect)




class EnemyTank(Tank):
    def __init__(self,left,top,speed):
        self.images = {
            "U": pygame.image.load('tankimages/enemytankup.jpg'),
            "D": pygame.image.load('tankimages/enemytankdown.jpg'),
            "L": pygame.image.load('tankimages/enemytankleft.jpg'),
            "R": pygame.image.load('tankimages/enemytankright.jpg')
        }
        self.direction = self.randirection()
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = speed
        self.stop = True
        self.step=20
        self.live=True
    def randirection(self):
        num=random.randint(1,4)
        if num==1:
            return"U"
        elif num==2:
            return"D"
        elif num==3:
            return"L"
        elif num==4:
            return"R"
    def randmove(self):
        if self.step <=0:
            self.direction=self.randirection()
            self.step=20
        else:
            self.move()
            self.step-=1
    def move(self):
        self.oldleft = self.rect.left
        self.oldtop = self.rect.top
        if self.direction=="L":
            if self.rect.left>0:
                self.rect.left-=self.speed
        elif self.direction=="R":
            if self.rect.left+self.rect.height<MainGame.screenwidth:
                self.rect.left+=self.speed
        elif self.direction=="U":
            if self.rect.top>0:
                self.rect.top-=self.speed
        elif self.direction=="D":
            if self.rect.top+self.rect.height<MainGame.screenheight:
                self.rect.top+=self.speed
    def shot(self):
        num=random.randint(1,100)
        if num <=10:
            return Bullet(self)
    def hitmytank(self):
        if MainGame.tankp1 and MainGame.tankp1.live:
            if pygame.sprite.collide_rect(self,MainGame.tankp1):
                self.stay()

class Bullet(Baseitem):
    def __init__(self,tank):
        self.image=pygame.image.load("tankimages/bullet.jpg")
        self.direction=tank.direction
        self.rect=self.image.get_rect()
        self.speed=15
        if self.direction=="U":
            self.rect.left=tank.rect.left+tank.rect.width/2-self.rect.width/2
            self.rect.top=tank.rect.top-self.rect.height
        elif self.direction=="D":
            self.rect.left = tank.rect.left + tank.rect.width / 2  -self.rect.width/2
            self.rect.top=tank.rect.top + tank.rect.height

        elif self.direction=="L":
            self.rect.left=tank.rect.left-self.rect.width
            self.rect.top = tank.rect.top + tank.rect.width / 2  -self.rect.width/2

        elif self.direction=="R":
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        self.live=True

    def bulletmove(self):
        if self.direction== "U":
           if self.rect.top>0:
               self.rect.top-=self.speed
           else:
               self.live=False
        elif self.direction=="D":
            if self.rect.top<=MainGame.screenheight-self.rect.height:
                self.rect.top+=self.speed
            else:
                self.live = False

        elif self.direction=="L":
            if self.rect.left>0:
                self.rect.left-=self.speed
            else:
                self.live = False
        elif self.direction=="R":
            if self.rect.left<=MainGame.screenwidth-self.rect.width:
                self.rect.left+=self.speed
            else:
                self.live = False
    def displaybullet(self):
        MainGame.window.blit(self.image,self.rect)
    def hitenemytank(self):
        for etank in MainGame.enemytank_list:
            if pygame.sprite.collide_rect(etank,self):
                explode=Explode(etank)
                MainGame.explode_list.append(explode)
                self.live=False
                etank.live=False
                return True
    def hitmytank(self):
        if pygame.sprite.collide_rect(MainGame.tankp1, self):
            explode=Explode(MainGame.tankp1)
            MainGame.explode_list.append(explode)
            self.live=False
            MainGame.tankp1.live=False
            return True
    def hitwalls(self):
        for wall in MainGame.wall_list:
            if pygame.sprite.collide_rect(wall,self):
                self.live=False
                wall.hp-=1
                if wall.hp<=0:
                    wall.live=False
    #def hitsensors(self):
        #if pygame.sprite.collide_rect(MainGame.sensor_s,self):
            #explode = Explode(MainGame.sensor_s)
            #MainGame.explode_list.append(explode)
        #if pygame.sprite.collide_rect(MainGame.sensor_b,self):
            #explode = Explode(MainGame.sensor_b)
            #MainGame.explode_list.append(explode)
        #if pygame.sprite.collide_rect(MainGame.sensor_l,self):
            #explode = Explode(MainGame.sensor_l)
            #MainGame.explode_list.append(explode)
        #if pygame.sprite.collide_rect(MainGame.sensor_r,self):
            #explode = Explode(MainGame.sensor_r)
            #MainGame.explode_list.append(explode)

class Explode():
    def __init__(self,tank):
        self.rect=tank.rect
        self.step=0
        self.images=[                   pygame.image.load('tankimages/blast0.jpg'),
                                        pygame.image.load('tankimages/blast1.jpg'),
                                        pygame.image.load('tankimages/blast2.jpg'),
                                        pygame.image.load('tankimages/blast3.jpg'),
                                        pygame.image.load('tankimages/blast4.jpg')
                                        ]
        self.image=self.images[self.step]
        self.live=True
    def displayexplode(self):
        if self.step<len(self.images):
            MainGame.window.blit(self.image,self.rect)
            self.image=self.images[self.step]
            self.step+=1
        else:
            self.live=False
            self.step=0
class Wall():
    def __init__(self,left,top):
        self.image=pygame.image.load("tankimages/REDAIWALL.png")
        self.rect=self.image.get_rect()
        self.rect.left=left
        self.rect.top=top
        self.live=True
        self.hp=50
    def displaywall(self):
        MainGame.window.blit(self.image,self.rect)
class Music():
    def __init__(self,filename):
        pygame.mixer.init()
        self.filename=filename
        pygame.mixer.music.load(self.filename)
    def play(self,loops):
        pygame.mixer.music.play(loops)


