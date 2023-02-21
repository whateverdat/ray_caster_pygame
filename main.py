import sys, pygame
from math import cos, sin, tan, pi, sqrt
pygame.init()

# One degree in radians, to cast rays one degree apart
DR = 0.0174533


class Settings:
    """Game Settings"""

    # Set screen Resolution
    size = width, height = 1024, 512

    # Set background color rgb, grey
    background = 75, 75, 75

    # Set title
    title = "Ray-Casting Demo"


class Game:
    """Game class to store game functions"""

    # Main game settings
    def __init__(self):

        # Initialize screen and set title
        self._screen = pygame.display.set_mode(Settings.size)
        pygame.display.set_caption(Settings.title)

        # Initilize font
        self._font = pygame.font.SysFont("Arial" , 18 , bold = True)

        # Initilize clock for FPS counter
        self._clock = pygame.time.Clock()

    # Function to count and set fps
    def fps_counter(self, screen):

        fps = str(int(self._clock.get_fps()))
        fps_text = self._font.render(fps, 1, pygame.Color("RED"))
        screen.blit(fps_text,(530,0))
        self._clock.tick(60)

    # Initilize game
    def main(self):

        # Create player
        player = Player()

        # Main loop
        while True:
            for event in pygame.event.get():

                # Quit condition
                if event.type == pygame.QUIT: sys.exit()
                
            # Fill background
            self._screen.fill(Settings.background)

            # Draw map
            game_map = Map()
            game_map.draw(self._screen)
            
            # Draw player
            player.draw(self._screen)
            player.cast_rays(self._screen)
            player.move()

            # Fps counter
            game.fps_counter(self._screen)

            # Update display to the screen
            pygame.display.flip()


