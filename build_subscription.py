# -*- coding: utf-8 -*-
"""Сборка subscription.html: стили, секция пирогов, корзина и скрипты берутся из index.html (один источник правды).
Добавляет: заставку с логотипом Марьи, кнопку «Order once» в шапку."""
import re

repo = '/home/hatch/workspace/marya-pies-repo/'
index = open(repo + 'index.html', encoding='utf-8').read()
old_sub = open(repo + 'subscription.html', encoding='utf-8').read()

css = re.search(r'<style>(.*?)</style>', index, re.S).group(1)
pies = index[index.index('<!-- PIES -->'):index.index('<!-- FAMILY NIGHT -->')].rstrip()
shop = index[index.index('<div id="pieModal"'):index.index('</aside>', index.index('<div id="pieModal"')) + len('</aside>')]
scripts = re.findall(r'<script>.*?</script>', index, re.S)
assert len(scripts) == 3, scripts
fn_script = re.search(r'<script>\ndocument\.getElementById\(\'fnForm\'\).*?</script>', old_sub, re.S).group(0)

FN_CSS = """
/* ---- Pie Club page ---- */
.fn-splash .hero-inner{padding:36px 0 32px; text-align:center}
.fn-splash .hero-logo{width:min(200px,50vw)}
.fn-splash .hero-tagline{font-size:clamp(27px,5.6vw,42px)}
.fn-hero{padding:40px 0 4px; text-align:center}
.fn-hero h1{font-size:clamp(38px,7.5vw,64px); line-height:1.05; margin:0 0 10px; color:var(--cherry); font-weight:400}
.fn-hero .lead{font-size:clamp(19px,3.4vw,26px); color:var(--ink); max-width:640px; margin:0 auto 12px}
.fn-hero .sub{font-size:16.5px; color:var(--ink-soft); max-width:600px; margin:0 auto}
.fn-price{display:flex; gap:10px; justify-content:center; flex-wrap:wrap; margin:26px 0 6px}
.fn-price span{background:var(--cream-2); border:1px solid var(--line); border-radius:999px; padding:9px 18px; font-size:15.5px; box-shadow:var(--shadow-card)}
.fn-price b{color:var(--cranberry)}
.fn-grid{display:grid; grid-template-columns:repeat(2,1fr); gap:18px; margin:34px 0}
@media(max-width:820px){.fn-grid{grid-template-columns:1fr}}
.fn-card{background:var(--cream-2); border:1px solid var(--line); border-radius:20px; padding:24px 22px; box-shadow:var(--shadow-card)}
.fn-card .ic{font-size:30px; margin-bottom:8px}
.fn-card h3{margin:0 0 6px; font-size:21px; color:var(--cherry); font-weight:400}
.fn-card p{margin:0; font-size:15.5px; color:var(--ink-soft)}
.fn-steps{display:grid; grid-template-columns:repeat(3,1fr); gap:18px; margin:10px 0 34px}
@media(max-width:820px){.fn-steps{grid-template-columns:1fr}}
.fn-step{text-align:center; padding:10px}
.fn-step .n{display:inline-flex; width:40px; height:40px; border-radius:50%; background:var(--cherry); color:var(--butter); align-items:center; justify-content:center; font-size:19px; margin-bottom:8px}
.fn-step h3{margin:0 0 4px; font-size:19px; color:var(--cherry); font-weight:400}
.fn-step p{margin:0; font-size:15px; color:var(--ink-soft)}
.fn-h{font-size:clamp(26px,4.5vw,36px); color:var(--cherry); font-weight:400; text-align:center; margin:38px 0 6px}
.fn-form{background:var(--cherry); color:var(--cream); border-radius:28px; padding:34px 28px; margin:20px 0 44px}
.fn-form h2{margin:0 0 4px; font-size:clamp(26px,4.5vw,34px); font-weight:400; color:#FFF6EC; text-align:center}
.fn-form .fp{text-align:center; color:#FFEEDD; opacity:.9; margin:0 0 20px; font-size:16px}
.fn-form form{display:grid; grid-template-columns:1fr 1fr; gap:12px; max-width:640px; margin:0 auto}
@media(max-width:640px){.fn-form form{grid-template-columns:1fr}}
.fn-form input,.fn-form textarea{width:100%; border:1px solid rgba(240,203,129,.35); background:#FFF9F1; border-radius:14px; padding:13px 15px; font-size:16px; color:var(--ink)}
.fn-form textarea{grid-column:1/-1}
.fn-form button{grid-column:1/-1; justify-self:center; min-width:min(320px,100%)}
.fn-ok{display:none; text-align:center; font-size:18px; color:var(--butter); padding:10px 0 2px}
.fn-note{text-align:center; color:#FFEEDD; opacity:.85; font-size:14.5px; margin:14px auto 0; max-width:520px}
.fn-faq{max-width:760px; margin:0 auto 10px}
.fn-faq div{border-top:1px solid var(--line); padding:14px 4px}
.fn-faq b{color:var(--cherry); font-size:16.5px}
.fn-faq p{margin:3px 0 0; color:var(--ink-soft); font-size:15.5px}
.fn-close{text-align:center; font-size:19px; color:var(--cherry); margin:36px 0 8px}
.fn-footer{background:var(--cherry-deep); color:#FFEEDD; padding:30px 0; margin-top:44px}
.fn-footer .footer-in{display:flex; gap:16px; align-items:center; justify-content:space-between; flex-wrap:wrap}
.fn-footer img{width:54px; height:auto}
.fn-footer a{color:var(--butter); text-decoration:none; font-weight:700}
"""

