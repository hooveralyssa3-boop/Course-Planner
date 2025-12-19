import json
import re
import os
import hashlib

# --- Configuration ---
ROOT_DIR = "/Users/alyssahoover"
OUTPUT_PATH = os.path.join(ROOT_DIR, "course-planner/src/data.json")

# --- Manual Notebook Mapping (Gold Standard) ---
# Format: (Class, Chapter String, Page String, Title String)
NOTEBOOK_DATA = [
    # --- Basic Adult Healthcare ---
    ("Basic Adult Healthcare", "Ch 1", "p. 3", "Student Tips for Success (Nursing Process)"),
    ("Basic Adult Healthcare", "Ch 1", "p. 4", "Strategies for Prioritization Power"),
    ("Basic Adult Healthcare", "Ch 3", "p. 99", "Health Promotion"),
    ("Basic Adult Healthcare", "Ch 4", "p. 81–85", "Client Preference and Profile; Culture; Diversity"),
    ("Basic Adult Healthcare", "Ch 5", "p. 11, 215", "Adaptation: Stress & Coping; Protection: Inflammation"),
    ("Basic Adult Healthcare", "Ch 8", "p. 25, 107", "Elder Abuse; Dementia and Alzheimer’s"),
    ("Basic Adult Healthcare", "Ch 9", "p. 111–115", "Comfort: Pain; Acute Pain; Chronic Pain"),
    ("Basic Adult Healthcare", "Ch 10", "p. 141–163", "Homeostasis; Hypo/Hyperkalemia; Dehydration"),
    ("Basic Adult Healthcare", "Ch 11", "p. 49", "Circulation: Perfusion (Shock Concepts)"),
    ("Basic Adult Healthcare", "Ch 14-16", "p. 439", "Safety: Postoperative"),
    ("Basic Adult Healthcare", "Ch 18", "p. 251", "Epistaxis"),
    ("Basic Adult Healthcare", "Ch 19", "p. 259", "Pneumonia"),
    ("Basic Adult Healthcare", "Ch 20", "p. 371–373", "Asthma; Chronic Obstructive Pulmonary Disease"),
    ("Basic Adult Healthcare", "Ch 23", "p. 59, 69", "Acute Coronary Syndrome; Myocardial Infarction"),
    ("Basic Adult Healthcare", "Ch 25", "p. 65", "Heart Failure"),
    ("Basic Adult Healthcare", "Ch 26", "p. 57, 73", "Pulmonary Embolism; Deep Vein Thrombosis"),
    ("Basic Adult Healthcare", "Ch 27", "p. 67", "Hypertension"),
    ("Basic Adult Healthcare", "Ch 28", "p. 421", "Safety: Blood Administration"),
    ("Basic Adult Healthcare", "Ch 29", "p. 271–275", "Iron Deficiency Anemia; Sickle Cell Anemia"),
    ("Basic Adult Healthcare", "Ch 32", "p. 219", "Human Immunodeficiency Virus"),
    ("Basic Adult Healthcare", "Ch 34", "p. 225, 227", "Systemic Lupus Erythematosus; Rheumatoid Arthritis"),
    ("Basic Adult Healthcare", "Ch 36", "p. 173, 175", "Osteoarthritis; Hip/Knee Arthroplasty"),
    ("Basic Adult Healthcare", "Ch 37", "p. 171", "Fractures"),
    ("Basic Adult Healthcare", "Ch 40", "p. 359", "Peptic Ulcer Disease"),
    ("Basic Adult Healthcare", "Ch 41", "p. 325, 331", "Intestinal Obstruction; Inflammatory Bowel Disease"),
    ("Basic Adult Healthcare", "Ch 43", "p. 363, 365", "Cirrhosis; Hepatitis"),
    ("Basic Adult Healthcare", "Ch 44", "p. 221", "Pancreatitis"),
    ("Basic Adult Healthcare", "Ch 45", "p. 317–319", "Addison’s; Cushing’s; Hyper/Hypothyroidism"),
    ("Basic Adult Healthcare", "Ch 45", "p. 347, 349", "Diabetes Insipidus; SIADH"),
    ("Basic Adult Healthcare", "Ch 46", "p. 335–337", "Diabetes Mellitus (Insulin vs Non-Insulin)"),
    ("Basic Adult Healthcare", "Ch 48", "p. 309, 311", "Acute Kidney Injury; Chronic Kidney Disease"),
    ("Basic Adult Healthcare", "Ch 49", "p. 307", "Urinary Tract Infection"),
    ("Basic Adult Healthcare", "Ch 51", "p. 113", "Acute Pain (Relevant to Hysterectomy Scenario)"),
    ("Basic Adult Healthcare", "Ch 53", "p. 297, 299", "Benign Prostatic Hyperplasia; Prostate Cancer"),
    ("Basic Adult Healthcare", "Ch 58", "p. 387, 389", "Glaucoma; Cataracts"),
    ("Basic Adult Healthcare", "Ch 61", "p. 303", "Increased Intracranial Pressure"),
    ("Basic Adult Healthcare", "Ch 62", "p. 53–55", "Embolic Stroke; Hemorrhagic Stroke"),
    ("Basic Adult Healthcare", "Ch 65", "p. 191", "Parkinson’s Disease"),
    ("Basic Adult Healthcare", "Ch 67", "p. 431, 23", "Emergency Triage; Bites and Astings"),

    # --- Pharmacology ---
    ("Pharmacology", "Ch 4", "p. 437", "Safety: Medication Administration"),
    ("Pharmacology", "Ch 5", "p. 3", "Student Tips for Success (Math Prep)"),
    ("Pharmacology", "Ch 9", "p. 231", "Methicillin-Resistant Staphylococcus aureus (MRSA)"),
    ("Pharmacology", "Ch 9", "p. 233", "Vancomycin-Resistant Enterococci (VRE)"),
    ("Pharmacology", "Ch 15", "p. 215", "Concept: Protection – Immunity, Inflammation, Infection"),
    ("Pharmacology", "Ch 16", "p. 319", "Cushing’s Syndrome (Steroid Excess/Management)"),
    ("Pharmacology", "Ch 18", "p. 99", "Health Promotion: Immunizations"),
    ("Pharmacology", "Ch 21", "p. 135", "Depression"),
    ("Pharmacology", "Ch 23", "p. 195", "Seizures"),
    ("Pharmacology", "Ch 24", "p. 191", "Parkinson’s Disease"),
    ("Pharmacology", "Ch 26", "p. 111", "Concept: Comfort – Pain, Tissue Integrity"),
    ("Pharmacology", "Ch 26", "p. 113", "Acute Pain"),
    ("Pharmacology", "Ch 35", "p. 347", "Diabetes Insipidus"),
    ("Pharmacology", "Ch 35", "p. 349", "Syndrome of Inappropriate Antidiuretic Hormone"),
    ("Pharmacology", "Ch 36", "p. 317", "Addison’s Syndrome/Disease"),
    ("Pharmacology", "Ch 36", "p. 319", "Cushing’s Syndrome/Disease"),
    ("Pharmacology", "Ch 37", "p. 351", "Hyperthyroidism"),
    ("Pharmacology", "Ch 37", "p. 353", "Hypothyroidism"),
    ("Pharmacology", "Ch 37", "p. 343", "Hyperparathyroidism"),
    ("Pharmacology", "Ch 38", "p. 335", "Diabetes Mellitus—Insulin Dependent"),
    ("Pharmacology", "Ch 38", "p. 337", "Diabetes Mellitus—Non-Insulin Dependent"),
    ("Pharmacology", "Ch 43", "p. 67", "Hypertension"),
    ("Pharmacology", "Ch 44", "p. 65", "Heart Failure"),
    ("Pharmacology", "Ch 44", "p. 66", "NurseThink® Quick: Digoxin Toxicity"),
    ("Pharmacology", "Ch 46", "p. 59", "Acute Coronary Syndrome"),
    ("Pharmacology", "Ch 46", "p. 61", "Atherosclerosis"),
    ("Pharmacology", "Ch 48", "p. 51", "Coagulation Disorders"),
    ("Pharmacology", "Ch 48", "p. 73", "Deep Vein Thrombosis"),
    ("Pharmacology", "Ch 49", "p. 271", "Iron Deficiency Anemia"),
    ("Pharmacology", "Ch 51", "p. 163", "Fluid Overload (Diuretic Management)"),
    ("Pharmacology", "Ch 52", "p. 447", "Safety: Urinary Catheter"),
    ("Pharmacology", "Ch 55", "p. 371", "Asthma"),
    ("Pharmacology", "Ch 55", "p. 373", "Chronic Obstructive Pulmonary Disease"),
    ("Pharmacology", "Ch 57", "p. 359", "Peptic Ulcer"),
    ("Pharmacology", "Ch 58", "p. 321, 323", "Care for elimination abnormalities and colostomy/ileostomy procedures.")
]

