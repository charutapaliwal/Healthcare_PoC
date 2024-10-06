import openai
import os
import sys
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from data.vectorize_data import VectorizeData

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

data_obj = VectorizeData()

prompt = """You are a question answering chatbot for a general physician application who analyzes user query {input} and OPTIONAL context: {context}. 
            user query may be about an existing patient as supported by the context or a general user query about certain symptoms.
            Based on this, you MUST provide answer to the query.
            REMEMBER THAT YOU ARE THE HEALTHCARE PROFESSIONAL."""
offtopic_prompt="""Validate if user query {input} is related to healthcare and general medical concerns.
            return TRUE if it is in the scope of healthcare and general medicine else return FALSE        
        """

class GPTIntegration():
    def __init__(self) -> None:
        self.response = " "
        self.diagnosis = " "
        self.validation = True
    def generate_diagnosis(self,context, input):
        self.response = openai.chat.completions.create(
            model="gpt-4o",  
            messages = [
                {'role':"system", 'content':prompt.format(context = context, input=input)}
            ],
            temperature = 1
        )
        self.diagnosis = self.response.choices[0].message.content.strip()
        return self.diagnosis
    def validate_offtopics(self, input, score, result):
        self.response = openai.chat.completions.create(
            model="gpt-4o",  
            messages = [
                {'role':"system", 'content':offtopic_prompt.format(input=input)}
            ],
            temperature = 1
        )
        if self.response.choices[0].message.content.strip() == "FALSE":
            self.validation = False
            score['OffTopic'] = 1.0
            result['OffTopic'] = False
        else:
            score['OffTopic'] = 0.0
            result['OffTopic'] = True
        return self.validation, score, result

if __name__ == "__main__":
    # Example patient data for testing
    model = GPTIntegration()
    user_input = input(f"Enter your query")
    example_patient = data_obj.fetch_data(user_input)
    print(model.generate_diagnosis(example_patient, user_input))
