const fs = require('fs');
const dataStr = fs.readFileSync('c:/Users/Devon Thompson/Downloads/Mystery 2B - Blood on the Tracks/data.js', 'utf8');

// Use a regex to extract just the document IDs (they all seem to start with a \" and follow the pattern \"00_...\" or \"01_...\": {)
const matches = dataStr.matchAll(/\"(\d{2}_[^\"]+)\"[\s]*:[\s]*\{/g);
for (const match of matches) {
    console.log(match[1]);
}
