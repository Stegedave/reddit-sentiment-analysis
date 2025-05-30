from dotenv import load_dotenv # loads enviroment variables from .env file.
import os
import praw # reddit API wrapper.
import pandas as pd 
from datetime import datetime
import praw.exceptions
from textblob import TextBlob
import sys
import argparse

# loads the .env file contents into environment variables.
load_dotenv()

# initializing reddit and passing credentials from environment variables.
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# argparse to get cli arguments.
parser = argparse.ArgumentParser(description="Reddit Sentiment Analysis")
parser.add_argument("subreddit", help="Subreddit to search")
parser.add_argument("query", help="Search Phrase")
parser.add_argument("--limit", type=int, default=30, help="Number of posts to retrieve.(default: 30)")

args = parser.parse_args()

# setting cli arguments to variables

subreddit_name = args.subreddit # subreddit to search
query = args.query # search phrase
limit = args.limit # number of posts to retrieve. Default Limit: 30

try:
    if limit <= 0:
        raise ValueError("Limit must be a positive integer")
except ValueError as e:
    print(e)
    sys.exit(1)

results  = []
try:
    for submission in reddit.subreddit(subreddit_name).search(query, sort="new", time_filter="month", limit=limit):
        if submission.num_comments == 0: # skipping posts with 0 comments.
            continue

        full_text = f"{submission.title} {submission.selftext}".replace('\n', ' ').strip()
        blob = TextBlob(full_text)
        sentiment = blob.sentiment

        results.append({
            "id": submission.id,
            "title": submission.title,
            "selftext": submission.selftext,
            "score": submission.score,
            "num_comments": submission.num_comments,
            "created_utc": datetime.fromtimestamp(submission.created_utc),
            "url": submission.url,
            "subreddit": str(submission.subreddit),
            "polarity": sentiment.polarity,
            "subjectivity": sentiment.subjectivity
        })
except praw.exceptions.RedditAPIException as e:
    print(f"Reddit API error: {e}")
except Exception as e:
    print(f"An error occured: {e}")

# check if no posts are found 
if not results:
    print(f"No results were found for the given query: {query}")
else:
    print(f"Found {len(results)} posts.")
    # print(results)
    for r in results:
        print(f"[{r['created_utc']}] ({r['subreddit']}) {r['title']}")
        print(f"Score: {r['score']} | Comments: {r['num_comments']}")
        print(f"Sentiment → Polarity: {r['polarity']:.2f}, Subjectivity: {r['subjectivity']:.2f}")
        print(f"URL: {r['url']}")
        print("-" * 100)    

# save to csv
if results:
    df = pd.DataFrame(results)
    output_dir = r'D:\Coding\Projects\bot\data'
    filename = os.path.join(output_dir, f"reddit_{subreddit_name}_{query.replace(' ', '_')}_sentiment.csv")
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} posts to '{filename}'.")
