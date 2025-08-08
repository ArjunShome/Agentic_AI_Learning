import gradio as gr
from log import logger
from openai import OpenAI
from parse_env import ParseLocalEnv as config
from multiple_llm_collaboration import ChatBot, VerifierBot



if __name__ == '__main__':
    config = config.get_env_values()
    
    chat_client = OpenAI(api_key=config["OPENAI_API_KEY"])


    verifier_client = chat_client

    chat_bot = ChatBot(client=chat_client)
    verifier_bot = VerifierBot(client=verifier_client)

    MAX_RETRY = 3

    def chat(message: list[dict], history):

        user_msg = message

        # Build a history for the chat generator
        history = [msg for msg in history if msg["role"] in ('user', 'assistant')]

        # Draft message
        draft = chat_bot.generate(user_message=user_msg, history=history)

        # Revise the chat bot response or reverify by the verifier bot
        logger.info("Evaluating Bot response...")
        evaluation = verifier_bot.verify(user_message=user_msg, model_response_to_verify=draft)
        revision = 0  # Check for retries
        
        while not evaluation.is_approved and revision < MAX_RETRY:
            history = history + [{"role": "assistant", "content": draft}]
            draft = chat_bot.generate(user_msg, history, feedback=evaluation.feedback)
            evaluation = verifier_bot.verify(user_msg, draft)
            revision += 1

        # Return the final assistant response
        logger.info("Returning Final response to the user")
        return [{"role": "assistant", "content": draft}]
    
    chat_interface = gr.ChatInterface(chat, type="messages", title="Arjun's First Agent")
    chat_interface.launch()


"""
    Todos - 
    
    # Functional -
        1. Make the App more generic so that it can accept any -
            1. Document and share or talk about its details inside
            2. An image and analyze that image and answer questions on top of it.
            3. Playing a specific role with provided details 

    # Non Functional -
        1. Make the logs prettier.
        2. Dockerize the application.
        3. Add Documentation in a markdown file with details.
"""
