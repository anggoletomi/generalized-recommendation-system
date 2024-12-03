# Generalized Recommendation System

## Repository Structure

This repository is organized into the following folders:

1. **`notebooks/`**: Contains detailed analyses and exploratory steps of the project.
2. **`scripts/`**: Stores automated scripts for data processing and other tasks.
3. **`data/`**: Reserved for raw and processed data files.

   ### Note on Data Files

   The following data files are not included in this repository because they are too large to be stored in a Git repository. Instead, you can generate raw and processed data files using the provided scripts.

   - **`data/raw/`**:  
     This folder is intended for raw data files. You can generate raw data files by running the script below:

     ```bash
     python scripts/get_data_raw.py
     ```

   - **`data/processed/`**:  
     This folder is intended for processed data files. You can generate these processed files by running the script below:

     ```bash
     python scripts/get_data_processed.py
     ``` 