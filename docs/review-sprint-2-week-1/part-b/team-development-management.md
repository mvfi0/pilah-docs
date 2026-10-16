# Team Development Management

!!! success "Competency level: 3"
    Two detailed reviews of teammates' merge requests, each with feasible improvement suggestions:

    - **Gabriel's PIL-354** (pilah-be #97, 13 Oct). Two inline suggestions. Gabriel took both, and built a source-level guard on the first one.
    - **Ghani's PIL-248** (pilah-be #104, 16 Oct). One performance suggestion, measured against the current code before posting: same result, 5 queries down to 3, 91 ms down to 34 ms.

    The other side of reviewing is here too:

    - Tristan's 8 findings on my merge requests: each verified against the code, fixed test-first and answered in its thread.
    - A crash that every CI-built app would have hit on launch, found and raised.

## Review given: Gabriel's [pilah-be #97](https://github.com/bank-sampah-PILAH/pilah-be/pull/97) (PIL-354), 13 Oct

PIL-354 fixes CORS for the web dashboard. It allows the `Idempotency-Key` request header and exposes `Content-Disposition`, so browser downloads get their filename. Gabriel added a registry of custom headers in `shared_kernel/http_headers.py`, which both the CORS settings and the views are meant to read from.

[Review (approved)](https://github.com/bank-sampah-PILAH/pilah-be/pull/97#pullrequestreview-5505285204) · inline: [registry constant](https://github.com/bank-sampah-PILAH/pilah-be/pull/97#discussion_r4260067025), [test that can't fail](https://github.com/bank-sampah-PILAH/pilah-be/pull/97#discussion_r4260067038)

Before commenting, I checked that the registry covers everything that crosses origins. `Idempotency-Key` is the only custom header the API reads, and pilah-mobile sends nothing outside the default allowed set. `Content-Disposition` is written in four places, and the one exposed header covers all of them, including the draft-pencairan export that my PIL-341 web work uses.

| Suggestion | Why it matters | What Gabriel did (14 Oct) |
|---|---|---|
| **Use the registry constant where the header is written.** The docstring says the CORS setting and the code share one value. That held for `Idempotency-Key`, but the four writes of `Content-Disposition` still spelled the name out ([`ledger/views.py` L151](https://github.com/bank-sampah-PILAH/pilah-be/blob/02c685e/apps/ledger/views.py#L151), [L372](https://github.com/bank-sampah-PILAH/pilah-be/blob/02c685e/apps/ledger/views.py#L372), [L384](https://github.com/bank-sampah-PILAH/pilah-be/blob/02c685e/apps/ledger/views.py#L384), [`nasabah/home.py` L243](https://github.com/bank-sampah-PILAH/pilah-be/blob/02c685e/apps/nasabah/home.py#L243)) | It makes the docstring's claim true for both lists, and gives the next response header an obvious place to be registered | All four writes switched to `CONTENT_DISPOSITION` ([`e50d237`](https://github.com/bank-sampah-PILAH/pilah-be/commit/e50d237)). He went further, with a guard that fails if a registered name is spelled out anywhere else ([`67db001`](https://github.com/bank-sampah-PILAH/pilah-be/commit/67db001)). It went red on exactly those four lines before the fix ([reply](https://github.com/bank-sampah-PILAH/pilah-be/pull/97#discussion_r4266319916)) |
| **A test assertion that cannot fail.** django-cors-headers never echoes requested headers back, so `assertNotIn("x-pilah-tidak-terdaftar", allowed)` passes whatever the settings are. Only the next assertion, no `*`, guards anything | A test should say what it actually protects | Renamed as suggested, and the vacuous assertion became set equality against the allowed list, which also catches one stray header ([`0213cdf`](https://github.com/bank-sampah-PILAH/pilah-be/commit/0213cdf)). He checked it fails both ways ([reply](https://github.com/bank-sampah-PILAH/pilah-be/pull/97#discussion_r4266320168)) |

Both suggestions were marked as nits, so they didn't block the approval. #97 merged with both changes in.

## Review given: Ghani's [pilah-be #104](https://github.com/bank-sampah-PILAH/pilah-be/pull/104) (PIL-248), 16 Oct

PIL-248 adds an operational summary to the activity feed (count, weight, deposits, payouts, period balance) and a combined Excel export of deposits and payouts. Ghani asked me and Heraldo to review. Tristan had already flagged two issues (member filter, consistent snapshot) and Gabriel one (formulas without cached values), so I reviewed the head after those fixes, without repeating their points.

[Review](https://github.com/bank-sampah-PILAH/pilah-be/pull/104#pullrequestreview-5547040301) · inline: [database aggregates for the summary](https://github.com/bank-sampah-PILAH/pilah-be/pull/104#discussion_r4294071346)

**The suggestion: compute the summary in the database.** The feed now builds the summary on every page request, and it streams every `total_nilai` and `nominal` in the filtered range into Python to round each one down. With `periode=semua` that is the bank's whole history, read again on every scroll. Rounding down is `Floor` for non-negative amounts, so the same per-event rounding fits in `Sum(Floor(...))`, with the counts folded into the same queries. Before posting it, I ran a throwaway benchmark against the PR's own function (20,000 setoran and 5,000 pencairan, SQLite, best of 5):

| | Queries | Time | Result |
|---|---|---|---|
| Current `operational_summary` | 5 | 91 ms | — |
| Database aggregates | 3 | 34 ms | identical dict |

The comment says what wasn't measured (PostgreSQL), and when `Floor` would differ from the current rounding: negative amounts, which a `CheckConstraint` could rule out. It also points out that the feed parses its filters twice, in two calls that could drift apart.

**Checked and not raised.** The review also records what I checked and why it isn't a finding:

- **Formula escaping.** The leading apostrophe is visible in Excel. A typed text cell would hide it, but re-saving the file as CSV would then write the raw `=...` back out, so the current fix is the safer one.
- **The CI coverage change.** I measured the coverage gate with and without `tests/`: 99% either way. The 80% gate already counted the test modules under `apps/`, so the change doesn't loosen it.
- **The durable transaction.** It can't fire in production, because nothing wraps requests in `atomic`.

Gabriel's thread was still open, so the review is a comment, not an approval yet.

## Review received and answered: Tristan on #79, #62, #73 and #74, 11–12 Oct

Tristan reviewed four of my MRs on 11 Oct (and approved #92). I checked every finding against the code before changing anything; all 8 held up. Each fix went in test-first, and each thread got a reply with the commits.

| MR | Finding | What I did | Reply |
|---|---|---|---|
| #79 | [The seed writes price versions itself](https://github.com/bank-sampah-PILAH/pilah-be/pull/79#discussion_r4242257376), outside the approved write paths | Routed it through `catat_harga` ([`dc29a68`](https://github.com/bank-sampah-PILAH/pilah-be/commit/dc29a68)) | [thread](https://github.com/bank-sampah-PILAH/pilah-be/pull/79#discussion_r4247271876) |
| #79 | [Rerunning the seed reprices historical setoran](https://github.com/bank-sampah-PILAH/pilah-be/pull/79#discussion_r4242257381) at today's rate | Red test showed 3,500 becoming 99,999. Each setoran is now priced at its own date ([`857735b`](https://github.com/bank-sampah-PILAH/pilah-be/commit/857735b) → [`f67a84f`](https://github.com/bank-sampah-PILAH/pilah-be/commit/f67a84f)) | [thread](https://github.com/bank-sampah-PILAH/pilah-be/pull/79#discussion_r4247272237) |
| #79 | [The filter allow-list is outside PIL-304](https://github.com/bank-sampah-PILAH/pilah-be/pull/79#discussion_r4242257383) | Reverted here and re-applied unchanged as [#96](https://github.com/bank-sampah-PILAH/pilah-be/pull/96), stacked on #92 | [thread](https://github.com/bank-sampah-PILAH/pilah-be/pull/79#discussion_r4247272434) |
| #62 | [A partial save is reported as a failure](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/62#discussion_r4242257026) | The sheet now says the other fields saved and the price didn't, and stays open; retrying is safe ([`5a80375`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/5a80375) → [`f1ea8d9`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/f1ea8d9)) | [thread](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/62#discussion_r4247489293) |
| #62 | [An older list reload can overwrite a newer one](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/62#discussion_r4242257029) | Reloads are numbered and a stale answer is dropped ([`ece524b`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/ece524b) → [`bd21f70`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/bd21f70)) | [thread](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/62#discussion_r4247489545) |
| #73 | [`toInt()` drops a price's sen](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/73#discussion_r4242248044) | Prices are held in sen and parsed without `double` ([`de18bfc`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/de18bfc) → [`4226ca5`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/4226ca5)) | [thread](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/73#discussion_r4258201362) |
| #73 | [Versions past the first 100 disappear](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/73#discussion_r4242248049) | The history follows `next` to the last page ([`9ad13dd`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/9ad13dd) → [`510f02a`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/510f02a)) | [thread](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/73#discussion_r4258201663) |
| #74 | [The Sonar exclusion still hides the DI graph](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/74#discussion_r4242254526), plus a merge conflict | Removed the exclusion ([`26fcf40`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/26fcf40)). Merged `staging` and took Tristan's identical bloc fix from #71 | [thread](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/74#discussion_r4258097139), [comment](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/74#issuecomment-6144632095) |

Two findings had a cheaper but worse fix that I chose not to take, and the replies say why:

- **#62, the partial save.** Making the two writes atomic would need a backend endpoint that takes both. The API keeps the price separate on purpose, so that every change is a version. So the fix makes the state explicit and the retry safe instead.
- **#79, the filter split.** Force-pushing #79 would have broken last week's evidence links. A revert plus `cherry-pick -x` keeps the history intact.

## Raising a team-wide problem: CI-built apps would crash on launch, 11 Oct

While covering the generated dependency graph, I found that the graph CI and CD build could not create `AuthenticationBloc`, which `app.dart` creates at start-up. It had been that way since PIL-334. The next staging APK or web build would have crashed on launch; local `flutter run` hid it.

- **Reproduced first.** I regenerated the graph, built the bloc from it in a test, and got the exact error before reporting it.
- **Asked before touching shared code.** The fix touches the team's CI and a teammate's code, so I asked how to land it, then opened [#74](https://github.com/bank-sampah-PILAH/pilah-mobile/pull/74) against `staging`.
- **Outcome.** The same one-line fix also reached `staging` through Tristan's #71. #74 kept what was still new: a test that builds every registration, so this class of crash fails CI instead of the app.
