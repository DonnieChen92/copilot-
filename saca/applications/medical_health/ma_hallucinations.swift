// Swift version (concise, detailed comments, Xcode-ready; add to a Command Line Tool project in Xcode)
// For Windows enhancement: Use cross-platform Swift (e.g., via Swift for Windows) or add Foundation for console

struct Row {
    let approach: String
    let mechanism: String
    let target: String
    let onset: String
    let stability: String
    let involvement: String
    let risks: String
    let suitability: String
    let australiaStatus: String
}

func printTable(rows: [Row]) {
    let colWidth = 30  // Concise width adjustment

    // Header with details
    print("| \(String(format: "%-\(colWidth)s", "Approach")) | \(String(format: "%-\(colWidth)s", "Core Mechanism")) | \(String(format: "%-\(colWidth)s", "Target")) | \(String(format: "%-10s", "Speed")) | \(String(format: "%-12s", "Stability")) | \(String(format: "%-14s", "Involvement")) | \(String(format: "%-20s", "Risks")) | \(String(format: "%-32s", "MA Hallucinations Suitability")) | \(String(format: "%-30s", "Australia 2026 Status")) |")
    print(String(repeating: "-", count: 236))  // Separator

    // Rows (concise loop)
    for row in rows {
        print("| \(String(format: "%-\(colWidth)s", row.approach)) | \(String(format: "%-\(colWidth)s", row.mechanism)) | \(String(format: "%-\(colWidth)s", row.target)) | \(String(format: "%-10s", row.onset)) | \(String(format: "%-12s", row.stability)) | \(String(format: "%-14s", row.involvement)) | \(String(format: "%-20s", row.risks)) | \(String(format: "%-32s", row.suitability)) | \(String(format: "%-30s", row.australiaStatus)) |")
    }
}

// Data array (detailed for reference)
let rows: [Row] = [
    Row(approach: "Desensitisation/Exposure", mechanism: "Habituation + extinction", target: "Fear/avoidance of voices", onset: "Slow", stability: "Good", involvement: "High", risks: "Temp anxiety", suitability: "★★★★★", australiaStatus: "Yes (as part of CBT)"),
    Row(approach: "CBT / CBTp", mechanism: "Cognitive & behavioral change", target: "Beliefs about voices + coping", onset: "Medium", stability: "Excellent", involvement: "Very High", risks: "Very low", suitability: "★★★★☆", australiaStatus: "Strongly Recommended"),
    Row(approach: "ECT", mechanism: "Neurochemical reset", target: "Severe refractory psychosis", onset: "Very Fast", stability: "Moderate", involvement: "Very Low", risks: "Memory loss, cardiac", suitability: "★☆☆☆☆", australiaStatus: "Allowed (strictly limited)"),
    Row(approach: "Antipsychotics", mechanism: "D2 blockade (±5-HT2A)", target: "Acute hallucinations/delusions", onset: "Fast", stability: "Moderate", involvement: "Low", risks: "EPS, metabolic", suitability: "★★★★☆", australiaStatus: "Strongly Recommended (acute phase)"),
    Row(approach: "MA-induced Auditory Hallucinations (symptom)", mechanism: "Dopamine hyperactivity", target: "Persecutory/command voices", onset: "Acute–Residual", stability: "Poor", involvement: "None", risks: "Violence risk", suitability: "—", australiaStatus: "Treated as substance-induced psychosis"),
    Row(approach: "CBT for MA Hallucinations", mechanism: "Voice belief change + coping", target: "Residual voice distress", onset: "Medium", stability: "Good", involvement: "High", risks: "Very low", suitability: "★★★★☆", australiaStatus: "Strongly Recommended")
]

printTable(rows: rows)
