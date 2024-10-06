import streamlit as st
import openai
import os
from dotenv import load_dotenv
import pandas as pd
import tracemalloc
from gpt_integration.gpt_integration import GPTIntegration
import time
import warnings
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from red_team.red_team_integration import HealthcareRedTeam
from data.vectorize_data import VectorizeData
#from guardrails.guardrails_integration  import generate_diagnosis
from guardrails.guardrails_implementation import ImplementGuardrails
from risk_assessment.risk_questionnaire import risk_questionnaire

warnings.filterwarnings("ignore",category=Warning)

tracemalloc.start()

load_dotenv()
openai_api_key= os.getenv('OPENAI_API_KEY') 

#initialize instances
data_obj=VectorizeData()
gpt_obj=GPTIntegration()
red_team_obj = HealthcareRedTeam()
gd = ImplementGuardrails()

#globals / constants
context=[]
EVAL_METRICS = ""
IS_PROMPT_VALID = True
IS_RESPONSE_VALID = True
INVALID_PROMPT_RESPONSE = 'As a general physician chatbot, I cannot respond to this query. Is there something else that I can help you with?'

#helper functions
def stream_data(data):
    for word in data.split(" "):
        yield word + " "
        time.sleep(0.02)

def query_processing(question_list):
    answers_list = []
    context_list =[]
    for question in question_list:
        context_list.append(data_obj.fetch_data(question))
        answers_list.append(gpt_obj.generate_diagnosis(context, question))
    return context_list, answers_list

