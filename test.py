import stdio
from compass import Compass
from entities import Bee
from objects import Flower, Hive
import unittest

class Test(unittest.TestCase):
    
    def test_bee_update(self):
        bee = Bee(10, 12, 3, 4, Hive(3, 3, 2, 'B'))
        flowers = [Flower(12, 12, 'f'), Flower(11, 10, 'f'), Flower(11, 14, 'f'),Flower(8, 11, 'f')]
        bee.update(flowers)
        ret = bee.target
        print(f"{bee.target.row} {bee.target.col}")
        self.assertEqual((8,11), (bee.target.row, bee.target.col))


unittest.main()
