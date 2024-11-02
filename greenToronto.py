import pygame

pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Green City")

oakCount = 0 
hawthornCount = 0 

# Oak Tree  
oak = pygame.image.load('oak.png').convert()

#Hawthorn
hawthorn = pygame.image.load('hawthorn.png').convert

# Player Goose
player = pygame.image.load('goose1.png').convert()
player = pygame.transform.scale(player, (50, 50))
player_x, player_y = 0, 450

# Info popup summary images
info_normal = pygame.image.load('info1.png').convert()
info_normal = pygame.transform.scale(info_normal, (40, 30))
info_pressed = pygame.image.load('infoPressed.png').convert()  # Load the pressed image
info_pressed = pygame.transform.scale(info_pressed, (40, 30))
info_x, info_y = 450, 8

# Define colors
GREEN = (0, 128, 0)  
BACKGROUND_COLOR = (232, 220, 202)

# Urban
urban1 = pygame.image.load('urban1.png').convert()
urban1 = pygame.transform.scale(urban1, (250, 250))
u_x = -6
u_y = -25

blockSize = 50 

# Function to draw the grid
def drawGrid(): 
    for x in range(0, 500, blockSize):
        for y in range(0, 500, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, (255, 238, 217), rect, 1)  # Draw grid lines in black

# Coordinates for the opening (third column and fifth row)
opening_x = 2 * blockSize  # 2 columns over (0-indexed)
opening_y = 4 * blockSize  # 4 rows down (0-indexed)

running = True
info_pressed_state = False  # To track if the icon is pressed
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            running = False  

        if event.type == pygame.KEYDOWN:
            new_x, new_y = player_x, player_y  
            
            if event.key == pygame.K_LEFT and player_x > 0:
                new_x -= blockSize
            elif event.key == pygame.K_RIGHT and player_x < 500:
                new_x += blockSize
            elif event.key == pygame.K_UP and player_y > 0:
                new_y -= blockSize  
            elif event.key == pygame.K_DOWN and player_y < 500:
                new_y += blockSize

            # Check if the new position collides with the urban area
            # Allow movement only if the goose is at the opening
            is_colliding_with_urban = (new_x + 50 > u_x and new_x < u_x + 250 and 
                                       new_y + 50 > u_y and new_y < u_y + 250)

            # Check for the opening
            is_at_opening = (new_x == opening_x and new_y == opening_y)

            if not is_colliding_with_urban or is_at_opening:
                player_x, player_y = new_x, new_y  

        # Check for mouse button down event
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos 
            if info_x <= mouse_pos[0] <= info_x + 40 and info_y <= mouse_pos[1] <= info_y + 30:
                info_pressed_state = True 

        # Check for mouse button up event
        if event.type == pygame.MOUSEBUTTONUP:
            if info_pressed_state:
                info_pressed_state = False 

    # Fill the background
    screen.fill(BACKGROUND_COLOR)
    
    drawGrid()
    screen.blit(urban1, (u_x, u_y))
    screen.blit(player, (player_x, player_y))
    if info_pressed_state:
        screen.blit(info_pressed, (info_x, info_y))  
    else:
        screen.blit(info_normal, (info_x, info_y)) 
    
    pygame.display.flip()
    
pygame.quit()
