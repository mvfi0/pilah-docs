# Code Quality

!!! success "Competency level: 3"
    Every CI quality check passes on both PIL-222 PRs, no SonarQube issue is authored by me, and I traced why the mobile SonarQube project reports nothing at all.

## Automated checks in CI, all passing

**Backend ([#32](https://github.com/bank-sampah-PILAH/pilah-be/pull/32)):** `ruff check`, `ruff format --check`, `mypy --strict`, `makemigrations --check`, `manage.py check --deploy`, coverage ≥ 80% (91%, diff coverage 100%).

**Mobile ([#27](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/27)):** `flutter analyze --fatal-infos`, `dart format --set-exit-if-changed`, coverage and diff-coverage gates (35.3% overall, 87.5% diff).

## Quality of the change itself

The period filter was **shared, not copied**. The transaksi list already had the date-range logic, so it was generalised with a `TypeVar` bound to `Model` and reused, instead of duplicating four period branches:

```python
_Dated = TypeVar("_Dated", bound=Model)

def apply_period(queryset: QuerySet[_Dated], request: HttpRequest,
                 default: str | None = "hari_ini") -> QuerySet[_Dated]:
```

All 68 pre-existing transaksi period tests still pass, which is what makes the generalisation safe to claim.

## Diagnosing the mobile SonarQube project

The SonarQube check on #27 failed, and the mobile dashboard showed "The main branch has no lines of code". Rather than re-running until it passed, I read the logs:

1. The failed run never reached the server — `Connect timed out` on its first call to `/api/server/version`. A re-run passed, so that was infrastructure, not code.
2. The passing run still analysed nothing: `210 files indexed`, then `0 languages detected`. The scanner only looked for Java and Docker files.
3. The same holds on #26 and on other team members' PRs, so the mobile project has **never** analysed Dart. The server has no Dart analyser.

**Consequence for this claim:** a "0 issues" screenshot from the mobile project would be meaningless, so it is not used as evidence. The enforced static analysis for mobile is `flutter analyze --fatal-infos` in CI, which fails the build on infos as well as warnings. Reported to the team so the server can be fixed.

## Backend SonarQube

No open issue on `pilah-be-staging` is authored by me; the Author facet attributes all 14 to three other team members. The screenshot and the two setup gaps I found are on the [week 1 page](../../review/part-b/code-quality.md).