# --- Manual CCC Mapping (Gold Standard) ---
# Format: (Class, Textbook Chapter, CCC Section Title, NoteBook Page #, Brief Topic Summary)
CCC_DATA = [
    # --- Basic Adult Healthcare ---
    ("Basic Adult Healthcare", "Ch 1", "Ch. 01: The NurseThink® Way", "p. 3", "Focuses on critical thinking, the nursing process, and best practice study strategies."),
    ("Basic Adult Healthcare", "Ch 3", "Ch. 04: Unfolding Concepts II", "p. 99", "Strategies for lifestyle choices, risk reduction, and client education."),
    ("Basic Adult Healthcare", "Ch 4", "Ch. 02: Next Gen Clinical Judgment", "p. 81, 83, 85", "Covers cultural, spiritual, and developmental assessments."),
    ("Basic Adult Healthcare", "Ch 5", "Ch. 15: Adaptation", "p. 11, 215", "Addresses stress, coping mechanisms, and physiological immunity/inflammation."),
    ("Basic Adult Healthcare", "Ch 8", "Ch. 17: Cognition", "p. 25, 107", "Management of elder abuse, dementia, and Alzheimer’s disease."),
    ("Basic Adult Healthcare", "Ch 9", "Ch. 14: Comfort", "p. 111–115", "Priorities for acute and chronic pain management."),
    ("Basic Adult Healthcare", "Ch 10", "Ch. 08: Homeostasis", "p. 141–163", "Regulation of acid-base balance, electrolytes, and fluid volume."),
    ("Basic Adult Healthcare", "Ch 11", "Ch. 06: Circulation", "p. 75–81", "Priorities for cardiogenic, hypovolemic, and septic shock."),
    ("Basic Adult Healthcare", "Ch 17-20", "Ch. 09: Respiration", "p. 259, 371–373", "Care for pneumonia, asthma, and chronic obstructive pulmonary disease."),
    ("Basic Adult Healthcare", "Ch 21-25", "Ch. 06: Circulation", "p. 59, 65, 69", "Management of ACS, heart failure, and myocardial infarction."),
    ("Basic Adult Healthcare", "Ch 27", "Ch. 06: Circulation", "p. 67", "Monitoring for complications like stroke or heart failure."),
    ("Basic Adult Healthcare", "Ch 28", "Ch. 02: Next Gen Clinical Judgment", "p. 421", "Focuses on safe blood administration, pre-transfusion assessments, and monitoring for transfusion reactions."),
    ("Basic Adult Healthcare", "Ch 29", "Ch. 07: Protection", "p. 271, 275", "Management of iron deficiency and sickle cell crisis, focusing on perfusion and pain management."),
    ("Basic Adult Healthcare", "Ch 30", "Ch. 07: Protection", "p. 291, 297", "Nursing care for leukemia and multiple myeloma, specifically addressing infection prevention and bone pain."),
    ("Basic Adult Healthcare", "Ch 32", "Ch. 07: Protection", "p. 239", "Clinical mapping for HIV/AIDS, focusing on immune system collapse and opportunistic infections."),
    ("Basic Adult Healthcare", "Ch 33", "Ch. 07: Protection", "p. 235", "Recognition and emergency management of hypersensitivity reactions and anaphylaxis."),
    ("Basic Adult Healthcare", "Ch 34", "Ch. 15: Adaptation", "p. 241, 243", "Management of chronic autoimmune conditions like Lupus (SLE) and Rheumatoid Arthritis."),
    ("Basic Adult Healthcare", "Ch 36", "Ch. 13: Movement", "p. 173, 175", "Care for mobility issues related to osteoarthritis and osteoporosis."),
    ("Basic Adult Healthcare", "Ch 37", "Ch. 13: Movement", "p. 171", "Priorities for fracture management, including immobilization and neurovascular checks."),
    ("Basic Adult Healthcare", "Ch 40", "Ch. 11: Nutrition", "p. 359", "Priorities for Peptic Ulcer Disease, including H. pylori management and GI bleeding risks."),
    ("Basic Adult Healthcare", "Ch 41", "Ch. 11: Nutrition", "p. 321, 325", "Management of Crohn’s disease and intestinal obstructions."),
    ("Basic Adult Healthcare", "Ch 43", "Ch. 11: Nutrition", "p. 311, 313", "Clinical judgment for liver cirrhosis and the various types of viral hepatitis."),
    ("Basic Adult Healthcare", "Ch 45", "Ch. 12: Hormonal", "p. 317, 351", "Assessment of thyroid and adrenal gland dysfunctions (Addison's, Hyperthyroidism)."),
    ("Basic Adult Healthcare", "Ch 46", "Ch. 10: Regulation", "p. 335–341", "Comprehensive care for Type 1 and Type 2 diabetes, DKA, and HHNS."),
    ("Basic Adult Healthcare", "Ch 48", "Ch. 10: Regulation", "p. 361, 365", "Priorities for Acute Kidney Injury (AKI) and Chronic Kidney Disease (CKD)."),
    ("Basic Adult Healthcare", "Ch 58", "Ch. 13: Movement", "p. 201, 205", "Clinical judgment for cataracts and glaucoma, focusing on safety and sensory perception."),
    ("Basic Adult Healthcare", "Ch 61", "Ch. 17: Cognition", "p. 195, 303", "Care for patients with seizures and increased intracranial pressure."),
    ("Basic Adult Healthcare", "Ch 62", "Ch. 06: Circulation", "p. 53, 55", "Differentiating between ischemic (embolic) and hemorrhagic stroke interventions."),
    ("Basic Adult Healthcare", "Ch 65", "Ch. 13: Movement", "p. 191", "Nursing priorities for Parkinson’s disease, addressing mobility and safety."),
    ("Basic Adult Healthcare", "Ch 66", "Ch. 07: Protection", "p. 225, 261", "Focuses on influenza and tuberculosis transmission prevention and treatment."),
    ("Basic Adult Healthcare", "Ch 67", "Ch. 18: Multi-Concept", "p. 431", "Triage and injury prevention for trauma, bites, and environmental emergencies."),
    
    # --- Pharmacology ---
    ("Pharmacology", "Ch 4", "Ch. 02: Next Gen Clinical Judgment", "p. 437", "Guidelines for safe medication administration, rights of nursing, and error prevention."),
    ("Pharmacology", "Ch 5", "Ch. 02: Next Gen Clinical Judgment", "p. 3", "Success tips for mastering math conversions and clinical dosage logic."),
    ("Pharmacology", "Ch 9", "Ch. 07: Protection", "p. 231, 233", "Priorities for resistant infections like MRSA and VRE, focusing on infection control."),
    ("Pharmacology", "Ch 15", "Ch. 07: Protection", "p. 215", "Concept overview of immunity, inflammatory triggers, and protection nursing cues."),
    ("Pharmacology", "Ch 16", "Ch. 12: Hormonal", "p. 319", "Management of steroid therapy and monitoring for Cushing-like side effects."),
    ("Pharmacology", "Ch 18", "Ch. 04: Unfolding Concepts II", "p. 99", "Health promotion through immunizations and primary prevention strategies."),
    ("Pharmacology", "Ch 21", "Ch. 16: Emotion", "p. 135", "Assessing therapeutic effects and safety risks in patients with clinical depression."),
    ("Pharmacology", "Ch 23", "Ch. 13: Movement", "p. 195", "Monitoring seizure activity, types of seizures (tonic-clonic/absence), and safety cues."),
    ("Pharmacology", "Ch 24", "Ch. 13: Movement", "p. 191", "Focus on akinesis, rigidity, and the 'Ali Loves Boxing Matches' med mnemonic."),
    ("Pharmacology", "Ch 26", "Ch. 14: Comfort", "p. 111, 113", "Priorities for comfort and acute pain management, including respiratory monitoring."),
    ("Pharmacology", "Ch 35", "Ch. 12: Hormonal", "p. 347, 349", "Managing antidiuretic hormone imbalances and associated fluid volume cues."),
    ("Pharmacology", "Ch 36", "Ch. 12: Hormonal", "p. 317, 319", "Nursing care for cortisol imbalances (Addison's vs. Cushing's Syndrome)."),
    ("Pharmacology", "Ch 37", "Ch. 12: Hormonal", "p. 343, 351", "Assessing metabolic regulation, tremors, and temperature intolerance."),
    ("Pharmacology", "Ch 38", "Ch. 10: Regulation", "p. 335, 337", "Focus on the '3 P's' (polyuria, polydipsia, polyphagia) and hypoglycemia risks."),
    ("Pharmacology", "Ch 43", "Ch. 06: Circulation", "p. 67, 70", "Managing hypertension with the 'ABCD' treatment logic and monitoring for TIA."),
    ("Pharmacology", "Ch 44", "Ch. 06: Circulation", "p. 65, 68", "Managing HF using 'UNLOAD FAST' and monitoring for Digoxin toxicity (VANBAD)."),
    ("Pharmacology", "Ch 46", "Ch. 06: Circulation", "p. 59, 61", "Using 'MONAH' for acute coronary syndrome and managing atherosclerosis."),
    ("Pharmacology", "Ch 48", "Ch. 06: Circulation", "p. 51, 73", "Focus on DIC, DVT prevention, and pulmonary embolism (PE) risk factors."),
    ("Pharmacology", "Ch 49", "Ch. 07: Protection", "p. 271", "Priorities for iron deficiency and sickle cell anemia management."),
    ("Pharmacology", "Ch 51", "Ch. 08: Homeostasis", "p. 163", "Assessing fluid overload, edema, and effectiveness of loop vs. thiazide diuretics."),
    ("Pharmacology", "Ch 55", "Ch. 09: Respiration", "p. 371, 373", "Use of adrenergics and steroids to manage pink puffers (emphysema) vs. blue bloaters."),
    ("Pharmacology", "Ch 57", "Ch. 11: Nutrition", "p. 359", "Treatment for Peptic Ulcer Disease and H. pylori ('Please Make Tummy Better')."),
    ("Pharmacology", "Ch 58", "p. 321, 323", "Care for elimination abnormalities and colostomy/ileostomy procedures.")
]

