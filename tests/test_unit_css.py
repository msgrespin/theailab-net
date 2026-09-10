"""Unit tests for css/style.css: no dead selectors, no template cruft (T-09)."""
import re
from pathlib import Path

SITE_ROOT = Path(__file__).parent.parent
CSS = (SITE_ROOT / "css" / "style.css").read_text(encoding="utf-8")

# Classes applied by CSS state or reserved, not present as a literal class="" token.
ALLOWLIST = set()


def _class_selectors():
    # strip declaration blocks so we only scan selector text
    selectors = re.sub(r"\{[^}]*\}", "", CSS)
    selectors = re.sub(r"/\*.*?\*/", "", selectors, flags=re.S)
    return set(re.findall(r"\.([A-Za-z_][\w-]*)", selectors))


def test_no_dead_class_selectors():
    html_blob = "\n".join(
        p.read_text(encoding="utf-8")
        for p in SITE_ROOT.rglob("*.html")
        if ".venv" not in p.parts
    )
    used = set(re.findall(r'class="([^"]*)"', html_blob))
    used_classes = {c for group in used for c in group.split()}
    dead = sorted(
        cls for cls in _class_selectors()
        if cls not in used_classes and cls not in ALLOWLIST
    )
    assert not dead, f"CSS class selectors used by no HTML page: {dead}"


def test_no_wordpress_font_override():
    assert "NonBreakingSpaceOverride" not in CSS


def test_header_comment_describes_this_site():
    assert "Programming Humanity" not in CSS
    assert "programminghumanity" not in CSS


def test_has_print_stylesheet():
    assert "@media print" in CSS


# --------------------------------------------------------------------------
# Redesign v2: palette, contrast, and the no-web-fonts guarantee.
# --------------------------------------------------------------------------

REQUIRED_TOKENS = (
    "--bg", "--surface", "--text", "--text-lt",
    "--accent", "--accent-dk", "--border", "--code-bg",
)


def _token_value(name):
    m = re.search(rf"{re.escape(name)}\s*:\s*(#[0-9a-fA-F]{{3,8}})", CSS)
    assert m, f"token {name} not defined with a hex value in :root"
    return m.group(1)


def _luminance(hex_color):
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

    def chan(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)


def _contrast(a, b):
    la, lb = _luminance(a), _luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def test_palette_tokens_present():
    missing = [t for t in REQUIRED_TOKENS if f"{t}:" not in CSS.replace(" ", "")]
    assert not missing, f"palette tokens missing from :root: {missing}"


def test_no_legacy_accent_blue():
    """The old Kenyon link blue must be fully gone."""
    for legacy in ("#0073aa", "#005177"):
        assert legacy not in CSS.lower(), f"legacy colour {legacy} still in stylesheet"


def test_body_text_contrast_meets_aa():
    ratio = _contrast(_token_value("--text"), _token_value("--bg"))
    assert ratio >= 4.5, f"--text on --bg is only {ratio:.1f}:1 (need >= 4.5)"


def test_muted_text_contrast_meets_aa():
    ratio = _contrast(_token_value("--text-lt"), _token_value("--bg"))
    assert ratio >= 4.5, f"--text-lt on --bg is only {ratio:.1f}:1 (need >= 4.5)"


def test_accent_contrast_meets_aa():
    ratio = _contrast(_token_value("--accent"), _token_value("--bg"))
    assert ratio >= 4.5, f"--accent on --bg is only {ratio:.1f}:1 (need >= 4.5)"


def test_no_web_fonts():
    lowered = CSS.lower()
    for bad in ("@font-face", "fonts.googleapis", "fonts.gstatic", ".woff", ".ttf", ".otf"):
        assert bad not in lowered, f"stylesheet pulls a web font ({bad}); everything must be system fonts"


def test_button_styles_defined():
    for sel in (".btn", ".btn-primary", ".btn-ghost"):
        assert sel in CSS, f"button selector {sel} missing"
