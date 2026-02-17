const express = require('express');
const path = require('path');
const app = express();

// Try multiple possible build output paths
const possiblePaths = [
  path.join(process.cwd(), 'dist'),
  path.join(process.cwd(), 'dist/app/browser'),
  path.join(process.cwd(), 'dist/browser')
];

let DIST_FOLDER = possiblePaths.find(p => {
  try {
    return require('fs').existsSync(p);
  } catch {
    return false;
  }
}) || possiblePaths[0];

console.log(`Serving from: ${DIST_FOLDER}`);

// Serve static files from the build folder
app.use(express.static(DIST_FOLDER));

// Route all other requests to index.html (SPA support)
app.get('*', (req, res) => {
  res.sendFile(path.join(DIST_FOLDER, 'index.html'));
});

const port = process.env.PORT || 8080;
app.listen(port, () => {
  console.log(`✅ Server listening on port ${port}`);
  console.log(`📂 Serving files from: ${DIST_FOLDER}`);
});
