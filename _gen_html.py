# -*- coding: utf-8 -*-
"""全ページを生成する。

パターンごとに hero / card / sections が切り替わるため、同じ関数が
3種類のマークアップを出し分ける。栄養士版のテンプレートは使っていない。
"""
import os
import re
import hashlib
import html as _html
from _patterns import PATTERNS
import _data as D

ROOT = os.path.dirname(os.path.abspath(__file__))
IMGDIR = os.path.join(ROOT, "assets", "img")

NAV = [
    ("list.html", "求人を探す"),
    ("column.html", "お仕事コラム"),
    ("faq.html", "よくある質問"),
    ("about.html", "サイトについて"),
    ("contact-company.html", "掲載のご相談"),
]

SHOKU_IDX = {k: i + 1 for i, (k, *_rest) in enumerate(D.SHOKUSHU)}

# style.css の内容から算出したバージョン。<link> に ?v= として付けることで、
# CSSを直したのにブラウザやCDNが古い版を配り続ける状態を防ぐ。
CSS_VER = ""


JS_VER = ""


def _hash(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:8]


def set_css_ver(pattern_key):
    """そのパターンの style.css と共通 app.js の内容ハッシュを設定する。"""
    global CSS_VER, JS_VER
    CSS_VER = _hash(os.path.join(ROOT, pattern_key, "style.css"))
    JS_VER = _hash(os.path.join(ROOT, "assets", "app.js"))


def e(s):
    return _html.escape(str(s), quote=True)


def img(name):
    """写真が未配置ならプレースホルダーSVGを参照する。"""
    if os.path.exists(os.path.join(IMGDIR, name)):
        return "../assets/img/" + name
    return "../assets/img/" + os.path.splitext(name)[0] + ".svg"


def yakin_class(j):
    # 夜勤専従はヒーローの3択の一つなので、夜勤ありと同じ見た目にしない
    return {"none": "y-none", "some": "y-some", "senju": "y-senju"}[j["yakin"]]


def shoku_of(j):
    return D.SHOKUSHU_BY_KEY[j["shokushu"]]


def shisetsu_of(j):
    return D.SHISETSU_BY_KEY[j["shisetsu"]]


def fmt(n):
    return f"{n:,}"


def pay_compact(s):
    """カードの狭いセル用に給与表記を詰める。
    「月給 21.0万円 〜 25.0万円」→「月給 21.0〜25.0万円」"""
    return re.sub(r"([\d,.]+)(?:万円|円)\s*〜\s*", r"\1〜", s)


