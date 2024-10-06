import os
import openai
from dotenv import load_dotenv
from nemoguardrails import LLMRails, RailsConfig
import nemoguardrails
import asyncio
from guardrails.nemo_config import colang_content, yaml_content

load_dotenv()
openai.api_key=os.getenv("OPENAI_API_KEY")

prompt = """You are a question answering chatbot for a general physician application who analyzes user query {input} and OPTIONAL context: {context}. 
            user query may be about an existing patient as supported by the context or a general user query about certain symptoms.
            Based on this, you MUST provide answer to the query.
            REMEMBER THAT YOU ARE THE HEALTHCARE PROFESSIONAL."""

def generate_diagnosis(input, data):
    try:
        config = RailsConfig.from_content(
            yaml_content = yaml_content,
            colang_content = colang_content
        )
        # config = RailsConfig.from_path("./guardrails/config")
        rails = LLMRails(config)
        # res = await rails.generate_async(prompt = input)
        res = rails.generate(
            prompt=prompt.format(context=data, input=input),
            messages=[{'role':'user','content':input}]
        )
        info = rails.explain()
        info.print_llm_calls_summary()
        return res
    except Exception as e:
        print(f"Exception occured at guardrails diagnosis: {e}")

if __name__ == "__main__":
    #Example usage for testing
    input = "What is SSN of Elizabeth Hartman?"
    async def main():
        result = await generate_diagnosis(input, data = "SSN IS 0123")
        print(result)
    asyncio.run(main())
