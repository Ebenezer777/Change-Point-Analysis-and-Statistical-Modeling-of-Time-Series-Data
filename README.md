# Bayesian Inference & MCMC: Change Point Detection Demo

A beginner-friendly tutorial demonstrating **Bayesian inference** and **Markov Chain Monte Carlo (MCMC)** using a simple time-series change point detection problem.

## 🎯 What This Project Teaches

This project provides a hands-on introduction to:

- **Bayesian inference**: Understanding priors, likelihoods, and posteriors
- **MCMC sampling**: How to approximate complex posterior distributions
- **Change point detection**: Finding regime shifts in time series data
- **Uncertainty quantification**: Getting credible intervals, not just point estimates
- **Event attribution**: Linking statistical changes to real-world events

## 📊 The Problem

We analyze synthetic price time series (similar to oil prices) that experience **regime shifts**:

**Notebook 1: Single Change Point**
- Prices start around $30 (low regime)
- At some point, they jump to $60 (high regime)
- We want to detect **when** this change occurred and **how large** it was

**Notebook 2: Multiple Change Points** (NEW!)
- Prices go through 3-4 different regimes (e.g., $30 → $50 → $70)
- Detect 2-3 change points simultaneously
- Understand the complexity and challenges of multiple regime shifts

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.9 or higher
- pip or conda

### Installation

1. **Clone the repository** (or navigate to the project directory):
   ```bash
   cd Bayesian-inference-and-Monte-Carlo-Markov-Chain
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Demo

1. **Launch Jupyter**:
   ```bash
   jupyter notebook
   ```

2. **Choose a notebook**:
   - **Start here**: `notebooks/01_demo_bayes_changepoint.ipynb` (single change point)
   - **Advanced**: `notebooks/02_multiple_changepoints.ipynb` (2-3 change points)
   - Run all cells sequentially (Cell → Run All)

3. **Expected outputs**:
   - `data/demo_prices*.csv` - Synthetic price data
   - `data/demo_events*.csv` - Events table
   - `outputs/*.png` - All visualization plots
   - Printed diagnostics and summary statistics

## 📁 Project Structure

```
.
├── README.md                          # This file
├── EXPLANATION.md                     # Detailed explanation of methods and outputs
├── requirements.txt                   # Python dependencies
├── notebooks/
│   ├── 01_demo_bayes_changepoint.ipynb     # Single change point tutorial
│   └── 02_multiple_changepoints.ipynb      # Multiple change points (2-3 CPs)
├── src/
│   ├── __init__.py
│   ├── demo_data.py                   # Data generation (single & multiple CPs)
│   └── plots.py                       # Visualization helpers
├── data/                              # Generated CSV files
│   ├── demo_prices.csv
│   ├── demo_events.csv
│   ├── demo_prices_multiple.csv
│   └── demo_events_multiple.csv
└── outputs/                           # Saved plots
    ├── 01_price_with_true_changepoint.png
    ├── 02_price_with_events.png
    ├── 03_trace_plots.png
    ├── 04_posterior_tau.png
    ├── 05_posterior_means.png
    ├── 06_price_with_estimated_changepoint.png
    └── 07_comparison_true_vs_estimated.png
```

## 🧠 Key Concepts Covered

### 1. Bayesian Model Components

- **Priors**: Initial beliefs about parameters
  - `τ ~ DiscreteUniform(0, N-1)` - Change point location
  - `μ₁ ~ Normal(30, 10)` - Mean before change
  - `μ₂ ~ Normal(60, 10)` - Mean after change
  - `σ ~ HalfNormal(5)` - Noise level

- **Likelihood**: How well parameters explain data
  - `price[i] ~ Normal(μ₁, σ)` if `i < τ`
  - `price[i] ~ Normal(μ₂, σ)` if `i ≥ τ`

- **Posterior**: Updated beliefs after seeing data
  - Computed via MCMC sampling (not analytically)

### 2. MCMC Diagnostics

- **Trace plots**: Visual check for convergence
- **R-hat**: Should be ≈ 1.00 (measures chain convergence)
- **ESS**: Effective sample size (accounts for autocorrelation)

### 3. Visualizations

All plots are saved to `outputs/` and include:
1. Price with true change point
2. Price with events overlay
3. MCMC trace plots
4. Posterior distribution of change point
5. Posterior distributions of means (μ₁, μ₂)
6. Price with estimated change point
7. Comparison: true vs estimated

## 🛢️ Connection to Brent Oil Prices

This demo is designed as a stepping stone to analyzing **real Brent crude oil prices**:

- **Real-world application**: Detect regime shifts in oil markets
- **Event attribution**: Link price changes to geopolitical events, supply shocks, etc.
- **Extensions**: Multiple change points, trend modeling, predictive forecasting

See the notebook's final section for detailed discussion.

## 📚 Learning Path

1. **Start here**: Run the notebook and read the explanations
2. **Experiment**: Change priors, add noise, modify the true change point
3. **Extend**: Try multiple change points or different likelihood models
4. **Apply**: Use real Brent oil data instead of synthetic data

## 🔗 Resources

- **PyMC Documentation**: https://www.pymc.io/
- **ArviZ (Diagnostics)**: https://arviz-devs.github.io/arviz/
- **Bayesian Methods for Hackers**: https://github.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers

## 📄 License

This is an educational demo project. Feel free to use and modify for learning purposes.

## 🤝 Contributing

This is a teaching resource. Suggestions for improving clarity or adding beginner-friendly features are welcome!

## ❓ Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'pymc'`
- **Solution**: Make sure you've activated your virtual environment and run `pip install -r requirements.txt`

**Issue**: MCMC sampling is very slow
- **Solution**: Reduce `draws` and `tune` to 500 each for faster testing

**Issue**: Plots don't show up in Jupyter
- **Solution**: Make sure you have `%matplotlib inline` or are using a compatible backend

**Issue**: R-hat values are high (> 1.01)
- **Solution**: Increase `tune` to 2000 or adjust `target_accept` to 0.95

## 📧 Questions?

For questions about Bayesian inference or MCMC, consult the resources above or PyMC community forums.
