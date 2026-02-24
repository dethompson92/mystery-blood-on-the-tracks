import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add SOLVE CASE button
button_html = '''<button class="action-btn" onclick="showSolveCasePage()" style="background-color: var(--accent-color); color: white; border: none; font-weight: bold;">SOLVE CASE</button>
                <button class="action-btn" onclick="toggleNotes()">'''
html = html.replace('<button class="action-btn" onclick="toggleNotes()">', button_html)

# 2. Add Solve Case UI HTML inside #content-viewer
solve_case_html = '''
            <div id="solve-case-page" style="display: none; height: 100%; overflow-y: auto;">
                <div class="document-body">
                    <h1 style="font-family: 'Special Elite', cursive; color: var(--accent-color); text-align: center; font-size: 2.5rem; margin-top: 0;">SOLVE THE MYSTERY</h1>
                    <p style="text-align: center; font-size: 1.2rem; margin-bottom: 40px;">Select the most conclusive piece of evidence for each question to prove your deductions and officially close the case.</p>
                    
                    <div id="questions-container" style="max-width: 600px; margin: 0 auto;"></div>
                    
                    <div style="text-align: center; margin-top: 40px;">
                        <button onclick="submitSolution()" style="padding: 15px 40px; background-color: var(--accent-color); color: white; border: none; font-family: 'Special Elite', cursive; font-size: 1.3rem; cursor: pointer; border-radius: 4px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">SUBMIT FINDINGS</button>
                    </div>
                </div>
            </div>
'''
html = html.replace('<div id="doc-active-content" style="display: none;">', solve_case_html + '\n            <div id="doc-active-content" style="display: none;">')

# 3. Add solving logic to script
js_code = '''
        const solveQuestions = [
            { id: 'q1', text: '1. WHO is the killer?', allowedAnswers: ['20_charlotte_devereaux_confession_2024', '19_cold_case_review_memo_2024'] },
            { id: 'q2', text: '2. HOW did they escape the locked room?', allowedAnswers: ['20_charlotte_devereaux_confession_2024', '02_crime_scene_investigation_report'] },
            { id: 'q3', text: '3. WHY was Vivienne murdered? (Motive)', allowedAnswers: ['11_love_letters_evidence', '09_journal_entries_devereaux_1957', '20_charlotte_devereaux_confession_2024'] },
            { id: 'q4', text: '4. WHAT happened to the murder weapon?', allowedAnswers: ['08_trunk_discovery_report_2024', '07_dna_analysis_2024_cold_case'] },
            { id: 'q5', text: '5. WHO is the "mystery woman in burgundy"?', allowedAnswers: ['15_margaret_sinclair_detailed_statement', '20_charlotte_devereaux_confession_2024'] }
        ];

        function showSolveCasePage() {
            document.getElementById('landing-page').style.display = 'none';
            document.getElementById('doc-active-content').style.display = 'none';
            document.getElementById('solve-case-page').style.display = 'block';
            document.getElementById('breadcrumb').innerText = `CASE_FILES / SOLVE CASE`;
            currentDoc = null;
            
            if (window.innerWidth <= 768) {
                document.getElementById('sidebar').classList.remove('sidebar-open');
            }
            
            renderSolveDropdowns();
        }

        function renderSolveDropdowns() {
            const container = document.getElementById('questions-container');
            container.innerHTML = '';
            
            // Generate list of all available documents for the dropdowns
            let optionsHtml = '<option value="">-- Select Evidence --</option>';
            Object.keys(caseData.documents).forEach(id => {
                if(spoilerDocs.includes(id) && id !== '20_charlotte_devereaux_confession_2024' && id !== '19_cold_case_review_memo_2024' && id !== '07_dna_analysis_2024_cold_case' && id !== '08_trunk_discovery_report_2024') {
                    // Hide some endgame docs from selection except the crucial recent ones players might find or know about 
                    // Actually, let's include all non-solution spoiler docs
                    if(id === '27_complete_solution_document') return;
                }
                const doc = caseData.documents[id];
                optionsHtml += `<option value="${id}">${doc.shortTitle || doc.title}</option>`;
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
                
                const select = document.createElement('select');
                select.id = `select-${q.id}`;
                select.style.width = '100%';
                select.style.padding = '10px';
                select.style.fontFamily = 'inherit';
                select.style.fontSize = '1rem';
                select.style.borderRadius = '4px';
                select.style.border = '1px solid #ccc';
                select.innerHTML = optionsHtml;
                
                qDiv.appendChild(label);
                qDiv.appendChild(select);
                container.appendChild(qDiv);
            });
        }

        function submitSolution() {
            let allCorrect = true;
            solveQuestions.forEach(q => {
                const select = document.getElementById(`select-${q.id}`);
                const val = select.value;
                if (!val || !q.allowedAnswers.includes(val)) {
                    allCorrect = false;
                    select.style.borderColor = '#e74c3c';
                    select.style.backgroundColor = 'rgba(231, 76, 60, 0.1)';
                } else {
                    select.style.borderColor = '#2ecc71';
                    select.style.backgroundColor = 'rgba(46, 204, 113, 0.1)';
                }
            });
            
            if (allCorrect) {
                alert("CONGRATULATIONS DETECTIVE!\\n\\nYou have correctly assembled the evidence to solve the mystery. The Official Case Resolution document has been unlocked.");
                if (!unlockedDocs.includes('27_complete_solution_document')) {
                    unlockedDocs.push('27_complete_solution_document');
                    localStorage.setItem('unlockedDocs', JSON.stringify(unlockedDocs));
                }
                document.getElementById('solve-case-page').style.display = 'none';
                document.getElementById('doc-active-content').style.display = 'block';
                loadDocument('27_complete_solution_document');
            } else {
                alert("INCORRECT EVIDENCE.\\n\\nSome of your conclusions are entirely wrong or lack the most definitive evidence. Review the highlighted fields and reconsider your deductions.");
            }
        }
        
        // Override loadDocument slightly to hide solve page
        const origLoadDocument = loadDocument;
        loadDocument = function(id) {
            document.getElementById('solve-case-page').style.display = 'none';
            origLoadDocument(id);
        };
'''
html = html.replace('function startInvestigation() {', js_code + '\n        function startInvestigation() {')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Solve Case UI injected successfully.")
