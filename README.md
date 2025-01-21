# Generalized Recommendation System

This repository demonstrates how to build a **recommendation system** that can handle different item datasets such as books, or movies. It includes data preprocessing, model training with [Surprise](https://surpriselib.com/), and a script that generates user-specific recommendations in JSON format.

This project uses [Surprise](https://surpriselib.com/) for collaborative filtering. We focus on `(user, item, rating)` input, but it can be adapted to other data structures such as `(user, item, sales_qty)`

---

- **data**: Holds raw CSVs (downloaded from Kaggle), processed data (cleaned & merged), and final output (`user_recommendations.json`).
- **images**: Plots or figures from EDA
- **models**: Stores trained model files (`svd.joblib` and `svdpp.joblib`).
- **notebooks**: Jupyter notebooks for data preprocessing (`01-preprocessing.ipynb`) and model building (`02-model-preparation-and-building.ipynb`).
- **scripts**: Python scripts for:
  - `get_raw_data.py` to fetch Kaggle data,
  - `get_recommendation.py` to generate a JSON file of user recommendations.

---

## Project Flow

### 1. Acquire Dataset  
Run `scripts/get_raw_data.py` to download data from Kaggle:

- **Script**: `get_raw_data.py`  
- **Destination**: `data/raw/`  
- **Kaggle Path**: `'arashnic/book-recommendation-dataset'`  

Example:
```bash
python scripts/get_raw_data.py
```
After this step, `Books.csv`, `Ratings.csv`, and `Users.csv` appear in **`data/raw`**.

### 2. Data Preprocessing & EDA  
**`notebooks/01-preprocessing.ipynb`** to:
1. Load raw CSVs (`Books.csv`, `Ratings.csv`, `Users.csv`).
2. Clean & merge them into a single dataset (`ratings_with_detailed_users_and_books.csv`) saved in **`data/processed`**.
3. Perform EDA & save any plots in **`images/`**.

### 3. Build & Train the Model  
**`notebooks/02-model-preparation-and-building.ipynb`** to:
1. Load the processed CSV (`ratings_with_detailed_users_and_books.csv`).
2. Create a recommendation model (SVD, SVD++) using [Surprise](https://surpriselib.com/).
3. Optionally tune hyperparameters with `GridSearchCV`.
4. Save the final model in **`models/`** (`svd.joblib`, `svdpp.joblib`).

### 4. Generate User Recommendations  
Run **`scripts/get_recommendation.py`** to produce recommendations for all (or a subset of) users:

- **Loads** the model from `models/svdpp.joblib` (or any chosen model).
- **Loads** the processed CSV.
- Loops through a sample of users, calls `recommend_for_user()` to get top-N recommendations.
- **Saves** results as **`user_recommendations.json`** in **`data/output`**.

Example usage:
```bash
python scripts/get_recommendation.py
```
---

## End-to-End

1. **`get_raw_data.py`** → downloads raw CSVs into `data/raw/`.  
2. **`01-preprocessing.ipynb`** → merges & cleans data → `data/processed/ratings_with_detailed_users_and_books.csv` + EDA plots in `images/`.  
3. **`02-model-preparation-and-building.ipynb`** → trains & saves model (`svd.joblib`, `svdpp.joblib`) in `models/`.  
4. **`get_recommendation.py`** → loads model + data → generates a JSON file of user recommendations in `data/output/`.