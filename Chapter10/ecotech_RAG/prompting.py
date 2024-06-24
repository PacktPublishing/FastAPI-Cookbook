from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

template: str = """
    You are a customer support Chatbot. 
    You assist users with general inquiries
    and technical issues.
    You will answer to the question: 
    {question} 
    Your answer will only be based on the knowledge 
    of the context below you are trained on.
    -----------
    {context}
    -----------
    if you don't know the answer, 
    you will ask the user to rephrase the question  or
    redirect the user the support@ecotech.com
    always be friendly and helpful
    at the end of the conversation, 
    ask the user if they are satisfied with the answer
    if yes, say goodbye and end the conversation
    """

system_message_prompt = (
    SystemMessagePromptTemplate.from_template(
        template
    )
)

human_message_prompt = (
    HumanMessagePromptTemplate.from_template(
        template="{question}",
    )
)

chat_prompt_template = (
    ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )
)
