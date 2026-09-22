# Code Quality

!!! warning "Competency level: 2–3"
    All CI checks clean on my code; 3 new SonarQube issues on the shared project are still to be traced to their authors.

## 15–21 Sep

### Automated checks in CI, all passing on PR #19

- `ruff check` and `ruff format --check`: no issues
- `mypy --strict` (`mypy api config`): no issues
- `makemigrations --check`, `manage.py check --deploy`: clean
- Coverage gate (≥ 80%): passed; my new code is 100% covered ([evidence](../../sprints/sprint-1/evidence/PIL-176-coverage.md))

### SonarQube (`pilah-be-staging`)

- The latest analysis ran on my branch and succeeded.
- **Quality gate: failed on 3 new issues** (required 0). "New code" on this server means everything changed since 10 Sep by the whole team, so the issues are not necessarily mine. **Still to check:** Analysis → Issues → New Code filter, then trace each issue's file and line.

## Configuration gap found

- CI measures coverage with `--source=api`, but SonarQube also analyses `config/`, so `config/` lines always show 0%. Changing CI to `--source=api,config` would make SonarQube's numbers accurate for the whole team.

## Local tooling

- SonarQube for IDE (VS Code, 5.10) installed to catch issues while coding.
