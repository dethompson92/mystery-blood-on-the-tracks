const fs = require('fs');
const dataStr = fs.readFileSync('c:/Users/Devon Thompson/Downloads/Mystery 2B - Blood on the Tracks/data.js', 'utf8');

// Quick and dirty way to parse caseData from data.js
const scriptCode = dataStr + '\nmodule.exports = caseData;';
const tmpFile = 'c:/Users/Devon Thompson/Downloads/Mystery 2B - Blood on the Tracks/temp_parse_data.js';
fs.writeFileSync(tmpFile, scriptCode);

const caseData = require(tmpFile);

const doc06 = caseData.documents['06_photographer_witness_statement'];
const doc15 = caseData.documents['15_margaret_sinclair_detailed_statement'];

console.log('DOC 06 TITLE:', doc06.title);
console.log('DOC 06 BODY PREVIEW:', doc06.body.substring(0, 500));
console.log('');
console.log('DOC 15 TITLE:', doc15.title);
console.log('DOC 15 BODY PREVIEW:', doc15.body.substring(0, 500));

fs.unlinkSync(tmpFile);
