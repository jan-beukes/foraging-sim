from compass import Compass
from custom import PathQueue
import math

class Entity:
    """
    Base class of entities
    """
    def __init__(self, row, col, speed, char):
        self.row = row 
        self.col = col
        self.speed = speed
        self.char = char
        self.compass = Compass(self.row, self.col, self.speed)
       
    # Entities that belong to a hive should implement
    # move()
    # update()
    
    def random_move(self, _map):
        """
        performs a random move given by entities compass
        """
        trajectory = self.compass.get_next_trajectory()
        distance = trajectory.get_distance()
        direction = trajectory.get_direction_in_radians()
        
        x = int(distance * round(math.cos(direction)))
        y = int(distance * round(math.sin(direction)))
        
        self.row = min(_map.size-1,max(self.row+y,0))
        self.col = min(_map.size-1,max(self.col+x,0))
    
    def move_to_target(self, _map, target):
        """
        move towards target's position with distance given by compass
        """
        trajectory = self.compass.get_next_trajectory()
        distance = trajectory.get_distance()
        x = 0
        y = 0
        # same row/col
        if self.row == target.row:
            x = distance if self.col < target.col else -distance
        elif self.col == target.col:
            y = distance if self.row < target.row else -distance
        # move diagonal
        elif target.row > self.row:
            x = distance if self.col < target.col else -distance
            y = distance
        else:
            x = distance if self.col < target.col else -distance
            y = -distance
            
        self.row = min(_map.size-1,max(self.row+y,0))
        self.col = min(_map.size-1,max(self.col+x,0))

class Bee(Entity):
    def __init__(self, row, col, speed, perception, hive):
        super().__init__(row, col, speed, 'b')
        self.perception = perception
        self.hive = hive
        self.searching = True
        self.target = None
        self.pollen = None
        
    def move(self, _map) -> bool:
        if not self.searching:
            self.move_to_target(_map, self.hive)
            return
        elif self.target and self.target.get_pollen_count() > 0:
            self.move_to_target(_map, self.target)
            return

        self.random_move(_map)

    def collect_pollen(self) -> bool:
        """
        Try to collect pollen from target flower
        return True if successful
        """
        if self.target and self.target.get_pollen_count() > 0:
            if self.row == self.target.row and self.col == self.target.col:
                # check fot fighting
                if self.target.active_bee_count <= self.target.get_pollen_count():
                    self.pollen = self.target.pop_pollen()
                    self.target = self.hive
                    self.searching = False
                    return True
                else:
                    self.prev_target = self.target # After fighting to not detect flower currently on
                    self.target = None
                    return False
        return False
   
    def update(self, flowers):
        self.prev_target = None
        
        # check if back to hive
        if not self.searching:
            if self.row == self.hive.row and self.col == self.hive.col:
                self.hive.add_pollen(self.pollen)
                self.pollen = None
                self.target = None
                self.searching = True
        # check if on flower
        elif self.collect_pollen():
            return
    
        closest_flower = None
        closest_distance = None
        for flower in flowers:  
            if flower.get_pollen_count() == 0 or flower is self.prev_target:
                continue
            # detecting flower in perception
            if self.searching and self.is_in_range(flower.row, flower.col):
                if closest_flower is None: 
                    closest_flower = flower
                    closest_distance = max(abs(self.row-flower.row), abs(self.col - flower.col))
                else:
                    # comparing flower priority
                    distance = max(abs(self.row-flower.row), abs(self.col - flower.col))
                    if distance < closest_distance:
                        closest_flower = flower
                        closest_distance = distance
                    elif distance == closest_distance:
                        if flower.row < closest_flower.row:
                            closest_flower = flower
                            closest_distance = distance
                            continue
                        if (flower.row == closest_flower.row and flower.col < closest_flower.col):
                            closest_flower = flower
                            closest_distance = distance
                            continue        
        if closest_flower:
            self.target = closest_flower
            self.collect_pollen() # handle bee currently on the new target
          
    def is_in_range(self, row, col):
        """
        returns True when position (row, col) is within perception 
        """
        if self.row - self.perception <= row <= self.row + self.perception:
            if self.col - self.perception <= col <= self.col + self.perception:
                return True
        return False      

