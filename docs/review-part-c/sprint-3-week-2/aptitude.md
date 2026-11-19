# Aptitude, Applying Knowledge

!!! success "Competency level: 3"
    One new learning from outside the class material, applied in the PILAH project this week (Sprint 3 Week 2, 4 – 10 Nov) and linked to the code that shows it:

    1. **Flutter's widget and route lifecycle across an async gap,** and Riverpod's container API for reaching providers safely after it.

The rubric's level 3 is one or two new learnings outside the class material, applied in the project. Things the course already covers are left out: basic TDD, widget tests, Git branching, SonarQube, UAT.

## The learning applied this week

| Learning | Applied in | Evidence |
|---|---|---|
| **What a widget may still do after `await`.** The parts I learned and used: <ul><li>`PopScope(canPop:)` to keep a dialog open while its request is in flight, instead of the default `barrierDismissible`;</li><li>reading every notifier **before** the `await`, because `ref` and `context` may belong to a disposed widget afterwards;</li><li>applying the server's outcome whether or not the widget is still mounted, since the server state changed either way;</li><li>`ModalRoute.of(context).isCurrent` to tell "this dialog is closing" from "this dialog is on top", so a late `pop` can't close the page underneath;</li><li>`ProviderScope.containerOf` and `container.exists`, to reload only the providers a screen already built.</li></ul> | The PIL-428 Hapus dialog (#193), after Heraldo's and Scallss's findings | [`472c506`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/472c506b), [`be7b6d0`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/be7b6d06), and the tests in [`17125d0`](https://github.com/bank-sampah-PILAH/pilah-mobile/commit/17125d07) |

## How it changed the work

- **It found a bug nobody had reported.** Knowing that a dialog animates closed for a few frames led to the third test: an answer arriving during that animation closed the Riwayat page. The fix is one condition on the route.
- **It made the tests possible.** Staging an in-flight request needs a stub API with a set latency and `tester.pump` with exact durations. Without those, the race can't be reproduced, so a fix can't be proven.
- **It keeps the app from doing extra work.** `container.exists` means a void reloads the dashboard only if the pengurus already opened it, instead of building every screen and sending their requests.

## Also used

- **Reading ZAP's results against the app's state.** On 9 Nov the "SQL injection" turned out to be the first attack voiding the setoran, so every later attack got 409. This builds on last week's ZAP learning, so it isn't claimed again.
- **openpyxl's merged ranges and column widths** (PIL-480), moved from `A:N` to `A:M`. A small API detail, not a new learning.
