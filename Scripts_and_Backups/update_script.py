import re
import os

filepath = r"c:\Users\Devon Thompson\Downloads\Mystery 2B - Blood on the Tracks\data.js"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

new_body = r"""<div class=\"container\">\n        <h1>\ud83d\udd0d MYSTERY #2B: BLOOD ON THE TRACKS</h1>\n        <h2 style=\"text-align: center; color: #8b0000;\">Investigation Guide for Players</h2>\n\n            <div class=\"evidence-image-container\">\n                <img src=\"Images/22_chicago_union_station_1957.png\" class=\"evidence-image\" alt=\"Chicago Union Station\">\n                <div class=\"image-caption\">Fig 23.1: Chicago Union Station - Departure Point, November 1957</div>\n            </div>\n\n        <div class=\"intro-box\">\n            <h3 style=\"margin-top: 0;\">Welcome, Detective!</h3>\n            <p>You are about to investigate one of the most perplexing locked-room mysteries in American criminal history. On November 14, 1957, jazz singer Vivienne Marchand was murdered aboard the luxurious Silver Comet passenger train. The crime remained unsolved for 67 years\u2014until new evidence emerged in 2024.</p>\n            <p><strong>Your mission:</strong> Examine all the evidence, interview transcripts, and forensic reports to determine: <strong>WHO killed Vivienne Marchand, HOW they did it, and WHY?</strong></p>\n        </div>\n\n        <h2>\ud83d\udccb How to Play</h2>\n\n            <div class=\"evidence-image-container\">\n                <img src=\"Images/33_silver_comet_route_map.png\" class=\"evidence-image\" alt=\"Silver Comet Route Map\">\n                <div class=\"image-caption\">Fig 23.3: Silver Comet Route - New Orleans to Chicago</div>\n            </div>\n        <ol>\n            <li><strong>Read the Documents:</strong> You have access to 20+ original police reports, witness statements, forensic analyses, and investigative notes from both 1957 and 2024.</li>\n            <li><strong>Analyze the Evidence:</strong> Look for inconsistencies, hidden connections, and overlooked clues.</li>\n        </ol>\n\n        <div class=\"tip\">\n            \ud83d\udca1 <strong>Tip:</strong> This is a HISTORICAL mystery with sensitive themes. The case involves LGBTQ+ persecution in 1957 America. Approach with empathy and historical awareness.\n        </div>\n\n        <h2>\ud83c\udfaf Key Questions to Answer</h2>\n        <div class=\"evidence-list\">\n            <h3>Phase 1: 1957 Initial Investigation</h3>\n            <ol>\n                <li><strong>WHO</strong> was aboard the train and had the opportunity?</li>\n                <li><strong>HOW</strong> did the killer escape from a compartment that was locked from the inside?</li>\n            </ol>\n            \n            <h3>Phase 2: The Cold Case Break</h3>\n            <ol>\n                <li><strong>WHAT</strong> is the significance of the \"mystery woman in burgundy\"?</li>\n                <li><strong>WHERE</strong> did the murder weapon (the burgundy-gold silk scarf) go?</li>\n            </ol>\n            \n            <h3>Phase 3: The Truth Revealed</h3>\n            <ol>\n                <li><strong>WHY</strong> was Vivienne murdered? What was the true motive?</li>\n                <li><strong>WHO</strong> is the killer?</li>\n            </ol>\n        </div>\n\n        <div style=\"background-color: #1e3c72; color: white; padding: 30px; margin-top: 50px; border-radius: 10px; text-align: center;\">\n            <h2 style=\"color: white; border: none; margin-top: 0;\">Ready to Begin?</h2>\n            <p style=\"font-size: 18px;\">Start your investigation by reading the initial police reports.</p>\n            <p style=\"font-size: 20px; font-weight: bold; margin-top: 20px;\">Good luck, Detective. Justice has been waiting 67 years.</p>\n        </div>\n    </div>"""

# find the body tag for 23_player_investigation_guide
import re

pattern = re.compile(r'("23_player_investigation_guide": \{\s*"title": "Investigation Guide for Players",\s*"body": ")(.*?)(",\n\s*"icon":)', re.DOTALL)

def repl(match):
    return match.group(1) + new_body + match.group(3)

new_content = pattern.sub(repl, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Done")
