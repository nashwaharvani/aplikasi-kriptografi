"""tema.py – Tema Arcade Retro Pixel untuk CryptoLab.

Panggil ``terapkan_tema()`` tepat setelah ``st.set_page_config`` di app.py.
Fungsi ini menyuntikkan CSS + HTML dekoratif via st.markdown(unsafe_allow_html=True).

Aturan keras:
  - Tidak ada gambar eksternal atau file biner besar.
  - Semua dekorasi dari CSS, SVG inline, atau emoji.
  - Font dimuat dari Google Fonts (Press Start 2P, VT323, JetBrains Mono).
  - Tidak ada karakter berhak cipta.
"""

import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# HTML HEADER BERANDA — banner pita + judul CRYPTO LAB + balon LEVEL UP
# ─────────────────────────────────────────────────────────────────────────────
BERANDA_HTML = """
<div style="text-align:center; padding:1rem 0 2.5rem; user-select:none;">

  <!-- Pita banner bergaya "MEET US FOR" -->
  <div style="
    display:inline-block;
    background:#35B6C6;
    border:3px solid #111111;
    box-shadow:5px 5px 0 #111111;
    padding:0.45rem 2.5rem;
    font-family:'Press Start 2P',cursive;
    font-size:0.75rem;
    color:#111111;
    letter-spacing:4px;
    margin-bottom:1.25rem;
  ">🎮 SELAMAT DATANG DI 🎮</div>

  <br>

  <!-- Judul utama CRYPTO LAB — kuning, outline hitam, bayangan offset -->
  <div class="arcade-blink" style="
    font-family:'Press Start 2P',cursive;
    font-size:clamp(1.5rem,5vw,3rem);
    color:#FFD93D;
    text-shadow:
      3px  3px 0 #111111,
      6px  6px 0 #111111,
      9px  9px 0 rgba(0,0,0,0.40);
    letter-spacing:6px;
    line-height:1.4;
    margin:0.5rem 0 1.5rem;
  ">CRYPTO LAB</div>

  <!-- Balon ucapan pixel bergaya "LEVEL UP" -->
  <div style="
    display:inline-block;
    position:relative;
    background:#FFD93D;
    border:3px solid #111111;
    box-shadow:5px 5px 0 #111111;
    padding:0.55rem 2rem;
    font-family:'Press Start 2P',cursive;
    font-size:0.78rem;
    color:#111111;
    letter-spacing:2px;
    margin-bottom:2rem;
  ">
    ⭐ LEVEL UP! ⭐
    <!-- ekor balon — isi -->
    <div style="
      position:absolute;
      bottom:-13px; left:22px;
      width:0; height:0;
      border-left:9px solid transparent;
      border-right:9px solid transparent;
      border-top:13px solid #FFD93D;
    "></div>
    <!-- ekor balon — border -->
    <div style="
      position:absolute;
      bottom:-17px; left:19px;
      width:0; height:0;
      border-left:12px solid transparent;
      border-right:12px solid transparent;
      border-top:14px solid #111111;
      z-index:-1;
    "></div>
  </div>

  <br>

  <!-- Ikon dekoratif pixel-art generik (emoji) -->
  <div style="margin-top:0.5rem; font-size:1.5rem; letter-spacing:0.6rem; line-height:2;">
    <span class="arcade-float">🕹️</span>
    <span>🪙</span>
    <span class="arcade-float" style="animation-delay:.6s;">❤️</span>
    <span>🏆</span>
    <span class="arcade-float" style="animation-delay:1.2s;">⭐</span>
    <span>🔐</span>
    <span class="arcade-float" style="animation-delay:1.8s;">🔑</span>
    <span>🍒</span>
  </div>

</div>
"""

