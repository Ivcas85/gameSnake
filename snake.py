import pyglet
import random
from pyglet.window import key
from pathlib import Path

# input variables settings
SQUARE_SIZE = 64
count_x = 20
count_y = 12
WIDHT = count_x*SQUARE_SIZE
HEIGHT = count_y*SQUARE_SIZE
cornerX = (WIDHT/SQUARE_SIZE)-1
cornerY = (HEIGHT/SQUARE_SIZE)-3


# music and sounds settings
music = pyglet.resource.media('snake-tiles/green_anaconda.wav') # link:https://www.youtube.com/watch?v=F000UK_kUq4
looper = pyglet.media.SourceGroup(music.audio_format, None)
looper.loop = True
looper.queue(music)
p = pyglet.media.Player()
p.queue(looper)

bomb_sound = pyglet.resource.media('snake-tiles/bum.wav')
au_sound = pyglet.resource.media('snake-tiles/au.wav',streaming=False)
mouse_sound = pyglet.resource.media('snake-tiles/pisk.wav', streaming=False)

window = pyglet.window.Window(width=WIDHT, height=HEIGHT) # load window

# load images
TILES_DIRECTORY = Path('snake-tiles')
snake_tiles = {}
for path in TILES_DIRECTORY.glob('*.png'):
    snake_tiles[path.stem] = pyglet.image.load(path)


class SNAKE:
    "'Definition of class Snake, which contains settings for game and movement settings. '"
    def __init__(self):
        "' Definition of snake, mouse and other settings. '"
        self.skore = 0
        self.position =[(1, 0),(2,0),(3,0),(4,0)]
        self.direction = 1, 0
        self.live = True
        self.bomb = [(7,4)]
        self.static_bomb = [(0,0),(cornerX,cornerY)]
        self.mouse = []
        self.gameOver = [(cornerX/2.5,cornerY/2)]
        self.hedgehog = []
        self.add_some("mouse")
        self.add_some("bomb")
        self.add_some("hedgehog")
        self.height = (HEIGHT/SQUARE_SIZE)-2
        self.widht = (WIDHT/SQUARE_SIZE)
        self.directions = []

    def tik(self):
        "' Definition of snake movement. '"

        if not self.live:
            p.pause()
            return
        x, y = self.position[-1]


        a,b = self.direction

        append_x = x+a
        append_y = y+b

        if append_x <0:
            if append_y == self.height-1:
                append_x +=1
                append_y +=-1
                self.direction=0,-1
            else:
                append_x += 1
                append_y += 1
                self.direction=1,0
        if append_x == self.widht-1 and append_y == -1:
            append_x +=-1
            append_y +=1
            self.direction = -1,0
        if append_x == self.widht-1:
            if append_y == self.height-1 and self.direction == (0,1):
                append_x += -1
                append_y += 1
                self.direction = -1,0
            if append_y == self.height-1:
                append_x += -1
                append_y += 1
                self.direction = 0,-1
        if append_y <0:
            append_x += 1
            append_y += 1
            self.direction = 0,1

        if append_x >self.widht-1:
            if append_y == self.height and self.direction==(-1,0):
                append_x = append_x-1
                append_y += -1
                self.direction = 0,-1
            else:
                append_x += -1
                append_y += 1
                self.direction = -1,0
        if append_y > self.height-1:

            append_x += 1
            append_y += -1
            self.direction = 0,-1

        new_head = append_x, append_y

        if new_head in self.bomb or new_head in self.static_bomb:   # snake meet bomb
            self.live = False # play bomb sound
            bomb_sound.play()
        if new_head in self.position:  # snake bite itself
            self.live = False # play "au" sound
            au_sound.play()
        if new_head in self.hedgehog and len(self.position) == 2:
            self.live = False
            au_sound.play() # play "au" sound

        self.position.append(new_head)

        if new_head in self.mouse:
            self.skore += 1   # snake eat mouse
            self.mouse.remove(new_head)
            self.add_some("mouse")
            p.pause() # play "au" sound
            mouse_sound.play()
            p.play()

        elif new_head in self.hedgehog:
         # snake eat hedgehog
            self.skore = self.skore -1
            self.hedgehog.remove(new_head)
            self.add_some("hedgehog")
            del self.position[0:-2]
            p.pause()   # play "au" sound
            au_sound.play()
            p.play()

        else:
            del self.position[0]

    def add_some(self,object_name):
        "' Definition of new some position and counted score.'"
        for i in range(128):
            x = random.randrange(16)
            y = random.randrange(8)
            position = x, y
            if (position not in self.position) and (position not in self.mouse) and (position not in self.bomb) and (position not in self.static_bomb) and (position not in self.hedgehog):
                if object_name == "mouse":
                    self.mouse.append(position)
                    if len(self.mouse)>1:
                        del self.mouse[0]
                if object_name == "hedgehog":
                    self.hedgehog.append(position)
                    if len(self.hedgehog)>1:
                        del self.hedgehog[0]
                if object_name == "bomb":
                    self.bomb.append(position)
                    del self.bomb [0]
                return