# =============================================================== 共通パーツ
def head(p, key, title, desc, page, body_attr=""):
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}｜{e(D.BRAND_EN)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex">
<link rel="stylesheet" href="style.css{('?v=' + CSS_VER) if CSS_VER else ''}">
</head>
<body data-page="{e(page)}"{body_attr}>
"""


def masthead(current):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'<li><a href="{href}"{cur}>{e(label)}</a></li>')
    return f"""<header class="masthead">
<input type="checkbox" id="navtoggle" class="navtoggle">
<div class="wrap masthead-in">
  <a class="brand" href="index.html">
    <span class="brand-en">{e(D.BRAND_EN)}</span>
    <span class="brand-ja">{e(D.BRAND_JA)}</span>
  </a>
  <label class="burger" for="navtoggle"><span></span><span></span><span></span>
    <span class="sr-only">メニューを開閉する</span></label>
  <nav class="mastnav" aria-label="サイト内メニュー"><ul>{''.join(items)}</ul></nav>
</div>
</header>
"""


def crumbs(items):
    li = []
    for i, (label, href) in enumerate(items):
        if href and i < len(items) - 1:
            li.append(f'<li><a href="{href}">{e(label)}</a></li>')
        else:
            li.append(f'<li aria-current="page">{e(label)}</li>')
    return f'<nav class="crumbs" aria-label="パンくずリスト"><div class="wrap"><ol>{"".join(li)}</ol></div></nav>'


def footer():
    shoku_links = "".join(
        f'<li><a href="list.html">{e(s[1])}の求人</a></li>' for s in D.SHOKUSHU[:5]
    )
    shisetsu_links = "".join(
        f'<li><a href="list.html">{e(s[1])}の求人</a></li>' for s in D.SHISETSU[:5]
    )
    return f"""<footer class="foot">
<div class="wrap">
  <div class="foot-cols">
    <div class="foot-brand">
      <a class="brand" href="index.html"><span class="brand-en">{e(D.BRAND_EN)}</span>
        <span class="brand-ja">{e(D.BRAND_JA)}</span></a>
      <p>{e(D.TAGLINE)}。会員登録なしで、掲載施設へ直接応募いただけます。</p>
    </div>
    <div><h2>職種から探す</h2><ul>{shoku_links}</ul></div>
    <div><h2>施設種別から探す</h2><ul>{shisetsu_links}</ul></div>
    <div><h2>サイト情報</h2><ul>
      <li><a href="about.html">サイトについて</a></li>
      <li><a href="faq.html">よくある質問</a></li>
      <li><a href="contact-company.html">掲載のご相談（企業様）</a></li>
      <li><a href="terms.html">利用規約</a></li>
      <li><a href="privacy.html">プライバシーポリシー</a></li>
    </ul></div>
  </div>
  <p class="foot-note">本サイトはデザイン提案用のデモページです。掲載している求人・施設・数値・
    「働く人の声」はすべて架空のサンプルであり、実在の施設・人物とは関係ありません。
    利用規約およびプライバシーポリシーもサンプル文面のため、公開前に法務確認が必要です。<br>
    © {e(D.BRAND_JA)}（デモ）</p>
</div>
</footer>
"""


def mobilebar(primary_href="list.html", primary_label="求人を探す"):
    return f"""<div class="mobilebar">
  <a class="btn btn-ghost" href="faq.html">よくある質問</a>
  <a class="btn btn-main" href="{primary_href}">{e(primary_label)}</a>
</div>
"""


def tail():
    src = "../assets/app.js" + (("?v=" + JS_VER) if JS_VER else "")
    return f'<script src="{src}" defer></script>\n</body>\n</html>\n'


# ============================================================ 求人カード3種
def card_dense(j, compact=False):
    s = shoku_of(j)
    si = SHOKU_IDX[j["shokushu"]]
    flags = []
    if j["has_timeline"]:
        flags.append("1日の流れ掲載")
    if j["has_voice"]:
        flags.append("働く人の声あり")
    flag_html = "".join(f'<span class="has-flag">{e(t)}</span>' for t in flags)

    if compact:
        cells = [("給与", pay_compact(j["pay_main"]), "pay"), ("勤務シフト", j["shift"], "")]
        cell_html = "".join(
            f'<div class="jrow-cell"><dt>{e(k)}</dt><dd class="{cls}">{e(v)}</dd></div>'
            for k, v, cls in cells
        )
        return f"""<article class="jrow" data-s="s{si}">
  <div class="jrow-stripe" aria-hidden="true"></div>
  <div class="jrow-photo">
    <img src="{img(j['photo'])}" alt="{e(shisetsu_of(j)[1])}のイメージ写真" loading="lazy" width="400" height="300">
  </div>
  <div class="jrow-in">
    <div class="jrow-top">
      <span class="chip-shoku sk{si}">{e(s[2])}</span>
      <span class="chip-emp">{e(j['employment'])}</span>
    </div>
    <h3 class="jrow-title"><a href="{D.job_file(j['id'])}">{e(j['title'])}</a></h3>
    <p class="jrow-facility">{e(j['facility'])}／{e(j['pref'])}</p>
    <dl class="jrow-grid">{cell_html}</dl>
    <div class="jrow-has">{flag_html}</div>
    <div class="jrow-foot">
      <a class="btn btn-main" href="{D.apply_file(j['id'])}">応募する</a>
      <a class="detail" href="{D.job_file(j['id'])}">詳細 →</a>
    </div>
  </div>
</article>"""

    cells = [
        ("給与", pay_compact(j["pay_main"]), "pay"),
        ("勤務シフト", j["shift"], ""),
        ("勤務地", j["pref"], ""),
        ("施設種別", shisetsu_of(j)[2], ""),
    ]
    cell_html = "".join(
        f'<div class="jrow-cell"><dt>{e(k)}</dt><dd class="{cls}">{e(v)}</dd></div>'
        for k, v, cls in cells
    )
    tags = "".join(f"<span>{e(t)}</span>" for t in j["tags"][:6])
    return f"""<article class="jrow" data-s="s{si}">
  <div class="jrow-stripe" aria-hidden="true"></div>
  <div class="jrow-photo">
    <img src="{img(j['photo'])}" alt="{e(shisetsu_of(j)[1])}のイメージ写真" loading="lazy" width="400" height="300">
  </div>
  <div class="jrow-in">
    <div class="jrow-top">
      <span class="chip-shoku sk{si}">{e(s[2])}</span>
      <span class="chip-yakin {yakin_class(j)}">{e(j['shift'])}</span>
      <span class="chip-emp">{e(j['employment'])}</span>
      <span class="jrow-updated">{e(j['updated'])}更新</span>
    </div>
    <h3 class="jrow-title"><a href="{D.job_file(j['id'])}">{e(j['title'])}／{e(j['facility'])}</a></h3>
    <p class="jrow-facility">{e(j['area'])}／{e(j['access'])}</p>
    <dl class="jrow-grid">{cell_html}</dl>
    <div class="jrow-has">{flag_html}</div>
    <div class="jrow-tags">{tags}</div>
    <div class="jrow-foot">
      <a class="btn btn-main" href="{D.apply_file(j['id'])}">この求人に応募する</a>
      <a class="detail" href="{D.job_file(j['id'])}">求人の詳細を見る →</a>
    </div>
  </div>
</article>"""


def card_story(j):
    flags = []
    if j["has_timeline"]:
        flags.append("1日の流れ掲載")
    if j["has_voice"]:
        flags.append("働く人の声あり")
    flags.append(f"職員構成を公開")
    flag_html = "".join(f"<span>{e(t)}</span>" for t in flags)
    peek = ""
    if j["has_timeline"]:
        picks = [j["timeline"][0], j["timeline"][len(j["timeline"]) // 2], j["timeline"][-1]]
        items = "".join(f"<li><b>{e(t)}</b>{e(l)}</li>" for t, l, _d in picks)
        peek = f"""<div class="jstory-peek">
      <p class="peek-label">{e(j['timeline_label'])}（抜粋）</p>
      <ul>{items}</ul>
    </div>"""
    elif j["has_voice"]:
        peek = f"""<div class="jstory-peek">
      <p class="peek-label">働く人の声（抜粋）</p>
      <ul><li>{e(j['voice']['body'][:60])}…</li></ul>
    </div>"""
    tags = "".join(f"<span>{e(t)}</span>" for t in j["tags"][:5])
    return f"""<article class="jstory">
  <div class="jstory-photo">
    <img src="{img(j['photo'])}" alt="{e(shisetsu_of(j)[1])}のイメージ写真" loading="lazy" width="960" height="420">
    <div class="jstory-flags">{flag_html}</div>
  </div>
  <div class="jstory-in">
    <p class="jstory-catch">{e(j['catch'])}</p>
    <div class="jstory-who">
      <span class="title">{e(j['title'])}（{e(j['employment'])}）</span>
      <span class="facility">{e(j['facility'])}</span>
      <span class="updated">{e(j['updated'])}更新</span>
    </div>
    <dl class="jstory-facts">
      <div><dt>給与</dt><dd class="pay">{e(j['pay_main'])}</dd></div>
      <div><dt>勤務シフト</dt><dd>{e(j['shift'])}</dd></div>
      <div><dt>勤務地</dt><dd>{e(j['area'])}</dd></div>
    </dl>
    {peek}
    <div class="jstory-tags">{tags}</div>
    <div class="jstory-foot">
      <a class="btn btn-main" href="{D.apply_file(j['id'])}">この求人に応募する</a>
      <a class="btn btn-ghost" href="{D.job_file(j['id'])}">求人の詳細を見る</a>
    </div>
  </div>
</article>"""


def table_jobs(jobs):
    rows = []
    for j in jobs:
        tags = "".join(f"<span>{e(t)}</span>" for t in j["tags"][:4])
        tl = '<span class="on">✓ 1日の流れ</span>' if j["has_timeline"] else '<span class="off">− 1日の流れ</span>'
        vo = '<span class="on">✓ 働く人の声</span>' if j["has_voice"] else '<span class="off">− 働く人の声</span>'
        rows.append(f"""<tr>
    <td class="jt-main">
      <div class="jt-head">
        <img class="jt-thumb" src="{img(j['photo'])}" alt="{e(shisetsu_of(j)[1])}のイメージ写真" loading="lazy" width="160" height="120">
        <div>
          <p class="jt-title"><a href="{D.job_file(j['id'])}">{e(j['title'])}</a></p>
          <p class="jt-facility">{e(j['facility'])}</p>
        </div>
      </div>
      <div class="jt-tags">{tags}</div>
    </td>
    <td data-label="給与"><span class="jt-pay">{e(j['pay_main'])}</span>
      <p class="jt-paynote">{e(j['employment'])}</p></td>
    <td class="jt-shift" data-label="夜勤"><span class="jt-yakin {yakin_class(j)}">{e(j['shift'])}</span></td>
    <td data-label="勤務地">{e(j['pref'])}<p class="jt-paynote">{e(shisetsu_of(j)[2])}</p></td>
    <td data-label="掲載情報"><div class="jt-has">{tl}{vo}</div></td>
    <td class="jt-updated" data-label="更新日">{e(j['updated'])}</td>
    <td class="jt-act"><a class="btn btn-main" href="{D.apply_file(j['id'])}">この求人に応募する</a></td>
  </tr>""")
    return f"""<div class="jtable-scroll"><table class="jtable">
  <thead><tr>
    <th scope="col">求人・施設</th><th scope="col">給与</th><th scope="col">夜勤</th>
    <th scope="col">勤務地・種別</th><th scope="col">掲載情報</th><th scope="col">更新日</th>
    <th scope="col"><span class="sr-only">応募</span></th>
  </tr></thead>
  <tbody>{''.join(rows)}</tbody>
</table></div>"""


def render_cards(p, jobs):
    if p["card"] == "dense":
        return "".join(card_dense(j) for j in jobs)
    if p["card"] == "story":
        return "".join(card_story(j) for j in jobs)
    return table_jobs(jobs)


# ================================================================= ヒーロー
def hero_yakin():
    picks = []
    for key, headline, desc, count, where in D.YAKIN_AXIS:
        picks.append(f"""<a class="ypick" href="list.html" data-yk="{e(key)}" data-yk-label="{e(headline)}" data-yk-count="{count}">
      <span class="yp-head">{e(headline)}</span>
      <span class="yp-count"><b data-count="{count}">{fmt(count)}</b><small>件</small></span>
      <span class="yp-desc">{e(desc)}</span>
      <span class="yp-where">主な施設：{e(where)}</span>
    </a>""")
    return f"""<section class="yakinhero">
  <div class="wrap yakinhero-in">
    <div class="yh-top">
      <div class="yh-copy">
        <h1>夜勤は、自分で選べる。</h1>
        <p class="h-sub">特養・老健・デイ・訪問介護まで。介護の求人を毎日更新。会員登録なしで直接応募できます。</p>
        <div class="h-meta">
          <span>掲載求人 {fmt(D.TOTAL_JOBS)}件</span>
          <span>掲載事業所 {fmt(D.TOTAL_COMPANIES)}法人</span>
          <span>本日の新着 {fmt(D.TODAY_NEW)}件</span>
          <span>最終更新 {e(D.UPDATED)}</span>
        </div>
      </div>
      <div class="yh-photo">
        <img src="{img('hero-a-yakin.jpg')}" alt="夜勤明けの職員が、出勤してきた日勤の職員に申し送りをしている様子" loading="eager">
      </div>
    </div>
    <div class="yakinshare" aria-hidden="true">
      <span class="ys none" style="width:{D.YAKIN_AXIS[0][3] / D.TOTAL_JOBS * 100:.1f}%"></span>
      <span class="ys some" style="width:{D.YAKIN_AXIS[1][3] / D.TOTAL_JOBS * 100:.1f}%"></span>
      <span class="ys senju" style="width:{D.YAKIN_AXIS[2][3] / D.TOTAL_JOBS * 100:.1f}%"></span>
    </div>
    <p class="yakinshare-l">掲載求人の内訳：夜勤なし {D.YAKIN_AXIS[0][3] / D.TOTAL_JOBS * 100:.0f}%／夜勤あり {D.YAKIN_AXIS[1][3] / D.TOTAL_JOBS * 100:.0f}%／夜勤専従 {D.YAKIN_AXIS[2][3] / D.TOTAL_JOBS * 100:.0f}%</p>
    <div class="yakinpick">{''.join(picks)}</div>
  </div>
</section>
<div class="yakinhero-tail"></div>"""


def hero_timeline():
    j = D.JOBS_BY_ID[1]
    # 「1日が見える」と言う以上、出勤で切らずに退勤まで見せる。
    # 全項目を出すと縦に伸びるため、始点と終点を含む4項目を等間隔で抜く。
    tl = j["timeline"]
    n = 4
    idx = sorted({round(i * (len(tl) - 1) / (n - 1)) for i in range(n)})
    peek = [tl[i] for i in idx]
    rows = "".join(f"""<div class="daily-row">
      <div class="daily-time">{e(t)}</div>
      <div class="daily-axis" aria-hidden="true"></div>
      <div class="daily-body"><p class="daily-label">{e(l)}</p></div>
    </div>""" for t, l, _d in peek)
    return f"""<section class="timelinehero">
  <div class="wrap thero-grid">
    <div class="thero-copy">
      <h1>働く前に、1日が見える。</h1>
      <p class="h-sub">出勤から退勤までの時間割を、掲載施設に書いてもらいました。読んでから決めてください。</p>
      <div class="h-stat">
        <div><b data-count="{D.TOTAL_JOBS}">{fmt(D.TOTAL_JOBS)}</b>掲載求人</div>
        <div><b data-count="{D.TOTAL_COMPANIES}">{fmt(D.TOTAL_COMPANIES)}</b>掲載法人</div>
        <div><b data-count="{D.TODAY_NEW}">{fmt(D.TODAY_NEW)}</b>本日の新着</div>
      </div>
      <div class="btns">
        <a class="btn btn-main" href="list.html">求人を探す</a>
        <a class="btn btn-ghost" href="#voices">働く人の声を読む</a>
      </div>
    </div>
    <div class="thero-card">
      <div class="thero-photo">
        <img src="{img('hero-b-day.jpg')}" alt="介護施設の明るい共有スペースで職員と利用者が会話している様子" loading="eager">
      </div>
      <div class="thero-card-body">
        <div class="tc-top">
          <span class="who">{e(j['timeline_label'])}（抜粋）</span>
          <span class="at">{e(j['facility'])}／{e(j['title'])}</span>
        </div>
        <div class="daily">{rows}</div>
        <p class="tc-foot">全{len(tl)}項目と給与の内訳は求人ページに。
          <a href="{D.job_file(j['id'])}">求人を見る →</a></p>
      </div>
    </div>
  </div>
</section>"""


def hero_search():
    shoku = "".join(
        f'<label class="pill"><input type="checkbox" name="shokushu" value="{e(k)}">{e(short)}'
        f'<span class="num">{fmt(cnt)}</span></label>'
        for k, _n, short, _c, cnt, _p, _d in D.SHOKUSHU
    )
    area = "".join(
        f'<label class="pill"><input type="checkbox" name="area" value="{e(a)}">{e(a)}</label>'
        for a in D.AREA_CHIPS
    )
    emp = "".join(
        f'<label class="pill"><input type="checkbox" name="emp" value="{e(a)}">{e(a)}</label>'
        for a in D.EMPLOYMENT_CHIPS
    )
    # トップの検索はよく使う10条件まで。残りは求人一覧側で絞り込む（モバイルで縦に伸びすぎるため）
    cond = "".join(
        f'<label class="pill"><input type="checkbox" name="cond" value="{e(a)}">{e(a)}</label>'
        for a in D.CONDITION_CHIPS[:10]
    )
    return f"""<section class="searchhero">
  <div class="wrap">
    <h1>条件は、並べて比べる。</h1>
    <p class="h-sub">基本給・手当・賞与を分けて掲載。25の条件で絞り込めます。会員登録は不要です。</p>
    <div class="h-stat">
      <span><b data-count="{D.TOTAL_JOBS}">{fmt(D.TOTAL_JOBS)}</b>掲載求人</span>
      <span><b data-count="{D.TOTAL_COMPANIES}">{fmt(D.TOTAL_COMPANIES)}</b>掲載法人</span>
      <span><b data-count="{D.TODAY_NEW}">{fmt(D.TODAY_NEW)}</b>本日の新着</span>
      <span>最終更新 {e(D.UPDATED)}</span>
    </div>
    <div class="searchhero-photo">
      <img src="{img('hero-c-genba.jpg')}" alt="介護記録に記入する職員の手元" loading="eager">
      <span class="cap">現場の記録から生まれた検索軸です</span>
    </div>
    <form class="sform" action="list.html" method="get">
      <div class="sform-row"><div class="k"><label for="kw">キーワード</label></div>
        <div class="v"><input type="text" id="kw" name="kw" placeholder="施設名・駅名・資格名など"></div></div>
      <div class="sform-row"><div class="k">職種</div>
        <div class="v"><div class="pillset">{shoku}</div></div></div>
      <div class="sform-row"><div class="k">エリア</div>
        <div class="v"><div class="pillset">{area}</div></div></div>
      <div class="sform-row"><div class="k">雇用形態</div>
        <div class="v"><div class="pillset">{emp}</div></div></div>
      <div class="sform-row"><div class="k">こだわり条件</div>
        <div class="v"><div class="pillset">{cond}</div>
          <p class="sform-more"><a href="list.html">残り{len(D.CONDITION_CHIPS) - 10}件の条件で絞り込む →</a></p></div></div>
      <div class="sform-go">
        <p class="hit">該当求人 <b data-count="{D.TOTAL_JOBS}">{fmt(D.TOTAL_JOBS)}</b>件</p>
        <button class="btn btn-main" type="submit">この条件で検索する</button>
      </div>
    </form>
  </div>
</section>"""


def hero(p):
    return {"yakin": hero_yakin, "timeline": hero_timeline, "search": hero_search}[p["hero"]]()


# ================================================================ セクション
def sec_coverage(p):
    stats = D.coverage_stats()
    cells = []
    for label, got, total, note in stats:
        pct = round(got / total * 100)
        cells.append(f"""<div class="cov">
      <p class="cov-label">{e(label)}</p>
      <div class="cov-bar"><i data-w="{pct}" style="width:{pct}%"></i></div>
      <p class="cov-val"><b>{got}</b> / {total}件の求人に掲載（{pct}%）</p>
      <p class="cov-note">{e(note)}</p>
    </div>""")
    return f"""<section class="band band-tint">
  <div class="wrap">
    <div class="band-head">
      <span class="eyebrow">掲載情報の充実度</span>
      <h2>入ってから「聞いてない」をなくす</h2>
      <p class="lede">条件面だけでなく、次の6項目まで掲載施設に書いてもらっています。<a href="column-kyujinhyo.html">求人票の見方はこちら</a></p>
    </div>
    <div class="coverage">{''.join(cells)}</div>
  </div>
</section>"""


def _rgb(hexcode):
    h = hexcode.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def sec_matrix(p):
    # 42マスの数字を1つずつ読ませるのではなく、濃淡で分布が一目で分かるようにする。
    # 件数の分布が偏っているため、平方根寄りの階調にして小さい値も見えるようにした。
    r, g, b = _rgb(p["tokens"]["--accent"])
    mx = max(v for row in D.MATRIX.values() for v in row.values())
    head_cells = "".join(f'<th scope="col">{e(s[2])}</th>' for s in D.SHISETSU)
    body = []
    for k, name, short, _c, cnt, _pay, _desc in D.SHOKUSHU:
        si = SHOKU_IDX[k]
        tds = []
        for sk, *_r in D.SHISETSU:
            v = D.MATRIX[k][sk]
            if v == 0:
                tds.append('<td class="zero">—</td>')
            else:
                a = 0.05 + 0.40 * (v / mx) ** 0.6
                tds.append(
                    f'<td style="background:rgba({r},{g},{b},{a:.3f})">'
                    f'<a href="list.html">{fmt(v)}</a></td>'
                )
        body.append(
            f'<tr><th scope="row"><span class="dot sk{si}"></span>{e(short)}</th>'
            f'{"".join(tds)}<td class="num"><b>{fmt(cnt)}</b></td></tr>'
        )
    foot_tds = "".join(f"<td>{fmt(s[4])}</td>" for s in D.SHISETSU)
    # 凡例はセルとまったく同じ式で色を出し、見本と実物がずれないようにする
    legend = "".join(
        f'<i class="lg" style="background:rgba({r},{g},{b},'
        f'{0.05 + 0.40 * t ** 0.6:.3f})"></i>'
        for t in (0.04, 0.2, 0.45, 0.72, 1.0)
    )
    return f"""<section class="band">
  <div class="wrap">
    <div class="band-head">
      <span class="eyebrow">職種 × 施設種別</span>
      <h2>同じ介護職でも、施設が変われば別の仕事</h2>
      <p class="lede">色が濃いほど求人が多い組み合わせです。数字からそのまま求人一覧に進めます。</p>
    </div>
    <div class="matrixwrap"><table class="matrix">
      <caption class="sr-only">職種と施設種別の組み合わせごとの求人件数</caption>
      <thead><tr><th scope="col">職種＼施設種別</th>{head_cells}<th scope="col">合計</th></tr></thead>
      <tbody>{''.join(body)}</tbody>
      <tfoot><tr><th scope="row">合計</th>{foot_tds}<td>{fmt(D.TOTAL_JOBS)}</td></tr></tfoot>
    </table></div>
    <p class="matrix-legend"><span>少ない</span>{legend}<span>多い</span></p>
    <p class="matrix-note">件数は{e(D.UPDATED)}時点のものです。数値はデモ用のサンプルです。</p>
  </div>
</section>"""


def sec_rails(p):
    rails_by_key = {r[0]: r for r in D.RAILS}
    blocks = []
    for key in p["rails"]:
        rk, title, desc, fn = rails_by_key[key]
        jobs = [j for j in D.JOBS if fn(j)]
        cards = "".join(card_dense(j, compact=True) for j in jobs)
        blocks.append(f"""<div class="rail">
      <div class="rail-head">
        <div><h3>{e(title)}（{len(jobs)}件）</h3><p>{e(desc)}</p></div>
        <a href="list.html">すべて見る →</a>
      </div>
      <div class="rail-track">{cards}</div>
    </div>""")
    return f"""<section class="band band-tint">
  <div class="wrap">
    <div class="band-head">
      <span class="eyebrow">気になっていることから</span>
      <h2>いま気になっている点から</h2>
      <p class="lede">応募前に確かめたくなる条件ごとに、求人をまとめました。</p>
    </div>
    {''.join(blocks)}
  </div>
</section>"""


def sec_shindan(p):
    """3つの質問で件数が動く絞り込み。選んだ夜勤条件はブラウザに記憶される。"""
    yakin = "".join(
        f'<button type="button" data-v="{e(k)}" data-n="{cnt}" data-label="{e(head)}" '
        f'aria-pressed="false">{e(head)}</button>'
        for k, head, _d, cnt, _w in D.YAKIN_AXIS
    )
    shoku = "".join(
        f'<button type="button" data-v="{e(k)}" data-r="{cnt / D.TOTAL_JOBS:.4f}" '
        f'data-label="{e(short)}" aria-pressed="false">{e(short)}</button>'
        for k, _n, short, _c, cnt, _p, _d in D.SHOKUSHU
    )
    area_counts = [842, 586, 548, 452, 418, 396, 364, 312, 298, 186]
    area = "".join(
        f'<button type="button" data-v="a{i}" data-r="{c / D.TOTAL_JOBS:.4f}" '
        f'data-label="{e(a)}" aria-pressed="false">{e(a)}</button>'
        for i, (a, c) in enumerate(zip(D.AREA_CHIPS, area_counts))
    )
    return f"""<section class="band band-surface" id="shindan">
  <div class="wrap">
    <div class="band-head">
      <span class="eyebrow">3つの質問</span>
      <h2>あなたの条件だと、何件あるか</h2>
      <p class="lede">選ぶたびに件数が変わります。会員登録は不要です。</p>
    </div>
    <div class="dx">
      <div class="dx-q">
        <p class="dx-label">1. 夜勤はどうしますか</p>
        <div class="dx-opts" data-g="yakin">{yakin}</div>
      </div>
      <div class="dx-q">
        <p class="dx-label">2. 職種は</p>
        <div class="dx-opts" data-g="shoku">{shoku}</div>
      </div>
      <div class="dx-q">
        <p class="dx-label">3. エリアは</p>
        <div class="dx-opts" data-g="area">{area}</div>
      </div>
      <div class="dx-out">
        <p class="dx-res"><span class="dx-n" data-base="{D.TOTAL_JOBS}">{fmt(D.TOTAL_JOBS)}</span><span class="dx-l">件（3つ選ぶと、あなたに合う求人の数になります）</span></p>
        <a class="btn btn-main dx-go" href="list.html" hidden>この条件の求人を見る</a>
      </div>
    </div>
    <p class="matrix-note">選んだ夜勤の条件はご利用中のブラウザに保存され、次にお越しいただいたときに引き継がれます。当サイトのサーバーには送信されません。</p>
  </div>
</section>"""


def sec_prevjob(p):
    """前職 → 介護 の橋渡し。応募者が「いま持っているもの」を先に言語化する。"""
    if p["card"] == "table":
        rows = "".join(f"""<tr>
      <th scope="row">{e(b['from_'])}</th>
      <td>{e(b['gain'])}</td>
      <td>{e(b['fit'])}</td>
      <td class="n"><a href="list.html">{fmt(b['count'])}件</a></td>
    </tr>""" for b in D.PREV_JOBS)
        inner = f"""<div class="soubawrap"><table class="souba">
      <caption class="sr-only">前職ごとに、介護で活きる経験と相性のいい職場</caption>
      <thead><tr><th scope="col">前職</th><th scope="col">介護で活きる経験</th>
        <th scope="col">相性のいい職場</th><th scope="col">求人数</th></tr></thead>
      <tbody>{rows}</tbody>
    </table></div>"""
    else:
        def mk(b):
            return f"""<a class="bcard" href="list.html">
      <span class="b-from">
        <span class="b-label">前職</span>
        <span class="b-name">{e(b['from_'])}</span>
      </span>
      <span class="b-to">
        <span class="b-label">介護では</span>
        <span class="b-gain">{e(b['gain'])}</span>
        <span class="b-why">{e(b['why'])}</span>
        <span class="b-foot">相性のいい職場：{e(b['fit'])}<b>{fmt(b['count'])}件</b></span>
      </span>
    </a>"""

        # 6枚すべてを並べると縦に伸びるため、4枚を出して残りは開いたときに見せる
        shown = "".join(mk(b) for b in D.PREV_JOBS[:4])
        rest = "".join(mk(b) for b in D.PREV_JOBS[4:])
        inner = (f'<div class="bridge">{shown}</div>'
                 f'<details class="more"><summary>'
                 f'<span class="more-open">ほかの前職も見る（{len(D.PREV_JOBS) - 4}件）</span>'
                 f'<span class="more-close">閉じる</span></summary>'
                 f'<div class="bridge">{rest}</div></details>')
    return f"""<section class="band band-surface">
  <div class="wrap">
    <div class="band-head">
      <span class="eyebrow">前職から探す</span>
      <h2>未経験でも、ゼロからではない</h2>
      <p class="lede">介護に入る人の3人に1人は他業種から。前職はここで活きます。</p>
    </div>
    {inner}
  </div>
</section>"""


def sec_shokushu_guide(p):
    # 平均月給は6職種を見比べる数字なので、テキストで並べずバーで比較できるようにする。
    # 目盛は0起点（途中から始めると差が実際より大きく見えるため）。
    SCALE = 35.0
    cards = []
    for k, name, short, _c, cnt, pay, desc in D.SHOKUSHU:
        val = float(pay.replace("万円", ""))
        w = round(val / SCALE * 100)
        cards.append(f"""<a class="guide" data-s="{e(k)}" href="list.html">
      <span class="guide-name">{e(name)}</span>
      <span class="guide-pay">
        <span class="gp-bar"><i style="width:{w}%"></i></span>
        <b>{e(pay)}</b>
      </span>
      <span class="guide-stats"><span>求人 <b>{fmt(cnt)}</b>件</span></span>
      <span class="guide-desc">{e(desc)}</span>
    </a>""")
    return f"""<section class="band">
  <div class="wrap">
    <div class="band-head">
      <span class="eyebrow">職種から探す</span>
      <h2>今の資格で、どこまで狙えるか</h2>
      <p class="lede">バーの長さが平均月給です（0〜35万円で表示）。数値はデモ用サンプルです。</p>
    </div>
    <div class="guidegrid">{''.join(cards)}</div>
  </div>
</section>"""


def sec_shisetsu(p):
    # 7種は件数に3倍近い差がある。数字だけでは規模差が伝わらないためバーを添える
    mxs = max(x[4] for x in D.SHISETSU)
    cards = []
    for k, name, short, photo, cnt, yakin, desc in D.SHISETSU:
        w = round(cnt / mxs * 100)
        cards.append(f"""<a class="shcard" href="list.html">
      <span class="shcard-photo"><img src="{img(photo)}" alt="{e(name)}のイメージ写真" loading="lazy" width="600" height="450"></span>
      <span class="shcard-in">
        <span class="shcard-name">{e(name)}</span>
        <span class="shcard-yakin">{e(yakin)}</span>
        <span class="shcard-desc">{e(desc)}</span>
        <span class="shcard-count">
          <span class="shc-bar"><i style="width:{w}%"></i></span>
          掲載求人 <b>{fmt(cnt)}</b>件
        </span>
      </span>
    </a>""")
    return f"""<section class="band band-tint">
  <div class="wrap">
    <div class="band-head">
      <span class="eyebrow">施設種別から探す</span>
      <h2>どこで働くかで、1日は変わる</h2>
      <p class="lede">夜勤の有無とあわせて選んでください。</p>
    </div>
    <div class="shisetsu-grid">{''.join(cards)}</div>
  </div>
</section>"""


def sec_voices(p):
    boxes = []
    for t in D.TESTIMONIALS:
        stars = "★" * t["rating"] + "☆" * (5 - t["rating"])
        boxes.append(f"""<article class="voicebox">
      <div class="voice-meta">
        <span class="who">{e(t['age'])}・{e(t['pref'])}</span>
        <span class="voice-stars" aria-label="5段階中{t['rating']}">{stars}</span>
      </div>
      <div class="voice-move">
        <span>{e(t['before'])}</span><span class="arrow">→</span><span class="to">{e(t['after'])}</span>
      </div>
      <p class="voice-body">{e(t['body'])}</p>
    </article>""")
    return f"""<section class="band" id="voices">
  <div class="wrap">
    <div class="band-head">
      <span class="eyebrow">利用した方の声</span>
      <h2>迷った人が、最後に何を見て決めたか</h2>
      <p class="lede">いまのあなたと近い状況だった方に伺いました。</p>
    </div>
    <div class="voicegrid">{''.join(boxes)}</div>
    <p class="voice-note">※本ページはデザイン提案用のデモです。掲載している声はすべて架空のサンプルであり、実在の人物のものではありません。</p>
  </div>
</section>"""


def sec_story_jobs(p):
    """Bは1件あたりの面積が大きいので5件に絞る。ただしID順の先頭5件を取ると
    夜勤なしばかりになり、サイト全体の比率（夜勤なし33%）と食い違うため、
    夜勤なし・あり・専従を1件ずつ先に確保してから残りを埋める。"""
    pool = [j for j in D.JOBS if j["has_timeline"] or j["has_voice"]]
    picked = []
    for k in ("none", "some", "senju"):
        first = next((j for j in pool if j["yakin"] == k), None)
        if first:
            picked.append(first)
    for j in pool:
        if len(picked) >= 5:
            break
        if j not in picked:
            picked.append(j)
    jobs = sorted(picked, key=lambda j: j["id"])[:5]
    return f"""<section class="band band-tint">
  <div class="wrap">
    <div class="band-head">
      <span class="eyebrow">掲載中の求人</span>
      <h2>読んでから決められる求人</h2>
      <p class="lede">条件表では分からない部分を、施設に書いてもらいました。</p>
    </div>
    {''.join(card_story(j) for j in jobs)}
    <p class="band-more"><a class="btn btn-ghost" href="list.html">すべての求人を見る（{fmt(D.TOTAL_JOBS)}件）</a></p>
  </div>
</section>"""


def sec_table_jobs(p):
    return f"""<section class="band">
  <div class="wrap">
    <div class="band-head">
      <span class="eyebrow">新着求人</span>
      <h2>同じ並びで、まとめて比べる</h2>
      <p class="lede">給与・夜勤・掲載情報を横一列に。更新日の新しい順に{len(D.JOBS)}件。</p>
    </div>
    {table_jobs(sorted(D.JOBS, key=lambda j: j['posted_days']))}
    <p class="band-more"><a class="btn btn-ghost" href="list.html">すべての求人を見る（{fmt(D.TOTAL_JOBS)}件）</a></p>
  </div>
</section>"""


def sec_popular(p):
    # 件数はバーの長さで見せる。上位3件だけ出し、残りは開いたときに見せる。
    counts = [4820, 3892, 3186, 2148, 1862, 1420, 1204, 986, 824, 756, 634, 512]
    mx = counts[0]

    def row(i, cond):
        top = " top" if i < 3 else ""
        w = round(counts[i] / mx * 100)
        return f"""<a class="rank{top}" href="list.html">
      <span class="rank-fill" style="width:{w}%"></span>
      <span class="rank-no">{i+1}</span>
      <span class="rank-name">{e(cond)}</span>
      <span class="rank-count">{fmt(counts[i])}件</span>
    </a>"""

    shown = "".join(row(i, c) for i, c in enumerate(D.CONDITION_CHIPS[:3]))
    rest = "".join(row(i + 3, c) for i, c in enumerate(D.CONDITION_CHIPS[3:12]))
    return f"""<section class="band band-surface">
  <div class="wrap">
    <div class="band-head">
      <span class="eyebrow">人気の条件</span>
      <h2>他の人は、まず何で絞っているか</h2>
      <p class="lede">バーの長さが指定回数です。</p>
    </div>
    <div class="ranklist">{shown}</div>
    <details class="more">
      <summary><span class="more-open">4位以下も見る（9件）</span><span class="more-close">閉じる</span></summary>
      <div class="ranklist">{rest}</div>
    </details>
  </div>
</section>"""


def sec_souba(p):
    maxpay = 30.8
    rows = []
    for shikaku, exp, pay, nen, cnt, memo in D.SHIKAKU_SOUBA:
        val = float(pay.replace("万円", ""))
        w = round(val / maxpay * 100)
        rows.append(f"""<tr>
      <th scope="row">{e(shikaku)}</th>
      <td class="n">{e(exp)}</td>
      <td class="n pay">{e(pay)}<span class="souba-gauge" style="width:{w}%"></span></td>
      <td class="n">{e(nen)}</td>
      <td class="n">{fmt(cnt)}件</td>
      <td class="memo">{e(memo)}</td>
    </tr>""")
    return f"""<section class="band">
  <div class="wrap">
    <div class="band-head">
      <span class="eyebrow">資格別の給与相場</span>
      <h2>今の資格の相場と、次の資格での伸び</h2>
      <p class="lede">無資格からケアマネまで、月給でおよそ10万円の幅があります。<a href="column-shikaku.html">資格と給与の関係はこちら</a></p>
    </div>
    <div class="soubawrap"><table class="souba">
      <caption class="sr-only">資格別の平均月給・平均年収・求人件数</caption>
      <thead><tr><th scope="col">資格</th><th scope="col">想定経験</th><th scope="col">平均月給</th>
        <th scope="col">平均年収</th><th scope="col">求人数</th><th scope="col">備考</th></tr></thead>
      <tbody>{''.join(rows)}</tbody>
    </table></div>
    <p class="souba-note">{e(D.UPDATED)}時点。平均月給は基本給に各種手当（処遇改善手当・資格手当）を含み、賞与・夜勤手当は含みません。1件の求人が複数の資格に該当する場合があるため、資格別の求人数の合計は掲載求人数（{fmt(D.TOTAL_JOBS)}件）と一致しません。掲載している数値はデモ用のサンプルです。</p>
  </div>
</section>"""


def sec_area(p):
    # 件数の大小はバーで見せる。上位5件だけ出し、残りは開いたときに見せる。
    counts = [842, 586, 548, 452, 418, 396, 364, 312, 298, 186]
    mx = counts[0]

    def row(i, a):
        w = round(counts[i] / mx * 100)
        return (f'<a href="list.html"><span class="ar-fill" style="width:{w}%"></span>'
                f'<span class="ar-n">{e(a)}</span>'
                f'<span class="c">{fmt(counts[i])}</span></a>')

    shown = "".join(row(i, a) for i, a in enumerate(D.AREA_CHIPS[:5]))
    rest = "".join(row(i + 5, a) for i, a in enumerate(D.AREA_CHIPS[5:]))
    return f"""<section class="band band-tint">
  <div class="wrap">
    <div class="band-head">
      <span class="eyebrow">エリアから探す</span>
      <h2>都道府県別の掲載件数</h2>
    </div>
    <div class="arealist">{shown}</div>
    <details class="more">
      <summary><span class="more-open">6位以下も見る（5件）</span><span class="more-close">閉じる</span></summary>
      <div class="arealist">{rest}</div>
    </details>
  </div>
</section>"""


def sec_columns(p):
    # トップは3枚まで（3カラムグリッドで1枚だけ余るのを避ける）。全件は column.html に出す。
    cards = "".join(f"""<a class="colcard" href="{c['slug']}.html">
      <span class="cmeta"><span class="ccat">{e(c['cat'])}</span><span>{e(c['read'])}</span></span>
      <h3>{e(c['title'])}</h3>
      <p>{e(c['excerpt'])}</p>
    </a>""" for c in D.COLUMNS[:3])
    return f"""<section class="band">
  <div class="wrap">
    <div class="band-head">
      <span class="eyebrow">お仕事コラム</span>
      <h2>迷っている間に、読んでおくこと</h2>
    </div>
    <div class="colgrid">{cards}</div>
    <p class="band-more"><a class="btn btn-ghost" href="column.html">コラム一覧を見る</a></p>
  </div>
</section>"""


def sec_faq(p):
    cat, qas = D.FAQ[1]  # 夜勤・働き方
    items = "".join(f"""<details><summary>{e(q)}</summary><p class="ans">{e(a)}</p></details>"""
                    for q, a in qas)
    return f"""<section class="band band-tint">
  <div class="wrap-narrow">
    <div class="band-head">
      <span class="eyebrow">よくある質問</span>
      <h2>{e(cat)}</h2>
    </div>
    <div class="faqlist">{items}</div>
    <p class="band-more"><a class="btn btn-ghost" href="faq.html">すべての質問を見る</a></p>
  </div>
</section>"""


def sec_cta(p):
    return f"""<section class="ctaband">
  <div class="wrap">
    <h2>迷っている段階で、応募して大丈夫です</h2>
    <p>会員登録も、面談も、営業電話もありません。届くのは応募先からの連絡だけです。</p>
    <div class="btns">
      <a class="btn btn-main" href="list.html">求人を探す</a>
      <a class="btn btn-ghost" href="faq.html">応募の流れを見る</a>
    </div>
  </div>
</section>"""


SECTION_FN = {
    "yakin": lambda p: "",  # ヒーローで出力済み
    "coverage": sec_coverage,
    "prevjob": sec_prevjob,
    "shindan": sec_shindan,
    "matrix": sec_matrix,
    "rails": sec_rails,
    "shokushu_guide": sec_shokushu_guide,
    "shisetsu": sec_shisetsu,
    "voices": sec_voices,
    "story_jobs": sec_story_jobs,
    "table_jobs": sec_table_jobs,
    "popular": sec_popular,
    "souba": sec_souba,
    "area": sec_area,
    "columns": sec_columns,
    "faq": sec_faq,
    "cta": sec_cta,
}


# ================================================================ index.html
def page_index(p):
    body = [hero(p)]
    for key in p["sections"]:
        body.append(SECTION_FN[key](p))
    return (
        head(p, "index", f"{D.BRAND_JA}｜{D.TAGLINE}",
             f"{D.TAGLINE}。{D.TOTAL_JOBS:,}件の求人を、夜勤の有無・職種・施設種別・こだわり条件から探せます。会員登録不要で直接応募できます。",
             "index")
        + masthead("")
        + '<div id="resumeMount"></div>'
        + "<main>" + "".join(body) + '<div id="recentMount"></div>' + "</main>"
        + footer() + mobilebar() + tail()
    )


# ================================================================= list.html
def page_list(p):
    def pillgroup(name, values):
        return "".join(
            f'<label class="pill"><input type="checkbox" name="{name}" value="{e(v)}">{e(v)}</label>'
            for v in values
        )

    filt = f"""<aside class="filter">
  <h2>条件で絞り込む</h2>
  <form action="list.html" method="get">
    <div class="fgroup"><h3><label for="fkw">キーワード</label></h3>
      <input type="text" id="fkw" name="kw" placeholder="施設名・駅名・資格名"></div>
    <div class="fgroup"><h3>夜勤</h3><div class="pillset">
      {pillgroup("yakin", ["夜勤なし", "日勤のみ", "夜勤あり", "夜勤専従"])}</div></div>
    <div class="fgroup"><h3>職種</h3><div class="pillset">
      {pillgroup("shokushu", [s[2] for s in D.SHOKUSHU])}</div></div>
    <div class="fgroup"><h3>施設種別</h3><div class="pillset">
      {pillgroup("shisetsu", [s[2] for s in D.SHISETSU])}</div></div>
    <div class="fgroup"><h3>雇用形態</h3><div class="pillset">
      {pillgroup("emp", D.EMPLOYMENT_CHIPS)}</div></div>
    <div class="fgroup"><h3>エリア</h3><div class="pillset">
      {pillgroup("area", D.AREA_CHIPS)}</div></div>
    <div class="fgroup"><h3>こだわり条件</h3><div class="pillset">
      {pillgroup("cond", D.CONDITION_CHIPS)}</div></div>
    <button class="btn btn-main btn-wide" type="submit">この条件で絞り込む</button>
  </form>
</aside>"""

    pager = """<nav class="pager" aria-label="ページ送り">
  <span class="off">前へ</span><span class="on">1</span>
  <span class="off">2</span><span class="off">3</span><span class="off">…</span>
  <span class="off">次へ</span>
</nav>
<p class="matrix-note">※デモページのため、ページ送りと絞り込みは動作しません。</p>"""

    return (
        head(p, "list", "求人一覧", f"介護施設の求人{D.TOTAL_JOBS:,}件を、夜勤の有無・職種・施設種別・こだわり条件から絞り込めます。", "list")
        + masthead("list.html")
        + crumbs([("トップ", "index.html"), ("求人一覧", None)])
        + f"""<main><div class="wrap listwrap">
  {filt}
  <div>
    <div class="listhead">
      <h1>介護の求人一覧</h1>
      <p class="hit">該当 <b>{fmt(D.TOTAL_JOBS)}</b>件中 1〜{len(D.JOBS)}件</p>
      <div class="sortwrap"><label for="sortSelect">並び替え</label>
        <select id="sortSelect" name="sort">
          <option>更新日が新しい順</option><option>給与が高い順</option>
          <option>夜勤なしを優先</option><option>掲載情報が多い順</option>
        </select></div>
    </div>
    {render_cards(p, D.JOBS)}
    {pager}
  </div>
</div></main>"""
        + footer() + mobilebar() + tail()
    )


# ================================================================== job page
def block_paybreak(j):
    rows = "".join(f"<tr><th scope=\"row\">{e(k)}</th><td>{e(v)}</td></tr>" for k, v in j["pay_rows"])
    return f"""<section class="jobsec">
  <h2>給与の内訳</h2>
{pay_stack(j)}  <table class="paybreak"><caption class="sr-only">給与の内訳</caption><tbody>{rows}</tbody></table>
  <p class="paymodel">※ {e(j['pay_model'])}</p>
</section>"""


def pay_stack(j):
    """モデル月収の内訳を積み上げバーで見せる。

    基本給と手当の比率が絵で分かると「夜勤を外すといくら下がるか」が
    一目で読める。時給制の求人は内訳が分解できないため出さない。
    幅は flex-grow に実額をそのまま渡すので、丸め誤差なく合計と一致する。
    """
    st = j.get("pay_stack") or []
    if len(st) < 2:
        return ""
    total = sum(v for _, v in st)
    # 各項目を独立に四捨五入すると凡例の合計が99%や101%になるため、
    # 最大剰余法で配分し、表示上の合計をきっちり100%にする
    raw = [v / total * 100 for _, v in st]
    pcts = [int(x) for x in raw]
    for i in sorted(range(len(st)), key=lambda i: raw[i] - pcts[i], reverse=True)[:100 - sum(pcts)]:
        pcts[i] += 1

    segs, legs = [], []
    for i, (label, v) in enumerate(st):
        night = "夜勤" in label
        cls = "night" if night else ("t1" if i == 0 else ("t2" if i == 1 else "t3"))
        segs.append(
            f'<span class="ps-seg {cls}" style="flex-grow:{v}" '
            f'title="{e(label)} {v:,}円（{pcts[i]}%）"></span>'
        )
        legs.append(
            f'<li><i class="ps-key {cls}"></i><span class="ps-k">{e(label)}</span>'
            f'<b>{v:,}円</b><span class="ps-p">{pcts[i]}%</span></li>'
        )
    night_sum = sum(v for label, v in st if "夜勤" in label)
    note = (f'<p class="ps-note">夜勤手当を除くと <b>{total - night_sum:,}円</b>／月になります。</p>'
            if night_sum else "")
    return f"""  <div class="paystack">
    <p class="ps-head"><span>モデル月収の内訳</span><b>{total:,}円</b></p>
    <div class="ps-bar" role="img" aria-label="モデル月収{total:,}円の内訳。{e('、'.join(f'{k} {v:,}円' for k, v in st))}">{''.join(segs)}</div>
    <ul class="ps-legend">{''.join(legs)}</ul>
    {note}
  </div>
"""


def block_work(j):
    rows = "".join(f"<tr><th scope=\"row\">{e(k)}</th><td>{e(v)}</td></tr>" for k, v in j["work_rows"])
    return f"""<section class="jobsec">
  <h2>仕事内容</h2>
  <table class="spectable"><caption class="sr-only">仕事内容</caption><tbody>{rows}</tbody></table>
</section>"""


def block_req(j):
    rows = "".join(f"<tr><th scope=\"row\">{e(k)}</th><td>{e(v)}</td></tr>" for k, v in j["req_rows"])
    extra = f"""<tr><th scope="row">勤務地</th><td>{e(j['area'])}</td></tr>
    <tr><th scope="row">アクセス</th><td>{e(j['access'])}</td></tr>"""
    return f"""<section class="jobsec">
  <h2>募集要項</h2>
  <table class="spectable"><caption class="sr-only">募集要項</caption><tbody>{rows}{extra}</tbody></table>
</section>"""


def _mins(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def _mins_seq(tl):
    """時刻の並びを通し分に直す。夜勤は日付をまたぐため、時刻が前の項目より
    小さくなったところで24時間足す。そのまま引き算すると所要時間が負になり、
    帯の幅が壊れる。"""
    out, add, prev = [], 0, None
    for row in tl:
        m = _mins(row[0])
        if prev is not None and m < prev:
            add += 24 * 60
        prev = m
        out.append(m + add)
    return out


def _dur_label(m):
    h, mi = divmod(m, 60)
    if h and mi:
        return f"{h}時間{mi}分"
    if h:
        return f"{h}時間"
    return f"{mi}分"


def block_timeline(j):
    """1日の流れ。時刻の箇条書きだけでは時間の偏りが読み取れないため、
    先に実時間の幅を持った帯を出し、そのあとに各項目の詳細を並べる。"""
    if not j["has_timeline"]:
        return ""
    tl = j["timeline"]
    at = _mins_seq(tl)
    span = max(at[-1] - at[0], 1)

    # 帯：各項目から次の項目までを、実際の所要時間に比例した幅で並べる
    segs = []
    for i in range(len(tl) - 1):
        t, label, _d = tl[i]
        dur = at[i + 1] - at[i]
        w = dur / span * 100
        kind = " rest" if any(x in label for x in ("休憩", "昼食", "仮眠")) else ""
        segs.append(
            f'<span class="tb-seg{kind}" style="width:{w:.2f}%" '
            f'title="{e(t)}〜{e(tl[i + 1][0])}　{e(label)}（{_dur_label(dur)}）">'
            f'<span class="tb-in">{e(label)}</span></span>'
        )

    rows = []
    for i, (t, l, d) in enumerate(tl):
        dur = ""
        if i < len(tl) - 1:
            dur = f'<span class="daily-dur">{_dur_label(at[i + 1] - at[i])}</span>'
        rows.append(f"""<div class="daily-row">
    <div class="daily-time">{e(t)}{dur}</div>
    <div class="daily-axis" aria-hidden="true"></div>
    <div class="daily-body"><p class="daily-label">{e(l)}</p>
      {f'<p class="daily-desc">{e(d)}</p>' if d else ''}</div>
  </div>""")

    return f"""<section class="jobsec">
  <h2>1日の流れ</h2>
  <p class="daily-cap">{e(j['timeline_label'])}</p>
  <div class="timeband">
    <div class="tb-bar">{''.join(segs)}</div>
    <div class="tb-ends"><span>{e(tl[0][0])} {e(tl[0][1])}</span>
      <span>{e(tl[-1][0])} {e(tl[-1][1])}</span></div>
    <p class="tb-note">出勤から退勤まで {_dur_label(span)}。帯の幅が各業務にかかる時間です。</p>
  </div>
  <div class="daily">{''.join(rows)}</div>
</section>"""


def block_voice(j):
    if not j["has_voice"]:
        return ""
    v = j["voice"]
    return f"""<section class="jobsec">
  <h2>この職場で働く人の声</h2>
  <div class="voice-inline">
    <p class="who">{e(v['name'])}</p>
    <p class="prev">{e(v['years'])}</p>
    <p class="body">{e(v['body'])}</p>
  </div>
  <p class="gallery-note">※デモページのため、掲載している声は架空のサンプルです。</p>
</section>"""


def block_office(j):
    rows = "".join(f"<tr><th scope=\"row\">{e(k)}</th><td>{e(v)}</td></tr>" for k, v in j["office"])
    return f"""<section class="jobsec">
  <h2>事業所の情報</h2>
  <table class="spectable"><caption class="sr-only">事業所の情報</caption><tbody>{rows}</tbody></table>
</section>"""


def block_selection(j):
    steps = "".join(f'<div class="flowstep"><span>{e(s)}</span></div>' for s in j["selection"])
    return f"""<section class="jobsec">
  <h2>応募から入職までの流れ</h2>
  <div class="flowsteps">{steps}</div>
</section>"""


def block_gallery(j):
    n = min(j["photo_count"], 4)
    thumbs = "".join(
        f'<img src="{img(j["photo"])}" alt="{e(j["facility"])}の施設写真{i+1}" loading="lazy" width="400" height="300">'
        for i in range(n)
    )
    return f"""<div class="gallery-lead">
    <img src="{img(j['photo'])}" alt="{e(j['facility'])}の施設写真" width="960" height="480"></div>
  <div class="gallery">{thumbs}</div>
  <p class="gallery-note">掲載写真 {j['photo_count']}枚（デモページのためイメージ写真を繰り返し表示しています）</p>"""


def block_related(p, j):
    rel = [D.JOBS_BY_ID[i] for i in j["related"]]
    if p["card"] == "table":
        inner = table_jobs(rel)
    elif p["card"] == "story":
        inner = "".join(card_story(r) for r in rel)
    else:
        inner = "".join(card_dense(r) for r in rel)
    return f"""<section class="jobsec">
  <h2>似ている求人</h2>
  {inner}
</section>"""


def block_jobfaq():
    qas = [
        ("会員登録をしないと応募できませんか？", "会員登録は不要です。応募フォームに必要事項を入力いただくだけで、掲載施設へ直接応募できます。"),
        ("応募後、どのくらいで連絡が来ますか？", "掲載施設の採用担当者より、3営業日以内にご連絡します。"),
        ("求人内容について質問だけしたいのですが？", "応募フォームの「ご質問・ご要望」欄にご記入ください。応募の可否を決める前の質問としてお伝えします。"),
    ]
    items = "".join(f"<details><summary>{e(q)}</summary><p class=\"ans\">{e(a)}</p></details>" for q, a in qas)
    return f"""<section class="jobsec">
  <h2>応募に関するよくある質問</h2>
  <div class="faqlist">{items}</div>
</section>"""


def job_sidebox(j):
    return f"""<aside class="jobside">
  <div class="sidebox">
    <p class="s-label">給与</p>
    <p class="s-pay">{e(j['pay_main'])}</p>
    <dl>
      <div><dt>雇用形態</dt><dd>{e(j['employment'])}</dd></div>
      <div><dt>勤務シフト</dt><dd>{e(j['shift'])}</dd></div>
      <div><dt>勤務地</dt><dd>{e(j['pref'])}</dd></div>
      <div><dt>施設種別</dt><dd>{e(shisetsu_of(j)[1])}</dd></div>
      <div><dt>更新日</dt><dd>{e(j['updated'])}</dd></div>
    </dl>
    <a class="btn btn-main btn-wide" href="{D.apply_file(j['id'])}">この求人に応募する</a>
    <a class="keep" href="#keep">キープする（ブラウザに保存）</a>
  </div>
  <div class="sidebox">
    <h2>この求人に載っている情報</h2>
    <div class="jt-has">
      <span class="{'on' if j['has_timeline'] else 'off'}">{'✓' if j['has_timeline'] else '−'} 1日の流れ</span>
      <span class="{'on' if j['has_voice'] else 'off'}">{'✓' if j['has_voice'] else '−'} 働く人の声</span>
      <span class="on">✓ 給与の内訳</span>
      <span class="on">✓ 職員構成</span>
      <span class="on">✓ 選考プロセス</span>
      <span class="on">✓ 写真{j['photo_count']}枚</span>
    </div>
  </div>
</aside>"""


def page_job(p, j):
    s = shoku_of(j)
    si = SHOKU_IDX[j["shokushu"]]
    meta = f"""<div class="jobmeta">
    <span class="chip-shoku sk{si}">{e(s[2])}</span>
    <span class="chip-yakin {yakin_class(j)}">{e(j['shift'])}</span>
    <span class="chip-emp">{e(j['employment'])}</span>
    <span class="jrow-updated">{e(j['updated'])}更新</span>
  </div>"""

    if p["job_hero"] == "gallery":
        top = f"""{block_gallery(j)}
  <h1 class="jobtitle">{e(j['title'])}／{e(j['facility'])}</h1>
  {meta}
  <p class="jobcatch">{e(j['catch'])}</p>"""
        order = [block_timeline, block_voice, block_work, block_paybreak, block_req,
                 block_office, block_selection]
    elif p["job_hero"] == "compare":
        top = f"""<h1 class="jobtitle">{e(j['title'])}／{e(j['facility'])}</h1>
  {meta}
  <p class="jobcatch">{e(j['catch'])}</p>"""
        order = [block_req, block_paybreak, block_work, block_office,
                 block_timeline, block_voice, block_selection]
    else:
        top = f"""<h1 class="jobtitle">{e(j['title'])}／{e(j['facility'])}</h1>
  {meta}
  <p class="jobcatch">{e(j['catch'])}</p>"""
        order = [block_work, block_paybreak, block_req, block_timeline,
                 block_voice, block_office, block_selection]

    blocks = "".join(fn(j) for fn in order)
    return (
        head(p, "job", f"{j['title']}／{j['facility']}",
             f"{j['facility']}の{j['title']}（{j['employment']}）の求人。{j['pay_main']}、{j['shift']}、{j['area']}。会員登録不要で直接応募できます。",
             "job",
             f' data-job-title="{e(j["title"])}" data-job-facility="{e(j["facility"])}"'
             f' data-job-url="{D.job_file(j["id"])}"')
        + masthead("list.html")
        + crumbs([("トップ", "index.html"), ("求人一覧", "list.html"), (j["facility"], None)])
        + f"""<main><div class="wrap jobwrap">
  <div class="jobmain">
    {top}
    {blocks}
    {block_jobfaq()}
    {block_related(p, j)}
  </div>
  {job_sidebox(j)}
</div></main>"""
        + footer() + mobilebar(D.apply_file(j["id"]), "この求人に応募する") + tail()
    )


# ================================================================ apply page
def page_apply(p, j):
    shisetsu_tiles = "".join(
        f'<label class="tile"><input type="checkbox" name="shisetsu" value="{e(s[1])}">{e(s[1])}</label>'
        for s in D.SHISETSU
    )
    shikaku_tiles = "".join(
        f'<label class="tile"><input type="radio" name="shikaku" value="{e(k[0])}">{e(k[0])}</label>'
        for k in D.SHIKAKU_SOUBA
    )
    pref_opts = "".join(f"<option>{e(a)}</option>" for a in D.AREA_CHIPS)
    years = "".join(f"<option>{y}年</option>" for y in range(1955, 2009))
    return (
        head(p, "apply", f"{j['facility']}に応募する",
             f"{j['facility']}の{j['title']}に、会員登録なしで応募できます。5つのステップで完了します。", "apply")
        + masthead("list.html")
        + crumbs([("トップ", "index.html"), ("求人一覧", "list.html"),
                  (j["facility"], D.job_file(j["id"])), ("応募する", None)])
        + f"""<main><div class="wrap-narrow applywrap">
  <h1 class="sr-only">{e(j['facility'])}の{e(j['title'])}に応募する</h1>
  <div class="applyhead">
    <p class="to">応募先</p>
    <p class="name">{e(j['facility'])}／{e(j['title'])}（{e(j['employment'])}）</p>
    <p class="pay">{e(j['pay_main'])}｜{e(j['shift'])}｜{e(j['pref'])}</p>
  </div>
  <ol class="stepbar">
    <li class="on">1 希望する施設</li><li class="on">2 保有資格</li>
    <li class="on">3 希望時期</li><li class="on">4 プロフィール</li><li class="on">5 連絡先</li>
  </ol>
  <form action="#" method="post">
    <section class="qblock">
      <h2>1. 希望する施設種別</h2>
      <p class="qnote">複数選べます。この求人以外にも近い条件の求人があればご案内します。</p>
      <div class="tilegrid">{shisetsu_tiles}</div>
    </section>
    <section class="qblock">
      <h2>2. 保有している資格</h2>
      <p class="qnote">資格がなくても応募いただけます。</p>
      <div class="tilegrid">{shikaku_tiles}</div>
    </section>
    <section class="qblock">
      <h2>3. 入職を希望する時期</h2>
      <div class="fieldrow"><label for="timing">希望時期<span class="req">必須</span></label>
        <select id="timing" name="timing"><option>すぐにでも</option><option>1ヶ月以内</option>
          <option>3ヶ月以内</option><option>半年以内</option><option>良い求人があれば</option></select></div>
      <div class="fieldrow"><label for="pref">希望勤務地（都道府県）<span class="req">必須</span></label>
        <select id="pref" name="pref">{pref_opts}</select></div>
    </section>
    <section class="qblock">
      <h2>4. お名前と生まれ年</h2>
      <div class="fieldrow"><label for="name">お名前<span class="req">必須</span></label>
        <input type="text" id="name" name="name" autocomplete="name" placeholder="介護 花子"></div>
      <div class="fieldrow"><label for="birth">生まれ年<span class="req">必須</span></label>
        <select id="birth" name="birth">{years}</select></div>
    </section>
    <section class="qblock">
      <h2>5. ご連絡先</h2>
      <div class="fieldrow"><label for="tel">電話番号<span class="req">必須</span></label>
        <input type="tel" id="tel" name="tel" autocomplete="tel" placeholder="09012345678">
        <span class="hint">応募先の施設から直接ご連絡します。</span></div>
      <div class="fieldrow"><label for="mail">メールアドレス<span class="req">必須</span></label>
        <input type="email" id="mail" name="mail" autocomplete="email" placeholder="example@example.com"></div>
      <div class="fieldrow"><label for="memo">ご質問・ご要望（任意）</label>
        <textarea id="memo" name="memo" rows="4" placeholder="夜勤の回数について確認したい、など"></textarea></div>
    </section>
    <div class="applyfoot">
      <a class="btn btn-ghost" href="{D.job_file(j['id'])}">求人内容に戻る</a>
      <button class="btn btn-main" type="submit">この内容で応募する</button>
    </div>
    <p class="applynote">会員登録は不要です。ご入力いただいた情報は応募先の施設にのみ提供されます。<br>
      送信をもって<a href="terms.html">利用規約</a>と<a href="privacy.html">プライバシーポリシー</a>に同意したものとみなします。<br>
      ※デモページのため、送信は行われません。</p>
  </form>
</div></main>"""
        + footer() + mobilebar(D.job_file(j["id"]), "求人内容に戻る") + tail()
    )


# ================================================================== faq.html
def page_faq(p):
    blocks = []
    for i, (cat, qas) in enumerate(D.FAQ):
        items = "".join(f"<details><summary>{e(q)}</summary><p class=\"ans\">{e(a)}</p></details>"
                        for q, a in qas)
        first = " first" if i == 0 else ""
        blocks.append(f'<h2 class="faqcat{first}">{e(cat)}</h2><div class="faqlist">{items}</div>')
    return (
        head(p, "faq", "よくある質問", "応募方法、夜勤・働き方、求人掲載、個人情報の取り扱いについてのよくある質問をまとめています。", "faq")
        + masthead("faq.html")
        + crumbs([("トップ", "index.html"), ("よくある質問", None)])
        + f"""<main><div class="wrap-narrow static">
  <h1>よくある質問</h1>
  <p>ご不明な点がありましたら、こちらをご確認ください。解決しない場合は<a href="contact-company.html">お問い合わせ</a>よりご連絡ください。</p>
  {''.join(blocks)}
</div></main>"""
        + footer() + mobilebar() + tail()
    )


# ================================================================ about.html
def page_about(p):
    covs = "".join(f"<li>{e(label)}（{got}/{total}件に掲載）</li>" for label, got, total, _n in D.coverage_stats())
    return (
        head(p, "about", "サイトについて", f"{D.BRAND_JA}は{D.TAGLINE}です。会員登録不要・直接応募の求人媒体としての方針と、掲載情報の考え方をご説明します。", "about")
        + masthead("about.html")
        + crumbs([("トップ", "index.html"), ("サイトについて", None)])
        + f"""<main><div class="wrap-narrow static">
  <h1>サイトについて</h1>
  <p>{e(D.BRAND_JA)}（{e(D.BRAND_EN)}）は、{e(D.TAGLINE)}です。介護職員・生活相談員・ケアマネージャー・サービス提供責任者・施設長・施設内看護師まで、介護施設で働くすべての職種の求人を扱っています。</p>

  <h2>会員登録は不要です</h2>
  <p>本サイトは求人媒体です。会員登録・ログインの仕組みはなく、気になった求人からそのまま掲載施設へ直接応募いただけます。キャリアアドバイザーによる面談や電話でのご提案、スカウトメールの配信は行っていません。</p>

  <h2>求人票に何が書かれているかを揃える</h2>
  <p>介護の求人は、同じ「介護職員・月給22万円」でも、夜勤の回数・職員の配置・記録業務のやり方によって働き方が大きく変わります。そのため掲載施設には、条件面に加えて次の項目の記入をお願いしています。</p>
  <ul class="bul">{covs}</ul>
  <p>いずれも任意項目のため、すべての求人に揃っているわけではありません。どの求人にどの情報が載っているかは、求人一覧と求人詳細ページで確認できます。</p>

  <h2>掲載内容の確認について</h2>
  <p>掲載前に募集内容を確認したうえで公開し、内容に変更があった場合は随時更新して、求人ごとに更新日を表示しています。求人票の内容と実際の労働条件が異なるとお気づきになった場合は、<a href="contact-company.html">お問い合わせ</a>よりご連絡ください。掲載施設に確認のうえ、必要に応じて修正または掲載を停止します。</p>

  <h2>運営者情報</h2>
  <p>本ページはデザイン提案用のデモです。掲載している求人・施設・数値・「働く人の声」はすべて架空のサンプルであり、実在の施設・人物とは関係ありません。運営者情報・所在地・連絡先は、公開時に実際の情報へ差し替えてください。</p>
</div></main>"""
        + footer() + mobilebar() + tail()
    )


# =============================================================== column pages
def page_column_index(p):
    cards = "".join(f"""<a class="colcard" href="{c['slug']}.html">
      <span class="cmeta"><span class="ccat">{e(c['cat'])}</span><span>{e(c['read'])}</span></span>
      <h2>{e(c['title'])}</h2>
      <p>{e(c['excerpt'])}</p>
    </a>""" for c in D.COLUMNS)
    return (
        head(p, "column", "お仕事コラム", "介護の夜勤の働き方、資格と給与の関係、未経験からの転職など、求人を探す前に知っておきたいことをまとめています。", "column")
        + masthead("column.html")
        + crumbs([("トップ", "index.html"), ("お仕事コラム", None)])
        + f"""<main><div class="wrap article">
  <h1>お仕事コラム</h1>
  <p class="lead">介護の求人を探すときに前提となる、夜勤の働き方・資格と給与の関係・未経験からの転職についてまとめています。</p>
  <div class="colgrid" style="margin-top:28px">{cards}</div>
</div></main>"""
        + footer() + mobilebar() + tail()
    )


def page_column(p, c):
    secs = "".join(f"<h2>{e(t)}</h2><p>{e(b)}</p>" for t, b in c["sections"])
    return (
        head(p, c["slug"], c["title"], c["excerpt"], "column-article")
        + masthead("column.html")
        + crumbs([("トップ", "index.html"), ("お仕事コラム", "column.html"), (c["title"], None)])
        + f"""<main><div class="wrap-narrow article">
  <h1>{e(c['title'])}</h1>
  <div class="ameta"><span>{e(c['cat'])}</span><span>{e(c['read'])}</span><span>{e(D.UPDATED)}更新</span></div>
  <p class="lead">{e(c['lead'])}</p>
  {secs}
  <div class="acta">
    <p>{e(c['cta'])}</p>
    <a class="btn btn-main" href="list.html">求人を探す</a>
  </div>
</div></main>"""
        + footer() + mobilebar() + tail()
    )


# ============================================================ 企業向け・規約
def page_contact(p):
    return (
        head(p, "contact-company", "掲載のご相談（企業様向け）",
             "介護施設・事業所の採用ご担当者様向けに、求人掲載のご相談を受け付けています。", "contact")
        + masthead("contact-company.html")
        + crumbs([("トップ", "index.html"), ("掲載のご相談", None)])
        + f"""<main><div class="wrap-narrow static">
  <h1>掲載のご相談（企業様向け）</h1>
  <p>介護施設・事業所の採用ご担当者様向けのページです。求職者の方は<a href="list.html">求人一覧</a>または<a href="faq.html">よくある質問</a>をご覧ください。</p>

  <h2>掲載できる求人</h2>
  <ul class="bul">
    <li>特別養護老人ホーム・介護老人保健施設・有料老人ホーム・サービス付き高齢者向け住宅・デイサービス・訪問介護などの介護事業所</li>
    <li>介護職員／生活相談員／ケアマネージャー／サービス提供責任者／施設長・管理者／施設内看護師</li>
    <li>正社員・契約社員・パート・派遣・業務委託</li>
  </ul>

  <h2>記入をお願いしている項目</h2>
  <p>求職者が応募前に判断できるよう、条件面に加えて次の項目のご記入をお願いしています。いずれも任意項目ですが、記入いただいた求人はトップページの専用の枠に掲載されます。</p>
  <ul class="bul">
    <li>月あたりの夜勤回数（夜勤がある場合）</li>
    <li>給与の内訳（基本給・処遇改善手当・資格手当・夜勤手当・賞与）</li>
    <li>1日の流れ（出勤から退勤までの時間割）</li>
    <li>職員構成（職種ごとの人数・平均年齢）</li>
    <li>在職中の職員のコメント（ご本人の了承が得られる場合）</li>
    <li>選考プロセス（応募から入職までの流れ）</li>
  </ul>

  <h2>お問い合わせ</h2>
  <form action="#" method="post">
    <div class="fieldrow"><label for="cname">法人・施設名<span class="req">必須</span></label>
      <input type="text" id="cname" name="cname"></div>
    <div class="fieldrow"><label for="cperson">ご担当者名<span class="req">必須</span></label>
      <input type="text" id="cperson" name="cperson"></div>
    <div class="fieldrow"><label for="cmail">メールアドレス<span class="req">必須</span></label>
      <input type="email" id="cmail" name="cmail" autocomplete="email"></div>
    <div class="fieldrow"><label for="ctel">電話番号</label>
      <input type="tel" id="ctel" name="ctel" autocomplete="tel"></div>
    <div class="fieldrow"><label for="cmemo">ご相談内容</label>
      <textarea id="cmemo" name="cmemo" rows="5"></textarea></div>
    <button class="btn btn-main" type="submit">この内容で問い合わせる</button>
    <p class="applynote">※デモページのため、送信は行われません。</p>
  </form>
</div></main>"""
        + footer() + mobilebar() + tail()
    )


def page_terms(p):
    return (
        head(p, "terms", "利用規約", "本サイトの利用規約（サンプル文面）です。", "terms")
        + masthead("")
        + crumbs([("トップ", "index.html"), ("利用規約", None)])
        + f"""<main><div class="wrap-narrow static">
  <h1>利用規約</h1>
  <p>本規約は、{e(D.BRAND_JA)}（以下「本サイト」）の利用条件を定めるものです。<strong>本文面はデザイン提案用のサンプルです。公開前に必ず法務確認のうえ差し替えてください。</strong></p>
  <h2>第1条（適用）</h2>
  <p>本規約は、本サイトの利用に関する一切の関係に適用されます。</p>
  <h2>第2条（サービス内容）</h2>
  <p>本サイトは、介護施設・事業所の求人情報を掲載し、利用者と掲載事業所とを直接つなぐ求人情報サービスです。職業紹介事業には該当せず、当社が利用者と事業所の間に立って雇用のあっせんを行うことはありません。</p>
  <h2>第3条（会員登録）</h2>
  <p>本サイトに会員登録の仕組みはありません。応募の際にご入力いただいた情報は、当該応募先への提供のみに利用します。</p>
  <h2>第4条（掲載情報について）</h2>
  <p>掲載する求人情報は、掲載事業所から提供された内容に基づいています。当社は掲載前に内容を確認し、変更の連絡を受けた場合は速やかに更新しますが、掲載内容の完全性・最新性を保証するものではありません。掲載内容と実際の労働条件が異なる場合は、お問い合わせよりご連絡ください。</p>
  <h2>第5条（禁止事項）</h2>
  <p>利用者は、法令または公序良俗に違反する行為、当社もしくは第三者の権利を侵害する行為、本サイトの運営を妨害する行為を行ってはなりません。</p>
  <h2>第6条（免責事項）</h2>
  <p>当社は、本サイトの利用によって利用者に生じた損害について、当社の故意または重過失による場合を除き、責任を負いません。</p>
  <h2>第7条（規約の変更）</h2>
  <p>当社は、必要と判断した場合には、利用者に通知することなく本規約を変更することができるものとします。</p>
</div></main>"""
        + footer() + mobilebar() + tail()
    )


def page_privacy(p):
    return (
        head(p, "privacy", "プライバシーポリシー", "本サイトの個人情報の取り扱いについて（サンプル文面）です。", "privacy")
        + masthead("")
        + crumbs([("トップ", "index.html"), ("プライバシーポリシー", None)])
        + f"""<main><div class="wrap-narrow static">
  <h1>プライバシーポリシー</h1>
  <p>{e(D.BRAND_JA)}（以下「本サイト」）における個人情報の取り扱いについて定めます。<strong>本文面はデザイン提案用のサンプルです。公開前に必ず法務確認のうえ差し替えてください。</strong></p>
  <h2>1. 取得する情報</h2>
  <p>応募フォームを通じて、お名前・生まれ年・電話番号・メールアドレス・希望条件・保有資格などをご入力いただきます。あわせて、アクセス解析のためにCookieおよび閲覧情報を取得します。</p>
  <h2>2. 利用目的</h2>
  <p>ご入力いただいた情報は、応募先の施設・事業所への応募内容の伝達、応募に関するご連絡、およびお問い合わせへの対応のために利用します。</p>
  <h2>3. 第三者への提供</h2>
  <p>応募情報は、利用者が応募した施設・事業所にのみ提供します。それ以外の第三者に提供することはありません。法令に基づく開示請求があった場合はこの限りではありません。</p>
  <h2>4. キープ機能について</h2>
  <p>求人の「キープ」は、ご利用中のブラウザ内に保存される仕組みです。当社のサーバーには送信されないため、ブラウザのデータを消去した場合や別の端末では保存内容が引き継がれません。</p>
  <h2>5. 安全管理措置</h2>
  <p>取得した個人情報について、漏えい・滅失・毀損の防止その他の安全管理のために必要かつ適切な措置を講じます。</p>
  <h2>6. 開示・訂正・削除の請求</h2>
  <p>ご本人からの開示・訂正・利用停止・削除のご請求には、本人確認のうえ、法令に従い対応します。お問い合わせよりご連絡ください。</p>
  <h2>7. お問い合わせ窓口</h2>
  <p>本ポリシーに関するお問い合わせ先は、公開時に実際の連絡先へ差し替えてください。</p>
</div></main>"""
        + footer() + mobilebar() + tail()
    )


# ============================================================== 画像の代替生成
PLACEHOLDER_LABELS = {
    "cat-tokuyou": "特別養護老人ホーム",
    "cat-roken": "介護老人保健施設",
    "cat-yuuryou": "有料老人ホーム",
    "cat-sakoju": "サービス付き高齢者向け住宅",
    "cat-day": "デイサービス",
    "cat-houmon": "訪問介護",
}
PLACEHOLDER_COLORS = ["#D9E3EC", "#DCE6DE", "#E8E1EC", "#EDE4D9", "#DDE7EA", "#E6DEDA"]

# パターン専用のヒーロー写真（横長）。カテゴリ写真とは別に1枚ずつ用意する。
HERO_PLACEHOLDERS = {
    "hero-a-yakin": ("夜勤帯のイメージ写真（パターンA）", "#1B3B54", 2400, 900),
    "hero-b-day": ("朝の共有スペースのイメージ写真（パターンB）", "#D8CFE0", 2000, 1250),
    "hero-c-genba": ("記録・手元のイメージ写真（パターンC）", "#3A4250", 2400, 640),
}


def write_placeholders():
    os.makedirs(IMGDIR, exist_ok=True)
    for i, (stem, label) in enumerate(PLACEHOLDER_LABELS.items()):
        if os.path.exists(os.path.join(IMGDIR, stem + ".jpg")):
            continue
        bg = PLACEHOLDER_COLORS[i % len(PLACEHOLDER_COLORS)]
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1000" width="1600" height="1000" role="img" aria-label="{label}のイメージ写真（未配置）">
  <rect width="1600" height="1000" fill="{bg}"/>
  <g fill="none" stroke="#FFFFFF" stroke-width="4" opacity="0.6">
    <circle cx="800" cy="452" r="52"/>
    <path d="M716 578c0-46 38-84 84-84s84 38 84 84z"/>
  </g>
  <text x="800" y="640" text-anchor="middle" font-family="sans-serif" font-size="30"
    fill="#5A6470">{label}</text>
  <text x="800" y="682" text-anchor="middle" font-family="sans-serif" font-size="21"
    fill="#8A939E">写真未配置（差し替え用プレースホルダー）</text>
</svg>
"""
        with open(os.path.join(IMGDIR, stem + ".svg"), "w", encoding="utf-8") as f:
            f.write(svg)

    for stem, (label, bg, w, h) in HERO_PLACEHOLDERS.items():
        if os.path.exists(os.path.join(IMGDIR, stem + ".jpg")):
            continue
        cx, cy = w / 2, h / 2
        fs_label = max(20, min(30, w // 55))
        fs_sub = max(15, fs_label - 9)
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{label}（未配置）">
  <rect width="{w}" height="{h}" fill="{bg}"/>
  <g fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.45">
    <circle cx="{cx}" cy="{cy - fs_label * 0.9}" r="{fs_label * 0.9}"/>
    <path d="M{cx - fs_label * 1.5} {cy + fs_label * 1.5}c0-{fs_label * 1.5} {fs_label * 0.7}-{fs_label * 2.7} {fs_label * 1.5}-{fs_label * 2.7}s{fs_label * 1.5} {fs_label * 1.2} {fs_label * 1.5} {fs_label * 2.7}z"/>
  </g>
  <text x="{cx}" y="{cy + fs_label * 3}" text-anchor="middle" font-family="sans-serif" font-size="{fs_label}"
    fill="#FFFFFF" opacity="0.85">{label}</text>
  <text x="{cx}" y="{cy + fs_label * 3 + fs_sub * 1.6}" text-anchor="middle" font-family="sans-serif" font-size="{fs_sub}"
    fill="#FFFFFF" opacity="0.6">写真未配置（差し替え用プレースホルダー）</text>
</svg>
"""
        with open(os.path.join(IMGDIR, stem + ".svg"), "w", encoding="utf-8") as f:
            f.write(svg)


# ===================================================================== 出力
def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    write_placeholders()
    total = 0
    for key, p in PATTERNS.items():
        out = os.path.join(ROOT, key)
        os.makedirs(out, exist_ok=True)
        set_css_ver(key)
        pages = {
            "index.html": page_index(p),
            "list.html": page_list(p),
            "faq.html": page_faq(p),
            "about.html": page_about(p),
            "column.html": page_column_index(p),
            "contact-company.html": page_contact(p),
            "terms.html": page_terms(p),
            "privacy.html": page_privacy(p),
        }
        for j in D.JOBS:
            pages[D.job_file(j["id"])] = page_job(p, j)
            pages[D.apply_file(j["id"])] = page_apply(p, j)
        for c in D.COLUMNS:
            pages[c["slug"] + ".html"] = page_column(p, c)
        for name, content in pages.items():
            write(os.path.join(out, name), content)
        total += len(pages)
        print(f"{key}: {len(pages)} pages")
    print("total", total)


if __name__ == "__main__":
    main()
