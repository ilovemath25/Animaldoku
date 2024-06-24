import pygame
class Loading:
   def __init__(self):
      self.run = True
      self.count = 0
   def reset(self):
      self.run = True
      self.count = 0
   def draw(self,win):
      win.blit(pygame.image.load('image/start/loading.jpg'),(0,0))
      pygame.draw.rect(win,(255,190,70),(207,329,34+7.06*self.count,34),border_radius=40)
      self.count+=1
   def key(self):
      for event in pygame.event.get():
         if event.type == pygame.QUIT:self.run = False