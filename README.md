# XBot Project

## Overview

**XBot** is an intelligent Twitter bot designed to provide informative and accurate responses based on ingested data. It seamlessly integrates data ingestion from specified URLs, stores the information in a LanceDB database with embeddings, and leverages OpenAI's GPT models to handle user queries. XBot interacts with users via Twitter, posting insightful content and responding to queries directly on the platform.

## Features

- **Data Ingestion:** Automatically fetches and processes data from a list of specified URLs.
- **Embeddings:** Utilizes Sentence Transformers to generate meaningful embeddings for efficient data retrieval.
- **Database Management:** Employs LanceDB, a lightweight vector database, to store and retrieve data based on embeddings.
- **OpenAI Integration:** Harnesses the power of OpenAI's GPT models to generate intelligent and context-aware responses.
- **Twitter Integration:** Interacts with users by posting tweets and responding to queries via Twitter Direct Messages.
- **Configurable Character:** Defines XBot's personality, communication style, and interaction policies through a comprehensive JSON configuration.
- **Scalable and Modular Design:** Structured to allow easy updates, maintenance, and scalability.

## Project Structure

```
xbot-project/
├── bots/
│   └── xbot.py
├── config/
│   └── xbot_character.json
├── data/
│   └── data_ingestion.py
├── utils/
│   ├── config.py
│   ├── lance_db_utils.py
│   ├── openai_utils.py
│   └── twitter_utils.py
├── main.py
├── requirements.txt
└── .env.example
```

### Directory and File Descriptions

