import streamlit as st 
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import time

load_dotenv()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Chat With Raya Bot", page_icon="🐱‍🚀")

st.title("Chat With Raya Bot")


# get response 
def get_response(query, chat_history):
    template = """
    You are a helpfull assistant. Your Name is Raya, Do not forget your name. You need to answer the following Question considering the following conversation
    
    Chat history: {chat_history}
    
    User questions: {user_questions}
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    llm = ChatOpenAI()
    
    chain = prompt | llm | StrOutputParser()
    
    return chain.stream({
        "chat_history": chat_history,
        "user_questions": query
    })
    
    

for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"): 
            st.markdown(message.content)
            
def stream_data():
    res = get_response(user_query, st.session_state.chat_history)
    for word in res:
        yield word + ""
        time.sleep(0.1)
            


user_query = st.chat_input("Plase type your message")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(user_query))
    
    with st.chat_message("Human"):
        st.markdown(user_query)        
    
    with st.chat_message("AI"):
        
        ai_response = st.write_stream(stream_data())
        
    st.session_state.chat_history.append(AIMessage(ai_response))

