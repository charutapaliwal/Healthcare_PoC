from fairlearn.metrics import MetricFrame, selection_rate, demographic_parity_difference
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

# Assume the model is pre-trained (or load a pre-trained model)
model = RandomForestClassifier()

def detect_model_bias(X, y_true, sensitive_feature):
    """
    Detects model bias using Fairlearn.

    Parameters:
    X (pd.DataFrame): Feature data
    y_true (pd.Series): True labels
    sensitive_feature (str): Column name of the sensitive feature (e.g., 'Gender')

    Returns:
    MetricFrame: Bias detection results
    """
    # Generate predictions
    model.fit(X,y_true)
    y_pred = model.predict(X)

    # Create a MetricFrame to analyze bias
    metric_frame = MetricFrame(metrics=accuracy_score, 
                               y_true=y_true, 
                               y_pred=y_pred, 
                               sensitive_features=X[sensitive_feature])

    # Calculate demographic parity difference
    dpd = demographic_parity_difference(y_true, y_pred, sensitive_features=X[sensitive_feature])

    return metric_frame, dpd

if __name__ == "__main__":
    # Example usage for testing (replace with actual data)
    data = {
        'Age': [34, 45, 23, 45],
        'Gender': [0,1,1,1],
        'Symptoms_Length': [3, 4, 2, 5],
        'Lab_Results': [78, 65, 88, 90]
    }
    df = pd.DataFrame(data)
    y_true = pd.Series([0, 1, 1, 0])  # Replace with true labels

    metrics, dpd = detect_model_bias(df, y_true, 'Gender')
    print("MetricFrame results:", metrics)
    print("Demographic Parity Difference:", dpd)
