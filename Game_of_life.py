import pygame
import SaveManager as sl
from Render_Notes import *
from pygame.locals import *
pygame.init()
pygame.mixer.init()
pygame.display.init()
d=f'{os.getcwd()}/mp3 Notes'
sound=[]
count=0
for filename in os.listdir(d):
    sound.append(pygame.mixer.Sound(os.path.join(d, filename)))
BLOCK_SIZE = BLOCK_W, BLOCK_H = (10,10)
BLOCKS = BLOCKS_COLS, BLOCKS_ROWS = 60,40
size = width, height = (BLOCK_W * BLOCKS[0], BLOCK_H * BLOCKS[1])
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Game of Life")

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

class Grid(object):
    paused = False

    def __init__(self, screen, cells=[]):
        self.screen = screen
        self.cells = cells
        for _ in range(BLOCKS_COLS):
            cell = [False] * BLOCKS_ROWS
            self.cells.append(cell)
    def randomize(self):
        for x in range(BLOCKS_COLS):
            for y in range(BLOCKS_ROWS):
                if random.choice([True, False]):
                    self.cells[x][y] = True

    def toggle_pause(self):
        self.paused = not self.paused

    def click_at(self, point):
            x, y = point
            block_x, block_y = x // BLOCK_W, y // BLOCK_H
            self.cells[block_x][block_y] = not self.cells[block_x][block_y]

    def draw_grid(self):
        BLUISH = (30, 30, 100)
        for i in range(BLOCKS_COLS):
            start_point = (i * BLOCK_W, 0)
            end_point = (i * BLOCK_W, height)
            pygame.draw.line(self.screen, BLUISH, start_point, end_point, 1)
        for i in range(BLOCKS_ROWS):
            start_point = (0, i * BLOCK_H)
            end_point = (width, i * BLOCK_H)
            pygame.draw.line(self.screen, BLUISH, start_point, end_point, 1)
    
    def clear_grid(self):
        BLUISH = (30, 30, 100)
        for i in range(BLOCKS_COLS):
            for j in range(BLOCKS_ROWS):
                point = ((i * BLOCK_W)+1,(j * BLOCK_H)+1)
                if(self.cells[point[0]//BLOCK_W][point[1]//BLOCK_H]==True):
                    self.click_at(point)
                
    def draw_cells(self):
        for x in range(BLOCKS_COLS):
            for y in range(BLOCKS_ROWS):
                if self.cells[x][y]:
                    x2, y2 = x * BLOCK_W, y * BLOCK_H
                    cell = pygame.Rect([x2+1, y2+1, BLOCK_W-1, BLOCK_H-1])
                    pygame.draw.rect(self.screen, WHITE, cell)

    def border_at(self, point):
        borders = 0
        x, y = point
        points = ((x+1, y), (x+1, y+1), (x, y+1), (x-1, y+1), (x-1, y),
                  (x-1, y-1), (x, y-1), (x+1, y-1))
        for x2, y2 in points:
            try:
                if 0 <= x2 < BLOCKS_COLS and 0 <= y2 < BLOCKS_ROWS:
                    if self.cells[x2][y2]:
                        borders += 1
                else:
                    continue
            except IndexError:
                pass
        return borders
    def maps(self, value):
        proportion = (value - 0) / (2400 - 0)
        new_value = (proportion * ( len(sound)- 0)) + 0
        return new_value
    def step(self):
        channel1 = pygame.mixer.Channel(0)
        channel2 = pygame.mixer.Channel(1)
        if self.paused:
            return
        cells = copy.deepcopy(self.cells)
        for x in range(BLOCKS_COLS):
            for y in range(BLOCKS_ROWS):
                borders = self.border_at((x, y))
                if not self.cells[x][y]:
                    if borders == 3:
                        cells[x][y] = True
                elif self.cells[x][y]:
                    if not 2 <= borders <= 3:
                        cells[x][y] = False
        gets=render(self.cells)
        if(len(gets)>=2):
            np.sort(gets)
            m=gets[len(gets)-1]
            n=gets[len(gets)-2]
            channel1.play(sound[m])
            channel2.play(sound[n])
        self.cells = cells

grid = Grid(screen)
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                grid.toggle_pause()
            elif event.key == K_r:
                grid.clear_grid()
                grid.randomize()
            elif event.key == K_c:
                grid.clear_grid()
            elif event.key == K_s:
                sl.save(grid.cells)
            elif event.key == K_l:
                cells=sl.load()
                grid=Grid(screen,cells)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            grid.click_at(pygame.mouse.get_pos())

    screen.fill(BLACK)
    grid.draw_grid()
    grid.draw_cells()
    clock.tick(6)
    pygame.display.flip()
    grid.step()