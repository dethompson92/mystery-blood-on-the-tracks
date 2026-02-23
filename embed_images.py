#!/usr/bin/env python3
"""
Embed 38 missing images into data.js for Mystery 2B - Blood on the Tracks.
Uses verified anchor texts extracted from actual document headings.
Strategy: For portrait images, insert after first </table> in each document.
For content images, insert after specific verified h2 headings.
"""
import re, shutil

def img_html(filename, alt, caption, img_type='evidence'):
    """Generate image HTML in the exact escaped format."""
    if img_type == 'portrait':
        return (
            f'<div class=\\"portrait-container\\">\\n'
            f'                <img src=\\"Images/{filename}\\" class=\\"portrait-image\\" alt=\\"{alt}\\">\\n'
            f'                <div class=\\"image-caption\\">{caption}</div>\\n'
            f'            </div>'
        )
    else:
        return (
            f'<div class=\\"evidence-image-container\\">\\n'
            f'                <img src=\\"Images/{filename}\\" class=\\"evidence-image\\" alt=\\"{alt}\\">\\n'
            f'                <div class=\\"image-caption\\">{caption}</div>\\n'
            f'            </div>'
        )

def find_doc_body(content, doc_key):
    """Find the body string content range for a document."""
    key_pat = f'"{doc_key}"'
    key_pos = content.find(key_pat)
    if key_pos == -1:
        return None, None
    
    body_marker = '"body": "'
    bs = content.find(body_marker, key_pos)
    if bs == -1 or bs > key_pos + 300:
        return None, None
    bs += len(body_marker)
    
    icon_pos = content.find('"icon":', bs)
    if icon_pos == -1:
        return None, None
    be = content.rfind('"', bs, icon_pos)
    return bs, be

def insert_after_anchor(content, doc_key, anchor, html):
    """Insert image HTML after anchor text within document body."""
    bs, be = find_doc_body(content, doc_key)
    if bs is None:
        print(f"  FAIL: Doc '{doc_key}' not found")
        return content, False
    
    body = content[bs:be]
    pos = body.find(anchor)
    if pos == -1:
        print(f"  FAIL: Anchor not found in '{doc_key}': '{anchor[:50]}...'")
        return content, False
    
    insert_at = bs + pos + len(anchor)
    insertion = f"\\n\\n            {html}"
    content = content[:insert_at] + insertion + content[insert_at:]
    print(f"  OK: Inserted in '{doc_key}'")
    return content, True

def insert_after_first_table(content, doc_key, html):
    """Insert image HTML after the first </table> in a document body."""
    return insert_after_anchor(content, doc_key, "</table>", html)

