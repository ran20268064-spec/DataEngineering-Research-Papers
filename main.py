
import requests
import feedparser
import pandas as pd
import time

# ==========================================
# 1. Configuration
# ==========================================

API_URL = "https://export.arxiv.org/api/query"

TARGET_ROWS = 7500
BATCH_SIZE = 2000

HEADERS = {
    "User-Agent": "DataEngineeringStudentProject/1.0"
}

SEARCH_QUERY = (
    "cat:cs.* OR cat:stat.* OR cat:physics.*"
)

# ==========================================
# 2. Fetch Research Papers
# ==========================================

def fetch_papers(start, max_results):

    params = {
        "search_query": SEARCH_QUERY,
        "start": start,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }

    for attempt in range(5):

        try:

            response = requests.get(
                API_URL,
                params=params,
                headers=HEADERS,
                timeout=180
            )

            response.raise_for_status()

            feed = feedparser.parse(response.content)

            if feed.bozo and not feed.entries:
                raise ValueError("Invalid API response")

            return feed.entries

        except Exception as error:

            print(f"Request error: {error}")

            if attempt == 4:
                raise

            time.sleep(10 * (attempt + 1))


# ==========================================
# 3. Data Collection
# ==========================================

print("\n--- arXiv Data Collection Phase ---")

dataset = []
seen_ids = set()

start = 0

while len(dataset) < TARGET_ROWS:

    remaining = TARGET_ROWS - len(dataset)

    batch_size = min(BATCH_SIZE, remaining)

    print(f"\nFetching papers from position {start}...")

    entries = fetch_papers(start, batch_size)

    if not entries:
        print("No more papers available.")
        break

    for entry in entries:

        paper_id = entry.id.split("/abs/")[-1].split("v")[0]

        if paper_id in seen_ids:
            continue

        seen_ids.add(paper_id)

        title = " ".join(entry.title.split())

        abstract = " ".join(entry.summary.split())

        authors = ", ".join(
            author.name for author in entry.authors
        )

        primary_category = entry.arxiv_primary_category["term"]

        if primary_category.startswith(("cs.", "stat.")):
            category = "Technology"
        else:
            category = "Science"

        dataset.append({

            "ID": paper_id,

            "Title": title,

            "Category": category,

            "Author": authors,

            "Text_Content": abstract,

            "Published_Date": entry.published,

            "URL": entry.id

        })

    start += len(entries)

    # Save progress after every batch

    df = pd.DataFrame(dataset)

    df.to_csv(
        "arxiv_articles_partial.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print(f"Collected valid papers: {len(dataset)}")

    if len(dataset) >= TARGET_ROWS:
        break

    if len(entries) < batch_size:
        print("API returned fewer results than requested.")
        break

    # Respect arXiv API request policy
    time.sleep(3)


# ==========================================
# 4. Final Dataset
# ==========================================

df = pd.DataFrame(dataset)

if not df.empty:

    df = df.drop_duplicates(subset=["ID"])

    df.to_csv(
        "arxiv_articles.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\n--- Final Collection Results ---")

    print(f"Dataset Shape: {df.shape}")

    print(f"Total Articles: {len(df)}")

    print("\nCategory Distribution:")

    print(df["Category"].value_counts())

    print("\nDataset Preview:")

    print(df.head())

    if len(df) >= TARGET_ROWS:
        print("\nSUCCESS: 7500 research papers collected!")

    else:
        print(
            f"\nWARNING: Only {len(df)} papers collected."
        )

else:

    print("No data collected.")

print("\nData Collection Completed!")

# ==========================================
# 5. Data Quality Validation
# ==========================================

print("\n--- Data Quality Validation ---")

df = pd.read_csv("arxiv_articles.csv")

# 1. Check missing values

print("\nMissing Values:")
print(df.isnull().sum())

# 2. Check duplicate IDs

print("\nDuplicate IDs:")
print(df["ID"].duplicated().sum())

# 3. Check empty abstracts

empty_abstracts = (
    df["Text_Content"].fillna("").str.strip() == ""
).sum()

print("\nEmpty Abstracts:")
print(empty_abstracts)

# 4. Check duplicate abstracts

print("\nDuplicate Abstracts:")
print(df["Text_Content"].duplicated().sum())

# 5. Check minimum text length

print("\nAbstract Length Statistics:")
print(df["Text_Content"].str.len().describe())

# 6. Check URLs

print("\nInvalid URLs:")
print(
    (~df["URL"].str.startswith("http")).sum()
)

# 7. Final validation

if (
    len(df) >= 7000
    and df["ID"].nunique() == len(df)
    and empty_abstracts == 0
    and df["Title"].notna().all()
    and df["Author"].notna().all()
):

    print("\nDATA QUALITY CHECK PASSED!")

else:

    print("\nDATA QUALITY CHECK NEEDS REVIEW!")
