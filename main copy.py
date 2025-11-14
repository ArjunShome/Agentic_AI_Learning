from multiple_llm_collaboration import chat_bot_evaluator_optimizer_model as chat
import gradio as gd
from openai import OpenAI


openai = OpenAI()

def chat(message, history):
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
    return response.choices[0].message.content

if __name__ == '__main__':
    