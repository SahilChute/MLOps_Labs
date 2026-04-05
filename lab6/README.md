# PyTorch Hyperparameter Tuning with TensorBoard HParams Dashboard

A hyperparameter tuning lab that performs a grid search over a ResNet-style CNN trained on CIFAR-10, with full TensorBoard HParams dashboard integration.

## Overview

This project trains a small ResNet-style model on the CIFAR-10 image classification dataset while systematically searching over combinations of:

| Hyperparameter   | Values              |
|-------------------|---------------------|
| Learning Rate     | 0.1, 0.01, 0.001   |
| Residual Blocks   | 1, 2, 4            |
| Optimizer         | Adam, SGD           |

All 18 combinations are trained and logged. Results can be explored interactively in TensorBoard's HParams dashboard.

## Project Structure

```
lab6/
├── hparam_tuning.ipynb     # Main notebook (training + grid search)
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── data/                   # CIFAR-10 dataset (auto-downloaded)
│   └── cifar-10-batches-py/
└── logs/                   # TensorBoard logs (auto-generated)
    └── hparam_tuning/
        ├── run-0/
        ├── run-1/
        └── ...
```

---

## Option A: Running on Google Colab

### 1. Upload the notebook

Go to [colab.research.google.com](https://colab.research.google.com) and upload `hparam_tuning.ipynb` via **File → Upload notebook**.

### 2. Enable GPU (recommended)

Go to **Runtime → Change runtime type → T4 GPU** (or any available GPU), then click **Save**.

### 3. Install dependencies

Add and run this cell at the top of the notebook before any other code:

```python
!pip install -q torch torchvision tensorboard
```

> Colab typically has PyTorch pre-installed, but this ensures the correct versions.

### 4. Run all cells

Click **Runtime → Run all**, or step through each cell manually.

### 5. View results

See the **Viewing the TensorBoard Visualization** section below for how to launch and navigate the dashboard.

**Estimated run time on Colab (T4 GPU):** ~15–25 minutes for all 18 trials.

---

## Option B: Running on a Local Machine

### Prerequisites

- Python 3.8+
- A machine with at least 4 GB RAM (GPU recommended but not required)
- Jupyter Notebook or JupyterLab installed

### 1. Clone or download the project

Place all files in a project directory:

```
pytorch-hparam-lab/
├── hparam_tuning.ipynb
├── requirements.txt
└── README.md
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **GPU support (optional):** If you have an NVIDIA GPU, install the CUDA-enabled version of PyTorch instead. Visit [pytorch.org/get-started](https://pytorch.org/get-started/locally/) and select your CUDA version to get the correct install command.

### 4. Launch Jupyter and run the notebook

```bash
jupyter notebook hparam_tuning.ipynb
```

Run all cells in order. On first run, CIFAR-10 (~170 MB) will be downloaded automatically to a `./data/` directory.

### 5. View results

See the **Viewing the TensorBoard Visualization** section below for how to launch and navigate the dashboard.

**Estimated run times (all 18 trials):**

| Hardware         | ~Time     |
|------------------|-----------|
| NVIDIA GPU       | 15–30 min |
| Apple Silicon    | 30–60 min |
| CPU only         | 1–3 hrs   |

> **Tip:** To do a quick smoke test, set `NUM_EPOCHS = 1` and reduce the grid (e.g., two learning rates instead of three) in the notebook.

---

## Viewing the TensorBoard Visualization

TensorBoard is the visualization and analysis layer for this lab. It reads the structured logs written during training and provides an interactive dashboard to compare all 18 hyperparameter configurations. Without it, you'd be manually scanning printed terminal output to compare runs.

> **Important:** At least one trial must finish completely before TensorBoard will have any data to display. If you launch it too early, the dashboard will appear empty.

### On Google Colab

Add and run these two lines as the last cell in your notebook:

```python
%load_ext tensorboard
%tensorboard --logdir ./logs/hparam_tuning
```

TensorBoard will render directly below the cell inside the notebook.

### On a Local Machine

**Option 1 — Inside Jupyter** (add a cell at the end of the notebook):

```python
%load_ext tensorboard
%tensorboard --logdir ./logs/hparam_tuning
```

**Option 2 — From a separate terminal** (with your venv activated):

```bash
tensorboard --logdir ./logs/hparam_tuning
```

Then open your browser to: **http://localhost:6006**

### Navigating the Dashboard

Once TensorBoard is open, you'll see multiple tabs at the top. The two relevant ones are:

**SCALARS tab** — Shows per-epoch line charts for training/test loss and accuracy for each run. Useful for spotting overfitting, slow convergence, or instability in individual trials, but not the main focus of this lab.

**HPARAMS tab** — This is the core of the lab. It aggregates all 18 runs into three interactive views:

1. **Table View** — Lists every run's hyperparameters and final test accuracy side by side. Click column headers to sort by any metric or hyperparameter.
2. **Parallel Coordinates View** — Each vertical axis represents a hyperparameter or the accuracy metric. Each run is drawn as a line connecting its values across axes. Drag along any axis to filter runs and visually identify which hyperparameter ranges correlate with higher accuracy.
3. **Scatter Plot View** — Plot any single hyperparameter against the accuracy metric to see its individual effect on performance.

## Customization

**Change the number of epochs:**
Edit `NUM_EPOCHS` in the notebook. More epochs yield better accuracy but take longer.

**Modify the search space:**
Edit the `HPARAM_SPACE` dictionary to add, remove, or change hyperparameter values:

```python
HPARAM_SPACE = {
    "learning_rate": [0.1, 0.01, 0.001],
    "num_blocks":    [1, 2, 4],
    "optimizer":     ["adam", "sgd"],
    # Add more, e.g.:
    # "batch_size":  [64, 128, 256],
}
```

> If you add a new hyperparameter, make sure to update `run_trial()` to use it.

**Adjust model width:**
Change `base_channels` in the `MiniResNet` constructor call inside `run_trial()` (default is 64).

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError: No module named 'torch'` | Run `pip install -r requirements.txt` (local) or `!pip install torch torchvision tensorboard` (Colab) |
| CIFAR-10 download fails | Check your internet connection, or manually download from [cs.toronto.edu/~kriz/cifar.html](https://www.cs.toronto.edu/~kriz/cifar.html) and place in `./data/` |
| TensorBoard shows no data | Make sure the `--logdir` path matches where logs were written. Wait for at least one trial to finish. |
| TensorBoard won't load in Colab | Restart the runtime and re-run all cells. Try `%reload_ext tensorboard` before the `%tensorboard` command. |
| Out of memory (GPU) | Reduce `BATCH_SIZE` or `base_channels` in the notebook |
| Very slow on CPU | Reduce `NUM_EPOCHS` to 1–2 and shrink the search grid for a quick demo |
| Jupyter not found (local) | Run `pip install notebook` or `pip install jupyterlab` inside your venv |

## Cleaning Up

To start fresh, delete the logs directory:

```bash
rm -rf ./logs/
```
