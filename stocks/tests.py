from django.test import TestCase
from StockWebsite.utils import partition, quicksort, linear_search


class QuickSortTestCase(TestCase):
    def test_partition(self):
        # Opret testdata
        array = [{'værdi': 3}, {'værdi': 1}, {'værdi': 4}, {'værdi': 2}]

        # Kald partitionsfunktionen
        pivot_index = partition(array, 0, len(
            array) - 1, 'værdi', descending=False)

        # Bekræft at elementer til venstre for pivoten er mindre eller lig med og elementer til højre er større
        for i in range(pivot_index):
            self.assertTrue(array[i]['værdi'] <= array[pivot_index]['værdi'])
        for i in range(pivot_index + 1, len(array)):
            self.assertTrue(array[i]['værdi'] >= array[pivot_index]['værdi'])

    def test_quicksort(self):
        # Opret testdata
        array = [{'værdi': 3}, {'værdi': 1}, {'værdi': 4}, {'værdi': 2}]

        # Kald quicksort-funktionen
        sorteret_array = quicksort(array, 0, len(
            array) - 1, 'værdi', descending=False)

        # Bekræft at arrayet er sorteret
        for i in range(1, len(sorteret_array)):
            self.assertTrue(sorteret_array[i]['værdi']
                            >= sorteret_array[i-1]['værdi'])


class LinearSearchTestCase(TestCase):
    def test_linear_search_found(self):
        # Opret testdata
        tickers = [
            {'T': 'AAPL', 'Pris': 150.0},
            {'T': 'GOOGL', 'Pris': 2800.0},
            {'T': 'MSFT', 'Pris': 300.0}
        ]
        target = 'GOOGL'

        # Kald linear_search-funktionen
        resultat = linear_search(tickers, target)

        # Bekræft at resultatet er den korrekte ticker
        self.assertEqual(resultat, {'T': 'GOOGL', 'Pris': 2800.0})

    def test_linear_search_not_found(self):
        # Opret testdata
        tickers = [
            {'T': 'AAPL', 'Pris': 150.0},
            {'T': 'GOOGL', 'Pris': 2800.0},
            {'T': 'MSFT', 'Pris': 300.0}
        ]
        target = 'AMZN'

        # Kald linear_search-funktionen
        resultat = linear_search(tickers, target)

        # Bekræft at resultatet er -1, da target ikke blev fundet
        self.assertEqual(resultat, -1)
