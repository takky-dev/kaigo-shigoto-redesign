# -*- coding: utf-8 -*-
import os, re
from _patterns import PATTERNS
from _data import (BRAND_JA, TAGLINE, CATEGORIES, TOTAL_JOBS, TOTAL_COMPANIES, TODAY_NEW,
                    JOBS, JOBS_BY_ID, job_file, apply_file, CONDITION_CHIPS, AREA_CHIPS,
                    FAQ, COLUMNS, TESTIMONIALS)

CHECK_SVG = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M20 6 9 17l-5-5"/></svg>'

def nav_links(active=None):
    items = [("list.html", "求人を探す"), ("column.html", "コラム"), ("faq.html", "よくある質問"),
             ("about.html", "サイトについて"), ("contact-company.html", "掲載のお問い合わせ")]
    return "\n      ".join(f'<a href="{href}">{label}</a>' for href, label in items)

def header_html(p):
    brand = p["brand_display"]
    return f'''<header class="site">
  <input type="checkbox" id="navToggle" class="nav-toggle">
  <div class="header-row">
    <a href="index.html" class="brand">
      <span class="brand-mark"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-4.35-9.5-8.5C.7 9 2 5.5 5.5 5c2-.3 3.5 1 4.5 2.3C11 6 12.5 4.7 14.5 5c3.5.5 4.8 4 3 7.5C15 16.65 12 21 12 21z"/></svg></span>
      <span><span class="brand-name">{brand}</span><span class="brand-tag">{TAGLINE}</span></span>
    </a>
    <nav class="primary">
      {nav_links()}
    </nav>
    <div class="header-cta">
      <label for="navToggle" class="nav-burger" aria-label="メニューを開く"><span></span><span></span><span></span></label>
    </div>
  </div>
</header>'''

def footer_html(p):
    brand = p["brand_display"]
    return f'''<footer>
  <div class="wrap foot-grid">
    <div>
      <div class="brand" style="margin-bottom:10px;"><span class="brand-mark" style="width:32px;height:32px;"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-4.35-9.5-8.5C.7 9 2 5.5 5.5 5c2-.3 3.5 1 4.5 2.3C11 6 12.5 4.7 14.5 5c3.5.5 4.8 4 3 7.5C15 16.65 12 21 12 21z"/></svg></span><span class="brand-name" style="font-size:1.05rem;">{brand}</span></div>
      <p style="font-size:0.82rem;color:var(--ink-soft);max-width:32ch;">介護施設で働く人のための求人サイト。経験を、いちばん活きる現場へ。</p>
    </div>
    <div><h4>求人を探す</h4><ul><li><a href="list.html">特別養護老人ホーム</a></li><li><a href="list.html">介護老人保健施設</a></li><li><a href="list.html">デイサービス</a></li><li><a href="list.html">訪問介護</a></li></ul></div>
    <div><h4>サイトについて</h4><ul><li><a href="about.html">{brand}とは</a></li><li><a href="column.html">コラム</a></li><li><a href="faq.html">よくある質問</a></li><li><a href="index.html#why">選ばれる理由</a></li></ul></div>
    <div><h4>企業の方へ</h4><ul><li><a href="contact-company.html">掲載のお問い合わせ</a></li><li><a href="terms.html">利用規約</a></li><li><a href="privacy.html">プライバシーポリシー</a></li></ul></div>
  </div>
  <div class="wrap foot-bottom"><span>© 2026 {brand}</span><span>{TAGLINE}</span></div>
</footer>'''

def mobile_cta_html():
    return '''<div class="mobile-cta">
  <a href="list.html" class="btn btn-warm" style="width:100%;">求人を探す</a>
</div>'''

