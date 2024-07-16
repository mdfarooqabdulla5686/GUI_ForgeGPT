import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# # st.write("""Hello World""")
# with st.chat_message("user"):
#     st.write("Hello ")

# Title of the LLM
st.set_page_config(page_title="ForgeGPT")
st.title("ForgeGPT")

#Get Response from LLM
def get_response (query,chat_history):
    template = """
    Answer the following question based in the provided context and your internal knowledge.
    Give priority to context and if you are not sure then say you are not aware of topic:
    
    </context>
    Chat history: {chat_history}
    User question: {user_question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    llm = Ollama(model="llama3")
    # llm

    chain = prompt | llm | StrOutputParser()
    return chain.invoke({
        "chat_history": chat_history,
        "user_question": user_query,
    })


#Chat history storing in array
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

#User Input Box 
user_query = st.chat_input("Your Message")

#Conversation
for message in st.session_state.chat_history:
    if isinstance(message,HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)   


#Human Vs AI Message and Response
if user_query is not None and user_query!="":
    st.session_state.chat_history.append(HumanMessage(user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        ai_response = get_response(user_query, st.session_state.chat_history)
        st.markdown(ai_response)

    st.session_state.chat_history.append(AIMessage(ai_response))