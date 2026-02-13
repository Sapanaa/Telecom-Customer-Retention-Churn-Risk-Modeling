import os
import pandas as pd

# IBM official dataset link
DATA_URL = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"

def download_dataset(save_path="data/raw/Telco-Customer-Churn.csv"):
    """
    Downloads Telco churn dataset and saves locally.
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    df = pd.read_csv(DATA_URL)
    df.to_csv(save_path, index=False)
    
    print(f"Dataset downloaded and saved to {save_path}")
    print(f"Shape: {df.shape}")
    
    return df


if __name__ == "__main__":
    download_dataset()
