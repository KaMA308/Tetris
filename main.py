import pygame

def main():
    pygame.init()
    size = width, height = 500, 700
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Tetris')



    while pygame.event.wait().type != pygame.QUIT:
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
