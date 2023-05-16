import pygame
from pygame import mixer
from player import Player

mixer.init()
pygame.init()

#create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BAZ")
clock = pygame.time.Clock()
FPS = 60
RED = (255, 0, 0)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

#variabel game
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]#player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

#player data
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

#music and sounds
pygame.mixer.music.load("assets/audio/548619__zhr__fighting-music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/86049__nextmaking__sword.aiff")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

#background image
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

#spritesheets and number of steps in each animation
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

#define font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)
gameover_font = pygame.font.Font("assets/fonts/turok.ttf", 50)

#function for drawing text
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#function for drawing background
def draw_bg():
  scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bg, (0, 0))

#function for drawing health bars and energy bars
def draw_health_bar(health, x, y):
  ratio = health / 100
  pygame.draw.rect(screen, BLACK, (x - 2, y - 2, 404, 34))
  pygame.draw.rect(screen, GREY, (x, y, 400, 30))
  pygame.draw.rect(screen, RED, (x, y, 400 * ratio, 30))

def energy_bar(energy, x_pos, y_pos):
    pygame.draw.rect(screen, BLACK, (x_pos-3, y_pos+7, 256, 26))
    pygame.draw.rect(screen, GREY, (x_pos, y_pos+10, 250, 20))
    pygame.draw.rect(screen, BLUE, (x_pos, y_pos+10, 250*(energy/100), 20))

#create two character
char1 = Player(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
char2 = Player(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

#game loop
run = True
while run:

  clock.tick(FPS)

  #draw background
  draw_bg()

  #show player stats
  draw_health_bar(char1._hp, 20, 20)
  draw_health_bar(char2._hp, 580, 20)
  energy_bar(char1._energy, 20, 60)
  energy_bar(char2._energy, 580, 60)
  draw_text("P1: " + str(score[0]), score_font, RED, 20, 95)
  draw_text("P2: " + str(score[1]), score_font, RED, 580, 95)

  #update countdown
  if intro_count <= 0:
    #move players
    char1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, char2, round_over)
    char2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, char1, round_over)
  else:
    #display count timer
    draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
    #update count timer
    if (pygame.time.get_ticks() - last_count_update) >= 1000:
      intro_count -= 1
      last_count_update = pygame.time.get_ticks()

  #update characters
  char1.update()
  char2.update()

  #draw characters
  char1.draw(screen)
  char2.draw(screen)

  #check for player defeat
  if round_over == False:
    if char1.alive == False:
      score[1] += 1
      round_over = True
      round_over_time = pygame.time.get_ticks()
    elif char2.alive == False:
      score[0] += 1
      round_over = True
      round_over_time = pygame.time.get_ticks()
  else:
    #display gameover text
    draw_text('Game Over', gameover_font, RED, 360, 150)
    if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
      round_over = False
      intro_count = 3
      char1 = Player(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
      char2 = Player(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  #update display
  pygame.display.update()

#exit pygame
pygame.quit()
