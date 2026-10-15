from pathlib import Path

APP = (Path(__file__).resolve().parents[1] / "app.py").read_text(encoding="utf-8")

def test_dependent_controls_are_reactive():
    assert "with st.form('resource_form'" not in APP
    assert "submit=st.button('Position berechnen und hinzufügen'" in APP
    assert "disabled=not quantify" in APP
    assert "disabled=not priced" in APP

def test_ktd_brand_asset_present():
    assert (Path(__file__).resolve().parents[1] / "assets" / "ktd_logo.jpg").is_file()
