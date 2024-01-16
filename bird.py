import pygame as pg


class Bird(pg.sprite.Sprite):                   # inherit from sprite module in sprite class
    def __init__(self, scale_factor):
        super(Bird, self).__init__()              # constructor of super class of Bird
        # load the images of bird
        self.img_list = [pg.transform.scale_by(pg.image.load("assets/birdup.png").convert_alpha(),scale_factor),
                         pg.transform.scale_by(pg.image.load("assets/birddown.png").convert_alpha(),scale_factor)]
        self.img_index = 0     # used for switching the image
        self.image = self.img_list[self.img_index]
        self.img_rect = self.image.get_rect(center=(100,100))
        self.y_velocity= 0    # velocity means speed
        self.gravity = 10
        self.flap_speed = 250
        self.anim_counter = 0
        self.update_on = False
   
    def update(self,dt):
        if self.update_on:
            self.playAnimation()
            self.apply_gravity(dt)
            # for bird will not go upside of screen
            # bird do not stuck for some time on upper portion of screen
            if self.img_rect.y <=0 and self.flap_speed == 250:
                self.img_rect.y = 0
                self.flap_speed = 0    
            elif self.img_rect.y >0 and self.flap_speed==0:
                self.flap_speed =250
                


    # apply gravity on bird
    def apply_gravity(self,dt):       # here we change y_valocity
            self.y_velocity += self.gravity*dt
            self.img_rect.y += self.y_velocity     # bird drop downword
    # flap the bird mens it goes up's and down's when press space
    def flap(self,dt):                                                  # here we set y_velocity
        self.y_velocity=-self.flap_speed*dt  
    # apply animation on bird means both two images of bird work together as a one    
    def playAnimation(self):
        if self.anim_counter==5:
            self.image=self.img_list[self.img_index]
            if self.img_index==0: self.img_index=1
            else: self.img_index=0
            self.anim_counter=0
        
        self.anim_counter+=1
    # method for Reset the position of bird when game will restart
    def resetPosition(self):
        self.img_rect.center= (100,100)
        self.y_velocity =0



        

