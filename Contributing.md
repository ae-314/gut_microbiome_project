# Contribution guideline

This document provides an analysis of the current code structure in the `modularize-training` branch of the `AI-For-Food-Allergies/gut_microbiome_project` repository and outlines the necessary interventions as defined by the open GitHub issues.

## 1. Current Code Structure

### 1.1. High-Level Overview

The project is structured around the core components of a machine learning workflow, with dedicated directories and files for each step.

| Component | Directory/File | Purpose |
| :--- | :--- | :--- |
| **Data Preparation** | `data_preprocessing/` | Contains logic for cleaning, transforming, and preparing raw data. |
| **Model Components** | `modules/` | Intended to house reusable classes and functions for the model architecture (e.g., `MicrobiomeTransformer`). |
| **Training/Execution** | `train.py`, `main.py` | The main entry points for running the training and overall pipeline. |
| **Evaluation** | `evaluation/` | Intended to house scripts or modules for model performance assessment. |
| **Configuration** | `pyproject.toml` | Project dependencies and packaging. |
| **Utilities** | `data_loading.py` | Contains functions for loading data, which is a key part of the workflow. |
| **Examples/Legacy** | `example_scripts/` | Example scripts training a classifier based on MicrobiomeTransformer(`predict_milk.py`, `predict_hla.py`) |

### 1.2. Modular approach


*   **Separation of Concerns:** The creation of `data_preprocessing/`, `modules/`, and `evaluation/` clearly separates the data, model, and assessment logic.
*   **Centralized Execution:** `main.py` and `train.py` serve as clean entry points, abstracting the complexity of the underlying modules.
*   **Data Handling:** Use `data_loading.py` to separate the I/O logic from the core ML algorithms.

## 2. Open issues

| Issue ID | Title | Description of Intervention |
| :--- | :--- | :--- |
| \#8 | **Implement data loading** | This task involves refactoring the data loading logic into a dedicated, robust module that handles all I/O, ID alignment, and data structure creation, likely consolidating logic from `data_loading.py` and `utils.py`. |
| \#7 | **Implement training script** | This task requires finalizing and centralizing the training loop logic within `train.py`, ensuring it correctly imports the necessary data loader and model modules to execute the full training process (e.g., cross-validation, hyperparameter tuning). |
| \#6 | **Implement modules** | This task is to complete the implementation of all reusable model components (e.g., the `MicrobiomeTransformer` wrapper, feature extraction logic) and place them within the `modules/` directory, decoupling the model logic from the training script. |
| \#5 | **Implement evaluation script** | This task is to develop a dedicated script or module (e.g., `evaluation/evaluate.py`) that takes a trained model and test data, and produces the required metrics and visualizations, replacing the evaluation logic currently embedded in the legacy scripts. |

## 3. Development Roadmap
### Phase 1: Core Module Implementation

The first step is to build the reusable components that the main scripts will rely on.

1.  **Address Issue \#6: Implement modules**
    *   Define and implement the core model classes (e.g., `MicrobiomeModel`, `FeatureExtractor`) in the `modules/` directory.
    *   Ensure these modules are clean, well-documented, and only handle model-related logic.

2.  **Address Issue \#8: Implement data loading**
    *   Create a dedicated data module (e.g., `data_preprocessing/data_loader.py`).
    *   Move all data-related functions (SRA ↔ MicrobeAtlas ↔ DIABIMMUNE mappings, embedding loading, sample vector building) from `data_loading.py` and `utils.py` into this new module.
    *   The goal is to have a single, clean interface for retrieving processed data ready for training.

### Phase 2: Pipeline Integration

Once the core components are modularized, they can be integrated into the main execution scripts.

3.  **Address Issue \#7: Implement training script**
    *   Refine `train.py` to import the new data loader and model modules.
    *   Implement the final, clean training loop, including the 5-fold Stratified CV and cohort balancing logic.
    *   Ensure the script saves the trained model artifacts.

4.  **Address Issue \#5: Implement evaluation script**
    *   Create `evaluation/evaluate.py`.
    *   Implement the logic to load a trained model, load the test data using the new data loader, compute metrics, and generate the required plots (`milk_cm.png`, `fla_cm.png`).
    *   This script should be runnable independently to assess any trained model.

### Phase 3: Cleanup and Finalization

5.  **Configuration Refinement:** Review `config.yaml` and ensure all new modules and scripts correctly reference the configuration parameters.
6.  **Documentation:** Update the main `README.md` to reflect the new modular structure and provide clear instructions on how to run the `train.py` and `evaluation/evaluate.py` scripts.
7.  **Deprecation:** Remove or clearly mark the legacy/notebook-like scripts in `example_scripts/` to prevent confusion.