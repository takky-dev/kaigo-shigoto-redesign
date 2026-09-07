# -*- coding: utf-8 -*-
"""3パターンのデザイントークンと「構成」の定義

重要：3パターンの違いはトークン（色・書体）だけではなく、SECTIONS で定義される
トップページの構成そのもの、および card / hero で切り替わるコンポーネントの
作り自体が異なる。栄養士版の反省（同じ構成を色で塗り分けただけに見える）を
踏まえ、モジュールの取捨選択と並び順をパターンごとに変えている。
"""

PATTERNS = {
    # ------------------------------------------------------------------ A
    "pattern-a": {
        "name": "夜勤で選ぶ",
        "sub": "介護の求人選びで最初に決まる「夜勤をするかどうか」を入口に据えた構成。職種ごとに色を割り当て、職種×施設種別のクロスマトリクスで探せる。情報密度を最優先。",
        "concept_short": "夜勤軸・多色コーディング・高密度",
        # --- 構成 ---
        "hero": "yakin",
        "card": "dense",
        # 求人（rails）を上に置く。求人サイトで実物に届くまで説明が続くのを避けるため。
        "sections": ["yakin", "rails", "shindan", "prevjob", "coverage", "matrix", "shokushu_guide", "columns", "faq", "cta"],
        # 売りである「掲載情報の充実度」は、パネルで主張するのではなく
        # 実物の求人レールで見せる（ジョブメドレーが取っている方法）。
        # 未経験は直下の prevjob、資格は shokushu_guide が担うため重複を外した。
        "rails": ["yakin-none", "timeline", "voice"],
        "voice": False,
        "souba": False,
        "job_hero": "spec",       # 求人詳細の冒頭：スペック要約カード
        "list_layout": "dense",
        # --- トークン ---
        "font_body": "'BIZ UDPGothic', 'Hiragino Sans', 'Meiryo', sans-serif",
        "font_head": "'BIZ UDPGothic', 'Hiragino Sans', 'Meiryo', sans-serif",
        "font_num": "'Roboto Mono', ui-monospace, monospace",
        "gfont": "family=BIZ+UDPGothic:wght@400;700&family=Roboto+Mono:wght@500;700",
        "head_weight": "700",
        "head_spacing": "0.01em",
        "tokens": {
            "--bg": "#FFFFFF",
            "--bg-alt": "#F2F5F8",
            "--surface": "#FFFFFF",
            "--surface-alt": "#F7F9FB",
            "--ink": "#16222E",
            "--ink-soft": "#5B6B7A",
            "--ink-faint": "#8593A1",
            "--line": "#D9E1E8",
            "--line-strong": "#B4C2CE",
            "--accent": "#12496E",
            "--accent-strong": "#0B3450",
            "--accent-tint": "#E7EFF5",
            "--accent-ink": "#FFFFFF",
            "--warm": "#E0553C",
            "--warm-strong": "#C13A22",
            "--warm-tint": "#FDEDE9",
            "--radius-s": "3px",
            "--radius-m": "4px",
            "--radius-l": "6px",
            "--shadow": "0 1px 2px rgba(22,34,46,.10)",
            "--shadow-lift": "0 3px 10px rgba(22,34,46,.13)",
            # 職種カラー（コメディカルドットコム方式の多色コーディング）
            "--s1": "#1F7AC4", "--s1-tint": "#E6F1FA",
            "--s2": "#0E9488", "--s2-tint": "#E1F4F2",
            "--s3": "#8B5CC4", "--s3-tint": "#F0EAF9",
            "--s4": "#C4741F", "--s4-tint": "#FAF0E1",
            "--s5": "#2E7D46", "--s5-tint": "#E6F3EA",
            "--s6": "#C4406B", "--s6-tint": "#FAE9EF",
        },
    },
    # ------------------------------------------------------------------ B
    "pattern-b": {
        "name": "1日が見える",
        "sub": "「出勤から退勤までの1日」をヒーローに置き、働く人の声と現場の写真で読ませる構成。求人カードはキャッチコピー主導の縦型で、1件あたりの面積を大きく取る。",
        "concept_short": "1日のタイムライン・職員の声・読み物型",
        # --- 構成 ---
        "hero": "timeline",
        "card": "story",
        "sections": ["voices", "shindan", "story_jobs", "shisetsu", "coverage", "columns", "faq", "cta"],
        "rails": [],
        "voice": True,
        "souba": False,
        "job_hero": "gallery",    # 求人詳細の冒頭：写真ギャラリー＋キャッチコピー
        "list_layout": "story",
        # --- トークン ---
        "font_body": "'Noto Sans JP', 'Hiragino Sans', sans-serif",
        "font_head": "'Klee One', 'Hiragino Mincho ProN', serif",
        "font_num": "'Noto Sans JP', sans-serif",
        "gfont": "family=Klee+One:wght@400;600&family=Noto+Sans+JP:wght@400;500;700",
        "head_weight": "600",
        "head_spacing": "0.03em",
        "tokens": {
            "--bg": "#FBF8F4",
            "--bg-alt": "#F3EDE6",
            "--surface": "#FFFFFF",
            "--surface-alt": "#FAF5EF",
            "--ink": "#2E2833",
            "--ink-soft": "#6A6272",
            "--ink-faint": "#948D9C",
            "--line": "#E4DCE6",
            "--line-strong": "#CFC3D4",
            "--accent": "#6A5A8C",
            "--accent-strong": "#4E4069",
            "--accent-tint": "#EFEAF5",
            "--accent-ink": "#FFFFFF",
            "--warm": "#DE8A4F",
            "--warm-strong": "#BE6A2F",
            "--warm-tint": "#FBEEE0",
            "--radius-s": "8px",
            "--radius-m": "14px",
            "--radius-l": "22px",
            "--shadow": "0 2px 10px rgba(46,40,51,.06)",
            "--shadow-lift": "0 10px 28px rgba(46,40,51,.12)",
            "--s1": "#6A5A8C", "--s1-tint": "#EFEAF5",
            "--s2": "#6A5A8C", "--s2-tint": "#EFEAF5",
            "--s3": "#6A5A8C", "--s3-tint": "#EFEAF5",
            "--s4": "#6A5A8C", "--s4-tint": "#EFEAF5",
            "--s5": "#6A5A8C", "--s5-tint": "#EFEAF5",
            "--s6": "#6A5A8C", "--s6-tint": "#EFEAF5",
        },
    },
    # ------------------------------------------------------------------ C
    "pattern-c": {
        "name": "条件で絞る",
        "sub": "検索フォームそのものをヒーローに置き、資格別の給与相場表・人気条件ランキングなどデータで比較させる構成。求人一覧はテーブル的な行レイアウトで、条件を横並びで見比べられる。",
        "concept_short": "検索主導・給与相場データ・テーブル型",
        # --- 構成 ---
        "hero": "search",
        "card": "table",
        "sections": ["popular", "shindan", "souba", "prevjob", "table_jobs", "matrix", "area", "coverage", "columns", "faq", "cta"],
        "rails": [],
        "voice": True,
        "souba": True,
        "job_hero": "compare",    # 求人詳細の冒頭：給与内訳の比較テーブル
        "list_layout": "table",
        # --- トークン ---
        "font_body": "'IBM Plex Sans JP', 'Hiragino Sans', sans-serif",
        "font_head": "'IBM Plex Sans JP', 'Hiragino Sans', sans-serif",
        "font_num": "'IBM Plex Sans JP', sans-serif",
        "gfont": "family=IBM+Plex+Sans+JP:wght@400;500;600;700",
        "head_weight": "600",
        "head_spacing": "-0.005em",
        # 比較しやすさのために装飾は抑えるが、寒色のグレーで冷たくしない。
        # ニュートラルはすべて暖色寄り、アクセントも黒ではなく焦茶にしている。
        "tokens": {
            "--bg": "#F7F4EF",
            "--bg-alt": "#EFE8DE",
            "--surface": "#FFFFFF",
            "--surface-alt": "#FBF8F4",
            "--ink": "#2A241F",
            "--ink-soft": "#6B6157",
            "--ink-faint": "#998F84",
            "--line": "#E4DCD1",
            "--line-strong": "#C7BCAC",
            "--accent": "#3E332A",
            "--accent-strong": "#271F18",
            "--accent-tint": "#F1E9DF",
            "--accent-ink": "#FFFFFF",
            "--warm": "#C0553A",
            "--warm-strong": "#9E4029",
            "--warm-tint": "#FBEDE5",
            "--radius-s": "4px",
            "--radius-m": "6px",
            "--radius-l": "10px",
            "--shadow": "0 1px 3px rgba(42,36,31,.08)",
            "--shadow-lift": "0 4px 14px rgba(42,36,31,.12)",
            "--s1": "#3E332A", "--s1-tint": "#F1E9DF",
            "--s2": "#3E332A", "--s2-tint": "#F1E9DF",
            "--s3": "#3E332A", "--s3-tint": "#F1E9DF",
            "--s4": "#3E332A", "--s4-tint": "#F1E9DF",
            "--s5": "#3E332A", "--s5-tint": "#F1E9DF",
            "--s6": "#3E332A", "--s6-tint": "#F1E9DF",
        },
    },
}
