import pygame
from a_star_constants import *
from node import *

def main(win, width):
    ROWS=50
    grid = make_grid(ROWS, width)
    start= None 
    end =None 
    run = True 
    started =False
    while run :
        draw(win,ROWS,grid,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started :
                continue
            if pygame.mouse.get_pressed()[0]: #left mouse click
                pos = pygame.mouse.get_pos()
                row,col= get_clicked_pos(pos,ROWS,width)
                spot = grid[row][col]
                if not start and spot !=end:
                    start = spot
                    start.make_start()
                elif not end and spot !=start:
                    end = spot
                    end.make_end()
                elif spot !=start and spot !=end :
                    spot.make_barrier()
                
            if pygame.mouse.get_pressed()[2]: # mouse click
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS,width)
                spot = grid[row][col]
                spot.reset()
                if spot ==start:
                    start=None 
                elif spot ==end :
                    end = None
            
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE and not started:
                    print("Updating ...")
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    print("done")
                    algorithm(lambda: draw(win, ROWS, grid, width),grid,start,end)
                    
                if event.key==pygame.K_c:
                    start =None 
                    end =None 
                    grid =make_grid(ROWS, width)
                
    pygame.quit()
    
if __name__=="__main__":
    main(win, WIDTH)