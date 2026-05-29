from pathlib import Path
import pandas as pd


DATA_PATH = Path("data/bitext.csv")


def load_dataset() -> pd.DataFrame:
    """
    Load the Bitext customer service dataset.
    """
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH}. "
            "Please place bitext.csv inside the data folder."
        )

    df = pd.read_csv(DATA_PATH)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df