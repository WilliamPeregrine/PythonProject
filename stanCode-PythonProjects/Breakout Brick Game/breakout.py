"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

To fet a better score o this game
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 10         # 100 frames per second
NUM_LIVES = 3			# Number of attempts


def main():
    graphics = BreakoutGraphics()

    # Add the animation loop here!
    while True:
        dx = graphics.get_dx()
        dy = graphics.get_dy()
        obj = graphics.check_collision()
        if obj is not None:
            graphics.rebounce(obj)
        # Update
        graphics.ball.move(dx, dy)
        # Check for collisions with walls
        if graphics.ball.x <= 0 or graphics.ball.x + graphics.ball.width >= graphics.window.width:
            graphics.set_dx()
        if graphics.ball.y <= 0:
            graphics.set_dy()
        # back to start point
        if graphics.ball.y + graphics.ball.height >= graphics.window.height:
            graphics.lose_life()
        # Pause
        pause(FRAME_RATE)


if __name__ == '__main__':
    main()

