import os
import platform  
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain.agents import create_agent
from langchain_core.tools import tool

# --- TOOLS DEFINITIONS ---

@tool
def read_file(path: str) -> str:
    """Read and returns the contents of a local text file given its path."""
    try:
        with open(path, encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

@tool
def list_files(folder_path: str = ".") -> str:
    """
    List all files and directories in the given folder path.
    If no path is provided, list the current directory.
    """
    
    try:
        items = os.listdir(folder_path)
        return str(items)
    except Exception as e:
        return f"Error listing files: {str(e)}"

@tool
def create_file(path: str, content: str) -> str:
    """
    Creates a new file at the given path with the provided content.
    Overwrites the file if it already exits.
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully created file {path}"
    except Exception as e:
        return f"Error creating file: {str(e)}"

@tool
def get_system_info() -> str:
    """
    Returns basic information about the computer system (OS, version, machine).
    """
    try:
        info = f"System: {platform.system()}\nRelease: {platform.release()}\nMachine: {platform.machine()}"
        return info
    except Exception as e:
        return f"Error getting system info: {str(e)}"

# --- AGENT SETUP ---

def run_modern_agent():
    """
    Sets up and runs a modern LangChain v1.0 agent.
    """
    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        print("🔴 Error: GOOGLE_API_KEY not found in .env file.")
        return
    print("🟢 GOOGLE_API_KEY loaded.")

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", convert_system_message_to_human=True)
    print("🟢 ChatGoogleGenerativeAI model initialized.")

    # <--- ERROR 5 FIXED: Added ALL tools to the list
    tools = [read_file, list_files, create_file, get_system_info]
    
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="You are a helpful assistant. Answer questions clearly and concisely."
    )
    print("🟢 Modern LangChain v1.0 agent created.")

    messages = []

    print("\n💬 Modern LangChain v1.0 Agent is running. Type 'exit' or 'quit' to end.")
    print("-" * 50)

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("\n👋 Goodbye!")
                break
            
            messages.append(HumanMessage(content=user_input))
            
            response = agent.invoke({"messages": messages})
            
            ai_message = response["messages"][-1]
            messages.append(ai_message)
            
            # --- SMART PRINTING LOGIC (Hides the Jargon) ---
            content = ai_message.content
            final_text = ""
            
            if isinstance(content, str):
                final_text = content
            elif isinstance(content, list):
                for part in content:
                    if isinstance(part, dict) and "text" in part:
                        final_text += part["text"]
                    elif isinstance(part, str):
                        final_text += part
            
            print(f"Agent: {final_text}")
            # ------------------------------------------------
        
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"🔴 Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    run_modern_agent()
