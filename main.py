# coding=utf-8
# import the pygame module, so you can use it
import pygame
from random import randint
import sys
# import resource

sys.setrecursionlimit(1000000)
# resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))

# define a main function

def main():

    def gen(size,count):
        matrix = [[-1 for i in range(0, size)] for i in range(0, size)]
        while count > 0:
            x,y = randint(0,size-1),randint(0,size-1)
            if matrix[x][y] == -1:
                matrix[x][y] = 10
                count -= 1
        return matrix

    def scan(x,y,matrix):
        count = 0
        for i in range(-1,2):
            for j in range(-1, 2):
                if len(matrix[0]) > x-i >= 0 and len(matrix) > y-j >=0 :
                    if matrix[x-i][y-j] == 10:
                            count +=1
        matrix[x][y] = count
        # update()
        # print('x:{} y:{}'.format(x,y))
        if count == 0:
            for i in range(-1,2):
                for j in range(-1, 2):
                    if len(matrix[0]) > x-i >= 0 and len(matrix) > y-j >=0 :
                        if matrix[x - i][y - j] == -1:
                            scan(x - i, y - j, matrix)
    # initialize the pygame module
    pygame.init()
    clock = pygame.time.Clock()
    # load and set the logo
    logo = pygame.image.load("logo.png")
    cell = pygame.image.load("cell.png")
    cell_empty = pygame.image.load("cell_empty.png")
    cell_bomb = pygame.image.load("cell_bmb.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("MineSweeper")

    # print (pygame.font.get_fonts())
    # create a surface on screen that has the size of 240 x 180
    font = pygame.font.SysFont("liberationserif", 15)

    size = 20 #input("количество клеток по стороне: ")
    count = 60 #input("количество бомб: ")

    # 0-8 количество бомб вокруг клетки
    # 9   знак флага
    # 10/11  мина
    # 12 флаг на мине
    cellText = [font.render(str(i), True, (i*24, i+130/(i+1), i*1)) for i in range(0,9)]
    cellText.append(font.render("F", True, (0, 0, 0)))
    cellText.append(font.render("*", True, (0, 0, 0)))
    cellText.append(font.render("*", True, (0, 0, 0)))
    cellText.append(font.render("F", True, (0, 0, 0)))

# задаем размер игровой области и экрана с отступом
    x,y = cell.get_rect().size[0]*size,cell.get_rect().size[1]*size
    screen = pygame.display.set_mode((x, y+50))

    status = "Bombs left: "

    matrix = gen(size,count)
    # define a variable to control the main loop
    running = True
    def update():
        for i in range(0,x//cell.get_rect().size[0]):
            screen.blit(cell, (i* cell.get_rect().size[0],0))
            for j in range(0,y//cell.get_rect().size[1]):
                if matrix[i][j] == 0:
                    screen.blit(cell_empty, (i* cell_empty.get_rect().size[0],j * cell_empty.get_rect().size[1]))
                elif matrix[i][j] != 10:
                    if matrix[i][j] == -1:
                        screen.blit(cell, (i * cell.get_rect().size[0], j * cell.get_rect().size[1]))
                    if matrix[i][j] != -1:
                        if matrix[i][j] == 11:
                            screen.blit(cell_bomb, (i * cell.get_rect().size[0], j * cell.get_rect().size[1]))
                        else:
                            screen.blit(cell_empty, (i * cell.get_rect().size[0], j * cell.get_rect().size[1]))
                        screen.blit(cellText[matrix[i][j]],(i*cell.get_rect().size[0]+3,j * cell.get_rect().size[1]-2))
                elif matrix[i][j] == 10:
                    screen.blit(cell, (i * cell.get_rect().size[0], j * cell.get_rect().size[1]))

        text = font.render(status + str(count), True, (0, 200, 0))
        screen.blit(text,(0,y+5))
        clock.tick(120)
        pygame.display.flip()
    # main loop
    while running:
        screen.fill((0,0,0))

# рендеринг клетки с содержимым
        update()

        # for i,j in enumerate(cellText):
        #     screen.blit(j,(i*16+3,0-2))

        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Set the x, y postions of the mouse click
                xe, ye = event.pos
                posx, posy = xe//cell.get_rect().size[0],ye//cell.get_rect().size[1]
                if event.button == 3:
                    if matrix[posx][posy] == 10:
                        count -= 1
                        matrix[posx][posy] = 12
                    elif matrix[posx][posy] == 9:
                        matrix[posx][posy] = -1
                    elif matrix[posx][posy] == 12:
                        matrix[posx][posy] = 10
                        count += 1
                    elif matrix[posx][posy] == -1:
                        matrix[posx][posy] = 9
                    if count == 0:
                        status = "You win! bombs left: "
                if event.button == 1:
                    if matrix[posx][posy] == 10:
                        status = "yor louse. bombs left: "
                        for i in range(0,len(matrix)-1):
                            for j in range(0,len(matrix[i])-1):
                                if matrix[i][j] == 10:
                                    matrix[i][j] = 11

                    scan(posx,posy,matrix)
        # pygame.time.delay(50)
        clock.tick(30)
        pygame.display.flip()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()