def page_head(p, title, description):
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{p["font_link"]}">
<link rel="stylesheet" href="style.css">
</head>
<body>
'''

def page_wrap(head, body):
    return head + body + "\n</body>\n</html>\n"

# ---------- 部品 ----------

def job_card_html(job, related=False):
    if related:
        return f'''<div class="job-card">
          <div class="job-photo" style="background-image:url('../assets/img/{job["photo"]}')"></div>
          <div class="job-top"><div><div class="job-facility">{job["facility"]}</div><div class="job-title">{job["title"]}</div></div><div class="job-salary">{job["salary"]}</div></div>
          <div class="badge-row"><span class="badge">{job["badges"][0][0]}</span><span class="badge warm">{job["badges"][1][0]}</span></div>
          <a href="{job_file(job["id"])}" class="job-cta">求人の詳細を見る →</a>
        </div>'''
    spec = "".join(f'<div><dt>{k}</dt><span>{v}</span></div>' for k, v in job["spec"])
    tags = "".join(f'<span class="tag">{t}</span>' for t in job["tags"])
    return f'''<div class="job-card">
          <div class="job-photo" style="background-image:url('../assets/img/{job["photo"]}')"></div>
          <div class="job-top"><div><div class="job-facility">{job["facility"]}</div><div class="job-title">{job["title"]}</div></div><div class="job-salary">{job["salary"]}</div></div>
          <div class="badge-row"><span class="badge">{job["badges"][0][0]}</span><span class="badge warm">{job["badges"][1][0]}</span></div>
          <div class="spec-list">{spec}</div>
          <div class="tag-row">{tags}</div>
          <a href="{job_file(job["id"])}" class="job-cta">求人の詳細を見る →</a>
        </div>'''

def categories_html():
    cards = []
    for name, photo, count in CATEGORIES:
        cards.append(f'''        <a href="list.html" class="cat-card"><span class="cat-icon" style="background-image:url('../assets/img/{photo}')"></span><div class="name">{name}</div><div class="count">{count:,}件</div></a>''')
    return "\n".join(cards)

def testimonial_html():
    cards = []
    for t in TESTIMONIALS:
        stars = "★" * t["rating"] + "☆" * (5 - t["rating"])
        cards.append(f'''        <div class="testi-card">
          <div class="testi-top"><span class="testi-meta">{t["pref"]}・{t["age"]}</span><span class="testi-stars">{stars}</span></div>
          <div class="testi-change">転職前：<b>{t["before"]}</b> → 転職後：<b>{t["after"]}</b></div>
          <p class="testi-body">{t["body"]}</p>
        </div>''')
    return f'''
  <section class="alt">
    <div class="wrap">
      <div class="section-head"><div><span class="kicker">VOICE</span><h2>利用者の声</h2></div></div>
      <p class="listing-note" style="margin-top:-20px;">※ご紹介する体験談は、本デザイン案のためのサンプルです。実在する利用者の声ではありません。</p>
      <div class="testi-grid">
{chr(10).join(cards)}
      </div>
    </div>
  </section>'''

def hero_photo_html(p, eyebrow, h1, lead):
    return f'''  <div class="hero">
    <div class="hero-photo">
      <div class="hero-inner">
        <div class="hero-text">
          <span class="eyebrow">{eyebrow}</span>
          <h1>{h1}</h1>
          <p class="lead">{lead}</p>
          <div class="btnrow">
            <a href="#jobs" class="btn btn-hero-primary">求人を探す</a>
          </div>
        </div>
      </div>
    </div>
  </div>'''

def hero_grid_html(p, eyebrow, h1, checks):
    check_items = "\n          ".join(f'<li>{CHECK_SVG}{c}</li>' for c in checks)
    return f'''  <section class="hero">
    <div class="wrap hero-grid">
      <div>
        <span class="eyebrow">{eyebrow}</span>
        <h1>{h1}</h1>
        <ul class="check-list">
          {check_items}
        </ul>
        <div class="btnrow">
          <a href="#jobs" class="btn btn-warm">求人を探す</a>
        </div>
      </div>
      <div class="photo-wrap">
        <div class="photo" style="background-image:url('../assets/img/{p["hero_photo"]}')"></div>
        <div class="float-badge b1">✓ 未経験OK</div>
        <div class="float-badge b2">✓ 夜勤なし相談可</div>
      </div>
    </div>
  </section>'''

HERO_COPY = {
    "pattern-a": {"eyebrow": "2クリックでカンタン応募", "h1": "その経験を、次の現場へ。",
                  "lead": "特別養護老人ホーム・老健・デイサービス・訪問介護まで。無資格・未経験からのスタートも、資格を活かした転職も。介護の求人を毎日更新しています。"},
    "pattern-b": {"eyebrow": "介護のお仕事探しなら", "h1": "自分らしく働ける<br>現場が、見つかる。",
                  "checks": ["無資格・未経験の求人も多数", "2クリックでカンタン応募", "夜勤なしの求人も選べる"]},
    "pattern-c": {"eyebrow": "介護の現場で、まっすぐ働く。", "h1": "その想いを、<br>次のキャリアへ。",
                  "lead": "特養・老健・グループホームまで。施設の雰囲気や夜勤の有無まで、現場のリアルな条件がわかる介護専門の求人サイトです。"},
}

def hero_html(pattern_key, p):
    c = HERO_COPY[pattern_key]
    if p["hero"] == "grid":
        return hero_grid_html(p, c["eyebrow"], c["h1"], c["checks"])
    return hero_photo_html(p, c["eyebrow"], c["h1"], c["lead"])

def search_band_html(pattern_key):
    stat_html = f'''<div class="stat-strip">
          <div><div class="stat-num mono">{TOTAL_JOBS:,}件</div><div class="stat-label">掲載求人数</div></div>
          <div><div class="stat-num mono">{TOTAL_COMPANIES}社</div><div class="stat-label">掲載企業数</div></div>
          <div><div class="stat-num mono">{TODAY_NEW}件</div><div class="stat-label">本日の新着</div></div>
        </div>'''
    return f'''  <section style="padding-top:0;">
    <div class="wrap search-overlap">
      <form class="search-card" action="list.html" method="get">
        <div class="search-row">
          <div class="field">
            <label for="kw">キーワード</label>
            <input id="kw" type="text" placeholder="介護職員 / ケアマネ / 特養 など">
          </div>
          <div class="field">
            <label for="areaSelect">エリア</label>
            <select id="areaSelect">
              <option>エリアを選ぶ</option>
              <option>東京都</option><option>神奈川県</option><option>大阪府</option><option>愛知県</option>
            </select>
          </div>
          <div class="field">
            <label for="emp">雇用形態</label>
            <select id="emp">
              <option>指定なし</option>
              <option>正社員</option><option>パート・アルバイト</option><option>契約社員</option>
            </select>
          </div>
          <button class="search-btn" type="submit">求人を検索</button>
        </div>
        {stat_html}
      </form>
    </div>
  </section>'''

WHY_CARDS = [
    ("特養から訪問介護まで、求人の幅が広い",
     "特別養護老人ホーム・老健・有料老人ホーム・デイサービス・訪問介護まで、介護施設で働く人の求人だけを毎日更新して掲載しています。",
     [f"掲載求人数 {TOTAL_JOBS:,}件（毎日更新）", f"掲載企業数 {TOTAL_COMPANIES}社", "対応エリア 全国8都道府県"]),
    ("2クリックでカンタン応募",
     "会員登録は不要。気になる求人があれば、その場で応募フォームからすぐに応募できます。",
     ["入力はタイル選択が中心、最短1分", "スマートフォンからも同じ手順で応募可能", "応募後は3営業日以内に採用担当者からご連絡"]),
    ("掲載前に確認済みの求人だけ",
     "掲載前に募集内容を確認したうえで公開しています。求人票と実際の条件に相違があった場合は、掲載企業に確認のうえ速やかに対応します。",
     ["給与・勤務条件を掲載前にチェック", "内容に変更があれば随時更新", "気になる点は掲載企業へお問い合わせから確認可能"]),
]

def why_faq_html(pattern_key, p):
    cards = []
    for i, (title, body, items) in enumerate(WHY_CARDS, start=1):
        li = "".join(f"<li>{x}</li>" for x in items)
        cards.append(f'''        <div class="why-card">
          <div class="why-num">0{i}</div>
          <h3>{title}</h3>
          <p>{body}</p>
          <ul>{li}</ul>
        </div>''')
    faq_preview = FAQ[0][1][:3]
    faq_html = []
    for q, a in faq_preview:
        faq_html.append(f'''        <div class="faq-item">
          <p class="faq-q"><span class="qmark">Q.</span>{q}</p>
          <p class="faq-a"><span class="amark">A.</span>{a}</p>
        </div>''')
    brand = p["brand_display"]
    return f'''  <section id="why" class="alt">
    <div class="wrap">
      <div class="section-head"><div><span class="kicker">WHY US</span><h2>{brand} が選ばれる理由</h2></div></div>
      <div class="why-grid">
{chr(10).join(cards)}
      </div>

      <div class="section-head" style="margin-top:56px;"><div><span class="kicker">FAQ</span><h2>よくある質問</h2></div></div>
      <div class="faq-list">
{chr(10).join(faq_html)}
      </div>
      <a href="faq.html" class="see-all" style="display:inline-block;margin-top:20px;">よくある質問をもっと見る →</a>
    </div>
  </section>'''

def cta_band_html():
    return '''  <section>
    <div class="wrap">
      <div class="cta-band">
        <div>
          <h2>会員登録なしで、今すぐ応募できます。</h2>
          <p>掲載求人は毎日更新。気になる求人があれば、その場で応募フォームに進めます。</p>
        </div>
        <a href="list.html" class="btn btn-warm">求人を探す</a>
      </div>
    </div>
  </section>'''

# ---------- ページ生成 ----------

def render_index(pattern_key, p):
    brand = p["brand_display"]
    pickup = JOBS[0:4]
    new = JOBS[4:8]
    pickup_html = "\n".join(f'        {job_card_html(j)}' for j in pickup)
    new_html = "\n".join(f'        {job_card_html(j)}' for j in new)
    testimonial = testimonial_html() if p["testimonial"] else ""
    body = f'''
{header_html(p)}

