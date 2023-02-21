# RAY-CASTING DEMO #
### Video Demo: ###
### Description:

Upon completing CS50X, for better understanding of programming itself, I decided to took CS50P as well. As my final project, I decided to explore technique of ray-casting using Pygame library.

Ray casting is first popularized by Wolfenstein 3D in 1992. Followed by DOOM, these two games could today be considered the "godfather" of all FPS genre.

My imports are limited to pygame, math and sys --to exit the program safely. After initializing the pygame module, I had to set a constant variable for conversion of one degree in radian, which will be used while casting rays later --because math library returns values in radian.

First class is Settings, where I decided to store basic game settings, which are size of the window --resolution, the main background color, which is light-grey and lastly the title of the window.

Second class is Game, where the actual prototype is run. First function is for initializing the class, where I set screen of pygame application, display title and set clock and font for the FPS counter.

FPS counter works by getting FPS from pygame class function get_fps and display it on screen via font.render and screen.blit. The tick is set to 60.

The main function of game class is where the main loop is. First, I initialized the player, then created the main loop to check if game is terminated via pygame quit --in which case program exits with sys.exit. Later in the loop window is filled with background color, game_map is initialized and drawn, as well as player and rays to cast. Along with player movement function and FPS counter, just before updating display inside the loop.

The player function is where I handled many things. The class initialization contains player color in the mini-map and initial position, which are yellow and 300, 300 --respectively. The initial angle of the player is upwards, and delta of x and y --the movement variables-- are set to 1.5 times of the cos and sin of the player angle, since the returned values of which are rather small.

The draw function of player class draws the player and the angle player faces.

Check_wall function returns the index of the block player is facing, block that is behind the player, as well as the block to their left and right. The map is a list of 64 elements, where every 9th element is the beginning of a new row. So assuming that player is at block number 10 and facing up: the block they are facing is number 2, behind them are block 18, to their left and right 7 and 9 respectively.

In the later move function, with the help of check_wall function, the map information (list) is checked. If any given block's number is 0, then the player is allowed to move with W, A, S and D. With right and left arrows, player angle shifts. These formulas are where used the most of the research on the topic: Youtube (https://www.youtube.com/watch?v=gYRrGTC7GtA&ab_channel=3DSage) and Internet (https://www.pygame.org/project/3919).

Next function within the class is cast_rays. It loads the game_map to access the list where the positions will be checked. Initial ray angle is set to player angle minus 30 degrees, which will cause the rays to be cast 30 degrees to player's left and 30 to their right. (Radian to degree conversion constant is used here) First two if statements check and keep the ray angle within circle. The following for loop casts 60 rays. Depth of field variable limits the ray check, prevents the infinite loop. Then I set two variables to store the distance of shortest ray, for both cases, being horizontal and vertical. Since the ray casting method itself requires an above average understanding of math and trigonometry, most of the conditions, conversions and variables later on are implemented from aforementioned online second sources. The fundamental understanding I gained through documentations, allowed me to imitate a basic C code for ray-casting into python using pygame library, and solve the minor errors derive from the difference between two languages. I later optimized the code for what I had in mind when I started implementing my demo version of ray-casting. 

Based on the length of the rays that are casted from the player towards the wall --checked with the block being either 1 or 0 on game_map-- number of straight lines are back-to-back casted to the right side of the screen. The longer the ray travels without being interrupted by a wall, the shorter it is projected to the right --since the wall is further away from the player's perspective. Shorter the ray, longer the projection --which means the wall is closer to the player's perspective.

Depending on whether the distance calculated by a vertical, or horizontal grid on the map --using trigonometry-- the wall color is slightly darker or bright white. Which simulates a basic concept of shadows and different lightnings.

One problem of a simple ray-casting engine such as this one arises --since math-- when the player is close to the wall. Rays casted from the center of the player are shorter. Because rays to the left and the right travel diagonally. This is known as the fish-eye effect and can be solved in our situation by readjusting each rays distance ever so slightly by subtracting from the player angle. If the found angle exceeds the two pi --360 degrees in radian-- then it is readjusted again. Finally the distance of the ray is set to previous distance times cosines of this calculated angle. Maximum wall height is fixed to 320, per screen resolution, and some offset is given to center the projection to the middle of the right side of the screen. At the end of every iteration of the loop, degree increases by one, and checked again if it is in the 2 times pi (or 360 degrees).

Last function of player class is used to calculate hypotenuse, which is then used to find the shortest ray. There already is a built in hypotenuse function on the math library, but I could not get it to work and decided to implement my own.

Last class is map, Where the map is drawn according to the layout defined in initializing function of the class. Each block size is eight by eight. After initialization, map is drawn to the screen by two nested for loops, one of which is for x axis and the other is for y axis --width and height.
