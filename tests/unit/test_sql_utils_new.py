import unittest
from mindsdb.integrations.utilities.sql_utils import FilterCondition, FilterOperator, parse_conditions, filter_dataframe
import pandas as pd


class TestSQLUtils(unittest.TestCase):

    def test_parse_conditions_empty_list(self):
        """Test parse_conditions with empty list"""
        result = parse_conditions([])
        self.assertEqual(result, {})

    def test_parse_conditions_single_condition(self):
        """Test parse_conditions with single condition"""
        conditions = [
            FilterCondition(column="name", op=FilterOperator.EQUAL, value="test")
        ]
        result = parse_conditions(conditions)
        expected = {"name": ["test"]}
        self.assertEqual(result, expected)

    def test_parse_conditions_multiple_conditions_same_column(self):
        """Test parse_conditions with multiple conditions on same column"""
        conditions = [
            FilterCondition(column="name", op=FilterOperator.EQUAL, value="test1"),
            FilterCondition(column="name", op=FilterOperator.EQUAL, value="test2")
        ]
        result = parse_conditions(conditions)
        expected = {"name": ["test1", "test2"]}
        self.assertEqual(result, expected)

    def test_parse_conditions_multiple_columns(self):
        """Test parse_conditions with conditions on different columns"""
        conditions = [
            FilterCondition(column="name", op=FilterOperator.EQUAL, value="test"),
            FilterCondition(column="age", op=FilterOperator.GREATER_THAN, value=25),
            FilterCondition(column="city", op=FilterOperator.EQUAL, value="NYC")
        ]
        result = parse_conditions(conditions)
        expected = {
            "name": ["test"],
            "age": [25],
            "city": ["NYC"]
        }
        self.assertEqual(result, expected)

    def test_get_values_for_column_existing_column(self):
        """Test get_values_for_column with existing column"""
        parsed_conditions = {"name": ["test1", "test2"], "age": [25]}
        result = FilterCondition.get_values_for_column(parsed_conditions, "name")
        self.assertEqual(result, "test1")  # Returns first value

    def test_get_values_for_column_non_existing_column(self):
        """Test get_values_for_column with non-existing column"""
        parsed_conditions = {"name": ["test"], "age": [25]}
        result = FilterCondition.get_values_for_column(parsed_conditions, "city")
        self.assertIsNone(result)  # Returns None when key doesn't exist

    def test_get_values_for_column_empty_list(self):
        """Test get_values_for_column with empty list for column"""
        parsed_conditions = {"name": [], "age": [25]}
        result = FilterCondition.get_values_for_column(parsed_conditions, "name")
        self.assertIsNone(result)  # Returns None when list is empty

    def test_filter_dataframe_no_conditions(self):
        """Test filter_dataframe with no conditions"""
        # Create test DataFrame
        df = pd.DataFrame({
            'name': ['Alice', 'Bob'],
            'age': [25, 30]
        })

        # Apply filter with empty conditions
        result = filter_dataframe(df, [])

        # Should return all rows
        self.assertEqual(len(result), 2)
        self.assertEqual(list(result['name']), ['Alice', 'Bob'])


if __name__ == '__main__':
    unittest.main()
