# Digits Classification MLflow Lab

This lab walks you through training and tracking a simple binary classifier on the scikit-learn **digits** dataset using **MLflow**. You will:

- Load the built-in digits dataset (no external files needed)
- Train a baseline **logistic regression** model
- Track parameters, metrics, and the model artifact with MLflow
- Register the model and (optionally) serve it for inference

The code for the lab lives in `starter.ipynb`.

---

## 1. Prerequisites

You can run this lab on macOS, Windows, or Linux as long as you have:

- **Conda** (Anaconda or Miniconda) installed, or Python 3.9+ with `pip`
- Internet access to install Python packages

Everything else (MLflow, scikit-learn, etc.) is installed from `requirements.txt`.

---

## 2. Set up the environment

From any shell (Terminal, PowerShell, Command Prompt), run:

```bash
# (Optional but recommended) Create a fresh conda environment
conda create -n mlflow-lab python=3.10 -y

# Activate the environment
conda activate mlflow-lab

# Move into the lab folder
cd /path/to/labs/lab5/MLFlow

# Install required packages
pip install -r requirements.txt
```

If you don’t use conda, you can instead do:

```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate

cd /path/to/labs/lab5/MLFlow
pip install -r requirements.txt
```

---

## 3. Run the lab notebook

With the environment activated and dependencies installed:

```bash
cd /path/to/labs/lab5/MLFlow
jupyter notebook starter.ipynb
```

Then in your browser:

1. Make sure the kernel is using your environment (e.g. `mlflow-lab`).
2. Run all cells from top to bottom (for example: **Run → Run All** in the Jupyter menu).

The notebook will:

- Load and explore the digits dataset
- Create a binary label (digit ≥ 5 vs. < 5)
- Split data into train/validation/test
- Train a logistic regression model and log to MLflow
- Register the model under the name `digit_classifier`

---

## 4. View Experiments & Results in MLflow UI

In a separate terminal (with the same environment activated):

```bash
cd /path/to/labs/lab5/MLFlow
conda activate mlflow-lab
mlflow ui --port 5000
```

Then open **http://localhost:5000** in your browser to see:

- 📊 **Experiments** - All training runs (baseline + XGBoost)
- 🏆 **Models** - Registered `digit_classifier` model with versions
- 📈 **Metrics** - AUC scores, parameters, and performance comparisons
- ✅ **Production Model** - Best model promoted to production stage

---

## 5. Understanding Results

After running the notebook, you'll see:

- **Baseline Model (LogisticRegression):**
  - Run name: `logreg_digits_baseline`
  - AUC score should be > 0.85

- **Advanced Model (XGBoost + Hyperopt):**
  - Run name: `xgboost_models` with nested tuning runs
  - Best model selected and promoted to Production
  - AUC score should be > 0.90

- **Validation:** Final cell displays prediction ranges, confusion matrix, and classification metrics

---

## Key Learnings

- **Data Loading**: Using scikit-learn's built-in digits dataset
- **Binary Classification**: Creating custom labels (digit ≥ 5 vs. < 5)
- **Experiment Tracking**: Logging parameters and metrics with MLflow
- **Model Registry**: Registering and versioning trained models
- **Hyperparameter Tuning**: Using Hyperopt + SparkTrials for optimization
- **Model Validation**: Verifying predictions and performance metrics

---

## 6. (Optional) Serve the registered model

Once you've run the notebook and registered the model, you can serve the production version locally:

```bash
mlflow models serve \
  --env-manager=local \
  -m models:/digit_classifier/production \
  -h 0.0.0.0 -p 5001
```

Send a test request from another terminal or a Python script using the payload format shown in the last cells of the notebook (it uses the `dataframe_split` format based on `X_test`).

This is enough to run the lab end‑to‑end on any machine with Python and MLflow installed.

### Explanation:
We use the requests library to send a POST request to the deployed model's API endpoint.
The URL should be set to the correct endpoint where the model is served.
We prepare the input data in the desired format and send it as JSON in the request.
The response contains the model's predictions, which we extract using response.json().
Finally, we print the predictions.
Expected Output:
The output will be the model's predictions for the input data sent in the request.

### Note:
Real-time inference allows you to use the deployed model to make predictions on new data as it becomes available.
Ensure that the model serving endpoint is running and accessible before making real-time inference requests.
Replace the endpoint URL with the actual URL where your model is served.

## Step 18: Cleaning Up and Conclusion

In this final step, we'll wrap up the lab and perform any necessary clean-up tasks.

### Clean-Up Tasks:

- **Stop the Model Serving**: If you've started the model serving process, make sure to stop it when you're done with real-time inference. You can do this by stopping the MLflow Model Serving process or using appropriate commands.

- **Close Resources**: Ensure that any resources or connections used during the lab are properly closed or released.

- **Save Documentation**: Save this lab documentation for future reference or sharing with others.

### Conclusion:

In this lab, we've covered various aspects of the machine learning lifecycle, including data preparation, model training, evaluation, deployment, and real-time inference. Here are the key takeaways:

- Data preparation is essential for training and evaluating machine learning models. Cleaning, transforming, and splitting the data are crucial steps.

- Model training involves selecting an appropriate algorithm, training the model, and evaluating its performance using relevant metrics.

- Model deployment involves registering the model, transitioning it to the production stage, and serving it for real-time inference.

- Real-time inference allows you to use the deployed model to make predictions on new data as it arrives.

By following these steps, you can effectively develop and deploy machine learning models for various applications.

Thank you for completing this lab!




