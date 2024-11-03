import pygame

pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Green City")

# Load sound effects
walk_sound = pygame.mixer.Sound('walk.mp3')
plant_sound = pygame.mixer.Sound('plot.mp3')
info_sound = pygame.mixer.Sound('info.wav')

# Counts
oakCount = 0
hawthornCount = 0
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

# Hawthorn
hawthorn = pygame.image.load('hawthorn.png').convert()
hawthorn = pygame.transform.scale(hawthorn, (44, 44))
hawthornPop = pygame.image.load('hawthornPop.png').convert()
hawthornPop = pygame.transform.scale(hawthornPop, (500, 150))  # Assuming the size is similar
hawthornPopx, hawthornPopy = 0, 350 
 
# Info popup
infoPop = pygame.image.load('infoPop.png').convert()
infoPop = pygame.transform.scale(infoPop, (500, 150))  # Assuming size is similar to oakPop and hawthornPop

# Track visibility of info popup
info_pop_visible = False  # Track if the info popup image is visible

# Define colors
BACKGROUND_COLOR = (232, 220, 202)

# Urban area
urban1 = pygame.image.load('urban1.png').convert()
urban1 = pygame.transform.scale(urban1, (250, 250))
u_x = -6
u_y = -25

# Green area
greenery = pygame.image.load('greenery.png').convert()
greenery = pygame.transform.scale(greenery, (185, 185))
g_x = 340
g_y = 325

# Block size
blockSize = 50 

# Opening coordinates
opening_x = 2 * blockSize  
opening_y = 4 * blockSize  

# Define the opening2 limits
opening2_limit_column = 7 * blockSize
opening2_limit_rows = [450, 400, 350]  # Bottom three rows (in pixels)

running = True
info_pressed_state = False  
tree_position = None  # Track the position of the oak tree
hawthorn_position = None  # Track the position of the hawthorn tree
oak_pop_visible = False  # Track if the oak popup image is visible
hawthorn_pop_visible = False  # Track if the hawthorn popup image is visible

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
                walk_sound.play()  # Play walking sound
            elif event.key == pygame.K_RIGHT and player_x < 500 - 50:
                new_x += blockSize
                walk_sound.play()  # Play walking sound
            elif event.key == pygame.K_UP and player_y > 0:
                new_y -= blockSize  
                walk_sound.play()  # Play walking sound
            elif event.key == pygame.K_DOWN and player_y < 500 - 50:
                new_y += blockSize
                walk_sound.play()  # Play walking sound

            # Check for collisions and openings
            is_colliding_with_urban = (new_x + 50 > u_x and new_x < u_x + 250 and new_y + 50 > u_y and new_y < u_y + 250)
            is_at_opening = (new_x == opening_x and new_y == opening_y)

            # Check for opening2 restrictions (bottom three rows)
            is_in_restricted_area = new_y in opening2_limit_rows and new_x >= opening2_limit_column

            if not is_colliding_with_urban or is_at_opening:
                if not is_in_restricted_area:
                    player_x, player_y = new_x, new_y  

                # Update tree position if at opening
                if is_at_opening:
                    tree_position = (player_x + 5, player_y - 40)  # Center tree above the goose
                else:
                    tree_position = None  # Remove tree if not at opening

                # Hide the oak popup if the goose moves away from the opening
                if not is_at_opening and oak_pop_visible:
                    oak_pop_visible = False

                # Check if the hawthorn position is set and whether to show/hide hawthorn popup
                if player_x == 8 * blockSize and player_y == 300:  # Check for 4th row from the bottom and 2nd from the right
                    hawthorn_position = (8 * blockSize, 350)  # Set hawthorn position to below the goose
                else:
                    hawthorn_position = None  # Remove hawthorn position if not in the correct area
                    hawthorn_pop_visible = False  # Hide hawthorn popup

            # Place oak tree when Enter is pressed
            if event.key == pygame.K_RETURN and tree_position:
                planted_positions.append(tree_position)  # Add the position to the planted list
                oakCount += 1  # Increment count
                oak_pop_visible = True  # Show the oak popup image
                tree_position = None  # Remove visual tree
                plant_sound.play()  # Play planting sound

            # Place hawthorn tree when Enter is pressed
            if event.key == pygame.K_RETURN and hawthorn_position:
                planted_positions.append(hawthorn_position)  # Add the position to the planted list
                hawthornCount += 1  # Increment count
                hawthorn_pop_visible = True  # Show the hawthorn popup image
                hawthorn_position = None  # Remove visual tree
                plant_sound.play()  # Play planting sound

            # Hide info popup if the player moves
            info_pop_visible = False

        # Mouse events
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos 
            if info_x <= mouse_pos[0] <= info_x + 40 and info_y <= mouse_pos[1] <= info_y + 30:
                info_pressed_state = True 
                info_pop_visible = True  # Show the info popup
                info_sound.play()

        if event.type == pygame.MOUSEBUTTONUP:
            if info_pressed_state:
                info_pressed_state = False 

    # Fill the background
    screen.fill(BACKGROUND_COLOR)

    # Draw the grid
    drawGrid()

    # Greenery placeholder rectangle
    rect_width, rect_height = 400, 350
    rect_x, rect_y = 350, 350  # New coordinates for the rectangle
    pygame.draw.rect(screen, (255, 0, 0), (rect_x, rect_y, rect_width, rect_height))

    # Draw areas and player
    screen.blit(urban1, (u_x, u_y))
    screen.blit(greenery, (g_x, g_y))
    screen.blit(player, (player_x, player_y))
    
    # Show oak tree above the goose if at opening
    if tree_position:
        screen.blit(oak, tree_position)  # Show the visual tree above the goose

    # Check if the hawthorn position is set and draw it
    if hawthorn_position:
        screen.blit(hawthorn, hawthorn_position)  # Draw the hawthorn in its position

    # Show planted trees
    for spot in planted_positions:
        screen.blit(oak, spot)  # Draw the planted tree at the tracked position

    # Draw oak popup image if visible
    if oak_pop_visible:
        screen.blit(oakPop, (oakPopx, oakPopy))  # Display oak popup image at a specific position

    # Draw hawthorn popup image if visible
    if hawthorn_pop_visible:
        screen.blit(hawthornPop, (hawthornPopx, hawthornPopy))  # Display hawthorn popup image at a specific position

    # Draw info popup image if visible
    if info_pop_visible:
        screen.blit(infoPop, (oakPopx, oakPopy))  # Display info popup image at the same position as oakPop/hawthornPop

    if info_pressed_state:
        screen.blit(info_pressed, (info_x, info_y))  
    else:
        screen.blit(info_normal, (info_x, info_y)) 
    
    pygame.display.flip()
    
pygame.quit()
