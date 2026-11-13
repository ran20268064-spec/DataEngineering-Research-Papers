
import pandas as pd
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import nltk
import re
import os
from collections import Counter
from nltk.corpus import stopwords
from textblob import Word


# ==========================================
# 1. LOAD DATASET
# ==========================================

print("\n========== DATA PROFILING ==========\n")

DATASET_PATH = "arxiv_articles.csv"

if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(
        f"Dataset not found: {DATASET_PATH}"
    )

df = pd.read_csv(DATASET_PATH)

print("Dataset loaded successfully!")
print("Dataset Shape:", df.shape)
print("Total Articles:", len(df))


# ==========================================
# 2. TEXT TOKENIZATION
# ==========================================

print("\n========== TEXT TOKENIZATION ==========\n")

def tokenize_text(text):
    text = str(text).lower()
    tokens = re.findall(r"\b[a-z]+\b", text)
    return tokens


df["Tokens"] = df["Text_Content"].apply(tokenize_text)

all_tokens = [
    token
    for tokens in df["Tokens"]
    for token in tokens
]

print("Total Tokens:", len(all_tokens))
print("Unique Words:", len(set(all_tokens)))

print("\nSample Tokenization:")
print(df["Tokens"].iloc[0][:20])


# ==========================================
# 3. TOP 10 MOST FREQUENT WORDS
# ==========================================

print("\n========== TOP 10 FREQUENT WORDS ==========\n")

word_frequency = Counter(all_tokens)

top_10_words = word_frequency.most_common(10)

for word, frequency in top_10_words:
    print(f"{word}: {frequency}")


# ==========================================
# 4. STOPWORDS ANALYSIS
# ==========================================

print("\n========== STOPWORDS ANALYSIS ==========\n")

nltk.download("stopwords", quiet=True)

stop_words = set(stopwords.words("english"))

all_stopwords = [
    word for word in all_tokens
    if word in stop_words
]

stopword_frequency = Counter(all_stopwords)

print("Total Stopwords Occurrences:", len(all_stopwords))

print("\nTop 10 Most Frequent Stopwords:")

top_10_stopwords = stopword_frequency.most_common(10)

for word, frequency in top_10_stopwords:
    print(f"{word}: {frequency}")


# ==========================================
# 5. TEXT VISUALIZATION - CHART 1
# Top 10 Frequent Words
# ==========================================

os.makedirs("charts", exist_ok=True)

words = [item[0] for item in top_10_words]
frequencies = [item[1] for item in top_10_words]

plt.figure(figsize=(12, 6))

plt.bar(words, frequencies)

plt.title("Top 10 Most Frequent Words in Research Abstracts")
plt.xlabel("Words")
plt.ylabel("Frequency")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("charts/top_10_words.png", dpi=300)
plt.show()


# ==========================================
# 6. TEXT VISUALIZATION - CHART 2
# Abstract Length Distribution
# ==========================================

df["Abstract_Word_Count"] = df["Tokens"].apply(len)

plt.figure(figsize=(12, 6))

plt.hist(
    df["Abstract_Word_Count"],
    bins=30,
    edgecolor="black"
)

plt.title("Distribution of Abstract Lengths")
plt.xlabel("Number of Words per Abstract")
plt.ylabel("Number of Research Papers")

plt.tight_layout()

plt.savefig("charts/abstract_length_distribution.png", dpi=300)
plt.show()


# ==========================================
# 7. SPELLING MISTAKES DETECTION
# ==========================================

print("\n========== SPELLING CHECK ==========\n")

# Check the 300 most frequent non-stopwords.
# This keeps spelling analysis manageable.

candidate_words = [
    (word, frequency)
    for word, frequency in word_frequency.most_common()
    if word not in stop_words and len(word) >= 4
][:300]

spelling_errors = []

for word, frequency in candidate_words:

    suggestions = Word(word).spellcheck()

    if suggestions:
        suggested_word, confidence = suggestions[0]

        if suggested_word != word and confidence >= 0.5:

            spelling_errors.append({
                "Word": word,
                "Frequency": frequency,
                "Suggested_Correction": suggested_word,
                "Confidence": round(confidence, 3)
            })


spelling_df = pd.DataFrame(spelling_errors)

print("Words Checked:", len(candidate_words))
print("Potential Spelling Issues:", len(spelling_df))

if not spelling_df.empty:

    print("\nTop Potential Spelling Issues:")
    print(spelling_df.head(20).to_string(index=False))

    spelling_df.to_csv(
        "potential_spelling_issues.csv",
        index=False
    )

else:
    print("No potential spelling issues detected.")


# ==========================================
# 8. SAVE PROFILING RESULTS
# ==========================================

df.drop(columns=["Tokens"]).to_csv(
    "profiled_dataset.csv",
    index=False
)

print("\n========== PROFILING COMPLETED ==========")

print("\nGenerated Files:")
print("1. charts/top_10_words.png")
print("2. charts/abstract_length_distribution.png")
print("3. potential_spelling_issues.csv")
print("4. profiled_dataset.csv")

print("\nData Profiling Completed Successfully!")
