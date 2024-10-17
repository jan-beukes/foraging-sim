
class Hive():
    """
    The Hive class which is a home to all bee type objects
    """
    def __init__(self, row, col, n, char):
        self.row = row
        self.col = col
        self.char = char    
        self.entity_count = n
        self.entities = []
        self.pollen_list = []

    def add_entity(self, entity):
        self.entities.append(entity)
    
    def add_pollen(self, pollen):
        self.pollen_list.append(pollen)   
 
    def move_entities(self, _map):
        """
        moves all entities belonging to the hive and 
        updates their position on the map board
        """
        i = 0
        bees_killed = 0
        for entity in self.entities[:]:
            row, col = entity.row, entity.col
            entity.move(_map)

            if _map.map_board[entity.row][entity.col] in ('w', 'W'):
                self.entities.pop(i)
                _map.remove_from_board(row, col, entity.char)
                bees_killed += 1
            else: 
                _map.add_to_board(entity)
                _map.remove_from_board(row, col, entity.char)
                i += 1
        return bees_killed
    
    def update_entities(self, _map):
        """
        perform actions of all entities for the current iteration
        """
        for entity in self.entities:
            entity.update(_map.flowers)
            
    # used by Honey Bee hives to alert foragers
    def honey_bee_alert_foragers(self, flower):
        if self.char != 'H': return

        for entity in self.entities:
            entity.alert_forager(flower)

class WaspHive():
    """
    The WaspHive class manages Wasp objects
    """
    def __init__(self, row, col, n, char):
        self.row = row
        self.col = col
        self.char = char    
        self.entity_count = n
        self.entities = []
    
    def add_entity(self, entity):
        self.entities.append(entity)
    
    def move_entities(self, _map):
        """
        Move all wasps
        """
        for entity in self.entities:
            row, col = entity.row, entity.col
            entity.move(_map)
            _map.add_to_board(entity)
            _map.remove_from_board(row, col, entity.char)

class Flower:
    """
    Flower class which stores pollen for bees to collect
    """
    def __init__(self, row, col, pollen_type):
        self.char = 'F'
        self.row = row
        self.col = col
        self.pollen_type = pollen_type
        self.pollen_list = []
        self.active_bee_count = 0
        
    def add_pollen(self, pollen):
        self.pollen_list.append(pollen)
        
    def pop_pollen(self):
        """
        if the flower has pollen it removes it and returns it's value
        otherwise returns None
        """
        if len(self.pollen_list) > 0:
            self.active_bee_count -= 1
            return self.pollen_list.pop()
        else:
            return None
        
    def get_pollen_count(self):
        return len(self.pollen_list)

    def count_bees(self, hives):
        """
        set the active bee count to the current number of bees on the flower
        """
        self.active_bee_count = 0
        for hive in hives:
            for entity in hive.entities:
                if entity.pollen:
                    continue
                if entity.row == self.row and entity.col == self.col:
                    self.active_bee_count += 1
