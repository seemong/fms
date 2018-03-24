from __future__ import print_function
import pygame

def main():
    print("Hello World")

    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))

    pygame.display.flip()
    while True:
        event == pygame.event.wait()
        if event.type == pygame.QUIT:
            break

if __name__ == "__main__":
    main()
