# GitHub Projects board setup

The connected GitHub integration did not have issue-write permission, so the live board and issues must be created in the repository owner's GitHub session before resubmission. This is the only part of the remediation that cannot be completed in source code.

## Create the board

1. Open the repository on GitHub and select **Projects**.
2. Select **Link a project** → **New project** → **Board**.
3. Name it `Restaurant Booking — Resubmission` and add a short description linking the board to the project goals in the README.
4. Add or rename status values to `Backlog`, `Ready`, `In progress`, `Review`, and `Done`.
5. Add an iteration named `Resubmission sprint` and a Priority field with `Must`, `Should`, and `Could`.

## Create the issues

Create one issue for each US1–US9 row in [AGILE.md](AGILE.md). Use the user-story sentence as the issue description and copy its acceptance criteria as a GitHub task list. Add the Epic, Priority, and Goal values from the same row. Suggested titles:

1. `[Must][Accounts] Create a Client profile for every user`
2. `[Must][Reservations] Provide clear validated booking inputs`
3. `[Must][Reservations] Let users view only their own reservations`
4. `[Must][Reservations] Edit reservations securely`
5. `[Must][Reservations] Cancel and release a table`
6. `[Must][Reservations] Permanently delete a reservation`
7. `[Must][Quality] Test critical journeys automatically`
8. `[Should][UX] Build a responsive accessible interface`
9. `[Must][Documentation] Document design, testing, and deployment`

Add every issue to the project and the resubmission iteration. Set priorities explicitly, then move issues through the board as work is checked. Completed code work may move through `In progress` and `Review` to `Done`; preserve issue and board history for assessment rather than deleting completed items.

## Final evidence check

- Make the board visible to the assessor.
- Add the board URL beside the repository and live-site links at the top of `README.md`.
- Ensure each issue includes acceptance criteria, priority, epic, iteration, and project goal.
- Link relevant commits or pull requests from each issue where possible.
- Confirm the final board contains all nine stories and a meaningful lifecycle history.
