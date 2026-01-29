from pathlib import Path

import pandas as pd

INTEREST_WEIGHTS = {
    'click': 1.0,
    'add_to_cart': 3.0,
    'purchase': 5.0,
}

POPULARITY_WEIGHTS = {
    'click': 0.5,
    'add_to_cart': 3.0,
    'purchase': 5.0,
}

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data'


def data_path(filename: str) -> Path:
    return DATA_DIR / filename


events_csv = data_path('test.csv')
interest_csv = data_path('interest_scores.csv')
popularity_csv = data_path('popularity_scores.csv')


def load_events(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    required_columns = {
        'uid',
        'pid',
        'brand',
        'click',
        'add_to_cart',
        'purchase',
    }
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f'Missing columns: {missing}')

    return df


def compute_interest_scores(df: pd.DataFrame) -> pd.DataFrame:
    scored = df.copy()

    scored['interest_score'] = (
            scored['click'] * INTEREST_WEIGHTS['click']
            + scored['add_to_cart'] * INTEREST_WEIGHTS['add_to_cart']
            + scored['purchase'] * INTEREST_WEIGHTS['purchase']
    )

    result = (
        scored
        .groupby(['uid', 'pid', 'brand'], as_index=False)
        .agg(
            interest_score=('interest_score', 'sum'),
            purchase_count=('purchase', 'sum'),
        )
    )

    return result


def compute_popularity_scores(df: pd.DataFrame) -> pd.DataFrame:
    scored = df.copy()

    scored['popularity_score'] = (
            scored['click'] * POPULARITY_WEIGHTS['click']
            + scored['add_to_cart'] * POPULARITY_WEIGHTS['add_to_cart']
            + scored['purchase'] * POPULARITY_WEIGHTS['purchase']
    )

    result = (
        scored
        .groupby(['pid', 'brand'], as_index=False)
        .agg(
            popularity_score=('popularity_score', 'sum'),
        )
        .sort_values('popularity_score', ascending=False)
    )

    return result


def main():
    df = load_events(events_csv)

    interest_df = compute_interest_scores(df)
    popularity_df = compute_popularity_scores(df)

    interest_df.to_csv(interest_csv, index=False)
    popularity_df.to_csv(popularity_csv, index=False)

    print('Interest and popularity scores computed successfully')


if __name__ == '__main__':
    main()
