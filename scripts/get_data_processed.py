import os
import pandas as pd

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, ".."))
destination_dir = os.path.join(project_root, "data/raw")

raw_dir = os.path.join(project_root, "data/raw")

books = pd.read_csv(f"{raw_dir}/Books.csv", encoding="latin1", low_memory=False)

def merge_raw_data():

    # Step 1: Load the Data & Rename Columns

    raw_dir = os.path.join(project_root, "data/raw")

    books = pd.read_csv(f"{raw_dir}/Books.csv", encoding="latin1", low_memory=False)
    ratings = pd.read_csv(f"{raw_dir}/Ratings.csv", encoding="latin1")
    users = pd.read_csv(f"{raw_dir}/users.csv", encoding="latin1")

    def clean_columns(df):
        df.columns = df.columns.str.lower().str.replace('-', '_', regex=True)

    for df in [books, ratings, users]:
        clean_columns(df)

    users.rename(columns={'age': 'user_age'}, inplace=True)
    books.rename(columns={col: f"book_{col}" for col in ['year_of_publication', 'publisher','image_url_s', 'image_url_m', 'image_url_l'] if col in books.columns}, inplace=True)

    # Step 2: Handle Missing Values

    books['book_author'] = books['book_author'].fillna('Unknown')
    books['book_publisher'] = books['book_publisher'].fillna('Unknown')
    books['book_image_url_l'] = books['book_image_url_l'].fillna('-')

    books['book_year_of_publication'] = pd.to_numeric(books['book_year_of_publication'], errors='coerce') # Convert the column to numeric, invalid years become NaN
    books['book_year_of_publication'] = books['book_year_of_publication'].fillna(books['book_year_of_publication'].median()) # fill with median because it's robust to outliers

    users['user_age'] = users['user_age'].fillna(users['user_age'].median()).astype(int)

    # Step 3 : Split `location` Column

    location_split = users['location'].str.split(',', expand=True)

    users['user_city'] = location_split[0].str.strip().str.upper()
    users['user_state'] = location_split[1].str.strip().str.upper()
    users['user_country'] = location_split[2].str.strip().str.upper()

    users = users.drop(columns=['location'])

    # Step 4: Merge Datasets

    ratings_with_detailed_users = pd.merge(ratings, users, on='user_id', how='inner')
    ratings_with_detailed_users_and_books = pd.merge(ratings_with_detailed_users, books, on='isbn', how='inner')

    # Step 5: Save Processed Data

    process_dir = os.path.join(project_root, "data/processed")
    processed_path = f"{process_dir}/ratings_with_detailed_users_and_books.csv"
    ratings_with_detailed_users_and_books.to_csv(processed_path, index=False)
    print(f"Processed dataset saved to {processed_path}")

if __name__ == "__main__":
    
    merge_raw_data()