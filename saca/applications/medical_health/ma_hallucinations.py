# Python version: More concise with detailed comments
class Row:
    def __init__(self, approach, mechanism, target, onset, stability, involvement, risks, suitability, australiaStatus):
        self.approach = approach
        self.mechanism = mechanism
        self.target = target
        self.onset = onset
        self.stability = stability
        self.involvement = involvement
        self.risks = risks
        self.suitability = suitability
        self.australiaStatus = australiaStatus

def print_table(rows):
    col_width = 30  # Concise width
    # Header (detailed for clarity)
    print(f"| {'Approach':<{col_width}} | {'Core Mechanism':<{col_width}} | {'Target':<{col_width}} | {'Speed':<10} | {'Stability':<12} | {'Involvement':<14} | {'Risks':<20} | {'MA Hallucinations Suitability':<32} | {'Australia 2026 Status':<30} |")
    print('-' * 236)  # Line separator

    # Rows loop (concise)
    for row in rows:
        print(f"| {row.approach:<{col_width}} | {row.mechanism:<{col_width}} | {row.target:<{col_width}} | {row.onset:<10} | {row.stability:<12} | {row.involvement:<14} | {row.risks:<20} | {row.suitability:<32} | {row.australiaStatus:<30} |")

# Data (detailed for completeness)
rows = [
    Row("Desensitisation/Exposure", "Habituation + extinction", "Fear/avoidance of voices", "Slow", "Good", "High", "Temp anxiety", "★★★★★", "Yes (as part of CBT)"),
    Row("CBT / CBTp", "Cognitive & behavioral change", "Beliefs about voices + coping", "Medium", "Excellent", "Very High", "Very low", "★★★★☆", "Strongly Recommended"),
    Row("ECT", "Neurochemical reset", "Severe refractory psychosis", "Very Fast", "Moderate", "Very Low", "Memory loss, cardiac", "★☆☆☆☆", "Allowed (strictly limited)"),
    Row("Antipsychotics", "D2 blockade (±5-HT2A)", "Acute hallucinations/delusions", "Fast", "Moderate", "Low", "EPS, metabolic", "★★★★☆", "Strongly Recommended (acute phase)"),
    Row("MA-induced Auditory Hallucinations (symptom)", "Dopamine hyperactivity", "Persecutory/command voices", "Acute–Residual", "Poor", "None", "Violence risk", "—", "Treated as substance-induced psychosis"),
    Row("CBT for MA Hallucinations", "Voice belief change + coping", "Residual voice distress", "Medium", "Good", "High", "Very low", "★★★★☆", "Strongly Recommended")
]

print_table(rows)
