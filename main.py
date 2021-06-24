import pygame, sys
import os ,time
from constants import *
import Snake_class

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
pygame.font.init()
pygame.mixer.init()

gameDisplay = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Snake Mania")


GAME_OVER = pygame.USEREVENT + 1 # When snake's head dashes with one of it's body parts.
FOOD_EATEN = pygame.USEREVENT + 2 # When the snake eats the food


SCORE_FONT = pygame.font.SysFont("comicsans", 50, bold = True)
COUNTER_FONT = pygame.font.SysFont("Comic Sans MS", 50, bold = True)

#----------------------code for working on terminal----------
final_path = os.getcwd()
path_list = final_path.split("\\")
if path_list[-1] == "Snake_game" or  path_list[-1] == "Snake_game-master":
    final_path = final_path + "\\" + "music_and_sounds" + "\\"
#----------------------code for working on terminal----------

#----------------------code for working on vs code----------
else:
    final_path = os.path.dirname(__file__) + "\\" + "music_and_sounds" + "\\"
#----------------------code for working on vs code----------

BACKGROUND_MUSIC = pygame.mixer.Sound(final_path + "background_music.wav")
BACKGROUND_MUSIC.set_volume(0.5)
FOOD_EATING_SOUND = pygame.mixer.Sound(final_path + "eating_sound.wav")
FOOD_EATING_SOUND.set_volume(1)
GAME_TIMER = pygame.mixer.Sound(final_path + "game_timer.wav")
GAME_TIMER.set_volume(0.5)
GO_SOUND = pygame.mixer.Sound(final_path + "game_start.wav")
GO_SOUND.set_volume(0.5)
CHEERING_SOUND = pygame.mixer.Sound(final_path + "cheering.wav")
CHEERING_SOUND.set_volume(1)

channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)

def draw_score_board():
    gameDisplay.fill(BLACK)

    score = SCORE_FONT.render("YOUR SCORE : {}".format(SCORE), 1, ORANGE)

    gameDisplay.blit(score,(WIDTH/2-(score.get_width())/2, HEIGHT/2 -(score.get_height())/2))

    pygame.display.update()
    channel2.play(CHEERING_SOUND, 1, 5000)
    time.sleep(5)

def draw_timer(count):
    gameDisplay.fill(BLACK)

    Count = COUNTER_FONT.render("{}".format(count), 1, ORANGE)

    gameDisplay.blit(Count,(WIDTH/2-(Count.get_width())/2, HEIGHT/4 -(Count.get_height())/2))

    pygame.display.update()




def draw_display(snake, snake_food):
    gameDisplay.fill(BLACK)
    ptr = Snake_class.Snake()
    ptr = snake.head

    # drawing the snake
    while ptr is not None: 
        pygame.draw.rect(gameDisplay, WHITE, pygame.Rect(ptr.x, ptr.y, SNAKE_NODE_SIDE, SNAKE_NODE_SIDE), 2) # drawing each node
        pygame.draw.rect(gameDisplay, GREEN, pygame.Rect(ptr.x + 2, ptr.y + 2, SNAKE_NODE_SIDE - 6, SNAKE_NODE_SIDE - 6), 0)
        ptr = ptr.next
    condition = snake.food_eaten(snake_food)
    if condition:# it doesn't draw the food if it is eaten.
            pygame.event.post(pygame.event.Event(FOOD_EATEN))
            channel2.play(FOOD_EATING_SOUND ,1, 200)
    else:
        # drawing the snake food if and only if the snake hasn't eaten the food
        x = snake_food[0]
        y = snake_food[1]
        pygame.draw.rect(gameDisplay, RED, pygame.Rect(x, y, SNAKE_NODE_SIDE, SNAKE_NODE_SIDE)) # drawing the snake food

    pygame.display.update()


def main():
    exit_code = 0

    global SCORE, SCORE_VALUE

    clock = pygame.time.Clock()
    running = True

    count=3
    while count>=0:
        if(count != 0):
            draw_timer(count)
            channel2.play(GAME_TIMER, 1, 700)
            count -= 1
            time.sleep(1)
        else:
            draw_timer("Start eating!")
            channel2.play(GO_SOUND, 1, 2300)
            count -= 1
            time.sleep(3)
    channel1.play(BACKGROUND_MUSIC,-1)
    snake = Snake_class.Snake()
    snake.initialize_snake()

    snake_food = snake.food_spawn() # First food the snake is going to eat

    while running: # Game loop

        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.KEYDOWN:
                # updating the head velocity direction.
                if event.key == pygame.K_UP and not(snake.head.vel_direction == 2):
                    snake.head.vel_direction = 1
                    snake.head.change_value = 1       
                # elif because it can move only in direction at a time
                elif event.key == pygame.K_DOWN and not(snake.head.vel_direction == 1): 
                    snake.head.vel_direction = 2
                    snake.head.change_value = 1
                elif event.key == pygame.K_LEFT and not(snake.head.vel_direction == 4):
                    snake.head.vel_direction = 3
                    snake.head.change_value = 1
                elif event.key == pygame.K_RIGHT and not(snake.head.vel_direction == 3):
                    snake.head.vel_direction = 4
                    snake.head.change_value = 1

            if event.type == FOOD_EATEN:
                SCORE += 10
                snake_food = snake.food_spawn() 
                # passing in snake to avoid the food being respawn over the snake's body

            if event.type == GAME_OVER:
                channel1.stop()
                draw_score_board()
                exit_code = 1
                break
        if exit_code == 1:
            break   
        snake.update_all_nodes()
        if snake.head_collision():
            pygame.event.post(pygame.event.Event(GAME_OVER))
        snake.snake_movement()
        draw_display(snake, snake_food)
    
    main()


if __name__=='__main__':
    main()