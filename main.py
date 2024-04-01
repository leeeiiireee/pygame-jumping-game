# game heavily inspired by the game Doodle Jump
import pygame
import random
pygame.init()

# lib of game constants so we can use or change them easily if needed
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
pink = (255, 192, 203)
WIDTH = 400  # width of game window
HEIGHT = 500 # height of game window
background = white
player = pygame.transform.scale(pygame.image.load('kittycat.png'), (90, 70)) # load image of player, in our case a pink cat
fps = 60 
font = pygame.font.SysFont("arial", 16) 
timer = pygame.time.Clock() 
score = 0
high_score = 0
game_over = False


# game variables used throughout the code
player_x = 170
player_y = 400
platforms = [[175, 480, 70, 10], [85, 370, 70, 10], [265, 370, 70, 10], [175, 260, 70, 10], [85, 150, 70, 10], [265, 150, 70, 10], [175, 40, 70, 10]] # x, y, width, height, 4 coordinates to form a platform (pygame rectangle) 
jump = False # works with gravity to make the player jump and know when to stop
y_change = 0 
x_change = 0
player_speed = 3
score_last = 0 
super_jumps = 2 # number of double jumps
jumplast = 0


# game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jump, Dood, jump!') # title of game window


# check for collision between player and platforms
def check_collision(rect_list, j):
    global player_x  # global variables call for position of player
    global player_y
    global y_change # tells direction of player, controls how much you move per frame, if its positive youre coming down, if its negative youre going up, so w can use it to control the jump
    for i in range(len(rect_list)):
        if rect_list[i].colliderect([player_x + 20, player_y + 60, 35, 5]) and jump == False and y_change > 0:
            j = True
    return j



# update player y position every loop

def update_player(y_pos):
    global jump
    global y_change
    jump_height = 10
    gravity = .4    # gravity constant so we can control how fast the player falls

    if jump:
        y_change = -jump_height
        jump = False
    y_pos += y_change
    y_change += gravity
    return y_pos


# handle movement of platforms as game progresses
def update_platforms(my_list, y_pos, change):
    global score
    if y_pos < 250 and change < 0:
        for i in range(len(my_list)):
            my_list[i][1] -= change # if the player is moving up, the platforms move down, so we feel like we're moving up
    else:
        pass

    for item in range(len(my_list)):
        if my_list[item][1] > 500:
            my_list[item] = [random.randint(10, 320), random.randint(-50, -10), 70, 10] # if the platform is off the screen, we reset it to a random position
            score += 1 # if the platform is off the screen, we add a point to the score
    return my_list




# game loop   
running = True
while running == True:
    timer.tick(fps)
    screen.fill(background)
    screen.blit(player, (player_x, player_y))
    blocks = []
    high_score_text = font.render('High Score: ' + str(high_score), True, black, background) # display high score
    screen.blit(high_score_text, (280, 0))
    score_text = font.render('Score: ' + str(score), True, black, background) # display current score
    screen.blit(score_text, (320, 20))

    jump_text = font.render('Double jumps: ' + str(super_jumps), True, black, background) # display number of double jumps
    screen.blit(jump_text, (10, 10))
    if game_over:
        game_over_text = font.render('womp womp :( ', True, black, pink) # display game over text
        screen.blit(game_over_text, (150, 40))


    for i in range(len(platforms)):
        block = pygame.draw.rect(screen, black, platforms[i], 0, 3)
        blocks.append(block)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:
                game_over = False
                player_x = 170
                player_y = 400
                score = 0
                background = white
                score_last = 0
                super_jumps = 2
                jumplast = 0
                platforms = [[175, 480, 70, 10], [85, 370, 70, 10], [265, 370, 70, 10], [175, 260, 70, 10], [85, 150, 70, 10], [265, 150, 70, 10], [175, 40, 70, 10]]
            if event.key == pygame.K_SPACE and not game_over and super_jumps > 0:
                super_jumps -= 1
                y_change = -15
            if event.key == pygame.K_LEFT:
                x_change = -player_speed
            if event.key == pygame.K_RIGHT:
                x_change = player_speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                x_change = 0
            if event.key == pygame.K_RIGHT:
                x_change = 0


    jump = check_collision(blocks, jump)
    player_x += x_change


    if player_y < 440:
        player_y = update_player(player_y)

    else:
        game_over = True
        y_change = 0
        x_change = 0


    platforms = update_platforms(platforms, player_y, y_change)


    if player_x < -20:
        player_x = -20
    elif player_x > 330:
        player_x = 330
    
    # change direction of cat based on movement so it looks like the cat is facing the direction its moving
    if x_change > 0:
        player = pygame.transform.scale(pygame.image.load('kittycat.png'), (90, 70)) 
    elif x_change < 0:
        player = pygame.transform.flip(pygame.transform.scale(pygame.image.load('kittycat.png'), (90, 70)), 1, 0)


    if score > high_score:
        high_score = score

    
    if score - score_last > 15:
        score_last = score
        background = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)) # change background color every 15 points

    if score - jumplast > 50:
        jumplast = score
        super_jumps += 1 # add a double jump every 50 points
   
    pygame.display.flip()

pygame.quit()
  
