"""
This script sets up a FastAPI server to interact with a language model from Vertex AI. It is specifically configured to handle user queries related to data finding, leveraging the 'chat-bison' model. The server processes user queries, retrieves relevant context from stored data, and generates responses based on the context and the model's capabilities.

Key Components:
- Load data and model: The script begins by loading necessary data and initializing the chat model.
- API routes: Defines an API route to handle POST requests where users can submit their queries.
- Query processing: User queries are processed to extract keywords, fetch relevant document context, and generate responses using the chat model.

Usage:
1. Send a POST request to the API endpoint with a user query.
2. The server processes the query, finds relevant documents, and generates a response using the chat model.
3. The response is then sent back to the user.

Example:
    POST /
    {
        "question": "Tell me about data storage solutions",
        "new_chat": "true"
    }

Dependencies:
- FastAPI: For setting up the API server.
- Pydantic: For data validation and settings management.
- VertexAI: For accessing and using the language models.
- Helper modules: Custom modules for query processing, data handling, and interacting with the chat model.
"""

from fastapi import APIRouter, Body
from pydantic import BaseModel
import vertexai
import json


# Importing helper modules
from .helper.query_helper import *
from .helper.data_helper import *
from .helper.relevant_data_helper import *
from .helper.prompt_helper import *
from ..helper import *

# Initialize FastAPI router
router = APIRouter()

# Execute before taking requests

# Load data from a GCP bucket
blob = read_from_bucket('template-chatbot', 'Data/bot_context_data1.json')
data = json.loads(blob.download_as_string(client=None))

# Load the ChatModel
chat_model = vertexai.language_models.ChatModel.from_pretrained('chat-bison@001')

# Defining Model Parameters for the chat model
parameters = {
    "temperature": 0.2,
    "max_output_tokens": 256,
    "top_p": 0.8,
    "top_k": 40
}

# Pydantic model for handling query requests
class Query(BaseModel):
    question: str
    new_chat: str

# Chat class for managing chat sessions
class Chat():
    def __init__(self):
        self.chat_model = vertexai.language_models.ChatModel.from_pretrained('chat-bison@001')
        self.chat = self.chat_model.start_chat()

    def getOldChat(self):
        return self.chat

    def getNewChat(self, relevant_docs):
        self.chat = self.chat_model.start_chat(context=str(relevant_docs), examples=chat_prompt_examples)
        return self.chat

# Initialize chat model
chat = Chat()

# API route to handle POST requests and provide bot responses
@router.post("/", response_description="Bot Response")
async def get_datafinder_BotResponse(query: Query):
    if query.new_chat == 'true':
        # Extract keywords from the query
        query_keywords = get_keywords(query.question)

        # Retrieve relevant documents based on keywords
        relevant_docs = get_relevant_docs(query_keywords, data)

        try:
            # Start a new chat session with relevant context
            new_chat = chat.getNewChat(relevant_docs)

            # Send initial prompt to the model
            new_chat.send_message(initial_prompt)

            # Send the user's query to the model
            new_chat.send_message(query.question + cmd, **parameters)

            # Additional command for checking context relevance
            cmd3 = 'is this present in the context, if it is then reply saying yes I have information regarding this doc followed by the same previous answer, if not just say I do not have infomation regarding this'
            response = new_chat.send_message(cmd3, **parameters).text

        except:
            response = "I don't have information regarding this"

    else:
        # Continue the existing conversation
        old_chat = chat.getOldChat()
        response = old_chat.send_message(query.question + cmd, **parameters).text

    return ResponseModel(response, "bot reply")

# Additional routes and functions can be added as needed.
