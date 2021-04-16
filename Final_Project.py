# Final Project
# Contributers: Simon Elizondo

#Credits: 
#   Walkthrough provided by Coding With Russ 
#   https://youtu.be/Ongc4EVqRjo
#   https://github.com/russs123/Platformer

#   Sprites Provided by Tarkan809
#   https://www.spriters-resource.com/fullview/85390/


import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60


screen_width = 1000
screen_hight = 800

screen = pygame.display.set_mode((screen_width,screen_hight))
pygame.display.set_caption('Final Project')

#define game variables
tile_size = 50
gameover = 0
main_menu = True


#loads images
bg_img = pygame.image.load('Assets/sky.jpg')                    #Loads Background image
restart_img = pygame.image.load("Assets/respawn.png")
start_img = pygame.image.load("Assets/start_btn.jpg")

class Button():
    def __init__(self, x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouse over and and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        #draw button
        screen.blit(self.image, self.rect)

        return action

class Player():
    def __init__(self, x, y):
        #self.images_right = []
        #self.images_left = []
        #self.index = 0
        #self.counter = 0
        #for num in range(1, 6):  
        #    img_right = pygame.image.load(f'Assets/Steve{num}.png')
        #    img_right = pygame.transform.scale(img_right,(40,80))
        #    img_left = pygame.transform.flip(img_right,True, False)
        #    self.images_right.append(img_right)
        #    self.images_left.append(img_left)
        
        ##self.image = pygame.transform.scale(img,(40,80))
        #self.dead_image = pygame.image.load("Assets/Steve_dead1.png")
        #self.image = self.images_right[self.index]
        #self.rect = self.image.get_rect()
        #self.rect.x = x
        #self.rect.y = y
        #self.width = self.image.get_width()
        #self.height = self.image.get_height()
        #self.vel_y = 0
        #self.jumped = False
        #self.direction = 0

        self.reset(x,y)

    def update(self, gameover):
        dx = 0
        dy = 0
        walk_cooldown = 5

        if gameover == 0:

            #gets key inputs
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                self.vel_y= -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            #handle animation
            #self.counter += 1
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
            #adds gravity
            self.vel_y += 1
            if self.vel_y>10:
                self.vel_y = 10

            dy += self.vel_y

            #Check for collision
            self.in_air = True
            for tile in world.tile_list:
                #check for collision in the x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                #check for collision in the y direction
                if tile[1].colliderect(self.rect.x,self.rect.y + dy,self.width,self.height):
                    #check if below the ground
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    #check if above gound
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            #check for collision with enemeies
            if pygame.sprite.spritecollide(self,creeper_group, False):
                gameover = -1
            if pygame.sprite.spritecollide(self,lava_group, False):
                gameover = -1


            #update player coordiates
            self.rect.x += dx
            self.rect.y += dy

            #if self.rect.bottom > screen_hight:
            #    self.rect.bottom = screen_hight
            #    dy = 0


        elif gameover == -1:
            self.image = self.dead_image

            self.rect.y -= 5
        #Draws the player character on screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen,(255,255,255),self.rect,2)

        return gameover
    def reset(self,x,y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 6):  
            img_right = pygame.image.load(f'Assets/Steve{num}.png')
            img_right = pygame.transform.scale(img_right,(40,80))
            img_left = pygame.transform.flip(img_right,True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        
        #self.image = pygame.transform.scale(img,(40,80))
        self.dead_image = pygame.image.load("Assets/Steve_dead1.png")
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True

class World():
    def __init__(self, data):
        self.tile_list = []
        #load images
        dirt_img = pygame.image.load('Assets/dirt.jpg')
        grass_img = pygame.image.load("Assets/grass.jpg")

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    creeper = Enemy(col_count * tile_size, row_count * tile_size)
                    creeper_group.add(creeper)
                if tile == 6:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])
            pygame.draw.rect(screen,(255,255,255),tile[1],2)
      
            

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Assets/Creeper.jpg")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1

        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
class Lava(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("Assets/lava.jpg")
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1], 
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1], 
[1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 2, 2, 2, 2, 2, 2, 2, 6, 2, 6, 2, 6, 2, 2, 2, 2, 2, 1]
]

player = Player(100, screen_hight - 130)

creeper_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()

world = World(world_data)

#creates buttons
restart_button = Button(screen_width // 2 - 175, screen_hight // 2, restart_img)
start_button = Button(screen_width // 2 - 200, screen_hight // 2, start_img)


run = True
while run:

    clock.tick(fps)

    screen.blit(bg_img, (0, 0))
    if main_menu == True:
        if start_button.draw():
            main_menu = False
    else:
        world.draw()

        if gameover == 0:
            creeper_group.update()
        creeper_group.draw(screen)
        lava_group.draw(screen)

        gameover = player.update(gameover)

        #the player has died
        if gameover == -1:
            if restart_button.draw():
                player.reset(100, screen_hight - 130)
                gameover = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()