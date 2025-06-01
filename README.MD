# Reddit Sentiment Analysis Tool

This is a command-line Python tool that searches a specific subreddit for recent posts matching a search query, performs sentiment analysis using `TextBlob`, and saves the results as a CSV file. It filters out posts with no comments to focus on engaging content.

## Features

- Searches Reddit posts via the Reddit API (using PRAW)
- Filters out posts with 0 comments
- Performs sentiment analysis (polarity & subjectivity) using TextBlob
- Saves results to a CSV file with detailed metadata
- Customizable number of posts to fetch via CLI
- Stores output to a predefined directory (e.g., `D:\Coding\Projects\bot\data`)

## Requirements
pip install -r requirements.txt 

## ⚙️ Setup
Create a .env file in the root directory with your Reddit API credentials:
- REDDIT_CLIENT_ID=your_client_id
- REDDIT_CLIENT_SECRET=your_client_secret
- REDDIT_USER_AGENT=your_user_agent


# Usage
## example
python script.py mentalhealth anxiety --limit 50

This will:

Search the r/mentalhealth subreddit for posts containing "anxiety"

Retrieve up to 50 of the most recent results from the past month

Filter out posts with 0 comments

Analyze sentiment

Save the results to:
'D:\Coding\Projects\bot\data'

## 📊 Output
Each post is analyzed and saved with the following fields:

id

title

selftext

score

num_comments

created_utc

url

subreddit

polarity (range: -1 to 1)

subjectivity (range: 0 to 1)