def main():
    filepath = 'data.js'
    shutil.copy2(filepath, 'data.js.backup')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    orig_len = len(content)
    ok = 0; fail = 0
    
    # All insertions using verified anchors
    # Format: (num, doc_key, anchor_type, filename, alt, caption, img_type)
    insertions = [
        # --- PORTRAITS (insert after first </table> in target doc) ---
        
        # 01: Vivienne portrait -> Doc 01
        (1, "01_railroad_police_incident_report", "table",
         "01_vivienne_marchand_victim_portrait.png",
         "Vivienne Marchand - Victim",
         "Fig 1.0: Vivienne Marie Marchand (1925-1957) - Jazz Vocalist and Victim",
         "portrait"),
        
        # 02: Charlotte portrait -> Doc 10
        (2, "10_suspect_statement_devereaux_1957", "table",
         "02_charlotte_devereaux_suspect_portrait.png",
         "Charlotte Devereaux - Suspect",
         "Fig 10.0: Charlotte Devereaux, Age 28 - Primary Suspect",
         "portrait"),
        
        # 03: Vincent DeLuca portrait -> Doc 05
        (3, "05_suspect_interview_deluca", "table",
         "03_vincent_deluca_suspect_portrait.png",
         "Vincent DeLuca",
         "Fig 5.0: Vincent DeLuca, Age 38 - Victim's Fiance",
         "portrait"),
        
        # 04: Maggie Sinclair portrait -> Doc 15
        (4, "15_margaret_sinclair_detailed_statement", "table",
         "04_maggie_sinclair_witness_portrait.png",
         "Margaret Sinclair",
         "Fig 15.0: Margaret Sinclair, Age 20 - Critical Eyewitness",
         "portrait"),
        
        # 05: Dr. Caldwell/Hayes portrait -> Doc 14
        (5, "14_dr_hayes_interview", "table",
         "05_dr_richard_caldwell_witness_portrait.png",
         "Dr. Evelyn Hayes",
         "Fig 14.0: Dr. Evelyn Hayes, Age 35 - Person of Interest",
         "portrait"),
        
        # 06: Ernest Washington portrait -> Doc 04 
        (6, "04_porter_witness_statement", "table",
         "06_ernest_washington_porter_portrait.png",
         "Ernest Washington",
         "Fig 4.0: Ernest Washington, Age 43 - Pullman Porter",
         "portrait"),
        
        # 07: Conductor portrait -> Doc 13
        (7, "13_conductor_witness_statement", "table",
         "07_father_murphy_witness_portrait.png",
         "Theodore Blackwood",
         "Fig 13.0: Theodore Blackwood, Age 55 - Head Conductor",
         "portrait"),
        
        # 08: Bartender portrait -> Doc 12
        (8, "12_bartender_witness_statement", "table",
         "08_thomas_eleanor_whitfield_couple_portrait.png",
         "Billy Ray Henderson",
         "Fig 12.0: Billy Ray Henderson - Bar Car Attendant",
         "portrait"),
        
        # 09: Photographer portrait -> Doc 06
        (9, "06_photographer_witness_statement", "table",
         "09_bobby_chen_suspect_portrait.png",
         "Arthur Whitmore",
         "Fig 6.0: Arthur Whitmore, Age 51 - Photographer",
         "portrait"),
        
        # 10: Detective Chen portrait -> Doc 19 (no table, use first h2)
        (10, "19_cold_case_review_memo_2024", "h2_first",
         "10_detective_sarah_chen_2024_portrait.png",
         "Detective Lt. Sarah Chen",
         "Fig 19.0: Detective Lt. Sarah Chen - NOPD Cold Case Unit, 2024",
         "portrait"),
        
        # --- EVIDENCE PHOTOS ---
        
        # 12: Steamer trunk -> Doc 08 (after heading "DISCOVERY CIRCUMSTANCES")
        (12, "08_trunk_discovery_report_2024", "heading:DISCOVERY CIRCUMSTANCES</h2>",
         "12_steamer_trunk_evidence_photo.png",
         "Steamer Trunk Evidence",
         "Fig 8.1: Steamer Trunk Discovered in Devereaux Estate - November 2024",
         "evidence"),
        
        # 13: Charlotte journal -> Doc 09 (after first table)
        (13, "09_journal_entries_devereaux_1957", "table",
         "13_charlotte_journal_1957_evidence.png",
         "Charlotte Devereaux Journal",
         "Fig 9.1: Charlotte Devereaux Private Journal - 1957",
         "evidence"),
        
        # 14: Love letters -> Doc 11 (after first table)
        (14, "11_love_letters_evidence", "table",
         "14_love_letters_evidence_photo.png",
         "Love Letters Evidence",
         "Fig 11.1: Correspondence Between Vivienne and Charlotte (1954-1957)",
         "evidence"),
        
        # 15: Train tickets -> Doc 01 (after evidence section - use exact anchor)
        (15, "01_railroad_police_incident_report", "heading:IV. Evidence Collected</h2>",
         "15_train_tickets_1957_evidence.png",
         "1957 Train Tickets",
         "Fig 1.5: Silver Comet Passenger Tickets - Evidence Items",
         "evidence"),
        
        # 16: Crime scene -> Doc 02 (after scene overview heading)
        (16, "02_crime_scene_investigation_report", "heading:I. Scene Overview",
         "16_vivienne_compartment_crime_scene_1957.png",
         "Crime Scene - Compartment 7",
         "Fig 2.0: Crime Scene Overview - Compartment 7, Magnolia Sleeper Car",
         "evidence"),
        
        # 17: Sleeper compartment -> Doc 02 (after measurements heading)
        (17, "02_crime_scene_investigation_report", "heading:II. Compartment Physical Description",
         "17_sleeper_compartment_interior_general.png",
         "Sleeper Compartment Interior",
         "Fig 2.1: Typical First-Class Sleeper Compartment Configuration",
         "evidence"),
        
        # 18: Vivienne & Charlotte photo -> Doc 20 (after first h3 or content start)
        (18, "20_charlotte_devereaux_confession_2024", "h2_first",
         "18_photograph_vivienne_charlotte_together_1955.png",
         "Vivienne and Charlotte Together",
         "Fig 20.1: Vivienne Marchand and Charlotte Devereaux - circa 1955",
         "evidence"),
        
        # 19: Silver Comet exterior -> Doc 01 (after scene description heading)
        (19, "01_railroad_police_incident_report", "heading:II. Scene Description",
         "19_silver_comet_sleeper_car_exterior_1957.png",
         "Silver Comet Sleeper Car",
         "Fig 1.2: Silver Comet Magnolia Sleeper Car - Exterior View, 1957",
         "evidence"),
        
        # 20: Lounge car -> Doc 12 (after heading "Statement of Witness")
        (20, "12_bartender_witness_statement", "heading:Statement of Witness</h2>",
         "20_lounge_observation_car_interior_1957.png",
         "Lounge Car Interior",
         "Fig 12.1: Silver Comet Lounge Car Interior",
         "evidence"),
        
        # 21: Dining car -> Doc 04 (after WITNESS STATEMENT heading)
        (21, "04_porter_witness_statement", "heading:WITNESS STATEMENT (Question and Answer Format)</h2>",
         "21_dining_car_interior_1957.png",
         "Dining Car Interior",
         "Fig 4.1: Silver Comet Dining Car Interior",
         "evidence"),
        
        # 22: Chicago Union Station -> Doc 23 (after first h2)
        (22, "23_player_investigation_guide", "h2_first",
         "22_chicago_union_station_1957.png",
         "Chicago Union Station",
         "Fig 23.1: Chicago Union Station - Departure Point, November 1957",
         "evidence"),
        
        # 23: Silver Comet at night -> Doc 25 (after first table)
        (23, "25_timeline_reconstruction", "table",
         "23_silver_comet_train_night_countryside.png",
         "Silver Comet at Night",
         "Fig 25.1: The Silver Comet Traveling Through the Night",
         "evidence"),
        
        # 24: New Orleans French Quarter -> Doc 09 (after WITNESS STATEMENT heading)
        (24, "09_journal_entries_devereaux_1957", "heading:WITNESS STATEMENT (Question and Answer Format)</h2>",
         "24_new_orleans_french_quarter_1957.png",
         "New Orleans French Quarter",
         "Fig 9.2: New Orleans French Quarter - 1957",
         "evidence"),
        
        # 25: Newspaper headline -> Doc 18 (after Executive Summary heading)
        (25, "18_case_closure_1958", "heading:Executive Summary</h2>",
         "25_1957_newspaper_headline_murder.png",
         "1957 Newspaper Headline",
         "Fig 18.1: Jackson Daily News - Murder Aboard the Silver Comet",
         "evidence"),
        
        # 26: Train schedule -> Doc 17 (after COMPREHENSIVE TIMELINE heading)
        (26, "17_detective_notes_timeline", "heading:COMPREHENSIVE TIMELINE",
         "26_silver_comet_train_schedule_1957.png",
         "Train Schedule",
         "Fig 17.1: Silver Comet Schedule, November 1957",
         "evidence"),
        
        # 27: NOPD evidence tag -> Doc 08 (after INVENTORY heading)
        (27, "08_trunk_discovery_report_2024", "heading:INVENTORY OF TRUNK CONTENTS</h2>",
         "27_nopd_evidence_bag_tag_2024.png",
         "NOPD Evidence Tag",
         "Fig 8.2: NOPD Evidence Processing Tag - November 2024",
         "evidence"),
        
        # 28: Jackson PD report cover -> Doc 00 (after Project Statistics)
        (28, "00_MASTER_INDEX_AND_CATALOG", "heading:Project Statistics</h3>",
         "28_jackson_pd_police_report_cover_1957.png",
         "Jackson PD Case File",
         "Fig 0.1: Jackson PD - Case File 57-1114-HOMI",
         "evidence"),
        
        # 29: Compartment 7 floor plan -> Doc 02 (after FLOOR PLAN DIAGRAM)
        (29, "02_crime_scene_investigation_report", "heading:COMPARTMENT 7 - FLOOR PLAN DIAGRAM</h3>",
         "29_compartment_7_floor_plan_diagram.png",
         "Compartment 7 Floor Plan",
         "Fig 2.3: Compartment 7 Floor Plan with Evidence Markers",
         "evidence"),
        
        # --- INFOGRAPHICS & DIAGRAMS ---
        
        # 32: Murder timeline -> Doc 17 (after PERSONS OF INTEREST heading)
        (32, "17_detective_notes_timeline", "heading:PERSONS OF INTEREST / SUSPECTS</h2>",
         "32_murder_timeline_infographic.png",
         "Murder Timeline",
         "Fig 17.2: Timeline of Events - November 13-14, 1957",
         "evidence"),
        
        # 33: Route map -> Doc 23 (after How to Play heading)
        (33, "23_player_investigation_guide", "heading:How to Play</h2>",
         "33_silver_comet_route_map.png",
         "Silver Comet Route Map",
         "Fig 23.3: Silver Comet Route - New Orleans to Chicago",
         "evidence"),
        
        # 34: Evidence board -> Doc 26 (first h3 or start)
        (34, "26_evidence_board_visualization", "h2_first",
         "34_detective_evidence_board.png",
         "Evidence Board",
         "Fig 26.1: Detective Holloway Investigation Evidence Board",
         "evidence"),
        
        # 35: Character relationship web -> Doc 24 (start of doc)
        (35, "24_character_dossiers", "h2_first",
         "35_character_relationship_web.png",
         "Character Relationships",
         "Fig 24.1: Character Relationships and Connections",
         "evidence"),
        
        # 36: Historical context -> Doc 28 (after first h2)
        (36, "28_historical_context_document", "heading:I. INTRODUCTION: THE WORLD OF 1957</h2>",
         "36_historical_context_1957_vs_2024.png",
         "Historical Context",
         "Fig 28.1: Historical Context - 1957 vs 2024",
         "evidence"),
        
        # 37: Chain of custody -> Doc 32 (evidence chain of custody doc)
        (37, "32_evidence_chain_of_custody", "table",
         "37_evidence_chain_custody_flowchart.png",
         "Chain of Custody",
         "Fig 32.1: Evidence Chain of Custody Flowchart",
         "evidence"),
        
        # 38: Evidence catalog -> Doc 16 (after first table)
        (38, "16_evidence_photographs_documentation", "table",
         "38_evidence_catalog_grid.png",
         "Evidence Catalog",
         "Fig 16.2: Complete Evidence Catalog",
         "evidence"),
        
        # 40: Dead ends -> Doc 33 (investigative dead ends doc)
        (40, "33_investigative_dead_ends", "table",
         "40_investigative_dead_ends_diagram.png",
         "Investigative Dead Ends",
         "Fig 33.1: Summary of Investigative Dead Ends",
         "evidence"),
        
        # 41: DNA comparison -> Doc 07 (after RESULTS heading)
        (41, "07_dna_analysis_2024_cold_case", "heading:RESULTS</h2>",
         "41_dna_comparison_chart_2024.png",
         "DNA Comparison Chart",
         "Fig 7.1: DNA Analysis Results - Silk Scarf Evidence",
         "evidence"),
        
        # 42: Forensic science -> Doc 21 (after first h2)
        (42, "21_district_attorney_summary_2024", "heading:Case Summary: NOPD-COLD-2024-0847</h2>",
         "42_forensic_science_1957_vs_2024.png",
         "Forensic Science Comparison",
         "Fig 21.1: Forensic Science - 1957 vs 2024",
         "evidence"),
    ]
    
    for num, doc_key, anchor_type, filename, alt, caption, img_type in insertions:
        print(f"[{num:02d}] {filename} ({img_type})")
        html = img_html(filename, alt, caption, img_type)
        
        if anchor_type == "table":
            content, success = insert_after_first_table(content, doc_key, html)
        elif anchor_type == "h2_first":
            # Find first <h2 in the document body and insert after the </h2>
            bs, be = find_doc_body(content, doc_key)
            if bs is None:
                print(f"  FAIL: Doc '{doc_key}' not found")
                fail += 1
                continue
            body = content[bs:be]
            # Find first h2 closing tag
            h2_close = body.find("</h2>")
            if h2_close == -1:
                # Try h3
                h2_close = body.find("</h3>")
            if h2_close == -1:
                # Fall back to first </p>
                h2_close = body.find("</p>")
            if h2_close == -1:
                print(f"  FAIL: No heading found in '{doc_key}'")
                fail += 1
                continue
            h2_close += len("</h2>")
            insert_at = bs + h2_close
            insertion = f"\\n\\n            {html}"
            content = content[:insert_at] + insertion + content[insert_at:]
            print(f"  OK: Inserted in '{doc_key}' (after first heading)")
            ok += 1
            continue
        elif anchor_type.startswith("heading:"):
            anchor_text = anchor_type[len("heading:"):]
            content, success = insert_after_anchor(content, doc_key, anchor_text, html)
        else:
            print(f"  FAIL: Unknown anchor type '{anchor_type}'")
            fail += 1
            continue
        
        if anchor_type != "h2_first":
            if success:
                ok += 1
            else:
                fail += 1
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    new_len = len(content)
    print(f"\n{'='*60}")
    print(f"Successful: {ok}")
    print(f"Failed: {fail}")
    print(f"Size: {orig_len:,} -> {new_len:,} (+{new_len - orig_len:,})")
    
    refs = set(re.findall(r'Images/\d+_[a-zA-Z0-9_]+\.png', content))
    print(f"Unique images referenced: {len(refs)}/42")
    
    if fail > 0:
        print("\n*** Some insertions FAILED ***")
        # Show which images are still missing
        import os
        all_imgs = set(f for f in os.listdir('Images') if f.endswith('.png'))
        found = set(m.split('/')[-1] for m in re.findall(r'Images/([^"\\]+\.png)', content))
        missing = sorted(all_imgs - found)
        print(f"Still missing ({len(missing)}):")
        for m in missing:
            print(f"  {m}")

if __name__ == '__main__':
    main()
