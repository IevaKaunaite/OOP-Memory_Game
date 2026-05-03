import unittest
from main import Kortele, RezultatuValdiklis


class TestKortele(unittest.TestCase):

    def test_reiksme(self):
        k = Kortele(5)
        self.assertEqual(k.gauti_reiksme(), 5)

    def test_atvertimas(self):
        k = Kortele(3)
        k.atversti()
        self.assertTrue(k.atversta)

    def test_uzvertimas(self):
        k = Kortele(3)
        k.atversti()
        k.uzversti()
        self.assertFalse(k.atversta)

    def test_vaizdavimas_paslepta(self):
        k = Kortele(7)
        self.assertEqual(k.vaizduoti(), "*")


class TestSingleton(unittest.TestCase):

    def test_singleton(self):
        a = RezultatuValdiklis()
        b = RezultatuValdiklis()
        self.assertIs(a, b)


if __name__ == "__main__":
    unittest.main()
