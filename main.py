import pygame
import copy
from random import choice, randint
from time import sleep

pygame.init()

size = width, height = 600, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Tetris')
# иконку
clock = pygame.time.Clock()

snow = []
count_snow = 400
max_size = 5

for i in range(count_snow):
    x_snow = randint(0, width)
    y_snow = randint(0, height)
    size_snow = randint(1, 5)

    snow.append([x_snow, y_snow, size_snow])


class Button:
    def __init__(self, width_but, height_but, text, color, size_font):

        self.width = width_but
        self.height = height_but
        self.text = text
        self.color = color
        self.size_font = size_font

    def draw(self, x, y):
        pygame.draw.rect(screen, (43, 66, 158), (x, y, self.width, self.height))
        font = pygame.font.Font('font/main_font.otf', self.size_font)
        text = font.render(self.text, True, pygame.Color('white'))
        screen.blit(text, (x, y))

        # if pygame.mouse.get_pressed()[0]:
        if x < pygame.mouse.get_pos()[0] < x + self.width and y < pygame.mouse.get_pos()[1] < y + self.height:
            pygame.draw.rect(screen, (255, 255, 255), (x, y, self.width, self.height), 0)
            text = font.render(self.text, True, pygame.Color('Black'))
            screen.blit(text, (x, y))
            if pygame.mouse.get_pressed()[0]:
                transilition(self.text)


def transilition(text):
    if text == 'Exit':
        menu()
    elif text == 'PLAY':
        main()


def snow_fall():
    for i in range(count_snow):
        x_snow = snow[i][0]
        y_snow = snow[i][1]
        size_snow = snow[i][2]

        pygame.draw.circle(screen, tuple([51 * size_snow] * 3), (x_snow, y_snow), size_snow)
        if y_snow > height:
            y_snow = -size_snow
        if x_snow > width:
            x_snow = -size_snow
        snow[i] = [x_snow + size_snow, y_snow + size_snow, size_snow]


def menu():
    screen.fill((43, 66, 158))
    title_pic = pygame.image.load('images/Title.png')
    title_pic = pygame.transform.smoothscale(title_pic, (300, 200))
    title_pic.convert()

    play_btn = Button(185, 90, 'PLAY', (0, 0, 0), 70)

    FPS = 30

    running = True

    while running:
        screen.fill((43, 66, 158))

        # Отрисовка снега
        snow_fall()

        screen.blit(title_pic, (140, 200))
        play_btn.draw(200, 400)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit()

        pygame.display.flip()
        clock.tick(FPS)


