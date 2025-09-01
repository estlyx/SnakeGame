import pygame
import random


pygame.init()

# init consts
BLACK = (0, 0, 0)
RED = (213, 50, 80)
BLUE = (50, 153, 213)

DIS_WIDTH = 800
DIS_HEIGHT = 600
SNAKE_BLOCK = 10
SNAKE_SPEED = 15

DIS = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('PythonProject')
CLOCK = pygame.time.Clock()
MSG_FONT = pygame.font.SysFont(name=None, size=25)
SCORE_FONT = pygame.font.SysFont(name=None, size=35)


def disp_current_score(score):
    value = SCORE_FONT.render(f'Your score: {score}', True, BLACK)
    DIS.blit(value, [0, 0])


def disp_snake(SNAKE_BLOCK, snake_list):
    for x in snake_list:
        pygame.draw.rect(DIS, BLACK, [x[0], x[1], SNAKE_BLOCK, SNAKE_BLOCK])


def disp_message(msg, color):
    rendered_msg = MSG_FONT.render(msg, True, color)
    DIS.blit(rendered_msg, [DIS_WIDTH / 4, DIS_HEIGHT / 3])


def game_loop():
    game_over = False
    game_close = False
    snake_list = []
    snake_length = 1

    snake_head_x = DIS_WIDTH / 2
    snake_head_y = DIS_HEIGHT / 2
    snake_head_x_delta = 0
    snake_head_y_delta = 0
    food_x = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    food_y = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

    while not game_over:
        while game_close:
            DIS.fill(BLUE)
            disp_message("Game over! Press Q to exit. Press C to restart", RED)
            disp_current_score(snake_length - 1)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake_head_x_delta = -SNAKE_BLOCK
                    snake_head_y_delta = 0
                elif event.key == pygame.K_RIGHT:
                    snake_head_x_delta = SNAKE_BLOCK
                    snake_head_y_delta = 0
                elif event.key == pygame.K_UP:
                    snake_head_y_delta = -SNAKE_BLOCK
                    snake_head_x_delta = 0
                elif event.key == pygame.K_DOWN:
                    snake_head_y_delta = SNAKE_BLOCK
                    snake_head_x_delta = 0

        if snake_head_x >= DIS_WIDTH or snake_head_x < 0 or snake_head_y >= DIS_HEIGHT or snake_head_y < 0:
            game_close = True

        DIS.fill(BLUE)
        pygame.draw.rect(DIS, RED, [food_x, food_y, SNAKE_BLOCK, SNAKE_BLOCK])

        snake_head_x += snake_head_x_delta
        snake_head_y += snake_head_y_delta
        snake_head = [snake_head_x, snake_head_y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        disp_snake(SNAKE_BLOCK, snake_list)
        disp_current_score(snake_length - 1)
        pygame.display.update()

        if snake_head_x == food_x and snake_head_y == food_y:
            food_x = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            food_y = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            snake_length += 1
        CLOCK.tick(SNAKE_SPEED)

    pygame.quit()
    quit()


if __name__ == '__main__':
    game_loop()
