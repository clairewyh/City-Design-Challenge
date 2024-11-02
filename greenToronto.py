import pygame

pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Green City")

# Counts
oakCount = 0
planted_positions = []  # List to track planted tree positions

# Player Goose
player = pygame.image.load('goose1.png').convert()
player = pygame.transform.scale(player, (50, 50))
player_x, player_y = 0, 450

# Info popup summary images
info_normal = pygame.image.load('info1.png').convert()
info_normal = pygame.transform.scale(info_normal, (40, 30))
info_pressed = pygame.image.load('infoPressed.png').convert()
info_pressed = pygame.transform.scale(info_pressed, (40, 30))
info_x, info_y = 450, 8

# Oak
oak = pygame.image.load('oak.png').convert()
oak = pygame.transform.scale(oak, (40, 40))
oakPop = pygame.image.load('oakPop.png').convert()
oakPop = pygame.transform.scale(oakPop, (500, 150))
oakPopx, oakPopy = 0, 350

#Hawthorn
hawthorn = pygame.image.load('hawthorn.png').convert()
hawthorn = pygame.transform.scale(hawthorn,(40,40))
hawthornPop = pygame.image.load('hawthornPop.png').convert()
hawthornPopx, hawthornPopy = 0, 350 

# Define colors
BACKGROUND_COLOR = (232, 220, 202)

# Urban area
urban1 = pygame.image.load('urban1.png').convert()
urban1 = pygame.transform.scale(urban1, (250, 250))
u_x = -6
u_y = -25

greenery = pygame.image.load('greenery.png').convert()
greenery = pygame.transform.scale(greenery,(185,185))
g_x= 340
g_y = 340

# Block size
blockSize = 50 

# Opening coordinates
opening_x = 2 * blockSize  
opening_y = 4 * blockSize  

running = True
info_pressed_state = False  
tree_position = None  # Track the position of the tree
oak_pop_visible = False  # Track if the oak popup image is visible

# Function to draw the grid
def drawGrid(): 
    for x in range(0, 500, blockSize):
        for y in range(0, 500, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, (255, 238, 217), rect, 1)  # Draw grid lines in light color

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

            # Check for collisions and openings
            is_colliding_with_urban = (new_x + 50 > u_x and new_x < u_x + 250 and 
                                       new_y + 50 > u_y and new_y < u_y + 250)

            is_at_opening = (new_x == opening_x and new_y == opening_y)

            if not is_colliding_with_urban or is_at_opening:
                player_x, player_y = new_x, new_y  

                # Update tree position if at opening
                if is_at_opening:
                    tree_position = (player_x + 5, player_y - 40)  # Center tree above the goose
                else:
                    tree_position = None  # Remove tree if not at opening

                # Hide the oak popup if the goose moves away from the opening
                if not is_at_opening and oak_pop_visible:
                    oak_pop_visible = False

            # Place tree when Enter is pressed
            if event.key == pygame.K_RETURN and tree_position:
                planted_positions.append(tree_position)  # Add the position to the planted list
                oakCount += 1  # Increment count
                oak_pop_visible = True  # Show the oak popup image
                tree_position = None  # Remove visual tree

        # Mouse events
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos 
            if info_x <= mouse_pos[0] <= info_x + 40 and info_y <= mouse_pos[1] <= info_y + 30:
                info_pressed_state = True 

        if event.type == pygame.MOUSEBUTTONUP:
            if info_pressed_state:
                info_pressed_state = False 

    # Fill the background
    screen.fill(BACKGROUND_COLOR)

    # Draw the grid
    drawGrid()

    # Draw areas and player
    screen.blit(urban1, (u_x, u_y))
    screen.blit(greenery, (g_x,g_y))
    screen.blit(player, (player_x, player_y))
    
    # Show tree above the goose if at opening
    if tree_position:
        screen.blit(oak, tree_position)  # Show the visual tree above the goose
    
    # Show planted trees
    for spot in planted_positions:
        screen.blit(oak, spot)  # Draw the planted tree at the tracked position

    # Draw oak popup image if visible
    if oak_pop_visible:
        screen.blit(oakPop, (oakPopx, oakPopy))  # Display oak popup image at a specific position

    if info_pressed_state:
        screen.blit(info_pressed, (info_x, info_y))  
    else:
        screen.blit(info_normal, (info_x, info_y)) 

    pygame.display.flip()
    
pygame.quit()
