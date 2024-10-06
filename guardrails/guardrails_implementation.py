import os
import openai
from dotenv import load_dotenv

from llm_guard import scan_output, scan_prompt
from llm_guard.input_scanners import Toxicity, BanTopics, Gibberish, Sentiment
from llm_guard.output_scanners import NoRefusal, Relevance, Sensitive

load_dotenv()
openai.api_key=os.getenv("OPENAI_API_KEY")

INPUT_SCANNERS = [Toxicity(), Gibberish(threshold=0.99), Sentiment(threshold = -0.5),BanTopics(topics=["violence"])]
OUTPUT_SCANNERS = [Relevance(), Sensitive(entity_types=['EMAIL_ADDRESS','US_SSN','US_SSN_RE','ADDRESS','PHONE_NUMBER','EMAIL_ADDRESS_RE'])]

class ImplementGuardrails:
    def __init__(self) -> None:
        self.is_valid = True

    def scan_input(self, input_query):
        sanitized_prompt, results_valid, results_score = scan_prompt(INPUT_SCANNERS,input_query)
        if False in results_valid.values():
            self.is_valid = False
        return self.is_valid, sanitized_prompt, results_score, results_valid
    
    def scan_output(self, sanitized_input, response):
        sanitized_response_text, results_valid, results_score = scan_output(
            OUTPUT_SCANNERS, sanitized_input, response
        )
        if False in results_valid.values():
            self.is_valid = False
        return self.is_valid, sanitized_response_text, results_valid, results_score

if __name__ == "__main__":
    #Example usage for testing
    gd = ImplementGuardrails()
    input_query = input("Enter your query")
    is_valid, prompt_sn, score, results = gd.scan_input(input_query)
    print("Input scan results:")
    print(is_valid, prompt_sn, score, results)
    output = input("Enter your response")
    is_valid, response, results, score = gd.scan_output(prompt_sn,output)
    print("output scan results:")
    print(is_valid, response, score, results)
   
