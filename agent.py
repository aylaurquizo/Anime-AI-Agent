from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLDatabase.from_uri("sqlite:///anime.db")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)

agent = create_sql_agent(
    llm=llm,
    db=db,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=15,
    agent_executor_kwargs={"handle_parsing_errors": True}
)

print("Heyo! Welcome to Aylas Anime Database! Hope you find a great rec, ask away!")
print("Type 'exit' to quit.\n")

while True:
    question = input("Ask a question: ")
    if question.lower() == "exit":
        print("Goodbye!")
        break
    try:
        response = agent.invoke(question)
        print(response["output"])
        print()
    except Exception as e:
        print(f"\nSomething went wrong: {e}\n")
        print("Try rephrasing your question!\n")