# --- Manual CJ Sim Mapping (Gold Standard) ---
# Format: (Class, Textbook Chapter, Patient Name, Patient Summary)
CJ_SIM_DATA = [
    # --- Basic Adult Healthcare ---
    ("Basic Adult Healthcare", "Ch. 10", "Simon Andrews", "68-year-old male presenting with signs of severe dehydration, including poor skin turgor and dark urine."),
    ("Basic Adult Healthcare", "Ch. 11", "Ashley Johnson", "44-year-old female in the Stepdown Unit being monitored for septic shock following a severe infection."),
    ("Basic Adult Healthcare", "Ch. 19", "Walter McCaffery", "69-year-old male diagnosed with pulmonary tuberculosis; requires isolation and long-term anti-TB drug therapy."),
    ("Basic Adult Healthcare", "Ch 20", "Tyrone Baker", "33-year-old male with a history of chronic asthma presenting with acute wheezing and shortness of breath."),
    ("Basic Adult Healthcare", "Ch 25", "Jedidiah Billings", "60-year-old male with heart failure experiencing peripheral edema and orthopnea."),
    ("Basic Adult Healthcare", "Ch 26", "Lorna Anderson", "68-year-old female on the Medical Unit with a suspected deep vein thrombosis in her left lower extremity."),
    ("Basic Adult Healthcare", "Ch 34", "Collete Youncy", "51-year-old female managing rheumatoid arthritis; focuses on joint protection and inflammatory triggers."),
    ("Basic Adult Healthcare", "Ch 36", "Jack Armstrong", "52-year-old male scheduled for physical therapy due to advanced osteoarthritis in both knees."),
    ("Basic Adult Healthcare", "Ch 41", "Willow Gussma", "22-year-old female presenting to the ED with acute RLQ pain and nausea, indicative of appendicitis."),
    ("Basic Adult Healthcare", "Ch 42", "Jenna Batch", "37-year-old female seeking consultation for metabolic syndrome and obesity management."),
    ("Basic Adult Healthcare", "Ch 45", "Peggy Sue Allen", "72-year-old female presenting with fatigue and cold intolerance, characteristic of hypothyroidism."),
    ("Basic Adult Healthcare", "Ch 48", "Sidney Barnes", "31-year-old female experiencing acute kidney injury following a severe trauma."),
    ("Basic Adult Healthcare", "Ch 57", "Roxy Hillside", "20-year-old female admitted to the Surgical Care Unit with partial-thickness burns on her upper extremities."),

    # --- Pharmacology ---
    ("Pharmacology", "Ch. 4", "Avery Dawson", "26-year-old female requiring medication reconciliation and education on safe medication use."),
    ("Pharmacology", "Ch. 21", "Thor Smyth", "27-year-old male in the Mental Health Unit being started on antidepressant therapy for major depressive disorder."),
    ("Pharmacology", "Ch. 27", "Earl Duckworth", "58-year-old male requiring multi-drug therapy to manage chronic, resistant hypertension."),
    ("Pharmacology", "Ch 44", "Sadrac Joicin", "51-year-old male receiving Digoxin for heart failure; requires monitoring for toxicity and electrolyte balance."),
    ("Pharmacology", "Ch 55", "Henrique Ramirez", "8-year-old male in the Pediatric Unit requiring inhaled bronchodilators and steroids for asthma management."),
    ("Pharmacology", "Ch 57", "Madilynn Weaver", "27-year-old female with peptic ulcer disease requiring education on proton pump inhibitors and antacids.")
]

