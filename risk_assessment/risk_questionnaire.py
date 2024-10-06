import streamlit as st
import plotly.express as px

# Helper functions
def calculate_weighted_risk_score(answers, weights):
    """
    Calculate the risk score based on the answers provided and the weights.
    """
    score = 0
    for answer, weight in zip(answers, weights):
        if answer == 'No':
            score += weight
    return score

def risk_category(score):
    """
    Categorize the risk level based on the score.
    """
    if score >= 15:
        return "High Risk"
    elif 8 <= score < 15:
        return "Medium Risk"
    else:
        return "Low Risk"
def remediation_strategy(risk_level):
    """
    Return remediation strategies based on the risk level.
    """
    if risk_level == "High Risk":
        return """
        **Remediation for High Risk**:
        1. Immediate audit of data privacy and security policies.
        2. Introduce additional encryption for data at rest and in transit.
        3. Increase bias auditing frequency and review datasets for fairness.
        4. Implement continuous monitoring of AI outputs for harmful decisions.
        """
    elif risk_level == "Medium Risk":
        return """
        **Remediation for Medium Risk**:
        1. Conduct regular reviews of data handling and retention policies.
        2. Strengthen access control to sensitive patient information.
        3. Perform periodic bias detection audits.
        """
    else:
        return "Your system is operating under Low Risk. Continue monitoring and best practices."

def personalized_recommendations(answers):
    """
    Provide personalized remediation recommendations based on the answers.
    """
    recommendations = []
    if answers[0] == 'No':
        recommendations.append("Ensure patient data is anonymized before processing.")
    if len(answers) > 10 and answers[10] == 'No':
        recommendations.append("Improve AI decision transparency for physicians.")
    return recommendations

def display_risk_dashboard(score):
    """
    Display a risk dashboard using Plotly.
    """
    categories = ['Data Privacy', 'Bias and Fairness', 'Transparency', 'Model Accuracy', 'Ethics', 'Regulatory', 'Guardrails']
    values = [10, 7, 5, 9, 8, 4, score]
    fig = px.pie(values=values, names=categories, title="Risk Distribution Across Categories")
    st.plotly_chart(fig)

