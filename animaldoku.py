import pygame
import os
from src.start import Start
from src.codeh import Sudoku
from src.loading import Loading
from src.time_game import time_game
pygame.init()
win = pygame.display.set_mode((800,550))
pygame.display.set_caption('animaldoku')
run = True
in_loading = True
in_start = False
in_game = False
newgame = False
start = Start()
loading = Loading()
seconds = 0
pos = []
os.system('cls')
bgm = pygame.mixer.music.load('music/bgm.wav')
while run:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:run = False
   if in_loading:
      pygame.time.delay(20)
      loading.draw(win)
      loading.key()
      if loading.count==52:
         pygame.time.delay(1000)
         in_start = True
         in_loading = False
         if not newgame:pygame.mixer.music.play(-1)
   elif in_start:
      start.draw(win)
      start.key()
      run = start.run
      if start.accept:
         sudoku = Sudoku(start.choice+1)
         start_ticks = pygame.time.get_ticks()
         in_game = True
         in_start = False
   elif in_game:
      if not(sudoku.won):
         seconds=(pygame.time.get_ticks()-start_ticks)/1000
         sudoku.win()
      sudoku.draw(win,time_game(int(seconds)))
      sudoku.key()
      run = sudoku.run
      if sudoku.newgame:
         newgame = sudoku.newgame
         in_loading = True
         in_start = False
         in_game = False
         loading.reset()
         start.reset()
   pygame.display.update()
pygame.quit()