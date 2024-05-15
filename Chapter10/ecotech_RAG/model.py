from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema import StrOutputParser
from langchain_community.vectorstores import Chroma
from langchain_openai import (
    ChatOpenAI,
    OpenAIEmbeddings,
)

load_dotenv()


template: str = """/
    You are a customer support Chatbot /
    You assist users with general inquiries /
    and technical issues. /
    You will answer to the {question} only based on
    the knowledge {context} you are trained on /
    if you don't know the answer, /
    you will ask the user to rephrase the question  or
    redirect the user the support@eco-tech.com /
    always be friendly and helpful /
    at the end of the conversation, /
    ask the user if they are satisfied with the answer /
    if yes, say goodbye and end the conversation  /
    """

system_message_prompt = (
    SystemMessagePromptTemplate.from_template(
        template
    )
)
human_message_prompt = (
    HumanMessagePromptTemplate.from_template(
        input_variables=["question", "context"],
        template="{question}",
    )
)
chat_prompt_template = (
    ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )
)
model = ChatOpenAI(
    model="gpt-3.5-turbo", temperature=0.3
)


def load_embeddings(documents, user_query):
    db = Chroma.from_documents(
        documents, OpenAIEmbeddings()
    )
    docs = db.similarity_search(user_query)
    print(docs)
    context = docs[0].page_content
    return context


async def generate_response(retriever, query):
    chain = (
        chat_prompt_template
        | model
        | StrOutputParser()
    )
    return await chain.ainvoke(
        {"question": query, "context": retriever}
    )


async def query_assistant(query, documents):
    retriever = load_embeddings(documents, query)
    response = await generate_response(
        retriever, query
    )
    return response
