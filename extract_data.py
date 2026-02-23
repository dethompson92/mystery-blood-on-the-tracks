import os
import re
import json

base_dir = r"c:/Users/Devon Thompson/Downloads/Mystery 2B - Blood on the Tracks"
output_file = os.path.join(base_dir, "data.js")

documents = {}

# Categories mapping (File prefix -> Category)
# This is a rough mapping based on the filenames and user request
sections = [
    {"title": "📋 CASE OVERVIEW", "items": ["00_MASTER_INDEX_AND_CATALOG", "23_player_investigation_guide", "29_gameplay_facilitation_guide"]},
    {"title": "👥 CHARACTERS", "items": ["24_character_dossiers", "34_psychological_analysis"]},
    {"title": "📄 OFFICIAL REPORTS (1957)", "items": ["01_railroad_police_incident_report", "02_crime_scene_investigation_report", "03_medical_examiner_autopsy_report", "18_case_closure_1958"]},
    {"title": "💬 WITNESS STATEMENTS (1957)", "items": ["04_porter_witness_statement", "06_photographer_witness_statement", "12_bartender_witness_statement", "13_conductor_witness_statement", "14_dr_hayes_interview", "15_margaret_sinclair_detailed_statement"]},
    {"title": "🔍 SUSPECT INTERVIEWS (1957)", "items": ["05_suspect_interview_deluca", "10_suspect_statement_devereaux_1957"]},
    {"title": "🧪 PHYSICAL EVIDENCE", "items": ["11_love_letters_evidence", "16_evidence_photographs_documentation", "32_evidence_chain_of_custody"]},
    {"title": "📰 PRESS & DOCUMENTS", "items": ["30_press_release_collection_1957", "33_investigative_dead_ends"]},
    {"title": "🧩 INVESTIGATION TOOLS", "items": ["17_detective_notes_timeline", "25_timeline_reconstruction", "26_evidence_board_visualization"]},
    {"title": "❄️ COLD CASE FILES (2024)", "items": ["19_cold_case_review_memo_2024", "07_dna_analysis_2024_cold_case", "08_trunk_discovery_report_2024", "20_charlotte_devereaux_confession_2024", "21_district_attorney_summary_2024", "22_final_case_closure_2024", "31_press_release_2024"]},
    {"title": "📚 CONTEXT & EDUCATION", "items": ["28_historical_context_document", "35_educational_discussion_guide"]},
    {"title": "✅ SOLUTION", "items": ["27_complete_solution_document"]}
]

# Track which files we've assigned to a category
assigned_files = []
for s in sections:
    assigned_files.extend(s['items'])

# Walk through the directory
for filename in os.listdir(base_dir):
    if filename.endswith(".html") and filename != "index.html":
        file_path = os.path.join(base_dir, filename)
        file_id = os.path.splitext(filename)[0]
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Extract Title
            title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            title = title_match.group(1) if title_match else file_id
            
            # Extract Style (for preserving specific fonts/layouts if needed per page)
            # Actually, most styles are similar. We'll extract the <body> content.
            body_match = re.search(r'<body>(.*?)</body>', content, re.IGNORECASE | re.DOTALL)
            body_content = body_match.group(1) if body_match else ""
            
            # Remove any existing navigation or index buttons if they exist
            # (Optional, but helps keep it clean)
            
            documents[file_id] = {
                "title": title,
                "body": body_content.strip()
            }

# Catch any files that weren't in the preset sections and add to "MISC"
misc_items = [fid for fid in documents.keys() if fid not in assigned_files]
if misc_items:
    sections.append({"title": "📁 ADDITIONAL FILES", "items": misc_items})

# Add icons based on keywords
for doc_id in documents:
    title = documents[doc_id]['title'].lower()
    if 'report' in title or 'incident' in title: documents[doc_id]['icon'] = '📄'
    elif 'interview' in title or 'statement' in title: documents[doc_id]['icon'] = '💬'
    elif 'dossier' in title or 'portrait' in title: documents[doc_id]['icon'] = '👥'
    elif 'evidence' in title or 'discovery' in title: documents[doc_id]['icon'] = '🧪'
    elif 'notes' in title or 'timeline' in title: documents[doc_id]['icon'] = '🧩'
    elif 'case' in title and '2024' in doc_id: documents[doc_id]['icon'] = '❄️'
    elif 'solution' in title: documents[doc_id]['icon'] = '✅'

final_data = {
    "documents": documents,
    "structure": sections
}

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("const caseData = " + json.dumps(final_data, indent=2) + ";")

print(f"Extraction complete. {len(documents)} files processed into data.js")
