from phi.assistant import Assistant
from phi.tools.duckduckgo import DuckDuckGo
from typing import Generator, Optional, List, Dict, Any, Literal
from pydantic import BaseModel
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector2

######################################################
## Assistant Construct - default
## from phi.llm.openai import OpenAIChat
## assistant = Assistant(
##   llm=OpenAIChat(
##         model="gpt-3.5-turbo",
##       ),
##       description="You help people with their health and fitness goals.",
## )
###################################################### 

class Response(BaseModel):
    chat_history: List[Dict[str, Any]]

# Assistant - Web_search
async def assistant_web_search(prompt: str):
  assistant = Assistant(tools=[DuckDuckGo()], show_tool_calls=True)
  assistant.print_response(prompt, markdown=True)
  
  Response.chat_history = assistant.memory.get_chat_history()

  return Response.chat_history

# Assistant - RAG_knowledge_base
async def assistant_knowledge_base(prompt: str):
  knowledge_base = PDFUrlKnowledgeBase(
      # Read PDFs from URLs
      urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
      # Store embeddings in the `ai.recipes` table
      vector_db=PgVector2(
          collection="recipes",
          db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
      ),
  )
  # Load the knowledge base
  knowledge_base.load(recreate=False)

  assistant = Assistant(
      knowledge_base=knowledge_base,
      # The add_references_to_prompt will update the prompt with references from the knowledge base.
      add_references_to_prompt=True,
  )
  assistant.print_response(prompt, markdown=True)
  Response.chat_history = assistant.memory.get_chat_history()

  return Response.chat_history