<main>
{hero_html(pattern_key, p)}

{search_band_html(pattern_key)}

  <section id="fields" class="alt">
    <div class="wrap">
      <div class="section-head">
        <div><span class="kicker">WORKPLACE</span><h2>現場から探す</h2></div>
        <a href="list.html" class="see-all">すべての現場を見る →</a>
      </div>
      <div class="cat-grid">
{categories_html()}
      </div>
    </div>
  </section>

  <section id="jobs">
    <div class="wrap">
      <div class="section-head">
        <div><span class="kicker">PICK UP</span><h2>掲載中の求人例</h2></div>
        <a href="list.html" class="see-all">すべての求人を見る →</a>
      </div>
      <p class="listing-note">※施設名・条件は本デザイン案のための掲載例です。実際の求人ではありません。</p>
      <div class="job-grid">
{pickup_html}
      </div>
    </div>
  </section>

  <section class="alt">
    <div class="wrap">
      <div class="section-head">
        <div><span class="kicker">NEW</span><h2>新着求人</h2></div>
        <a href="list.html" class="see-all">すべての求人を見る →</a>
      </div>
      <div class="job-grid">
{new_html}
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head"><div><span class="kicker">CONDITION</span><h2>人気の条件から探す</h2></div></div>
      <div class="chip-wrap">
        {"".join(f'<a href="list.html" class="chip">{c}</a>' for c in CONDITION_CHIPS)}
      </div>
    </div>
  </section>

  <section class="alt" id="area">
    <div class="wrap">
      <div class="section-head"><div><span class="kicker">AREA</span><h2>エリアから探す</h2></div></div>
      <div class="chip-wrap">
        {"".join(f'<a href="list.html" class="chip">{a}</a>' for a in AREA_CHIPS)}
      </div>
    </div>
  </section>
{testimonial}
{why_faq_html(pattern_key, p)}

{cta_band_html()}
</main>

{footer_html(p)}

{mobile_cta_html()}
'''
    head = page_head(p, f"{brand} | {TAGLINE}", f"介護施設で働く人のための求人サイト。特養・老健・デイサービス・訪問介護まで、経験や資格を活かせる求人だけを集めました。")
    return page_wrap(head, body)


def render_list(pattern_key, p):
    brand = p["brand_display"]
    cards = "\n        ".join(job_card_html(j) for j in JOBS)
    role_checks = ["介護職員・ヘルパー", "生活相談員", "ケアマネージャー", "サービス提供責任者", "施設長・管理者", "看護師（施設内）"]
    facility_checks = [c[0] for c in CATEGORIES]
    cond_checks = CONDITION_CHIPS
    body = f'''
{header_html(p)}

