# Agile planning and traceability

The resubmission work is organised as a short remediation sprint. GitHub Issues hold the user stories and acceptance criteria; GitHub Projects tracks them through `Backlog`, `Ready`, `In progress`, `Review`, and `Done`. Priorities use `must-have`, `should-have`, and `could-have` labels.

## Epics and user stories

| ID | Epic | Priority | User story | Acceptance criteria | Goal |
|---|---|---|---|---|---|
| US1 | Accounts | Must | As an account holder, I want a profile created regardless of how my user was registered, so I can use booking features. | Admin-created and signup-created users each have one Client; booking does not redirect a superuser to signup. | Reliable access |
| US2 | Reservations | Must | As a diner, I want to create a reservation using clear controls, so I know which values are accepted. | Date picker blocks past dates; time picker shows allowed hours; guest input is 1–12; errors are visible. | Easy booking |
| US3 | Reservations | Must | As a diner, I want to view my reservations, so I can review my plans. | Only the signed-in user's records appear with date, time, party, table, and status. | Data privacy |
| US4 | Reservations | Must | As a diner, I want to edit my reservation, so I can change my plans. | Valid changes persist; the current record is excluded from availability conflicts; other users receive 404. | Full CRUD |
| US5 | Reservations | Must | As a diner, I want to cancel while retaining history, so the restaurant can release the table. | POST changes status to Cancelled; cancelled record no longer blocks the slot. | Availability |
| US6 | Reservations | Must | As a diner, I want to permanently delete a reservation, so I control my stored data. | A confirmation screen explains permanence; POST deletes from the database; other users cannot delete it. | Full CRUD |
| US7 | Quality | Must | As an assessor, I want automated tests for critical journeys, so behaviour is evidenced and repeatable. | Tests cover profiles, validation, CRUD, table release, and ownership; suite passes. | Confidence |
| US8 | UX | Should | As a mobile user, I want a responsive and accessible interface, so I can book on any device. | Layout works from 320px; controls have labels and focus states; messages are announced. | Inclusive UX |
| US9 | Documentation | Must | As a developer, I want setup and deployment instructions, so I can reproduce the project. | README lists prerequisites, variables, migrations, static collection, local run, and Render deployment. | Reproducibility |

## Sprint record

| Sprint | Objective | Stories | Definition of done |
|---|---|---|---|
| Initial delivery | Authentication and core reservation management | US1–US5 | Feature implemented and manually checked |
| Resubmission remediation | Resolve assessor blockers and add traceable evidence | US1–US9 | Acceptance criteria met, automated tests pass, documentation updated, issue moved to Done |

This document records the plan in the repository. The live board must remain available with the submission so issue movement, labels, and completion history can be inspected.
