from phi.assistant import Assistant
from phi.tools.duckduckgo import DuckDuckGo
from typing import Generator, Optional, List, Dict, Any, Literal
from pydantic import BaseModel

class Response(BaseModel):
    chat_history: List[Dict[str, Any]]

# Assistant - Web_search
async def assistant_web_search(prompt: str):
  assistant = Assistant(tools=[DuckDuckGo()], show_tool_calls=True)
  assistant.print_response(prompt, markdown=True)
  
  Response.chat_history = assistant.memory.get_chat_history()

  return Response.chat_history

# Assistant - RAG
# async def assistant_web_search(prompt: str):
#   assistant = Assistant(tools=[DuckDuckGo()], show_tool_calls=True)
#   assistant.print_response(prompt, markdown=True)
  
#   Response.chat_history = assistant.memory.get_chat_history()

#   return Response.chat_history