<main>
  <section style="padding-bottom:0;">
    <div class="wrap">
      <div class="breadcrumb"><a href="index.html">TOP</a> ＞ 求人一覧</div>
      <div class="section-head"><div><span class="kicker">SEARCH</span><h1>求人を探す</h1></div></div>

      <form class="filter-card" action="list.html" method="get">
        <div class="filter-row">
          <div class="field"><label for="kw">キーワード</label><input id="kw" type="text" placeholder="介護職員 / ケアマネ / 特養 など"></div>
          <div class="field"><label for="areaSelect">エリア</label><select id="areaSelect"><option>エリアを選ぶ</option>{"".join(f"<option>{a}</option>" for a in AREA_CHIPS)}</select></div>
          <div class="field"><label for="emp">雇用形態</label><select id="emp"><option>指定なし</option><option>正社員</option><option>パート・アルバイト</option><option>契約社員</option></select></div>
          <button class="search-btn" type="submit">検索する</button>
        </div>

        <div class="filter-group">
          <div class="label">職種</div>
          <div class="check-grid">
            {"".join(f'<label class="check-pill"><input type="checkbox">{r}</label>' for r in role_checks)}
          </div>
        </div>
        <div class="filter-group">
          <div class="label">施設種別</div>
          <div class="check-grid">
            {"".join(f'<label class="check-pill"><input type="checkbox">{f}</label>' for f in facility_checks)}
          </div>
        </div>
        <div class="filter-group">
          <div class="label">こだわり条件</div>
          <div class="check-grid">
            {"".join(f'<label class="check-pill"><input type="checkbox">{c}</label>' for c in cond_checks[:6])}
          </div>
        </div>
      </form>

      <p class="listing-note">※施設名・条件は本デザイン案のための掲載例です。実際の求人ではありません。</p>
      <div class="result-head">
        <div class="result-count"><b>{TOTAL_JOBS:,}</b>件中 1〜{len(JOBS)}件を表示</div>
        <label for="sortSelect" class="sr-only">並び替え</label><select id="sortSelect" class="sort-select"><option>おすすめ順</option><option>新着順</option><option>給与が高い順</option></select>
      </div>

      <div class="job-grid">
        {cards}
      </div>

      <nav class="pagination" aria-label="ページ送り">
        <span class="current">1</span>
        <span class="page-inactive" aria-disabled="true">2</span><span class="page-inactive" aria-disabled="true">3</span><span class="page-inactive" aria-disabled="true">4</span><span class="page-inactive" aria-disabled="true">5</span>
        <span class="page-inactive" aria-disabled="true">次へ ›</span>
      </nav>
    </div>
  </section>
</main>

{footer_html(p)}

{mobile_cta_html()}
'''
    head = page_head(p, f"求人一覧 | {brand}", "介護施設の求人一覧。職種・施設種別・エリア・こだわり条件で絞り込んで、気になる求人にそのまま応募できます。")
    return page_wrap(head, body)


def render_job(pattern_key, p, job):
    brand = p["brand_display"]
    badges = "".join(f'<span class="badge{" warm" if i==1 else ""}">{t}</span>' for i, (t, w) in enumerate(job["badges"]))
    points = "\n        ".join(f'<li>{CHECK_SVG}{pt}</li>' for pt in job["points"])
    work_rows = "\n        ".join(f'<tr><th>{k}</th><td>{v}</td></tr>' for k, v in job["work_rows"])
    req_rows = "\n        ".join(f'<tr><th>{k}</th><td>{v}</td></tr>' for k, v in job["req_rows"])
    related_html = "\n        ".join(job_card_html(JOBS_BY_ID[rid], related=True) for rid in job["related"])
    body = f'''
{header_html(p)}

<main>
  <section>
    <div class="wrap" style="max-width:840px;">
      <div class="breadcrumb"><a href="index.html">TOP</a> ＞ <a href="list.html">求人一覧</a> ＞ {job["area_short"]} ＞ 求人詳細</div>

      <div class="job-hero" style="background-image:url('../assets/img/{job["photo"]}')"></div>

      <div class="job-facility" style="margin-bottom:8px;">{job["facility"]}</div>
      <h1 class="job-detail-title">{job["title"]}</h1>
      <div class="badge-row" style="margin-bottom:20px;">
        {badges}
      </div>

      <div class="highlight-box">
        {job["highlight"]}
      </div>

      <div class="detail-ctarow">
        <button type="button" class="btn btn-line" style="flex:0.6;">♡ キープする</button>
        <a href="{apply_file(job["id"])}" class="btn btn-warm">この求人に応募する</a>
      </div>
      <p class="disclaimer">※施設名・条件は本デザイン案のための掲載例です。実際の求人ではありません。応募後、企業の採用担当者より3営業日以内にご連絡いたします。</p>

      <div class="spec-section-title">この求人のポイント</div>
      <ul class="check-list" style="margin-bottom:32px;">
        {points}
      </ul>

      <div class="spec-section-title">仕事内容</div>
      <table class="spec-table">
        {work_rows}
      </table>

      <div class="spec-section-title">募集要項</div>
      <table class="spec-table">
        {req_rows}
      </table>

      <div class="detail-ctarow" style="margin-top:32px;">
        <button type="button" class="btn btn-line" style="flex:0.6;">♡ キープする</button>
        <a href="{apply_file(job["id"])}" class="btn btn-warm">この求人に応募する</a>
      </div>

      <div class="related-title">似ている求人</div>
      <div class="job-grid">
        {related_html}
      </div>
    </div>
  </section>
</main>

{footer_html(p)}

<div class="sticky-apply">
  <button type="button" class="btn btn-line" style="flex:0.5;">♡ キープ</button>
  <a href="{apply_file(job["id"])}" class="btn btn-warm">この求人に応募する</a>
