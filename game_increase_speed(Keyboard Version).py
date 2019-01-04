import pygame
from pygame.locals import *
import math
import random

################# Create Levels<----Remaining ####################
RUN, PAUSE = 1, 0

def start(screen):
	#Start Page
	black=(0,0,0)
	end_it=False
	play = pygame.image.load("resources/images/play.png")
	while (end_it==False):
		screen.fill(black)
		pygame.font.init()
		font1 = pygame.font.Font("resources/myfont.ttf", 72)
		text1 = font1.render("Boring Game!", True, (255, 255, 255))
		textRect1 = text1.get_rect()
		textRect1.centerx = screen.get_rect().centerx
		playRect = play.get_rect()
		playRect.centerx = screen.get_rect().centerx
		playRect.centery = screen.get_rect().centery
		for e in pygame.event.get():
			if e.type==pygame.QUIT:
				pygame.quit()
				exit(0)
			if e.type==MOUSEBUTTONDOWN:
				x, y = pygame.mouse.get_pos()
				if playRect.collidepoint(x, y):
					end_it=True
		screen.blit(text1,textRect1)
		screen.blit(play, playRect)
		pygame.display.flip()
	return

def timer(screen):
	w, h = pygame.display.get_surface().get_size()#get screen size
	font = pygame.font.Font(None, 24)
	survivedtext = font.render(str((pygame.time.get_ticks())/60000)+":"+str((pygame.time.get_ticks())/1000%60).zfill(2), True, (0,0,0))
	textRect = survivedtext.get_rect()
	textRect.topright=[w-80,5]
	screen.blit(survivedtext, textRect)
	return

def scoreboard(screen, badguy_kill):
	w, h = pygame.display.get_surface().get_size()#get screen size
	font = pygame.font.Font(None, 24)
	score = font.render(str(badguy_kill), True, (0,0,0))
	scoreRect = score.get_rect()
	scoreRect.topright=[(w-80)/3,5]
	screen.blit(score, scoreRect)
	return
    
def accuracymeter(screen, accuracy):
	w, h = pygame.display.get_surface().get_size()#get screen size
	font = pygame.font.Font(None, 24)
	accurac = font.render("{0:.2f}".format(round(accuracy,2)), True, (0,0,0))
	accurect = accurac.get_rect()
	accurect.topright=[2*(w-80)/3,5]
	screen.blit(accurac, accurect)
	return

