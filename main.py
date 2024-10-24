# Quinten Reed
# U2 Project(?)
# Bear Fish River

from ecosystem import *
from time import sleep

DAYS_SIMULATED = 30
RIVER_SIZE = 15
START_BEARS = 10
START_FISH = 10

def BearFishRiver():

  r = River(RIVER_SIZE, START_BEARS, START_FISH)
  day = 0
  done = False
  while day < DAYS_SIMULATED and done == False:
    print(f"\n\nDay: {day+1}")
    print(r)
    print(f"Starting Population: {r.population} animals")
    done = r.new_day()
    print(f"Ending Population: {r.population} animals")
    print(r)
    day += 1
    sleep(1)

if __name__ == "__main__":
  BearFishRiver()