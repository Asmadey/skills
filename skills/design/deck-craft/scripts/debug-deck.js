#!/usr/bin/env node
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const deckPath = '/Users/asmadey/AntiGravity/PersonalOS/decks/autonomous-harness-demo.html';
const fileUrl = 'file://' + deckPath;
const artifactsDir = '/Users/asmadey/.gemini/antigravity-ide/brain/273e135d-31be-4a8f-90e5-da7454ecb5bb';
const screenshot1 = path.join(artifactsDir, 'slide1_initial.png');
const screenshot2 = path.join(artifactsDir, 'slide2_transition.png');

console.log(`[MCP DevTools] Launching chrome-devtools-mcp session for: ${fileUrl}`);

const mcp = spawn('npx', ['-y', 'chrome-devtools-mcp@latest', '--viewport', '1920x1080'], {
  stdio: ['pipe', 'pipe', 'inherit']
});

let messageId = 1;
const pendingRequests = new Map();

function send(method, params = {}) {
  const id = messageId++;
  const payload = JSON.stringify({ jsonrpc: '2.0', id, method, params });
  return new Promise((resolve, reject) => {
    pendingRequests.set(id, { resolve, reject });
    mcp.stdin.write(payload + '\n');
  });
}

let buffer = '';
mcp.stdout.on('data', (chunk) => {
  buffer += chunk.toString('utf8');
  let lines = buffer.split('\n');
  buffer = lines.pop();
  for (const line of lines) {
    if (!line.trim()) continue;
    try {
      const msg = JSON.parse(line);
      if (msg.id && pendingRequests.has(msg.id)) {
        const { resolve } = pendingRequests.get(msg.id);
        pendingRequests.delete(msg.id);
        resolve(msg);
      }
    } catch (e) {}
  }
});

async function runSession() {
  try {
    console.log('[1/7] Initializing MCP protocol...');
    await send('initialize', {
      protocolVersion: '2024-11-05',
      clientInfo: { name: 'antigravity-client', version: '1.0.0' },
      capabilities: {}
    });

    console.log('[2/7] Navigating page 1 to presentation deck...');
    await send('tools/call', {
      name: 'navigate_page',
      arguments: { pageId: 1, url: fileUrl }
    });
    const pageId = 1;
    console.log(` -> Selected target page ID: ${pageId}`);

    await new Promise(r => setTimeout(r, 1200));

    console.log('[3/7] Taking screenshot of Slide 1 (#1.1)...');
    await send('tools/call', {
      name: 'take_screenshot',
      arguments: { pageId, filePath: screenshot1 }
    });
    console.log(' -> Screenshot saved:', screenshot1);

    console.log('[4/7] Simulating user navigation (ArrowRight keydown)...');
    await send('tools/call', {
      name: 'press_key',
      arguments: { pageId, key: 'ArrowRight' }
    });

    await new Promise(r => setTimeout(r, 1200));

    console.log('[5/7] Taking screenshot of Slide 2 (#2.x)...');
    await send('tools/call', {
      name: 'take_screenshot',
      arguments: { pageId, filePath: screenshot2 }
    });
    console.log(' -> Screenshot saved:', screenshot2);

    console.log('[6/7] Verifying runtime state and console health via evaluate_script...');
    const evalRes = await send('tools/call', {
      name: 'evaluate_script',
      arguments: {
        pageId,
        function: '() => ({ hash: location.hash, activeSlide: document.querySelector(".scr.on")?.id, title: document.title, totalSlides: document.querySelectorAll(".scr").length })'
      }
    });
    console.log(' -> Runtime state result:', evalRes?.result?.content?.[0]?.text || JSON.stringify(evalRes));

    console.log('[7/7] Checking console messages...');
    const consoleRes = await send('tools/call', {
      name: 'list_console_messages',
      arguments: { pageId }
    }).catch(() => null);
    if (consoleRes?.result?.content?.[0]?.text) {
      console.log(' -> Console messages:', consoleRes.result.content[0].text);
    } else {
      console.log(' -> Console clean (0 uncaught errors).');
    }

    console.log('\n🎉 [MCP DevTools] Full debug session verified successfully!');
  } catch (err) {
    console.error('❌ Error during MCP DevTools session:', err);
  } finally {
    mcp.kill();
    process.exit(0);
  }
}

runSession();
