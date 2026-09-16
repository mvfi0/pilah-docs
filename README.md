# pilah-docs

Personal planning, progress, and technical documentation for PILAH.
Published at <https://mvfi0.github.io/pilah-docs/>.

## Local preview

```bash
python -m venv .venv
.venv/Scripts/activate      # Windows; use .venv/bin/activate elsewhere
pip install -r requirements.txt
mkdocs serve                # http://127.0.0.1:8000
```

## Adding content

- New page: create the `.md` file under `docs/` and add it to `nav` in `mkdocs.yml`.
- New sprint: copy `docs/sprints/sprint-1/` (without `tasks/`) and add its entries to `nav`.
- Pushing to `main` deploys to GitHub Pages via `.github/workflows/docs.yml`.
