// Rust version (concise, detailed comments; for Windows enhancement: use std::io, cross-platform, or add console libs like termion for color; compile with cargo)
// cargo run to execute

#[derive(Clone)]
struct Row {
    approach: String,
    mechanism: String,
    target: String,
    onset: String,
    stability: String,
    involvement: String,
    risks: String,
    suitability: String,
    australia_status: String,
}

fn print_table(rows: &[Row]) {
    let col_width: usize = 30; // Concise width

    // Header (detailed)
    println!("| {:<col_width$} | {:<col_width$} | {:<col_width$} | {:<10} | {:<12} | {:<14} | {:<20} | {:<32} | {:<30} |", "Approach", "Core Mechanism", "Target", "Speed", "Stability", "Involvement", "Risks", "MA Hallucinations Suitability", "Australia 2026 Status");
    println!("{}", "-".repeat(236)); // Separator

    // Rows (concise loop)
    for row in rows {
        println!("| {:<col_width$} | {:<col_width$} | {:<col_width$} | {:<10} | {:<12} | {:<14} | {:<20} | {:<32} | {:<30} |",
            row.approach, row.mechanism, row.target, row.onset, row.stability, row.involvement, row.risks, row.suitability, row.australia_status);
    }
}

fn main() {
    let rows = vec![
        Row { approach: "Desensitisation/Exposure".to_string(), mechanism: "Habituation + extinction".to_string(), target: "Fear/avoidance of voices".to_string(), onset: "Slow".to_string(), stability: "Good".to_string(), involvement: "High".to_string(), risks: "Temp anxiety".to_string(), suitability: "★★★★★".to_string(), australia_status: "Yes (as part of CBT)".to_string() },
        Row { approach: "CBT / CBTp".to_string(), mechanism: "Cognitive & behavioral change".to_string(), target: "Beliefs about voices + coping".to_string(), onset: "Medium".to_string(), stability: "Excellent".to_string(), involvement: "Very High".to_string(), risks: "Very low".to_string(), suitability: "★★★★☆".to_string(), australia_status: "Strongly Recommended".to_string() },
        Row { approach: "ECT".to_string(), mechanism: "Neurochemical reset".to_string(), target: "Severe refractory psychosis".to_string(), onset: "Very Fast".to_string(), stability: "Moderate".to_string(), involvement: "Very Low".to_string(), risks: "Memory loss, cardiac".to_string(), suitability: "★☆☆☆☆".to_string(), australia_status: "Allowed (strictly limited)".to_string() },
        Row { approach: "Antipsychotics".to_string(), mechanism: "D2 blockade (±5-HT2A)".to_string(), target: "Acute hallucinations/delusions".to_string(), onset: "Fast".to_string(), stability: "Moderate".to_string(), involvement: "Low".to_string(), risks: "EPS, metabolic".to_string(), suitability: "★★★★☆".to_string(), australia_status: "Strongly Recommended (acute phase)".to_string() },
        Row { approach: "MA-induced Auditory Hallucinations (symptom)".to_string(), mechanism: "Dopamine hyperactivity".to_string(), target: "Persecutory/command voices".to_string(), onset: "Acute–Residual".to_string(), stability: "Poor".to_string(), involvement: "None".to_string(), risks: "Violence risk".to_string(), suitability: "—".to_string(), australia_status: "Treated as substance-induced psychosis".to_string() },
        Row { approach: "CBT for MA Hallucinations".to_string(), mechanism: "Voice belief change + coping".to_string(), target: "Residual voice distress".to_string(), onset: "Medium".to_string(), stability: "Good".to_string(), involvement: "High".to_string(), risks: "Very low".to_string(), suitability: "★★★★☆".to_string(), australia_status: "Strongly Recommended".to_string() },
    ];

    print_table(&rows);
}
