class WumpusWorld:
  def __init__(self, blocks, pits, gold, wumpus, initial_location):
    self.initial_location = initial_location    # 최초 위치 복사
    self.wumpus = wumpus
    self.pits = pits
    self.gold = gold
    self.blocks = blocks
    self.player = self.initial_location #agent의 위치
    self.has_arrow = True
    self.arrow = int(3)
    self.has_gold = False
    self.visited = list()



    self.breeze = {}    # 바람이 부는 좌표 저장
    self.stench = {}    # 냄새가 나는 좌표 저장
    
    for p in self.pits: # 바람이 부는 좌표 초기화
      for l in self.neighbours(p):
        self.breeze[l] = True
    for w in self.wumpus: # 냄새가 나는 좌표 초기화
      for l in self.neighbours(w):
        self.stench[l] = True
      
      
  def neighbours(self, loc):    #이웃 좌표를 tuple loc = (x,y) 형태로 return
    return [(loc[0]+1,loc[1]), (loc[0]-1,loc[1]), (loc[0],loc[1]+1), (loc[0],loc[1]-1)]

  def arrow_hits(self, location, dx, dy): # 화살이 명중했을 때
    while location not in self.blocks:
      location = (location[0]+dx, location[1]+dy)
      if location in self.wumpus:
        print("Scream")
        return True
    return False
  
  def print(self):            # 상태 프린트 (useful for debugging)
    print(self.player)
    self.visited.append(self.player)
    xmin = min([x for x,y in self.blocks])
    xmax = max([x for x,y in self.blocks])
    ymin = min([y for x,y in self.blocks])
    ymax = max([y for x,y in self.blocks])
    for y in range(ymin, ymax+1):
      for x in range(xmin, xmax+1): 
        
        if (x,ymax-y) in self.blocks:
          print('B',end='')
        elif (x,ymax-y) in self.wumpus:
          print('W',end='')
        elif (x,ymax-y) in self.pits:
          print('P',end='')
        elif (x,ymax-y) in self.gold:
          print('G',end='')
        elif self.player == (x, ymax - y):
          print('Y',end='')
        else:
          print(' ',end='')
      print("")
    b = self.player in self.breeze       # is their square breezy?
    s = self.player in self.stench       # is it smelly?
    print("arrow: " + str(self.arrow))
    print("breezy: " + str(b))
    print("stenchy: " + str(s))
    print("has gold: " + str(self.has_gold))
    

  def visited(self):
    print(self.visited) 

  def sim(self, agent):   #판별
    t = 0
    self.has_arrow = True
    self.player = self.initial_location
    while t < 1000: 
      t+=1

      self.print()

      b = self.player in self.breeze       # is their square breezy?
      s = self.player in self.stench       # is it smelly?
      agent.give_senses(self.player, b, s)  # give the agent its senses
      action = agent.get_action()       # get the agents action
      print(action, end='\n\n')

      new_location = self.player
      if action == 'MOVE_UP':             # action에 따른 agent의 location 재지정
        new_location = (self.player[0], self.player[1]+1)
      elif action == 'MOVE_DOWN':
        new_location = (self.player[0], self.player[1]-1)
      elif action == 'MOVE_LEFT':
        new_location = (self.player[0]-1,self.player[1])
      elif action == 'MOVE_RIGHT':
        new_location = (self.player[0]+1,self.player[1])
      elif not self.has_arrow and action[0:5] == 'SHOOT':  # 화살을 쏘기 전, 화살 보유 여부 판독
        return 'NO ARROW'
      elif action == 'SHOOT_UP':                      # check to see if the agent killed the wumpus
        if self.arrow_hits(self.player, 0, 1):
          self.wumpus = {}
          agent.killed_wumpus()
      elif action == 'SHOOT_DOWN':
        if self.arrow_hits(self.player, 0, -1):
          self.wumpus = {}
          agent.killed_wumpus()
      elif action == 'SHOOT_LEFT':
        if self.arrow_hits(self.player, -1, 0):
          self.wumpus = {}
          agent.killed_wumpus()
      elif action == 'SHOOT_RIGHT':
        if self.arrow_hits(self.player, 1, 0):
          self.wumpus = {}
          agent.killed_wumpus()
      elif action == 'QUIT':
        return 'QUIT'


      if action[0:5] == 'SHOOT':      # 화살 개수 관리
        self.arrow = self.arrow - 1
        if self.arrow <= 0:
          self.has_arrow = False

      if new_location in self.pits:   # check if fell into a pit
        return 'FELL'
      if new_location in self.wumpus: # check if eaten by wumpus
        return 'EATEN'
      if new_location in self.gold:   # check if found gold
        self.has_gold = True

        visited_set = set(self.visited)
        self.visited = list(visited_set)
        print(self.visited)
        #여기에 agent에 gohome() 함수 추가하기
        return 'GOLD'

      if new_location not in self.blocks: # 죽으면 원래 자리로 복귀
        self.player = new_location