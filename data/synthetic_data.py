import pandas as pd
from faker import Faker
import yaml

def generate_synthetic_data(num_records=100):
    fake = Faker()
    data = []

    icd10_codes = {
        'A00-B99': (
            ['Infectious and parasitic diseases', 'Fever, chills, and flank pain', 'Urinary Tract Infection', 'Ciprofloxacin', '120/80', 25],
            ['Infectious and parasitic diseases', 'Cough, fever, and difficulty breathing', 'Pneumonia', 'Azithromycin', '130/90', 28],
            ['Infectious and parasitic diseases', 'Diarrhea, vomiting, and abdominal cramps', 'Gastroenteritis', 'None', '110/70', 22]
        ),
        'C00-D49': (
            ['Neoplasms', 'Lump in the breast, nipple discharge, and breast pain', 'Breast Cancer', 'Tamoxifen', '140/95', 30],
            ['Neoplasms', 'Coughing up blood, chest pain, and difficulty breathing', 'Lung Cancer', 'Chemotherapy', '150/100', 32],
            ['Neoplasms', 'New or changing moles, skin lesions, and itching', 'Skin Cancer', 'Surgery', '120/80', 25]
        ),
        'D50-D89': (
            ['Diseases of the blood and blood-forming organs', 'Fatigue, weakness, and pale skin', 'Anemia', 'Ferrous Sulfate', '110/70', 20],
            ['Diseases of the blood and blood-forming organs', 'Fever, fatigue, and weight loss', 'Leukemia', 'Chemotherapy', '130/90', 28],
            ['Diseases of the blood and blood-forming organs', 'Fatigue, weakness, and pale skin', 'Thalassemia', 'Blood Transfusions', '120/80', 22]
        ),
        'E00-E89': (
            ['Endocrine, nutritional and metabolic diseases', 'Increased thirst and urination, fatigue, and blurred vision', 'Diabetes', 'Metformin', '140/95', 30],
            ['Endocrine, nutritional and metabolic diseases', 'Fatigue, weight gain, and dry skin', 'Hypothyroidism', 'Levothyroxine', '120/80', 25],
            ['Endocrine, nutritional and metabolic diseases', 'Weight loss, rapid heartbeat, and nervousness', 'Hyperthyroidism', 'Methimazole', '130/90', 28]
        ),
        'F00-F99': (
            ['Mental and behavioral disorders', 'Feeling anxious or fearful, rapid heartbeat, and sweating', 'Anxiety', 'Xanax', '120/80', 22],
            ['Mental and behavioral disorders', 'Feeling sad or empty, loss of interest in activities, and changes in appetite', 'Depression', 'Fluoxetine', '110/70', 20],
            ['Mental and behavioral disorders', 'Flashbacks, nightmares, and avoidance of triggers', 'PTSD', 'Sertraline', '130/90', 28]
        ),
        'G00-G99': (
            ['Diseases of the nervous system', 'Severe headache, sensitivity to light and sound, and nausea', 'Migraine', 'Sumatriptan', '140/95', 30],
            ['Diseases of the nervous system', 'Seizures, confusion, and loss of consciousness', 'Epilepsy', 'Phenytoin', '130/90', 28],
            ['Diseases of the nervous system', 'Tremors, stiffness, and difficulty with movement', 'Parkinson\'s Disease', 'Levodopa', '120/80', 25]
        ),
        'H00-H59': (
            ['Diseases of the eye and adnexa', 'Blurred vision, eye pain, and sensitivity to light', 'Glaucoma', 'Timolol', '120/80', 22],
            ['Diseases of the eye and adnexa', 'Cloudy vision, double vision, and eye pain', 'Cataracts', 'Surgery', '110/70', 20],
            ['Diseases of the eye and adnexa', 'Blurred vision, blind spots, and distorted vision', 'Macular Degeneration', 'None', '130/90', 28]
        ),
        'H60-H95': (
            ['Diseases of the ear and mastoid process', 'Ear pain, fever, and difficulty hearing', 'Ear Infection', 'Amoxicillin', '120/80', 22],
            ['Diseases of the ear and mastoid process', 'Ringing in the ears, hearing loss, and ear fullness', 'Hearing Loss', 'Hearing Aids', '110/70', 20],
            ['Diseases of the ear and mastoid process', 'Dizziness, nausea, and vomiting', 'Vertigo', 'Meclizine', '130/90', 28]
        ),
        'I00-I99': (
            ['Diseases of the circulatory system', 'High blood pressure, chest pain, and shortness of breath', 'Hypertension', 'Lisinopril', '150/100', 32],
            ['Diseases of the circulatory system', 'Shortness of breath, fatigue, and swelling in the legs', 'Heart Failure', 'Furosemide', '140/95', 30],
            ['Diseases of the circulatory system', 'Irregular heartbeat, palpitations, and shortness of breath', 'Atrial Fibrillation', 'Warfarin', '130/90', 28]
        ),
        'J00-J99': (
            ['Diseases of the respiratory system', 'Wheezing, coughing, and shortness of breath', 'Asthma', 'Albuterol', '120/80', 22],
            ['Diseases of the respiratory system', 'Shortness of breath, wheezing, and coughing', 'Chronic Obstructive Pulmonary Disease', 'Salmeterol', '130/90', 28],
            ['Diseases of the respiratory system', 'Coughing, fever, and difficulty breathing', 'Pneumonia', 'Azithromycin', '140/95', 30]
        ),
        'K00-K93': (
            ['Diseases of the digestive system', 'Heartburn, regurgitation, and difficulty swallowing', 'Gastroesophageal Reflux Disease', 'Omeprazole', '120/80', 25],
            ['Diseases of the digestive system', 'Abdominal pain, bloating, and changes in bowel movements', 'Irritable Bowel Syndrome', 'None', '110/70', 22],
            ['Diseases of the digestive system', 'Diarrhea, abdominal pain, and weight loss', 'Inflammatory Bowel Disease', 'Prednisone', '130/90', 28]
        ),
        'L00-L99': (
            ['Diseases of the skin and subcutaneous tissue', 'Acne, blackheads, and oily skin', 'Acne', 'Benzoyl Peroxide', '120/80', 22],
            ['Diseases of the skin and subcutaneous tissue', 'Red, scaly patches, and itching', 'Psoriasis', 'Methotrexate', '130/90', 28],
            ['Diseases of the skin and subcutaneous tissue', 'Dry, itchy skin, and small bumps', 'Eczema', 'Hydrocortisone', '110/70', 20]
        ),
        'M00-M99': (
            ['Diseases of the musculoskeletal system and connective tissue', 'Joint pain, stiffness, and limited mobility', 'Osteoarthritis', 'Ibuprofen', '120/80', 25],
            ['Diseases of the musculoskeletal system and connective tissue', 'Joint pain, swelling, and stiffness', 'Rheumatoid Arthritis', 'Methotrexate', '130/90', 28],
            ['Diseases of the musculoskeletal system and connective tissue', 'Widespread muscle pain, fatigue, and tender points', 'Fibromyalgia', 'Pregabalin', '110/70', 22]
        ),
        'N00-N99': (
            ['Diseases of the genitourinary system', 'Severe pain, nausea, and vomiting', 'Kidney Stones', 'Pain Relievers', '140/95', 30],
            ['Diseases of the genitourinary system', 'Painful urination, frequent urination, and abdominal pain', 'Urinary Tract Infection', 'Ciprofloxacin', '130/90', 28],
            ['Diseases of the genitourinary system', 'Difficulty starting urination, weak urine flow, and frequent urination', 'Prostate Cancer', 'Surgery', '120/80', 25]
        ),
        'O00-O99': (
            ['Pregnancy, childbirth and the puerperium', 'Morning sickness, fatigue, and mood swings', 'Pregnancy', 'Folic Acid', '110/70', 20],
            ['Pregnancy, childbirth and the puerperium', 'Labor pain, contractions, and vaginal discharge', 'Childbirth', 'None', '120/80', 22],
            ['Pregnancy, childbirth and the puerperium', 'Feeling sad, empty, and hopeless', 'Postpartum Depression', 'Fluoxetine', '130/90', 28]
        ),
        'P00-P96': (
            ['Certain conditions originating in the perinatal period', 'Premature birth, low birth weight, and respiratory distress', 'Premature Birth', 'Oxygen Therapy', '110/70', 20],
            ['Certain conditions originating in the perinatal period', 'Low birth weight, small size, and developmental delays', 'Low Birth Weight', 'Nutritional Support', '120/80', 22],
            ['Certain conditions originating in the perinatal period', 'Lack of oxygen, brain damage, and developmental delays', 'Birth Asphyxia', 'Ventilatory Support', '130/90', 28]
        ),
        'Q00-Q99': (
            ['Congenital malformations, deformations and chromosomal abnormalities', 'Cleft lip, cleft palate, and difficulty feeding', 'Cleft Palate', 'Surgery', '120/80', 25],
            ['Congenital malformations, deformations and chromosomal abnormalities', 'Intellectual disability, delayed development, and physical characteristics', 'Down Syndrome', 'None', '110/70', 20],
            ['Congenital malformations, deformations and chromosomal abnormalities', 'Spinal cord damage, paralysis, and bowel and bladder problems', 'Spina Bifida', 'Surgery', '130/90', 28]
        ),
        'R00-R99': (
            ['Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified', 'Headache, fatigue, and sensitivity to light', 'Headache', 'Acetaminophen', '120/80', 22],
            ['Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified', 'Feeling tired, weak, and lacking energy', 'Fatigue', 'None', '110/70', 20],
            ['Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified', 'Feeling lightheaded, dizzy, and disoriented', 'Dizziness', 'Meclizine', '130/90', 28]
        ),
        'S00-T88': (
            ['Injury, poisoning and certain other consequences of external causes', 'Pain, swelling, and limited mobility', 'Broken Bone', 'Pain Relievers', '140/95', 30],
            ['Injury, poisoning and certain other consequences of external causes', 'Burns, blisters, and scarring', 'Burns', 'Silver Sulfadiazine', '130/90', 28],
            ['Injury, poisoning and certain other consequences of external causes', 'Nausea, vomiting, and abdominal pain', 'Poisoning', 'Activated Charcoal', '120/80', 25]
        ),
        'V00-Y99': (
            ['External causes of morbidity', 'Pain, swelling, and limited mobility', 'Car Accident', 'Physical Therapy', '140/95', 30],
            ['External causes of morbidity', 'Pain, swelling, and limited mobility', 'Fall', 'Pain Relievers', '130/90', 28],
            ['External causes of morbidity', 'Pain, swelling, and limited mobility', 'Sports Injury', 'Ice', '120/80', 25]
        ),
        'Z00-Z99': (
            ['Factors influencing health status and contact with health services', 'None', 'Wellness Check', 'None', '110/70', 20],
            ['Factors influencing health status and contact with health services', 'None', 'Vaccination', 'Vaccine', '120/80', 22],
            ['Factors influencing health status and contact with health services', 'None', 'Screening', 'None', '130/90', 28]
        )
    }
    # with open('icd10_codes.yaml','r')as file:
    #     icd10_codes = yaml.safe_load(file)
    for _ in range(num_records):
        code = fake.random_element(elements=list(icd10_codes.keys()))
        description, symptoms,diagnosis, medication, blood_pressure, BMI = fake.random_element(elements=icd10_codes[code])
        record = {
            'Patient_ID': fake.uuid4(),
            'Name' : fake.name(),
            'Age': fake.random_int(min=18, max=85),
            'Gender': fake.random_element(elements=('Male', 'Female')),
            'Address':fake.address(),
            'SSN': fake.ssn(),
            'ICD10_Code': code,
            'Code_Description':description,
            'Previous_Symptoms': symptoms,
            'Previous_Diagnosis': diagnosis,
            'Current_Medication': medication,
            'Blood_Pressure': blood_pressure,
            'Body_Mass_Index': BMI
       }
        data.append(record)

    df = pd.DataFrame(data)
    df.set_index('Patient_ID', inplace=True)
    df.to_csv('Synthetic_Data.csv')
    return df

if __name__ == "__main__":
    # For testing and standalone execution
    df = generate_synthetic_data()
    print(df.head())