import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def generate_synthetic_prices(n_days=400, mu1_true=30, mu2_true=60, sigma_true=3.5, 
                               tau_true_pct=0.5, seed=42):
    """
    Generate synthetic time-series price data with a single change point.
    
    Parameters
    ----------
    n_days : int
        Number of days to generate
    mu1_true : float
        Mean price before change point
    mu2_true : float
        Mean price after change point
    sigma_true : float
        Standard deviation of noise
    tau_true_pct : float
        Position of change point as fraction of n_days (0 to 1)
    seed : int
        Random seed for reproducibility
        
    Returns
    -------
    df : pd.DataFrame
        DataFrame with columns: date, price
    tau_true : int
        True change point index
    """
    np.random.seed(seed)
    
    tau_true = int(n_days * tau_true_pct)
    
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(n_days)]
    
    prices = np.zeros(n_days)
    for i in range(n_days):
        if i < tau_true:
            prices[i] = np.random.normal(mu1_true, sigma_true)
        else:
            prices[i] = np.random.normal(mu2_true, sigma_true)
    
    prices = np.maximum(prices, 1.0)
    
    df = pd.DataFrame({
        'date': dates,
        'price': prices
    })
    
    return df, tau_true


def generate_events(tau_true, n_days=400, seed=42):
    """
    Generate a synthetic events table with 2-3 events.
    One event will be near the true change point.
    
    Parameters
    ----------
    tau_true : int
        True change point index
    n_days : int
        Total number of days
    seed : int
        Random seed
        
    Returns
    -------
    events_df : pd.DataFrame
        DataFrame with columns: event_name, start_date, end_date, category
    """
    np.random.seed(seed + 1)
    
    start_date = datetime(2023, 1, 1)
    
    events = []
    
    event_start = start_date + timedelta(days=max(0, tau_true - 10))
    event_end = start_date + timedelta(days=min(n_days - 1, tau_true + 10))
    events.append({
        'event_name': 'Major Supply Disruption',
        'start_date': event_start,
        'end_date': event_end,
        'category': 'supply_shock'
    })
    
    early_event_day = np.random.randint(30, min(100, tau_true - 50))
    events.append({
        'event_name': 'Policy Announcement',
        'start_date': start_date + timedelta(days=early_event_day),
        'end_date': start_date + timedelta(days=early_event_day + 5),
        'category': 'policy'
    })
    
    if tau_true + 80 < n_days:
        late_event_day = tau_true + np.random.randint(60, 100)
        events.append({
            'event_name': 'Market Correction',
            'start_date': start_date + timedelta(days=late_event_day),
            'end_date': start_date + timedelta(days=late_event_day + 7),
            'category': 'market'
        })
    
    events_df = pd.DataFrame(events)
    return events_df


def generate_synthetic_prices_multiple(n_days=400, mu_true=[30, 50, 70], 
                                       tau_true_pct=[0.33, 0.66], sigma_true=3.5, seed=42):
    """
    Generate synthetic time-series price data with MULTIPLE change points.
    
    Parameters
    ----------
    n_days : int
        Number of days to generate
    mu_true : list of float
        Mean prices for each regime (length = n_changepoints + 1)
        Example: [30, 50, 70] creates 3 regimes with 2 change points
    tau_true_pct : list of float
        Positions of change points as fractions of n_days (0 to 1)
        Must be sorted in ascending order
        Example: [0.33, 0.66] creates change points at 1/3 and 2/3 of the series
    sigma_true : float
        Standard deviation of noise
    seed : int
        Random seed for reproducibility
        
    Returns
    -------
    df : pd.DataFrame
        DataFrame with columns: date, price, regime
    tau_true : list of int
        True change point indices
    """
    np.random.seed(seed)
    
    n_changepoints = len(tau_true_pct)
    assert len(mu_true) == n_changepoints + 1, "mu_true must have length = n_changepoints + 1"
    assert all(tau_true_pct[i] < tau_true_pct[i+1] for i in range(len(tau_true_pct)-1)), \
        "tau_true_pct must be sorted in ascending order"
    
    tau_true = [int(n_days * pct) for pct in tau_true_pct]
    
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(n_days)]
    
    prices = np.zeros(n_days)
    regimes = np.zeros(n_days, dtype=int)
    
    for i in range(n_days):
        regime = 0
        for j, tau in enumerate(tau_true):
            if i >= tau:
                regime = j + 1
        
        regimes[i] = regime
        prices[i] = np.random.normal(mu_true[regime], sigma_true)
    
    prices = np.maximum(prices, 1.0)
    
    df = pd.DataFrame({
        'date': dates,
        'price': prices,
        'regime': regimes
    })
    
    return df, tau_true


