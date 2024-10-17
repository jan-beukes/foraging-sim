import sys
import stdio

import simulation
from entities import Bee ,DesertBee, HoneyBee, Wasp
from objects import Flower, Hive, WaspHive

def read_map():
    '''
    Read the simulation's map setup from standard input
    Returns a Simulation object when a valid map is read
    '''
    try:
        line = stdio.readLine().split()
        if len(line) != 4:
            stdio.writeln("ERROR: Invalid configuration line")
            exit()
            
        map_size = int(line[0])
        duration = int(line[1])  
        pollen_type = line[2]
        pollen_action = line[3]
        
        # config validation
        if pollen_type not in ['s','f']:
            stdio.writeln("ERROR: Invalid configuration line")
            exit()
        if pollen_type == 's' and pollen_action != "sort":
            stdio.writeln("ERROR: Invalid configuration line")
            exit()
        elif pollen_type == 'f' and not pollen_action in ('max','min','sum','sort'):
            stdio.writeln("ERROR: Invalid configuration line")
            exit()         
        if duration < 0:
            stdio.writeln("ERROR: Invalid configuration line")
            exit()     
        if not (1 <= map_size <= 100):
            stdio.writeln("ERROR: Invalid configuration line")
            exit()      
    except (TypeError, ValueError):
        stdio.writeln(f"ERROR: Invalid configuration line")
        exit()
    
    _map = simulation.Map(map_size)
    
    # objects
    line_num = 1
    while not stdio.isEmpty():
        line_num += 1
        try:
            # Check setup count
            tokens = stdio.readLine().split()
            if len(tokens) != 4:
                stdio.writeln(f"ERROR: Invalid object setup on line {line_num}")
                exit()
            # config     
            _object = tokens[0]
            col, row = int(tokens[1]),int(tokens[2]) # input is col, row
            if not(0 <= row < map_size) or not(0 <= col < map_size):
                stdio.writeln(f"ERROR: Invalid object setup on line {line_num}")
                exit()
                
            n = int(tokens[3])
            if n < 0:
                stdio.writeln(f"ERROR: Invalid object setup on line {line_num}")
                exit()
                
            if not _map.is_open(row, col):
                if _object == "F":
                    stdio.writeln(f"ERROR: Cannot place flower at already occupied location ({row}, {col})")
                else:
                    stdio.writeln(f"ERROR: Cannot place hive at already occupied location ({row}, {col})")
                exit()
                
            # Create objects        
            if _object == "F":
                flower = Flower(row, col, pollen_type)
                for i in range(n):
                    pollen = stdio.readLine()
                    line_num += 1
                    if pollen_type == 'f':
                        if len(pollen.split()) > 1:
                            stdio.writeln(f"ERROR: Invalid object setup on line {line_num}")
                            exit()
                        else:
                            pollen = float(pollen)   
                    flower.add_pollen(pollen)
                    
                _map.add_flower(flower)              
            elif _object in ['B','D','H']:
                hive = Hive(row, col, n, _object)        

                line = stdio.readLine().split()
                line_num += 1
                if len(line) != 2: 
                    stdio.writeln(f"ERROR: Invalid object setup on line {line_num}")
                    exit() 

                speed,perception = int(line[0]), int(line[1]) 
                for i in range(n):
                    if _object == 'B': 
                        bee = Bee(row,col,speed,perception, hive)
                    elif _object == 'D': 
                        bee = DesertBee(row,col,speed,perception, hive)
                    elif _object == 'H': 
                        bee = HoneyBee(row,col,speed,perception, hive) 
                    hive.add_entity(bee)
                _map.add_beehive(hive)           
            elif _object == "W":
                hive = WaspHive(row, col, n, 'W')
                             
                line = stdio.readLine().split()
                line_num += 1
                if len(line) != 1: 
                    stdio.writeln(f"ERROR: Invalid object setup on line {line_num}")
                    exit() 
                speed = int(line[0])
                for i in range(n):
                    wasp = Wasp(row,col,speed)
                    hive.add_entity(wasp)
                _map.add_wasphive(hive)
            else:
                stdio.writeln(f"ERROR: Invalid object setup on line {line_num}")
                exit()
        except (TypeError,ValueError, EOFError) :
            stdio.writeln(f"ERROR: Invalid object setup on line {line_num}")
            exit()
    
    return simulation.Simulation(_map, duration, pollen_action, pollen_type)

def main():
    # validate arguments
    if len(sys.argv) > 2:
        stdio.writeln("ERROR: Too many arguments")
        exit()
    if len(sys.argv) < 2:
        stdio.writeln("ERROR: Too few arguments")
        exit()
    if sys.argv[1] not in ['0','1']:
        stdio.writeln("ERROR: Invalid argument: " + sys.argv[1])    
        
    gui_mode = int(sys.argv[1])
    sim = read_map()
    sim.run(gui_mode)
    
if __name__ == "__main__": 
    main()
