#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const PAPERS_DIR = path.join(__dirname, '../docs/papers');
const OUTPUT_FILE = path.join(__dirname, '../public/papers-data.json');

if (!fs.existsSync(path.dirname(OUTPUT_FILE))) {
  fs.mkdirSync(path.dirname(OUTPUT_FILE), { recursive: true });
}

const papers = [];

const files = fs.readdirSync(PAPERS_DIR)
  .filter((file) => file.startsWith('paper_') && file.endsWith('.md'))
  .sort();

files.forEach((filename) => {
  const filepath = path.join(PAPERS_DIR, filename);
  
  try {
    const content = fs.readFileSync(filepath, 'utf-8');
    const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---\n/);
    if (!frontmatterMatch) {
      console.warn(`⚠️  No frontmatter found in ${filename}`);
      return;
    }

    const frontmatterText = frontmatterMatch[1];
    const paperData = {};

    frontmatterText.split('\n').forEach((line) => {
      if (!line.includes(':')) return;
      
      const colonIndex = line.indexOf(':');
      const key = line.substring(0, colonIndex).trim();
      let value = line.substring(colonIndex + 1).trim();

      if (value.startsWith('"') && value.endsWith('"')) {
        value = value.slice(1, -1);
      }

      if (value.startsWith('[') && value.endsWith(']')) {
        value = value
          .slice(1, -1)
          .split(',')
          .map((v) => v.trim().replace(/^["']|["']$/g, ''))
          .filter((v) => v);
      }

      paperData[key] = value;
    });

    const docId = filename.replace('.md', '');

    papers.push({
      id: docId,
      title: paperData.title || 'Unknown',
      tags: Array.isArray(paperData.tags) ? paperData.tags : [],
    });

    console.log(`✓ ${docId}: ${(paperData.tags || []).length} tags`);
  } catch (error) {
    console.error(`✗ Error processing ${filename}:`, error.message);
  }
});

fs.writeFileSync(OUTPUT_FILE, JSON.stringify(papers, null, 2), 'utf-8');
console.log(`\n✓ Generated ${OUTPUT_FILE} with ${papers.length} papers`);
