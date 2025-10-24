# Task 2: Import the Libraries
import requests
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, Settings, Document
from llama_index.core.node_parser import SentenceSplitter
from pydantic import BaseModel
from utils import get_apikey, get_gemini_apikey
from openai import OpenAI
import google.generativeai as genai
import json



# Task 3a: Create and develop the WikiPageList class
class WikiPageList(BaseModel):
    """Data model for WikiPageList"""
    pages: list

# Task 3b: Define the OpenRouter API calling function
def call_deepseek_api_openrouter(prompt, api_key, model="deepseek/deepseek-r1:free"):
    # Initialize OpenAI client with OpenRouter's DeepSeek-compatible base URL
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    # Make a chat completion request using the specified model
    completion = client.chat.completions.create(
        extra_headers={},  # Optional custom headers
        extra_body={},     # Optional additional payload
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts Wikipedia page names from text and returns ONLY JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2  # Low temperature for consistent and structured responses
    )

    # Return just the message content from the response
    return completion.choices[0].message.content


# Task 3b (Gemini): Define the Gemini API calling function
def call_gemini_api(prompt, api_key, model="gemini-1.5-flash"):
    # Configure the Gemini API with the provided key
    genai.configure(api_key=api_key)
    
    # Initialize the Gemini model
    gemini_model = genai.GenerativeModel(model)
    
    # Create the full prompt with system instructions
    full_prompt = f"""You are a helpful assistant that extracts Wikipedia page names from text and returns ONLY JSON.

{prompt}"""
    
    # Generate response
    response = gemini_model.generate_content(
        full_prompt,
        generation_config=genai.GenerationConfig(
            temperature=0.2,
        )
    )
    
    # Return the generated text
    return response.text




# Task 3c: Complete the wikipage_list() function
def wikipage_list(query, model=None):
    # Create a prompt asking the model to extract Wikipedia page names in JSON format
    prompt = f"""
    Please extract Wikipedia page names from the following sentence:
    '{query}'
    Respond only with a JSON object like:
    {{ "pages": ["Natural language processing", "Neural networks"] }}
    """

    # Determine which API to use based on the model
    if model and model.startswith("gemini"):
        api_key = get_gemini_apikey()
        raw_response = call_gemini_api(prompt, api_key, model)
    else:
        # Default to DeepSeek via OpenRouter
        api_key = get_apikey()
        if model and not model.startswith("gemini"):
            raw_response = call_deepseek_api_openrouter(prompt, api_key, model)
        else:
            raw_response = call_deepseek_api_openrouter(prompt, api_key)

    # Attempt to parse the LLM response into a structured WikiPageList
    try:
        # Clean up the response - remove markdown code blocks if present
        cleaned_response = raw_response.strip()
        if cleaned_response.startswith("```"):
            # Remove markdown code block formatting
            lines = cleaned_response.split("\n")
            cleaned_response = "\n".join([line for line in lines if not line.strip().startswith("```")])
        
        return WikiPageList.model_validate_json(cleaned_response.strip())
    except Exception as e:
        print("Could not parse LLM response:", raw_response)
        print("Error:", e)
        # Try to extract JSON from the response manually
        try:
            # Look for JSON object in the response
            start_idx = raw_response.find("{")
            end_idx = raw_response.rfind("}") + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = raw_response[start_idx:end_idx]
                return WikiPageList.model_validate_json(json_str)
        except:
            pass
        return WikiPageList(pages=[])  # Return an empty list if parsing fails



# Task 4: Define the function to safely load Wikipedia pages
def safe_load_documents(page_titles):
    print("PAGE_TITLES", page_titles)
    documents = []

    for title in page_titles:
        try:
            # Try to fetch the full Wikipedia page content
            wiki_page = wikipedia.page(title, auto_suggest=False, redirect=True)
            content = wiki_page.content
            metadata = {"title": wiki_page.title, "source": "wikipedia"}

            # Wrap the content and metadata in a Document object
            documents.append(Document(text=content, metadata=metadata))
            print(f"Successfully loaded content for '{title}'.")

        except wikipedia.exceptions.PageError:
            print(f"PageError: Wikipedia page '{title}' not found.")

        except wikipedia.exceptions.DisambiguationError as e:
            print(f"DisambiguationError: '{title}' has multiple meanings: {e.options}")

        except Exception as e:
            print(f"Unhandled error for page '{title}': {e}")

    return documents



# Task 4 (continued): Wrapper function to create Wiki documents
def create_wikidocs(wikipage_requests):
    # Load the documents for all Wikipedia pages listed in the request
    documents = safe_load_documents(wikipage_requests.pages)
    return documents



# Task 5: Define the create_index() function
def create_index(query, model=None):
    global index

    # Extract Wikipedia page names from the query using the specified model
    wikipage_requests = wikipage_list(query, model)

    # Download and structure the content of each Wikipedia page
    documents = create_wikidocs(wikipage_requests)

    # Split the documents into manageable chunks for embedding
    text_splits = SentenceSplitter(chunk_size=150, chunk_overlap=45)
    nodes = text_splits.get_nodes_from_documents(documents)

    try:
        # Initialize the embedding model and assign it to the global Settings
        embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
        Settings.embed_model = embed_model

        # Create a vector index from the text nodes
        index = VectorStoreIndex(nodes, embed_model=embed_model)
        return index
    except Exception as e:
        print(f"Error initializing embedding model or index: {e}")
        return None



# Task 5: Allow CLI execution for debugging purposes
if __name__ == "__main__":
    query = "/get wikipages: paris, lagos"
    index = create_index(query)
    print("INDEX CREATED", index)


