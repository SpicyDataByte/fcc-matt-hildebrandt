import unittest
import pandas as pd
from validate import ColumnValidator, is_clean_name, is_not_empty

class TestValidateFunctions(unittest.TestCase):

    def test_is_clean_name(self):
        self.assertTrue(is_clean_name("Visa"))
        self.assertFalse(is_clean_name("bad@name"))
        self.assertFalse(is_clean_name("Two Words"))

    def test_is_not_empty(self):
        self.assertTrue(is_not_empty("Text"))
        self.assertFalse(is_not_empty(""))

    def test_column_validator(self):
        df = pd.DataFrame({
            'col1': ["good", "bad@value", ""],
            'col2': ["yes", None, " "]
        })
        validator = ColumnValidator(df)
        validator.validate('col1', is_clean_name)
        validator.validate('col2', is_not_empty)

        invalids = validator.get_invalid_rows()
        self.assertEqual(len(invalids), 2)
        self.assertIn('failed_columns', invalids.columns)
