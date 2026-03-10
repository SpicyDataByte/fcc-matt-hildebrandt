from extract import extract_data
from transform import build_star_schema, generate_insights
from forecast import forecast_monthly_registrations
from validate import ColumnValidator, is_clean_name, is_not_empty
from load import save_to_csv
import pandas as pd
import warnings
import unittest
import sys
import os

warnings.filterwarnings("ignore", category=UserWarning)

print("=== Running Tests ===")
loader = unittest.TestLoader()
suite = loader.discover(start_dir="tests", pattern="test_*.py")
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

if not result.wasSuccessful():
    print("Tests failed. Halting pipeline.")
    sys.exit(1)

print("All tests passed.\n")

# === Extract ===
print("Starting data extraction...")
base_path = "data"

user = extract_data(os.path.join(base_path, "user.csv"))
user_registration = extract_data(os.path.join(base_path, "user_registration.csv"))
plan = extract_data(os.path.join(base_path, "plan.csv"))
plan_payment_frequency = extract_data(os.path.join(base_path, "plan_payment_frequency.csv"))
channel_code = extract_data(os.path.join(base_path, "channel_code.csv"))
status_code = extract_data(os.path.join(base_path, "status_code.csv"))
user_play_session = extract_data(os.path.join(base_path, "user_play_session.csv"))
user_plan = extract_data(os.path.join(base_path, "user_plan.csv"))
user_payment_detail = extract_data(os.path.join(base_path, "user_payment_detail.csv"))

print("Extraction complete.\n")

# === Transform ===
print("Starting data transformation...")

# Build Star Schema
dim_user, dim_plan, dim_channel, dim_status, fact_play_session, fact_subscription = build_star_schema(
    user, user_registration, plan, plan_payment_frequency, channel_code, status_code, user_play_session, user_plan, user_payment_detail
)

# Generate Required Insights
platform_sessions, subscription_prefs, gross_revenue = generate_insights(fact_play_session, fact_subscription)

print("\n=== KEY INSIGHTS FOR 2025 ===")
print(f"Total Gross Revenue Generated: ${gross_revenue:,.2f}")
print("\nPlay Sessions by Platform:")
print(platform_sessions.to_string(index=False))
print("\nPurchases by Payment Frequency:")
print(subscription_prefs.to_string(index=False))
print("===============================\n")

# Forecasting (from your original logic, using the new fact table)
monthly_counts = fact_subscription.groupby(['year_month', 'payment_method_value']).size().reset_index(name='registrations')
monthly_counts.rename(columns={'payment_method_value': 'cleaned_payment_method_value'}, inplace=True)
forecast_all = forecast_monthly_registrations(monthly_counts)

# === Validation ===
print("Validating data...")
validator = ColumnValidator(fact_subscription)
validator.validate('payment_method_value', is_clean_name)
validator.validate('payment_method_code', is_not_empty)

invalid_rows = validator.get_invalid_rows()
print(f"Validation complete. Found {len(invalid_rows)} invalid records.\n")

# === Load ===
print("\n=== Load ===")
# Save Dimensions
save_to_csv(dim_user, "dim_user.csv")
save_to_csv(dim_plan, "dim_plan.csv")
save_to_csv(dim_channel, "dim_channel.csv")
save_to_csv(dim_status, "dim_status.csv")

# Save Facts
save_to_csv(fact_play_session, "fact_play_session.csv")
save_to_csv(fact_subscription, "fact_subscription_payment.csv")

# Save Additions
save_to_csv(forecast_all, "forecast_registrations.csv")
save_to_csv(invalid_rows, "invalid_payment_rows.csv")
print("All dataframes successfully structured and saved to output directory.\n")