# --- Manual Interactive Case Study Mapping (Gold Standard) ---
# Format: (Class, Textbook Chapter, Case Study Title, Description) - simplified to just title and description for consistency
INTERACTIVE_CASE_STUDY_DATA = [
    # --- Basic Adult Healthcare ---
    ("Basic Adult Healthcare", "Ch. 10", "Fluids and Electrolyte Imbalance", "Regulation of body fluids, acid-base balance, and electrolyte gain/loss."),
    ("Basic Adult Healthcare", "Ch. 19", "Pneumonia", "Managing infectious pulmonary disorders and gas exchange."),
    ("Basic Adult Healthcare", "Ch 20", "Chronic Obstructive Pulmonary Disease (COPD)", "Managing \"pink puffers\" vs. \"blue bloaters\" and respiratory depression."),
    ("Basic Adult Healthcare", "Ch 23", "Angina; Myocardial Infarction", "Utilizing \"MONAH\" and managing acute coronary syndrome."),
    ("Basic Adult Healthcare", "Ch 25", "Heart Failure; Pulmonary Edema", "Priorities for \"UNLOAD FAST\" and decreasing afterload."),
    ("Basic Adult Healthcare", "Ch 26", "Chronic Obstructive Pulmonary Disease and Peripheral Vascular Disease", "Managing deep vein thrombosis (DVT) and arterial clotting risks."),
    ("Basic Adult Healthcare", "Ch 27", "Hypertension", "Monitoring for complications like stroke or heart failure."),
    ("Basic Adult Healthcare", "Ch 34", "Systemic Lupus Erythematosus", "Addressing \"Soap Brain MD\" symptoms and immunologic triggers."),
    ("Basic Adult Healthcare", "Ch 36", "Osteoarthritis; Wounds", "Mobility priorities and tissue integrity for degenerative joints."),
    ("Basic Adult Healthcare", "Ch 37", "Fracture", "Managing \"BLT Lard\" (Bone, Location, Type) and neurovascular checks."),
    ("Basic Adult Healthcare", "Ch 45", "Hyperthyroidism; Hypothyroidism", "Managing metabolic regulation and potential \"Thyroid Storm\"."),
    ("Basic Adult Healthcare", "Ch 46", "Diabetes; Type 2 Diabetes Mellitus", "Focus on the \"3 P's\" and insulin vs. non-insulin dependency."),
    ("Basic Adult Healthcare", "Ch 48", "Acute Kidney Injury; Chronic Kidney Disease", "Managing \"AEIOU\" (Anemia, Electrolytes, Infection, Other, Uremia)."),
    
    # --- Pharmacology ---
    ("Pharmacology", "Ch. 4", "Drug Administration and Medication Safety", "Preventing medication errors and following safety protocols."),
    ("Pharmacology", "Ch. 21", "Pharmacologic Treatment of Depression", "Assessing therapeutic effects and psychotropic side effects."),
    ("Pharmacology", "Ch. 23", "Pharmacologic Treatment of Epilepsy", "Monitoring \"FACT\" (Focus, Activity, Color, Time) for seizures."),
    ("Pharmacology", "Ch 24", "Pharmacologic Treatment of Parkinson and Alzheimer Diseases", "Assessing therapeutic effects and psychotropic side effects."), 
    ("Pharmacology", "Ch 27", "Pharmacologic Treatment of Stroke", "Managing embolic vs. hemorrhagic stroke pharmacotherapy."), 
    ("Pharmacology", "Ch 38", "Pharmacologic Treatment of Diabetes", "Managing \"Hot and Dry\" (High Sugar) vs. \"Cold and Clammy\" (Low Sugar)."),
    ("Pharmacology", "Ch 43", "Pharmacologic Treatment of Hypertension", "Utilizing \"ABCD\" treatment logic (ACE, Beta blockers, Calcium, Diuretics)."),
    ("Pharmacology", "Ch 46", "Pharmacologic Treatment of Myocardial Ischemia", "Utilization of nitroglycerin and managing angina pectoris."),
    ("Pharmacology", "Ch 55", "Pharmacologic Treatment of Asthma", "Utilizing \"ASTHMA\" treatment priorities (Adrenergics, Steroids, Theophyllines, etc.)."),
    ("Pharmacology", "Ch 57", "Pharmacologic Treatment of Peptic Ulcer Disease", "Utilizing \"Please Make Tummy Better\" treatment for H. pylori.")
]