class Player:
    """Draw player"""

    # Player color and intial x y
    def __init__(self):
        self._color = 255, 255, 0
        self._x, self._y = 300, 300

        # Initial angel is set upwards, 
        # I think beause I divide the angles on the player movement function, the formula is backwards
        # Up should be PI / 2, yet it is 3 * PI / 2
        self._angle = 3 * pi / 2
        self._delta_x = cos(self._angle) * 1.5
        self._delta_y = sin(self._angle) * 1.5
        
    # "Screen" is for pygame display variable
    def draw(self, screen):

        # Player
        pygame.draw.circle(screen, self._color, (self._x, self._y), 6)

        # Line to represent the direction player is facing
        pygame.draw.line(screen, "RED", (self._x, self._y), (self._x + self._delta_x * 10, self._y + self._delta_y * 10), 2)

    # Returns the block index of sepcific blocks
    def check_wall(self, key):
        map_x = int()
        map_y = int()
        
        # Return the wall player is facings 
        if key == "w":

            # Get the current block player is facing
            map_x = int(self._x + self._delta_x * 10) >> 6
            map_y = int(self._y + self._delta_y * 10) >> 6
            return (map_y * 8 + map_x) 

        if key == "s":

             # Get the current block behind the player
            map_x = int(self._x + self._delta_x * -10) >> 6
            map_y = int(self._y + self._delta_y * -10) >> 6
            return (map_y * 8 + map_x)  

        if key == "d":

            # Current block right to the player
            map_x = int(self._x + self._delta_y * -10) >> 6
            map_y = int(self._y + self._delta_x * 10) >> 6
            
            return (map_y * 8 + map_x) 

        # For some reason when I store map_x in a variable, it always returns zero,
        # So I fixed it by retuning the value immediately, without ever storing, yet the formula is similar
        if key == "a":
            # map_X = int(self._x - self._delta_y * -10) >> 6
            # map_y = int(self._y - self._delta_x * 10) >> 6
            # print("map_y: ", map_y)
            # print("map_x: ", map_x)
            # print("Wrong: ", int(self._y - self._delta_x * 10) >> 6)
            # print("calculate: ", map_y * 8 + map_x)
            return ((int(self._y - self._delta_x * 10) >> 6) * 8 + (int(self._x - self._delta_y * -10) >> 6))
        

    # Movement
    def move(self):

        # Load game map to check walls
        game_map = Map()
        map_layout = game_map.get_map()

        # W check for wall
        facing_block = self.check_wall("w")

        # S check for wall
        behind_block = self.check_wall("s")

        # A check for wall
        left_block = self.check_wall("a")

        # D check for wall 
        right_block = self.check_wall("d")
    

        # Decetc keys
        keys = pygame.key.get_pressed()

        
        # WASD movement 
        if keys[pygame.K_w] and map_layout[facing_block] == 0:

            self._x += self._delta_x
            self._y += self._delta_y

        if keys[pygame.K_s] and map_layout[behind_block] == 0:

            self._x -= self._delta_x
            self._y -= self._delta_y

        if keys[pygame.K_a] and map_layout[left_block] == 0:
            
            self._x += self._delta_y
            self._y -= self._delta_x

        if keys[pygame.K_d] and map_layout[right_block] == 0:
            
            self._y += self._delta_x
            self._x -= self._delta_y

            
        # Change player facing direction: adjusted formula from "5:45" "https://www.youtube.com/watch?v=gYRrGTC7GtA&ab_channel=3DSage"
        if keys[pygame.K_LEFT]:
            
            self._angle -= 0.05
            if self._angle < 0:
                self._angle += 2 * pi
            self._delta_x = cos(self._angle) * 1.5
            self._delta_y = sin(self._angle) * 1.5
            

        if keys[pygame.K_RIGHT]:

            self._angle += 0.05
            if self._angle > 2 * pi:
                self._angle -= 2 * pi
            self._delta_x = cos(self._angle) * 1.5
            self._delta_y = sin(self._angle) * 1.5


    # Cast and draw rays
    def cast_rays(self, screen):

        # Load game map to check walls
        game_map = Map()
        map_layout = game_map.get_map()

        # Ray angle will initially be equal to player angle minus 30 degrees
        # With each ray casted, value will increase by a degree
        ray_angle = self._angle - DR * 30

        # If condition to keep the ray angle within range
        if ray_angle < 0:
            ray_angle += 2 * pi

        if ray_angle > 2 * pi:
            ray_angle -= 2 * pi
        
        # Cast 60 rays
        for rays in range(60):

            # Depth of field, how many grids will be checked
            depth_of_field = 0

            # Variable to store the shortest distance, which initially is set to a high value 
            horizontal_distance = 100000

            # To store the info of the shortest ray
            horizontal_x = self._x
            horizontal_y = self._y

            # Tan of the ray angle
            a_tan = -1 / tan(ray_angle)

            # Horizontal ray "https://www.youtube.com/watch?v=gYRrGTC7GtA&ab_channel=3DSage"
            if ray_angle > pi:
                ray_y = ((int(self._y)>>6)<<6)-0.0001
                ray_x = (self._y - ray_y) * a_tan + self._x
                y_offset = -64
                x_offset = -y_offset * a_tan
            if ray_angle < pi:
                ray_y = ((int(self._y)>>6)<<6) + 64
                ray_x = (self._y - ray_y) * a_tan + self._x
                y_offset = 64
                x_offset = -y_offset * a_tan
            if ray_angle == 0 or ray_angle == pi:
                ray_x = self._x
                ray_y = self._y
                depth_of_field = 8
            while depth_of_field < 8:
                map_x = int(ray_x)>>6
                map_y = int(ray_y)>>6
                map_position = map_y * 8 + map_x
                if map_position > 0 and map_position < 8 * 8 and map_layout[map_position] == 1:
                    horizontal_x = ray_x
                    horizontal_y = ray_y
                    horizontal_distance = Player.shortest_ray(self._x, self._y, horizontal_x, horizontal_y, ray_angle)
                    depth_of_field = 8
                else:
                    ray_x += x_offset
                    ray_y += y_offset
                    depth_of_field += 1

            # Vertical ray "https://www.youtube.com/watch?v=gYRrGTC7GtA&ab_channel=3DSage"
            depth_of_field = 0
            vertical_distance = 100000
            vertical_x = self._x
            vertical_y = self._y

            # Negative tan of the ray angle
            n_tan = -tan(ray_angle)

            if ray_angle > pi / 2 and ray_angle < 3 * pi / 2:
                ray_x = ((int(self._x)>>6)<<6)-0.0001
                ray_y = (self._x - ray_x) * n_tan + self._y
                x_offset = -64
                y_offset = -x_offset * n_tan
            if ray_angle < pi / 2 or ray_angle > 3 * pi / 2:
                ray_x = ((int(self._x)>>6)<<6) + 64
                ray_y = (self._x - ray_x) * n_tan + self._y
                x_offset = 64
                y_offset = -x_offset * n_tan
            if ray_angle == 0 or ray_angle == pi:
                ray_y = self._y
                ray_x = self._x
                depth_of_field = 8
            while depth_of_field < 8:
                map_x = int(ray_x)>>6
                map_y = int(ray_y)>>6
                map_position = map_y * 8 + map_x
                if map_position > 0 and map_position < 8 * 8 and map_layout[map_position] == 1:
                    vertical_x = ray_x
                    vertical_y = ray_y
                    vertical_distance = Player.shortest_ray(self._x, self._y, vertical_x, vertical_y, ray_angle)
                    depth_of_field = 8
                else:
                    ray_x += x_offset
                    ray_y += y_offset
                    depth_of_field += 1

            # Determine whether horizontal or vertical ray, depending on the distance
            # Store the x and y of the whichever ray that is the shortest
            if vertical_distance < horizontal_distance:
                ray_x = vertical_x
                ray_y = vertical_y

                # Set a color variable to create different color of walls depending on the wall projection 
                # This will simulate shadows as vertical projected walls will be white
                color = (255, 255, 255)

                # Store distance to draw the walls
                distance = vertical_distance

            # If the shortest ray is horizontal
            if horizontal_distance < vertical_distance:
                ray_x = horizontal_x
                ray_y = horizontal_y

                # Horizontal projected walls will be grey
                color = (155, 155, 155)

                # Store distance to draw the walls
                distance = horizontal_distance

            # Cast ray
            pygame.draw.line(screen, (0, 255, 0), (self._x, self._y), (ray_x, ray_y) , 1) 

            # Account for fish-eye effect (Where the center of the wall becomes larger as you get closer)
            # It is due to center rays being shorter, when walls are close 
            # "https://www.youtube.com/watch?v=gYRrGTC7GtA&ab_channel=3DSage"
            ca = self._angle - ray_angle

            if ca < 0:
                ca += 2 * pi

            if ca > 2 * pi:
                ca -= 2 * pi

            # Update new angle
            distance = distance * cos(ca)

            # Draw 3D walls
            line_height = (64 * 320) / distance

            if line_height > 320:
                line_height = 320

            # Line offset, to center the lines on the screen
            line_offset = 160 - line_height / 2

            # Draw walls
            pygame.draw.lines(screen, color, True, [(rays * 8+530, line_offset),(rays * 8+530, line_height + line_offset)] , 8) 

            # Increase degree
            ray_angle += DR

            # Check if new value is within range
            if ray_angle < 0:
                ray_angle += 2 * pi

            if ray_angle > 2 * pi:
                ray_angle -= 2 * pi 

    # Custom hypothenus function to calculate the length of the shortest ray,
    # Distance between the wall and the player 
    def shortest_ray(ax, ay, bx, by, ang):
        return ( sqrt((bx - ax) * (bx-ax) + (by - ay) * (by - ay)) )   
                    

