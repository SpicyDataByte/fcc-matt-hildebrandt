import pandas as pd


def calculate_session_duration(df):
    df = df.copy()
    df['start_datetime'] = pd.to_datetime(df['start_datetime'])
    df['end_datetime'] = pd.to_datetime(df['end_datetime'])
    df['duration_minutes'] = (df['end_datetime'] - df['start_datetime']).dt.total_seconds() / 60
    return df


def clean_payment_methods(df, allowed):
    df = df.copy()
    df['cleaned_payment_method_value'] = df['payment_method_value'].where(
        df['payment_method_value'].isin(allowed), other='Other'
    )
    return df


def merge_user_plan(user_plan, user_payment_detail, plan, freq):
    result = pd.merge(user_plan, user_payment_detail, on='payment_detail_id', how='left')
    result = pd.merge(result, plan, on='plan_id', how='left')
    result = pd.merge(result, freq, on='payment_frequency_code', how='left')
    return result


def build_star_schema(user, user_registration, plan, plan_payment_frequency, channel_code, status_code, user_play_session, user_plan, user_payment_detail):
    print("Building Star Schema...")
    
    # --- DIMENSIONS ---
    dim_user = pd.merge(user, user_registration, on='user_id', how='left')
    dim_plan = pd.merge(plan, plan_payment_frequency, on='payment_frequency_code', how='left')
    dim_channel = channel_code.copy()
    dim_status = status_code.copy()
    
    # --- FACTS ---
    # Fact: Play Sessions
    fact_play_session = user_play_session.copy()
    fact_play_session['start_datetime'] = pd.to_datetime(fact_play_session['start_datetime'])
    fact_play_session['end_datetime'] = pd.to_datetime(fact_play_session['end_datetime'])
    fact_play_session['duration_minutes'] = (fact_play_session['end_datetime'] - fact_play_session['start_datetime']).dt.total_seconds() / 60
    
    # Fact: Subscription Payments
    # Merging user plans with their payment details and the plan dimension
    fact_subscription = pd.merge(user_plan, user_payment_detail, on='payment_detail_id', how='left')
    fact_subscription = pd.merge(fact_subscription, dim_plan, on='plan_id', how='left')
    fact_subscription['start_date'] = pd.to_datetime(fact_subscription['start_date'])
    fact_subscription['year_month'] = fact_subscription['start_date'].dt.to_period('M')

    return dim_user, dim_plan, dim_channel, dim_status, fact_play_session, fact_subscription


def generate_insights(fact_play_session, fact_subscription):
    print("Generating Key Business Insights...")
    
    # Insight 1: Online vs Mobile App Play Sessions
    platform_sessions = fact_play_session.groupby('channel_code').size().reset_index(name='total_sessions')
    
    # Insight 2: Registered users opt-in frequency (Onetime vs Subscription)
    subscription_prefs = fact_subscription.groupby('payment_frequency_code').size().reset_index(name='total_purchases')
    
    # Insight 3: Gross Revenue Generated
    gross_revenue = fact_subscription['cost_amount'].sum()
    
    return platform_sessions, subscription_prefs, gross_revenue