# ─────────────────────────────────────────────────────────────────────────────
# HTML HEADER SIDEBAR — logo kotak arcade bergaya menu game
# ─────────────────────────────────────────────────────────────────────────────
SIDEBAR_LOGO_HTML = """
<div style="
  text-align:center;
  font-family:'Press Start 2P',cursive;
  font-size:0.72rem;
  color:#FFD93D;
  text-shadow:2px 2px 0 #111111;
  padding:0.75rem 0.5rem;
  border:3px solid #FFD93D;
  box-shadow:4px 4px 0 #111111;
  background-color:#1B1F4B;
  margin-bottom:1rem;
  letter-spacing:1px;
  line-height:1.8;
">
  🕹️ CRYPTO LAB 🕹️<br>
  <span style="color:#35B6C6; font-size:0.62rem; letter-spacing:2px;">
    KRIPTOGRAFI · UDINUS
  </span>
</div>
"""


# ─────────────────────────────────────────────────────────────────────────────
# FUNGSI PUBLIK
# ─────────────────────────────────────────────────────────────────────────────
def terapkan_tema() -> None:
    """Suntikkan CSS Arcade Retro Pixel ke aplikasi Streamlit.

    Dipanggil sekali di app.py tepat setelah st.set_page_config.
    """
    st.markdown(_CSS, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# CSS UTAMA
# ─────────────────────────────────────────────────────────────────────────────
_CSS = """
<style>
/* ================================================================
   GOOGLE FONTS
   Press Start 2P : judul, header, tab, tombol, label pendek
   VT323          : paragraf, isi tabel, widget (lebih mudah dibaca)
   JetBrains Mono : blok kode hex / cipherteks
   ================================================================ */
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&family=JetBrains+Mono:wght@400;700&display=swap');

/* ================================================================
   VARIABEL WARNA
   ================================================================ */
:root {
  --arc-yellow : #FFD93D;   /* kuning arcade             */
  --arc-red    : #F2545B;   /* merah koral               */
  --arc-pink   : #E8528F;   /* pink                      */
  --arc-cyan   : #35B6C6;   /* cyan                      */
  --arc-purple : #6A4C9C;   /* ungu                      */
  --arc-blue   : #2F5DA8;   /* biru                      */
  --arc-orange : #F5A623;   /* oranye piala              */
  --arc-green  : #44FF44;   /* hijau pixel (sukses)      */
  --navy       : #1B1F4B;   /* navy panel isi            */
  --navy-dark  : #0D0F2B;   /* navy gelap (bg, sidebar)  */
  --pink-lt    : #EBD2E2;   /* teks di atas navy         */
  --black      : #111111;   /* garis hitam tebal         */
}

/* ================================================================
   FONT GLOBAL
   ================================================================ */
html, body, .stApp {
  font-family: 'VT323', monospace !important;
}

/* ================================================================
   LATAR APLIKASI: SUNBURST + HALFTONE
   Sunburst hanya terlihat DI BELAKANG panel konten;
   panel sendiri solid agar teks selalu terbaca.
   ================================================================ */
.stApp {
  background:
    radial-gradient(ellipse at center,
      rgba(0,0,0,0.08) 0%,
      rgba(0,0,0,0.30) 100%),
    repeating-conic-gradient(
      from 0deg at 50% 50%,
      #FFD93D   0deg  15deg,
      #F2545B  15deg  30deg,
      #E8528F  30deg  45deg,
      #35B6C6  45deg  60deg,
      #6A4C9C  60deg  75deg,
      #2F5DA8  75deg  90deg,
      #FFD93D  90deg 105deg,
      #F2545B 105deg 120deg,
      #E8528F 120deg 135deg,
      #35B6C6 135deg 150deg,
      #6A4C9C 150deg 165deg,
      #2F5DA8 165deg 180deg,
      #FFD93D 180deg 195deg,
      #F2545B 195deg 210deg,
      #E8528F 210deg 225deg,
      #35B6C6 225deg 240deg,
      #6A4C9C 240deg 255deg,
      #2F5DA8 255deg 270deg,
      #FFD93D 270deg 285deg,
      #F2545B 285deg 300deg,
      #E8528F 300deg 315deg,
      #35B6C6 315deg 330deg,
      #6A4C9C 330deg 345deg,
      #2F5DA8 345deg 360deg
    ) !important;
  min-height: 100vh;
  position: relative;
}

/* Tekstur halftone tipis di atas sunburst */
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image: radial-gradient(
    circle,
    rgba(0,0,0,0.14) 1px,
    transparent 1px
  );
  background-size: 8px 8px;
  pointer-events: none;
  z-index: 0;
}

/* ================================================================
   PANEL KONTEN UTAMA
   Solid navy — sunburst terlihat dari tepi panel.
   ================================================================ */
.block-container {
  background-color: var(--navy) !important;
  border: 4px solid var(--black) !important;
  box-shadow: 8px 8px 0 var(--black) !important;
  border-radius: 0 !important;
  padding: 2rem 2.5rem 3rem !important;
  margin-top: 1.5rem !important;
  margin-bottom: 1.5rem !important;
  position: relative;
  z-index: 1;
  max-width: 1200px !important;
}

/* Hapus bg tambahan dari wrapper Streamlit */
section[data-testid="stMain"] > div {
  background-color: transparent !important;
}

/* ================================================================
   TEKS UMUM DI DALAM PANEL
   ================================================================ */
.block-container p,
.block-container li,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
  font-family: 'VT323', monospace !important;
  font-size: 1.28rem !important;
  line-height: 1.55 !important;
  color: var(--pink-lt) !important;
}

strong, b {
  color: var(--arc-yellow) !important;
  font-family: 'VT323', monospace !important;
}

/* ================================================================
   H1 — Judul besar, kuning, outline hitam, bayangan offset
   ================================================================ */
h1,
.stMarkdown h1 {
  font-family: 'Press Start 2P', cursive !important;
  color: var(--arc-yellow) !important;
  text-shadow:
    3px 3px 0 var(--black),
    6px 6px 0 rgba(0,0,0,0.40) !important;
  font-size: clamp(1rem, 2.5vw, 1.7rem) !important;
  letter-spacing: 2px !important;
  line-height: 1.7 !important;
  margin-bottom: 1rem !important;
}

/* ================================================================
   H2, H3, H4
   ================================================================ */
h2, .stMarkdown h2 {
  font-family: 'Press Start 2P', cursive !important;
  color: var(--arc-cyan) !important;
  text-shadow: 2px 2px 0 var(--black) !important;
  font-size: clamp(0.78rem, 1.8vw, 1.05rem) !important;
  letter-spacing: 1px !important;
  line-height: 1.75 !important;
  border-bottom: 3px solid var(--arc-cyan);
  padding-bottom: 0.5rem;
  margin-bottom: 1rem !important;
}

h3, .stMarkdown h3 {
  font-family: 'Press Start 2P', cursive !important;
  color: var(--arc-yellow) !important;
  text-shadow: 2px 2px 0 var(--black) !important;
  font-size: clamp(0.68rem, 1.4vw, 0.92rem) !important;
  line-height: 1.75 !important;
  margin-bottom: 0.75rem !important;
}

h4, .stMarkdown h4 {
  font-family: 'Press Start 2P', cursive !important;
  color: var(--arc-orange) !important;
  font-size: clamp(0.62rem, 1.2vw, 0.82rem) !important;
  line-height: 1.65 !important;
  margin-bottom: 0.5rem !important;
}

/* Caption / small text */
small,
.stCaption,
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {
  font-family: 'VT323', monospace !important;
  font-size: 1.08rem !important;
  color: #D0D7F4 !important;
}

/* ================================================================
   SIDEBAR — Menu game gelap bergaya arcade
   ================================================================ */
[data-testid="stSidebar"] {
  background-color: var(--navy-dark) !important;
  border-right: 4px solid var(--black) !important;
  box-shadow: 4px 0 0 var(--black) !important;
}

[data-testid="stSidebar"] > div:first-child {
  padding: 1.5rem 1rem 1rem !important;
}

/* Teks caption info di sidebar */
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,
[data-testid="stSidebar"] small {
  font-family: 'VT323', monospace !important;
  font-size: 1.02rem !important;
  color: #D0D7F4 !important;
  text-align: center !important;
  display: block;
}

/* Label pilihan navigasi (radio) di sidebar */
[data-testid="stSidebar"] [data-testid="stRadio"] label {
  font-family: 'VT323', monospace !important;
  font-size: 1.18rem !important;
  color: var(--pink-lt) !important;
  padding: 0.5rem 0.75rem !important;
  display: block;
  border: 2px solid transparent !important;
  cursor: pointer;
  line-height: 1.5 !important;
  border-radius: 0 !important;
  transition: border-color 0.08s, background-color 0.08s, color 0.08s;
  margin-bottom: 2px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
  border-color: var(--arc-yellow) !important;
  color: var(--arc-yellow) !important;
  background-color: rgba(255,217,61,0.10) !important;
}

/* Item aktif sidebar (gunakan :has() untuk modern browser) */
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
  background-color: var(--arc-yellow) !important;
  color: var(--black) !important;
  border-color: var(--black) !important;
  box-shadow: 3px 3px 0 var(--black) !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p,
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) span {
  color: var(--black) !important;
  text-shadow: none !important;
}

[data-testid="stSidebar"] hr {
  border: none !important;
  border-top: 2px solid #232750 !important;
  margin: 1rem 0 !important;
}

/* ================================================================
   TOMBOL UTAMA — Arcade tebal, shadow keras, efek klik geser
   ================================================================ */
.stButton > button {
  font-family: 'VT323', monospace !important;
  font-size: 1.15rem !important;
  background-color: var(--arc-red) !important;
  color: var(--black) !important;
  border: 3px solid var(--black) !important;
  border-radius: 0 !important;
  box-shadow: 5px 5px 0 var(--black) !important;
  padding: 0.65rem 1.25rem !important;
  letter-spacing: 1px !important;
  cursor: pointer;
  text-transform: uppercase;
  transition:
    background-color 0.08s,
    color            0.08s,
    transform        0.05s,
    box-shadow       0.05s !important;
}

.stButton > button:hover {
  background-color: var(--arc-yellow) !important;
  color: var(--black) !important;
  transform: translate(-2px, -2px) !important;
  box-shadow: 7px 7px 0 var(--black) !important;
}

/* Efek tekan: geser ke kanan-bawah */
.stButton > button:active {
  transform: translate(4px, 4px) !important;
  box-shadow: 1px 1px 0 var(--black) !important;
}

/* Tombol primary khusus (Enkripsi) */
.stButton > button[kind="primary"] {
  background-color: var(--arc-pink) !important;
  color: var(--black) !important;
}
.stButton > button[kind="primary"]:hover {
  background-color: var(--arc-yellow) !important;
  color: var(--black) !important;
}

/* ================================================================
   DOWNLOAD BUTTON
   ================================================================ */
[data-testid="stDownloadButton"] > button {
  font-family: 'VT323', monospace !important;
  font-size: 1.15rem !important;
  background-color: var(--arc-blue) !important;
  color: #FFFFFF !important;
  border: 3px solid var(--black) !important;
  border-radius: 0 !important;
  box-shadow: 4px 4px 0 var(--black) !important;
  padding: 0.55rem 1rem !important;
  cursor: pointer;
  transition: background-color 0.08s, transform 0.05s, box-shadow 0.05s !important;
}

[data-testid="stDownloadButton"] > button:hover {
  background-color: var(--arc-cyan) !important;
  color: var(--black) !important;
  transform: translate(-2px, -2px) !important;
  box-shadow: 6px 6px 0 var(--black) !important;
}

[data-testid="stDownloadButton"] > button:active {
  transform: translate(3px, 3px) !important;
  box-shadow: 1px 1px 0 var(--black) !important;
}

/* ================================================================
   TAB — Bergaya game, tab aktif kuning
   ================================================================ */
[data-baseweb="tab-list"] {
  background-color: var(--navy-dark) !important;
  border: 3px solid var(--black) !important;
  border-bottom: none !important;
  gap: 0 !important;
  padding: 0 !important;
}

[data-baseweb="tab"] {
  font-family: 'VT323', monospace !important;
  font-size: 1.2rem !important;
  color: var(--pink-lt) !important;
  background-color: var(--navy-dark) !important;
  border-right: 3px solid var(--black) !important;
  border-radius: 0 !important;
  padding: 0.75rem 0.9rem !important;
  letter-spacing: 0.5px !important;
  line-height: 1.4 !important;
  transition: background-color 0.08s, color 0.08s !important;
}

[data-baseweb="tab"]:last-child {
  border-right: none !important;
}

[data-baseweb="tab"]:hover:not([aria-selected="true"]) {
  background-color: rgba(255,217,61,0.14) !important;
  color: var(--arc-yellow) !important;
}

/* Tab aktif — kuning, teks hitam */
[data-baseweb="tab"][aria-selected="true"] {
  background-color: var(--arc-yellow) !important;
  color: var(--black) !important;
  border-bottom: 3px solid var(--arc-yellow) !important;
}

[data-baseweb="tab"][aria-selected="true"] * {
  color: var(--black) !important;
}

/* Panel isi tab */
[data-baseweb="tab-panel"] {
  border: 3px solid var(--black) !important;
  border-top: none !important;
  background-color: var(--navy) !important;
  padding: 1.5rem 1rem !important;
}

/* ================================================================
   INPUT, TEXTAREA, SELECTBOX
   ================================================================ */
[data-baseweb="input"],
[data-baseweb="textarea"],
[data-baseweb="select"] {
  border: 3px solid var(--black) !important;
  border-radius: 0 !important;
  background-color: var(--navy-dark) !important;
  box-shadow: 3px 3px 0 var(--black) !important;
}

[data-testid="stTextInputRootElement"] {
  border: 3px solid var(--arc-cyan) !important;
  border-radius: 0 !important;
  background-color: #121738 !important;
  box-shadow: 5px 5px 0 var(--arc-cyan) !important;
}

[data-baseweb="input"] input,
[data-testid="stTextInputRootElement"] input,
[data-baseweb="textarea"] textarea,
[data-testid="stTextAreaRootElement"] textarea {
  font-family: 'VT323', monospace !important;
  font-size: 1.3rem !important;
  color: var(--pink-lt) !important;
  background-color: transparent !important;
  caret-color: var(--arc-yellow) !important;
}

[data-baseweb="input"]:focus-within,
[data-testid="stTextInputRootElement"]:focus-within,
[data-baseweb="textarea"]:focus-within {
  border-color: var(--arc-yellow) !important;
  box-shadow: 3px 3px 0 var(--arc-yellow) !important;
}

[data-testid="stTextInputRootElement"]:focus-within {
  box-shadow: 5px 5px 0 var(--arc-yellow) !important;
}

[data-baseweb="textarea"] {
  border-color: var(--arc-cyan) !important;
  background-color: #121738 !important;
  box-shadow: 5px 5px 0 var(--arc-cyan) !important;
}

[data-testid="stTextAreaRootElement"] {
  border: 3px solid var(--arc-cyan) !important;
  border-radius: 0 !important;
  background-color: #121738 !important;
  box-shadow: 5px 5px 0 var(--arc-cyan) !important;
}

[data-baseweb="textarea"]:focus-within,
[data-testid="stTextAreaRootElement"]:focus-within {
  border-color: var(--arc-yellow) !important;
  box-shadow: 5px 5px 0 var(--arc-yellow) !important;
}

/* Label widget */
[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label,
[data-testid="stSlider"] > label,
[data-testid="stRadio"] > label {
  font-family: 'VT323', monospace !important;
  font-size: 1.18rem !important;
  color: var(--arc-cyan) !important;
  letter-spacing: 0.5px;
}

/* Nilai di dalam selectbox */
[data-baseweb="select"] [data-baseweb="select-input"] > div,
[data-baseweb="select"] [data-baseweb="select-input"] span {
  font-family: 'VT323', monospace !important;
  font-size: 1.25rem !important;
  color: var(--pink-lt) !important;
}

/* Dropdown popup selectbox */
[data-baseweb="popover"] {
  border: 3px solid var(--black) !important;
  border-radius: 0 !important;
  box-shadow: 5px 5px 0 var(--black) !important;
}

[data-baseweb="menu"] {
  background-color: var(--navy) !important;
  border-radius: 0 !important;
}

[data-baseweb="menu"] ul li {
  font-family: 'VT323', monospace !important;
  font-size: 1.2rem !important;
  color: var(--pink-lt) !important;
  border-radius: 0 !important;
}

[data-baseweb="menu"] ul li:hover,
[data-baseweb="menu"] ul li[aria-selected="true"] {
  background-color: var(--arc-yellow) !important;
  color: var(--black) !important;
}

/* Number input */
[data-testid="stNumberInput"] input {
  font-family: 'VT323', monospace !important;
  font-size: 1.25rem !important;
  color: var(--pink-lt) !important;
  background-color: var(--navy-dark) !important;
}

[data-testid="stNumberInput"] button {
  background-color: var(--arc-purple) !important;
  border: 2px solid var(--black) !important;
  color: var(--arc-yellow) !important;
  border-radius: 0 !important;
}

/* ================================================================
   RADIO BUTTONS (di halaman utama, bukan sidebar)
   ================================================================ */
[data-testid="stRadio"] label p,
[data-testid="stRadio"] > div label {
  font-family: 'VT323', monospace !important;
  font-size: 1.25rem !important;
  color: var(--pink-lt) !important;
}

/* ================================================================
   SLIDER
   ================================================================ */
[data-testid="stSlider"] [role="slider"] {
  background-color: var(--arc-yellow) !important;
  border: 3px solid var(--black) !important;
  border-radius: 0 !important;
  width: 18px !important;
  height: 18px !important;
  box-shadow: 2px 2px 0 var(--black) !important;
}

/* ================================================================
   METRIC — Kotak score bergaya pixel
   ================================================================ */
[data-testid="stMetric"] {
  background-color: var(--navy-dark) !important;
  border: 3px solid var(--black) !important;
  box-shadow: 4px 4px 0 var(--black) !important;
  padding: 1rem !important;
  border-radius: 0 !important;
}

[data-testid="stMetricLabel"] > div {
  font-family: 'VT323', monospace !important;
  font-size: 1.12rem !important;
  color: var(--arc-cyan) !important;
}

[data-testid="stMetricValue"] > div {
  font-family: 'VT323', monospace !important;
  font-size: 1.7rem !important;
  color: var(--arc-yellow) !important;
  text-shadow: 2px 2px 0 var(--black) !important;
}

/* ================================================================
   PROGRESS BAR — Bar nyawa bergaya pixel
   ================================================================ */
[data-testid="stProgressBar"] {
  border: 3px solid var(--black) !important;
  border-radius: 0 !important;
  background-color: var(--navy-dark) !important;
  height: 22px !important;
  box-shadow: 3px 3px 0 var(--black) !important;
  overflow: hidden !important;
}

[data-testid="stProgressBar"] > div {
  height: 100% !important;
  background: linear-gradient(
    90deg,
    var(--arc-red)    0%,
    var(--arc-yellow) 50%,
    var(--arc-green) 100%
  ) !important;
  border-radius: 0 !important;
  transition: width 0.3s !important;
}

/* ================================================================
   BLOK KODE st.code — Font JetBrains Mono, border cyan
   ================================================================ */
[data-testid="stCode"] {
  border: 3px solid var(--arc-cyan) !important;
  border-radius: 0 !important;
  box-shadow: 4px 4px 0 var(--black) !important;
  background-color: #060810 !important;
}

[data-testid="stCode"] pre,
[data-testid="stCode"] code {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.96rem !important;
  color: #7DF9AA !important;
  background-color: transparent !important;
  line-height: 1.55 !important;
}

/* Inline code */
code:not(pre code) {
  font-family: 'JetBrains Mono', monospace !important;
  background-color: var(--navy-dark) !important;
  color: var(--arc-cyan) !important;
  border: 1px solid var(--arc-purple) !important;
  padding: 0.1rem 0.35rem !important;
  border-radius: 0 !important;
  font-size: 0.96rem !important;
}

/* ================================================================
   ALERT / NOTIFIKASI — Kotak pixel berbeda warna per tipe
   ================================================================ */
[data-testid="stAlert"] {
  border-width: 3px !important;
  border-style: solid !important;
  border-radius: 0 !important;
  box-shadow: 4px 4px 0 var(--black) !important;
}

[data-testid="stAlert"] p {
  font-family: 'VT323', monospace !important;
  font-size: 1.22rem !important;
  line-height: 1.55 !important;
}

/* Info — biru cyan */
[data-testid="stAlert"][data-baseweb="notification"] {
  background-color: #071B2E !important;
  border-color: var(--arc-cyan) !important;
  color: var(--arc-cyan) !important;
}

/* Agar tiap tipe alert benar warnanya, kita andalkan kelas Streamlit */
div[class*="stSuccess"],
.stSuccess,
[data-testid="stAlert"].stSuccess {
  background-color: #041A0A !important;
  border-color: var(--arc-green) !important;
}

div[class*="stWarning"],
.stWarning,
[data-testid="stAlert"].stWarning {
  background-color: #1E1100 !important;
  border-color: var(--arc-yellow) !important;
}

div[class*="stError"],
.stError,
[data-testid="stAlert"].stError {
  background-color: #1E0404 !important;
  border-color: var(--arc-red) !important;
}

div[class*="stInfo"],
.stInfo,
[data-testid="stAlert"].stInfo {
  background-color: #071B2E !important;
  border-color: var(--arc-cyan) !important;
}

/* ================================================================
   TABEL — Teks timbul dua warna agar sel dan header tetap terbaca
   ================================================================ */
[data-testid="stTable"] {
  border: 3px solid var(--black) !important;
  box-shadow: 4px 4px 0 var(--black) !important;
  border-radius: 0 !important;
  background-color: var(--navy-dark) !important;
  overflow-x: auto !important;
}

.stMarkdown table,
[data-testid="stTable"] table {
  border: 3px solid var(--black) !important;
  border-collapse: collapse !important;
  font-family: 'VT323', monospace !important;
  font-size: 1.2rem !important;
  box-shadow: 5px 5px 0 var(--black) !important;
  min-width: 100% !important;
  margin: 1rem 0 !important;
}

.stMarkdown th,
[data-testid="stTable"] th {
  background-color: var(--arc-purple) !important;
  color: var(--arc-yellow) !important;
  font-family: 'VT323', monospace !important;
  font-size: 1.12rem !important;
  font-weight: 700 !important;
  border: 2px solid var(--black) !important;
  padding: 0.7rem 0.8rem !important;
  text-shadow: 1px 1px 0 var(--arc-cyan), 2px 2px 0 var(--black) !important;
}

.stMarkdown td,
[data-testid="stTable"] td {
  background-color: var(--navy-dark) !important;
  color: var(--pink-lt) !important;
  border: 2px solid #2A2F5B !important;
  padding: 0.5rem 0.75rem !important;
  font-family: 'VT323', monospace !important;
  text-shadow: 1px 1px 0 var(--arc-cyan), 2px 2px 0 var(--black) !important;
}

.stMarkdown tr:hover td,
[data-testid="stTable"] tr:hover td {
  background-color: rgba(106,76,156,0.22) !important;
}

/* ================================================================
   EXPANDER — Kotak pixel, header font pixel
   ================================================================ */
[data-testid="stExpander"] {
  border: 3px solid var(--black) !important;
  border-radius: 0 !important;
  box-shadow: 4px 4px 0 var(--black) !important;
  background-color: var(--navy-dark) !important;
  margin-bottom: 0.75rem !important;
}

[data-testid="stExpander"] summary {
  font-family: 'VT323', monospace !important;
  font-size: 1.2rem !important;
  color: var(--arc-cyan) !important;
  padding: 0.7rem 1rem !important;
  line-height: 1.7 !important;
}

details[data-testid="stExpander"][open] > summary {
  border-bottom: 3px solid var(--black) !important;
  color: var(--arc-yellow) !important;
  background-color: rgba(255,217,61,0.08) !important;
}

/* ================================================================
   DIVIDER
   ================================================================ */
hr {
  border: none !important;
  border-top: 3px dashed var(--arc-purple) !important;
  margin: 1.5rem 0 !important;
}

/* ================================================================
   FILE UPLOADER
   ================================================================ */
[data-testid="stFileUploader"] {
  border: 3px dashed var(--arc-cyan) !important;
  border-radius: 0 !important;
  background-color: var(--navy-dark) !important;
  padding: 1rem !important;
  box-shadow: 3px 3px 0 var(--black) !important;
}

[data-testid="stFileUploader"] label {
  font-family: 'VT323', monospace !important;
  color: var(--arc-cyan) !important;
  font-size: 1.2rem !important;
}

/* ================================================================
   LATEX (KaTeX) — Warna cyan agar kontras di atas navy
   ================================================================ */
.katex, .katex * {
  color: var(--arc-cyan) !important;
  font-size: 1.1em !important;
}

/* ================================================================
   IMAGE — Border pixel
   ================================================================ */
[data-testid="stImage"] {
  border: 3px solid var(--black) !important;
  box-shadow: 4px 4px 0 var(--black) !important;
}

[data-testid="stImage"] figcaption {
  font-family: 'VT323', monospace !important;
  font-size: 1.08rem !important;
  color: #D0D7F4 !important;
  background-color: var(--navy-dark) !important;
  padding: 0.2rem 0.5rem !important;
  border-top: 2px solid var(--black) !important;
}

/* ================================================================
   SCROLLBAR BERGAYA PIXEL
   ================================================================ */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track {
  background: var(--navy);
  border: 2px solid var(--black);
}
::-webkit-scrollbar-thumb {
  background: var(--arc-purple);
  border: 2px solid var(--black);
}
::-webkit-scrollbar-thumb:hover { background: var(--arc-yellow); }

/* ================================================================
   ANIMASI — Efek halus; hormati prefers-reduced-motion
   ================================================================ */
@keyframes arcade-blink {
  0%,  49% { opacity: 1;    }
  50%, 100% { opacity: 0.60; }
}

@keyframes arcade-float {
  0%, 100% { transform: translateY(0);   }
  50%       { transform: translateY(-5px); }
}

@media (prefers-reduced-motion: no-preference) {
  .arcade-blink {
    animation: arcade-blink 2s step-end infinite;
  }
  .arcade-float {
    display: inline-block;
    animation: arcade-float 3s ease-in-out infinite;
  }
}

/* ================================================================
   FOKUS KEYBOARD — Aksesibilitas tetap terlihat
   ================================================================ */
*:focus-visible {
  outline: 3px solid var(--arc-yellow) !important;
  outline-offset: 3px !important;
}

/* ================================================================
   RESPONSIF — Layar ponsel (≤ 768 px)
   ================================================================ */
@media (max-width: 768px) {
  .block-container {
    padding: 1rem 1rem 2rem !important;
    margin: 0.5rem !important;
    border-width: 3px !important;
    box-shadow: 5px 5px 0 var(--black) !important;
  }
  h1 { font-size: 1rem !important; }
  h2 { font-size: 0.78rem !important; }
  h3 { font-size: 0.68rem !important; }

  [data-baseweb="tab"] {
    font-size: 1.05rem !important;
    padding: 0.55rem 0.5rem !important;
  }
  .stButton > button {
    font-size: 1.05rem !important;
    padding: 0.5rem 0.75rem !important;
    box-shadow: 3px 3px 0 var(--black) !important;
  }

  .stMarkdown th,
  .stMarkdown td,
  [data-testid="stTable"] th,
  [data-testid="stTable"] td {
    padding: 0.55rem 0.45rem !important;
  }
}

/* ================================================================
   KOLOM (Columns) — Padding minimal agar konten tidak berhimpitan
   ================================================================ */
[data-testid="column"] {
  padding: 0.3rem !important;
}

</style>
"""
