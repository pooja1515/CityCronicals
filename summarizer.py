import pandas as pd
import torch
from transformers import pipeline
from tqdm import tqdm
import os

# ------------------- CONFIG -------------------
DEVICE = 0 if torch.cuda.is_available() else -1
CHECKPOINT_EVERY = 5  # Save every N articles
CHECKPOINT_PATH = "checkpoint_news.csv"

# ------------------- PIPELINE SETUP -------------------
summarizer = pipeline("summarization", model="facebook/bart-large", device=DEVICE)
tagger = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=DEVICE)
sentiment_analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment", device=DEVICE)

CANDIDATE_LABELS = [
    'Politics', 'Business', 'Health', 'Sports', 'Technology',
    'Entertainment', 'Environment', 'Education', 'Crime', 'Weather'
]

# ------------------- HELPER FUNCTIONS -------------------

def chunk_text(text, max_tokens=1024):
    words = text.split()
    for i in range(0, len(words), max_tokens):
        yield " ".join(words[i:i + max_tokens])

def summarize_article(text, max_chunk_tokens=1024):
    chunks = list(chunk_text(text, max_chunk_tokens))
    summaries = []
    for chunk in chunks:
        if chunk.strip():
            summary = summarizer(chunk, max_length=80, min_length=20, do_sample=False)
            summaries.append(summary[0]['summary_text'])
    return " ".join(summaries)

def classify_tags(text):
    result = tagger(text, CANDIDATE_LABELS, multi_label=False)
    labels = [label for label, score in zip(result['labels'], result['scores']) if score > 0.3]
    return ', '.join(labels) if labels else 'General'

def analyze_sentiment(text):
    result = sentiment_analyzer(text[:512])[0]
    label = result['label']
    if "1" in label or "2" in label:
        return "Negative"
    elif "3" in label:
        return "Neutral"
    else:
        return "Positive"

def process_article(article):
    try:
        if isinstance(article, str) and article.strip():
            summary = summarize_article(article)
            tags = classify_tags(article)
            sentiment = analyze_sentiment(article)
        else:
            summary, tags, sentiment = "No content", "General", "Neutral"
    except Exception as e:
        print(f"Error processing article: {e}")
        summary, tags, sentiment = "Error", "General", "Neutral"
    return summary, tags, sentiment

# ------------------- CHECKPOINTING -------------------

def save_checkpoint(df_partial, path):
    df_partial.to_csv(path, index=False)
    print(f"[Checkpoint] Saved {len(df_partial)} records to '{path}'")

# ------------------- MAIN PROCESSING -------------------

def enrich_dataframe(df):
    summaries, tags_list, sentiments = [], [], []

    for idx, article in enumerate(tqdm(df['Article'], desc="Processing articles"), start=1):
        summary, tags, sentiment = process_article(article)
        summaries.append(summary)
        tags_list.append(tags)
        sentiments.append(sentiment)

        # Checkpoint
        if idx % CHECKPOINT_EVERY == 0:
            df_partial = df.iloc[:idx].copy()
            df_partial['Summary'] = summaries
            df_partial['Tags'] = tags_list
            df_partial['Sentiment'] = sentiments
            save_checkpoint(df_partial, CHECKPOINT_PATH)

    df['Summary'] = summaries
    df['Tags'] = tags_list
    df['Sentiment'] = sentiments
    return df

def main(input_path: str, output_path: str):
    print("Loading data...")
    df = pd.read_csv(input_path)

    if os.path.exists(CHECKPOINT_PATH):
        print("Checkpoint found. Loading from checkpoint...")
        df_checkpoint = pd.read_csv(CHECKPOINT_PATH)
        processed_len = len(df_checkpoint)
        df_remaining = df.iloc[processed_len:]
        df = pd.concat([df_checkpoint, enrich_dataframe(df_remaining)], ignore_index=True)
    else:
        df = enrich_dataframe(df)

    df.to_csv(output_path, index=False)
    print(f"Saved final output to '{output_path}'")

# ------------------- ENTRY POINT -------------------

if __name__ == "__main__":
    main("news_articles.csv", "news_with_summaries_tags_sentiment.csv")
