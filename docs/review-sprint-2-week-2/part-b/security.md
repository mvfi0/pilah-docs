# Security

!!! warning "Competency level: 1"
    This week's work guards and names **two** OWASP Top 10 categories in its commits, **A01 Broken Access Control** and **A03 Injection**. Both come from one guard in PIL-341 slice 3 ([#127](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/127), 17 Oct).

    The two QA fixes are UI changes with no security surface, so I don't claim anything for them. Level 2 needs at least five categories named in commits, and level 3 a scan with a patch plan; this week has neither. The [Metasploit scan](../../security/index.md) and its patch plan were claimed in [Sprint 2 Week 1](../../review-sprint-2-week-1/part-b/security.md) and aren't counted again.

## OWASP guards in this week's code

| OWASP category | Guard | Commits | Named in the commit |
|---|---|---|---|
| **A01 Broken Access Control** | A draft link only opens a bare draft id, so a crafted link can't steer the pengurus's own authenticated requests to another endpoint | [`a491758`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/a491758) → [`7d938f9`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/7d938f9) | yes |
| **A03 Injection** | The same guard: input from the URL is never pasted into a request path unless it is a bare id | the same pair | yes |

### A01 and A03: the draft link

PIL-341 slice 3 lets a saved draft open from `/draft-pencairan/editor?id=<draftId>`. The editor builds its requests by appending that id to a path:

- `GET draft-pencairan/<id>`
- `PATCH` the same path
- `POST draft-pencairan/<id>/konfirmasi` and `POST draft-pencairan/<id>/batalkan`

So a crafted link such as `?id=../nasabah` or `?id=d-1%2Fkonfirmasi` would have sent the Pengurus's own authenticated requests to a path the editor never meant to call. That is user input injected into a request path (A03), used to reach past the intended access path with the victim's credentials (A01).

**The guard,** [`7d938f9`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/7d938f9): `DraftEditorArgs.fromRoute` accepts an id from a link only if it matches `^[A-Za-z0-9_-]{1,64}$`, the shape of a UUID or a slug. Anything else sends the user to the draft list.

**The test, red first,** [`a491758`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/a491758): it visits `?id=..%2Fnasabah`, `?id=d-1%2Fkonfirmasi` and `?id=%20`. For each it asserts that the user lands on the draft list, and that **no request** to a draft path is built from the link. It failed before the guard, because the editor opened.

**Checked end to end.** A Playwright run against a local build and backend confirmed it: `?id=..%2Fnasabah` lands on the list on desktop and phone, and a real UUID still opens its draft.