# --- Manual vSim Mapping (Gold Standard) ---
# Format: (Class, Textbook Chapter, Patient Name, Summary)
VSIM_DATA = [
    # --- Basic Adult Healthcare ---
    ("Basic Adult Healthcare", "Ch 11", "Jennifer Hoffman", "A 33-year-old female presenting in severe respiratory distress with an acute asthma exacerbation."),
    ("Basic Adult Healthcare", "Ch 19", "Kenneth Bronson", "A 27-year-old male with fever, difficulty breathing, and chest tightness; diagnosed with right lower lobe pneumonia."),
    ("Basic Adult Healthcare", "Ch 20", "Vincent Brody", "A 67-year-old male smoker presenting with wheezing and a productive cough due to a COPD exacerbation."),
    ("Basic Adult Healthcare", "Ch 23", "Carl Shapiro", "A 54-year-old male with a history of hypertension presenting with chest pain and diaphoresis; diagnosed with NSTEMI."),
    ("Basic Adult Healthcare", "Ch 37", "Marilyn Hughes", "A 45-year-old female POD 0 following an ORIF procedure for a mid-shaft tibia-fibula fracture."),
    ("Basic Adult Healthcare", "Ch 41", "Stan Checketts", "A 52-year-old male with severe abdominal pain, nausea, and vomiting; diagnosed with a suspected small bowel obstruction."),
    ("Basic Adult Healthcare", "Ch 46", "Skyler Hansen", "An 18-year-old male with Type 1 diabetes presenting with confusion and acting \"weird\" after exercise; diagnosed with hypoglycemia."),
    ("Basic Adult Healthcare", "Ch 51", "Doris Bowman", "A 39-year-old female in the PACU following a total abdominal hysterectomy for uterine fibroids."),
    ("Basic Adult Healthcare", "Ch 41/26", "Vernon Watkins", "A 69-year-old male POD 4 following a left hemicolectomy; primary clinical risk is a pulmonary embolism."),
    ("Basic Adult Healthcare", "Ch 36/28", "Lloyd Bennett", "A 76-year-old male POD 1 following a left hip arthroplasty requiring a blood transfusion for low hemoglobin."),

    # --- Pharmacology ---
    ("Pharmacology", "Ch 9", "Harry Hadley", "A patient with a MRSA infection receiving IV Vancomycin for cellulitis."),
    ("Pharmacology", "Ch 9", "Suzanne Morris", "Management of Clostridioides difficile infection and adverse drug effects related to antibiotic use."),
    ("Pharmacology", "Ch 21", "Jermaine Jones", "Management of mental health and depression focusing on drug and alcohol interactions."),
    ("Pharmacology", "Ch 21", "Daniella Young Bear", "Medication reconciliation and pain management focusing on opioid and antidepressant drug interactions."),
    ("Pharmacology", "Ch 26", "Yoa Li", "Post-operative pain management utilizing Patient-Controlled Analgesia (PCA) with morphine."),
    ("Pharmacology", "Ch 38", "Juan Carlos", "Diabetes management focusing on insulin therapy, oral hypoglycemics, and hypoglycemia risk."),
    ("Pharmacology", "Ch 44", "Mary Richards", "Heart Failure management with a focus on identifying and treating Digoxin toxicity."),
    ("Pharmacology", "Ch 46", "Junetta Cooper", "Angina and Coronary Artery Disease management focusing on Nitroglycerin therapy."),
    ("Pharmacology", "Ch 48", "Rachael Heidebrink", "Post-surgical anticoagulation therapy (Apixaban and Fondaparinux) following hip surgery."),
    ("Pharmacology", "Ch 53", "Toua Xiong", "Chronic Obstructive Pulmonary Disease (COPD) management focusing on inhaler and oxygen therapy.")
]