</div>
'''
    head = page_head(p, f'{job["title"]}｜{job["facility"]}の求人 | {brand}',
                      f'{job["facility"]}の{job["title"]}の求人情報。{job["salary"]}。仕事内容・募集要項・福利厚生を掲載しています。')
    return page_wrap(head, body)


def render_apply(pattern_key, p, job):
    brand = p["brand_display"]
    meta_dict = dict(job["req_rows"])
    body = f'''
{header_html(p)}

<main>
  <section>
    <div class="wrap">
      <h1 class="sr-only">応募フォーム</h1>
      <div class="breadcrumb"><a href="index.html">TOP</a> ＞ <a href="{job_file(job["id"])}">求人詳細</a> ＞ 応募する</div>

      <div class="wizard-wrap">
        <div>
          <button type="button" class="wizard-back" id="wizardBack">‹ 戻る</button>

          <div class="step-indicator">
            <div class="step-dot current" data-dot="1">1</div><div class="step-line" data-line="1"></div>
            <div class="step-dot" data-dot="2">2</div><div class="step-line" data-line="2"></div>
            <div class="step-dot" data-dot="3">3</div><div class="step-line" data-line="3"></div>
            <div class="step-dot" data-dot="4">4</div><div class="step-line" data-line="4"></div>
            <div class="step-dot" data-dot="5">5</div>
          </div>

          <div class="wizard-step active" data-step="1">
            <div class="wizard-q">🔍 ご経験を教えてください</div>
            <div class="tile-grid">
              <div class="tile">特別養護老人ホーム</div>
              <div class="tile">介護老人保健施設</div>
              <div class="tile">有料老人ホーム・サ高住</div>
              <div class="tile">デイサービス</div>
              <div class="tile">訪問介護</div>
              <div class="tile">グループホーム</div>
              <div class="tile">経験なし</div>
            </div>
            <button type="button" class="wizard-next" data-next="2"><span class="sub">あと4ステップで完了！</span>次のステップへ</button>
          </div>

          <div class="wizard-step" data-step="2">
            <div class="wizard-q">📋 お持ちの資格を教えてください</div>
            <div class="tile-grid">
              <div class="tile">介護福祉士</div>
              <div class="tile">初任者研修・実務者研修</div>
              <div class="tile">介護支援専門員</div>
              <div class="tile">看護師・准看護師</div>
              <div class="tile" style="grid-column:span 2;">該当なし</div>
            </div>
            <button type="button" class="wizard-next" data-next="3"><span class="sub">あと3ステップで完了！</span>次のステップへ</button>
          </div>

          <div class="wizard-step" data-step="3">
            <div class="wizard-q">📅 ご希望の転職時期を教えてください</div>
            <div class="tile-grid">
              <div class="tile">1ヶ月以内</div>
              <div class="tile">3ヶ月以内</div>
              <div class="tile">6ヶ月以内</div>
              <div class="tile">1年以内</div>
              <div class="tile" style="grid-column:span 2;">良い求人があればすぐ</div>
            </div>
            <div class="wizard-field">
              <label for="pref">📍 お住まいを教えてください</label>
              <select id="pref">
                <option>都道府県を選ぶ</option>
                <option>東京都</option><option>神奈川県</option><option>大阪府</option><option>愛知県</option>
                <option>福岡県</option><option>北海道</option><option>埼玉県</option><option>千葉県</option>
              </select>
            </div>
            <button type="button" class="wizard-next" data-next="4"><span class="sub">あと2ステップで完了！</span>次のステップへ</button>
          </div>

          <div class="wizard-step" data-step="4">
            <div class="wizard-q">👤 お名前と生まれ年を入力してください</div>
            <div class="wizard-field">
              <label for="wname">お名前</label>
              <input id="wname" type="text" placeholder="例：介護 花子">
            </div>
            <div class="wizard-field">
              <label for="wyear">生まれ年</label>
              <select id="wyear">
                <option>選択してください</option>
              </select>
            </div>
            <button type="button" class="wizard-next" data-next="5"><span class="sub">あと1ステップで完了！</span>次のステップへ</button>
          </div>

          <div class="wizard-step" data-step="5">
            <div class="wizard-q">📞 連絡先を教えてください</div>
            <div class="wizard-field">
              <label for="wtel">電話番号</label>
              <input id="wtel" type="tel" placeholder="例：090-1234-5678">
            </div>
            <div class="wizard-field">
              <label for="wemail">メールアドレス</label>
              <input id="wemail" type="email" placeholder="例：hanako@example.com">
            </div>
            <div class="wizard-field">
              <label for="wresume">履歴書・職務経歴書（任意）</label>
              <input id="wresume" type="file" accept=".pdf,.doc,.docx">
            </div>
            <button type="button" class="wizard-next wizard-final" id="wizardSubmit">この内容で応募を完了する</button>
          </div>

          <div class="wizard-step" data-step="done">
            <div class="wizard-done">
              <div class="check-circle"><svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M20 6 9 17l-5-5"/></svg></div>
              <h2 style="font-size:1.3rem;margin-bottom:10px;">応募が完了しました</h2>
              <p style="color:var(--ink-soft);font-size:0.9rem;">応募企業の採用担当者より、3営業日以内にご連絡いたします。<br>（このページはデザイン案のため、実際には送信されません）</p>
              <a href="index.html" class="btn btn-warm" style="margin-top:24px;display:inline-block;">TOPへ戻る</a>
            </div>
          </div>
        </div>

        <aside class="job-summary-card">
          <h4>あなたの応募する求人</h4>
          <div class="job-summary-photo" style="background-image:url('../assets/img/{job["photo"]}')"></div>
          <div class="title">{job["title"]}</div>
          <div class="facility">{job["facility"]}</div>
          <div class="meta">
            <div>勤務地：<span>{meta_dict.get("勤務地","")}</span></div>
            <div>雇用形態：<span>{meta_dict.get("雇用形態","")}</span></div>
            <div>給与：<span>{job["salary"]}</span></div>
          </div>
        </aside>
      </div>
    </div>
  </section>
