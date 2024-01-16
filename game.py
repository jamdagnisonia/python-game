import pygame as pg
import time
import sys                      # used for exit
from bird import Bird
from pipe import Pipe
pg.init()

# create a class
class Game:
    # create a constructor
    def __init__(self):
        # setting window configrations
        self.width =600
        self.height =768
        self.scale_factor = 1.5                     # for showing the image properly becoz our image size is less than our window size
        self.win = pg.display.set_mode((self.width, self.height))      # pass width and height as a tuple
        self.clock = pg.time.Clock()
        self.is_enter_press = False
        self.move_speed = 250
        self.setupBackgroundAndGround()
        self.bird = Bird(self.scale_factor)          # MAKE FROM Bird class
        self.pipes =[]
        self.pipe_genrate_counter = 71
        
        self.score = 0
        self.start_monitring =False   # used in check score monitring
        self.font = pg.font.Font("assets/font.ttf",24)
        self.score_text = self.font.render("score: 0 ",True,(255,0,0))
        self.score_text_rect = self.score_text.get_rect(center= (100, 30))
        self.restart_text = self.font.render("Restart ",True,(255,0,0))
        self.restart_text_rect = self.restart_text.get_rect(center= (300, 700))
        self.is_game_started = True     # tell game have started
        self.gameLoop()               # if we comment it window close instuntly
    # create a game loop    
    def gameLoop(self):
        last_time = time.time()
        while True: 
            # calculating delta time
            new_time = time.time()
            dt = new_time - last_time
            last_time = new_time

            for event in pg.event.get():      # pg.event.get() gives a list type object
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()                # used for exit from the loop -> means when we click on x button game exit
                if event.type == pg.KEYDOWN and self.is_game_started:
                    if event.key == pg.K_RETURN:
                       self.is_enter_press = True
                       self.bird.update_on = True
                    if event.key == pg.K_SPACE:
                        self.bird.flap(dt) 
                # to click on restart game will restart
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.restart_text_rect.collidepoint(pg.mouse.get_pos()):     # colidepoint() -> we can check is point collide or not                  
                        self.restart_game() 
            self.updateEveryThing(dt)
            self.checkCollision()
            self.check_score()
            self.drowEveryThing()
            
            pg.display.update()
            self.clock.tick(60)              # run by 60 frame per second for hendle CPU processing 

    # restart game
    def restart_game(self):
        self.score = 0 
        self.score_text = self.font.render("score: 0 ",True,(255,0,0))
        self.is_enter_press = False
        self.is_game_started = True
        self.bird.resetPosition()
        self.pipes.clear()     #all pipes are clear
        self.pipe_genrate_counter =71
        self.bird.update_on = False              
    # check score
    def check_score(self):
        if len(self.pipes)> 0:
            if (self.bird.img_rect.left> self.pipes[0].rect_down.left and
            self.bird.img_rect.right< self.pipes[0].rect_down.right and not self.start_monitring):
                self.start_monitring = True
            if self.bird.img_rect.left> self.pipes[0].rect_down.right and self.start_monitring:
                    self.start_monitring =False
                    self.score += 1
                    self.score_text = self.font.render(f"score: {self.score}",True,(255,0,0)) 

                        
    # check collision
    def checkCollision(self):
        if len(self.pipes):
            # stop bird when it will hit bottom ground
            if self.bird.img_rect.bottom >568:
                self.bird.update_on =False
                self.is_enter_press =False
                self.is_game_started =False
            # if bird collide with pipes   
            if (self.bird.img_rect.colliderect(self.pipes[0].rect_down) or
                self.bird.img_rect.colliderect(self.pipes[0].rect_up)):
                    self.is_enter_press=False
                    self.is_game_started =False
                      

                     
    def updateEveryThing(self,dt):
        if self.is_enter_press:
            # moving ground
            self.ground1_rectangle.x -= int(self.move_speed*dt)
            self.ground2_rectangle.x -= int(self.move_speed*dt)
            if self.ground1_rectangle.right<0:
                self.ground1_rectangle.x = self.ground2_rectangle.right
            if self.ground2_rectangle.right<0:
                self.ground2_rectangle.x = self.ground1_rectangle.right
            # genrating pipes    
            if self.pipe_genrate_counter>70:
                self.pipes.append(Pipe(self.scale_factor, self.move_speed))
                self.pipe_genrate_counter =0
                # print("pipe created")
            self.pipe_genrate_counter += 1
            # moving pipes
            for pipe in self.pipes: 
                pipe.update(dt) 
            # delete the extra pipes
            #removing pipes if out of screen
            if len(self.pipes)!=0:
                if self.pipes[0].rect_up.right<0:
                    self.pipes.pop(0)
                    # print("pipe removed")               
            # moving the bird 
            # call bird update method from bird module 
        self.bird.update(dt)      
                 
    def drowEveryThing(self): 
        # show background image
        self.win.blit(self.bg_image, (0,-300))
        # drow the pipes back of ground
        for pipe in self.pipes:
            pipe.drowPipe(self.win)
        self.win.blit(self.ground1_image, self.ground1_rectangle)
        self.win.blit(self.ground2_image, self.ground2_rectangle) 
        self.win.blit(self.bird.image, self.bird.img_rect)  
        self.win.blit(self.score_text, self.score_text_rect)
        if not self.is_game_started:
            self.win.blit(self.restart_text, self.restart_text_rect)   
    def setupBackgroundAndGround(self):
        # load background image
        self.bg_image = pg.transform.scale_by(pg.image.load("assets/bg.png").convert(),self.scale_factor)
        # load ground image
        self.ground1_image = pg.transform.scale_by(pg.image.load("assets/ground.png").convert(),self.scale_factor)
        self.ground2_image = pg.transform.scale_by(pg.image.load("assets/ground.png").convert(),self.scale_factor)

        # create rectangle for both ground images
        self.ground1_rectangle = self.ground1_image.get_rect()
        self.ground2_rectangle = self.ground2_image.get_rect()
        self.ground1_rectangle.x = 0
        self.ground2_rectangle.x = self.ground1_rectangle.right
        self.ground1_rectangle.y = 568
        self.ground2_rectangle.y =568




game = Game()


