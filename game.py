import pygame as pg
import sys,time
from bird import Bird
from pipe import Pipe
pg.init()

class Game:
    def __init__(self):
        # setting window config
        self.width=432
        self.height=600
        self.scale_factor=1.5
        self.win=pg.display.set_mode((self.width,self.height))
        self.clock=pg.time.Clock()
        self.move_speed=250
        self.start_monitoring=False
        self.score=0
        self.font=pg.font.Font("gallery/arial.ttf",24)
        self.res_font=pg.font.Font("gallery/arial.ttf",32)
        self.name_font=pg.font.Font("gallery/arial.ttf",18)
        self.sign_font=pg.font.Font("gallery/Jalliya.otf",40)

        self.score_text=self.font.render("Score: 0",True,(0,0,0))
        self.score_text_rect=self.score_text.get_rect(center=(50,40))

        self.restart_text=self.res_font.render("Restart",True,(255,0,26))
        self.restart_text_rect=self.restart_text.get_rect(center=(200,525))

        self.founder_name=self.name_font.render("Make by= Mr. Manvendra singh",True,(255,119,0))
        self.founder_name_rect=self.founder_name.get_rect(center=(135,11))

        self.founder_signature=self.sign_font.render("Manvendra singh",True,(0,0,0))
        self.founder_signature_rect=self.founder_signature.get_rect(center=(355,510))

        self.bird=Bird(self.scale_factor)
        self.is_game_start=False
        self.start_game=True
        self.pipes=[]
        self.pipe_generate_counter=71
        self.setUpBgANDGround()
        
        
        self.gameLoop()


    def gameLoop(self):
        last_time=time.time()
        while True:
            # calculating delta time
            new_time=time.time()
            dt=new_time-last_time
            last_time=new_time

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type==pg.KEYDOWN and self.start_game:
                    if event.key==pg.K_RETURN:
                        self.is_game_start=True
                        self.bird.update_on=True
                    if event.key==pg.K_SPACE and self.is_game_start:
                        self.bird.flap(dt)
                if event.type==pg.MOUSEBUTTONDOWN:
                    if self.restart_text_rect.collidepoint(pg.mouse.get_pos()):
                        self.restartGame()
            
            self.updateEverything(dt)
            self.checkCollisions()
            self.checkScore()
            self.drawEverything()
            pg.display.update()
            self.clock.tick(60)

    def restartGame(self):
        self.score=0
        self.score_text=self.font.render("Score: 0",True,(0,0,0))
        self.is_game_start=False
        self.start_game=True
        self.bird.resetPosition()
        self.pipes.clear()
        self.pipe_generate_counter=71
        self.bird.update_on=False

    def checkScore(self):
        if len(self.pipes)>0:
            if(self.bird.rect.left>self.pipes[0].rect_down.left and
            self.bird.rect.right<self.pipes[0].rect_down.right and not self.start_monitoring):
               self.start_monitoring=True
            if self.bird.rect.left>self.pipes[0].rect_down.right and self.start_monitoring:
                self.start_monitoring=False
                self.score+=1
                self.score_text=self.font.render(f"Score: {self.score}",True,(0,0,0))

    def checkCollisions(self):
        if len(self.pipes):
           if self.bird.rect.bottom>450:
            self.bird.update_on=False
            self.is_game_start=False
            self.start_game=False
           if (self.bird.rect.colliderect(self.pipes[0].rect_down) or
           self.bird.rect.colliderect(self.pipes[0].rect_up)):
               self.is_game_start=False
               self.start_game=False
            

    def updateEverything(self,dt):
        if self.is_game_start:
            # moving the ground
            self.ground1_rect.x-=int(self.move_speed*dt)
            self.ground2_rect.x-=int(self.move_speed*dt)

            if self.ground1_rect.right<0:
                 self.ground1_rect.x=self.ground2_rect.right
            if self.ground2_rect.right<0:
                 self.ground2_rect.x=self.ground1_rect.right
            
            # generating the pipes
            if self.pipe_generate_counter>70:
                self.pipes.append(Pipe(self.scale_factor,self.move_speed))
                self.pipe_generate_counter=0
                
            self.pipe_generate_counter+=1
            
            # moving the pipe
            for pipe in self.pipes:
                pipe.update(dt)
            
            # removing pipes if out of screen
            if len(self.pipes)!=0:
                if self.pipes[0].rect_up.right<0:
                    self.pipes.pop(0)
                    
            # moving the bird
        self.bird.update(dt)

    def drawEverything(self):
        self.win.blit(self.bg_img,(0,-400))
        for pipe in self.pipes:
            pipe.drawPipe(self.win)
        self.win.blit(self.ground1_img,self.ground1_rect)
        self.win.blit(self.ground2_img,self.ground2_rect)
        self.win.blit(self.bird.image,self.bird.rect)
        self.win.blit(self.score_text,self.score_text_rect)
        self.win.blit(self.founder_name,self.founder_name_rect)
        self.win.blit(self.founder_signature,self.founder_signature_rect)
        if not self.start_game:
            self.win.blit(self.restart_text,self.restart_text_rect)

    def setUpBgANDGround(self):
        # loading bg & ground imgage
        self.bg_img=pg.transform.scale_by(pg.image.load("gallery/game img/background.png").convert(),self.scale_factor)
        self.ground1_img=pg.transform.scale_by(pg.image.load("gallery/game img/groundway.png").convert(),self.scale_factor)
        self.ground2_img=pg.transform.scale_by(pg.image.load("gallery/game img/groundway.png").convert(),self.scale_factor)

        self.ground1_rect=self.ground1_img.get_rect()
        self.ground2_rect=self.ground1_img.get_rect()

        self.ground1_rect.x=0
        self.ground2_rect.x=self.ground1_rect.right
        self.ground1_rect.y=450
        self.ground2_rect.y=450


game = Game()
                    
