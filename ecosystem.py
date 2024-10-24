from random import randint

# I have not figured out how to make them not overlap, even though I tried everything that I thought would fix it
# But it's 10:49 PM and I have to go to bed
# I am annoyed I couldn't fix it
# 11:14 PM: I'm noticing other issues but it's probably going to take too long to fix everything

class River():
  def __init__(self, size, num_bears, num_fish):
    self.river = [["🟦 " for i in range(size)] for i in range(size)]
    self.size = size
    self.animals = []
    self.population = 0

    self.__initial_population(num_bears, num_fish)
    self.redraw_cells()

  def __str__(self):
    final = ""
    for i in range(self.size):
      str_line = ""

      for j in range(self.size):
        str_line += str(self.river[i][j])
      
      final += str_line + "\n"

    return final# + f"Population is {self.population}, there are {len([jtem for i in range(len(self.river)) for jtem in self.river[i] if jtem != '🟦 '])} on-screen"

  def __getitem__(self, y):
    if y < 0 or y >= self.size:
      raise IndexError("invalid index")
    
    return self.river[y]

  def __initial_population(self, num_bears, num_fish):
    for i in range(num_bears):
      x = randint(0, self.size-1)
      y = randint(0, self.size-1)

      while self.river[y][x] != "🟦 ":
        x = randint(0, self.size-1)
        y = randint(0, self.size-1)

      item = Bear(x, y, self.population)
      print(self.population, len(self.animals))

      self.river[y][x] = item
      self.animals.append(item)
      self.population += 1

    for i in range(num_fish):
      x = randint(0, self.size-1)
      y = randint(0, self.size-1)

      while self.river[y][x] != "🟦 ":
        x = randint(0, self.size-1)
        y = randint(0, self.size-1)

      item = Fish(x, y, self.population)
      print(self.population, len(self.animals))

      self.river[y][x] = item
      self.animals.append(item)
      self.population += 1

  def place_baby(self, baby):
    for item in baby:
      self.river[item.y][item.x] = item
      self.animals.append(item)
      self.population += 1

  def animal_death(self, other):
    for i, item in enumerate(self.animals):
      if item is other:
        del self.animals[i]

    for i in range(self.size):
      for j, jtem in enumerate(self.river[i]):
        if jtem is other:
          self.river[i][j] = "🟦 "
    
    self.population -= 1
    print(self.population, len(self.animals))

  def redraw_cells(self):
    for i in range(self.size):
      for j in range(self.size):
        self.river[i][j] = "🟦 "

    for item in self.animals:
      self.river[item.y][item.x] = item

  # Figured this would help
  def animal_move(self, item):
    #if self.river[item.y][item.x] is item:
    #  self.river[item.y][item.x] = "🟦 "

    x = item.x + randint(-1, 1)
    y = item.y + randint(-1, 1)

    if x >= self.size:
      x = self.size-1
    elif x < 0:
      x = 0

    if y >= self.size:
      y = self.size-1
    elif y < 0:
      y = 0

    while x == 0 and y == 0 or self.river[y][x] !=  "🟦 ":
      x = item.x + randint(-1, 1)
      y = item.y + randint(-1, 1)

      if x >= self.size:
        x = self.size-1
      elif x < 0:
        x = 0

      if y >= self.size:
        y = self.size-1
      elif y < 0:
        y = 0

    item.move(x, y, self)

  def new_day(self):
    for item in self.animals:
      self.animal_move(item)

    children = []

    self.redraw_cells()

    for item in self.animals:
      for jtem in self.animals:
        if item.x == jtem.x and item.y == jtem.y:
          new_child = item.collision(jtem, self)
          self.animal_move(jtem)

          if new_child != None:
            children.append(new_child)

    self.place_baby(children)

    return self.population >= self.size**2

class Animal():
  def __init__(self, x, y, debug_id):
    self.x = x
    self.y = y
    self.debug_id = debug_id
    self.bred_today = False

  def death(self, river):
    river.animal_death(self)

  def move(self, x, y, river):
    self.x = x
    self.y = y

  def collision(self, other, river):
    if type(self) == type(other) and self.bred_today == False and other.bred_today == False and self is not other:
      x = randint(0, river.size-1)
      y = randint(0, river.size-1)

      while river.river[y][x] != "🟦 ":
        x = randint(0, river.size-1)
        y = randint(0, river.size-1)
        print(river.river[y][x], self.debug_id, other.debug_id)

      self.bred_today = True
      other.bred_today = True
      
      print(river.population, len(river.animals))
      return type(self)(x, y, river.population)

    elif type(self) == "Fish" and type(other) == "Bear":
      other.consume(self, river)

    elif type(self) == "Bear" and type(other) == "Fish":
      self.consume(other, river)

class Fish(Animal):
  def __init__(self, x, y, debug_id):
    super().__init__(x, y, debug_id)

  def __str__(self):
    return "🐟 "#str(self.debug_id).zfill(2)

class Bear(Animal):
  def __init__(self, x, y, debug_id):
    super().__init__(x, y, debug_id)
    self.max_lives = 7
    self.lives = 7
    self.eaten_today = False

  def __str__(self):
    return "🐻 "#str(self.debug_id).zfill(2)

  def starve(self, river):
    if self.eaten_today == False:
      if self.lives <= 0:
        self.death(river)
      else:
        self.lives -= 1

  def consume(self, fish, river):
    fish.death(river)
    self.lives = self.max_lives