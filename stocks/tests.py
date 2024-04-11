from django.test import TestCase
from StockWebsite.utils import partition, quicksort, linear_search


class QuickSortTestCase(TestCase):
    def test_partition(self):
        # Create test data
        array = [{'value': 3}, {'value': 1}, {'value': 4}, {'value': 2}]

        # Call the partition function
        pivot_index = partition(array, 0, len(
            array) - 1, 'value', descending=False)

        # Assert that elements to the left of pivot are smaller or equal and elements to the right are greater
        for i in range(pivot_index):
            self.assertTrue(array[i]['value'] <= array[pivot_index]['value'])
        for i in range(pivot_index + 1, len(array)):
            self.assertTrue(array[i]['value'] >= array[pivot_index]['value'])

    def test_quicksort(self):
        # Create test data
        array = [{'value': 3}, {'value': 1}, {'value': 4}, {'value': 2}]

        # Call the quicksort function
        sorted_array = quicksort(array, 0, len(
            array) - 1, 'value', descending=False)

        # Assert that the array is sorted
        for i in range(1, len(sorted_array)):
            self.assertTrue(sorted_array[i]['value']
                            >= sorted_array[i-1]['value'])


class LinearSearchTestCase(TestCase):
    def test_linear_search_found(self):
        # Create test data
        tickers = [
            {'T': 'AAPL', 'Price': 150.0},
            {'T': 'GOOGL', 'Price': 2800.0},
            {'T': 'MSFT', 'Price': 300.0}
        ]
        target = 'GOOGL'

        # Call the linear_search function
        result = linear_search(tickers, target)

        # Assert that the result is the correct ticker
        self.assertEqual(result, {'T': 'GOOGL', 'Price': 2800.0})

    def test_linear_search_not_found(self):
        # Create test data
        tickers = [
            {'T': 'AAPL', 'Price': 150.0},
            {'T': 'GOOGL', 'Price': 2800.0},
            {'T': 'MSFT', 'Price': 300.0}
        ]
        target = 'AMZN'

        # Call the linear_search function
        result = linear_search(tickers, target)

        # Assert that the result is -1 since the target is not found
        self.assertEqual(result, -1)
