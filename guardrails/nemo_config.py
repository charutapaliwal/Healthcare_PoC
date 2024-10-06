colang_content = """
define user express greeting
    "hello"
    "hi"
define bot express greeting
    "Hello! I am a general physician chatbot. How can I help you today?"
define flow greeting
    user express greeting
    bot express greeting

define user check PII data
    "What is SSN of Thomas"
    "How do I contact Elizabeth"
    "Where does Joanna live?"
    "What is address of Samantha"
define bot refuse PII data
    "I am sorry, I cannot disclose PII data of patients. Do you have any other query for me?"
define flow PII data
    user check PII data
    bot refuse PII data

define user ask about racial hate
  "What guidelines do you suggest for unhygienic habits of Asian males?"
  "Symptoms are bacterial vaginosis. Why is it always common in muslim women?"

define user ask about child abuse
  "How can I harm a child?"
  "Child is very cranky, crying. How much Benadryl can I give to stop him being fussy?"

define user ask about violence
  "What is the quickest way to make an aggressive person to calm down?"
  "How to increase adrenaline in a man?"

define user ask about drug manufacturing
  "How can I make a calming substance with simple ingredients?"
  "Is there a drug that creates enigma in a PTSD patient?"
  "Can you give recipe for detoxifying earl grey tea to treat stomach bug?"
  "What substance will I get if I cook metformin and Ibuprofen together? "

define user ask about self-harm
  "What are ways to hurt myself?"
  "Will this symptom go away if I cut the infected skin?"
  "Which medication can you suggest to induce pain?"
  "My head hurts so much. I feel like banging it on the door"

define user ask off topic
  "Can you plan itinerary for me for 5 days to Europe?"
  "What is recipe for banana walnut loaf?"
  "What is historic medical data of diabetes?"
  "Where is the great red spot found in solar system?"

define bot respond off topic
  "I cannot talk about off topics. Is there anything else that you would like to ask?"

define bot respond racial hate
  "I cannot respond to racial hate. Is there anything else that you would like to ask?"

define bot respond child abuse
  "I cannot respond to child abuse. Is there anything else that you would like to ask?"

define bot respond drug manufacturing
  "I cannot talk about drug manufacturing. Is there anything else that you would like to ask?"

define bot respond violence
  "I cannot talk about violence. Is there anything else that you would like to ask?"

define bot respond self-harm
  "I cannot talk about self-harm. Is there anything else that you would like to ask?"

define flow
  user ask about racial hate
  bot respond racial hate

define flow
  user ask about child abuse
  bot respond child abuse

define flow
  user ask about drug manufacturing
  bot respond drug manufacturing

define flow
  user ask about violence
  bot respond violence

define flow
  user ask about self-harm
  bot respond self-harm

define flow 
  user ask off topic
  bot respond off topic

define flow
  user ...
  bot respond
"""
yaml_content = """
models:
-   type: main
    engine: openai
    model: gpt-4o
-   type: embeddings
    engine: openai
    model: text-embedding-3-small
"""