- **bots/xbot.py:** Core class handling data ingestion, query processing, and tweeting responses based on user queries.
- **config/xbot_character.json:** JSON file defining XBot's character, personality traits, communication style, goals, preferred topics, response formats, constraints, ingestion URLs, LLM settings, fallback responses, and interaction policies.
- **data/data_ingestion.py:** Standalone script for ingesting data from URLs into LanceDB.
- **utils/config.py:** Configuration loader and validator for environment variables.
- **utils/lance_db_utils.py:** Utilities for interacting with LanceDB and managing embeddings.
- **utils/openai_utils.py:** Interface with OpenAI's GPT models for generating responses.
- **utils/twitter_utils.py:** Handles Twitter API authentication and posting tweets.
- **main.py:** Entry point for initializing XBot, ingesting data, and processing sample queries.
- **requirements.txt:** Lists all Python dependencies required for the project.
- **.env.example:** Template for environment variables containing API keys and configurations.

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/xbot-project.git
cd xbot-project
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
```

Activate the virtual environment:

- **On macOS and Linux:**

  ```bash
  source venv/bin/activate
  ```

- **On Windows:**

  ```bash
  venv\Scripts\activate
  ```

### 3. Install Dependencies

Install all required Python packages using `pip` and the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

1. **Rename `.env.example` to `.env`:**

   ```bash
   cp .env.example .env
   ```

2. **Populate `.env` with Actual Values:**

   Open the `.env` file in a text editor and replace the placeholder values with your actual API keys and configurations.

   ```env
   OPENAI_API_KEY=your_openai_api_key
   TWITTER_API_KEY=your_twitter_api_key
   TWITTER_API_SECRET_KEY=your_twitter_api_secret_key
   TWITTER_ACCESS_TOKEN=your_twitter_access_token
   TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
   DB_PATH=my_lancedb
   EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
   LLM_MODEL=gpt-3.5-turbo
   CHARACTER_CONFIG_PATH=config/xbot_character.json
   ```

   **Note:** Ensure that the `.env` file is **never** committed to version control systems like Git to protect your sensitive information.

### 5. Configure XBot's Character and Ingestion URLs

1. **Open `config/xbot_character.json`:**

   This JSON file defines XBot's personality, communication style, goals, preferred topics, response formats, constraints, ingestion URLs, LLM settings, fallback responses, and interaction policies.

2. **Customize Configuration:**

   - **Personality Traits:** Adjust traits like friendliness, professionalism, helpfulness, etc.
   - **Communication Style:** Define how XBot communicates (e.g., clear, concise).
   - **Goals:** Outline what XBot aims to achieve.
   - **Preferred Topics:** Specify the subjects XBot focuses on.
   - **Response Format:** Set response length, language, structure, emoji usage, and hashtags.
   - **Constraints:** Define topics to avoid, promotional content policies, and privacy maintenance.
   - **Ingestion URLs:** Add or remove URLs from which XBot will ingest data.
   - **LLM Settings:** Configure OpenAI's GPT model parameters like temperature, max tokens, etc.
   - **Fallback Responses:** Define default responses when the bot cannot process a request.
   - **Interaction Policies:** Set rate limits, error handling strategies, and logging levels.

   ```json
   {
       "name": "XBot",
       "description": "XBot is an intelligent assistant designed to provide informative and accurate responses based on ingested data. It interacts with users via Twitter, posting helpful insights and answers to queries.",
       "personality_traits": {
           "friendly": true,
           "professional": true,
           "helpful": true,
           "concise": true,
           "informative": true,
           "respectful": true,
           "engaging": true,
           "curious": true,
           "empathetic": true
       },
       "tone": "neutral and informative",
       "communication_style": "clear and concise, avoiding jargon when possible, and ensuring that responses are easy to understand.",
       "goals": [
           "Provide accurate and relevant information to users' queries.",
           "Engage with the Twitter community by posting insightful and useful content.",
           "Maintain a consistent and professional presence on social media.",
           "Foster a supportive and informative online environment."
       ],
       "preferred_topics": [
           "Artificial Intelligence",
           "Machine Learning",
           "Technology Trends",
           "Data Science",
           "Software Development",
           "Cybersecurity",
           "Cloud Computing",
           "Internet of Things"
       ],
       "response_format": {
           "length": "up to 280 characters",
           "language": "English",
           "structure": "Complete sentences with proper grammar and punctuation.",
           "use_emojis": false,
           "include_hashtags": false
       },
       "constraints": {
           "avoid_sensitive_topics": [
               "politics",
               "religion",
               "personal opinions",
               "controversial issues",
               "health-related advice"
           ],
           "no_promotional_content": true,
           "maintain_privacy": true,
           "compliance_with_twitter_policies": true
       },
       "additional_instructions": "Ensure that all information shared is accurate and sourced from reliable data. Encourage user engagement through questions and prompts when appropriate. Avoid sharing unverified or speculative information.",
       "ingestion_urls": [
           "https://en.wikipedia.org/wiki/Artificial_intelligence",
           "https://en.wikipedia.org/wiki/Machine_learning",
           "https://en.wikipedia.org/wiki/Data_science",
           "https://en.wikipedia.org/wiki/Cloud_computing",
           "https://en.wikipedia.org/wiki/Cybersecurity",
           "https://en.wikipedia.org/wiki/Internet_of_Things"
       ],
       "llm_settings": {
           "model": "gpt-3.5-turbo",
           "temperature": 0.7,
           "max_tokens": 150,
           "top_p": 0.9,
           "frequency_penalty": 0.0,
           "presence_penalty": 0.6,
           "stop_sequences": ["\n", " User:", " XBot:"],
           "knowledge_cutoff": "2023-10",
           "fallback_responses": [
               "I'm sorry, but I couldn't process your request at the moment.",
               "Apologies, I'm having trouble understanding that. Could you please rephrase?",
               "I'm here to help! Let's try a different question."
           ]
       },
       "interaction_policies": {
           "rate_limit_per_minute": 60,
           "error_handling_strategy": "retry_with_exponential_backoff",
           "logging_level": "INFO"
       }
   }
   ```

## Usage

### 1. Data Ingestion

Ingest data from the specified URLs into the LanceDB database. This can be done using the standalone script or via the main application.

- **Using the Standalone Script:**

  ```bash
  python data/data_ingestion.py
  ```

- **Using the Main Application:**

  Running the main application will automatically ingest data as part of its execution.

  ```bash
  python main.py
  ```

### 2. Processing Queries and Posting Tweets

The main application (`main.py`) initializes XBot, ingests data, processes a sample query, and posts the response as a tweet.

- **Run the Main Application:**

  ```bash
  python main.py
  ```

- **Sample Output:**

  ```
  Response: Artificial Intelligence (AI) is widely used in healthcare for predictive analytics, in finance for fraud detection, and in transportation for autonomous vehicles.
  ```

  This response will be posted as a tweet on the authenticated Twitter account.

### 3. Customizing Queries

To process different queries, modify the `user_query` variable in `main.py` or extend the application to accept user inputs dynamically.

```python
# main.py