def generate_events_multiple(tau_true_list, n_days=400, seed=42):
    """
    Generate a synthetic events table with events near multiple change points.
    
    Parameters
    ----------
    tau_true_list : list of int
        List of true change point indices
    n_days : int
        Total number of days
    seed : int
        Random seed
        
    Returns
    -------
    events_df : pd.DataFrame
        DataFrame with columns: event_name, start_date, end_date, category
    """
    np.random.seed(seed + 1)
    
    start_date = datetime(2023, 1, 1)
    events = []
    
    event_names = [
        'Major Supply Disruption',
        'Geopolitical Crisis',
        'Production Increase',
        'Demand Shock',
        'Policy Change'
    ]
    
    categories = ['supply_shock', 'geopolitical', 'production', 'demand', 'policy']
    
    for idx, tau in enumerate(tau_true_list):
        event_start = start_date + timedelta(days=max(0, tau - 8))
        event_end = start_date + timedelta(days=min(n_days - 1, tau + 8))
        events.append({
            'event_name': event_names[idx % len(event_names)],
            'start_date': event_start,
            'end_date': event_end,
            'category': categories[idx % len(categories)]
        })
    
    if len(tau_true_list) > 0 and tau_true_list[0] > 60:
        early_event_day = np.random.randint(20, min(50, tau_true_list[0] - 30))
        events.append({
            'event_name': 'Early Market Adjustment',
            'start_date': start_date + timedelta(days=early_event_day),
            'end_date': start_date + timedelta(days=early_event_day + 5),
            'category': 'market'
        })
    
    if len(tau_true_list) > 0 and tau_true_list[-1] + 60 < n_days:
        late_event_day = tau_true_list[-1] + np.random.randint(40, 70)
        events.append({
            'event_name': 'Late Policy Announcement',
            'start_date': start_date + timedelta(days=late_event_day),
            'end_date': start_date + timedelta(days=late_event_day + 6),
            'category': 'policy'
        })
    
    events_df = pd.DataFrame(events)
    return events_df


def save_data(output_dir='data'):
    """
    Generate and save both price and events data to CSV files.
    
    Parameters
    ----------
    output_dir : str
        Directory to save CSV files
        
    Returns
    -------
    prices_df : pd.DataFrame
    events_df : pd.DataFrame
    tau_true : int
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    prices_df, tau_true = generate_synthetic_prices()
    events_df = generate_events(tau_true)
    
    prices_df.to_csv(f'{output_dir}/demo_prices.csv', index=False)
    events_df.to_csv(f'{output_dir}/demo_events.csv', index=False)
    
    print(f"✓ Generated {len(prices_df)} days of price data")
    print(f"✓ True change point at day {tau_true} ({prices_df.loc[tau_true, 'date'].date()})")
    print(f"✓ Generated {len(events_df)} events")
    print(f"✓ Saved to {output_dir}/")
    
    return prices_df, events_df, tau_true


def save_data_multiple(output_dir='data', n_changepoints=2):
    """
    Generate and save price and events data with MULTIPLE change points.
    
    Parameters
    ----------
    output_dir : str
        Directory to save CSV files
    n_changepoints : int
        Number of change points (2 or 3)
        
    Returns
    -------
    prices_df : pd.DataFrame
    events_df : pd.DataFrame
    tau_true_list : list of int
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    if n_changepoints == 2:
        mu_true = [30, 50, 70]
        tau_true_pct = [0.33, 0.66]
    elif n_changepoints == 3:
        mu_true = [25, 45, 65, 50]
        tau_true_pct = [0.25, 0.50, 0.75]
    else:
        raise ValueError("n_changepoints must be 2 or 3")
    
    prices_df, tau_true_list = generate_synthetic_prices_multiple(
        n_days=400,
        mu_true=mu_true,
        tau_true_pct=tau_true_pct,
        sigma_true=3.5,
        seed=42
    )
    
    events_df = generate_events_multiple(tau_true_list, n_days=400, seed=42)
    
    prices_df.to_csv(f'{output_dir}/demo_prices_multiple.csv', index=False)
    events_df.to_csv(f'{output_dir}/demo_events_multiple.csv', index=False)
    
    print(f"✓ Generated {len(prices_df)} days of price data with {n_changepoints} change points")
    for i, tau in enumerate(tau_true_list):
        print(f"✓ Change point {i+1} at day {tau} ({prices_df.loc[tau, 'date'].date()})")
    print(f"✓ Generated {len(events_df)} events")
    print(f"✓ Saved to {output_dir}/")
    
    return prices_df, events_df, tau_true_list
