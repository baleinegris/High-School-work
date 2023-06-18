# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 08:54:21 2023

@author: Oscar
"""
import pyxel
from random import randint

WIDTH = 300
HEIGHT = 250
TITLE = 'Space Invaders'

class Jeu():

    def __init__(self, sound = True):
        self.pause = False
        self.liste_tirs  = []
        self.liste_tirs_enemies = []
        self.liste_enemies = [] # les enemies sont de la forme [x, y, sens, masque, type, nv de vies]
        self.enemymask = 0
        self.vaisseau = [WIDTH//2-11,HEIGHT-HEIGHT//10-15]
        self.explosion = []
        self.rocket_explosions = []
        self.etoiles = []
        self.fire_mode = 1
        self.score = 0
        self.enemy_speed = 1
        self.misses = 0
        self.game_over = False
        self.level = 0
        self.scoreincrease = 1
        self.hitstreak = 0
        self.timer = 0
        self.speedtracker = 0
        self.lives = 3
        self.pos = 39
        self.boss = {}
        self.liste_homing_shots = [] # [[posx, posy], pente]
        self.pente = 0
        self.beam = False
        self.game_won = False
        self.cursor = ['play']
        self.shiptype = 'medium'
        self.meteors = []
        self.meteorframe = 0
        self.var = 0
        self.deets = []
        self.game_mode = "Endless"
        self.sound = sound
        f=open("spacehighscore.txt","r")
        self.highscore=int(f.readlines()[0])
        f.close()
        print(self.highscore)
        for y in range (HEIGHT):
            l = []
            for i in range (WIDTH):
                x = randint(0,75)
                if x == 1:
                    l.append(1)
                else:
                    l.append(0)
            self.etoiles.append(l)
        pyxel.init(WIDTH, HEIGHT, title = TITLE)
        pyxel.run(self.update,self.draw)
    
    
    def draw_highscore(self, location):
        pyxel.blt(location[0],location[1], 0, 2, 204, 29, 8)
        pyxel.blt(location[0]+26,location[1], 0, 5, 189, 36, 8)
        self.draw_score([location[0]+65,location[1]],self.highscore)

    def draw_score(self,location, num):
        n = 0
        for i in str(num):
            chiffre = int(i)
            x = location[0] + n*6
            y = location[1]
            bltlocationx = 6 + chiffre*6
            bltlocationy = 220
            pyxel.blt(x, y, 0, bltlocationx, bltlocationy, 5, 8)
            n+=1

    def creation_tir(self, location, typeshot):
        ''' location = liste avec coords x et y du tir'''
        self.liste_tirs.append([location, typeshot])
    
    def deplacement_tirs(self):
        if pyxel.frame_count % 1 == 0:
            for itir in range (len(self.liste_tirs)):
                if self.liste_tirs[itir][1] == 1:
                    if self.shiptype == 'medium':
                        self.liste_tirs[itir] = [[(self.liste_tirs[itir][0][0]),(self.liste_tirs[itir][0][1])-9],self.liste_tirs[itir][1]]
                    else:
                        self.liste_tirs[itir] = [[(self.liste_tirs[itir][0][0]),(self.liste_tirs[itir][0][1])-5],self.liste_tirs[itir][1]]
                if self.liste_tirs[itir][1] == 2:
                    self.liste_tirs[itir] = [[(self.liste_tirs[itir][0][0]),(self.liste_tirs[itir][0][1])-3],self.liste_tirs[itir][1]]
            for enemy in self.liste_enemies:
                for tir in self.liste_tirs:
                    if \
                        tir[0][0] >= enemy[0] \
                        and tir[0][0] <= enemy[0]+11 \
                        and tir[0][1] >= enemy[1] \
                        and tir[0][1] <= enemy[1] + 9\
                        and (enemy[3] == 1 or enemy[3] == 2):
                            self.hit(enemy,tir)
                    if \
                        tir[0][0] >= enemy[0] \
                        and tir[0][0] <= enemy[0]+22 \
                        and tir[0][1] >= enemy[1] \
                        and tir[0][1] <= enemy[1] + 11\
                        and (enemy[3] == 3):
                             self.hit(enemy,tir)
            for meteor in self.meteors:
                for tir in self.liste_tirs:
                    if \
                        tir[0][0] >= meteor[0][0] -2 \
                        and tir[0][0] <= meteor[0][0]+8 \
                        and tir[0][1] >= meteor[0][1]-8 \
                        and tir[0][1] <= meteor[0][1] + 6:
                            self.deets = [[meteor[0][0],meteor[0][1]],str((self.scoreincrease)*15)]
                            self.var = 1
                            self.meteors.remove(meteor)
                            self.explosion.append([meteor[0][0],meteor[0][1],0])
                            self.score+=(self.scoreincrease)*15
                            self.speedtracker += (self.scoreincrease)*15
                            self.liste_tirs.remove(tir)
            if self.level == 2:

                for tir in self.liste_tirs:
                    if tir[0][0] > self.boss['pos'][0] \
                        and tir[0][0] < self.boss['pos'][0] + 60 \
                        and tir[0][1] > self.boss['pos'][1] + 20 \
                        and tir[0][1] < self.boss['pos'][1] + 28:

                        if tir[1] == 1:
                            self.boss['health'] -= 1
                            self.explosion.append([tir[0][0],tir[0][1],0])

                        elif tir[1] == 2:
                            self.boss['health'] -= 5
                            self.rocket_explosions.append([[tir[0][0],tir[0][1]],0])
                        self.hitstreak += 1   
                        self.score += self.scoreincrease
                        self.liste_tirs.remove(tir)

        for enemy in self.liste_enemies:
            if enemy[4] <= 0:
                self.liste_enemies.remove(enemy)
                
        if self.liste_tirs != []:
            if self.liste_tirs[0][0][1] <= 0:
                self.liste_tirs.pop(0)
                self.hitstreak = 0
                self.scoreincrease = 1
                self.misses += 1
            
        if self.hitstreak >= 8 and self.hitstreak < 15:
            self.scoreincrease = 2
        if self.hitstreak >= 15:
            self.scoreincrease = 3

    def hit(self,enemy,tir):
        if tir[1] == 1:
            self.hitstreak += 1
            enemy[4] -= 1
            self.liste_tirs.remove(tir)
            self.explosion.append([enemy[0],enemy[1],0])
            self.score+=self.scoreincrease
            self.speedtracker += self.scoreincrease

        if tir[1] == 2:
            self.hitstreak += 1
            self.explosion.append([enemy[0],enemy[1],0])
            enemy[4] -= 1
            self.score += self.scoreincrease
            self.speedtracker += self.scoreincrease
            for enemyhit in self.liste_enemies:
                if enemyhit[0] >= tir[0][0] - 40 \
                    and enemyhit[0] <= tir[0][0] + 30\
                    and enemyhit[1] >= tir[0][1] - 40\
                    and enemyhit[1] <= tir[0][1] + 40:
                    enemyhit[4] -= 1
                    self.explosion.append([enemyhit[0],enemyhit[1],0])
                    self.score+= self.scoreincrease
                    self.speedtracker += self.scoreincrease
            self.liste_tirs.remove(tir)
            self.rocket_explosions.append([[tir[0][0], tir[0][1]],0])
            

    def creation_enemy(self, location, type_enemy, hp):
        ''' location = liste avec coords x et y de l'enemie '''
        self.liste_enemies.append([location[0],location[1],location[2], type_enemy,hp])

    def deplacement_enemies(self):
        if pyxel.frame_count % 3 == 0:
            for ienemy in range (len(self.liste_enemies)):
                #print (self.liste_enemies)
                if self.liste_enemies[ienemy][0] <= 0:
                    self.liste_enemies[ienemy][2] = 0
                    if self.liste_enemies[ienemy][3] != 4:
                        self.liste_enemies[ienemy][1] += 10
                    
                elif self.liste_enemies[ienemy][0] >= WIDTH:
                    self.liste_enemies[ienemy][2] = 1     
                    if self.liste_enemies[ienemy][3] != 4:
                        self.liste_enemies[ienemy][1] += 10  

                if self.liste_enemies[ienemy][1] >= HEIGHT:
                    self.game_over = True

                   
                if self.liste_enemies[ienemy][2] == 0:
                    self.liste_enemies[ienemy] = [self.liste_enemies[ienemy][0]+self.enemy_speed, self.liste_enemies[ienemy][1], self.liste_enemies[ienemy][2],self.liste_enemies[ienemy][3],self.liste_enemies[ienemy][4]]
                
                elif self.liste_enemies[ienemy][2] == 1:
                    self.liste_enemies[ienemy] = [self.liste_enemies[ienemy][0]-self.enemy_speed, self.liste_enemies[ienemy][1], self.liste_enemies[ienemy][2],self.liste_enemies[ienemy][3],self.liste_enemies[ienemy][4]]
    
    def deplacement_boss(self):
        if self.boss['attack'] != 'laser':        
            if pyxel.frame_count % 3 == 0:
                if self.boss['sens'] == 0:
                    self.boss['pos'][0] += 1
                elif self.boss['sens'] == 1:
                    self.boss['pos'][0] -= 1
                if self.boss['pos'][0] >= WIDTH - 70:
                    self.boss['sens'] = 1
                if self.boss['pos'][0] <= 0:
                    self.boss['sens'] = 0

                
    def lvl1_start(self):
        for y in range(20,60,10):
            for x in range (10,270,30):
                if y == 20 or y == 40:
                    self.creation_enemy([x,y,0],1,1)
                else:
                    self.creation_enemy([x,y, 1],1,1)

    def deplacement_tir_enemies(self):
        for tir in self.liste_tirs_enemies:
            tir[1] = tir[1] + 3
            if tir[0] >= self.vaisseau[0]+5 \
                and tir[0] <= self.vaisseau[0] + 18 \
                and tir[1] >= self.vaisseau[1] +8\
                and tir[1] <= self.vaisseau[1] + 15:
                self.liste_tirs_enemies.remove(tir)
                self.rocket_explosions.append([[tir[0], tir[1]],0])     
                self.lives -= 1
                self.explosion.append([WIDTH-35 + self.pos, 30,0])
                if self.lives == -1:
                    self.game_over = True
            
        for tir in self.liste_homing_shots:
            if tir[0][0] >= self.vaisseau[0]+5 \
                and tir[0][0] <= self.vaisseau[0] + 18 \
                and tir[0][1] >= self.vaisseau[1] +8\
                and tir[0][1] <= self.vaisseau[1] + 15:
                self.liste_homing_shots.remove(tir)
                self.rocket_explosions.append([[tir[0][0], tir[0][1]],0])     
                self.lives -= 1
                self.explosion.append([WIDTH-35 + self.pos, 30,0])
                if self.lives == -1:
                    self.game_over = True
                    
    def boss_start(self):
        self.liste_enemies = []
        self.boss = {'pos':[0,0],'health':100, 'sens':0, 'attack': 0, 'frame':0, 'cooldown': 0, 'rage': 1}

    def boss_attacks(self): 
        if self.boss['attack'] == 0:
            if self.boss['cooldown'] <= 0:
                attack_decide = randint(0,3)
                if attack_decide == 0:
                    self.boss['attack'] = 'laser'
                else:
                    self.boss['attack'] = 'homing shots'
            else:
                if self.boss['rage'] > 2:
                    self.boss['cooldown'] -= 2
                else:
                    self.boss['cooldown'] -= 1
        if self.boss['attack'] == 'laser':
            self.laser()
            
        if self.boss['attack'] == 'homing shots':
            self.homing_shots()
            
        for shot in self.liste_homing_shots:
            shot[0][1] += 2
            shot[0][0] += shot[1] 

        if pyxel.frame_count % 30 == 0 :
            self.liste_tirs_enemies.append([self.boss['pos'][0]+7,self.boss['pos'][1]+42])
            self.liste_tirs_enemies.append([self.boss['pos'][0]+54,self.boss['pos'][1]+42])
       
        if self.boss['health'] < 70 and self.boss['health'] > 50:
            self.boss['rage'] = 2
        if self.boss['health'] <= 50:
            self.boss['rage'] = 3
            
        if self.boss['rage'] > 1:
            if pyxel.frame_count % 500 == 0:
                for x in range (10,270,30):
                    self.creation_enemy([x,50,0],1,1)
        if self.boss['rage'] > 2:
            if pyxel.frame_count % 350 == 0:
                self.creation_enemy([0,10,1],3,3)
                self.creation_enemy([300,20,0],3,3)
        if self.boss['health'] <= 0:
            self.game_won = True

             
    def laser(self):
        if self.boss['frame'] < 35:
            self.boss['frame'] += 1
        elif self.boss['frame'] >= 35 and self.boss['frame'] < 65:
            self.beam = True
            laser = self.boss['pos'][0]+29
            if laser >= self.vaisseau[0]+5 \
                and laser + 5 <= self.vaisseau[0] + 18:  
                self.lives -= 1
                self.rocket_explosions.append([[self.vaisseau[0],self.vaisseau[1]],0])
                self.boss['attack'] = 0
                self.boss['frame'] = 0
                self.beam = False
                self.boss['cooldown'] = 150
                            
                if self.lives < 0:
                    self.game_over = True
            self.boss['frame'] += 1
        elif self.boss['frame'] >= 65:
            self.boss['attack'] = 0
            self.boss['frame'] = 0
            self.beam = False
            self.boss['cooldown'] = 150
                            
    def calcul_pente(self, pos1, pos2):
        x = pos2[0]-pos1[0]
        y = pos2[1]-pos1[1]
        if x == 0:
            return 0
        pente = round(x/y)
        if pente < 0:
            return pente - 1
        if pente > 0:
            return pente + 1
        if pente == 0:
            if x < 0:
                return pente - 1
            if x > 0:
                return pente - 1
        self.pente = pente
        return pente    
    
    def homing_shots(self):
        pente = self.calcul_pente([self.boss['pos'][0]+7,self.boss['pos'][1]+42],[self.vaisseau[0]+10, self.vaisseau[1]+10])
        self.liste_homing_shots.append([[self.boss['pos'][0]+7,self.boss['pos'][1]+42],pente])
        pente = self.calcul_pente([self.boss['pos'][0]+54,self.boss['pos'][1]+42],[self.vaisseau[0]+10, self.vaisseau[1]+10])
        self.liste_homing_shots.append([[self.boss['pos'][0]+54,self.boss['pos'][1]+42],pente])
        self.boss['attack'] = 0
        self.boss['frame'] = 0
        self.boss['cooldown'] = 30
    
    def reset(self):
        self.pause = False
        self.liste_tirs  = []
        self.liste_tirs_enemies = []
        self.liste_enemies = [] # les enemies sont de la forme [x, y, sens, masque, type, nv de vies]
        self.enemymask = 0
        self.vaisseau = [WIDTH//2-11,HEIGHT-HEIGHT//10-15]
        self.explosion = []
        self.rocket_explosions = []
        self.fire_mode = 1
        self.score = 0
        self.enemy_speed = 1
        self.misses = 0
        self.game_over = False
        self.level = 0
        self.scoreincrease = 1
        self.hitstreak = 0
        self.timer = 0
        self.speedtracker = 0
        self.lives = 3
        self.pos = 39
        self.boss = {}
        self.liste_homing_shots = [] # [[posx, posy], pente]
        self.pente = 0
        self.beam = False
        self.game_won = False
        self.cursor = ['play']
        self.meteors = []
        
    def meteor_spawn(self):
        var = 500
        y = randint(0,2)
        x = randint(0,1)
        lstx = [0,WIDTH]
        lsty = [10, 20, 30]
        if pyxel.frame_count % var == 0:
            if lstx[x] == WIDTH:
                self.meteors.append([[lstx[x],lsty[y],1],4, 1, y])
            else:
                self.meteors.append([[lstx[x],lsty[y],0],4, 1, y])
    
        if pyxel.frame_count % 3 == 0:
            for meteor in self.meteors:
                if meteor[0][2] == 1:
                    meteor[0][0] -= 7
                    meteor[0][1] += meteor[3]
                else:
                    meteor[0][0] += 7
                    meteor[0][1] += meteor[3]


    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        if pyxel.btnp(pyxel.KEY_P):
            self.reset()
        if self.game_won == True:
            if self.timer > 120:
                return
            x = randint(0,60)
            y = randint(20,25)
            if self.timer < 70:
                self.rocket_explosions.append([[self.boss['pos'][0] + x,self.boss['pos'][1]+y],0])
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()
            self.timer+=1
            return

        if self.level == 0:
            if pyxel.btnp(pyxel.KEY_DOWN):
                self.cursor = ['select']
            if pyxel.btnp(pyxel.KEY_UP):
                self.cursor = ['play']
            if pyxel.btnp(pyxel.KEY_SPACE) and self.cursor == ['play']:
                self.level = 'select_mode'
            if pyxel.btnp(pyxel.KEY_SPACE) and self.cursor == ['select']:
                self.level = 'select'
            return
        
        if self.level == 'select':
            if pyxel.btnp(pyxel.KEY_LEFT):
                if self.shiptype == 'medium':
                    self.shiptype = 'light'
                if self.shiptype == 'heavy':
                    self.shiptype = 'medium'

            if pyxel.btnp(pyxel.KEY_RIGHT):
                if self.shiptype == 'medium':
                    self.shiptype = 'heavy'
                if self.shiptype == 'light':
                    self.shiptype = 'medium'
                    
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.level = 0
            return
        
        if self.level == 'select_mode':
            if pyxel.btnp(pyxel.KEY_LEFT):
                self.cursor = ['campaign']

            if pyxel.btnp(pyxel.KEY_RIGHT):
                self.cursor = ['endless']
                
            if pyxel.btnp(pyxel.KEY_SPACE) and self.cursor == ['campaign']:
                self.game_mode = 'Campaign'
                self.level = 1
                
            if pyxel.btnp(pyxel.KEY_SPACE) and self.cursor == ['endless']:
                self.game_mode = 'Endless'
                self.level = 1
            return
        
        if self.level == 1:
            self.lvl1_start()
            self.level = 10
        
        if self.score >= 200:
            if self.game_mode == 'Campaign':
                if self.level!=2:
                    self.boss_start()
                    self.lives = 3
                    self.level = 2
        if self.level == 2:
            self.deplacement_boss()
            self.boss_attacks()
            
        if self.liste_enemies == [] and self.level == 10:
            self.lvl1_start()
            
        if self.game_over == True:
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()
            if pyxel.btnp(pyxel.KEY_R):
                self.liste_tirs  = []
                self.liste_tirs_enemies = []
                self.liste_enemies = [] 
                self.enemymask = 0
                self.vaisseau = [WIDTH//2-11,HEIGHT-HEIGHT//10-15]
                self.explosion = []
                self.rocket_explosions = []
                self.fire_mode = 1
                self.score = 0
                self.enemy_speed = 1
                self.misses = 0
                self.level = 1
                self.scoreincrease = 1
                self.hitstreak = 0
                self.timer = 0
                self.speedtracker = 0
                self.game_over = False
                self.lives = 3
                self.liste_homing_shots = [] # [[posx, posy], pente]
                self.beam = False
            self.timer += 1
            if self.timer >=35:
                if self.score > self.highscore:
                    f=open("spacehighscore.txt","w")
                    score = str(self.score)
                    f.write(score)
                    f.close()
                    self.highscore = self.score
                return
        
        # DEPLACEMENT DU VAISSEAU
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.vaisseau[0] += 4
        if pyxel.btn(pyxel.KEY_LEFT):
            self.vaisseau[0] -= 4

    
        # QUIT
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # TIRS
        if self.shiptype == 'medium':
            if pyxel.btnp(pyxel.KEY_UP):
                if self.fire_mode == 1:
                    if len(self.liste_tirs) <= 4:
                        self.creation_tir([self.vaisseau[0]+11,self.vaisseau[1]],1)
                elif self.fire_mode == 2:
                    if len(self.liste_tirs) == 0:
                        self.creation_tir([self.vaisseau[0]+11,self.vaisseau[1]],2)
        
        if self.shiptype == 'heavy':
            if pyxel.btn(pyxel.KEY_UP):
                if pyxel.frame_count%4 == 0:
                    if self.fire_mode == 1:
                        if len(self.liste_tirs) <= 10:
                            self.creation_tir([self.vaisseau[0]+11,self.vaisseau[1]],1)
        if self.shiptype == 'light':
            if pyxel.btnp(pyxel.KEY_UP):
                    if self.fire_mode == 1:
                        if len(self.liste_tirs) <= 2:
                            self.creation_tir([self.vaisseau[0]+11,self.vaisseau[1]],1)
                    if self.fire_mode == 2:
                        if len(self.liste_tirs) <= 2:
                            self.creation_tir([self.vaisseau[0]+11,self.vaisseau[1]],2)
        self.deplacement_tirs()
        
        #ENEMIES
        if self.level != 2:
            if pyxel.frame_count% (90// self.enemy_speed) == 0:
                if self.score < 50:
                    self.creation_enemy([0,10,1],1,1)
                elif self.score >= 50 and self.score<=100:
                    x = randint(0,10)
                    if x == 0:
                        self.creation_enemy([0,10,1],2,1)
                    else:
                        self.creation_enemy([0,10,1],1,1)
                elif self.score > 100:
                    x = randint(1,15)
                    if x == 15:
                        self.creation_enemy([0,10,1],3,3)
                    elif x >= 1 and x <=5:
                        self.creation_enemy([0,10,1],2,1)
                    else:
                        self.creation_enemy([0,10,1],1,1)
        self.meteor_spawn()
        self.deplacement_enemies()
        #POWERUPS
        if pyxel.btnp(pyxel.KEY_2):
            self.fire_mode = 2
        if pyxel.btnp(pyxel.KEY_1):
            self.fire_mode = 1

        #TIRS ENEMIES
        for enemy in self.liste_enemies:
            if enemy[3] == 2:
                if pyxel.frame_count % (120//self.enemy_speed) == 0 :
                    self.liste_tirs_enemies.append([enemy[0]+3,enemy[1]+6])
            if enemy[3] == 3:
                if pyxel.frame_count % (120//self.enemy_speed) == 0 :
                    self.liste_tirs_enemies.append([enemy[0]+3,enemy[1]+8])
                    self.liste_tirs_enemies.append([enemy[0]+10,enemy[1]+8])
                    self.liste_tirs_enemies.append([enemy[0]+17,enemy[1]+8])
        self.deplacement_tir_enemies()
        
        # SPEED
        if self.speedtracker >= 50:
            self.enemy_speed += 1
            self.speedtracker = 0
        if self.level == 1:
            if self.liste_enemies == []:
                self.lvl1_start()
                self.enemy_speed += 1
                self.score += 20
        
        
        
        
    def draw(self):
        
        if self.game_won == True:
            pyxel.cls(0)
            pyxel.text(130,135,'GAME WON', 10)
            if self.timer >120:
                return
            
        if self.game_over == True:
            if self.timer >= 35:
                pyxel.cls(0)
                pyxel.blt(WIDTH//2 - 25, HEIGHT//2 - 75, 0, 1, 158, 33, 21)
                self.draw_highscore([WIDTH//2, HEIGHT//2])
                pyxel.blt(WIDTH//2-80,HEIGHT//2, 0, 5, 189, 36, 8)
                self.draw_score([WIDTH//2 - 40, HEIGHT//2],self.score)
                return
        if pyxel.frame_count == 1 and self.sound == True:
            pyxel.playm(0,0,True)
            

        # BACKGROUND
        pyxel.cls(0)
        
        for row in range(len(self.etoiles)-1,0,-1):
            for pixel in range(len(self.etoiles[row])):
                if self.etoiles[row][pixel] == 1:
                    pyxel.rect(WIDTH-pixel,HEIGHT-row,1,1,7)
        if pyxel.frame_count %1 == 0:
            for i in range(1):
                self.etoiles.append(self.etoiles.pop(0))
    
        pyxel.load("space.pyxres")
        
        if self.level == 0:
            pyxel.blt(WIDTH//2 - 55, 20, 0, 1, 52, 107, 43)
            if self.shiptype == 'medium':
                pyxel.blt(WIDTH//2-11,HEIGHT-HEIGHT//10-15, 0, 8, 9, 23, 30,0)
            if self.shiptype == 'light':
                pyxel.blt(WIDTH//2-11,HEIGHT-HEIGHT//10-10, 0, 50, 95, 18, 30,0)
            if self.shiptype == 'heavy':
                pyxel.blt(WIDTH//2-15,HEIGHT-HEIGHT//10-10, 0, 81, 132, 30, 35,0)


            pyxel.rect(WIDTH//2 - 21, HEIGHT//2 - 11, 36, 10, 1)
            if self.cursor == ['play']:
                pyxel.rect(WIDTH//2 - 21, HEIGHT//2 - 11, 36, 10, 2)
            pyxel.blt(WIDTH//2 - 20, HEIGHT//2 - 10, 0, 102, 233, 35, 8, 0)
            
            
            pyxel.rect(WIDTH//2 - 23, HEIGHT//2+9, 40, 10, 1)
            if self.cursor == ['select']:
                pyxel.rect(WIDTH//2 - 23, HEIGHT//2+9, 40, 10, 2)
            pyxel.blt(WIDTH//2 - 22, HEIGHT//2+10, 0, 102, 209, 38, 8, 0)

            
            return
        
        if self.level == 'select':
            pyxel.blt(WIDTH//2-11,HEIGHT-HEIGHT//10-15, 0, 8, 9, 23, 30,0)
            pyxel.blt(WIDTH//2-50,HEIGHT-HEIGHT//10-10, 0, 50, 95, 18, 30,0)
            pyxel.blt(WIDTH//2+30,HEIGHT-HEIGHT//10-10, 0, 81, 132, 30, 35,0)
            
            if self.shiptype == 'medium':
                pyxel.blt(WIDTH//2-13,HEIGHT-HEIGHT//10-16, 0, 0, 249, 4, 4, 0)
                pyxel.blt(WIDTH//2+10,HEIGHT-HEIGHT//10-16, 0, 6, 249, 4, 4, 0)
                pyxel.blt(WIDTH//2+10,HEIGHT- 10, 0, 6, 244, 4, 4, 0)
                pyxel.blt(WIDTH//2+-13,HEIGHT- 10, 0, 0, 244, 4, 4, 0)
                
            if self.shiptype == 'light':
                pyxel.blt(WIDTH//2-55,HEIGHT-HEIGHT//10-16, 0, 0, 249, 4, 4, 0)
                pyxel.blt(WIDTH//2-32,HEIGHT-HEIGHT//10-16, 0, 6, 249, 4, 4, 0)
                pyxel.blt(WIDTH//2-32,HEIGHT- 14, 0, 6, 244, 4, 4, 0)
                pyxel.blt(WIDTH//2+-55,HEIGHT- 14, 0, 0, 244, 4, 4, 0)
                
            if self.shiptype == 'heavy':
                pyxel.blt(WIDTH//2+28,HEIGHT-HEIGHT//10-16, 0, 0, 249, 4, 4, 0)
                pyxel.blt(WIDTH//2+58,HEIGHT-HEIGHT//10-16, 0, 6, 249, 4, 4, 0)
                pyxel.blt(WIDTH//2+58,HEIGHT- 10, 0, 6, 244, 4, 4, 0)
                pyxel.blt(WIDTH//2+28,HEIGHT- 10, 0, 0, 244, 4, 4, 0)
            return
        
        if self.level == 'select_mode':
            pyxel.blt(WIDTH//2 - 55, 20, 0, 1, 52, 107, 43)

            pyxel.rect(WIDTH//2 - 76, HEIGHT//2-11, 63, 10, 1)
            pyxel.rect(WIDTH//2 +27, HEIGHT//2-11, 48, 10, 1)

            if self.cursor == ['endless']:
                pyxel.rect(WIDTH//2 +27, HEIGHT//2-11, 48, 10, 2)
                
            if self.cursor == ['campaign']:
                pyxel.rect(WIDTH//2 - 76, HEIGHT//2-11, 63, 10, 2)
                
            pyxel.blt(WIDTH//2+28,HEIGHT//2-10, 0, 144, 209, 50, 8, 0)
            pyxel.blt(WIDTH//2 - 75, HEIGHT//2-10, 0, 141, 233, 65, 8, 0)
            return

        #SCORE
        if self.scoreincrease == 2:
            pyxel.blt(230,10,0,2,125,10,7)
        if self.scoreincrease == 3:
            pyxel.blt(230,10,0,2,133,10,7)
        pyxel.text(250,10,f"SCORE: {self.score}",10)


        # VAISSEAU
        if self.shiptype == 'medium':
            pyxel.blt(self.vaisseau[0], self.vaisseau[1], 0, 8, 9, 23, 30,0)
        if self.shiptype == 'heavy':
            pyxel.blt(self.vaisseau[0], self.vaisseau[1], 0, 81, 132, 30, 35,0)
        if self.shiptype == 'light':
            pyxel.blt(self.vaisseau[0], self.vaisseau[1], 0, 50, 95, 18, 30,0)
        
        #VIES
        self.pos = 39
        for heart in range (self.lives):
            pyxel.blt(WIDTH-50+ self.pos, 30, 0, 99, 193, 11, 10, 0)
            self.pos -= 13
      
        # TIRS
        for tir in self.liste_tirs:
            if tir[1] == 1:
                pyxel.blt(tir[0][0],tir[0][1]-15, 0, 31, 13, 1, 10)
            elif tir[1] == 2:
                pyxel.blt(tir[0][0],tir[0][1]-15, 0, 35, 11, 5, 12,0)
        
        #ENEMIES
        for enemy in self.liste_enemies:
            if enemy[3] == 1:
                if self.enemymask == 0:
                    pyxel.blt(enemy[0],enemy[1], 0, 42, 10, 11, 9, 0)
                else:
                    pyxel.blt(enemy[0],enemy[1], 0, 55, 10, 11, 9, 0)
            if enemy[3] == 2:
                pyxel.blt(enemy[0],enemy[1], 0, 3, 96, 11, 9, 0)
                
            if enemy[3] == 3:
                pyxel.blt(enemy[0],enemy[1], 0, 18, 113, 22, 12, 0)
        
        for meteor in self.meteors:
            pyxel.blt(meteor[0][0],meteor[0][1], 0, 211, 213, 6, 6, 0)
        
        if self.level == 2:
            pyxel.blt(self.boss['pos'][0],self.boss['pos'][1], 0, 144, 136, 70, 50, 0)
                
        if pyxel.frame_count % 10 == 0:
            self.enemymask +=1
            if self.enemymask == 2:
                self.enemymask = 0

        if self.level == 2:
            pyxel.rect(45,245,200,4,0)
            pyxel.rect(45,245,self.boss['health']*2,2,8)
            pyxel.rect(44,245,1,2,10)
            pyxel.rect(245,245,1,2,10)
            pyxel.rect(45,244,200,1,10)
            pyxel.rect(45,247,200,1,10)
            pyxel.rect(45,245,1,2,10)
            pyxel.text(248,243,'Flagship',10)


        # TIRS ENEMIS
        for tir in self.liste_tirs_enemies:
            pyxel.blt(tir[0]-2,tir[1]-7,0, 4, 110, 5, 7, 0)
        for shot in self.liste_homing_shots:
            pyxel.blt(shot[0][0], shot[0][1], 0, 125, 133, 8, 8, 0)

        #EXPLOSIONS
        for explosions in self.explosion:
            if explosions[2] <= 2:
                pyxel.blt(explosions[0]+3,explosions[1]+3,0, 47, 31, 3, 4,0)
                explosions[2] += 1
            elif explosions[2] > 2 and explosions[2] <=4:
                pyxel.blt(explosions[0]+1,explosions[1]+1,0, 53, 29, 7, 6,0)
                explosions[2] += 1
            elif explosions[2] > 4:
                pyxel.blt(explosions[0],explosions[1],0, 64, 27, 9, 9,0)
                explosions[2] += 1
            if explosions[2] == 7:
                self.explosion.remove(explosions)

        if self.var == 1:
            if self.meteorframe < 20:
                pyxel.text(self.deets[0][0],self.deets[0][1],'+'+self.deets[1],10)
                self.meteorframe += 1
            else:
                self.var = 0

                self.meteorframe = 0       

        for rocket in self.rocket_explosions:
            if rocket[1] <= 2:
                pyxel.blt(rocket[0][0]+6,rocket[0][1]+6,0, 87, 37, 5, 5,0)
                rocket[1] += 1
            elif rocket[1] > 2 and rocket[1] <=4:
                pyxel.blt(rocket[0][0]+3,rocket[0][1]+3, 0, 108, 34, 10, 10,0)
                rocket[1] += 1
            elif rocket[1] > 4 and rocket[1] <=6:
                pyxel.blt(rocket[0][0]+1,rocket[0][1]+1, 0, 120, 32, 12, 12,0)
                rocket[1] += 1
            elif rocket[1] > 6 and rocket[1] <=8:
                pyxel.blt(rocket[0][0],rocket[0][1], 0, 134, 30, 16, 16,0)
                rocket[1] += 1
            elif rocket[1] > 8:
                pyxel.blt(rocket[0][0]-3,rocket[0][1]-3, 0, 164, 29, 24, 24,0)
                rocket[1] += 1
            if rocket[1] == 10:
                self.rocket_explosions.remove(rocket)
        ### TEMP

        if self.beam == True:
            pyxel.rect(self.boss['pos'][0]+29, self.boss['pos'][1] + 35, 5, HEIGHT, 8)
            pyxel.rect(self.boss['pos'][0]+30, self.boss['pos'][1] + 34, 3, HEIGHT, 2)
            #laser = self.boss['pos'][0]+29
            #pyxel.rect(self.vaisseau[0]+5, self.vaisseau[1]+8, 13, 7, 2)        
            #pyxel.rect(laser, self.boss['pos'][1], 5, 100, 6)
Jeu(False)