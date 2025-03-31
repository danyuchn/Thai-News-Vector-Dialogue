import feedparser
import datetime
import requests
from io import BytesIO
from openai import OpenAI

# ============================================
# 1. Create OpenAI client (replace with your API key)
# ============================================
client = OpenAI(api_key="sk-xxxxxxxxxxxxxxxx")  # Replace with your actual API key

# ============================================
# 2. Define functions for fetching and translating news
# ============================================
def fetch_news(rss_url):
    """
    Parse the specified RSS URL and return a list of news items from the past 24 hours.
    Each news item includes the title, link, and published time.
    """
    feed = feedparser.parse(rss_url)
    news_list = []
    now = datetime.datetime.now(datetime.timezone.utc)
    for entry in feed.entries:
        if hasattr(entry, 'published_parsed'):
            published = datetime.datetime(*entry.published_parsed[:6], tzinfo=datetime.timezone.utc)
            if now - published < datetime.timedelta(days=1):
                news_list.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": published.strftime("%Y-%m-%d %H:%M:%S")
                })
    return news_list

def translate_to_english(text):
    """
    Use the ChatCompletion API to translate the given news title into English.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # You may change to "gpt-4" as needed
        messages=[
            {"role": "system", "content": "You are a professional translator. Please translate the following news title into English."},
            # You may change to any target language
            {"role": "user", "content": text}
        ],
        max_tokens=100,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

# ============================================
# 3. Fetch news from RSS feeds and write to file news_titles.txt
# ============================================
rss_urls = [
    "https://www.thairath.co.th/rss/news.xml",
    "https://www.matichon.co.th/feed",
    "https://www.khaosod.co.th/feed",
    "https://www.prachachat.net/feed",
    "https://workpointtoday.com/feed/"
]

all_news = []
for url in rss_urls:
    news_list = fetch_news(url)
    all_news.extend(news_list)

with open("news_titles.txt", "w", encoding="utf-8") as f:
    for news in all_news:
        translated_title = translate_to_english(news["title"])
        # Format: Original Title | Translated Title | Link | Published Time
        f.write(f"{news['title']} | {translated_title} | {news['link']} | {news['published']}\n")

print("News data successfully saved to news_titles.txt")

# ============================================
# 4. Upload news_titles.txt to OpenAI's File API as a knowledge file
# ============================================
def upload_knowledge_file(file_path):
    """
    Upload the specified file to OpenAI's File API for building a knowledge base.
    """
    if file_path.startswith("http://") or file_path.startswith("https://"):
        response = requests.get(file_path)
        file_content = BytesIO(response.content)
        file_name = file_path.split("/")[-1]
        file_tuple = (file_name, file_content)
        result = client.files.create(
            file=file_tuple,
            purpose="assistants"
        )
    else:
        with open(file_path, "rb") as file_content:
            result = client.files.create(
                file=file_content,
                purpose="assistants"
            )
    print("Uploaded file ID:", result.id)
    return result.id

knowledge_file_id = upload_knowledge_file("news_titles.txt")

# ============================================
# 5. Create a vector store and add the uploaded file to it
# ============================================
vector_store = client.vector_stores.create(name="news_knowledge_base")
print("Vector store ID:", vector_store.id)

client.vector_stores.files.create(
    vector_store_id=vector_store.id,
    file_id=knowledge_file_id
)
print("File successfully added to the vector store")

# ============================================
# 6. Implement multi-turn conversation (with context memory):
# Use the responses API with the file_search tool to query the knowledge base
# ============================================
print("\nStarting multi-turn conversation, type 'quit' to end conversation.")
previous_response_id = None

while True:
    user_input = input("Please enter your question: ")
    if user_input.strip().lower() == "quit":
        print("Conversation ended.")
        break

    # For the first round or subsequent rounds, use the file_search tool and include previous_response_id for context memory
    if previous_response_id is None:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=user_input,
            tools=[{
                "type": "file_search",
                "vector_store_ids": [vector_store.id]
            }]
        )
    else:
        response = client.responses.create(
            model="gpt-4o-mini",
            previous_response_id=previous_response_id,
            input=[{"role": "user", "content": user_input}],
            tools=[{
                "type": "file_search",
                "vector_store_ids": [vector_store.id]
            }]
        )
    
    # Extract and display only the final response text
    try:
        print("Model response:", response.output_text)
    except AttributeError:
        for item in response.output:
            if hasattr(item, 'content') and isinstance(item.content, list):
                for content_item in item.content:
                    if hasattr(content_item, 'text'):
                        print("Model response:", content_item.text)
                        break
    previous_response_id = response.id
