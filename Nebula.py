import pygame,os
pygame.font.init()
pygame.mixer.init()

WIDTH = 800
HEIGHT = 550
VEL=1
sw,sh=50,50
health_font=pygame.font.SysFont("Pixelify Sans",60)
winner_font=pygame.font.SysFont("Pixelify Sans",100)
YELLOW_HIT=pygame.USEREVENT+1
RED_HIT=pygame.USEREVENT+2
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Nebula")
#Create Rectangle for border
border=pygame.Rect(WIDTH/2-7.5, 0,15,HEIGHT)
yellow_spaceimg= pygame.image.load("yellow.png")
yellow_spaceship=pygame.transform.rotate(pygame.transform.scale(yellow_spaceimg,(sw,sh)),90)
red_spaceimg= pygame.image.load("red.png")
red_spaceship=pygame.transform.rotate(pygame.transform.scale(red_spaceimg,(sw,sh)),-90)
bg=pygame.transform.scale(pygame.image.load("orange_space_bg.jpg"),(WIDTH,HEIGHT))

def handle_bullets(red_bullets,yellow_bullets,red,yellow):
    for bullet in red_bullets:
        bullet.x -=VEL
        if bullet.colliderect(yellow):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x<0:
            red_bullets.remove(bullet)    
    for bullet in yellow_bullets:
        bullet.x +=VEL
        if bullet.colliderect(red):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x>WIDTH:
            yellow_bullets.remove(bullet)

def yellow_movement(keypressed,yellow):
    if keypressed[pygame.K_a] and yellow.x>10:
        yellow.x-=VEL
    if keypressed[pygame.K_d] and yellow.x+yellow.width<border.x:
        yellow.x+=VEL
    if keypressed[pygame.K_w] and yellow.y>10:
        yellow.y-=VEL
    if keypressed[pygame.K_s] and yellow.y+yellow.height<HEIGHT:
        yellow.y+=VEL

def red_movement(keypressed,red):
    if keypressed[pygame.K_LEFT] and red.x>border.x+border.width:
        red.x-=VEL
    if keypressed[pygame.K_RIGHT] and red.x+red.width<WIDTH:
        red.x+=VEL
    if keypressed[pygame.K_UP] and red.y>10:
        red.y-=VEL
    if keypressed[pygame.K_DOWN] and red.y+red.height<HEIGHT:
        red.y+=VEL

def draw_screen(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health,winner):
    screen.blit(bg,(0,0))
    if winner=="":
        #drawing the border
        pygame.draw.rect(screen,"black",border)
        screen.blit(yellow_spaceship,(yellow.x,yellow.y))
        screen.blit(red_spaceship,(red.x,red.y))
        for bullet in red_bullets:
            pygame.draw.rect(screen,"white",bullet)
        for bullet in yellow_bullets:
            pygame.draw.rect(screen,"white",bullet)
        red_health_text= health_font.render("health:" +str(red_health),1,"white")
        yellow_health_text= health_font.render("health:" +str(yellow_health),1,"white")
        screen.blit(red_health_text,(WIDTH-160,20))
        screen.blit(yellow_health_text,(20,20))
    else:
        winner_text=winner_font.render(winner,1,"orange")
        screen.blit(winner_text,(100,HEIGHT/2))
    pygame.display.update()



def main():
    red = pygame.Rect(WIDTH-100,HEIGHT/2,sw,sh)
    yellow = pygame.Rect(100,HEIGHT/2,sw,sh)
    red_bullets=[]
    yellow_bullets=[]
    red_health=10
    yellow_health=10
    clock=pygame.time.Clock()
    run=True
    while run:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                run=False
                pygame.quit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_LSHIFT:
                    bullet = pygame.Rect(yellow.x+yellow.width,yellow.y+yellow.height/2,10,5)
                    yellow_bullets.append(bullet)
                if e.key==pygame.K_RSHIFT:
                    bullet = pygame.Rect(red.x,red.y+red.height/2,10,5)
                    red_bullets.append(bullet)
            if e.type==RED_HIT:
                red_health-=1
            if e.type==YELLOW_HIT:
                yellow_health-=1
        winner=""
        if red_health<=0:
            winner="GG yellow WINS U SUCK RED"
        elif yellow_health<=0:
            winner="GG red WINS U SUCK YELLOW"

        keypressed = pygame.key.get_pressed()
        yellow_movement(keypressed,yellow)
        red_movement(keypressed,red)
        handle_bullets(red_bullets,yellow_bullets,red,yellow)
        draw_screen(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health,winner)   
        #main()

main()
