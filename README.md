# Thai-News-Vector-Dialogue

This project integrates news scraping, title translation, vector store knowledge base creation, and multi-turn dialogue using OpenAI's API. It allows you to:
- Scrape news from multiple RSS feeds (within the last 24 hours).
- Translate news titles into Traditional Chinese.
- Save the news data into a file (`news_titles.txt`).
- Upload the file to OpenAI's File API and build a vector store knowledge base.
- Engage in multi-turn conversations using the OpenAI responses API with context memory, leveraging the uploaded knowledge.

## Features

- **News Scraping & Translation:**  
  Fetches news from various RSS feeds and translates the titles into Traditional Chinese.

- **Knowledge Base Creation:**  
  Saves the news data into `news_titles.txt`, then uploads it to create a vector store for semantic search.

- **Multi-turn Dialogue with Context Memory:**  
  Uses the OpenAI responses API to search the knowledge base (via file_search tool) and supports context retention over multiple interactions.

## Prerequisites

- Python 3.7 or later.
- Required Python packages:
  - `feedparser`
  - `requests`
  - `openai`
- A valid OpenAI API key with access to File API and vector store features.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/News-Vector-Dialogue.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd News-Vector-Dialogue
   ```
3. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use: env\Scripts\activate
   pip install -r requirements.txt
   ```

## Usage

1. **Set Your API Key:**  
   In `news_vector_chat.py`, replace the placeholder API key with your actual OpenAI API key:
   ```python
   client = OpenAI(api_key="sk-xxxxxxxxxxxxxxxx")
   ```

2. **Run the script:**
   ```bash
   python news_vector_chat.py
   ```

3. **Interact with the Dialogue System:**  
   - The script will scrape and translate news, build the knowledge base, and then enter a multi-turn dialogue mode.
   - Type your questions at the prompt.
   - Type `quit` to exit the dialogue.

## Project Structure

```
News-Vector-Dialogue/
├── news_vector_chat.py       # Main script integrating news scraping, translation, vector store upload, and dialogue.
├── news_titles.txt           # Generated file containing the scraped and translated news.
├── requirements.txt          # List of required Python packages.
└── README.md                 # Project documentation.
```

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
