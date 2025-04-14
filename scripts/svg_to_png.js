// SVG to PNG converter using WebKit
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Input/output paths
const svgPath = path.join(__dirname, '..', 'docs', 'images', 'logo.svg');
const pngPath = path.join(__dirname, '..', 'docs', 'images', 'logo.png');

// Read SVG content
const svgContent = fs.readFileSync(svgPath, 'utf8');

// Create a temporary HTML file
const tempHtmlPath = path.join(__dirname, 'temp_convert.html');
const htmlContent = `
<!DOCTYPE html>
<html>
<head>
  <title>SVG to PNG Converter</title>
  <style>
    body { margin: 0; padding: 0; }
  </style>
</head>
<body>
  ${svgContent}
  <script>
    // This script will run in the browser
    setTimeout(() => {
      // Just a placeholder - conversion happens in wkhtmltoimage
      console.log('Rendering SVG...');
    }, 100);
  </script>
</body>
</html>
`;

fs.writeFileSync(tempHtmlPath, htmlContent);

// Use wkhtmltoimage if available
try {
  console.log('Converting SVG to PNG...');
  execSync(`wkhtmltoimage --enable-local-file-access --transparent --width 500 ${tempHtmlPath} ${pngPath}`);
  console.log(`PNG saved to ${pngPath}`);
} catch (error) {
  console.error('Error converting SVG to PNG:', error.message);
  console.log('Please install wkhtmltopdf (which includes wkhtmltoimage) or use another tool to convert the SVG file.');
}

// Clean up
fs.unlinkSync(tempHtmlPath);
