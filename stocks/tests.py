from django.test import TestCase
from StockWebsite.utils import partition, quicksort, linear_search


class QuickSortTestCase(TestCase):
    def test_partition(self):
        # Opret testdata
        array = [{'value': 3}, {'value': 1}, {'value': 4}, {'value': 2}]

        # Kald partitionsfunktionen
        pivot_index = partition(array, 0, len(
            array) - 1, 'value', descending=False)

        # Bekræft at elementer til venstre for pivoten er mindre eller lig med og elementer til højre er større
        for i in range(pivot_index):
            self.assertTrue(array[i]['value'] <= array[pivot_index]['value'])
        for i in range(pivot_index + 1, len(array)):
            self.assertTrue(array[i]['value'] >= array[pivot_index]['value'])

    def test_quicksort(self):
        # Opret testdata
        array = [{'value': 3}, {'value': 1}, {'value': 4}, {'value': 2}]

        # Kald quicksort-funktionen
        sorted_array = quicksort(array, 0, len(
            array) - 1, 'value', descending=False)

        # Bekræft at arrayet er sorteret
        for i in range(1, len(sorted_array)):
            self.assertTrue(sorted_array[i]['value']
                            >= sorted_array[i-1]['value'])


class LinearSearchTestCase(TestCase):
    def test_linear_search_found(self):
        # Opret testdata
        tickers = [
            {'T': 'AAPL', 'c': 150.0},
            {'T': 'GOOGL', 'c': 2800.0},
            {'T': 'MSFT', 'c': 300.0}
        ]
        target = 'GOOGL'

        # Kald linear_search-funktionen
        result = linear_search(tickers, target)

        # Bekræft at resultet er den korrekte ticker
        self.assertEqual(result, {'T': 'GOOGL', 'c': 2800.0})

    def test_linear_search_not_found(self):
        # Opret testdata
        tickers = [
            {'T': 'AAPL', 'c': 150.0},
            {'T': 'GOOGL', 'c': 2800.0},
            {'T': 'MSFT', 'c': 300.0}
        ]
        target = 'AMZN'

        # Kald linear_search-funktionen
        result = linear_search(tickers, target)

        # Bekræft at resultet er -1, da target ikke blev fundet
        self.assertEqual(result, -1)