# клубные блоки из текущей страницы (между </section> hero и </main>) — вырезаем по маркерам из old_sub
def grab(start, end):
    return old_sub[old_sub.index(start):old_sub.index(end)]

hero_block = grab('<section class="fn-hero wrap">', '</section>') + '</section>'
# в hero_block убираем старую плашку-eyebrow (заставку добавили выше)
hero_block = re.sub(r'\s*<span class="fn-eyebrow">.*?</span>', '', hero_block)
cards_block = grab('<div class="fn-grid">', '</div>\n\n    <h2 class="fn-h">How it works</h2>') + '</div>'
steps_block = grab('<h2 class="fn-h">How it works</h2>', '<div class="fn-form" id="subscribe">')
form_block = grab('<div class="fn-form" id="subscribe">', '<h2 class="fn-h">Questions</h2>')
faq_block = grab('<h2 class="fn-h">Questions</h2>', '<p class="fn-close">')
faq_block += '<p class="fn-close">Happiness in the moment. Memories are forever.</p>\n    <p style="text-align:center; margin:0 0 10px"><a class="btn btn-cranberry" href="#pies">See all the pies</a></p>'

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<meta name="color-scheme" content="light" />
<link rel="icon" href="favicon.ico" sizes="any" />
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png" />
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png" />
<link rel="preload" href="fonts/Monomakh-Regular.ttf" as="font" type="font/ttf" crossorigin />
<title>Pie Club — Marya Pies</title>
<meta name="description" content="The Marya Pies Pie Club: every Friday two big pies — one savory, one sweet — baked in the morning and delivered to your door. $75/week, pause anytime. Pre-registration is open." />
<style>{css}</style>
<style>{FN_CSS}</style>
</head>
<body>
<header class="topbar">
  <div class="wrap topbar-inner">
    <a class="wordmark" href="index.html" aria-label="Marya Pies — home">MARYA PIES</a>
    <div class="menu-row">
      <nav class="nav" aria-label="Main">
        <a href="#pies">Pies</a>
        <a href="subscription.html">Pie Club</a>
        <a href="index.html#story">Our Story</a>
        <a href="index.html#find-us">Find Us</a>
      </nav>
      <div class="top-btns">
        <a class="btn btn-outline btn-small" href="index.html#pies">Order once</a>
        <a class="btn btn-butter btn-small" href="#subscribe">Join the club</a>
      </div>
    </div>
  </div>
</header>

<main id="top">
  <section class="hero fn-splash">
    <div class="wrap hero-inner">
      <span class="hero-eyebrow">Knightdale, North Carolina</span>
      <div class="hero-lockup">
        <span class="hero-logo-wrap"><img class="hero-logo" src="assets/girl-2.png" alt="Marya Pies logo — girl with a berry wreath biting a slice of cranberry pie" /></span>
        <h2 class="hero-tagline">Every pie tells a <em>fairy&nbsp;tale</em></h2>
      </div>
    </div>
  </section>

  {hero_block}

  <section class="wrap">
    {cards_block}
  </section>

{pies}

  <section class="wrap">
    {steps_block}
    {form_block}
    {faq_block}
  </section>
</main>

<footer class="fn-footer">
  <div class="wrap footer-in">
    <img src="assets/girl-2.png" alt="Marya Pies logo" />
    <span>Every pie tells a fairy tale</span>
    <a href="index.html">← Back to Marya Pies</a>
  </div>
</footer>

{shop}

{fn_script}
{scripts[0]}
{scripts[1]}
{scripts[2]}
</body>
</html>
"""
open(repo + 'subscription.html', 'w', encoding='utf-8').write(html)
print('subscription.html rebuilt:', len(html), 'bytes')
