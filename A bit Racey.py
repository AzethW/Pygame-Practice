try:
    import random
    import time
    import pygame
except ImportError as err:
    print("couldn't load module. %s" % (err))
    sys.exit(2)
 
pygame.init()
pygame.joystick.init()
 
display_width = 1366
display_height = 762

center_display_x = int(display_width/2)
center_display_y = int(display_height/2)

top_third_display = int(display_height/3)
bottom_third_display = int(display_height/3*2)

left_third_display = int(display_width/3)
right_third_display = int(display_width/3*2)
 
black = (0,0,0)
white = (255,255,255)

red = (200,0,0)
green = (0,200,0)
blue = (0,0,200)

bright_red = (255,0,0)
bright_green = (0,255,0)
bright_blue = (0,0,255)

highscore = 0
 
block_color = (53,115,255)
 
car_width = 50
 
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()
 
carImg = pygame.image.load('carasset.png')


joystick = pygame.joystick.Joystick(0)
joystick.init()
axes = joystick.get_numaxes()

leftchange = -5
rightchange = 5

gamepad = True

joybuttons = joystick.get_numbuttons()



all_sprites_list = pygame.sprite.Group()

timesinceshot = 0



class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        
        self.image =  pygame.image.load('D:\Data\School\SDD\Assessment\Pygame practice\A bit Racey\bulletasset.png')
        self.rect = self.image.get_rect()
 
    def update(self):
        """ Move the bullet. """
        self.rect.y -= 15

class Car(pygame.sprite.Sprite):
    def __init__(self):
        self.image, self.rect = pygame.image.load('carasset.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

    def update(self):
        for event in pygame.event.get():
            axis = joystick.get_axis(0)
            if axis <= -0.01:
                x_change = leftchange
            elif axis >= 0.01:
                x_change = rightchange
            else:
                x_change = 0

 
def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text,(0,0))
 
def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])
 

 
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
 
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
 
    pygame.display.update()   
    
 


def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ic, (x,y,w,h))
        if click[0] == 1 and action != None:
            if action == "play":
                game_loop()
            elif action == "quit":
                pygame.quit()
                quit()

    else:
        pygame.draw.rect(gameDisplay, ac, (x,y,w,h))

    smallText = pygame.font.Font('freesansbold.ttf', 20)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(TextSurf, TextRect)

def crash():
    message_display('You Crashed')

    play = False
    while play == False:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button('Try agian?', int(left_third_display)-75, int(bottom_third_display), 150, 50, green, bright_green, "play")
        button('Quit', int(right_third_display)-75, int(bottom_third_display), 150, 50, red, bright_red, "quit")

        pygame.display.update()
        clock.tick(20)

def car(x,y):
    gameDisplay.blit(carImg,(x,y))

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
                
        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects("A bit Racey", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button('GO!', int(left_third_display)-50, int(bottom_third_display), 100, 50, green, bright_green, "play")
        button('Quit', int(right_third_display)-50, int(bottom_third_display) , 100, 50, red, bright_red, "quit")



        pygame.display.update()
        clock.tick(15)

     
        
    
    

    
def game_loop():
    x = (display_width * 0.45)
    y = (display_height * 0.8)
 
    x_change = 0
 
    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 4
    thing_width = 100
    thing_height = 100
 
    thingCount = 1

    leftchange = -5
    rightchange = 5
 
    dodged = 0
 
    gameExit = False
 
    while not gameExit:
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            #print(event)
            axis = joystick.get_axis(0)
            if axis <= -0.01:
                x_change = leftchange
            elif axis >= 0.01:
                x_change = rightchange
            else:
                x_change = 0

                for i in range( joybuttons ):
                    button = joystick.get_button( i )

            if event.type == pygame.JOYBUTTONDOWN:
               pygame.event.get()
               # Fire a bullet if the user clicks the mouse button
               bullet = Bullet()
               # Set the bullet so it is where the player is
               bullet.rect.x = x+23
               bullet.rect.y = y
               # Add the bullet to the lists
               all_sprites_list.add(bullet)
               bullet_list.add(bullet)

        all_sprites_list.update()
 
        # Calculate mechanics for each bullet
        for bullet in bullet_list:
 
            # Remove the bullet if it flies up off the screen
            if bullet.rect.y < -10:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)
            
 
        x += x_change
        gameDisplay.fill(white)
 
        things(thing_startx, thing_starty, thing_width, thing_height, block_color)

        # Draw all the spites
        all_sprites_list.draw(gameDisplay)
 
 
        
        thing_starty += thing_speed
        car(x,y)
        things_dodged(dodged)
 
        if x > display_width - car_width or x < 0:
            crash()
 
        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0,display_width)
            dodged += 1
            thing_speed += 1
            thing_width += (dodged * 10)
            leftchange += -.5
            rightchange += .5
 
        if y < thing_starty+thing_height:          
 
            if x > thing_startx and x < thing_startx + thing_width or x+car_width > thing_startx and x + car_width < thing_startx+thing_width:
                crash()
        
        pygame.display.update()
        clock.tick(60)
bullet_list = pygame.sprite.Group()

game_intro()
game_loop()
pygame.quit()
quit()
