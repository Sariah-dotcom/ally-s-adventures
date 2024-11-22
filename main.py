import pygame
import random

pygame.init()
pygame.mixer.init()

# Create game window
screen_width = 500
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ally's Adventures")

# Background
backgroundImg = pygame.image.load('images/background.png')

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
coral = (255, 207, 157)

# Background Music
pygame.mixer.music.load('music/arcade.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

# Load alien player image and positions
alienImg = pygame.image.load('images/alien.png')
playerX = 150
playerY = 430
playerX_change = 0

def alien(playerX, playerY):
    screen.blit(alienImg, (playerX, playerY))

# Load obstacle images
obstacleImgs = [
    pygame.image.load('images/obstacles/obstacle1.png'),
    pygame.image.load('images/obstacles/obstacle2.png'),
    pygame.image.load('images/obstacles/obstacle3.png'),
    pygame.image.load('images/obstacles/obstacle4.png'),
    pygame.transform.scale(pygame.image.load('images/obstacles/obstacle5.png'), (150,150)),
    pygame.transform.scale(pygame.image.load('images/obstacles/obstacle6.png'), (150,150)),
    pygame.transform.scale(pygame.image.load('images/obstacles/obstacle7.png'), (150,150)),
    pygame.image.load('images/obstacles/obstacle8.png'),
]

# Obstacle initialization
obstacle = {"img": None, "x": 0, "y": 0, "speed": 0}
used_images = set()

def reset_obstacle():
    """Create a new obstacle with random properties."""
    global used_images

    # Pick a random obstacle image ensuring all are used eventually
    unused_images = list(set(obstacleImgs) - used_images)
    if not unused_images:  # If all images are used, reset the tracker
        used_images.clear()
        unused_images = obstacleImgs

    img = random.choice(unused_images)
    used_images.add(img)

    x = random.randint(3, 460)  # Random x position across the screen width
    y = random.randint(-200, -50)  # Start above the screen
    speed = random.uniform(5, 10)  # Random speed

    return {"img": img, "x": x, "y": y, "speed": speed}

# Initialize the first obstacle
obstacle = reset_obstacle()

def draw_obstacle(obstacle):
    screen.blit(obstacle["img"], (obstacle["x"], obstacle["y"]))

# Splash screen
def splash_screen():
    """Display the splash screen and wait for the user to press any key."""
    while True:
        screen.fill(coral)
        titleImg = pygame.image.load('images/title.png')
        promptImg = pygame.image.load('images/prompt.png')
        planetImg = pygame.image.load('images/obstacles/obstacle8.png')
        screen.blit(titleImg, (30, 20))
        screen.blit(promptImg, (30, 500))
        screen.blit(planetImg, (170, 300))

        pygame.display.update()

        #Wait for key press
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                return  # Exit the splash screen and start the game

# Story
def story():
    screen.fill(white)
    font_path = 'DarkerGrotesque-VariableFont_wght.ttf'
    font = pygame.font.Font(font_path, 20)

    # Story text
    story_text = ("Once upon a galaxy far, far away, Ally the alien set her sights on Earth for the ultimate vacation. "
                  "She quickly fell in love with Earth’s charm—flowers and bouncy balls!"
                  " But oh, the Earthlings’ generosity went a bit too far! Showers of flowers and balls filled the skies wherever Ally wandered."
                  " Help Ally stay light on her feet and make the most of her earthly adventure!"
                  )

    # Split the text into multiple lines to fit the screen width
    words = story_text.split()
    lines = []
    current_line = ""
    max_width = screen_width - 40  # Add some padding

    for word in words:
        # Check if adding the word would make the line too long
        if font.size(current_line + word)[0] < max_width:
            current_line += word + " "
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)  # Add the last line

    # Display the lines on the screen
    y_offset = 100  # Starting y position for text
    for line in lines:
        text_surface = font.render(line.strip(), True, black)
        screen.blit(text_surface, (20, y_offset))  # Align text with padding
        y_offset += font.size(line)[1] + 10  # Move to the next line with spacing

    promptImg = pygame.image.load('images/prompt.png')
    screen.blit(promptImg, (30, 500))

    pygame.display.update()

    # Wait for a key press
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                return  # Exit the story screen

# Game over screen
def game_over():

    """Display the game over screen and wait for the user to press any key to replay."""
    screen.fill(coral)
    font_path = 'DarkerGrotesque-VariableFont_wght.ttf'
    font = pygame.font.Font(font_path, 70)
    text = font.render("GAME OVER", True, black)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, 120))

    '''Display final score'''
    score_text = font.render(f"Final Score: {score}", True, black)
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 220))

    promptImg = pygame.image.load('images/prompt.png')
    screen.blit(promptImg, (30, 500))

    # Game over sound effect
    pygame.mixer.music.load('music/game-over.mp3')
    pygame.mixer.music.play()

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                return  # Exit the game over screen
            
# Reset game
def reset_game():
    """Reset game state variables and restart background music."""
    global playerX, playerY, playerX_change, obstacle, score

    # Reset player position and obstacle
    playerX = 150
    playerY = 430
    playerX_change = 0
    obstacle = reset_obstacle()

    # Reset the score
    score = 0

    # Restart background music
    pygame.mixer.music.load('music/arcade.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

# Main game loop
def main_game():
    global playerX, playerY, playerX_change, obstacle, score, font_path

    font_path = 'DarkerGrotesque-VariableFont_wght.ttf'

    score = 0
    clock = pygame.time.Clock()

    running = True
    while running:
        # Background
        screen.blit(backgroundImg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Player movement on key press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -8
                elif event.key == pygame.K_RIGHT:
                    playerX_change = 8

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        # Draw player and obstacles
        alien(playerX, playerY)
        draw_obstacle(obstacle)

        # Update player position
        playerX += playerX_change

        # Prevent player from moving off screen
        if playerX <= 0:
            playerX = 0
        elif playerX >= screen_width - alienImg.get_width():
            playerX = screen_width - alienImg.get_width()

        # Update obstacle position
        obstacle["y"] += obstacle["speed"]

        # Reset obstacle when it goes off the screen
        if obstacle["y"] > screen_height:
            obstacle = reset_obstacle()

        # Detect collision
        player_rect = pygame.Rect(playerX, playerY, alienImg.get_width(), alienImg.get_height())
        obstacle_rect = pygame.Rect(obstacle["x"], obstacle["y"], obstacle["img"].get_width(),
                                    obstacle["img"].get_height())

        if player_rect.colliderect(obstacle_rect):
            game_over()
            return 
        
        # Update and display the score
        score += 1
        font = pygame.font.Font(font_path, 40)
        score_text = font.render(f"Score: {score}", True, black)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(60)

        pygame.display.update()

game_play = 0

while True:
    #Show splash screen and story once
    if game_play == 0:
        splash_screen()
        story()
        game_play +=1
    else:   
        main_game()    
        game_over() 
        reset_game()     
pygame.quit()