class DesertBee(Entity):
    def __init__(self, row, col, speed, perception, hive):
        super().__init__(row, col, speed, 'd')
        self.perception = perception
        self.hive = hive
        self.searching = True
        self.target = None
        self.saved_flower = None
        self.pollen = None
        self.path = PathQueue()
    
    def move(self, _map):
        # hive is target
        if not self.searching:
            self.move_to_target(_map, self.hive)
        # flower is target
        elif self.target and self.target.get_pollen_count() > 0:
            self.move_to_target(_map, self.target)
            self.path.enqueue((self.row, self.col))
        # No target and searching
        elif self.searching and not self.saved_flower:
            self.random_move(_map)
            self.path.enqueue((self.row, self.col))
        # searching and has saved flower (following previous path)
        else:
            self.row, self.col = self.path.dequeue()

    def collect_pollen(self) -> bool:
        """
        Try to collect pollen from target flower
        return True if successful
        """
        if self.target and self.target.get_pollen_count() > 0:
            if self.row == self.target.row and self.col == self.target.col:
                # check for fighting
                if self.target.active_bee_count <= self.target.get_pollen_count():
                    self.pollen = self.target.pop_pollen()
                    self.saved_flower = self.target
                    self.target = self.hive
                    self.searching = False
                    return True
                else:
                    self.target = None
                    return False
        return False
    
    def update(self, flowers):
        # check if back to hive
        if not self.searching and self.target:
            if self.row == self.hive.row and self.col == self.hive.col:
                if self.pollen:
                    self.hive.add_pollen(self.pollen)
                self.pollen = None
                self.searching = True
                self.target = None

        # check if on flower when not following path
        elif not self.saved_flower and self.collect_pollen():
            return
        # Following path
        elif self.saved_flower:
            sflower = self.saved_flower
            if self.row == sflower.row and self.col ==  sflower.col:
                # check for fighting
                if sflower.active_bee_count <=  sflower.get_pollen_count():
                    self.pollen = sflower.pop_pollen()
                    self.target = self.hive
                    self.searching = False
                else:
                    self.target = self.hive
                    self.saved_flower = None
                    self.path.clear_queue()
                    self.searching = False
            return

        # Look for nearby flowers
        closest_flower = None
        for flower in flowers:  
            if flower.get_pollen_count() == 0:
                continue
            # detecting flower in perception
            if self.searching and self.is_in_range(flower.row, flower.col):
                if closest_flower is None: 
                    closest_flower = flower
                else:
                    closest_flower= self.get_closest_flower(flower, closest_flower)        
        if closest_flower:
            self.target = closest_flower
            self.collect_pollen() # handle bee currently on the new target

    def get_closest_flower(self, flower1, flower2):
        """
        returns the colest of the given flowers
        """
        distance1 = max(abs(self.row-flower1.row), abs(self.col - flower1.col))
        distance2 = max(abs(self.row-flower2.row), abs(self.col - flower2.col))

        if flower1 is None:
            return flower2, distance2
        if flower2 is None:
            return flower1, distance1

        if distance1 < distance2:
            return flower1
        elif distance1 == distance2:
            if flower1.row < flower2.row:
                return flower1
            if flower1.row == flower2.row and flower1.col < flower2.col:
                return flower1

        return flower2   

    def is_in_range(self, row, col):
        if self.row - self.perception <= row <= self.row + self.perception:
            if self.col - self.perception <= col <= self.col + self.perception:
                return True
        return False

