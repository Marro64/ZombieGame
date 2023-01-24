import pygame
import sys
from AI.helpers.keyboard_handler import KeyboardHandler
from AI.maze import Maze
from AI.helpers.constants import Constants
from AI.search import Search
from zombie_spawner import ZombieSpawner
from hand_tracking.cursor import Cursor


class Game:
    """
    Initialize PyGame and create a graphical surface to write. Similar
    to void setup() in Processing
    """
    def __init__(self):
        pygame.init()
        self.size = (Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(self.size)
        self.keyboard_handler = KeyboardHandler()
        self.font = pygame.font.SysFont(pygame.font.get_fonts()[0], 64)
        self.time = pygame.time.get_ticks()
        self.maze = Maze(Constants.GRID_COLS, Constants.GRID_ROWS, self.size)
        self.maze.generate_open_maze()
        self.search = Search(self.maze)

        self.start = (0, 0)
        self.target = (-1, -1)
        # self.search.pathfind((0, 0), (-1, -1))
        self.zombie_spawner = ZombieSpawner(self.size, self.target, self.maze)

        self.cursor = Cursor(shooting_handler=self.zombie_spawner)

    """
    Method 'game_loop' will be executed every frame to drive
    the display and handling of events in the background. 
    In Processing this is done behind the screen. Don't 
    change this, unless you know what you are doing.
    """
    def game_loop(self):
        current_time = pygame.time.get_ticks()
        delta_time = current_time - self.time
        self.time = current_time
        self.cursor.update()
        self.handle_events()
        self.update_game(delta_time)
        self.draw_components()

    """
    Method 'update_game' is there to update the state of variables 
    and objects from frame to frame.
    """
    def update_game(self, dt):
        self.zombie_spawner.update(dt)

    """
    Method 'draw_components' is similar is meant to contain 
    everything that draws one frame. It is similar to method
    void draw() in Processing. Put all draw calls here. Leave all
    updates in method 'update'
    """
    def draw_components(self):
        self.screen.fill([255, 255, 255])
        self.maze.draw_maze(self.screen)
        self.search.draw_path(self.screen)
        self.zombie_spawner.draw(self.screen)
        self.cursor.draw(self.screen)
        pygame.display.flip()

    # def draw_score(self):
    #     text = self.font.render(str(self.search.target.distance), True, (0,0,0))
    #     self.screen.blit(text, (self.size[0]/2-64, 20))

    def reset(self):
        pass

    """
    Method 'handle_event' loop over all the event types and 
    handles them accordingly. 
    In Processing this is done behind the screen. Don't 
    change this, unless you know what you are doing.
    """
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.handle_key_down(event)
            if event.type == pygame.KEYUP:
                self.handle_key_up(event)
            if event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_pressed(event)
            if event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_released(event)

    """
    This method will store a currently pressed buttons 
    in list 'keyboard_handler.pressed'.
    """
    def handle_key_down(self, event):
        self.keyboard_handler.key_pressed(event.key)
        # if event.key == pygame.K_m:
        #     print("Generating Maze")
        #     self.maze.generate_maze()
        # if event.key == pygame.K_o:
        #     print("Generating Obstacle")
        #     self.maze.generate_obstacles()
        # if event.key == pygame.K_r:
        #     print("Generating Rooms")
        #     self.maze.generate_room()
        if event.key == pygame.K_e:
            print("Generating Empty")
            self.maze.generate_open_maze()
        # if event.key == pygame.K_b:
        #     print("BFS")
        #     self.search.breadth_first_solution()
        # if event.key == pygame.K_d:
        #     print("DFS")
        #     self.search.depth_first_solution()
        # if event.key == pygame.K_g:
        #     print("Greedy")
        #     self.search.greedy_search()
        if event.key == pygame.K_a:
            print("AStar")
            self.search.pathfind(self.start, self.target)
        # if event.key == pygame.K_x:
        #     print("Recursive DFS")
        #     self.search.depth_first_recursive()
        if event.key == pygame.K_p:
            self.cursor.print_debug()

    """
    This method will remove a released button 
    from list 'keyboard_handler.pressed'.
    """

    def handle_key_up(self, event):
        self.keyboard_handler.key_released(event.key)

    """
    Similar to void mouseMoved() in Processing
    """
    def handle_mouse_motion(self, event):
        pass

    """
    Similar to void mousePressed() in Processing
    """
    def handle_mouse_pressed(self, event):
        pass
        x = event.pos[0]
        y = event.pos[1]
        if event.button == 1:
            self.start = (x, y)
        if event.button == 3:
            self.target = (x, y)
        self.search.pathfind(self.start, self.target)

    """
    Similar to void mouseReleased() in Processing
    """
    def handle_mouse_released(self, event):
        pass


if __name__ == "__main__":
    game = Game()
    while True:
        game.game_loop()
