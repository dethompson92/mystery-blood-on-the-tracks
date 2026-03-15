import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the layout
solve_case_html = '''
            <div id="solve-case-page" style="display: none; height: 100%; overflow-y: auto;">
                <div class="document-body">
                    <h1 style="font-family: 'Special Elite', cursive; color: var(--accent-color); text-align: center; font-size: 2.5rem; margin-top: 0;">SOLVE THE MYSTERY</h1>
                    <p style="text-align: center; font-size: 1.2rem; margin-bottom: 40px;">Select all corresponding pieces of evidence for each question and explain your deductions.</p>
                    
                    <div id="questions-container" style="max-width: 600px; margin: 0 auto;"></div>
                    
                    <div style="text-align: center; margin-top: 40px;">
                        <button onclick="submitSolution()" style="padding: 15px 40px; background-color: var(--accent-color); color: white; border: none; font-family: 'Special Elite', cursive; font-size: 1.3rem; cursor: pointer; border-radius: 4px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">SUBMIT FINDINGS</button>
                    </div>
                </div>
            </div>

            <div id="solve-results-page" style="display: none; height: 100%; overflow-y: auto;">
                <div class="document-body">
                    <h1 style="font-family: 'Special Elite', cursive; color: #2ecc71; text-align: center; font-size: 2.5rem; margin-top: 0;">EVIDENCE VERIFIED</h1>
                    <p style="text-align: center; font-size: 1.2rem; margin-bottom: 30px;">Your evidence supports the correct conclusions. Now, present your deductions for final grading.</p>
                    
                    <div id="results-container" style="max-width: 700px; margin: 0 auto; background: var(--bg-color); padding: 20px; border-radius: 8px; border: 1px dashed #ccc;"></div>
                    
                    <div style="text-align: center; margin-top: 30px;">
                        <button onclick="copyForAIGrading()" style="padding: 12px 30px; background-color: #3498db; color: white; border: none; font-family: 'Special Elite', cursive; font-size: 1.1rem; cursor: pointer; border-radius: 4px; box-shadow: 0 4px 10px rgba(0,0,0,0.2); margin-bottom: 20px;">📋 COPY FOR AI GRADING</button>
                        
                        <div style="margin-top: 30px; padding: 20px; border-top: 2px dashed #ccc;">
                            <h3 style="font-family: 'Special Elite', cursive;">Final Assessment</h3>
                            <p>Once graded by your AI partner, enter your final score (0-100) below to close the case.</p>
                            <input type="number" id="final-ai-score" min="0" max="100" placeholder="Score %" style="padding: 10px; font-size: 1.2rem; width: 120px; text-align: center; margin-right: 15px; border-radius: 4px; border: 1px solid #ccc;">
                            <button onclick="finalizeMystery()" style="padding: 12px 30px; background-color: var(--accent-color); color: white; border: none; font-family: 'Special Elite', cursive; font-size: 1.1rem; cursor: pointer; border-radius: 4px;">FINALIZE CASE</button>
                        </div>
                    </div>
                </div>
            </div>
'''

old_solve_case_html = re.search(r'\<div id="solve-case-page".*?\<div id="doc-active-content"', html, re.DOTALL)
if old_solve_case_html:
    html = html.replace(old_solve_case_html.group(0), solve_case_html + '\n            <div id="doc-active-content"')

