"""
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.py to edit this template
 """

import pygame
import random
import sys
import os
import math

# --- CONFIGURATION ---
TILE_SIZE = 32
GRID_WIDTH = 25
GRID_HEIGHT = 15
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE

# Aesthetic Colors
COLOR_PLAYER = (231, 76, 60)
COLOR_GOAL = (46, 204, 113)
COLOR_TEXT_MAIN = (0, 255, 255)
COLOR_BUTTON = (52, 152, 219)
COLOR_BUTTON_HOVER = (41, 128, 185)
COLOR_INPUT_ACTIVE = (255, 255, 255)
COLOR_INPUT_IDLE = (100, 100, 100)

class ProceduralGame:
    def __init__(self):
        pygame.init()
        # Creating the screen object for the game window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Setting the caption for the game window
        pygame.display.set_caption("Procedural Map Explorer")
        
        # Clock object maker for the time
        self.clock = pygame.time.Clock()
        
        # State of the game
        self.state = "MENU"
        # String that holds the user input for seed
        self.user_text = ""
        # Boolean to check if input box is clicked
        self.input_active = False
        # String that holds the active seed
        self.current_seed = ""
        # int for the movement speed delay
        self.move_delay = 0 
        
        # Font object for the main text
        self.font = pygame.font.SysFont("Consolas", 24, bold=True)
        # Font object for the title text
        self.title_font = pygame.font.SysFont("Consolas", 48, bold=True)
        # Font object for the smaller text
        self.small_font = pygame.font.SysFont("Consolas", 18)
        
        # Creating file path for the MapImages folder
        script_dir = os.path.dirname(__file__) 
        
        # Loading in the cobblestoneWall.png texture
        self.wall_texture = self._load_tex(os.path.join(script_dir, "MapImages", "cobblestoneWall.png"))
        # Loading in the dirtFloor.png texture
        self.floor_texture = self._load_tex(os.path.join(script_dir, "MapImages", "dirtFloor.png"))

        # level counter
        self.level = 1

    # Method that loads the texture images
    def _load_tex(self, path):
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        except Exception as e:
            return None

    # Method that starts the game and handles the seed
    def start_game(self):
        # Creating the seed from the user_text input
        self.current_seed = self.user_text if self.user_text else str(random.randint(1000, 9999))
        # Setting the random seed
        random.seed(self.current_seed)
        self.level = 1
        # Calling the method to make the level
        self.generate_level()
        self.state = "GAME"

    # Method that creates the grid for the map
    def generate_level(self):
        # Array that holds the grid map noise
        self.grid = [[1 if random.random() < 0.45 else 0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        # For loop to run the smoothing logic 5 times
        for _ in range(5): self._smooth()
        # Calling method to place player and goal
        self._place_entities()

    # Method to smooth out the wall neighbors
    def _smooth(self):
        new_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                count = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0: continue
                        nx, ny = x + i, y + j
                        if nx < 0 or ny < 0 or nx >= GRID_WIDTH or ny >= GRID_HEIGHT or self.grid[ny][nx] == 1:
                            count += 1
                new_grid[y][x] = 1 if count > 4 else 0
        self.grid = new_grid

    # Method that places the player and the goal in open floors
    def _place_entities(self):
        # Array that holds the available floor tiles
        floors = [(x, y) for y in range(GRID_HEIGHT) for x in range(GRID_WIDTH) if self.grid[y][x] == 0]
        if len(floors) < 2: self.generate_level(); return
        # Picking random floor index for player
        self.p_x, self.p_y = random.choice(floors)
        # Picking random floor index for goal
        self.g_x, self.g_y = random.choice(floors)

    # Method to check for key being held down for movement
    def handle_continuous_movement(self):
        if self.move_delay > 0:
            self.move_delay -= 1
            return

        # Getting the key that is being pressed
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        
        if keys[pygame.K_w]: dy = -1
        elif keys[pygame.K_s]: dy = 1
        elif keys[pygame.K_a]: dx = -1
        elif keys[pygame.K_d]: dx = 1

        if dx != 0 or dy != 0:
            nx = self.p_x + dx
            ny = self.p_y + dy
            # Checking to see if next tile is a floor
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and self.grid[ny][nx] == 0:
                self.p_x, self.p_y = nx, ny
                self.move_delay = 7 

    # Method to draw the main menu screen
    def draw_menu(self):
        self.screen.fill((25, 25, 25))
        # Printing out the title text
        title = self.title_font.render("CAVE EXPLORER", True, COLOR_TEXT_MAIN)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 60))
        
        # Creating the rectangle object for the input box
        self.input_rect = pygame.Rect(SCREEN_WIDTH//2 - 150, 190, 300, 50)
        box_color = COLOR_INPUT_ACTIVE if self.input_active else COLOR_INPUT_IDLE
        pygame.draw.rect(self.screen, box_color, self.input_rect, 2, border_radius=5)
        
        # Printing out the user_text string
        text_surf = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surf, (self.input_rect.x + 10, self.input_rect.y + 10))

        # Mouse position object
        mouse_pos = pygame.mouse.get_pos()
        # Creating the rectangle object for the play button
        self.button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 300, 200, 60)
        btn_color = COLOR_BUTTON_HOVER if self.button_rect.collidepoint(mouse_pos) else COLOR_BUTTON
        pygame.draw.rect(self.screen, btn_color, self.button_rect, border_radius=10)
        
        play_txt = self.font.render("PLAY", True, (255, 255, 255))
        self.screen.blit(play_txt, (self.button_rect.centerx - play_txt.get_width()//2, self.button_rect.centery - play_txt.get_height()//2))
        pygame.display.flip()

    # Method to draw the actual game map and textures
    def draw_game(self):
        # Nested for loop to draw the tiles
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pos = (x * TILE_SIZE, y * TILE_SIZE)
                # Drawing the floor texture
                if self.floor_texture: self.screen.blit(self.floor_texture, pos)
                # Drawing the wall texture if grid is 1
                if self.grid[y][x] == 1 and self.wall_texture: 
                    self.screen.blit(self.wall_texture, pos)
        
        # Float maker for the pulsing portal effect
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 6
        # Drawing the goal rectangle
        pygame.draw.rect(self.screen, COLOR_GOAL, (self.g_x*TILE_SIZE+4-pulse/2, self.g_y*TILE_SIZE+4-pulse/2, TILE_SIZE-8+pulse, TILE_SIZE-8+pulse), border_radius=4)
        
        # Drawing the player circle
        pygame.draw.circle(self.screen, COLOR_PLAYER, (self.p_x*TILE_SIZE + 16, self.p_y*TILE_SIZE + 16), 12)
        
        # Printing out the level depth counter
        depth_txt = self.font.render(f"DEPTH: {self.level}0m", True, COLOR_TEXT_MAIN)
        self.screen.blit(depth_txt, (10, 10))

        # Printing out the controls for menu and quit
        controls_txt = self.small_font.render("ESC: Menu | Q: Quit", True, (180, 180, 180))
        self.screen.blit(controls_txt, (10, SCREEN_HEIGHT - 30))

        # Printing out the active seed counter
        seed_disp = self.small_font.render(f"SEED: {self.current_seed}", True, (180, 180, 180))
        self.screen.blit(seed_disp, (SCREEN_WIDTH - seed_disp.get_width() - 10, SCREEN_HEIGHT - 30))
        
        pygame.display.flip()

    # Main run method that handles the game loop
    def run(self):
        while True:
            # Main for loop to check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                
                # Global quit key logic for Q
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    pygame.quit(); sys.exit()

                # Checking to see if in MENU state
                if self.state == "MENU":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.input_active = self.input_rect.collidepoint(event.pos)
                        if self.button_rect.collidepoint(event.pos): self.start_game()
                    if event.type == pygame.KEYDOWN and self.input_active:
                        if event.key == pygame.K_BACKSPACE: self.user_text = self.user_text[:-1]
                        elif event.key == pygame.K_RETURN: self.start_game()
                        else: 
                            if len(self.user_text) < 15: self.user_text += event.unicode
                
                # Checking to see if in GAME state
                elif self.state == "GAME":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = "MENU"

            if self.state == "MENU":
                # Calling the draw_menu method
                self.draw_menu()
            else:
                # Calling continuous movement method
                self.handle_continuous_movement()
                # Checking to see if player reached the goal
                if (self.p_x, self.p_y) == (self.g_x, self.g_y):
                    self.level += 1
                    self.generate_level()
                # Calling the draw_game method
                self.draw_game()
            
            # Setting the FPS to 60
            self.clock.tick(60)

# Main runner for the game class
if __name__ == "__main__":
    ProceduralGame().run()