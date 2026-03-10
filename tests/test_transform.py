import unittest
import pandas as pd
from transform import calculate_session_duration, clean_payment_methods, merge_user_plan

class TestTransformFunctions(unittest.TestCase):

    def test_calculate_session_duration(self):
        df = pd.DataFrame({
            'start_datetime': ['2024-01-01 10:00:00'],
            'end_datetime': ['2024-01-01 10:30:00']
        })
        df = calculate_session_duration(df)
        self.assertEqual(df['duration_minutes'].iloc[0], 30)

    def test_clean_payment_methods(self):
        df = pd.DataFrame({
            'payment_method_value': ['ApplePay', 'Cash', 'GooglePay']
        })
        allowed = ['ApplePay', 'GooglePay']
        cleaned_df = clean_payment_methods(df, allowed)
        self.assertListEqual(
            cleaned_df['cleaned_payment_method_value'].tolist(),
            ['ApplePay', 'Other', 'GooglePay']
        )

    def test_merge_user_plan(self):
        user_plan = pd.DataFrame({'payment_detail_id': [1], 'plan_id': [10], 'payment_frequency_code': ['M'], 'start_date': ['2024-01-01']})
        user_payment_detail = pd.DataFrame({'payment_detail_id': [1], 'value': ['x']})
        plan = pd.DataFrame({'plan_id': [10], 'type': ['Basic']})
        freq = pd.DataFrame({'payment_frequency_code': ['M'], 'label': ['Monthly']})

        result = merge_user_plan(user_plan, user_payment_detail, plan, freq)
        self.assertIn('type', result.columns)
        self.assertIn('label', result.columns)