STOPWORDS = {
    "the", "and", "of", "in", "to", "a", "for", "with", "on", "at", "by", "from", "or", "as", "an", "is", "be", "are", 
    "unit", "chapter", "part", "notebook", "page", "pages", "ref", "scenario", "case", "study",
    "nclex", "client", "needs", "essential", "essentials", "concept", "exemplar", "blueprint", "year", "years", "old",
    "new", "rn", "pn", "ncjmm", "analyze", "cues", "evaluate", "outcomes", "take", "actions", "prioritize", "hypotheses",
    "physiological", "adaptation", "basic", "comfort", "safety", "infection", "control", "reduction", "potential", "risk",
    "pharmacological", "parenteral", "therapies", "health", "promotion", "maintenance", "psychosocial", "integrity",
    "management", "care", "nursing", "practice", "introduction", "review", "clinical", "judgment", "evidencebased",
    "assessment", "adult", "function", "process", "disorders", "disease", "diseases", "system", "acute", "chronic"
}

data = {
    "chapters": [],
    "resources": []
}

# --- Helpers ---
def generate_id(text):
    return hashlib.md5(text.encode()).hexdigest()[:8]

def extract_keywords(text):
    if not text: return []
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    words = text.split()
    return [w for w in words if w not in STOPWORDS and len(w) > 2]

