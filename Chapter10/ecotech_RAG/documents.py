from langchain.text_splitter import (
    CharacterTextSplitter,
)
from langchain_community.document_loaders import (
    DirectoryLoader,
)
from langchain_community.vectorstores import Chroma


async def load_documents(
    db: Chroma,
):
    text_splitter = CharacterTextSplitter(
        chunk_size=100, chunk_overlap=0
    )

    raw_documents = DirectoryLoader(
        "docs", "*.txt"
    ).load()

    chunks = text_splitter.split_documents(
        raw_documents
    )
    await db.aadd_documents(chunks)


def get_context(user_query: str, db: Chroma) -> str:
    docs = db.similarity_search(user_query)
    return "\n\n".join(
        doc.page_content for doc in docs
    )