def main():
    def get_record():
        try:
            with open('record.txt', 'r') as f:
                return f.read()
        except FileNotFoundError:
            with open('record.txt', 'w') as f:
                f.write('0')
                return '0'

    def set_record(record):
        with open('record.txt', 'w') as f:
            f.write(str(record))

    w, h = 10, 20
    cell = 35

    play_zone = pygame.Surface((350, 700))
    play_zone.fill((18, 28, 89))

    field = [[0 for i in range(w)] for j in range(h)]

    shape_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                 [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                 [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                 [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                 [(0, 0), (0, -1), (0, 1), (-1, -1)],
                 [(0, 0), (0, -1), (0, 1), (1, -1)],
                 [(0, 0), (0, -1), (0, 1), (-1, 0)]]

    colors = [(238, 34, 39), (246, 143, 33), (253, 208, 37), (88, 185, 70), (23, 189, 234), (165, 56, 151)]
    color, next_color = choice(colors), choice(colors)

    shapes = [[pygame.Rect(x + w // 2, y + 1, 1, 1) for x, y in sha_pos] for sha_pos in shape_pos]

    shape_rect = pygame.Rect(0, 0, cell - 2, cell - 2)
    shape, next_shape = copy.deepcopy(choice(shapes)), copy.deepcopy(choice(shapes))

    font = pygame.font.Font('font/main_font.otf', 45)
    small_font = pygame.font.Font('font/main_font.otf', 40)

    score = 0
    score_title = small_font.render('Score:', True, pygame.Color('white'))
    record_title = small_font.render('Record:', True, pygame.Color('white'))
    count_record = small_font.render(get_record(), True, pygame.Color('white'))

    title = font.render('TETRIS', True, pygame.Color('white'))
    speed = 100
    count_speed = 0
    lim_speed = 1600

    net = [pygame.Rect(x * cell, y * cell, cell, cell) for x in range(w) for y in range(h)]

    exit_btn = Button(100, 50, 'Exit', (255, 255, 255), 45)

    FPS = 60

    running = True
    while running:
        pos = 0
        rotate = False

        screen.fill((43, 66, 158))

        # Отрисовка снега
        snow_fall()

        screen.blit(play_zone, (50, 50))
        play_zone.fill((18, 28, 89))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pos = -1

                elif event.key == pygame.K_RIGHT:
                    pos = 1

                elif event.key == pygame.K_UP:
                    rotate = True

                elif event.key == pygame.K_DOWN:
                    speed = 400

        shape_old = copy.deepcopy(shape)

        # передвижение по x
        for i in range(4):
            shape[i].x += pos
            if shape[i].x < 0 or shape[i].x > w - 1:
                shape = copy.deepcopy(shape_old)
                break

        count_speed += speed

        # счетчик скорости падения
        if count_speed >= lim_speed:
            count_speed = 0
            for i in range(4):
                shape[i].y += 1
                if shape[i].y > h - 1 or field[shape[i].y][shape[i].x]:
                    for i in range(4):
                        field[shape_old[i].y][shape_old[i].x] = color
                    color, next_color = next_color, choice(colors)
                    shape, next_shape = next_shape, copy.deepcopy(choice(shapes))
                    speed = 100
                    break

        # поворот
        if rotate:
            for i in range(4):
                x = shape[i].y - shape[0].y
                y = shape[i].x - shape[0].x
                shape[i].x = shape[0].x - x
                shape[i].y = shape[0].y + y
                if shape[i].x < 0 or shape[i].x > w - 1 or shape[i].y > h - 1 or field[shape[i].y][shape[i].x]:
                    shape = copy.deepcopy(shape_old)
                    break
        # проверка линий и подсчет очков
        line, count_line = h - 1, 0
        for row in range(h - 1, -1, -1):
            for i in range(w):
                if all(field[row]):
                    count_line += 1
                    field.pop(row)
                    field.insert(0, [0] * w)
        score += count_line * 100
        count_score = small_font.render(str(score), True, pygame.Color('white'))

        # Отрисовка сети
        for i in net:
            pygame.draw.rect(play_zone, (80, 80, 80), i, 1)

        pygame.draw.line(play_zone, (84, 3, 3), (0, 140), (350, 140), 2)

        # отрисовка фигуры
        for i in range(4):
            shape_rect.x = shape[i].x * cell
            shape_rect.y = shape[i].y * cell
            pygame.draw.rect(play_zone, color, shape_rect)

        # отрисовка следующей фигуры
        for i in range(4):
            shape_rect.x = next_shape[i].x * cell + 325
            shape_rect.y = next_shape[i].y * cell + 150
            pygame.draw.rect(screen, next_color, shape_rect)

        # отрисовка поля
        for y, raw in enumerate(field):
            for x, col in enumerate(raw):
                if col:
                    shape_rect.x, shape_rect.y = x * cell, y * cell
                    pygame.draw.rect(play_zone, col, shape_rect)

        # отрисовка текста
        screen.blit(title, (410, 50))
        screen.blit(record_title, (410, 400))
        screen.blit(count_record, (410, 440))
        screen.blit(score_title, (410, 500))
        screen.blit(count_score, (410, 540))

        # проверка на проигрыш
        if any(field[4]):
            speed = 100
            count_speed = 0

            for i in net:
                pygame.draw.rect(play_zone, choice(colors), i, 0)
                pygame.draw.rect(play_zone, pygame.Color('White'), i, 1)
                screen.blit(play_zone, (50, 50))
                pygame.display.flip()
                clock.tick(100)

            field = [[0 for i in range(w)] for j in range(h)]
            old_record = int(get_record())

            if score > old_record:
                for i in range(3):
                    count_record = small_font.render(get_record(), True, pygame.Color('white'))
                    screen.blit(record_title, (410, 400))
                    screen.blit(count_record, (410, 440))
                    pygame.display.flip()
                    sleep(0.5)
                    pygame.draw.rect(screen, (43, 66, 158), (410, 400, 200, 100))
                    pygame.display.flip()
                    sleep(0.5)

                n = 5
                if score - old_record > 100:
                    f = len(str(score - old_record))
                    n = 10 * (f - 2)

                for i in range(old_record, score + 1, n):
                    count_record = small_font.render(str(i), True, pygame.Color('white'))
                    screen.blit(record_title, (410, 400))
                    screen.blit(count_record, (410, 440))
                    pygame.display.flip()

                    sleep(0.1)

                    pygame.draw.rect(screen, (43, 66, 158), (410, 440, 200, 50))
                    pygame.display.flip()

            screen.blit(count_record, (410, 440))
            pygame.display.flip()

            set_record(max(score, old_record))
            count_record = small_font.render(get_record(), True, pygame.Color('white'))
            sleep(1)

        exit_btn.draw(410, 600)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    menu()