class Map:
    """"Draw map"""

    # Map specifications and layout
    def __init__(self):

        # Grid divisons and size
        self._map_x = 8
        self._map_y = 8
        self._block_size = 64

        # Map
        self._map = [ 
            1, 1, 1, 1, 1, 1, 1, 1, 
            1, 0, 1, 0, 0, 1, 0, 1,
            1, 0, 1, 0, 0, 1, 0, 1,
            1, 0, 1, 0, 0, 0, 0, 1,
            1, 0, 1, 1, 0, 0, 0, 1,
            1, 0, 0, 1, 0, 1, 0, 1,
            1, 0, 0, 0, 0, 0, 0, 1,
            1, 1, 1, 1, 1, 1, 1, 1,
        ]

    # Draw map
    def draw(self, screen):

        # Set some variables for cleaner syntax on loop
        size = self._block_size
        game_map = self._map
        map_x = self._map_x
        map_y = self._map_y
        
        # Loop to render map, x and y axis
        for x in range(0, self._map_x):
            for y in range(0, self._map_y):

                # Algorithm to check map list and render map layout "4:33" "https://www.youtube.com/watch?v=gYRrGTC7GtA&ab_channel=3DSage"
                if game_map[y * map_x + x] == 1:
                    # Square sizes are block_size -1 to render a grid
                    rect = pygame.Rect(x * size, y * size, size - 1, size - 1) 
                    # White color, solid block
                    pygame.draw.rect(screen, (255, 255, 255), rect, size) 

                else:
                    # Square sizes are block_size -1 to render a grid
                    rect = pygame.Rect(x * size, y * size, size - 1, size - 1) 
                    # Black color, open area
                    pygame.draw.rect(screen, (0, 0, 0), rect, size) 

    def get_map(self):
        return self._map


# Run main game function
if __name__ == "__main__":
    game = Game()
    game.main()