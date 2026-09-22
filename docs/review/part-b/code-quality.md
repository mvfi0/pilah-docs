# Code Quality

**Rubric (B5 · Code quality measurement):** no issues found by the code quality checker in newly developed code; a screenshot or link from SonarQube or another tool.

| Level | Requirement |
|---|---|
| 1 | Many issues, or one fatal issue |
| 2 | Minor issues remain, 1 or 2 |
| 3 | No issues reported by the tools |
| 4 | Improves the tool configuration or raises the quality standard |

**Proposed level: 2–3**, depending on who owns the three open SonarQube issues.

## Week of 15–21 Sep

### Automated checks in CI, all passing on PR #19

- `ruff check` and `ruff format --check`: no issues
- `mypy --strict` (`mypy api config`): no issues
- `makemigrations --check`, `manage.py check --deploy`: clean
- Coverage gate (≥ 80%): passed; my new code is 100% covered ([evidence](../../sprints/sprint-1/evidence/PIL-176-coverage.md))

### SonarQube (`pilah-be-staging`)

- The latest analysis ran on my branch and succeeded.
- **Quality gate: failed on 3 new issues** (required 0). "New code" on this server means everything changed since 10 Sep by the whole team, so the issues are not necessarily mine. **Still to check:** Analysis → Issues → New Code filter, then trace each issue's file and line.

## Toward level 4

- CI measures coverage with `--source=api`, but SonarQube also analyses `config/`, so `config/` lines always show 0%. Changing CI to `--source=api,config` would make SonarQube's numbers accurate for the whole team.

## Local tooling

- SonarQube for IDE (VS Code, 5.10) installed to catch issues while coding.
