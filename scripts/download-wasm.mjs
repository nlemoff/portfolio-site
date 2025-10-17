import fs from 'fs';
import path from 'path';
import https from 'https';

const wasmDir = path.join(process.cwd(), 'public', 'wasm');
const dracoDir = path.join(wasmDir, 'draco');
const meshoptDir = path.join(wasmDir, 'meshopt');

const dracoFiles = [
  { url: 'https://www.gstatic.com/draco/versioned/decoders/1.5.7/draco_decoder.js', name: 'draco_decoder.js' },
  { url: 'https://www.gstatic.com/draco/versioned/decoders/1.5.7/draco_decoder.wasm', name: 'draco_decoder.wasm' },
  { url: 'https://www.gstatic.com/draco/versioned/decoders/1.5.7/draco_wasm_wrapper.js', name: 'draco_wasm_wrapper.js' },
];

const meshoptFiles = [
    { url: 'https://unpkg.com/meshoptimizer@0.20.0/meshopt_decoder.js', name: 'meshopt_decoder.js' },
    { url: 'https://unpkg.com/meshoptimizer@0.20.0/meshopt_decoder.wasm', name: 'meshopt_decoder.wasm' },
];


function downloadFile(url, dest) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(dest);
    https.get(url, (response) => {
      if (response.statusCode !== 200) {
        reject(new Error(`Failed to get '${url}' (${response.statusCode})`));
        return;
      }
      response.pipe(file);
      file.on('finish', () => {
        file.close(resolve);
      });
    }).on('error', (err) => {
      fs.unlink(dest, () => reject(err));
    });
  });
}

async function main() {
  console.log('Downloading WASM decoders...');

  if (!fs.existsSync(wasmDir)) fs.mkdirSync(wasmDir);
  if (!fs.existsSync(dracoDir)) fs.mkdirSync(dracoDir);
  if (!fs.existsSync(meshoptDir)) fs.mkdirSync(meshoptDir);

  try {
    console.log('Downloading Draco decoders...');
    for (const file of dracoFiles) {
      const dest = path.join(dracoDir, file.name);
      console.log(`  -> ${file.name}`);
      await downloadFile(file.url, dest);
    }

    console.log('Downloading Meshopt decoders...');
    for (const file of meshoptFiles) {
        const dest = path.join(meshoptDir, file.name);
        console.log(`  -> ${file.name}`);
        await downloadFile(file.url, dest);
      }

    console.log('WASM decoders downloaded successfully.');
  } catch (error) {
    console.error('Error downloading WASM decoders:', error);
    process.exit(1);
  }
}

main();