def game(screen):
	w, h = pygame.display.get_surface().get_size()

	player = pygame.image.load("resources/images/soldierKV.png")
	grass = pygame.image.load("resources/images/grass.jpg")
	castle = pygame.image.load("resources/images/ship.png")
	arrow = pygame.image.load("resources/images/bulletraja.png")
	badguyimg = pygame.image.load("resources/images/zombie.png")
	healthbar = pygame.image.load("resources/images/healthbar.png")
	health = pygame.image.load("resources/images/health.png")

	#Sound Effect
	pygame.mixer.init()
	hit = pygame.mixer.Sound("resources/audio/explode.wav")
	enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
	shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
	hit.set_volume(0.05)
	enemy.set_volume(0.05)
	shoot.set_volume(0.05)
	pygame.mixer.music.load('resources/audio/moonlight.wav')
	pygame.mixer.music.play(-1, 0.0)
	pygame.mixer.music.set_volume(0.25)

	#Variables
	state = RUN
	keys = [False, False, False, False]
	playerpos=[(w-180)/2,h-244]
	acc=[0,0]
	arrows=[]
	badtimer=1
	badtimer1=0
	badguys=[]
	badrect=[]
	healthvalue=194
	badguy_kill=0
	speed_factor=50
	bg_vel = 2
	arrow_vel = 10
	accuracy = 0.0
	running = 1
	exitcode = 0
	rot = 0

	pygame.key.set_repeat(50,50) #Continuos Key input
	
	#Game loop
	while running:
	    if state == RUN:
		    badtimer -= 1
		    screen.fill(0) #clearing the screen

		    #1. Draws the game state to the screen
		    position = pygame.mouse.get_pos()
		    playerrot = pygame.transform.rotate(player, rot) #player rotation
		    playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)

		    #creating the environment
		    for x in range(w/grass.get_width()+1):
			for y in range(h/grass.get_height()+1):
			    screen.blit(grass,(x*100,y*100))
		    for x in range(30,w-180,105):
			screen.blit(castle,(x,h-180))
		    screen.blit(playerrot, playerpos1)

		    #shooting the arrow
		    for bullet in arrows:
			index=0
			#velocity of arrow
			velx=math.sin(bullet[0]*math.pi/180)*arrow_vel
			vely=math.cos(bullet[0]*math.pi/180)*arrow_vel
			bullet[1]-=velx
			bullet[2]-=vely
			if bullet[1]<-64 or bullet[1]>w or bullet[2]<-64 or bullet[2]>h:
			    arrows.pop(index)
			index+=1
		    for projectile in arrows:
			arrow1 = pygame.transform.rotate(arrow, projectile[0]+90)
			screen.blit(arrow1, (projectile[1], projectile[2]))

		    #speed function
		    if badguy_kill == speed_factor:
		    	if bg_vel < 32:
			    bg_vel *= 2
			    #get rotation vel
			    #To understand how the below equation came make time same at halfway
			    arrow_vel = math.sqrt(4*w*w+h*h)*bg_vel/h #mathematical equation --> more than required speed since components not broken
			    speed_factor -= 10
			    speed_factor = badguy_kill + speed_factor
			
		    #increase speed of generation
		    if badtimer<=0:
			badguys.append([random.randint(50,w-180), 0])
			badrect.append(pygame.Rect(badguyimg.get_rect()))
			badtimer=100-(badtimer1*2)#Main Line
			if badtimer1>=42:
			    badtimer1=42
			else:
			    badtimer1+=5

		    index=-1
		    for n in range(len(badguys)):
			badguys[n][1]+=bg_vel #velocity of badguys
			badrect[n]=pygame.Rect(badguyimg.get_rect())
			badrect[n].bottom=badguys[n][1]
			badrect[n].left=badguys[n][0]
			index+=1
			if badrect[n].bottom>(h-244):
			    hit.play()
			    healthvalue -= random.randint(5,20)
			    badguys.pop(index)
			    badrect.pop(index)
			    break
		    for badguy in badguys:
			screen.blit(badguyimg, badguy)

		    index1=0
		    for bullet in arrows:
			bullrect=pygame.Rect(arrow.get_rect())
			bullrect.left=bullet[1]
			bullrect.top=bullet[2]
			for bad in badrect:
			    if bullrect.colliderect(bad):
				enemy.play()
				acc[0]+=1
				remove_index = badrect.index(bad)
				badguys.pop(remove_index)
				badrect.pop(remove_index)
				badguy_kill+=1
				arrows.pop(index1)
			index1+=1

		    
		    timer(screen) #Timer
		    scoreboard(screen, badguy_kill) #Scoreboard
		    accuracymeter(screen, accuracy) #Accuracy

		    #health
		    screen.blit(healthbar, (5,5))
		    for health1 in range(healthvalue):
			screen.blit(health, (health1+8,8))

	    elif state == PAUSE:
	    	pygame.font.init()
		font1 = pygame.font.Font("resources/myfont.ttf", 72)
		text1 = font1.render("Paused", True, (0, 128, 0))
		textRect1 = text1.get_rect()
		textRect1.centerx = screen.get_rect().centerx
		textRect1.centery = screen.get_rect().centery-72
	    	screen.blit(text1, textRect1)
	    	
	    #2. Updates the game state
	    pygame.display.flip()
	    #3. Handles events 
	    #controls
	    for e in pygame.event.get():
		if e.type==pygame.QUIT:
		    pygame.quit()
		    exit(0)
		if e.type == pygame.KEYDOWN:
		    if pygame.key.get_pressed()[pygame.K_w]:#continuous press
		        keys[0]=True
		    elif pygame.key.get_pressed()[pygame.K_a]:
		        keys[1]=True
		    elif pygame.key.get_pressed()[pygame.K_s]:
		        keys[2]=True
		    elif pygame.key.get_pressed()[pygame.K_d]:
		        keys[3]=True
		    if pygame.key.get_pressed()[pygame.K_LEFT]:
                    	rot += 10
        		if rot > 360:
            			rot = 10
                    elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                    	rot -= 10
        		if rot < 0:
            			rot = 350
		    if e.key == pygame.K_p:
		    	if state == RUN:
		        	state = PAUSE
		        else:
		        	state = RUN
		if e.type == pygame.KEYUP:
		    if e.key==pygame.K_w:
		        keys[0]=False
		    elif e.key==pygame.K_a:
		        keys[1]=False
		    elif e.key==pygame.K_s:
		        keys[2]=False
		    elif e.key==pygame.K_d:
		        keys[3]=False
		    if e.key==pygame.K_SPACE:
			    shoot.play()
			    acc[1]+=1
			    arrows.append([rot,playerpos1[0]+32,playerpos1[1]+32])
    
	       #Move player
		if keys[0]:
		    playerpos[1]-=10
		elif keys[2]:
		   playerpos[1]+=10
		if keys[1]:
		    playerpos[0]-=10
		elif keys[3]:
		    playerpos[0]+=10

	    if badguy_kill == 1000:#maximum score
		running=0
		exitcode=1
	    if healthvalue<=0:
		running=0
		exitcode=0
	    if acc[1]!=0:
		accuracy=acc[0]*1.0/acc[1]*100
	    else:
		accuracy=0
	return exitcode, badguy_kill, accuracy

