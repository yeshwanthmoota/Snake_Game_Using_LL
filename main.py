import pygame, sys
import os
from constants import *
import Snake_class

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init() 

gameDisplay = pygame.display.set_mode((WIDTH,HEIGHT))




def draw_display():
    gameDisplay.fill(BLACK)


def main():

    clock = pygame.time.Clock()
    running = True

    snake = Snake_class.Snake()
    snake.initialize_snake()

    while running: # Game loop

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
            
        snake.update_all_nodes()
        snake.snake_movement()
        draw_display()
        snake.draw_snake(gameDisplay)
        
    pygame.quit()


if __name__=='__main__':
    main()