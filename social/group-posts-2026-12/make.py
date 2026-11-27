import asyncio, html
from posts import POSTS
from playwright.async_api import async_playwright
T = """<html><body style="margin:0"><div style="width:1080px;height:1080px;box-sizing:border-box;padding:96px 90px;
background:radial-gradient(circle at 85% 15%,#2a1a12 0%,#0A0A0A 55%);color:#fff;font-family:Poppins;position:relative;overflow:hidden">
<div style="position:absolute;right:-120px;bottom:-120px;width:520px;height:520px;border:3px solid rgba(193,104,58,.25);border-radius:50%"></div>
<div style="font:600 26px Poppins;letter-spacing:6px;color:#C1683A;text-transform:uppercase">For kitchen &amp; joinery owners</div>
<div style="margin-top:70px;font:800 92px/1.05 Poppins;letter-spacing:-2px">{a}</div>
<div style="margin-top:14px;font:800 92px/1.05 Poppins;letter-spacing:-2px;color:#C1683A">{b}</div>
<div style="margin-top:46px;font:500 36px/1.4 Inter;color:#E8E2D9;max-width:860px">{c}</div>
<div style="position:absolute;left:90px;right:90px;bottom:80px;display:flex;justify-content:space-between;align-items:center;border-top:1px solid rgba(255,255,255,.18);padding-top:30px">
<div style="font:700 34px Poppins">AI Office <span style="color:#C1683A">Flow</span></div>
<div style="font:500 26px Inter;color:#B9B2A8">by MeasureFlow &middot; ecosystem.measureflow.com.au</div></div></div></body></html>"""
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width":1080,"height":1080})
        for i,(a,bb,c,_,slug) in enumerate(POSTS,1):
            await pg.set_content(T.format(a=html.escape(a),b=html.escape(bb),c=html.escape(c)))
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=f"{i:02d}-{slug}.png")
        await b.close()
asyncio.run(main())