</main>

<footer>
  <div class="wrap foot-bottom" style="border-top:1px solid var(--line);padding-top:20px;"><span>© 2026 {brand}</span><span>{TAGLINE}</span></div>
</footer>

<script>
(function(){{
  const steps = Array.from(document.querySelectorAll('.wizard-step'));
  const dots = Array.from(document.querySelectorAll('.step-dot'));
  const lines = Array.from(document.querySelectorAll('.step-line'));
  const backBtn = document.getElementById('wizardBack');
  let current = 1;

  function show(stepKey){{
    steps.forEach(s => s.classList.toggle('active', s.dataset.step === String(stepKey)));
    if(stepKey === 'done'){{
      dots.forEach(d => {{ d.classList.add('done'); d.classList.remove('current'); d.textContent = '✓'; }});
      lines.forEach(l => l.classList.add('done'));
      backBtn.style.visibility = 'hidden';
      return;
    }}
    dots.forEach(d=>{{
      const n = Number(d.dataset.dot);
      d.classList.toggle('current', n === stepKey);
      d.classList.toggle('done', n < stepKey);
      d.textContent = n < stepKey ? '✓' : n;
    }});
    lines.forEach(l=>{{
      l.classList.toggle('done', Number(l.dataset.line) < stepKey);
    }});
    backBtn.style.visibility = stepKey === 1 ? 'hidden' : 'visible';
  }}

  document.querySelectorAll('.tile-grid').forEach(grid=>{{
    grid.addEventListener('click', (e)=>{{
      const tile = e.target.closest('.tile');
      if(!tile) return;
      grid.querySelectorAll('.tile').forEach(t=>t.classList.remove('selected'));
      tile.classList.add('selected');
    }});
  }});

  document.querySelectorAll('.wizard-next[data-next]').forEach(btn=>{{
    btn.addEventListener('click', ()=>{{
      current = Number(btn.dataset.next);
      show(current);
      window.scrollTo({{top:0, behavior:'smooth'}});
    }});
  }});

  backBtn.addEventListener('click', ()=>{{
    if(current > 1){{ current -= 1; show(current); }}
  }});

  document.getElementById('wizardSubmit').addEventListener('click', ()=>{{
    show('done');
    window.scrollTo({{top:0, behavior:'smooth'}});
  }});

  const yearSelect = document.getElementById('wyear');
  for(let y=2006; y>=1955; y--){{
    const opt = document.createElement('option');
    opt.textContent = y;
    yearSelect.appendChild(opt);
  }}

  show(current);
}})();
</script>
'''
    head = page_head(p, f'応募する｜{job["facility"]} | {brand}', f'{job["facility"]}の求人への応募フォームです。会員登録は不要、5ステップで応募が完了します。')
    return page_wrap(head, body)


def render_faq(pattern_key, p):
    brand = p["brand_display"]
    sections = []
    for cat, qas in FAQ:
        items = "\n        ".join(f'''<div class="faq-item">
          <p class="faq-q"><span class="qmark">Q.</span>{q}</p>
          <p class="faq-a"><span class="amark">A.</span>{a}</p>
        </div>''' for q, a in qas)
        sections.append(f'''      <div class="info-section">
        <h3>{cat}</h3>
        <div class="faq-list">
        {items}
        </div>
      </div>''')
    body = f'''
{header_html(p)}

<main>
  <section>
    <div class="wrap info-page">
      <div class="breadcrumb"><a href="index.html">TOP</a> ＞ よくある質問</div>
      <h1>よくある質問</h1>
      <p class="lead">応募方法やサイトのご利用について、よくいただくご質問をまとめました。こちらで解決しない場合は<a href="contact-company.html" style="color:var(--accent-strong);">お問い合わせ</a>よりご連絡ください。</p>
{chr(10).join(sections)}
    </div>
  </section>
</main>

{footer_html(p)}

{mobile_cta_html()}
'''
    head = page_head(p, f"よくある質問 | {brand}", f"{brand}のよくある質問。応募の流れ、求人掲載、個人情報の取り扱いについてお答えします。")
    return page_wrap(head, body)


def render_about(pattern_key, p):
    brand = p["brand_display"]
    body = f'''
{header_html(p)}

<main>
  <section>
    <div class="wrap info-page">
      <div class="breadcrumb"><a href="index.html">TOP</a> ＞ サイトについて</div>
      <h1>{brand}について</h1>
      <p class="lead">{brand}は、介護施設で働く人の資格や経験を活かせる仕事だけを集めた求人サイトです。特別養護老人ホーム・介護老人保健施設・有料老人ホーム・サービス付き高齢者向け住宅・デイサービス・訪問介護まで、介護に関わるあらゆる現場の求人を掲載しています。</p>

      <div class="info-section">
        <h3>サービスの特徴</h3>
        <p>{brand}は、企業が求人を直接掲載し、求職者が直接応募できる「求人メディア」です。アドバイザーとの面談やヒアリングを挟まず、気になる求人があればその場で応募フォームに進んでいただけます。</p>
        <ul>
          <li>会員登録不要。応募のたびに必要な項目を入力するだけです</li>
          <li>掲載前に募集内容を確認したうえで公開しています</li>
          <li>掲載求人・掲載企業数は毎日更新しています</li>
        </ul>
      </div>

      <div class="info-section">
        <h3>こんな方におすすめです</h3>
        <ul>
          <li>無資格・未経験から介護の仕事を始めたい方</li>
          <li>特養・老健・デイサービス・訪問介護など、複数の施設種別を比較しながら探したい方</li>
          <li>夜勤の有無や資格取得支援など、働き方の条件で絞り込んで探したい方</li>
        </ul>
      </div>

      <div class="info-section">
        <h3>運営について</h3>
        <p>{brand}は、求人メディア「シゴトLINK」のグループサービスとして運営しています。求人掲載に関するお問い合わせは<a href="contact-company.html" style="color:var(--accent-strong);">こちら</a>から承っております。</p>
      </div>
    </div>
  </section>
