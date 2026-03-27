# MLflow Digits Classification Lab

## Overview

This lab demonstrates MLflow experiment tracking, model registry, and hyperparameter optimization using the scikit-learn digits dataset.

**What it does:**
- Trains a baseline LogisticRegression model on binary digit classification (digit ≥ 5 vs. < 5)
- Performs hyperparameter tuning with XGBoost using Hyperopt + SparkTrials
- Logs all experiments, metrics, and models to MLflow
- Registers the best model in MLflow Model Registry
- Validates model outputs with prediction checks

**Runtime:** ~2-3 minutes

---

## Quick Start

### 1. Setup Environment

```bash
conda create -n mlflow-lab python=3.10 -y
conda activate mlflow-lab
cd /path/to/labs/lab5/MLFlow
pip install -r requirements.txt
```

### 2. Run Notebook

```bash
jupyter notebook starter.ipynb
```

Run all cells (Jupyter: **Run → Run All**). The final cell automatically launches MLflow UI.

### 3. View Results

Open **http://localhost:5000** to see:
- Experiments and runs
- Model registry (`digit_classifier`)
- Metrics and parameter comparisons

---

## What the Code Does

| Stage | Details |
|-------|---------|
| **Data** | Loads scikit-learn digits (1,797 samples, 64 features), creates binary target (digit ≥ 5) |
| **Split** | Train 60%, Validation 20%, Test 20% |
| **Baseline** | LogisticRegression (C=1.0), logged to MLflow as `logreg_digits_baseline` |
| **Tuning** | XGBoost + Hyperopt (12 evals, parallelism=4), nested under `xgboost_models` |
| **Registry** | Best model registered as `digit_classifier`, promoted to Production |
| **Validation** | Checks prediction ranges, AUC score, confusion matrix |

---

## Expected Results

- **Baseline AUC:** ~0.85+
- **Best Model AUC:** ~0.90+
- **Final Validation:** All assertions pass 

---

## Files

- `starter.ipynb` - Main notebook with full pipeline
- `requirements.txt` - Dependencies (mlflow, scikit-learn, xgboost, hyperopt, pyspark, etc.)
- `mlruns/` - Auto-generated MLflow tracking directory
