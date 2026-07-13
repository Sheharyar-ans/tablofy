# Tablofy Release Checklist

> Exact terminal commands for **Windows PowerShell**.

---

## Before Release

### 1. All tests pass
```
pytest
```

### 2. Ruff passes
```
ruff check .
```

### 3. Examples run
```
python examples/basic_usage.py
python examples/quickstart.py
python examples/exploration_demo.py
python examples/cleaning_demo.py
python examples/transform_demo.py
python examples/charts_demo.py
python examples/analytics_demo.py
python examples/sql_demo.py
python examples/report_demo.py
```

### 4. README quickstart works
Open `README.md` and copy the quickstart code block into a temporary script.
Run it against a real CSV file to confirm the code is correct.

### 5. Local editable install works
```
pip install -e .
python -c "import tablofy as tf; print(tf.__version__)"
```

### 6. Package builds
```
python -m build
```

### 7. Fresh virtual environment test
```
python -m venv .venv-test
.venv-test\Scripts\Activate.ps1
pip install dist\tablofy-1.0.0a0-py3-none-any.whl
python -c "import tablofy as tf; print(tf.__version__)"
Deactivate
Remove-Item -Recurse -Force .venv-test
```

### 8. No unsupported AI/ML features included
Check that `pyproject.toml` dependencies do **not** include:
- `scikit-learn`, `tensorflow`, `torch`, `transformers`, `openai`, `langchain`
- Any LLM or model-training libraries

### 9. Version updated
**Check these files for the same version:**
- `src/tablofy/__init__.py` — `__version__ = "1.0.0-alpha"`
- `pyproject.toml` — `version = "1.0.0-alpha"`

### 10. Changelog updated
Check `CHANGELOG.md` has a dated entry for the release tag,
e.g. `## 1.0.0-alpha (2026-07-13)`.

---

## TestPyPI

### 1. Build package
```
python -m build
```

### 2. Upload to TestPyPI
```
pip install twine
twine upload --repository-url https://test.pypi.org/legacy/ dist\*
```

### 3. Install from TestPyPI
```
python -m venv .venv-testpypi
.venv-testpypi\Scripts\Activate.ps1
pip install --index-url https://test.pypi.org/simple/ tablofy
```

### 4. Test import
```
python -c "import tablofy as tf; print(tf.__version__); print('OK')"
```

### 5. Run quickstart
```
python examples\quickstart.py
Deactivate
Remove-Item -Recurse -Force .venv-testpypi
```

---

## PyPI

### 1. Final upload
```
twine upload dist\*
```

### 2. Create GitHub release
```
gh release create v1.0.0-alpha --title "v1.0.0-alpha" --notes-file CHANGELOG.md
```

If `gh` is not available, create the release manually at:
https://github.com/anomalyco/Tablofy/releases/new

### 3. Add release notes
Copy the changelog entry for this version into the GitHub release description.
