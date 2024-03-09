from openai import OpenAI
import time

client = OpenAI(
    api_key = "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"
)

chat_response = client.chat.completions.create(
    
    model="gpt-3.5-turbo",
    messages = [
        {
            "role" : "user",
            "content" : "Me dê uma curta frase de motivação para manter o foco (em português)"
        }
    ]

)


print(chat_response)
    