# --- 1. Parse Chapters (TOC) ---
def parse_chapters(file_path):
    print(f"Parsing Chapters from TOC: {file_path}")
    if not os.path.exists(file_path): return

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    current_class = None
    current_section = "TOC"
    chapter_re = re.compile(r"Chapter\s+(\d+)\s*[:—–-]\s*(.+)")
    
    for line in lines:
        line = line.strip()
        if not line: continue

        if "Basic Adult Healthcare" in line and "Table of Contents" not in line:
            current_class = "Basic Adult Healthcare"
            current_section = "TOC"
        elif "Pharmacology" in line and "Table of Contents" not in line and "Next-Gen" not in line:
            if line == "Pharmacology": 
                current_class = "Pharmacology"
                current_section = "TOC"
        
        if "Next-Gen vSim" in line: current_section = "Other"
        if "Interactive Case Studies" in line: current_section = "Other"
        if "Textbook Table Of Contents" in line: current_section = "TOC"

        if current_section == "TOC":
            match = chapter_re.match(line)
            if match:
                chap_num = match.group(1)
                chap_title = match.group(2).strip()
                data["chapters"].append({
                    "id": f"{current_class[:3]}-{chap_num}",
                    "class": current_class,
                    "number": chap_num,
                    "title": chap_title,
                    "keywords": extract_keywords(chap_title),
                    "related_resources": []
                })

# --- 2. Process Notebook Pages (Manual List) ---
def process_manual_notebook():
    print("Processing Manual Notebook Mapping...")
    for class_name, chap_str, page_str, title_str in NOTEBOOK_DATA:
        # Normalize page_str (p. 347, 349 or p. 111–115)
        clean_pages = [p.strip() for p in page_str.replace('p.', '').replace('–', '-').split(',')]
        
        # Split title_str into individual topics
        titles = [t.strip() for t in re.split(r';', title_str)]
        
        formatted_title_parts = []
        
        page_numbers_expanded = []
        for p_item in clean_pages:
            if '-' in p_item: # Handle ranges like "111-115"
                start, end = map(int, p_item.split('-'))
                page_numbers_expanded.extend([str(i) for i in range(start, end + 1)])
            else:
                page_numbers_expanded.append(p_item)

        if len(titles) == len(page_numbers_expanded):
            for i in range(len(titles)):
                formatted_title_parts.append(f"{titles[i]} p. {page_numbers_expanded[i]}")
            full_title = " ".join(formatted_title_parts)
        elif len(titles) == 1 and len(page_numbers_expanded) > 0:
            full_title = f"{titles[0]} p. {', p. '.join(page_numbers_expanded)}"
        else: # Fallback for complex cases where mapping is unclear, just keep original title_str with all pages
            full_title = f"{title_str} p. {page_str.replace('p. ', '')}"
            

        res_id = generate_id(full_title + class_name) 
        
        data["resources"].append({
            "id": res_id,
            "type": "The Notebook",
            "title": full_title,
            "class": class_name,
            "manual_chap_refs": parse_chap_refs(chap_str)
        })