# 2. Update the javascript
js_code = '''
        const solveQuestions = [
            { id: 'q1', text: '1. WHO is the killer? (Select Required Evidence & Explain)', requiredEvidence: ['20_charlotte_devereaux_confession_2024', '19_cold_case_review_memo_2024'], actualAnswer: 'Charlotte Devereaux, performing a "mercy killing" to save Vivienne from exposure and prison.' },
            { id: 'q2', text: '2. HOW did they escape the locked room?', requiredEvidence: ['20_charlotte_devereaux_confession_2024', '02_crime_scene_investigation_report'], actualAnswer: 'She never left. She remained hidden in Compartment 2 while the porter opened the adjoining door, slipping out during the chaos.' },
            { id: 'q3', text: '3. WHY was Vivienne murdered? (Motive)', requiredEvidence: ['11_love_letters_evidence', '09_journal_entries_devereaux_1957'], actualAnswer: 'The Lavender Scare. Vivienne planned to expose their relationship out of spite, which would have destroyed Charlotte\\'s career and likely sent her to prison.' },
            { id: 'q4', text: '4. WHAT happened to the murder weapon?', requiredEvidence: ['08_trunk_discovery_report_2024', '07_dna_analysis_2024_cold_case'], actualAnswer: 'Charlotte hid the scarf in her steamer trunk, which was locked away in an attic for 67 years until discovered by her grand-niece.' },
            { id: 'q5', text: '5. WHO is the "mystery woman in burgundy"?', requiredEvidence: ['15_margaret_sinclair_detailed_statement', '20_charlotte_devereaux_confession_2024'], actualAnswer: 'It was Charlotte Devereaux, wearing Vivienne\\'s gifted burgundy scarf before using it as the murder weapon.' }
        ];

        function showSolveCasePage() {
            document.getElementById('landing-page').style.display = 'none';
            document.getElementById('doc-active-content').style.display = 'none';
            document.getElementById('solve-results-page').style.display = 'none';
            document.getElementById('solve-case-page').style.display = 'block';
            document.getElementById('breadcrumb').innerText = `CASE_FILES / SOLVE CASE`;
            currentDoc = null;
            
            if (window.innerWidth <= 768) {
                document.getElementById('sidebar').classList.remove('sidebar-open');
            }
            
            renderSolveCheckboxes();
        }

        function renderSolveCheckboxes() {
            const container = document.getElementById('questions-container');
            container.innerHTML = '';
            
            let evidenceOptions = [];
            Object.keys(caseData.documents).forEach(id => {
                if(spoilerDocs.includes(id) && id !== '20_charlotte_devereaux_confession_2024' && id !== '19_cold_case_review_memo_2024' && id !== '07_dna_analysis_2024_cold_case' && id !== '08_trunk_discovery_report_2024') {
                    if(id === '27_complete_solution_document') return;
                }
                const doc = caseData.documents[id];
                evidenceOptions.push({id: id, title: doc.shortTitle || doc.title});
            });

            solveQuestions.forEach(q => {
                const qDiv = document.createElement('div');
                qDiv.style.marginBottom = '25px';
                qDiv.style.padding = '15px';
                qDiv.style.backgroundColor = document.body.classList.contains('dark-mode') ? '#333' : '#f5f5f5';
                qDiv.style.borderLeft = '4px solid var(--text-color)';
                qDiv.style.borderRadius = '0 4px 4px 0';
                
                const label = document.createElement('label');
                label.style.display = 'block';
                label.style.fontWeight = 'bold';
                label.style.marginBottom = '10px';
                label.style.fontFamily = "'Cutive Mono', monospace";
                label.innerText = q.text;
                
                const checkboxContainer = document.createElement('div');
                checkboxContainer.style.background = '#fff';
                checkboxContainer.style.border = '1px solid #ccc';
                checkboxContainer.style.maxHeight = '150px';
                checkboxContainer.style.overflowY = 'auto';
                checkboxContainer.style.padding = '10px';
                checkboxContainer.style.marginBottom = '15px';
                if(document.body.classList.contains('dark-mode')) {
                    checkboxContainer.style.background = '#222';
                    checkboxContainer.style.borderColor = '#444';
                }

                evidenceOptions.forEach(opt => {
                    const row = document.createElement('div');
                    row.style.marginBottom = '5px';
                    const cb = document.createElement('input');
                    cb.type = 'checkbox';
                    cb.value = opt.id;
                    cb.id = `cb-${q.id}-${opt.id}`;
                    cb.className = `evidence-cb-${q.id}`;
                    
                    const cblabel = document.createElement('label');
                    cblabel.htmlFor = cb.id;
                    cblabel.innerText = ` ${opt.title}`;
                    cblabel.style.fontSize = '0.9rem';
                    
                    row.appendChild(cb);
                    row.appendChild(cblabel);
                    checkboxContainer.appendChild(row);
                });

                const textLabel = document.createElement('label');
                textLabel.innerText = "Rationale / Answer:";
                textLabel.style.display = "block";
                textLabel.style.marginBottom = "5px";
                textLabel.style.fontSize = "0.9rem";
                textLabel.style.fontWeight = "bold";

                const textArea = document.createElement('textarea');
                textArea.id = `text-${q.id}`;
                textArea.style.width = '100%';
                textArea.style.padding = '10px';
                textArea.style.fontFamily = 'inherit';
                textArea.style.fontSize = '1em';
                textArea.rows = 4;
                textArea.placeholder = "Explain how the evidence leads to your conclusion...";
                
                qDiv.appendChild(label);
                qDiv.appendChild(checkboxContainer);
                qDiv.appendChild(textLabel);
                qDiv.appendChild(textArea);
                container.appendChild(qDiv);
            });
        }

        function submitSolution() {
            let allCorrect = true;
            solveQuestions.forEach(q => {
                const checkboxes = document.querySelectorAll(`.evidence-cb-${q.id}`);
                const selected = Array.from(checkboxes).filter(cb => cb.checked).map(cb => cb.value);
                const qDiv = document.querySelector(`.evidence-cb-${q.id}`).parentElement.parentElement;
                
                const exactMatch = selected.length === q.requiredEvidence.length && 
                                   selected.every(v => q.requiredEvidence.includes(v));
                
                if (!exactMatch) {
                    allCorrect = false;
                    qDiv.style.borderColor = '#e74c3c';
                    qDiv.style.backgroundColor = 'rgba(231, 76, 60, 0.1)';
                } else {
                    qDiv.style.borderColor = '#2ecc71';
                    qDiv.style.backgroundColor = 'rgba(46, 204, 113, 0.1)';
                }
            });
            
            if (allCorrect) {
                document.getElementById('solve-case-page').style.display = 'none';
                document.getElementById('solve-results-page').style.display = 'block';
                renderResults();
            } else {
                alert("INCORRECT EVIDENCE.\\n\\nOne or more of your evidence selections are incorrect or missing required pieces. Review the highlighted fields. You must select the EXACT combinations of evidence required to prove the answers.");
            }
        }

        function renderResults() {
            const container = document.getElementById('results-container');
            container.innerHTML = '';
            solveQuestions.forEach(q => {
                const userText = document.getElementById(`text-${q.id}`).value.trim();
                
                const row = document.createElement('div');
                row.style.marginBottom = '25px';
                row.style.paddingBottom = '15px';
                row.style.borderBottom = '1px solid #ccc';
                
                row.innerHTML = `
                    <div style="font-weight: bold; font-size: 1.1rem; margin-bottom: 10px; color: var(--accent-color);">${q.text}</div>
                    <div style="background: rgba(0,0,0,0.05); padding: 10px; border-left: 3px solid #ccc; margin-bottom: 15px;">
                        <span style="font-weight: bold; font-size: 0.8rem; color: #555; display: block; margin-bottom: 5px;">YOUR RATIONALE:</span>
                        <em>${userText || "No rationale provided."}</em>
                    </div>
                    <div style="background: rgba(46, 204, 113, 0.1); padding: 10px; border-left: 3px solid #2ecc71;">
                        <span style="font-weight: bold; font-size: 0.8rem; color: #2ecc71; display: block; margin-bottom: 5px;">ACTUAL ANSWER:</span>
                        <strong>${q.actualAnswer}</strong>
                    </div>
                `;
                container.appendChild(row);
            });
        }

        function copyForAIGrading() {
            let text = "Please act as a detective evaluator and grade my deductions out of 100 based on the actual answers provided below.\\n\\n";
            solveQuestions.forEach((q, i) => {
                const userText = document.getElementById(`text-${q.id}`).value.trim() || 'No answer provided.';
                text += `Question ${i+1}: ${q.text}\\nUser Rationale: ${userText}\\nActual Answer: ${q.actualAnswer}\\n\\n`;
            });
            text += "Please provide brief feedback and a final percentage score out of 100.";
            
            navigator.clipboard.writeText(text).then(() => {
                alert("Copied! Paste this prompt into any AI chatbot (like ChatGPT, Claude, Gemini) to receive your grade.");
            }).catch(err => {
                alert("Failed to copy. Please manually copy the answers.");
            });
        }

        function finalizeMystery() {
            const score = document.getElementById('final-ai-score').value;
            if(!score || score < 0 || score > 100) {
                alert("Please enter a valid final score between 0 and 100.");
                return;
            }
            
            alert(`CASE CLOSED!\\n\\nFinal Score: ${score}%\\n\\nThe Official Case Resolution document is now unlocked.`);
            
            if (!unlockedDocs.includes('27_complete_solution_document')) {
                unlockedDocs.push('27_complete_solution_document');
                localStorage.setItem('unlockedDocs', JSON.stringify(unlockedDocs));
            }
            document.getElementById('solve-results-page').style.display = 'none';
            document.getElementById('doc-active-content').style.display = 'block';
            loadDocument('27_complete_solution_document');
        }
'''

old_js_regex = r'const solveQuestions = \[.*?\}\n        \}\n'
old_js_match = re.search(old_js_regex, html, re.DOTALL)

if old_js_match:
    html = html.replace(old_js_match.group(0), js_code + '\n')
else:
    print("Could not find Javascript block")

# Make sure origLoadDocument logic covers both solve and results pages:
orig_load_doc_regex = r'const origLoadDocument = loadDocument;\n        loadDocument = function\(id\) {\n            document\.getElementById\(\'solve-case-page\'\)\.style\.display = \'none\';\n            origLoadDocument\(id\);\n        };'
new_load_doc = '''const origLoadDocument = loadDocument;
        loadDocument = function(id) {
            document.getElementById('solve-case-page').style.display = 'none';
            document.getElementById('solve-results-page').style.display = 'none';
            origLoadDocument(id);
        };'''
if orig_load_doc_regex in html:
    html = re.sub(orig_load_doc_regex, new_load_doc, html)
else:
    # Use regular string replace if possible
    html = html.replace("document.getElementById('solve-case-page').style.display = 'none';", 
                        "document.getElementById('solve-case-page').style.display = 'none';\n            if(document.getElementById('solve-results-page')) document.getElementById('solve-results-page').style.display = 'none';")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated successfully")