</main>

{footer_html(p)}

{mobile_cta_html()}
'''
    head = page_head(p, f"サイトについて | {brand}", f"{brand}は、介護施設で働く人の資格や経験を活かせる求人だけを集めた求人メディアです。会員登録なしで直接応募できます。")
    return page_wrap(head, body)


def render_terms(pattern_key, p):
    brand = p["brand_display"]
    articles = [
        ("第1条（適用）", f"本規約は、{brand}（以下「本サービス」）の利用に関する条件を、本サービスを利用する求職者および掲載企業（以下「利用者」）との間で定めるものです。"),
        ("第2条（利用登録）", "本サービスは会員登録を必要とせず、利用者は求人詳細ページの応募フォームより直接応募することができます。"),
        ("第3条（禁止事項）", "利用者は、虚偽の情報を登録する行為、本サービスの運営を妨害する行為、法令に違反する行為を行ってはなりません。"),
        ("第4条（掲載情報の正確性）", "本サービスは、掲載企業から提供された情報をもとに求人情報を掲載していますが、内容の正確性・最新性について完全性を保証するものではありません。"),
        ("第5条（規約の変更）", "本サービスは、必要と判断した場合には利用者に通知することなく本規約を変更できるものとします。"),
    ]
    sec = "\n".join(f'''      <div class="info-section">
        <h3>{t}</h3>
        <p>{b}</p>
      </div>''' for t, b in articles)
    body = f'''
{header_html(p)}

<main>
  <section>
    <div class="wrap info-page">
      <div class="breadcrumb"><a href="index.html">TOP</a> ＞ 利用規約</div>
      <h1>利用規約</h1>
      <div class="info-section" style="background:var(--accent-tint);padding:16px 20px;border-radius:var(--radius-m);">
        <p style="margin:0;">※本ページはデザイン案用のサンプル条文です。公開前に必ず法務担当者の確認・調整を受けてください。</p>
      </div>
{sec}
    </div>
  </section>
</main>

{footer_html(p)}

{mobile_cta_html()}
'''
    head = page_head(p, f"利用規約 | {brand}", f"{brand}の利用規約です。")
    return page_wrap(head, body)


def render_privacy(pattern_key, p):
    brand = p["brand_display"]
    sections = [
        ("取得する情報", "氏名、生年月日、電話番号、メールアドレス、職務経歴、資格情報など、応募フォームにご入力いただく情報を取得します。"),
        ("利用目的", "取得した情報は、応募先企業への応募情報の提供、お問い合わせへの対応、本サービスの改善のために利用します。"),
        ("第三者提供について", "取得した応募情報は、応募先の企業にのみ提供します。ご本人の同意なく、その他の第三者に提供することはありません。"),
        ("情報の管理", "取得した個人情報は、不正アクセス・紛失・漏えいを防止するため、適切な安全管理措置を講じます。"),
        ("開示・削除のご請求", "ご自身の個人情報の開示・訂正・削除をご希望の場合は、掲載のお問い合わせよりご連絡ください。"),
    ]
    sec = "\n".join(f'''      <div class="info-section">
        <h3>{t}</h3>
        <p>{b}</p>
      </div>''' for t, b in sections)
    body = f'''
{header_html(p)}

<main>
  <section>
    <div class="wrap info-page">
      <div class="breadcrumb"><a href="index.html">TOP</a> ＞ プライバシーポリシー</div>
      <h1>プライバシーポリシー</h1>
      <div class="info-section" style="background:var(--accent-tint);padding:16px 20px;border-radius:var(--radius-m);">
        <p style="margin:0;">※本ページはデザイン案用のサンプル条文です。公開前に必ず法務担当者の確認・調整を受けてください。</p>
      </div>
{sec}
    </div>
  </section>
</main>

{footer_html(p)}

{mobile_cta_html()}
'''
    head = page_head(p, f"プライバシーポリシー | {brand}", f"{brand}のプライバシーポリシー（個人情報の取り扱いについて）です。")
    return page_wrap(head, body)


def render_contact_company(pattern_key, p):
    brand = p["brand_display"]
    why_cards = [
        ("介護施設に絞った掲載", "介護施設で働く人だけに向けて情報が届くため、ミスマッチの少ない応募が期待できます。"),
        ("直接応募だから早い", "アドバイザーを介さず直接応募のため、掲載から応募までのスピードが早いのが特長です。"),
        ("掲載前の内容確認", "掲載前に募集内容を確認するため、実際の労働条件と異なる求人が掲載されることを防ぎます。"),
    ]
    cards = "\n".join(f'''        <div class="why-card">
          <h3>{t}</h3>
          <p>{b}</p>
        </div>''' for t, b in why_cards)
    body = f'''
{header_html(p)}

