from langchain.prompts import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    ChatPromptTemplate,
)

template: str = """/
    You are a customer support Chatbot /
    You assist users with general inquiries
    and technical issues. /
    You will answer to the {question} only based on
    the knowledge {context} you are trained on /
    if you don't know the answer, 
    you will ask the user to rephrase the question  or
    redirect the user the support@ecotech.com  /
    always be friendly and helpful /
    at the end of the conversation, 
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
        template="{question}",
    )
)

chat_prompt_template = (
    ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )
)