def main():
    setup_logging()
    bot = XBot()

    # Ingest data from URLs specified in the character configuration
    bot.ingest_data()

    # Example: Process a query
    user_query = "Explain the role of machine learning in modern technology."
    response = bot.process_query(user_query)
    print(f"Response: {response}")
```

## Configuration

### 1. Character Configuration (`config/xbot_character.json`)

This JSON file centralizes XBot's personality, communication style, goals, preferred topics, response formats, constraints, ingestion URLs, LLM settings, fallback responses, and interaction policies.

- **Personality Traits:**

  Define characteristics that shape how XBot interacts with users.

  ```json
  "personality_traits": {
      "friendly": true,
      "professional": true,
      "helpful": true,
      "concise": true,
      "informative": true,
      "respectful": true,
      "engaging": true,
      "curious": true,
      "empathetic": true
  }
  ```

- **Communication Style:**

  Specifies how XBot conveys information.

  ```json
  "communication_style": "clear and concise, avoiding jargon when possible, and ensuring that responses are easy to understand."
  ```

- **Goals:**

  Outlines XBot's objectives.

  ```json
  "goals": [
      "Provide accurate and relevant information to users' queries.",
      "Engage with the Twitter community by posting insightful and useful content.",
      "Maintain a consistent and professional presence on social media.",
      "Foster a supportive and informative online environment."
  ]
  ```

- **Preferred Topics:**

  Subjects XBot focuses on to maintain relevance and expertise.

  ```json
  "preferred_topics": [
      "Artificial Intelligence",
      "Machine Learning",
      "Technology Trends",
      "Data Science",
      "Software Development",
      "Cybersecurity",
      "Cloud Computing",
      "Internet of Things"
  ]
  ```

- **Response Format:**

  Defines how responses are structured.

  ```json
  "response_format": {
      "length": "up to 280 characters",
      "language": "English",
      "structure": "Complete sentences with proper grammar and punctuation.",
      "use_emojis": false,
      "include_hashtags": false
  }
  ```

- **Constraints:**

  Sets boundaries to ensure appropriate and compliant interactions.

  ```json
  "constraints": {
      "avoid_sensitive_topics": [
          "politics",
          "religion",
          "personal opinions",
          "controversial issues",
          "health-related advice"
      ],
      "no_promotional_content": true,
      "maintain_privacy": true,
      "compliance_with_twitter_policies": true
  }
  ```

- **Ingestion URLs:**

  List of URLs from which XBot ingests data.

  ```json
  "ingestion_urls": [
      "https://en.wikipedia.org/wiki/Artificial_intelligence",
      "https://en.wikipedia.org/wiki/Machine_learning",
      "https://en.wikipedia.org/wiki/Data_science",
      "https://en.wikipedia.org/wiki/Cloud_computing",
      "https://en.wikipedia.org/wiki/Cybersecurity",
      "https://en.wikipedia.org/wiki/Internet_of_Things"
  ]
  ```

- **LLM Settings:**

  Configures parameters for OpenAI's GPT models to control response generation.

  ```json
  "llm_settings": {
      "model": "gpt-3.5-turbo",
      "temperature": 0.7,
      "max_tokens": 150,
      "top_p": 0.9,
      "frequency_penalty": 0.0,
      "presence_penalty": 0.6,
      "stop_sequences": ["\n", " User:", " XBot:"],
      "knowledge_cutoff": "2023-10",
      "fallback_responses": [
          "I'm sorry, but I couldn't process your request at the moment.",
          "Apologies, I'm having trouble understanding that. Could you please rephrase?",
          "I'm here to help! Let's try a different question."
      ]
  }
  ```

- **Fallback Responses:**

  Default responses when the bot cannot generate a suitable answer.

  ```json
  "fallback_responses": [
      "I'm sorry, but I couldn't process your request at the moment.",
      "Apologies, I'm having trouble understanding that. Could you please rephrase?",
      "I'm here to help! Let's try a different question."
  ]
  ```

- **Interaction Policies:**

  Defines how XBot manages interactions and handles errors.

  ```json
  "interaction_policies": {
      "rate_limit_per_minute": 60,
      "error_handling_strategy": "retry_with_exponential_backoff",
      "logging_level": "INFO"
  }
  ```

### 2. Environment Variables (`.env`)

Ensure all required environment variables are set in the `.env` file. These variables are crucial for authenticating with APIs and configuring the database.

```env
OPENAI_API_KEY=your_openai_api_key
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET_KEY=your_twitter_api_secret_key
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
DB_PATH=my_lancedb
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
LLM_MODEL=gpt-3.5-turbo
CHARACTER_CONFIG_PATH=config/xbot_character.json
```

**Note:** Replace the placeholder values with your actual credentials.

## Logging and Monitoring

XBot utilizes Python's built-in `logging` module to track events, monitor performance, and debug issues. Logging levels can be adjusted in the configuration to control the verbosity.

- **Logging Levels:**
  - `DEBUG`: Detailed information, typically of interest only when diagnosing problems.
  - `INFO`: Confirmation that things are working as expected.
  - `WARNING`: An indication that something unexpected happened.
  - `ERROR`: Due to a more serious problem, the software has not been able to perform some function.

**Configuration:**

Logging levels are defined in the `interaction_policies` section of the `xbot_character.json` file.

```json
"interaction_policies": {
    "rate_limit_per_minute": 60,
    "error_handling_strategy": "retry_with_exponential_backoff",
    "logging_level": "INFO"
}
```

To change the logging level to `DEBUG`, update the `logging_level` field:

```json
"logging_level": "DEBUG"
```

**Implementation:**

Logging is initialized in the `main.py` and `data_ingestion.py` scripts using the `setup_logging` function.

```python
# main.py