# --- 3. Process CCC Pages (Manual List) ---
def process_manual_ccc():
    print("Processing Manual CCC Mapping...")
    # CCC_DATA format: (Class, Textbook Chapter, CCC Section Title, Brief Topic Summary)
    # The CCC_DATA list is now correctly a list of 4-element tuples.
    for class_name, chap_str, ccc_section_title, brief_summary in CCC_DATA: # 4 fields now
        full_title = ccc_section_title
        # User confirmed to ignore notebook_page_num for CCC display itself.

        res_id = generate_id(full_title + chap_str + class_name)
        
        data["resources"].append({
            "id": res_id,
            "type": "CCC Page",
            "title": full_title,
            "description": brief_summary, 
            "class": class_name,
            "manual_chap_refs": parse_chap_refs(chap_str)
        })

# --- 4. Process CJ Sim (Manual List) ---
def process_manual_cjsim():
    print("Processing Manual CJ Sim Mapping...")
    for class_name, chap_str, patient_name, summary in CJ_SIM_DATA:
        full_title = patient_name 
        res_id = generate_id(full_title + class_name)
        
        data["resources"].append({
            "id": res_id,
            "type": "CJ Sim",
            "title": full_title,
            "description": summary,
            "class": class_name,
            "manual_chap_refs": parse_chap_refs(chap_str)
        })

# --- 5. Process Interactive Case Studies (Manual List) ---
def process_manual_interactive_case_studies():
    print("Processing Manual Interactive Case Study Mapping...")
    for class_name, chap_str, case_study_title, focus in INTERACTIVE_CASE_STUDY_DATA:
        full_title = f"{case_study_title}"
        res_id = generate_id(full_title + class_name)
        
        data["resources"].append({
            "id": res_id,
            "type": "Interactive Case Study",
            "title": full_title,
            "description": focus,
            "class": class_name,
            "manual_chap_refs": parse_chap_refs(chap_str)
        })

# --- 6. Process vSims (Manual List) ---
def process_manual_vsims():
    print("Processing Manual vSim Mapping...")
    for class_name, chap_str, patient_name, summary in VSIM_DATA:
        full_title = f"{patient_name}"
        res_id = generate_id(full_title + "vsim" + class_name)
        
        data["resources"].append({
            "id": res_id,
            "type": "vSim",
            "title": full_title,
            "description": summary,
            "class": class_name,
            "manual_chap_refs": parse_chap_refs(chap_str)
        })

def parse_chap_refs(chap_str):
    nums = []
    chap_str_cleaned = chap_str.replace('Ch', '').replace('.', '').strip()
    
    parts = re.split(r'[/-]', chap_str_cleaned)
    for part in parts:
        part = part.strip()
        if not part: continue
        if part.isdigit():
            nums.append(part)
        elif '-' in part: 
            sub_parts = part.split('-')
            if len(sub_parts) == 2 and sub_parts[0].isdigit() and sub_parts[1].isdigit():
                start, end = int(sub_parts[0]), int(sub_parts[1])
                nums.extend([str(i) for i in range(start, end + 1)])
    return nums

# --- Execution ---
parse_chapters(os.path.join(ROOT_DIR, "toc.txt"))
process_manual_notebook()
process_manual_ccc()
process_manual_cjsim()
process_manual_interactive_case_studies()
process_manual_vsims()

print("Matching...")
for chapter in data["chapters"]:
    
    for resource in data["resources"]:
        if resource.get("class") and resource["class"] != chapter["class"]:
            continue

        # --- Manual Matching (All) ---
        if "manual_chap_refs" in resource and chapter["number"] in resource["manual_chap_refs"]:
            chapter["related_resources"].append({
                "id": resource["id"],
                "title": resource["title"],
                "type": resource["type"],
                "reason": "Direct Map",
                "score": 100,
                "description": resource.get("description", "")
            })

    # Sort
    chapter["related_resources"].sort(key=lambda x: x["score"], reverse=True)

# Clean
for c in data["chapters"]:
    if "keywords" in c: del c["keywords"]
for r in data["resources"]:
    if "manual_chap_refs" in r: del r["manual_chap_refs"]

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Database updated. All resources integrated. Saved to {OUTPUT_PATH}")
