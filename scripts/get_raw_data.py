import os
import shutil
import kagglehub

def clear_kagglehub_cache(kaggle_path):
    cache_dir = os.path.expanduser(f"~/.cache/kagglehub/datasets/{kaggle_path}")
    if os.path.exists(cache_dir):
        print(f"Clearing KaggleHub cache at: {cache_dir}")
        shutil.rmtree(cache_dir)

def get_kaggle_dataset(kaggle_path,ext_to_search=None):
    """
    Downloads dataset from Kaggle and moves files with specified extensions to a destination folder.
    
    Args:
        ext_to_search (list): List of file extensions to search for (example: ['csv', 'xlsx']).
    """
    if ext_to_search is None:
        ext_to_search = ['csv']  # Default to .csv if no extensions are specified

    # Clear cache to ensure fresh download
    clear_kagglehub_cache(kaggle_path)

    # Define Path

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))

    # Download dataset from Kaggle
    download_path = kagglehub.dataset_download(kaggle_path)
    destination_dir = os.path.join(project_root, "data/raw")
    os.makedirs(destination_dir, exist_ok=True)

    for root, _, files in os.walk(download_path):
        for file in files:
            if any(file.endswith(f".{ext}") for ext in ext_to_search):
                source_file = os.path.join(root, file)
                destination_file = os.path.join(destination_dir, file)

                if os.path.exists(destination_file):
                    os.remove(destination_file)
                shutil.move(source_file, destination_file)
                print(f"Moved file: {source_file} -> {destination_file}")

    print(f"Files with extensions {ext_to_search} have been successfully replaced.")

if __name__ == "__main__":
    
    get_kaggle_dataset(kaggle_path='arashnic/book-recommendation-dataset',ext_to_search=['csv', 'xlsx'])