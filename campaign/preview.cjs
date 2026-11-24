// Phone-width PNG of one email for sign-off: node campaign/preview.cjs campaign/emails/<file>.html out.png
// Uses the repo's own copies of the email images (the workspace can't reach outside websites, so the
// company logo shows as its name here; in the real email it loads from the company's website).
const { chromium, devices } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const [src, out] = process.argv.slice(2);
  const pub = 'file://' + path.resolve(__dirname, '../web/public/email');
  let h = fs.readFileSync(src, 'utf8').replaceAll('https://officeflow.measureflow.com.au/email', pub);
  h = h.replace(/<td class="lg"[\s\S]*?<\/table><\/td>/, m => { const alt = (m.match(/alt="([^"]*)"/) || [])[1] || '';
    return `<td class="lg" align="right" style="padding:0"><span style="display:inline-block;background:#fff;border-radius:10px;padding:10px 14px;font:600 14px Arial;color:#0A0A0A">${alt}</span></td>`; });
  const tmp = path.join(require('os').tmpdir(), 'aof-preview.html'); fs.writeFileSync(tmp, h);
  const b = await chromium.launch(); const c = await b.newContext({ ...devices['iPhone 13'] }); const p = await c.newPage();
  await p.goto('file://' + tmp); await p.waitForTimeout(1500); await p.screenshot({ path: out, fullPage: true }); await b.close();
})();