def gameover(screen, replay, badguy_kill, accuracy):
	replayRect = replay.get_rect()
	pygame.font.init()
	font1 = pygame.font.Font("resources/myfont.ttf", 72)
	text1 = font1.render("Game Over", True, (255, 0, 0))
	textRect1 = text1.get_rect()
	textRect1.centerx = screen.get_rect().centerx
	textRect1.centery = screen.get_rect().centery-72
	font = pygame.font.Font(None, 24)
	text2 = font.render("Score: "+str(badguy_kill), True, (255,0,0))
	textRect2 = text2.get_rect()
	textRect2.centerx = screen.get_rect().centerx
	textRect2.centery = screen.get_rect().centery+24
	text = font.render("Accuracy: "+"{0:.2f}".format(round(accuracy,2))+"%", True, (255,0,0))
	textRect = text.get_rect()
	textRect.centerx = screen.get_rect().centerx
	textRect.centery = screen.get_rect().centery+48
	replayRect.centerx = screen.get_rect().centerx
	replayRect.centery = screen.get_rect().centery+100
	screen.fill((128, 0, 0))
	screen.blit(text1,textRect1)
	screen.blit(text2, textRect2)
	screen.blit(text, textRect)
	screen.blit(replay, replayRect)
	return replayRect
    
def win(screen, badguy_kill, accuracy):
	pygame.font.init()
	font1 = pygame.font.Font("resources/myfont.ttf", 72)
	text1 = font1.render("You Win", True, (0, 255, 0))
	textRect1 = text1.get_rect()
	textRect1.centerx = screen.get_rect().centerx
	textRect1.centery = screen.get_rect().centery-72
	font = pygame.font.Font(None, 24)
	text2 = font.render("Score: "+str(badguy_kill), True, (0, 255,0))
	textRect2 = text2.get_rect()
	textRect2.centerx = screen.get_rect().centerx
	textRect2.centery = screen.get_rect().centery+24
	text = font.render("Accuracy: "+"{0:.2f}".format(round(accuracy,2))+"%", True, (0,255,0))
	textRect = text.get_rect()
	textRect.centerx = screen.get_rect().centerx
	textRect.centery = screen.get_rect().centery+24
	screen.fill((0, 128, 0))
	screen.blit(text1,textRect1)
	screen.blit(text2, textRect2)
	screen.blit(text, textRect)
	return

def exitscreen(screen, exitcode, badguy_kill, accuracy):
	replay = pygame.image.load("resources/images/replay.png")
	w, h = pygame.display.get_surface().get_size()
	if exitcode==0:
		replayRect = gameover(screen, replay, badguy_kill, accuracy)

	else:
		win(screen, badguy_kill, accuracy)
	while 1:
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				pygame.quit()
				exit(0)
			if e.type==MOUSEBUTTONDOWN:
				x, y = pygame.mouse.get_pos()
				if replayRect.collidepoint(x, y):
					game(screen)
		pygame.display.flip()
	return

def main():
	#Initialization
	pygame.init()
	infoObject = pygame.display.Info()
	w, h = infoObject.current_w, infoObject.current_h
	screen = pygame.display.set_mode((w,h))
	pygame.display.set_caption('Boring Game!')
	#game
	start(screen)
	exitcode, badguy_kill, accuracy = game(screen)
	exitscreen(screen, exitcode, badguy_kill, accuracy)
	return

if __name__ == '__main__':
	main()
