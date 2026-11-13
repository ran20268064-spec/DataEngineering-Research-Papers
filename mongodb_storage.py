
import os
import pandas as pd

from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from dotenv import load_dotenv


# ==========================================
# 1. LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    raise ValueError(
        "MONGODB_URI not found. Check your .env file."
    )


# ==========================================
# 2. LOAD DATASET
# ==========================================

print("\n========== MONGODB DATA STORAGE ==========\n")

df = pd.read_csv("arxiv_articles.csv")

print("Dataset loaded successfully!")
print("Number of records:", len(df))


if len(df) < 7000:
    raise ValueError("Dataset must contain at least 7000 records.")

if df["ID"].duplicated().any():
    raise ValueError("Duplicate IDs found in dataset.")


# ==========================================
# 3. CONNECT TO MONGODB
# ==========================================

try:

    client = MongoClient(
        MONGODB_URI,
        serverSelectionTimeoutMS=10000
    )

    # Test connection
    client.admin.command("ping")

    print("\nSuccessfully connected to MongoDB Atlas!")


    # ==========================================
    # 4. CREATE DATABASE AND COLLECTION
    # ==========================================

    db = client["data_engineering_assignment"]

    collection = db["research_papers"]

    print("Database:", db.name)
    print("Collection:", collection.name)


    # ==========================================
    # 5. CREATE UNIQUE INDEX
    # ==========================================

    collection.create_index(
        "ID",
        unique=True
    )

    print("\nUnique index created on ID.")


    # ==========================================
    # 6. PREPARE DATA
    # ==========================================

    records = df.to_dict(orient="records")

    # Remove existing records to avoid duplicates
    collection.delete_many({})

    print("\nOld records cleared.")

    # Insert records in batches
    batch_size = 500
    total_inserted = 0

    for start in range(0, len(records), batch_size):

        batch = records[start:start + batch_size]

        result = collection.insert_many(
            batch,
            ordered=True
        )

        total_inserted += len(result.inserted_ids)

        print(
            f"Inserted {total_inserted} / {len(records)} records"
        )


    # ==========================================
    # 7. VERIFY STORED DATA
    # ==========================================

    print("\n========== STORAGE VERIFICATION ==========\n")

    total_documents = collection.count_documents({})

    print("Total documents in MongoDB:", total_documents)

    print(
        "Unique IDs in MongoDB:",
        len(collection.distinct("ID"))
    )

    print("\nSample Document:")

    sample = collection.find_one(
        {},
        {"_id": 0}
    )

    print(sample)


    # ==========================================
    # 8. FINAL VALIDATION
    # ==========================================

    if (
        total_documents == len(df)
        and len(collection.distinct("ID")) == len(df)
    ):

        print("\nSUCCESS: All records stored correctly!")

    else:

        print("\nWARNING: Storage verification failed.")


except Exception as e:

    print("\nMongoDB Error:")
    print(e)


finally:

    if "client" in locals():
        client.close()
        print("\nMongoDB connection closed.")
