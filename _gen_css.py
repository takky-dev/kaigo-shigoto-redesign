# -*- coding: utf-8 -*-
from _patterns import PATTERNS

def render_css(p):
    t = p["tokens"]
    root = "\n".join(f"  --{k}:{v};" for k, v in t.items())
    head_font = p["font_head"]
    body_font = p["font_body"]
    head_weight = p["head_weight"]

    css = f''':root{{
{root}
}}
*{{box-sizing:border-box;}}
.sr-only{{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:{body_font};line-height:1.75;-webkit-font-smoothing:antialiased;}}
h1,h2,h3{{font-family:{head_font};font-weight:{head_weight};text-wrap:balance;color:var(--ink);margin:0;letter-spacing:-.01em;}}
.mono{{font-family:"IBM Plex Mono",ui-monospace,monospace;font-variant-numeric:tabular-nums;}}
a{{color:inherit;}}
button{{font-family:inherit;}}
img,svg{{display:block;}}
.wrap{{max-width:1120px;margin:0 auto;padding:0 24px;}}
section{{padding:72px 0;}}
@media (max-width:720px){{section{{padding:48px 0;}}}}

header.site{{position:sticky;top:0;z-index:50;background:color-mix(in srgb, var(--bg) 90%, transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--line);}}
.header-row{{display:flex;align-items:center;justify-content:space-between;padding:14px 24px;max-width:1120px;margin:0 auto;}}
.brand{{display:flex;align-items:center;gap:10px;text-decoration:none;}}
.brand-mark{{width:38px;height:38px;border-radius:10px;background:var(--accent);display:flex;align-items:center;justify-content:center;flex:none;}}
.brand-name{{font-family:{head_font};font-weight:{head_weight};font-size:1.18rem;line-height:1;color:var(--ink);}}
.brand-tag{{font-size:0.68rem;color:var(--ink-soft);letter-spacing:.03em;margin-top:3px;display:block;font-weight:400;}}
nav.primary{{display:flex;align-items:center;gap:26px;}}
nav.primary a{{font-size:0.9rem;font-weight:500;text-decoration:none;color:var(--ink-soft);white-space:nowrap;}}
nav.primary a:hover{{color:var(--accent-strong);}}
.btn{{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:12px 22px;border-radius:999px;font-weight:700;font-size:0.88rem;text-decoration:none;border:1px solid transparent;cursor:pointer;white-space:nowrap;transition:transform .15s ease, box-shadow .15s ease, background .15s ease;}}
.btn:focus-visible{{outline:3px solid var(--accent-strong);outline-offset:2px;}}
.btn-warm{{background:var(--warm);color:var(--warm-ink);}}
.btn-warm:hover{{background:var(--warm-strong);}}
.btn-line{{border-color:var(--line-strong);color:var(--ink);background:transparent;}}
.btn-line:hover{{background:var(--surface-alt);}}
.header-cta{{display:flex;align-items:center;gap:14px;}}
.nav-toggle{{position:absolute;width:1px;height:1px;opacity:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);}}
.nav-toggle:focus-visible ~ .header-row .nav-burger{{outline:3px solid var(--accent-strong);outline-offset:3px;}}
.nav-burger{{display:none;flex-direction:column;gap:5px;width:34px;height:34px;align-items:center;justify-content:center;border-radius:8px;cursor:pointer;}}
.nav-burger span{{width:20px;height:2px;background:var(--ink);display:block;}}

/* hero: フルブリード写真タイプ（A・C） */
.hero{{padding:0;}}
.hero-photo{{position:relative;min-height:520px;display:flex;align-items:flex-end;background-size:cover;background-position:center;
  background-image:linear-gradient(0deg, rgba(10,14,20,0.86) 0%, rgba(10,14,20,0.30) 55%, rgba(10,14,20,0.06) 100%), url('../assets/img/{p["hero_photo"]}');}}
.hero-inner{{padding:56px 24px 48px;max-width:1120px;margin:0 auto;width:100%;}}
.hero-text{{max-width:600px;}}
.eyebrow{{display:inline-flex;align-items:center;gap:8px;font-size:0.76rem;font-weight:700;letter-spacing:.08em;color:#E7EEF4;background:rgba(10,14,20,0.55);padding:6px 14px;border-radius:999px;margin-bottom:20px;}}
.hero h1{{color:#fff;font-size:2.6rem;line-height:1.3;margin:0 0 16px;}}
.hero p.lead{{color:rgba(255,255,255,0.9);font-size:0.98rem;max-width:44ch;margin:0 0 28px;}}
.btnrow{{display:flex;gap:12px;flex-wrap:wrap;}}
.btn-hero-primary{{background:#fff;color:var(--accent-strong);font-weight:700;font-size:0.88rem;padding:13px 24px;border-radius:999px;white-space:nowrap;}}
.btn-hero-ghost{{border:1.5px solid rgba(255,255,255,0.7);color:#fff;font-weight:700;font-size:0.88rem;padding:12px 24px;border-radius:999px;white-space:nowrap;}}
.search-overlap{{margin-top:-56px;position:relative;z-index:5;}}
@media (max-width:720px){{.search-overlap{{margin-top:-40px;}}}}

/* hero: 2カラムグリッドタイプ（B） */
.hero-grid{{display:grid;grid-template-columns:1.05fr 0.95fr;gap:36px;align-items:center;padding:44px 0 0;}}
.hero-grid .check-list{{list-style:none;padding:0;margin:0 0 26px;display:flex;flex-direction:column;gap:10px;}}
.hero-grid .check-list li{{display:flex;align-items:center;gap:10px;font-size:0.92rem;font-weight:500;}}
.hero-grid .check-list svg{{color:var(--accent);flex:none;}}
.photo-wrap{{position:relative;}}
.photo-wrap .photo{{width:100%;aspect-ratio:4/5;border-radius:var(--radius-l);background-size:cover;background-position:center;box-shadow:0 28px 46px -22px rgba(60,40,20,0.35);}}
.float-badge{{position:absolute;background:#fff;border-radius:999px;padding:9px 18px;font-weight:700;font-size:0.8rem;box-shadow:0 12px 22px -10px rgba(0,0,0,0.25);}}
.float-badge.b1{{top:-14px;left:-14px;color:var(--warm-strong);}}
.float-badge.b2{{bottom:22px;right:-16px;color:var(--accent-strong);}}

.stat-strip{{display:flex;margin-top:22px;border-top:1px solid var(--line);padding-top:18px;}}
.stat-strip div{{flex:1;padding:0 16px;border-left:1px solid var(--line);}}
.stat-strip div:first-child{{border-left:none;padding-left:0;}}
.stat-num{{font-size:1.4rem;font-weight:900;color:var(--accent-strong);}}
.stat-label{{font-size:0.72rem;color:var(--ink-soft);margin-top:2px;font-weight:400;}}
@media (max-width:720px){{
  .stat-strip{{flex-wrap:nowrap;}}
  .stat-strip div{{flex:1 1 0;min-width:0;padding:0 6px;}}
  .stat-strip div:first-child{{padding-left:0;}}
  .stat-num{{font-size:1.05rem;}}
  .stat-label{{font-size:0.62rem;}}
}}

/* search */
.search-card{{margin-top:0;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius-l);padding:20px;box-shadow:var(--shadow);}}
.search-row{{display:grid;grid-template-columns:1.4fr 1fr 1fr auto;gap:10px;}}
.field{{display:flex;flex-direction:column;gap:6px;}}
.field label{{font-size:0.7rem;color:var(--ink-soft);font-weight:700;letter-spacing:.03em;}}
.field input,.field select{{border:1px solid var(--line);border-radius:var(--radius-s);padding:11px 12px;background:var(--surface-alt);color:var(--ink);font-size:0.92rem;font-family:inherit;}}
.field input:focus,.field select:focus{{outline:2px solid var(--accent);outline-offset:1px;}}
.search-btn{{background:var(--accent);color:var(--accent-ink);border:none;border-radius:var(--radius-s);padding:0 22px;font-weight:700;font-size:0.94rem;cursor:pointer;align-self:end;height:44px;white-space:nowrap;}}
.search-btn:hover{{background:var(--accent-strong);}}
@media (max-width:720px){{
  .search-row{{grid-template-columns:1fr;}}
  .search-btn{{height:46px;width:100%;}}
}}

/* section head */
.section-head{{display:flex;align-items:flex-end;justify-content:space-between;gap:20px;margin-bottom:32px;flex-wrap:wrap;}}
.section-head h1,.section-head h2{{font-size:1.6rem;}}
.section-head .kicker{{font-size:0.74rem;font-weight:700;letter-spacing:.1em;color:var(--accent-strong);margin-bottom:8px;display:block;}}
.section-head .see-all{{font-size:0.86rem;font-weight:700;color:var(--accent-strong);text-decoration:none;white-space:nowrap;}}
.alt{{background:var(--surface-alt);}}

/* categories */
.cat-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;}}
.cat-card{{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius-m);padding:18px 12px;text-align:center;text-decoration:none;color:var(--ink);transition:transform .15s ease, box-shadow .15s ease, border-color .15s ease;}}
.cat-card:hover{{transform:translateY(-3px);box-shadow:var(--shadow);border-color:var(--accent);}}
.cat-icon{{width:48px;height:48px;margin:0 auto 12px;border-radius:12px;background:var(--accent-tint);display:flex;align-items:center;justify-content:center;color:var(--accent-strong);overflow:hidden;background-size:cover;background-position:center;}}
.cat-card .name{{font-size:0.84rem;font-weight:700;}}
.cat-card .count{{font-size:0.7rem;color:var(--ink-soft);margin-top:4px;}}
@media (max-width:720px){{.cat-grid{{grid-template-columns:repeat(2,1fr);}}}}

/* jobs */
.listing-note{{font-size:0.76rem;color:var(--ink-soft);margin-top:-14px;margin-bottom:28px;}}
.job-grid{{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--line);border:1px solid var(--line);border-radius:var(--radius-m);overflow:hidden;}}
.job-card{{background:var(--surface);padding:22px;display:flex;flex-direction:column;gap:14px;}}
.job-photo{{aspect-ratio:16/9;border-radius:var(--radius-s);background-size:cover;background-position:center;}}
.job-top{{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;}}
.job-facility{{font-size:0.76rem;color:var(--ink-soft);}}
.job-title{{font-size:1.04rem;font-weight:700;margin-top:3px;}}
.job-salary{{font-family:"IBM Plex Mono";font-weight:600;color:var(--accent-strong);font-size:0.92rem;white-space:nowrap;}}
.badge-row{{display:flex;gap:8px;flex-wrap:wrap;}}
.badge{{background:var(--badge-bg);color:var(--badge-ink);font-size:0.7rem;font-weight:700;padding:4px 10px;border-radius:4px;}}
.badge.warm{{background:color-mix(in srgb, var(--warm) 18%, var(--surface));color:var(--warm-strong);}}
.spec-list{{display:grid;grid-template-columns:1fr 1fr;gap:6px 16px;font-size:0.8rem;color:var(--ink-soft);border-top:1px solid var(--line);padding-top:12px;}}
.spec-list dt{{font-weight:700;color:var(--ink);display:inline;}}
.spec-list div{{display:flex;gap:6px;}}
.tag-row{{display:flex;flex-wrap:wrap;gap:6px;}}
.tag{{font-size:0.7rem;color:var(--ink-soft);border:1px solid var(--line);padding:3px 9px;border-radius:4px;}}
.job-cta{{align-self:flex-start;font-size:0.82rem;font-weight:700;color:var(--accent-strong);text-decoration:none;margin-top:2px;}}
.job-cta:hover{{text-decoration:underline;}}
@media (max-width:720px){{.job-grid{{grid-template-columns:1fr;}}}}
@media (max-width:480px){{.spec-list{{grid-template-columns:1fr;}}}}

.chip-wrap{{display:flex;flex-wrap:wrap;gap:10px;}}
.chip{{background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:9px 16px;font-size:0.84rem;text-decoration:none;color:var(--ink);transition:border-color .15s ease, color .15s ease;}}
.chip:hover{{border-color:var(--accent);color:var(--accent-strong);}}

/* why */
.why-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;}}
.why-card{{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius-m);padding:26px;}}
.why-num{{font-family:"IBM Plex Mono";font-size:0.82rem;font-weight:700;color:var(--accent-strong);margin-bottom:10px;}}
.why-card h3{{font-size:1.02rem;margin-bottom:10px;}}
.why-card p{{font-size:0.86rem;color:var(--ink-soft);}}
.why-card ul{{list-style:none;padding:0;margin:14px 0 0;display:flex;flex-direction:column;gap:7px;}}
.why-card ul li{{font-size:0.82rem;color:var(--ink-soft);display:flex;gap:8px;line-height:1.5;}}
.why-card ul li::before{{content:"›";color:var(--accent);font-weight:700;flex:none;}}
@media (max-width:960px){{.why-grid{{grid-template-columns:1fr;}}}}

/* faq */
.faq-list{{display:flex;flex-direction:column;gap:14px;max-width:760px;}}
.faq-item{{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius-m);padding:18px 22px;}}
.faq-q{{font-weight:700;font-size:0.92rem;display:flex;gap:10px;margin:0 0 8px;}}
.faq-q .qmark{{color:var(--accent-strong);flex:none;font-family:"IBM Plex Mono";}}
.faq-a{{font-size:0.86rem;color:var(--ink-soft);padding-left:26px;margin:0;line-height:1.7;}}
.faq-a .amark{{color:var(--warm-strong);font-family:"IBM Plex Mono";margin-right:8px;}}

/* testimonial（B・Cのみ使用） */
.testi-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;}}
.testi-card{{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius-m);padding:22px;display:flex;flex-direction:column;gap:12px;}}
.testi-top{{display:flex;justify-content:space-between;align-items:center;}}
.testi-meta{{font-size:0.76rem;color:var(--ink-soft);}}
.testi-stars{{color:var(--warm-strong);font-size:0.86rem;letter-spacing:1px;}}
.testi-change{{font-size:0.76rem;color:var(--ink-soft);display:flex;align-items:center;gap:6px;flex-wrap:wrap;}}
.testi-change b{{color:var(--ink);font-weight:700;}}
.testi-body{{font-size:0.86rem;color:var(--ink);line-height:1.8;}}
@media (max-width:960px){{.testi-grid{{grid-template-columns:1fr;}}}}

/* cta band */
.cta-band{{background:var(--accent);color:#fff;border-radius:var(--radius-l);padding:40px 44px;display:flex;justify-content:space-between;align-items:center;gap:24px;flex-wrap:wrap;}}
.cta-band h2{{color:#fff;font-size:1.4rem;margin-bottom:8px;}}
.cta-band p{{color:rgba(255,255,255,0.85);font-size:0.9rem;margin:0;}}
@media (max-width:720px){{.cta-band{{padding:30px 22px;flex-direction:column;align-items:flex-start;}}}}

/* footer */
footer{{border-top:1px solid var(--line);padding:56px 0 28px;}}
.foot-grid{{display:grid;grid-template-columns:1.3fr repeat(3,1fr);gap:32px;max-width:1120px;margin:0 auto;padding:0 24px;}}
.foot-grid h4{{font-size:0.82rem;margin-bottom:14px;}}
.foot-grid ul{{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:9px;}}
.foot-grid a{{font-size:0.84rem;color:var(--ink-soft);text-decoration:none;}}
.foot-grid a:hover{{color:var(--accent-strong);}}
.foot-bottom{{margin-top:36px;padding-top:20px;border-top:1px solid var(--line);font-size:0.78rem;color:var(--ink-soft);display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px;}}
@media (max-width:960px){{.foot-grid{{grid-template-columns:1fr 1fr;}}}}
@media (max-width:720px){{.foot-grid{{grid-template-columns:1fr 1fr;gap:24px;}}}}

.mobile-cta{{display:none;}}
@media (max-width:720px){{
  .mobile-cta{{display:flex;position:fixed;bottom:0;left:0;right:0;z-index:60;background:var(--surface);border-top:1px solid var(--line);padding:10px 16px calc(10px + env(safe-area-inset-bottom));gap:10px;box-shadow:0 -10px 24px -18px rgba(0,0,0,0.35);}}
  .mobile-cta .btn{{flex:1;padding:13px 10px;}}
  body{{padding-bottom:74px;}}
  .header-cta .btn-line{{display:none;}}
  .hero h1{{font-size:1.9rem;}}
  .hero-photo{{min-height:440px;}}
  .btnrow{{flex-direction:column;align-items:stretch;}}
  .btn-hero-primary,.btn-hero-ghost{{text-align:center;}}
  .hero p.lead{{max-width:none;}}
  .hero-grid{{grid-template-columns:1fr;gap:28px;}}
}}
@media (max-width:1040px){{
  nav.primary{{position:fixed;top:0;right:0;height:100%;width:min(78vw,320px);background:var(--surface);border-left:1px solid var(--line);flex-direction:column;align-items:flex-start;gap:2px;padding:80px 24px 24px;transform:translateX(100%);transition:transform .25s ease;z-index:40;}}
  nav.primary a{{padding:12px 0;width:100%;border-bottom:1px solid var(--line);white-space:normal;}}
  .nav-toggle:checked ~ .header-row nav.primary{{transform:translateX(0);}}
  .nav-burger{{display:flex;}}
}}

/* ===== job list / detail / apply ===== */
.breadcrumb{{font-size:0.82rem;color:var(--ink-soft);margin-bottom:22px;}}
.breadcrumb a{{color:var(--ink-soft);text-decoration:none;}}
.breadcrumb a:hover{{color:var(--accent-strong);}}

.filter-card{{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius-m);padding:22px;margin-bottom:28px;}}
.filter-row{{display:grid;grid-template-columns:1.4fr 1fr 1fr auto;gap:10px;margin-bottom:20px;}}
.filter-group{{margin-bottom:16px;}}
.filter-group .label{{font-size:0.78rem;font-weight:700;color:var(--ink-soft);margin-bottom:8px;}}
.check-grid{{display:flex;flex-wrap:wrap;gap:8px;}}
.check-pill{{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);border-radius:999px;padding:7px 14px;font-size:0.82rem;cursor:pointer;}}
.check-pill:has(input:checked){{background:var(--accent-tint);border-color:var(--accent);color:var(--accent-strong);font-weight:700;}}
.result-head{{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:10px;}}
.result-count{{font-size:0.9rem;}}
.sort-select{{border:1px solid var(--line);border-radius:var(--radius-s);padding:8px 12px;font-size:0.84rem;font-family:inherit;background:var(--surface);}}
.pagination{{display:flex;gap:8px;justify-content:center;margin-top:32px;}}
.pagination a,.pagination span.current,.page-inactive{{display:inline-flex;align-items:center;justify-content:center;min-width:38px;height:38px;padding:0 10px;border:1px solid var(--line);border-radius:var(--radius-s);font-size:0.86rem;text-decoration:none;color:var(--ink);}}
.pagination span.current{{background:var(--accent);color:#fff;border-color:var(--accent);}}
.page-inactive{{color:var(--ink-soft);opacity:.45;cursor:default;}}

.job-hero{{aspect-ratio:21/9;border-radius:var(--radius-l);background-size:cover;background-position:center;margin-bottom:24px;}}
.job-detail-title{{font-size:1.6rem;margin-bottom:14px;}}
.highlight-box{{background:var(--accent-tint);border-radius:var(--radius-m);padding:18px 22px;font-size:0.9rem;color:var(--ink);margin-bottom:22px;}}
.detail-ctarow{{display:flex;gap:12px;margin-bottom:8px;}}
.detail-ctarow .btn{{flex:1;}}
.disclaimer{{font-size:0.76rem;color:var(--ink-soft);margin-bottom:32px;}}
.spec-table{{width:100%;border-collapse:collapse;margin-bottom:28px;}}
.spec-table th,.spec-table td{{text-align:left;padding:12px 14px;border-bottom:1px solid var(--line);font-size:0.88rem;vertical-align:top;}}
.spec-table th{{width:30%;color:var(--ink-soft);font-weight:700;background:var(--surface-alt);}}
.spec-section-title{{font-size:1.05rem;font-weight:700;margin:0 0 14px;}}
.related-title{{font-size:1.1rem;font-weight:700;margin:40px 0 18px;}}
.sticky-apply{{display:none;}}
@media (max-width:720px){{
  .sticky-apply{{display:flex;position:fixed;bottom:0;left:0;right:0;z-index:60;background:var(--surface);border-top:1px solid var(--line);padding:10px 16px calc(10px + env(safe-area-inset-bottom));gap:10px;box-shadow:0 -10px 24px -18px rgba(0,0,0,0.35);}}
  .sticky-apply .btn{{flex:1;padding:13px 10px;}}
  body{{padding-bottom:74px;}}
}}

.apply-form{{display:flex;flex-direction:column;gap:16px;max-width:560px;}}
.apply-form label{{font-size:0.84rem;font-weight:700;margin-bottom:6px;display:block;}}
.apply-form input,.apply-form select,.apply-form textarea{{width:100%;border:1px solid var(--line);border-radius:var(--radius-s);padding:11px 12px;font-size:0.92rem;font-family:inherit;background:var(--surface);}}
.required{{color:var(--warm-strong);margin-left:4px;}}
.apply-note{{font-size:0.78rem;color:var(--ink-soft);margin-top:20px;}}

/* ===== 応募ウィザード ===== */
.wizard-wrap{{display:grid;grid-template-columns:1.3fr 1fr;gap:32px;align-items:start;}}
.wizard-back{{background:none;border:none;color:var(--ink-soft);font-size:0.86rem;cursor:pointer;padding:0;margin-bottom:18px;}}
.step-indicator{{display:flex;align-items:center;margin-bottom:32px;}}
.step-dot{{width:28px;height:28px;border-radius:50%;background:var(--surface-alt);color:var(--ink-soft);display:flex;align-items:center;justify-content:center;font-size:0.78rem;font-weight:700;flex:none;border:2px solid var(--line);}}
.step-dot.current{{background:var(--accent);color:#fff;border-color:var(--accent);}}
.step-dot.done{{background:var(--accent-strong);color:#fff;border-color:var(--accent-strong);}}
.step-line{{flex:1;height:2px;background:var(--line);}}
.step-line.done{{background:var(--accent-strong);}}
.wizard-step{{display:none;}}
.wizard-step.active{{display:block;}}
.wizard-q{{font-size:1.1rem;font-weight:700;margin-bottom:20px;}}
.tile-grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:26px;}}
.tile{{border:1.5px solid var(--line);border-radius:var(--radius-m);padding:16px;text-align:center;font-size:0.92rem;font-weight:600;cursor:pointer;transition:border-color .15s,background .15s;}}
.tile.selected{{border-color:var(--accent);background:var(--accent-tint);color:var(--accent-strong);}}
.wizard-field{{margin-bottom:20px;}}
.wizard-field label{{font-size:0.84rem;font-weight:700;margin-bottom:8px;display:block;}}
.wizard-field input,.wizard-field select{{width:100%;border:1px solid var(--line);border-radius:var(--radius-s);padding:12px 14px;font-size:0.94rem;font-family:inherit;background:var(--bg);color:var(--ink);}}
.wizard-next{{width:100%;background:var(--accent);color:#fff;border:none;border-radius:var(--radius-m);padding:18px;font-weight:700;font-size:0.98rem;cursor:pointer;text-align:center;line-height:1.4;}}
.wizard-next:hover{{background:var(--accent-strong);}}
.wizard-next .sub{{display:block;font-size:0.76rem;font-weight:500;opacity:.85;margin-bottom:3px;}}
.wizard-final{{background:var(--warm);}}
.wizard-final:hover{{background:var(--warm-strong);}}
.job-summary-card{{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius-m);padding:22px;position:sticky;top:88px;}}
.job-summary-card h4{{font-size:0.76rem;color:var(--ink-soft);text-align:center;margin:0 0 16px;font-weight:700;letter-spacing:.04em;}}
.job-summary-photo{{aspect-ratio:16/9;border-radius:var(--radius-s);background-size:cover;background-position:center;margin-bottom:14px;}}
.job-summary-card .title{{font-weight:700;font-size:1.02rem;margin-bottom:4px;}}
.job-summary-card .facility{{font-size:0.84rem;color:var(--ink-soft);margin-bottom:14px;}}
.job-summary-card .meta{{display:flex;flex-direction:column;gap:8px;font-size:0.82rem;color:var(--ink-soft);border-top:1px solid var(--line);padding-top:14px;}}
.job-summary-card .meta span{{color:var(--ink);font-weight:600;}}
.wizard-done{{text-align:center;padding:40px 20px;}}
.wizard-done .check-circle{{width:64px;height:64px;border-radius:50%;background:var(--accent);color:#fff;display:flex;align-items:center;justify-content:center;margin:0 auto 20px;}}
@media (max-width:860px){{
  .wizard-wrap{{grid-template-columns:1fr;}}
  .job-summary-card{{position:static;}}
}}

/* ===== info page（about/faq/terms/privacy/column） ===== */
.info-page h1,.info-page h2{{font-size:1.6rem;margin-bottom:8px;}}
.info-page .lead{{color:var(--ink-soft);font-size:0.95rem;margin-bottom:36px;max-width:64ch;}}
.info-section{{margin-bottom:36px;}}
.info-section h3{{font-size:1.05rem;margin-bottom:12px;}}
.info-section p{{font-size:0.92rem;color:var(--ink-soft);max-width:70ch;margin-bottom:10px;}}
.info-section ul{{margin:0 0 10px;padding-left:20px;font-size:0.9rem;color:var(--ink-soft);}}
.info-section ul li{{margin-bottom:6px;}}
.contact-form{{display:flex;flex-direction:column;gap:16px;max-width:560px;}}
.contact-form label{{font-size:0.84rem;font-weight:700;margin-bottom:6px;display:block;}}
.contact-form input,.contact-form select,.contact-form textarea{{width:100%;border:1px solid var(--line);border-radius:var(--radius-s);padding:11px 12px;font-size:0.92rem;font-family:inherit;background:var(--surface);}}

/* ===== コラム ===== */
.mag-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;}}
.mag-card{{display:block;text-decoration:none;color:inherit;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius-m);overflow:hidden;transition:border-color .15s ease,transform .15s ease;}}
.mag-card:hover{{border-color:var(--accent);transform:translateY(-2px);}}
.mag-thumb{{aspect-ratio:16/9;background:var(--accent-tint);display:flex;align-items:center;justify-content:center;color:var(--accent-strong);}}
.mag-body{{padding:16px 18px 20px;}}
.mag-cat{{font-size:0.72rem;font-weight:700;color:var(--accent-strong);}}
.mag-title{{font-size:0.95rem;font-weight:700;margin:6px 0 8px;line-height:1.55;}}
.mag-excerpt{{font-size:0.82rem;color:var(--ink-soft);line-height:1.7;margin:0;}}
@media (max-width:720px){{.mag-grid{{grid-template-columns:1fr;}}}}
.col-hero{{aspect-ratio:21/9;border-radius:var(--radius-l);background:var(--accent-tint);color:var(--accent-strong);display:flex;align-items:center;justify-content:center;margin-bottom:28px;}}
.col-meta{{display:flex;gap:12px;align-items:center;font-size:0.8rem;color:var(--ink-soft);margin-bottom:10px;}}
.col-body h3{{font-size:1.08rem;margin:32px 0 12px;}}
.col-body p{{font-size:0.94rem;color:var(--ink-soft);line-height:1.9;max-width:70ch;margin-bottom:14px;}}
.col-cta{{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius-m);padding:22px 26px;margin-top:36px;display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap;}}
.col-cta p{{margin:0;font-size:0.9rem;color:var(--ink-soft);}}

@media (prefers-reduced-motion: reduce){{*{{transition:none !important;}}}}
'''
    return css

if __name__ == "__main__":
    import os
    for key, p in PATTERNS.items():
        os.makedirs(key, exist_ok=True)
        with open(os.path.join(key, "style.css"), "w", encoding="utf-8") as f:
            f.write(render_css(p))
        print("wrote", key, "style.css")