def setup_logging(level=logging.INFO):
    """
    Configure logging for the application.
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
```

## Security Considerations

- **Protect API Keys:**
  - Ensure the `.env` file is **never** committed to version control systems like Git. Add `.env` to your `.gitignore` file.

    ```gitignore
    # .gitignore

    # Environment Variables
    .env
    ```

- **Handle Sensitive Data Carefully:**
  - Avoid logging sensitive information such as API keys or personal user data.
  - Implement proper error handling to prevent leakage of sensitive information through logs.

- **Adhere to Twitter's Policies:**
  - Ensure that XBot complies with Twitter's automation rules and policies to prevent account suspension.
  - Regularly review Twitter's [Developer Policy](https://developer.twitter.com/en/developer-terms/policy) for updates.

## Extending Functionality

XBot's modular and scalable design allows for easy addition of new features and integrations. Here are some suggestions to extend XBot's capabilities:

- **Dynamic Query Handling:**
  - Implement mechanisms to allow users to submit queries via Twitter mentions or direct messages, triggering automatic responses.

- **Scheduled Tweets:**
  - Integrate scheduling libraries like `schedule` or `APScheduler` to post regular updates or insights without user prompts.

- **Enhanced Error Handling:**
  - Incorporate more robust error handling and retry mechanisms to handle API interactions gracefully.

- **User Interaction Analytics:**
  - Track and analyze user interactions to improve response quality and engagement strategies.

- **Multi-platform Integration:**
  - Extend XBot to interact with other social media platforms like Facebook, LinkedIn, or Discord.

- **Rich Media Responses:**
  - Enable XBot to post images, videos, or other media types alongside text responses.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- **OpenAI:** For providing powerful language models that enable intelligent response generation.
- **Twitter:** For offering APIs that facilitate seamless integration and interaction with users.
- **LanceDB:** For its efficient and scalable vector database solutions.
- **Sentence Transformers:** For their robust embedding models that enhance data retrieval capabilities.
- **LangChain:** For simplifying the integration of language models into applications.

## Contact

For any questions, suggestions, or support, please reach out to [batu.bora.tech@gmail.com](mailto:batu.bora.tech@gmail.com).

---

**Note:** Ensure that all configurations, especially API keys and sensitive information, are securely managed and not exposed in public repositories or logs. Regularly update dependencies to their latest stable versions to benefit from security patches and new features.

Feel free to customize this README further to better suit the unique aspects and requirements of your XBot project!