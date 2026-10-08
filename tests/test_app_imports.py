"""App updates must tolerate the already-loaded comparison module's original API."""
import sys
from types import ModuleType

from streamlit.testing.v1 import AppTest

from explorer import comparison
from tools.knowledge import ROOT


def test_app_update_with_original_comparison_module_cached(monkeypatch):
    # A warm Streamlit process can retain the module imported before the cost
    # fallback update. Preserve that actual original API, including its helpers.
    cached = ModuleType('explorer.comparison')
    for name in ('comparison_assessments', 'comparison_offers', 'usd_text'):
        setattr(cached, name, getattr(comparison, name))
    monkeypatch.setitem(sys.modules, 'explorer.comparison', cached)
    monkeypatch.setattr(sys.modules['explorer'], 'comparison', cached)
    monkeypatch.delitem(sys.modules, 'explorer.comparison_cost', raising=False)
    monkeypatch.delattr(sys.modules['explorer'], 'comparison_cost', raising=False)
    app = AppTest.from_file(str(ROOT / 'streamlit_app.py'), default_timeout=30).run()
    assert not app.exception
    app.sidebar.radio[0].set_value('Compare 2–5 Models').run()
    assert not app.exception
    app.multiselect[0].set_value(['qwen3-coder-next', 'claude-fable-5-1']).run()
    assert not app.exception
    grid = next(b for b in app.main if getattr(b, 'key', None) == 'comparison-grid')
    assert any(m.value == '**Published API rates**' for m in grid.markdown)
