# combined_script.py

from lance_db_utils import LanceDBUtils, LocalEmbeddings, OpenAILLM
from twitter_utils import create_api, send_direct_message, get_user_id

def main():
    # Initialize the LanceDB utilities
    db_utils = LanceDBUtils(db_path='my_lancedb')

    # Open the existing table
    table = db_utils.create_table('my_table')

    # Initialize the local embedding function
    embedding_fn = LocalEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    # Initialize the OpenAI LLM
    openai_llm = OpenAILLM(model='gpt-3.5-turbo')

    # Get the user's query (you can modify this to get input from the command line or other sources)
    user_query = input("Enter your question: ")

    # Retrieve relevant information from LanceDB
    relevant_texts = db_utils.retrieve_relevant_info(
        query_text=user_query,
        embedding_fn=embedding_fn,
        top_k=3  # Number of relevant documents to retrieve
    )

    # Check if any relevant texts were found
    if not relevant_texts:
        print("No relevant information found in the database.")
        return

    # Combine the retrieved information into a context for the LLM
    context = '\n'.join(relevant_texts)

    # Construct the prompt for the OpenAI LLM
    system_prompt = (
        "You are a helpful assistant. Use the following context to answer the user's question."
    )
    full_prompt = f"{context}\n\nUser's question: {user_query}\nAnswer:"

    # Generate a response
    response = openai_llm.generate_response(prompt=full_prompt, system_prompt=system_prompt)

    print("\nLLM Response:")
    print(response)

    # Initialize Twitter API
    api = create_api()

    # Get recipient user ID (replace 'recipient_screen_name' with the actual Twitter handle)
    recipient_screen_name = 'recipient_screen_name'
    recipient_id = get_user_id(api, recipient_screen_name)

    # Send the response as a direct message
    send_direct_message(api, recipient_id, response)
    print(f"Message sent to {recipient_screen_name}.")

if __name__ == '__main__':
    main()
