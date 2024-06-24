import pygame
class Start:
   def __init__(self):
      self.run = True
      self.choice = 0
      self.pos = []
      self.accept = False
   def reset(self):
      self.run = True
      self.choice = 0
      self.pos = []
      self.accept = False
   def draw(self,win):
      win.blit(pygame.image.load('image/start/menu.jpg'),(0,0))
      if self.choice==1:win.blit(pygame.image.load('image/start/2x2_glow.png'),(0,0))
      else:win.blit(pygame.image.load('image/start/2x2.png'),(0,0))
      if self.choice==2:win.blit(pygame.image.load('image/start/3x3_glow.png'),(0,0))
      else:win.blit(pygame.image.load('image/start/3x3.png'),(0,0))
   def check_mouse_pos(self,checkx,checky):
      if (self.pos[0][0] in checkx)and(
         self.pos[0][1] in checky)and(
         self.pos[1][0] in checkx)and(
         self.pos[1][1] in checky):return True
      return False
   def key(self):
      for event in pygame.event.get():
         if event.type == pygame.QUIT:self.run = False
         elif event.type == pygame.MOUSEMOTION:
            xy = pygame.mouse.get_pos()
            if(xy[0] in range(274,360))and(xy[1] in range(277,377)):self.choice = 1
            elif(xy[0] in range(441,528))and(xy[1] in range(277,377)):self.choice = 2
            else:self.choice = 0
         elif event.type == pygame.MOUSEBUTTONDOWN:self.pos.append(pygame.mouse.get_pos())
         elif event.type == pygame.MOUSEBUTTONUP:
            try:
               self.pos.append(pygame.mouse.get_pos())
               if self.check_mouse_pos(range(274,360),range(277,377)) or self.check_mouse_pos(range(441,528),range(277,377)):self.accept = True;self.pos = []
               else:self.pos = []
            except:self.pos = []