<main>
  <section>
    <div class="wrap info-page">
      <div class="breadcrumb"><a href="index.html">TOP</a> ＞ 掲載のお問い合わせ</div>
      <h1>掲載のお問い合わせ</h1>
      <p class="lead">介護施設で働く人に向けた求人掲載をご検討の企業様は、以下のフォームよりお問い合わせください。担当者より内容を確認のうえ、折り返しご連絡いたします。</p>

      <div class="why-grid" style="margin-bottom:48px;">
{cards}
      </div>

      <div class="info-section">
        <h3>お問い合わせフォーム</h3>
        <form class="contact-form">
          <div><label for="cname">会社名<span class="required">必須</span></label><input id="cname" type="text" placeholder="株式会社◯◯"></div>
          <div><label for="cperson">ご担当者名<span class="required">必須</span></label><input id="cperson" type="text" placeholder="山田 太郎"></div>
          <div><label for="ctel">電話番号<span class="required">必須</span></label><input id="ctel" type="tel" placeholder="03-1234-5678"></div>
          <div><label for="cemail">メールアドレス<span class="required">必須</span></label><input id="cemail" type="email" placeholder="saiyo@example.com"></div>
          <div><label for="cmsg">ご相談内容</label><textarea id="cmsg" rows="5" placeholder="掲載を検討している求人内容など"></textarea></div>
          <button type="button" class="btn btn-warm" style="align-self:flex-start;">この内容で問い合わせる</button>
        </form>
      </div>
    </div>
  </section>
</main>

{footer_html(p)}

{mobile_cta_html()}
'''
    head = page_head(p, f"掲載のお問い合わせ | {brand}", f"介護施設で働く人向けの求人掲載をご検討の企業さま向けのお問い合わせ窓口です。")
    return page_wrap(head, body)


def render_column_hub(pattern_key, p):
    brand = p["brand_display"]
    cards = []
    icons = {
        "column-shikaku": '<path d="M12 2 2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/>',
        "column-mikeiken": '<path d="M4 12h16M14 6l6 6-6 6"/>',
        "column-yakin": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/>',
    }
    for c in COLUMNS:
        icon = icons.get(c["slug"], "")
        cards.append(f'''        <a href="{c["slug"]}.html" class="mag-card">
          <div class="mag-thumb"><svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">{icon}</svg></div>
          <div class="mag-body">
            <span class="mag-cat">{c["cat"]}</span>
            <div class="mag-title">{c["title"]}</div>
            <p class="mag-excerpt">{c["excerpt"]}</p>
          </div>
        </a>''')
    body = f'''
{header_html(p)}

<main>
  <section>
    <div class="wrap info-page">
      <div class="breadcrumb"><a href="index.html">TOP</a> ＞ お仕事コラム</div>
      <h1>お仕事コラム</h1>
      <p class="lead">介護のお仕事選び、資格の取り方、働き方の選び方まで。お仕事探しに役立つ情報をまとめています。</p>

      <div class="mag-grid">
{chr(10).join(cards)}
      </div>
    </div>
  </section>
</main>

{footer_html(p)}

{mobile_cta_html()}
'''
    head = page_head(p, f"お仕事コラム | {brand}", "介護のお仕事探しに役立つコラム。資格の取り方、未経験からの転職、夜勤あり/なしの働き方を解説します。")
    return page_wrap(head, body)


COLUMN_ICONS = {
    "column-shikaku": '<path d="M12 2 2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/>',
    "column-mikeiken": '<path d="M4 12h16M14 6l6 6-6 6"/>',
    "column-yakin": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/>',
}

def render_column_article(pattern_key, p, c):
    brand = p["brand_display"]
    sections = "\n".join(f'''        <h3>{h}</h3>
        <p>{body}</p>''' for h, body in c["sections"])
    icon = COLUMN_ICONS.get(c["slug"], "")
    body = f'''
{header_html(p)}

<main>
  <section>
    <div class="wrap info-page">
      <div class="breadcrumb"><a href="index.html">TOP</a> ＞ <a href="column.html">お仕事コラム</a> ＞ {c["cat"]}</div>

      <div class="col-hero"><svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4">{icon}</svg></div>
      <div class="col-meta"><span class="mag-cat">{c["cat"]}</span><span>・</span><span>{c["read"]}</span></div>
      <h1>{c["title"]}</h1>
      <p class="lead">{c["lead"]}</p>

      <div class="col-body">
{sections}
      </div>

      <div class="col-cta">
        <p>{c["cta"]}</p>
        <a href="list.html" class="btn btn-warm">求人を探す</a>
      </div>
    </div>
  </section>
</main>

{footer_html(p)}

{mobile_cta_html()}
'''
    head = page_head(p, f'{c["title"]} | {brand}', c["excerpt"])
    return page_wrap(head, body)


def build_pattern(pattern_key, p):
    os.makedirs(pattern_key, exist_ok=True)
    files = {}
    files["index.html"] = render_index(pattern_key, p)
    files["list.html"] = render_list(pattern_key, p)
    for job in JOBS:
        files[job_file(job["id"])] = render_job(pattern_key, p, job)
        files[apply_file(job["id"])] = render_apply(pattern_key, p, job)
    files["faq.html"] = render_faq(pattern_key, p)
    files["about.html"] = render_about(pattern_key, p)
    files["terms.html"] = render_terms(pattern_key, p)
    files["privacy.html"] = render_privacy(pattern_key, p)
    files["contact-company.html"] = render_contact_company(pattern_key, p)
    files["column.html"] = render_column_hub(pattern_key, p)
    for c in COLUMNS:
        files[f'{c["slug"]}.html'] = render_column_article(pattern_key, p, c)

    for fname, content in files.items():
        with open(os.path.join(pattern_key, fname), "w", encoding="utf-8") as f:
            f.write(content)
    print(f"{pattern_key}: wrote {len(files)} files")


if __name__ == "__main__":
    for key, p in PATTERNS.items():
        build_pattern(key, p)
