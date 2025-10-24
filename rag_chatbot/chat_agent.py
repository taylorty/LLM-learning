# Task 6: Import the Libraries for Chat Agent
import chainlit as cl
from chainlit.input_widget import Select, TextInput
from llama_index.llms.openai import OpenAI
from llama_index.llms.gemini import Gemini
from llama_index.core.tools.query_engine import QueryEngineTool
from llama_index.core.tools.types import ToolMetadata
from llama_index.core import PromptTemplate
# from llama_index.core.agent.react.base import ReActAgent   
from llama_index.core.agent import ReActAgent
from index_wikipages import create_index
from utils import get_apikey, get_gemini_apikey


# Globals used to store runtime objects across Chainlit event hooks
index = None
agent = None

# Task 7: Initialize the Settings Menu
# Initializes the chat settings when the app starts
@cl.on_chat_start
async def on_chat_start():
    await cl.ChatSettings(
        [
            # Dropdown for selecting a model (DeepSeek via OpenRouter or Gemini)
            Select(
                id="MODEL",
                label="Model Selection",
                values=[
                    "deepseek/deepseek-r1:free",
                    "deepseek/deepseek-chat-v3-0324:free",
                    "gemini-2.0-flash-exp",
                    "gemini-1.5-pro",
                    "gemini-1.5-flash",
                ],
                initial_index=1,
            ),
            # Text input for entering a Wikipedia topic
            TextInput(id="WikiPageRequest", label="Request Wikipage"),
        ]
    ).send()

    # Prompt user to configure model and topic before starting
    await cl.Message(
        content="⚙️ Please configure the model and topic in settings before chatting."
    ).send()



# Task 8: Create the Wikipedia Search Engine
# Creates a query engine from the given index and LLM for compact Wikipedia search
def wikisearch_engine(index, llm):
    query_engine = index.as_query_engine(
        response_mode="compact",     # Returns concise results
        verbose=True,                # Enables detailed output for debugging
        similarity_top_k=3,          # Limit to top 3 most similar chunks
        llm=llm                      # Language model to use for generating responses
    )
    return query_engine



# Task 9: Create the ReAct Agent
# Creates and returns a ReAct agent using the selected LLM model and Wikipedia index
def create_react_agent(MODEL, index):
    global llm

    # Check if the model is a Gemini model or OpenRouter model
    if MODEL.startswith("gemini"):
        # Initialize the Gemini LLM
        llm = Gemini(
            model=MODEL,
            api_key=get_gemini_apikey(),
        )
    else:
        # Initialize the LLM via OpenRouter using the model selected by the user
        llm = OpenAI(
            api_key=get_apikey(),
            api_base="https://openrouter.ai/api/v1",
            model_name=MODEL,
        )

    # Set up a query engine tool for Wikipedia search
    query_engine_tool = QueryEngineTool(
        query_engine=wikisearch_engine(index, llm),
        metadata=ToolMetadata(
            name="Wikipedia",
            description="Useful for searching Wikipedia for information. Input should be a specific question or topic to search for.",
        ),
    )

    tools = [query_engine_tool]
    
    # Build the agent with the tools, LLM, and verbose setting
    # The ReActAgent class has to be instantiated directly, not from a class method.
    agent = ReActAgent(
        tools=tools,
        llm=llm,
        verbose=True
    )

    return agent



# Task 10: Finalize the Settings Menu
# Triggered whenever the user updates the settings menu (e.g., model or topic)
@cl.on_settings_update
async def setup_agent(settings):
    global agent  # Access the global agent so it can be updated
    global index  # Access the global index to store the Wikipedia search index

    # Extract the requested Wikipedia topic(s) from settings
    query = settings["WikiPageRequest"]
    if not isinstance(query, str):
        query = str(query)

    # Get the selected model name from settings
    MODEL = settings["MODEL"]
    if not isinstance(MODEL, str):
        MODEL = str(MODEL)

    # Create a document index for the given Wikipedia topic(s) using the selected model
    index = create_index(query, MODEL)
    print("Index created for query:", query, "using model:", MODEL)

    # Log the full settings for debugging purposes
    print("on_settings_update", settings)

    # Create a new ReAct agent using the model and indexed documents
    agent = create_react_agent(MODEL, index)

    # Send confirmation message to the chat UI
    await cl.Message(
        author="Agent", content=f"""Wikipage(s) "{query}" successfully indexed using {MODEL}"""
    ).send()



# Task 11: Script the Chat Interactions
@cl.on_message
async def main(message: str):
    global agent

    # Log the content of the incoming user message
    print("Received message:", message.content)

    if agent:
        response = await agent.run(message.content) 
        print("response:", response, "\n\n")
        await cl.Message(author="Agent", content=response.response).send()
    else:
        await cl.Message(
            author="Agent",
            content="Agent not initialized. Please set a WikiPageRequest in the settings."
        ).send()
