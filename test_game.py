import unittest
from dino import Dino, check_collision 

class TestDinoGame(unittest.TestCase):
    
    def setUp(self):
        self.dino = Dino()

    def test_dino_jump(self):
        """Test that the Dino jumps correctly."""
        self.dino.jump()
        self.assertTrue(self.dino.is_jumping)

  def test_collision_detection(self):
        """Test collision logic."""
        obstacle = {"x": 50, "y": 100}
        self.assertTrue(check_collision(self.dino, obstacle))

if __name__ == "__main__":
    unittest.main()
