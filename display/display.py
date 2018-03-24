from __future__ import print_function
import pygame

def main():
    print("Hello World")

    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    
    red = (255, 0, 0)
    
    pygame.draw.lines(screen, red, True, [(100, 100), (50, 300), (12, 13)], 2)

    pygame.display.flip()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break

    pygame.display.quit()
    print("Goodbye World")

if __name__ == "__main__":
    main()
