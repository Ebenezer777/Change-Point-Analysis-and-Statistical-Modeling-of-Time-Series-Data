import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import arviz as az
import os

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def plot_price_with_changepoint(df, tau, tau_label="Change Point", 
                                  output_path=None, title="Price Time Series"):
    """
    Plot price time series with a vertical line at the change point.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with 'date' and 'price' columns
    tau : int
        Change point index
    tau_label : str
        Label for the change point line
    output_path : str, optional
        Path to save the figure
    title : str
        Plot title
    """
    fig, ax = plt.subplots(figsize=(14, 6))
    
    ax.plot(df['date'], df['price'], linewidth=1.5, alpha=0.8, label='Price')
    ax.axvline(df.loc[tau, 'date'], color='red', linestyle='--', 
               linewidth=2, label=f'{tau_label} (day {tau})')
    
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    plt.show()


def plot_price_with_events(df, events_df, tau_true=None, output_path=None):
    """
    Plot price time series with event overlays.
    
    Parameters
    ----------
    df : pd.DataFrame
        Price data
    events_df : pd.DataFrame
        Events data with start_date, end_date, event_name
    tau_true : int, optional
        True change point to overlay
    output_path : str, optional
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=(14, 6))
    
    ax.plot(df['date'], df['price'], linewidth=1.5, alpha=0.8, 
            color='steelblue', label='Price')
    
    colors = ['orange', 'green', 'purple', 'brown']
    for idx, row in events_df.iterrows():
        ax.axvspan(row['start_date'], row['end_date'], 
                   alpha=0.2, color=colors[idx % len(colors)],
                   label=row['event_name'])
    
    if tau_true is not None:
        ax.axvline(df.loc[tau_true, 'date'], color='red', linestyle='--', 
                   linewidth=2, label=f'True Change Point (day {tau_true})')
    
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price', fontsize=12)
    ax.set_title('Price Time Series with Events Overlay', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10, loc='upper left')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    plt.show()


def plot_posterior_tau(trace, tau_true=None, output_path=None):
    """
    Plot posterior distribution of the change point tau.
    
    Parameters
    ----------
    trace : arviz.InferenceData
        MCMC trace
    tau_true : int, optional
        True change point value
    output_path : str, optional
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    tau_samples = trace.posterior['tau'].values.flatten()
    
    ax.hist(tau_samples, bins=50, density=True, alpha=0.7, 
            color='steelblue', edgecolor='black', label='Posterior samples')
    
    tau_mean = tau_samples.mean()
    tau_median = np.median(tau_samples)
    
    ax.axvline(tau_mean, color='blue', linestyle='-', linewidth=2, 
               label=f'Posterior mean = {tau_mean:.1f}')
    ax.axvline(tau_median, color='darkblue', linestyle='--', linewidth=2, 
               label=f'Posterior median = {tau_median:.1f}')
    
    if tau_true is not None:
        ax.axvline(tau_true, color='red', linestyle='--', linewidth=2, 
                   label=f'True τ = {tau_true}')
    
    ax.set_xlabel('Change Point (day index)', fontsize=12)
    ax.set_ylabel('Posterior Density', fontsize=12)
    ax.set_title('Posterior Distribution of Change Point τ', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    plt.show()


def plot_posterior_means(trace, mu1_true=None, mu2_true=None, output_path=None):
    """
    Plot posterior distributions of mu1 and mu2 (before/after means).
    
    Parameters
    ----------
    trace : arviz.InferenceData
        MCMC trace
    mu1_true : float, optional
        True mu1 value
    mu2_true : float, optional
        True mu2 value
    output_path : str, optional
        Path to save figure
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    mu1_samples = trace.posterior['mu1'].values.flatten()
    mu2_samples = trace.posterior['mu2'].values.flatten()
    
    axes[0].hist(mu1_samples, bins=40, density=True, alpha=0.7, 
                 color='coral', edgecolor='black')
    axes[0].axvline(mu1_samples.mean(), color='darkred', linestyle='-', 
                    linewidth=2, label=f'Posterior mean = {mu1_samples.mean():.2f}')
    if mu1_true is not None:
        axes[0].axvline(mu1_true, color='red', linestyle='--', 
                        linewidth=2, label=f'True μ₁ = {mu1_true}')
    axes[0].set_xlabel('μ₁ (mean before change)', fontsize=12)
    axes[0].set_ylabel('Density', fontsize=12)
    axes[0].set_title('Posterior: μ₁ (Before)', fontsize=13, fontweight='bold')
    axes[0].legend(fontsize=10)
    axes[0].grid(True, alpha=0.3)
    
    axes[1].hist(mu2_samples, bins=40, density=True, alpha=0.7, 
                 color='skyblue', edgecolor='black')
    axes[1].axvline(mu2_samples.mean(), color='darkblue', linestyle='-', 
                    linewidth=2, label=f'Posterior mean = {mu2_samples.mean():.2f}')
    if mu2_true is not None:
        axes[1].axvline(mu2_true, color='red', linestyle='--', 
                        linewidth=2, label=f'True μ₂ = {mu2_true}')
    axes[1].set_xlabel('μ₂ (mean after change)', fontsize=12)
    axes[1].set_ylabel('Density', fontsize=12)
    axes[1].set_title('Posterior: μ₂ (After)', fontsize=13, fontweight='bold')
    axes[1].legend(fontsize=10)
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    plt.show()


def plot_trace_summary(trace, output_path=None):
    """
    Plot trace plots for all parameters.
    
    Parameters
    ----------
    trace : arviz.InferenceData
        MCMC trace
    output_path : str, optional
        Path to save figure
    """
    fig = az.plot_trace(trace, var_names=['tau', 'mu1', 'mu2', 'sigma'],
                        figsize=(14, 10))
    
    plt.suptitle('MCMC Trace Plots', fontsize=16, fontweight='bold', y=1.001)
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    plt.show()


def plot_price_with_multiple_changepoints(df, tau_list, tau_labels=None, 
                                          output_path=None, title="Price Time Series"):
    """
    Plot price time series with MULTIPLE vertical lines at change points.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with 'date' and 'price' columns
    tau_list : list of int
        List of change point indices
    tau_labels : list of str, optional
        Labels for each change point
    output_path : str, optional
        Path to save the figure
    title : str
        Plot title
    """
    fig, ax = plt.subplots(figsize=(14, 6))
    
    ax.plot(df['date'], df['price'], linewidth=1.5, alpha=0.8, label='Price', color='steelblue')
    
    colors = ['red', 'orange', 'purple', 'brown', 'green']
    
    for i, tau in enumerate(tau_list):
        if tau_labels:
            label = f'{tau_labels[i]} (day {tau})'
        else:
            label = f'Change Point {i+1} (day {tau})'
        
        ax.axvline(df.loc[tau, 'date'], color=colors[i % len(colors)], 
                   linestyle='--', linewidth=2, label=label)
    
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    plt.show()


def plot_price_with_events_multiple(df, events_df, tau_true_list=None, output_path=None):
    """
    Plot price time series with event overlays and MULTIPLE change points.
    
    Parameters
    ----------
    df : pd.DataFrame
        Price data
    events_df : pd.DataFrame
        Events data with start_date, end_date, event_name
    tau_true_list : list of int, optional
        List of true change points to overlay
    output_path : str, optional
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=(14, 6))
    
    ax.plot(df['date'], df['price'], linewidth=1.5, alpha=0.8, 
            color='steelblue', label='Price')
    
    event_colors = ['orange', 'green', 'purple', 'brown', 'pink', 'cyan']
    for idx, row in events_df.iterrows():
        ax.axvspan(row['start_date'], row['end_date'], 
                   alpha=0.2, color=event_colors[idx % len(event_colors)],
                   label=row['event_name'])
    
    if tau_true_list is not None:
        cp_colors = ['red', 'darkred', 'crimson']
        for i, tau in enumerate(tau_true_list):
            ax.axvline(df.loc[tau, 'date'], color=cp_colors[i % len(cp_colors)], 
                       linestyle='--', linewidth=2, 
                       label=f'True Change Point {i+1} (day {tau})')
    
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price', fontsize=12)
    ax.set_title('Price Time Series with Events & Multiple Change Points', 
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=9, loc='upper left', ncol=2)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    plt.show()


