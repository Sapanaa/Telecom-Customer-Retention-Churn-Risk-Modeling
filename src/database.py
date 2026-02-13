import sqlite3
import pandas as pd

def create_database():
    conn = sqlite3.connect("churn.db")
    
    df = pd.read_csv("data/raw/Telco-Customer-Churn.csv")
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df = df.dropna()
    df.to_sql("customers", conn, if_exists="replace", index=False)
    
    print("Database created and data inserted.")
    conn.close()

if __name__ == "__main__":
    create_database()
