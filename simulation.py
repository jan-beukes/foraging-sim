import stdio
import stdarray

from objects import Flower, Hive
from custom import MergeSort
import gui

class Map:
    """
    Map class handles the board and the objects in the simulation
    """
    def __init__(self,size):
        self.size = size
        self.flowers = []
        self.wasp_hives = []
        self.hives = []
        self.map_board = stdarray.create2D(size, size)
        self.hidden_entities = {} # (row,col) : [chars]
    
    def add_wasphive(self, wasphive):
        self.wasp_hives.append(wasphive)
        self.map_board[wasphive.row][wasphive.col] = wasphive.char

    def add_beehive(self, beehive):
        self.hives.append(beehive)
        self.map_board[beehive.row][beehive.col] = beehive.char

    def add_flower(self, flower):
        self.flowers.append(flower)
        self.map_board[flower.row][flower.col] = flower.char

    def is_open(self, row, col) -> bool:
        """
        returns True if the position (row, col) on the map is open
        """
        for hive in self.hives:
            if hive.row == row and hive.col == col:
                return False
        for flower in self.flowers:
            if flower.row == row and flower.col == col:
                return False
        return True
    
    def add_to_board(self, entity):
        """
        Adds the entity to the 2D map board
        """
        row, col = entity.row, entity.col
        # Empty cell
        if self.map_board[row][col] is None:
            self.map_board[row][col] = entity.char
        # Cell already has multiple entities
        elif (row, col) in self.hidden_entities:
            self.hidden_entities[(row,col)].append(entity.char)
            if self.map_board[row][col] != 'w':
                 if self.map_board[row][col] != entity.char:
                    self.map_board[row][col] = 'm'
            if entity.char == 'w':
                self.map_board[row][col] = entity.char
        # Cell is a single entity, objects are ignored
        elif not self.map_board[row][col] in ('F', 'B', 'H', 'D', 'W'):
            self.hidden_entities[(row, col)] = [self.map_board[row][col], entity.char]

            if self.map_board[row][col] != 'w':
                 if self.map_board[row][col] != entity.char:
                    self.map_board[row][col] = 'm'
            if entity.char == 'w':
                self.map_board[row][col] = entity.char

    def remove_from_board(self, p_row, p_col, char):
        """
        Remove the entity from the the previous position on the board
        """
        # If entity was hidden
        if (p_row, p_col) in self.hidden_entities:
            hidden = self.hidden_entities[(p_row, p_col)]

            self.hidden_entities[(p_row, p_col)].pop(hidden.index(char))
            # no more hidden entities
            if len(hidden) == 1:
                self.map_board[p_row][p_col] = hidden[0]
                del self.hidden_entities[(p_row, p_col)]
            elif self.map_board[p_row][p_col] == 'm' and all(c == hidden[0] for c in hidden):
                self.map_board[p_row][p_col] = hidden[0] # All of same type
        # set back to empty cell
        elif self.map_board[p_row][p_col] not in ('F', 'B', 'H', 'D', 'W'):
            self.map_board[p_row][p_col] = None            

    def print_board(self):
        """
        Print the 2D map board to standard output
        """
        output = "   "
        for i in range(self.size):
            output += f" {i:03}"        
        output += "\n   +"
        for i in range(self.size):
            output += "---+"
        output += "\n" 
        
        # Board
        row_num = self.size-1
        for row in reversed(self.map_board):
            output += f"{row_num:03}|"       
            for col in row:
                if col:
                    output += f" {col} |"
                else:
                    output += "   |"            
            output += "\n   +"
            for j in range(self.size):
                output += "---+"
            output += "\n"
            row_num -= 1
        stdio.write(output)

class Simulation:
    """
    The class that handles all parts of a simulation
    """
    def __init__(self, _map: Map, duration: int, pollen_action, pollen_type):
        self.duration = duration
        self.pollen_action = pollen_action
        self._map = _map
        self.pollen_type = pollen_type
        
    def run(self, gui_mode):
        """
        The main simulation loop
        """
        if gui_mode == 1:
            gui.init_gui(self._map.size) # initialize GUI and show menu
            
            gui.render_frame(self._map.map_board, self._map.hidden_entities)
            self.update_all_entities()

            bees_killed = 0
            for i in range(self.duration):
                gui.handle_input()
                gui.set_window_title(str(i+1))

                bees_killed += self.move_all_entities()
                self.update_flowers()
                self.update_all_entities()
                
                gui.render_frame(self._map.map_board, self._map.hidden_entities)
        else:
            self._map.print_board()
            self.update_all_entities()
            bees_killed = 0
            for i in range(self.duration):
                bees_killed += self.move_all_entities()
                self.update_flowers()

                self.update_all_entities()
                self._map.print_board()
            
        result = self.get_result()
        output = ""
        if not result:
            output = "Answer:\nNo pollen collected"
        else:
            output = result
        if gui_mode == 1:
            gui.show_result(output, bees_killed, self.pollen_action, self._map.map_board,
                            self._map.hidden_entities)
            
        stdio.writeln(output)
             
    def move_all_entities(self) -> int:
        """
        Moves all the entites on the map
        """         
        # First move wasps so that Bees get killed on move
        for wasp_hive in self._map.wasp_hives:
            wasp_hive.move_entities(self._map)
        bees_killed = 0
        for hive in self._map.hives:
            bees_killed += hive.move_entities(self._map)
        return bees_killed
            
    def update_flowers(self):
        # Flowers count bees around them
        for flower in self._map.flowers:
            flower.count_bees(self._map.hives)
        
    def update_all_entities(self):
        for hive in self._map.hives:
            hive.update_entities(self._map)
    
    def get_result(self) -> str:
        """
        returns the result of this simulation
        """
        total_pollen = []
        for hive in self._map.hives:
            if not hive.pollen_list: 
                    continue
            total_pollen += hive.pollen_list
        
        if not total_pollen:
            return None
        
        if self.pollen_action == 'max':
            _max = max(total_pollen)
            return f"Answer:\n{_max}"
        if self.pollen_action == 'min':
            _min = min(total_pollen)
            return f"Answer:\n{_min}"
        if self.pollen_action == 'sum':
            _sum = sum(total_pollen)
            return f"Answer:\n{_sum}"
        if self.pollen_action == 'sort':
            merge = MergeSort(total_pollen)
            merge.sort(0, len(total_pollen)-1) # custom sort
            if self.pollen_type == 'f':
                total_pollen = list(map(str, total_pollen))
            return "Answer:\n" + "\n".join(total_pollen)
        return None
