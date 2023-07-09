"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

TO BUILD UP THE BREAKOUT BRICK GAME
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
from campy.gui.events.timer import pause
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Width of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10        # Number of rows of bricks
BRICK_COLS = 10        # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 75      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                 paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                 brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                 brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                 brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing)
                                            - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a moving paddle
        self.paddle = GRect(paddle_width, paddle_height)
        self.paddle.filled = True
        self.window.add(self.paddle, x=(self.window.width-self.paddle.width)/2,
                        y=self.window.height-paddle_offset)

        onmousemoved(self.reset_position)  # reset_position is method

        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius*2, ball_radius*2)
        self.ball.filled = True
        self.window.add(self.ball, x=(self.window.width-self.ball.width)/2,
                        y=(self.window.height-self.ball.height)/2)

        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = 0

        # Set score system
        self.score = 0
        self.score_label = GLabel(f"Score: {self.score}")
        self.score_label.font = "-20"
        self.window.add(self.score_label, x=0, y=self.score_label.height+10)

        # Set lives system
        self.lives = 3
        self.lives_label = GLabel(f"Life: {self.lives}")
        self.lives_label.font = "-20"
        self.window.add(self.lives_label, x=self.window.width - 80, y=self.lives_label.height+10)

        onmouseclicked(self.start_fall)
        # Draw bricks
        color_num = 0
        colors = ["red", "orange", "yellow", "green", "blue"]
        for i in range(brick_rows):
            for j in range(brick_cols):
                    self.brick = GRect(brick_width, brick_height)
                    self.brick.filled = True
                    self.brick.fill_color = colors[color_num]
                    self.brick.color = colors[color_num]
                    self.window.add(self.brick, (brick_width + brick_spacing)*j,
                                    brick_offset + (brick_height + brick_spacing)*i)
            if i%2 != 0:  # change the brick color in odd line
                color_num += 1

    def reset_position(self, mouse):  # make the paddle slide
        self.paddle.x = mouse.x - self.paddle.width / 2
        self.paddle.y = self.window.height-PADDLE_OFFSET

    def start_fall(self, mouse):  # make the ball to fall
        self.__dy = INITIAL_Y_SPEED
        self.__dx = random.randint(1, MAX_X_SPEED)
        if random.random() > 0.5:
            self.__dx = - self.__dx

    def get_dx(self):
        return self.__dx

    def get_dy(self):
        return self.__dy

    def set_dx(self):
        self.__dx = - self.__dx

    def set_dy(self):
        self.__dy = - self.__dy

    def check_collision(self):  # check collision type
        global score
        for i in range(0,3,2):
            for j in range(0,3,2):
                object = self.window.get_object_at(self.ball.x+i*BALL_RADIUS, self.ball.y+j*BALL_RADIUS)
                if object is not None and object is not self.score_label:
                    return object

    def rebounce(self, obj):  # rebounce when collide
        if obj is self.paddle:
            self.ball.y = self.window.height - self.paddle.height - PADDLE_OFFSET - self.ball.height
            self.__dy = - self.__dy
        else:
            self.window.remove(obj)
            self.__dy = - self.__dy
            self.score += 1
            self.score_label.text = f"Score: {str(self.score)}"

    def lose_life(self):  # Show bouncing "GAME OVER"
        self.lives -= 1
        self.lives_label.text = f"Life: {self.lives}"
        # move ball back to center of screen
        self.ball.x = (self.window.width - self.ball.width) / 2
        self.ball.y = (self.window.height - self.ball.height) / 2
        self.__dy = 0
        self.__dx = 0
        if self.lives == 0:
            game_over_label = GLabel("GAME OVER", x=self.window.width - 300, y=40)
            game_over_label.font = "-20"
            game_over_label.color = "Red"
            self.window.add(game_over_label)
            vx = 20
            while True:
                game_over_label.move(vx, 0)
                if game_over_label.x <= 80 or game_over_label.x >= self.window.width - 360:
                    vx = -vx
                pause(200)