class HoneyBee(Entity):
    def __init__(self, row, col, speed, perception, hive):
        super().__init__(row, col, speed, 'h')
        self.hive = hive
        self.target = None # not used by scout
        self.saved_flower = None
        self.scout = self.compass.is_scout()
        self.char = 's' if self.scout else 'f'
        self.perception = perception * 2 if self.scout else perception
        self.searching = self.scout
        self.pollen = None
        self.forager_search_remaining = 5
    
    def move(self, _map):
        # Forager
        if not self.scout:
            # Dormant
            if not self.searching and not self.target:
                return
            # move to saved flower or hive
            elif self.target and not self.searching:
                self.move_to_target(_map, self.target)
            # moving around flower
            elif self.searching and self.forager_search_remaining > 0:
                if self.target and  self.target.get_pollen_count() > 0:
                    self.move_to_target(_map, self.target)
                    self.forager_search_remaining -= 1              
                else:
                    self.random_move(_map)
                    self.forager_search_remaining -= 1
            else:
                self.target = self.hive
                self.searching = False
                self.move_to_target(_map, self.hive)            
        # Scout
        elif self.searching:
            self.random_move(_map)
        else:
            self.move_to_target(_map, self.hive)
          
    def collect_pollen(self) -> bool:
        """
        Try to collect pollen from target flower
        return True if successful
        """
        if self.row == self.target.row and self.col == self.target.col:
            if self.target.get_pollen_count() == 0:
                self.searching = True
                self.target = None
                return False   
            # check for fighting
            if self.target.active_bee_count <= self.target.get_pollen_count():
                self.pollen = self.target.pop_pollen()
                self.target = self.hive
                self.searching = False
                return True
            else:
                self.prev_target = self.target # After fighting to not detect flower currently on
                self.target = None
                self.searching = True
                return False
                
    def update(self, flowers):
        # Dormant forager
        if not self.scout and not self.target and not self.searching:
            return
        self.prev_target = None
        
        if self.scout:
            if not self.searching:
                if self.row == self.hive.row and self.col == self.hive.col:
                    self.hive.honey_bee_alert_foragers(self.saved_flower)
                    self.searching = True
                else:
                    return
        else:
            # Forager back to hive
            if self.target is self.hive:
                if self.row == self.hive.row and self.col == self.hive.col:
                    if self.pollen:
                        self.hive.add_pollen(self.pollen)
                    self.pollen = None
                    self.target = None
                    self.searching = False
                    self.forager_search_remaining = 5
                    return
                else:
                    return
            # Forager successfully collected pollen
            elif self.target and self.collect_pollen():
                return
            elif not self.searching and self.target:
                return

         # Look for nearby flowers
        closest_flower = None
        for flower in flowers:  
            if flower.get_pollen_count() == 0 or flower is self.prev_target:
                continue
            # detecting flower in perception
            if self.searching and self.is_in_range(flower.row, flower.col):
                if closest_flower is None: 
                    closest_flower = flower
                else:
                    closest_flower= self.get_closest_flower(flower, closest_flower)        

        if closest_flower and not self.scout:
            # When forager is searching for 5 iterations
            self.target = closest_flower
            self.collect_pollen() # handle bee currently on the new target
        elif closest_flower:
            self.saved_flower = closest_flower
            self.searching = False
  
    def alert_forager(self, flower):
        if self.scout: return
        if self.row != self.hive.row or self.col != self.hive.col: return
        if self.target is self.hive: return

        # set target to closest for double scout case
        self.target = self.get_closest_flower(flower, self.target)

    def get_closest_flower(self, flower1, flower2):
        """
        returns the colest of the given flowers
        """
        if flower1 is None:
            return flower2
        if flower2 is None:
            return flower1

        distance1 = max(abs(self.row-flower1.row), abs(self.col - flower1.col))
        distance2 = max(abs(self.row-flower2.row), abs(self.col - flower2.col))

        if distance1 < distance2:
            return flower1
        elif distance1 == distance2:
            if flower1.row < flower2.row:
                return flower1
            if flower1.row == flower2.row and flower1.col < flower2.col:
                return flower1

        return flower2
  
    def is_in_range(self, row, col):
        if self.row - self.perception <= row <= self.row + self.perception:
            if self.col - self.perception <= col <= self.col + self.perception:
                return True
        return False  
  
class Wasp(Entity):
    def __init__(self, row, col, speed):
        super().__init__(row, col, speed, 'w')

    def move(self, _map):
       self.random_move(_map)
    
    def update():
        pass
