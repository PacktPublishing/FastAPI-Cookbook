import os
from dotenv import load_dotenv
from langchain_openai import (
    ChatOpenAI,
    OpenAIEmbeddings,
)
from langchain_community.document_loaders import (
    TextLoader,
)
from langchain.text_splitter import (
    CharacterTextSplitter,
)
from langchain.prompts.chat import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import (
    RunnablePassthrough,
)
from langchain_community.vectorstores import Chroma

load_dotenv()

# https://python.langchain.com/docs/modules/data_connection/vectorstores/

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGUAGE_MODEL = "gpt-3.5-turbo-instruct"

template: str = """/
    You are a customer support specialist /
    question: {question}. /
    You assist users with general inquiries /
    based on {context} /
    and  technical issues. /
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

model = ChatOpenAI()


def format_docs(docs):
    return "\n\n".join(
        [d.page_content for d in docs]
    )


def load_documents():
    raw_documents = TextLoader(
        "./docs/faq_abc.txt"
    ).load()
    text_splitter = CharacterTextSplitter(
        chunk_size=100, chunk_overlap=0
    )
    return text_splitter.split_documents(
        raw_documents
    )


def load_embeddings(documents, user_query):
    db = Chroma.from_documents(
        documents, OpenAIEmbeddings()
    )
    docs = db.similarity_search(user_query)
    print(docs)
    return db.as_retriever()


def generate_response(retriever, query):
    # pass
    # Create a prompt template using a template from the config module and input variables
    # representing the context and question.
    # create the prompt

    chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough(),
        }
        | chat_prompt_template
        | model
        | StrOutputParser()
    )
    return chain.invoke(query)


def query(query):
    documents = load_documents()
    retriever = load_embeddings(documents, query)
    response = generate_response(retriever, query)
    return response
