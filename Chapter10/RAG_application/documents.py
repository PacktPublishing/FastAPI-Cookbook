from fastapi import FastAPI
from contextlib import asynccontextmanager


from langchain.text_splitter import (
    CharacterTextSplitter,
)
from langchain_community.document_loaders import (
    TextLoader,
)


def format_docs(docs):
    return "\n\n".join(
        [d.page_content for d in docs]
    )


def load_documents():
    raw_documents = TextLoader(
        "./docs/faq_ecotech.txt"
    ).load()
    text_splitter = CharacterTextSplitter(
        chunk_size=100, chunk_overlap=0
    )
    return text_splitter.split_documents(
        raw_documents
    )