def plot_posterior_tau_multiple(trace, n_changepoints, tau_true_list=None, output_path=None):
    """
    Plot posterior distributions of MULTIPLE change points.
    
    Parameters
    ----------
    trace : arviz.InferenceData
        MCMC trace
    n_changepoints : int
        Number of change points
    tau_true_list : list of int, optional
        List of true change point values
    output_path : str, optional
        Path to save figure
    """
    fig, axes = plt.subplots(1, n_changepoints, figsize=(7*n_changepoints, 5))
    
    if n_changepoints == 1:
        axes = [axes]
    
    colors = ['steelblue', 'coral', 'mediumseagreen']
    
    for i in range(n_changepoints):
        tau_samples = trace.posterior['tau'].values[:, :, i].flatten()
        
        axes[i].hist(tau_samples, bins=50, density=True, alpha=0.7, 
                    color=colors[i % len(colors)], edgecolor='black', 
                    label='Posterior samples')
        
        tau_mean = tau_samples.mean()
        tau_median = np.median(tau_samples)
        
        axes[i].axvline(tau_mean, color='blue', linestyle='-', linewidth=2, 
                       label=f'Mean = {tau_mean:.1f}')
        axes[i].axvline(tau_median, color='darkblue', linestyle='--', linewidth=2, 
                       label=f'Median = {tau_median:.1f}')
        
        if tau_true_list is not None and i < len(tau_true_list):
            axes[i].axvline(tau_true_list[i], color='red', linestyle='--', linewidth=2, 
                           label=f'True τ{i+1} = {tau_true_list[i]}')
        
        axes[i].set_xlabel(f'Change Point {i+1} (day index)', fontsize=12)
        axes[i].set_ylabel('Posterior Density', fontsize=12)
        axes[i].set_title(f'Posterior: τ{i+1}', fontsize=13, fontweight='bold')
        axes[i].legend(fontsize=10)
        axes[i].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    plt.show()


