import pygame
import random
import copy
class Sudoku:
   num = {str(i):pygame.image.load('image/number/'+str(i)+'.png') for i in range(1,10)}
   num2 = {str(i):pygame.image.load('image/number/2x2/'+str(i)+'.png') for i in range(1,5)}
   def __init__(self,n):
      self.n = n
      self.m = '1' if self.n==3 else '2'
      self.run = True
      self.newgame = False
      self.pos = []
      self.put = []
      self.grid,self.solved = self.generateboard(n)
      self.board = copy.deepcopy(self.grid)
      self.writenum = '1'
      self.tool = 'write'
      self.count = [0]
      self.won = False
      while self.countSolutions()>1:
         self.grid,self.solved = self.generateboard(n)
         self.board = copy.deepcopy(self.grid)
      self.grid = copy.deepcopy(self.board)
      self.button = {
         'eraser':[527,103,83,75,pygame.image.load('image/eraser.png')],
         'write':[611,103,83,75,pygame.image.load('image/write.png')],
         'notes':[695,103,83,75,pygame.image.load('image/notes.png')],
         'number':[518,200,275,275,pygame.image.load('image/number/number'+self.m+'.png')],
         'num_list':{str(j*3+i+1):[i*91+518+i,j*91+200+j,91,91] for j in range(3) for i in range(3)},
         'board1':[12,22,497,497],'board2':[67,77,386,386],
         'new game':[475,287,140,60]
      }
      self.boxposx = {'1':[[12+i*55,12+(i+1)*55] for i in range(n**2)],'2':[[67+i*96,67+(i+1)*96] for i in range(n**2)]}
      self.boxposy = {'1':[[22+i*55,22+(i+1)*55] for i in range(n**2)],'2':[[77+i*96,77+(i+1)*96] for i in range(n**2)]}
   def isSafe(self,row, col, num):
      for x in range(self.n**2):
         if self.grid[row][x] == num:return False
      for x in range(self.n**2):
         if self.grid[x][col] == num:return False
      startRow = row - row % self.n
      startCol = col - col % self.n
      for i in range(self.n):
         for j in range(self.n):
            if self.grid[i + startRow][j + startCol] == num:return False
      return True
   def solveSudoku(self, row, col):
      if (row == self.n**2 - 1 and col == self.n**2):
         self.count[0] += 1
         return
      if col == self.n**2:
         row += 1
         col = 0
      if self.grid[row][col] > 0:
         self.solveSudoku(row, col + 1)
         return
      for num in range(1, self.n**2 + 1, 1):
         if self.isSafe(row, col, num):
            self.grid[row][col] = num
            self.solveSudoku(row, col + 1)
            self.grid[row][col] = 0
   def countSolutions(self):
      self.count = [0]
      self.solveSudoku(0, 0)
      return self.count[0]
   def generateboard(self,n):
      rows  = [ g*n + r for g in random.sample(range(n),n) for r in random.sample(range(n),n)]
      cols  = [ g*n + c for g in random.sample(range(n),n) for c in random.sample(range(n),n)]
      nums  = random.sample(range(1,n*n+1),n*n)
      board = [[nums[(self.n*(r%self.n)+r//self.n+c)%(self.n**2)] for c in cols] for r in rows]
      solve = copy.deepcopy(board)
      empties = int(n**4 * 0.6)
      for p in random.sample(range(n**4),empties):board[p//n**2][p%n**2] = 0
      return board,solve
   def transparent_blit(self,win,image,x,y,opacity):
      temp = image.copy()
      temp.set_alpha(opacity)
      win.blit(temp,(x,y))
   def win(self):
      if self.grid == self.solved:
         self.count = [0]
         self.won = True
   def check_mouse_pos(self,keyword,check):
      if (self.pos[0][0] in range(check[keyword][0],check[keyword][0]+check[keyword][2]))and(
         self.pos[0][1] in range(check[keyword][1],check[keyword][1]+check[keyword][3]))and(
         self.pos[1][0] in range(check[keyword][0],check[keyword][0]+check[keyword][2]))and(
         self.pos[1][1] in range(check[keyword][1],check[keyword][1]+check[keyword][3])):return True
      return False
   def draw(self,win,time):
      if not(self.won):
         win.blit(pygame.image.load('image/bg.jpg'),(0,0))
         win.blit(pygame.font.SysFont('comicsans',30,True).render(time,1,(0,0,0)),(595,49))
         for row,line in enumerate(self.board):
            for col,num in enumerate(line):
               if num==0:continue
               else:
                  if self.n==3:
                     self.transparent_blit(win,pygame.transform.scale(pygame.image.load('image/selected.png'),(55,55)),self.boxposx[self.m][row][0],self.boxposy[self.m][col][0],100)
                     win.blit(self.num[str(num)],(self.boxposx[self.m][row][0],self.boxposy[self.m][col][0]))
                  elif self.n==2:
                     self.transparent_blit(win,pygame.transform.scale(pygame.image.load('image/selected.png'),(96,96)),self.boxposx[self.m][row][0],self.boxposy[self.m][col][0],100)
                     win.blit(pygame.transform.scale(self.num2[str(num)],(96,96)),(self.boxposx[self.m][row][0],self.boxposy[self.m][col][0]))
         for row,line in enumerate(self.grid):
            for col,num in enumerate(line):
               if num==0:continue
               elif isinstance(num,int):
                  if self.n==3:win.blit(self.num[str(num)],(self.boxposx[self.m][row][0],self.boxposy[self.m][col][0]))
                  elif self.n==2:win.blit(pygame.transform.scale(self.num2[str(num)],(96,96)),(self.boxposx[self.m][row][0],self.boxposy[self.m][col][0]))
               elif isinstance(num,list):
                  notes = [num[i:i+3] for i in range(0,len(num),self.n)]
                  for r2,l2 in enumerate(notes):
                     for c2,n2 in enumerate(l2):
                        if n2==0:continue
                        else:
                           if self.n==3:win.blit(pygame.transform.scale(self.num[str(n2)],(18,18)),(self.boxposx[self.m][row][0]+r2*18,self.boxposy[self.m][col][0]+c2*18))
                           elif self.n==2:win.blit(pygame.transform.scale(self.num[str(n2)],(32,32)),(self.boxposx[self.m][row][0]+r2*32,self.boxposy[self.m][col][0]+c2*32))
         self.transparent_blit(win,self.button['eraser'][4],self.button['eraser'][0],self.button['eraser'][1],118)
         self.transparent_blit(win,self.button['write'][4],self.button['write'][0],self.button['write'][1],118)
         self.transparent_blit(win,self.button['notes'][4],self.button['notes'][0],self.button['notes'][1],118)
         win.blit(self.button[self.tool][4],(self.button[self.tool][0],self.button[self.tool][1]))
         win.blit(self.button['number'][4],(self.button['number'][0],self.button['number'][1]))
         if(self.n==2):win.blit(pygame.image.load('image/frame2.png'),(67,77))
         elif(self.n==3):win.blit(pygame.image.load('image/frame1.png'),(12,22))
         win.blit(pygame.image.load('image/selected.png'),(self.button['num_list'][self.writenum][0],self.button['num_list'][self.writenum][1]))
         if self.put!=[]:
            if self.n==3:
               if self.board[(self.put[0]-12)//55][(self.put[1]-22)//55] == 0:
                  if self.tool == 'eraser':
                     self.grid[(self.put[0]-12)//55][(self.put[1]-22)//55] = 0
                     self.put = []
                  elif self.tool == 'write':
                     win.blit(pygame.image.load('image/number/'+self.writenum+'.png'),(self.put[0],self.put[1]))
                     self.grid[(self.put[0]-12)//55][(self.put[1]-22)//55] = int(self.writenum)
                     self.put = []
                  elif self.tool == 'notes':
                     if self.grid[(self.put[0]-12)//55][(self.put[1]-22)//55]==0:self.grid[(self.put[0]-12)//55][(self.put[1]-22)//55] = [0 for _ in range(self.n**2)]
                     if isinstance(self.grid[(self.put[0]-12)//55][(self.put[1]-22)//55],int):self.put = []
                     else:
                        if self.grid[(self.put[0]-12)//55][(self.put[1]-22)//55][int(self.writenum)-1] == 0:self.grid[(self.put[0]-12)//55][(self.put[1]-22)//55][int(self.writenum)-1] = int(self.writenum)
                        else:self.grid[(self.put[0]-12)//55][(self.put[1]-22)//55][int(self.writenum)-1] = 0
                     self.put = []
               else:self.put = []
            elif self.n==2:
               if self.board[(self.put[0]-67)//96][(self.put[1]-77)//96] == 0:
                  if self.tool == 'eraser':
                     self.grid[(self.put[0]-67)//96][(self.put[1]-77)//96] = 0
                     self.put = []
                  elif self.tool == 'write':
                     win.blit(pygame.image.load('image/number/'+self.writenum+'.png'),(self.put[0],self.put[1]))
                     self.grid[(self.put[0]-67)//96][(self.put[1]-77)//96] = int(self.writenum)
                     self.put = []
                  elif self.tool == 'notes':
                     if self.grid[(self.put[0]-67)//96][(self.put[1]-77)//96]==0:self.grid[(self.put[0]-67)//96][(self.put[1]-77)//96] = [0 for _ in range(self.n**2)]
                     if isinstance(self.grid[(self.put[0]-67)//96][(self.put[1]-77)//96],int):self.put = []
                     else:
                        if self.grid[(self.put[0]-67)//96][(self.put[1]-77)//96][int(self.writenum)-1] == 0:self.grid[(self.put[0]-67)//96][(self.put[1]-77)//96][int(self.writenum)-1] = int(self.writenum)
                        else:self.grid[(self.put[0]-67)//96][(self.put[1]-77)//96][int(self.writenum)-1] = 0
                     self.put = []
               else:self.put = []
      elif self.won:
         pygame.time.delay(0)
         self.transparent_blit(win,pygame.image.load('image/win.png'),0,0,self.count[0])
         self.transparent_blit(win,pygame.image.load('image/new_game.png'),0,0,self.count[0])
         self.transparent_blit(win,pygame.font.SysFont('comicsans',30,True).render(time,1,(0,0,0)),475,170,self.count[0])
         if self.count[0]==0:win.blit(pygame.transform.scale(pygame.image.load('image/selected.png'),(800,800)),(0,0))
         for row,line in enumerate(self.solved):
            for col,num in enumerate(line):
               if self.n==3:self.transparent_blit(win,pygame.transform.scale(self.num[str(num)],(33.31,33.31)),self.boxposx[self.m][row][0]*0.603+94,self.boxposy[self.m][col][0]*0.603+96,self.count[0])
               elif self.n==2:self.transparent_blit(win,pygame.transform.scale(self.num[str(num)],(74.62,74.62)),self.boxposx[self.m][row][0]*0.7773+48,self.boxposy[self.m][col][0]*0.7773+48,self.count[0])
         if(self.n==2):self.transparent_blit(win,pygame.transform.scale(pygame.image.load('image/frame2.png'),(300,300)),100,110,self.count[0])
         elif(self.n==3):self.transparent_blit(win,pygame.transform.scale(pygame.image.load('image/frame1.png'),(300,300)),100,110,self.count[0])
         if self.count[0]<255:self.count[0]+=15
         self.transparent_blit(win,pygame.image.load('image/excellent.png'),-10,0,self.count[0])
   def key(self):
      for event in pygame.event.get():
         if event.type == pygame.QUIT:self.run = False
         elif event.type == pygame.MOUSEBUTTONDOWN:self.pos.append(pygame.mouse.get_pos())
         elif event.type == pygame.MOUSEBUTTONUP:
            self.pos.append(pygame.mouse.get_pos())
            try:
               if not(self.won):
                  if (self.check_mouse_pos('eraser',self.button)):self.tool = 'eraser';self.pos = []
                  elif (self.check_mouse_pos('write',self.button)):self.tool = 'write';self.pos = []
                  elif (self.check_mouse_pos('notes',self.button)):self.tool = 'notes';self.pos = []
                  elif (self.check_mouse_pos('number',self.button)):
                     for num in self.button['num_list'].items():
                        if self.n==3:
                           if(self.check_mouse_pos(num[0],self.button['num_list'])):self.writenum = num[0];self.pos = [];break
                        elif self.n==2:
                           if(self.check_mouse_pos(num[0],self.button['num_list']))and(num[0] in ['1','2','3','4']):self.writenum = num[0];self.pos = [];break
                     self.pos = []
                  elif(self.n==3)and(self.check_mouse_pos('board1',self.button)):
                     for x in self.boxposx[self.m]:
                        for y in self.boxposy[self.m]:
                           if(self.pos[0][0]in range(x[0],x[1]))and(self.pos[1][0]in range(x[0],x[1]))and(
                              self.pos[0][1]in range(y[0],y[1]))and(self.pos[1][1]in range(y[0],y[1])):self.put = [x[0],y[0]]
                     self.pos = []
                  elif(self.n==2)and(self.check_mouse_pos('board2',self.button)):
                     for x in self.boxposx[self.m]:
                        for y in self.boxposy[self.m]:
                           if(self.pos[0][0]in range(x[0],x[1]))and(self.pos[1][0]in range(x[0],x[1]))and(
                              self.pos[0][1]in range(y[0],y[1]))and(self.pos[1][1]in range(y[0],y[1])):self.put = [x[0],y[0]]
                     self.pos = []
                  else:self.pos = []
               elif self.won:
                  if (self.check_mouse_pos('new game',self.button)):self.newgame = True
                  else:self.pos = []
            except:self.pos = []
if __name__=='__main__':
   sudoku = Sudoku(2)
   print('2x2')
   for line in sudoku.grid:print(line)
   sudoku = Sudoku(3)
   print('3x3')
   for line in sudoku.grid:print(line)