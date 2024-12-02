import os
import random
import pygame
from os import listdir
from os.path import isfile, join

pygame.display.set_caption("First Platformer")

#Game variables

FPS = 60
BG_COLOR = (255,255,255)
WIDTH,HEIGHT = 1000 , 800
PLAYER_VEL=5

window = pygame.display.set_mode((WIDTH,HEIGHT))

# Game functions
def get_background(name):
    image = pygame.image.load (join("assets","Background",name))
    _,_,width , height = image.get_rect()
    tiles = []
    for k in range (WIDTH // width + 1):
        for l in range(HEIGHT// height +1 ):
            pos = (k*width , l*height)
            tiles.append(pos)
    return tiles , image

def flip (sprites):
    return [pygame.transform.flip(sprite , True , False) for sprite in sprites]

def load_sprite_sheets (dir1,dir2,width,height , directions = False):
    path = join("assets",dir1,dir2)
    images = [f for f in listdir(path) if isfile(join(path,f))]

    all_sprites = {}

    for image in images :
        sprite_sheet = pygame.image.load(join(path , image)).convert_alpha()
        sprites = []
        for i in range ( sprite_sheet.get_width() // width):
            surface = pygame.Surface((width,height),pygame.SRCALPHA,32)
            rect = pygame.Rect(i*width,0,width,height)
            surface.blit(sprite_sheet,(0,0),rect)
            sprites.append(pygame.transform.scale2x(surface))
        if directions:
            all_sprites [image.replace(".png","")+"_right"]=sprites
            all_sprites[image.replace(".png","")+"_left"]=flip(sprites)
        else:
            all_sprites[image.replace(".png","")] = sprites

    return all_sprites  


        

class Player(pygame.sprite.Sprite):
    COLOR = (255,0,0)
    GRAVITY = 0.000001
    SPRITES = load_sprite_sheets("MainCharacters","MaskDude",32,32,True)
    ANIMATION_DELAY = 3
    def __init__(self,x,y,width,height ):
        self.rect = pygame.Rect(x,y,width,height) 
        self.y_vel = 0
        self.x_vel= 0 
        self.animation_count = 0
        self.fall_count = 0
        self.direction = "left"
        self.mask = None 

    def move(self , dx , dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left ( self , vel ):
        self.y_vel -= vel
        if self.direction != "left":
            self.direction = "left"
         
    def move_right (self , vel ):
        self.y_vel += vel 
        if self.direction != "right":
            self.direction = "right"

    def loop (self , fps ):
        self.move(self.y_vel,self.x_vel)
        # self.x_vel += min(1, self.x_vel + self.GRAVITY) 
        self.fall_count += 1
        self.update_sprite()

    def draw (self , win):
        
        win.blit(self.sprite , (self.rect.x , self.rect.y))
    
    def update_sprite(self):
        sprite_sheet="idle"
        if self.x_vel != 0 :
            sprite_sheet ="run"
        
        sprite_sheet_name = sprite_sheet+"_"+self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count +=1


def handle_mov(player):
    keys= pygame.key.get_pressed()
    player.y_vel=0
    if keys[pygame.K_a]:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_d]:
        player.move_right(PLAYER_VEL)

def draw (window ,background , bg_image , player):
    for tile in background :
        window.blit(bg_image , tile)
    
    player.draw(window)
    pygame.display.update()

    
def main (window):
    clock = pygame.time.Clock()
    background,bg_image = get_background("D:\\Dv\\Coding\\Game Dev\\py-game\\assets\Background\\Brown.png")
    run =True
    player = Player(100,100,50,50)
    while run :
        clock.tick(FPS)

        for event in pygame.event.get():
            if event. type == pygame.QUIT:
                run = False 
                break
        handle_mov(player)
        player.loop(FPS)
        draw (window ,  background , bg_image, player )
        
    pygame.quit()
    quit()
if __name__=="__main__":
    main(window)