def plot_posterior_means_multiple(trace, n_regimes, mu_true_list=None, output_path=None):
    """
    Plot posterior distributions of MULTIPLE regime means.
    
    Parameters
    ----------
    trace : arviz.InferenceData
        MCMC trace
    n_regimes : int
        Number of regimes (n_changepoints + 1)
    mu_true_list : list of float, optional
        List of true mean values
    output_path : str, optional
        Path to save figure
    """
    fig, axes = plt.subplots(1, n_regimes, figsize=(5*n_regimes, 5))
    
    if n_regimes == 1:
        axes = [axes]
    
    colors = ['coral', 'skyblue', 'lightgreen', 'plum']
    
    for i in range(n_regimes):
        mu_samples = trace.posterior['mu'].values[:, :, i].flatten()
        
        axes[i].hist(mu_samples, bins=40, density=True, alpha=0.7, 
                    color=colors[i % len(colors)], edgecolor='black')
        axes[i].axvline(mu_samples.mean(), color='darkred', linestyle='-', 
                       linewidth=2, label=f'Mean = {mu_samples.mean():.2f}')
        
        if mu_true_list is not None and i < len(mu_true_list):
            axes[i].axvline(mu_true_list[i], color='red', linestyle='--', 
                           linewidth=2, label=f'True μ{i+1} = {mu_true_list[i]}')
        
        axes[i].set_xlabel(f'μ{i+1} (Regime {i+1} mean)', fontsize=12)
        axes[i].set_ylabel('Density', fontsize=12)
        axes[i].set_title(f'Posterior: μ{i+1}', fontsize=13, fontweight='bold')
        axes[i].legend(fontsize=10)
        axes[i].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    plt.show()