def risk_questionnaire():
    """
    Display the AI Risk Questionnaire and collect user responses.
    Dynamically adjust based on role and conditional logic.
    """
    st.subheader("AI Risk Questionnaire for Chat with Physician Agent")

    # Role selection
    role = st.selectbox("Select your role", ["IT Personnel", "Compliance Officer", "Medical Professional"], key='role_select')
    # Initialize answers and weights for scoring
    answers = []
    weights = []
    # Common questions (applicable to all roles)
    st.write("### Common Questions")
    privacy_anonymization = st.radio("Is patient data anonymized before processing?", ('Yes', 'No'), key='privacy_anonymization')
    answers.append(privacy_anonymization)
    weights.append(2)
    # Conditional Question for privacy anonymization
    if privacy_anonymization == 'No':
        explore_anonymization = st.radio("Would you like to explore solutions for anonymizing patient data?", ('Yes', 'No'), key='explore_anonymization')
    data_encryption = st.radio("Is patient data securely encrypted during storage and transmission?", ('Yes', 'No'), key='data_encryption')
    answers.append(data_encryption)
    weights.append(2)
    # Conditional Question for data encryption
    if data_encryption == 'No':
        encryption_solution = st.radio("Would you like to explore encryption solutions for patient data?", ('Yes', 'No'), key='encryption_solution')
    access_control = st.radio("Is access to patient data restricted to authorized personnel only?", ('Yes', 'No'), key='access_control')
    answers.append(access_control)
    weights.append(1)
    # Conditional Question for access control
    if access_control == 'No':
        implement_access_control = st.radio("Would you like to implement stricter access control for patient data?", ('Yes', 'No'), key='implement_access_control')
    data_retention = st.radio("Is there a clear data retention and deletion policy for patient records?", ('Yes', 'No'), key='data_retention')
    answers.append(data_retention)
    weights.append(1)
    # Conditional Question for data retention policy
    if data_retention == 'No':
        retention_policy_help = st.radio("Would you like to establish a data retention and deletion policy?", ('Yes', 'No'), key='retention_policy_help')
    # Role-specific questions
    if role == "IT Personnel":
        st.write("### IT-Specific Questions")
        system_audit = st.radio("Are systems regularly audited for vulnerabilities?", ('Yes', 'No'), key='system_audit')
        answers.append(system_audit)
        weights.append(2)
        # Conditional Question for system audits
        if system_audit == 'No':
            audit_schedule = st.radio("Would you like to schedule regular system security audits?", ('Yes', 'No'), key='audit_schedule')
        security_measures = st.radio("Are security measures up-to-date for protecting healthcare data?", ('Yes', 'No'), key='security_measures')
        answers.append(security_measures)
        weights.append(2)
        # Conditional Question for security measures
        if security_measures == 'No':
            implement_security_measures = st.radio("Would you like to implement updated security measures?", ('Yes', 'No'), key='implement_security_measures')
    elif role == "Compliance Officer":
        st.write("### Compliance-Specific Questions")
        hipaa_compliance = st.radio("Is the AI system fully compliant with healthcare regulations such as HIPAA?", ('Yes', 'No'), key='hipaa_compliance')
        answers.append(hipaa_compliance)
        weights.append(3)
        # Conditional Question for HIPAA compliance
        if hipaa_compliance == 'No':
            hipaa_help = st.radio("Would you like to explore solutions for HIPAA compliance?", ('Yes', 'No'), key='hipaa_help')
        regulatory_audits = st.radio("Are regular audits conducted for regulatory compliance?", ('Yes', 'No'), key='regulatory_audits')
        answers.append(regulatory_audits)
        weights.append(2)
        # Conditional Question for regulatory audits
        if regulatory_audits == 'No':
            audit_help = st.radio("Would you like to schedule regular regulatory audits?", ('Yes', 'No'), key='audit_help')
    elif role == "Medical Professional":
        st.write("### Medical Professional Questions")
        decision_explainability = st.radio("Can the AI system’s diagnostic decisions be fully explained to physicians?", ('Yes', 'No'), key='decision_explainability')
        answers.append(decision_explainability)
        weights.append(3)
        # Conditional Question for explainability
        if decision_explainability == 'No':
            explainability_help = st.radio("Would you like to introduce explainability mechanisms?", ('Yes', 'No'), key='explainability_help')
        clinician_feedback = st.radio("Can clinicians provide feedback on the AI's decisions?", ('Yes', 'No'), key='clinician_feedback')
        answers.append(clinician_feedback)
        weights.append(2)
        # Conditional Question for clinician feedback
        if clinician_feedback == 'No':
            feedback_system_help = st.radio("Would you like to implement a feedback system for clinicians?", ('Yes', 'No'), key='feedback_system_help')
        model_accuracy = st.radio("Is the AI model’s diagnostic accuracy regularly evaluated?", ('Yes', 'No'), key='model_accuracy')
        answers.append(model_accuracy)
        weights.append(2)
        # Conditional Question for model accuracy
        if model_accuracy == 'No':
            accuracy_help = st.radio("Would you like to implement regular accuracy evaluations?", ('Yes', 'No'), key='accuracy_help')
    
    # Calculate the risk score
    score = calculate_weighted_risk_score(answers, weights)
    risk_level = risk_category(score)

    # Display the results
    st.write(f"### Your Risk Score: {score}")
    st.write(f"### Risk Level: {risk_level}")

    # Display remediation strategies based on risk level
    if risk_level in ["High Risk", "Medium Risk"]:
        st.write(remediation_strategy(risk_level))
    
    # Display personalized recommendations
    recommendations = personalized_recommendations(answers)
    if recommendations:
        st.write("### Personalized Recommendations")
        for recommendation in recommendations:
            st.write(f"- {recommendation}")
            
    # Display risk dashboard
    st.write("### Risk Dashboard")
    display_risk_dashboard(score)

    # Show success message after submission
    if st.button("Submit Questionnaire"):
        st.success(f"Risk Assessment Completed! You are in the {risk_level} category.")