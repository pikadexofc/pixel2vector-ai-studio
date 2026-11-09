# Product Experience Contract

**Status:** Governing product rule, approved 2026-11-03  
**Applies to:** PixelPerfect Studio, Pickko AI, every Skill, the ChatGPT interface, the web application, the reconstruction engine, and all supporting services.

## North star

**Task completion comes first.** A customer came to get a job done, not to manage our infrastructure, usage counters, provider budgets, integrations, or internal workflow state. The product must choose the smoothest truthful path that gets the customer as close as possible to the requested outcome.

**Usage metering is best-effort.** Usage records, quota counters, entitlement checks, reminders, analytics, and telemetry are supporting operations. They must not block, delay, interrupt, truncate, or discard an in-progress customer task.

## Priority order

1. **P0, complete the user's task:** understand the requested outcome and produce the most complete safe result available.
2. **P0, preserve continuity:** retain context, inputs, decisions, and completed artifacts; recover without making the customer repeat work.
3. **P0, be truthful:** distinguish actual execution, manual work, pending operations, and unavailable verification.
4. **P1, maintain quality:** preserve fidelity, correctness, privacy, accessibility, and clear communication while choosing the best available execution path.
5. **P2, reconcile operations:** record usage, enforce entitlement bookkeeping, send eligible reminders, collect analytics, and process rewards without interrupting the task.

Safety rules, legal requirements, user consent, access control, and honest capability limits still apply. The experience-first rule never authorizes unsafe content, unauthorized actions, fabricated results, or access to data the user cannot access.

## Request lifecycle

**Deliver the answer first.** Usage metering is reconciled after delivery. Reminder only after delivery: append a reminder only when the 20-minute cooldown permits it.

The normal customer-facing sequence is:

1. Accept the request and reuse all context and files already available.
2. Select the best available automated path.
3. Execute the task and deliver the answer or the most useful complete result possible.
4. Only after delivery, run best-effort usage reconciliation, reminder eligibility checks, telemetry, and reward bookkeeping.
5. If an operation failed, preserve it for safe retry or mark it pending. Never make a customer repeat the main task merely to repair internal bookkeeping.

Do not make a quota or metering preflight a blocking gate for the current request. Do not wait for usage writes, analytics, or notification webhooks before returning the result.

## Free allowance and reminders

The current Pickko AI baseline is 100 free completed cycles, with a friendly reminder after that allowance. The reminder must:

- appear only after the current answer or deliverable has been provided;
- appear at most once every 20 minutes;
- never cover, truncate, delay, or replace the result;
- be omitted when reminder state is unavailable or uncertain;
- stop while a valid Pro entitlement is active.

The allowance is an acquisition and product-planning mechanism, not a reason to abandon an in-progress request. A metering outage must not cause a user-facing denial. If the count is uncertain, preserve the user experience and reconcile the count later using idempotent events where possible.

This policy does not promise unlimited model capacity or unlimited third-party API funding. When a provider genuinely cannot execute the automated request, use an available alternative or continue manually in ChatGPT. State any quality or verification difference. Never silently degrade a deliverable.

## Graceful degradation

When an integration, model, renderer, storage service, database, queue, or host capability fails:

1. Preserve the request, available files, approvals, and completed work.
2. Retry only safe transient failures, with bounded attempts.
3. Switch to another already-authorized available route when appropriate.
4. Activate manual ChatGPT continuation whenever the conversation and required host capabilities remain available.
5. Produce the best useful result available; mark unavailable automation and verification as pending.
6. Create or update a private internal checkpoint when work remains incomplete or the execution mode changes. Never attach or link it as a reconstruction deliverable.

The manual route is a real completion path, not an error page. Do not ask the customer to repeat known details or upload an attachment that remains accessible.

## Cost and capacity controls

Optimize cost behind the scenes before degrading the customer experience. Preferred controls include caching, efficient model routing, bounded retries, batch processing, deduplication, lower-cost models for suitable subtasks, and post-completion reconciliation.

If a genuine capacity constraint prevents full automation, continue with the best available safe mode and disclose any difference. Do not stop midway solely because a usage counter, entitlement write, analytics call, or reminder service failed.

## Success measures

Optimize and review, in this order:

- task completion rate;
- percentage of jobs resumed without customer repetition;
- successful recovery from service failures;
- time to first useful result and time to completed result;
- output quality and user-reported usefulness;
- number of unnecessary user actions and interruptions;
- only then, metering accuracy, cost per completed job, reminder delivery, and reward reconciliation.

Do not improve a backend metric by making the customer experience materially worse.

## Acceptance checks

A release must demonstrate that:

1. A completed answer is returned even when the usage write fails.
2. A quota threshold does not interrupt a request already in progress.
3. A reminder is appended only after the result and never more than once within 20 minutes.
4. If reminder state cannot be read, the result still ships and the reminder is skipped.
5. A provider or integration outage triggers an available fallback without asking for known context again.
6. An unavailable automation is never represented as completed.
7. A manual continuation preserves the same goal, decisions, and deliverable contract.
8. Pending metering and telemetry events can be reconciled without duplicating usage or rewards.

## References

- `docs/architecture/MANUAL-CONTINUITY-CONTRACT.md`
- `resources/MANUAL-FALLBACK-PROTOCOL.md`
- `skills/manual-fallback-continuity/SKILL.md`


## Reconstruction output contract

For PixelPerfect Studio reconstruction tasks, the only customer-facing deliverable is one `DELIVERABLE_VERIFIED` standalone HTML file. All intermediate artifacts are internal. Never expose previews, image crops, source assets, manifests, analysis, QA reports, difference maps, project folders or ZIP bundles as part of the default handoff. If the final verification gate cannot pass, deliver no HTML candidate and state the blocker concisely. See `resources/FINAL-HTML-ONLY-DELIVERY.md`.