@window.event
def on_key_press(sym,mod):
    "'User press key for setting snake direction.'"

    if sym == key.LEFT:

        snake.direction=-1,0
    elif sym ==key.RIGHT:
        snake.direction=1,0

    elif sym==key.UP:
        snake.direction=0,1
    elif sym ==key.DOWN:
        snake.direction=0,-1

def draw_text(text,font_size, x, y, anchor_x):
    text = pyglet.text.Label(
            text,
            font_name='Ariel',
            font_size=font_size,
            x=x, y=y, anchor_x=anchor_x)
    text.draw()

snake=SNAKE()
@window.event
def on_draw():
    "' Draw game in playfield. '"
    window.clear()


    draw_text("Ahoj, vítej v mém tak trochu jiném hadovi. Chutnají mu myši a za každou snězenou máš bod, ale když se střetne s ježkem, přijde o bod a tělo, případně o život.",
                font_size=12,
                x = 0,
                y = HEIGHT - 25,
                anchor_x="left"
                )
    draw_text("Když se pokouše nabo narazí na minu, hra končí. A neboj, had je ochočený - neuteče. Ale pozor, ve dvou rozích je mina-to abys nenechal hada běhat jen tak bez dozoru.",
                font_size=12,
                x = 0,
                y = HEIGHT - 50,
                anchor_x="left"
                )
    draw_text("Hra se ovládá se šipkami na klávesnici. Zapni si zvuk. Hezkou zábavu.",
                font_size=12,
                x = 0,
                y = HEIGHT - 75,
                anchor_x="left"
                )
    draw_text(150*"-",
                    font_size=30,
                    x=0,
                    y=HEIGHT - 130,
                    anchor_x="left")

    draw_text("Tvůj počet bodů je " + str(snake.skore) + " .",
                font_size=20,
                x = WIDHT/2,
                y = HEIGHT - 110,anchor_x="center"
                )

    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

    # Draw pictures in playfield
    snake.directions.clear()
    for index, xy in enumerate(snake.position[:-1]):
        snake.direction_x = snake.position[index+1][0] - xy[0]
        snake.direction_y = snake.position[index+1][1] - xy[1]
        snake.directions.append((snake.direction_x, snake.direction_y))


    snake.directions.append((0,1))

    dict_directions = {(0, 1): 'top', (0, -1): 'bottom', (1, 0): 'right', (-1, 0): 'left'}

    snake_tiles_names = []
    for index, dir in enumerate(snake.directions):
        if index == 0:
            dir_from = 'end'
        else:
            previous_to = snake_tiles_names[index - 1][1]
            if previous_to == 'top':
                dir_from = 'bottom'
            elif previous_to == 'bottom':
                dir_from = 'top'
            elif previous_to == 'right':
                dir_from = 'left'
            elif previous_to == 'left':
                dir_from = 'right'
        dir_to = dict_directions[dir]

        snake_tiles_names.append((dir_from,dir_to))

    snake_tiles_names[-1] = (snake_tiles_names[-1][0],'head')

    for index, (x,y) in enumerate(snake.position):
        source = snake_tiles_names[index][0]
        dest = snake_tiles_names[index][1]
        snake_tiles[source + "-" + dest].blit(
            x * SQUARE_SIZE, y * SQUARE_SIZE)

    for(x,y) in snake.mouse:
        snake_tiles['mouse'].blit(x*SQUARE_SIZE,y*SQUARE_SIZE)
    for (x,y) in snake.bomb:
        snake_tiles['bomb'].blit(x*SQUARE_SIZE,y*SQUARE_SIZE)
    for (x,y) in snake.static_bomb:
        snake_tiles['bomb'].blit(x*SQUARE_SIZE,y*SQUARE_SIZE)
    for (x,y) in snake.hedgehog:
        snake_tiles['hedgehog'].blit(x*SQUARE_SIZE,y*SQUARE_SIZE)
    if not snake.live:
        for (x,y) in snake.gameOver:
            snake_tiles['gameOver'].blit(x*SQUARE_SIZE,y*SQUARE_SIZE)


def tik(dt):
    snake.tik()
def tik_icons(dt):
    snake.add_some("bomb")
    snake.add_some("mouse")
    snake.add_some("hedgehog")

pyglet.clock.schedule_interval(tik, 1/3)
pyglet.clock.schedule_interval(tik_icons, 10/1)

p.play()    # play music
pyglet.app.run()
