# Research Papers Data Collection and Analysis

## 1. Project Overview

This project collects, processes, analyzes, and stores research paper metadata and abstracts from **arXiv**, an open-access repository of scientific research papers.

The dataset contains 7,500 research papers collected using the arXiv API. The project applies text analysis and data profiling techniques to explore the content of research abstracts. The collected data is also stored in a MongoDB database.

## 2. Dataset Description

The dataset contains 7,500 records and 7 columns.

| Column | Description |
|---|---|
| ID | Unique identifier of the research paper |
| Title | Title of the research paper |
| Category | Grouped research category: Technology or Science |
| Author | Author or authors of the paper |
| Text_Content | Research paper abstract |
| Published_Date | Publication date |
| URL | Link to the paper on arXiv |

The papers are collected from arXiv categories related to Computer Science, Statistics, and Physics.

The `Category` column groups Computer Science and Statistics papers under **Technology**, while Physics papers are grouped under **Science**. This is a project-defined grouping based on the papers' primary arXiv categories.

## 3. Potential Applications

The collected dataset can be used for several data science and text analytics applications, including:

- Research trend analysis.
- Text mining and Natural Language Processing (NLP).
- Keyword extraction and frequency analysis.
- Research paper classification.
- Topic discovery and clustering.
- Exploring the distribution of scientific publications.

## 4. Data Collection

Data was collected from the arXiv API using Python.

The collection process retrieves research paper information in batches and extracts the required fields, including titles, authors, abstracts, publication dates, categories, and paper URLs.

The final dataset contains:

- **Total records:** 7,500
- **Total columns:** 7
- **Data source:** arXiv API

The collected data is saved in `arxiv_articles.csv`.

## 5. Data Quality Validation

Several validation checks were performed after data collection.

| Validation Check | Result |
|---|---:|
| Total records | 7,500 |
| Missing values | 0 |
| Duplicate IDs | 0 |
| Empty abstracts | 0 |
| Duplicate abstracts | 1 |
| Invalid URLs | 0 |

The dataset passed the implemented data quality validation checks.

## 6. Data Profiling and Text Analysis

The project performs text profiling on the research paper abstracts.

The following operations are implemented:

1. **Text Tokenization:** Converts abstracts into individual lowercase word tokens.
2. **Word Frequency Analysis:** Identifies and displays the 10 most frequent words.
3. **Stopwords Analysis:** Counts English stopword occurrences and identifies the 10 most frequent stopwords.
4. **Text Visualization:** Generates two visualizations:
   - Top 10 most frequent words.
   - Distribution of abstract lengths.
5. **Spelling Analysis:** Uses TextBlob to identify potential spelling issues among frequent words.

Spelling results are considered potential issues because scientific terminology, abbreviations, and technical vocabulary may not be recognized by general-purpose spelling tools.

### Generated Profiling Outputs

- `charts/top_10_words.png`
- `charts/abstract_length_distribution.png`
- `potential_spelling_issues.csv` (if potential issues are detected)
- `profiled_dataset.csv`

## 7. MongoDB Database Storage

The collected dataset is stored in MongoDB Atlas.

**Database name:** `data_engineering_assignment`

**Collection name:** `research_papers`

Each research paper is stored as a separate MongoDB document.

A unique index is created on the `ID` field to prevent duplicate paper identifiers.

The storage process includes:

- Connecting to MongoDB Atlas.
- Creating/accessing the database and collection.
- Inserting records in batches.
- Verifying the total number of stored documents and unique IDs.

The expected number of stored documents is 7,500.

## 8. Project Structure

```text
DataEngineering/
│
├── main.py
├── profiling.py
├── mongodb_storage.py
├── arxiv_articles.csv
├── profiled_dataset.csv
├── potential_spelling_issues.csv
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
└── charts/
    ├── top_10_words.png
    └── abstract_length_distribution.png
```

Some generated files may only appear after running the corresponding scripts.

## 9. Requirements and Installation

Python 3 is required.

Install the project dependencies using:

```bash
pip install -r requirements.txt
```

The project uses the following main libraries:

- pandas
- requests
- feedparser
- matplotlib
- nltk
- textblob
- pymongo
- python-dotenv

## 10. How to Run the Project

Run the scripts in the following order.

### Step 1: Data Collection

```bash
python main.py
```

This script collects research papers from arXiv and saves the dataset as `arxiv_articles.csv`.

### Step 2: Data Profiling

```bash
python profiling.py
```

This script performs text analysis, calculates word frequencies and stopwords, checks potential spelling issues, and generates charts.

### Step 3: MongoDB Storage

Create a `.env` file in the project directory and add your MongoDB connection string:

```env
MONGODB_URI=your_mongodb_connection_string
```

Then run:

```bash
python mongodb_storage.py
```

This script connects to MongoDB Atlas, inserts the dataset, and verifies the stored records.

**Important:** Never upload your `.env` file or expose your MongoDB credentials.

## 11. Technologies Used

- Python
- arXiv API
- Pandas
- NLTK
- TextBlob
- Matplotlib
- MongoDB Atlas
- PyMongo

## 12. Conclusion

This project demonstrates an end-to-end data engineering workflow, starting with collecting real-world textual data from an external source, followed by data quality validation and text profiling, and finally storing the processed dataset in a NoSQL database using MongoDB.

The resulting dataset provides a foundation for further research analytics and Natural Language Processing applications.