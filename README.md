## General Physician Chatbot Application

### Introduction
Welcome to our General Physician Chatbot Application! This application is designed to provide users with a conversational interface to query symptoms or patient history and receive responses based on the retrieved context. Additionally, we have incorporated some trustworthy AI components to ensure the accuracy and reliability of the responses.

### Getting Started
To run the application, follow these steps:

- Clone the repository from GitHub: 
```sh
git clone https://github.com/charutapaliwal/Healthcare_PoC.git
```
- Create a virtual environment: 
``` sh 
python -m venv env
```
- Install dependencies using pip: 
```sh 
pip install -r requirements.txt
```
- Install additional dependencies:
```sh
pip install llm-guard
```
- If you encounter error in above installation, execute following:
```sh
pip install wheel
pip install torch
pip install llm-guard --no-build-isolation
```
- Run the application: 
```sh
streamlit run app.py
```

### Components
Our chatbot application consists of the following components:

- RAG (Rule-Based, Artificial Intelligence, and Graph-based) Approach: Our chatbot uses a combination of rule-based, artificial intelligence, and graph-based approaches to retrieve and respond to user queries.
- Trustworthy AI Components:
    - Red Teaming with Results: Our application includes a red teaming feature that simulates potential attacks on the AI model and provides results to ensure the accuracy and reliability of the responses.
    - Data Bias Detection: We have incorporated a data bias detection feature to identify and mitigate potential biases in the data used to train the AI model.
    - Risk Questionnaire: Our application includes a risk questionnaire that helps users assess the potential risks associated with their symptoms or patient history.

### Technical Requirements
- Python 3.8 or higher
- Streamlit 1.10.0 or higher
- Wheel 0.37.0 or higher
- Torch 1.10.0 or higher
- LLM-Guard 0.1.0 or higher

### Troubleshooting
If you encounter any issues while running the application, please refer to the following troubleshooting steps:

- Check that you have installed all the required dependencies.
- Verify that you have created a virtual environment and activated it.
- Check the application logs for any errors or warnings.

### Contributing
We welcome contributions to our chatbot application! If you would like to contribute, please fork the repository and submit a pull request with your changes.

We hope you find our chatbot application helpful! If you have any questions or feedback, please don't hesitate to reach out to us.