import os
import pandas as pd
import joblib
import random
import json

def load_model(model_path):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")

    model = joblib.load(model_path)
    print(f"Loaded model from {model_path}.")

    return model

def load_data(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Processed file not found: {file_path}")

    # Determine the file extension
    _, file_extension = os.path.splitext(file_path)

    if file_extension.lower() == '.csv':
        df = pd.read_csv(file_path)
    elif file_extension.lower() in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

    print(f"Loaded processed dataset. Shape: {df.shape}")
    return df

def recommend_for_user(
    model,
    df,
    user_id,
    user_col='user_id',
    item_col='isbn',
    rating_col='book_rating',
    title_col='book_title',
    top_n=5,
    exclude_rated=False
):
    """
    Recommend top_n items for a given user using a trained Surprise model.
    If the user is unknown, return globally popular items based on average rating_col.

    :param model:   Recommendation model.
    :param df:      Pandas DataFrame with user/item/rating data (and possibly a title column).
    :param user_id:      The user to recommend items for.
    :param user_col:     Name of the user ID column in df.
    :param item_col:     Name of the item ID column in df.
    :param rating_col:   Name of the column that holds numeric ratings.
    :param title_col:    Name of the column for item titles (if any).
    :param top_n:        Number of items to recommend.
    :param exclude_rated:If True, exclude items the user already rated.
    :return:             A list of (item_id, predicted_score, item_title).
    """

    try:
        # Check if user is known to the model
        model.trainset.to_inner_uid(str(user_id))

        # All item IDs in df
        all_items = df[item_col].unique()

        if exclude_rated:
            # Items the user already rated
            already_rated = df.loc[df[user_col] == user_id, item_col].unique()
            candidate_items = [itm for itm in all_items if itm not in already_rated]
        else:
            candidate_items = all_items

        # Predict ratings for candidate items
        predictions = []
        for itm in candidate_items:
            pred = model.predict(str(user_id), str(itm), verbose=False)
            predictions.append((itm, pred.est))

        # Sort by predicted rating, descending
        predictions.sort(key=lambda x: x[1], reverse=True)
        top_preds = predictions[:top_n]

        # Map item ID -> Title
        if title_col in df.columns:
            item_to_title = (df.drop_duplicates(item_col)
                             .set_index(item_col)[title_col]
                             .to_dict())
        else:
            item_to_title = {}

        results = [(itm, score, item_to_title.get(itm, "Unknown Title")) for itm, score in top_preds]
        return results

    except ValueError:
        # Fallback for unknown user: pick top globally rated items
        top_global = (
            df
            .groupby(item_col)[rating_col]
            .mean()
            .sort_values(ascending=False)
            .head(top_n)
            .index.tolist()
        )

        if title_col in df.columns:
            item_to_title = (df.drop_duplicates(item_col)
                             .set_index(item_col)[title_col]
                             .to_dict())
        else:
            item_to_title = {}

        return [(itm, 0.0, item_to_title.get(itm, "Unknown Title")) for itm in top_global]

if __name__ == "__main__":

    # Define Variable
    df = load_data("./data/processed/ratings_with_detailed_users_and_books.csv")
    model = load_model("./models/svdpp.joblib")
    user_col='user_id'
    item_col='isbn'
    rating_col='book_rating'
    title_col='book_title'
    top_n=5
    exclude_rated=True
    user_list = df[user_col].unique().tolist()
    user_size = 10 # fill with 0 if we want to take all user

    # Process Recommendation
    sampled_users = user_list if user_size == 0 else random.sample(user_list, min(user_size, len(user_list)))

    recommendations_dict = {}

    for u in sampled_users:
        recs  = recommend_for_user(model,
                                   df,
                                   user_id=u,
                                   user_col=user_col,
                                   item_col=item_col,
                                   rating_col=rating_col,
                                   title_col=title_col,
                                   top_n=top_n,
                                   exclude_rated=exclude_rated)

        rec_list = []
        for (item_id, score, title) in recs:
            rec_list.append({
                "item_id": str(item_id),
                "predicted_score": float(score),
                "title": title
            })

        recommendations_dict[str(u)] = rec_list

    # Save to a JSON file
    output_path = "./data/output/user_recommendations.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(recommendations_dict, f, ensure_ascii=False, indent=2)

    print(f"JSON file saved to {output_path}")