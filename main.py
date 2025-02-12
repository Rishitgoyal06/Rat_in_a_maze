import pygame
import time

pygame.init()

WIDTH, HEIGHT = 600, 600
CELL_SIZE = 50
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

background_img = pygame.image.load("background.jpeg")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

wall_texture = pygame.image.load("wall_texture.jpg")
wall_texture = pygame.transform.scale(wall_texture, (CELL_SIZE, CELL_SIZE))

floor_texture = pygame.image.load("floor_texture.jpg")
floor_texture = pygame.transform.scale(floor_texture, (CELL_SIZE, CELL_SIZE))

rat_img = pygame.image.load("rat_image.jpg")
rat_img = pygame.transform.scale(rat_img, (CELL_SIZE, CELL_SIZE))

move_sound = pygame.mixer.Sound("move.mp3")

pygame.mixer.init()  
pygame.mixer.music.load("background_music.mp3")  
pygame.mixer.music.set_volume(0.3)  
pygame.mixer.music.play(-1)  

win_sound = pygame.mixer.Sound("win.mp3")  
win_sound.set_volume(1.0)  
 

mazes = {
    "Level 1": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 1],  
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],

    "Level 2": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1],
        [1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1],  
        [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 1],  
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],

    "Level 3": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1],  
        [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 1],  
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
}

def level_selection():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 50)
    levels = list(mazes.keys())

    for i, level in enumerate(levels):
        color = YELLOW if i == 2 else WHITE  # Highlight hardest level
        text = font.render(f"Press {i+1} for {level}", True, color)
        screen.blit(text, (WIDTH//4, HEIGHT//3 + i * 60))
    
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    return levels[event.key - pygame.K_1]

def draw_maze(maze, path):
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            x, y = col * CELL_SIZE, row * CELL_SIZE

            if maze[row][col] == 1:
                screen.blit(wall_texture, (x, y))
                
            else:
                screen.blit(floor_texture, (x, y))
            3
            
            if maze[row][col] == 2:
                pygame.draw.rect(screen, GREEN, (x, y, CELL_SIZE, CELL_SIZE))

    for pos in path:
        pygame.draw.rect(screen, BLUE, (pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)
        
def move_rat(dx, dy, maze, rat_pos, path):
    new_x, new_y = rat_pos[0] + dx, rat_pos[1] + dy
    
    if maze[new_y][new_x] != 1: 
        rat_pos = (new_x, new_y)
        path.append(rat_pos)
        move_sound.play()

    return rat_pos

def show_win_message():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200) 
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0)) 

    font = pygame.font.Font(None, 100)  
    text = font.render("YOU WON!!", True, GREEN) 
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    screen.blit(text, text_rect)
    pygame.display.update()
    time.sleep(3)  

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Graphical Rat in a Maze")

selected_level = level_selection()
maze = mazes[selected_level]
rat_pos = (1, 1)
path = [rat_pos]

clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)
    draw_maze(maze, path)
    screen.blit(rat_img, (rat_pos[0] * CELL_SIZE, rat_pos[1] * CELL_SIZE)) 
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            moves = {pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0), pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1)}
            if event.key in moves:
                rat_pos = move_rat(*moves[event.key], maze, rat_pos, path)

    if maze[rat_pos[1]][rat_pos[0]] == 2:
        win_sound.play()
        show_win_message()
        running = False

    clock.tick(FPS)

pygame.quit()