# streamlit implementation
try:
    # Streamlit UI
    st.set_page_config(layout = 'wide', page_title='Trustaworthy AI Healthcare Diagnostics')

    # Main Tabs: Chat and TWAI Components
    tab1, tab2 = st.tabs(["Chat", "TWAI Components"])

    with tab1:
        st.header("Chat with Physician Agent")

        input_query = st.chat_input("Enter your query")
        if input_query:
            with st.spinner("Processing query ..."):
                IS_PROMPT_VALID, gd_prompt, gd_score, gd_results = gd.scan_input(input_query)
                IS_ONTOPIC, gd_score, gd_results = gpt_obj.validate_offtopics(gd_prompt, gd_score, gd_results)
                print(IS_PROMPT_VALID, IS_ONTOPIC, gd_score, gd_results)
                if IS_PROMPT_VALID and IS_ONTOPIC:
                    context = data_obj.fetch_data(input_query)
                    diagnosis = gpt_obj.generate_diagnosis(context,gd_prompt)
                    IS_RESPONSE_VALID, gd_response, gd_results, gd_score = gd.scan_output(gd_prompt,diagnosis)
                    print(IS_RESPONSE_VALID, gd_response, gd_results, gd_score)
                    if IS_RESPONSE_VALID:
                        st.chat_message('assistant').write_stream(stream_data(diagnosis))
                    else:
                        st.chat_message('assistant').write_stream(stream_data(INVALID_PROMPT_RESPONSE))
                        st.write(gd_results, gd_score)
                else:
                    st.chat_message('assistant').write_stream(stream_data(INVALID_PROMPT_RESPONSE))
                    st.write(gd_results, gd_score)
    with tab2:
        st.header("TWAI Components")

        # Sub-tabs within TWAI Components
        sub_tab1, sub_tab2, sub_tab3 = st.tabs(["Red Teaming", "Bias Detection", "Risk Questionnaire"])

        with sub_tab1:
            data = '''
                    The harms generative AI systems create are, in many cases, different from other forms of AI in both scope and scale. 
                    Red teaming generative AI is specifically designed to generate harmful content that has no clear analogue in traditional software systems — 
                    from generating demeaning stereotypes and graphic images to flat out lying. 
                    For this application, we have demonstrated red teaming efforts with below degradation objectives (some objectives were derived from incidents of AI incident databse and OWASP top 10 LLM applications):
            '''
            st.write(data)
            # Implement red teaming functionalities
            col1, col2 = st.columns([1,3])
            with col1:
                if st.button("Toxicity / Offensive content"):
                    objective = "Toxicity / Offensive content"
                    EVAL_METRICS = "ToxicityMetric"
                    question_list = red_team_obj.red_teamer_prompt_list(objective)
                    context_list, answers_list = query_processing(question_list)
                    with col2:
                        for question, answer, context in zip(question_list, answers_list, context_list):
                            st.write("Q: ",question)
                            st.write("A:",answer)
                            st.write("Context:", context)
                            score, success, reason = red_team_obj.deep_evaluate(question,answer,context,objective,EVAL_METRICS)
                            st.write("Evaluation:",f"Score:{score}", f"Success:{success}", f"Reason: {reason}")
                if st.button("Criminal / Illicit activities"):
                    objective = "Criminal / Illicit activities"
                    EVAL_METRICS = "Criminal"
                    question_list = red_team_obj.red_teamer_prompt_list(objective)
                    context_list,answers_list = query_processing(question_list)
                    with col2:
                        for question, answer, context in zip(question_list, answers_list,context_list):
                            st.write("Q: ",question)
                            st.write("A:",answer)
                            st.write("Context:", context)
                            score, success, reason = red_team_obj.deep_evaluate(question,answer,context,objective,EVAL_METRICS)
                            st.write("Evaluation:",f"Score:{score}", f"Success:{success}", f"Reason: {reason}")
                if st.button("Bias Propagation"):
                    objective ="Bias Propagation"
                    EVAL_METRICS = 'BiasMetric'
                    question_list = red_team_obj.red_teamer_prompt_list(objective)
                    context_list,answers_list = query_processing(question_list)
                    with col2:
                        for question, answer, context in zip(question_list, answers_list, context_list):
                            st.write("Q: ",question)
                            st.write("A:",answer)
                            st.write("Context:", context)
                            score, success, reason = red_team_obj.deep_evaluate(question,answer,context,objective,EVAL_METRICS)
                            st.write("Evaluation:",f"Score:{score}", f"Success:{success}", f"Reason: {reason}")
                if st.button("Privacy and Data Security"):
                    objective = "Privacy and Data Security"
                    EVAL_METRICS="PrivacyDataSecurity"
                    question_list = red_team_obj.red_teamer_prompt_list(objective)
                    context_list,answers_list = query_processing(question_list)
                    with col2:
                        for question, answer,context in zip(question_list, answers_list, context_list):
                            st.write("Q: ",question)
                            st.write("A:",answer)
                            st.write("Context:", context)
                            score, success, reason = red_team_obj.deep_evaluate(question,answer,context,objective,EVAL_METRICS)
                            st.write("Evaluation:",f"Score:{score}", f"Success:{success}", f"Reason: {reason}")
                if st.button("Off Topic"):
                    objective = "Off Topic"
                    EVAL_METRICS = "OffTopic"
                    question_list = red_team_obj.red_teamer_prompt_list(objective)
                    context_list,answers_list = query_processing(question_list)
                    with col2:
                        for question, answer, context in zip(question_list, answers_list, context_list):
                            st.write("Q: ",question)
                            st.write("A:",answer)
                            st.write("Context:", context)
                            score, success, reason = red_team_obj.deep_evaluate(question,answer,context,objective,EVAL_METRICS)
                            st.write("Evaluation:",f"Score:{score}", f"Success:{success}", f"Reason: {reason}")
                if st.button("Hallucinations"):
                    objective = "Hallucinations"
                    EVAL_METRICS = 'HallucinationsMetric'
                    question_list = red_team_obj.red_teamer_prompt_list(objective)
                    context_list, answers_list = query_processing(question_list)
                    with col2:
                        for question, answer, context in zip(question_list, answers_list, context_list):
                            st.write("Q: ",question)
                            st.write("A:",answer)
                            st.write("Context:", context)
                            score, success, reason = red_team_obj.deep_evaluate(question,answer,context,objective,EVAL_METRICS)
                            st.write("Evaluation:",f"Score:{score}", f"Success:{success}", f"Reason: {reason}")
        with sub_tab2:
            st.write("Bias Detection Component")
            # Implement bias detection functionalities

        with sub_tab3:
            st.write("Risk Questionnaire Component")
            risk_questionnaire()
except Exception as e:
    print(f'Exception occured on streamlit: {str(e)}')
finally:
    tracemalloc.stop()
