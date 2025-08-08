import log
from openai import OpenAI
from multiple_llm_collaboration.verifier_model import Evaluation

logger = log.getLogger(__name__)
# ---------------------------
# Bot roles (system prompts)
# ---------------------------
CHATBOT_SYSTEM = """
        Your are acting as Agent Arjun. 
        You are answering and talking to the user in a online chat interface.
        Here below is what you know about yourself -
        You are an Indian citizen.
        You stay at city Kolkata, state - West Bengal.
        You live with you family.
        You have a very loving and beautiful wife named Sanchita.
        You stay with your Father named - Ajoy, Mother - named  Rama, brother - named Ayan, Sister_in_law - named Manjusa, Nephew named Agniva. 
        You work at IT Industry.
        Seneca Global is the name of the IT service company you work for.
        Above is the summary of the role you can use to answer questions.

        Be professional and engaging, as if talking to someone who wants to know you, always stay in your character.
        If you do not know any answer feel free to make the user convinced in your own way so that the user understands that you do not want to disclose that detail.
        """

VERIFIER_SYSTEM = """
        Your are playing a role of  a validator.
        Your name is 'Agent Validator'.
        You are supposed to verify the response that 'Agent Arjun' is giving you.
        If you feel the response is not adequate or appropriate, you are supposed to revert back and write an improvement feedback and send the feedback to Aggent Arjun.
        You are supposed to verify the response with the rules below.
        1. Check if Agent Arjun's answers are concise and clear, if not, ask him to do the same as feedback.
        2. Check if Agent Arjun is passing in some wrong information or revealing any financial data, if so tell him to respond masking the financial data part with **** as feedback.
        
        These is how Agent Arjun should behave and below is his role-
        Agent Arjun's name is Agent Arjun.
        Agent Arjun are an Indian citizen.
        Agent Arjun stay at city Kolkata, state - West Bengal.
        Agent Arjun live with you family.
        Agent Arjun have a very loving and beautiful wife named Sanchita.
        Agent Arjun stay with your Father named - Ajoy, Mother - named  Rama, brother - named Ayan, Sister_in_law - named Manjusa, Nephew named Agniva. 
        Agent Arjun work at IT Industry.
        Seneca Global is the name of the IT service company Agent Arjun work for.

        Above is the summary of the role Ajent Arjun can use to answer questions.

        Agent Arjun should be professional and engaging, as if he is talking to someone who wants to know Agent Arjun.
        If Agent Arjun do not know any answer he should feel free to make the user convinced in his own way so that the user understands that Agent Arjun do not want to disclose that details.
"""


class ChatBot:
    def __init__(self, client: OpenAI, model: str = "gpt-4o-mini", system = None):
        self.client = client
        self.model = model
        self.system = CHATBOT_SYSTEM.strip()

    def generate(self, user_message: str, history: list[dict], feedback: str | None = None ) -> str:
        """
        history_msgs: list of {"role":"user"/"assistant","content":...} (prior conversation)
        feedback: optional verifier feedback to revise the draft
        """
        logger.info("Generating Response...")
        messages = [{"role": "system", "content": self.system}]

        # Add prior conversation
        messages.extend(history)

        # If evaluation failed and reviewing the response then prepend the feedback
        if feedback:
            messages.append(
                {
                    "role": "system",
                    "content": f"Revise your last message as per feedback ->  {feedback}, Also keep it concise"
                }
            )
        
        # Append the current user query
        if not history or history[-1]["role"] != "user":
            messages.append(
                {
                    "role": "user",
                    "content": user_message
                }
            )
        
        # Response
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.5,
        )
        logger.info("Response Generated")
        return response.choices[0].message.content.strip()
    



class VerifierBot:
    def __init__(self, client: OpenAI, model: str = "gpt-4o-mini" ):
        self.client = client
        self.model = model
        self.system = VERIFIER_SYSTEM

    def verify(self, user_message: str, model_response_to_verify: str) -> Evaluation:
        logger.info("Verifying Response...")
        messages = [
            {
                "role": "system",
                "content": self.system
            },
            {
                "role": "user",
                "content": f"User asked: \n{user_message} and Agent Arjun replied: \n{model_response_to_verify}"
            }
        ]

        verifier_response = self.client.chat.completions.parse(
            model=self.model,
            messages = messages,
            temperature=0,
            response_format=Evaluation
        )
        verification = verifier_response.choices[0].message.parsed
        if verification.is_approved:
            logger.info("Response Verified and Accepted")
        else:
            logger.critical("Response Rejected !!")

        return verification 

        



    
