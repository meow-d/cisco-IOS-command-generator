import unittest


def main():
    pass


class MyTest(unittest.TestCase):
    def test_addition(self):
        self.assertEqual((2 + 3), 5)


if __name__ == "__main__":
    unittest.main()
