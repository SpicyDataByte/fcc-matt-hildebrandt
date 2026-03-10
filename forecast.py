import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def forecast_monthly_registrations(monthly_counts):
    print("Forecasting next 12 months for each payment method...")
    forecast_results = []

    for method in monthly_counts['cleaned_payment_method_value'].unique():
        method_df = monthly_counts[monthly_counts['cleaned_payment_method_value'] == method].copy()
        method_df['month_index'] = np.arange(len(method_df))

        model = LinearRegression()
        model.fit(method_df[['month_index']], method_df['registrations'])

        future_months = np.arange(len(method_df), len(method_df) + 12).reshape(-1, 1)
        predicted = model.predict(future_months)

        forecast_df = pd.DataFrame({
            'year_month': pd.period_range(
                start=method_df['year_month'].max() + 1,
                periods=12,
                freq='M'
            ),
            'predicted_registrations': predicted.round(0).astype(int),
            'cleaned_payment_method_value': method
        })
        forecast_results.append(forecast_df)

    return pd.concat(forecast_results).reset_index(drop=True)
