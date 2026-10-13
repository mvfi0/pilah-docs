# Team Development Management

!!! success "Competency level: 2"
    No review of a teammate's merge request fell in these days: the review of Pascal's #84 (9 Oct) is claimed in Sprint 1 Week 3. What this week has is the other side of reviewing:

    - Tristan's review of four of my merge requests: all 8 findings verified against the code, fixed test-first and answered in their threads, two of them with a reasoned choice of a different fix.
    - A crash raised that every CI-built app would have hit on launch.

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
