import re

# We will inject a large chunk of CSS right before </style> in the FIRST <style> block,
# and also inside the <style> of SLIDE 21 (since we injected one there too).

mobile_css_global = """
/* MODO RESPONSIVO - CELULAR */
@media (max-width: 768px) {
  /* Slides gerais */
  .slide { padding: 40px 20px 60px; overflow-y: auto; overflow-x: hidden; }
  .slide-counter { top: auto; bottom: 20px; right: 20px; padding: 6px 12px; font-size: 11px; z-index: 150;}
  .nav-arrow { width: 36px; height: 36px; font-size: 14px; top: auto; bottom: 20px; transform: none; z-index: 150;}
  .nav-prev { left: 20px; }
  .nav-next { left: 66px; }
  #next { right: 20px; left: auto; }
  
  /* Textos padrao */
  .k { font-size: 10px; letter-spacing: 2px; text-align: center; }
  h2 { font-size: 32px !important; text-align: center; }
  .f, .f2 { font-size: 40px !important; line-height: 1.1 !important; text-align: center; }
  .p { font-size: 14px !important; text-align: center; }
  
  /* Elementos de UI dos slides iniciais */
  .inner { justify-content: center !important; text-align: center !important; align-items: center !important; }
  .cards, .topics, .pills { flex-direction: column !important; align-items: stretch !important; gap: 15px !important; }
  .pill { font-size: 12px; }
  .obj-card { width: 100% !important; margin: 20px 0 !important; }
  
  /* Slide Inscrição / QR */
  .slide > div > div > img, .qr-box img { max-width: 150px; height: auto; }
  .slide > div > div[style*="display:flex;align-items:center;gap:60px;"] { flex-direction: column !important; gap: 30px !important; }
  .slide > div > div[style*="background:#fff;padding:20px;"] { width: fit-content; margin: 0 auto; }
  .slide > div > div[style*="text-align:left;"] { text-align: center !important; }
}
"""

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Inject into Global Style
first_style_end = text.find('</style>')
if first_style_end != -1:
    text = text[:first_style_end] + mobile_css_global + text[first_style_end:]

# CSS Specific to Slide 21 and Modal
mobile_css_s21 = """
@media (max-width: 768px) {
  /* S21 Content */
  .s21 { padding: 0 !important; }
  .s21 .inner { padding: 40px 20px 80px !important; }
  .s21 h2 { font-size: 28px !important; }
  .s21 p.desc { font-size: 13px !important; margin-bottom: 20px !important; }
  .category-nav { gap: 8px !important; margin-bottom: 20px !important; }
  .cat-btn { padding: 8px 12px !important; font-size: 11px !important; width: 48%; text-align: center; }
  .cat-btn[data-cat="all"] { width: 100%; }
  .ideias-grid { grid-template-columns: 1fr !important; }
  
  /* Modal e Canvas Responsive Fixes */
  .modal-content { padding: 16px !important; width: 95vw !important; overflow-x: hidden; }
  .modal-header { flex-direction: column; align-items: flex-start; gap: 10px; margin-bottom: 10px; padding-right: 30px;}
  .modal-header h2 { font-size: 16px !important; }
  .close-btn { top: 10px !important; right: 10px !important; width: 30px !important; height: 30px !important; }
  
  /* Force scale origin to left center so it doesn't expand right */
  #canvas-render-area { transform-origin: top left !important; align-items: flex-start !important; overflow-x: scroll; overflow-y: hidden; width: 100%; padding-bottom: 20px; }
  .card-a5 { transform-origin: top left !important; }
  
  .form-reserva { grid-template-columns: 1fr !important; }
  .modal-form-container h3 { font-size: 14px !important; }
  .modal-form-container p { font-size: 11px !important; }
}

@media (max-width: 900px) { .card-a5 { transform: scale(0.85); margin-bottom: -84px; } }
@media (max-width: 700px) { .card-a5 { transform: scale(0.60); margin-bottom: -224px; } }
@media (max-width: 500px) { .card-a5 { transform: scale(0.40); margin-bottom: -336px; } }
@media (max-width: 400px) { .card-a5 { transform: scale(0.35); margin-bottom: -364px; } }
"""

# The second style block starts with /* Fixes specific to Slide 21 */
# and ends right before <section class="slide s21
s21_style_end = text.find('</style>\n\n<section class="slide s21')
if s21_style_end != -1:
    text = text[:s21_style_end] + mobile_css_s21 + text[s21_style_end:]

# We also need to remove the old scale rules which were:
# @media (max-width: 900px) { .card-a5 { transform: scale(0.85); margin-bottom: -84px; } }
# ...
# @media (max-width: 500px) ...
text = re.sub(r'@media \(max-width: \d+px\) \{ \.card-a5 \{ transform: scale\(0\.\d+\); margin-bottom: -\d+px; \} \}', '', text)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("RESPONSIVENESS INJECTED")
