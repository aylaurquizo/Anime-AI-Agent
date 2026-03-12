import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()
google_api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="Aylas Anime Recommendation Bot", page_icon=":tv:", layout="centered")
st.title("Aylas Anime Recommendation Bot")
st.caption("Hey! Ask me anything about anime, I'll be adding my comments to ones I've sen, so keep an eye out for that. Ask anything about recommendations, stats, comparisons, etc. You'll find a list of the columns this bot queries on at the bottom.")

if "messages" not in st.session_state:
    st.session_state.messages = []

@st.cache_resource
def load_agent():
    db = SQLDatabase.from_uri("sqlite:///anime.db")
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0
    )
    agent = create_sql_agent(
        llm=llm,
        db=db,
        verbose=False,
        handle_parsing_errors=True,
        max_iterations=15,
        agent_executor_kwargs={"handle_parsing_errors": True}
    )
    return agent

agent = load_agent()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask away!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = agent.invoke(prompt)
                    answer = response["output"]
                except Exception as e:
                    answer = f"Error: {str(e)}"
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})