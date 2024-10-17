import random

# Constants
board_size = 100
N = 1000 
type = 'f'
action = 'sort'


print(f"{board_size} {N} {type} {action}")

flower_grid = 30
pollen = 10
offset = (board_size-flower_grid)//2
# Flower
for row in range(offset, board_size-offset):
    for col in range(offset, board_size-offset):
        print(f"F {col} {row} {pollen}")
        for i in range(pollen):
            print(random.randint(0, 6969))


