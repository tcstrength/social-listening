import pandas as pd

__PREFIX = "./data/sentiment"
LABEL_TO_INT = {"NEG": 0, "NEU": 0, "POS": 1}
INT_TO_LABEL = {0: "NEG", 1: "POS"}

def load_all_tweets() -> list:
    df = pd.read_csv(f"{__PREFIX}/part1.csv")
    df["content"] = df["content"].astype(str)
    df["target"] = df["label"].map(LABEL_TO_INT)
    return list(zip(df["content"].tolist(), df["target"].tolist()))