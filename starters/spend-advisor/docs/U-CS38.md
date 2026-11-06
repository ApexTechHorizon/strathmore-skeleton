# U-CS38 — design, scope and QA

Owner/contributor: Eeshan Vaghjiani. Implementation: `starters/spend-advisor`.
This fills the applicable service design/QA content without copying empty
institutional templates or claiming supervisor approval. IDs below are local
traceability labels, **not invented approved SRS clause numbers**.

## Concept and design

Help a household review up to three discretionary-category budget differences,
with an explicit action, reason and exact KES scenario. This is decision support,
not financial advice, an anomaly verdict, a forecast or proof of affordability.

```text
Trusted synthetic staging operator / authorized server
  -> FastAPI request validation + bearer credential
  -> immutable validated synthetic budget snapshot
  -> approved positive-gap baseline -> highest three opportunities
  -> exact JSON response + versioned SQLite offers
  -> explicit shown/accepted/declined feedback -> defined acceptance counts
```

No U-CS37/U-CS46 calls, internet reads, training, Flutter dependency or source
budget writes. Staging data is read-only. Keys are environment-only. Credentials
do not authorize household ownership; that remains a trusted caller obligation.

### Data

- Input snapshot: `isSynthetic:true`, list of budgets keyed by `targetId`; each
  contains household/month/year, category, approved allocation and actual amount.
- One category per household-period; targets are unique across the snapshot.
- Feedback `offers`: SHA-256 content/household/period identity, exact payload,
  first-prepared timestamp, explicit shown timestamp, latest decision, revision
  and active marker. SQLite parameter binding is used for all values.
- `source_state`: current snapshot hash; prevents running old workers from
  writing as if they were current. Source provenance does not cause duplicate
  offers when unrelated households change.
- Only synthetic identities/reasons are stored. A persistent hosting volume and
  approved access/retention arrangements would be needed beyond local staging.

### Baseline

For allowed categories with approved allocations:

`conditional_reduction_kes = recorded_actual_kes - approved_allocation_kes`

Keep positive differences only, sort by reduction descending then target ID,
return at most three. The reason gives both amounts and states the retrospective,
conditional interpretation. An allocation is not proof a future reduction is
feasible. Essential categories outside the allowlist are never automatically cut.

## Requirement-to-test map

| Local ID | Requirement | Evidence in `tests/test_contract.py` |
|---|---|---|
| CS38-01 | Required recommendation route/shape | `test_exact_contract_cap_ranking_and_baseline_number` |
| CS38-02 | At most 3 actionable, reasoned KES scenarios | Same test; `test_equal_gaps_have_stable_target_order` |
| CS38-03 | No invented households/history or fabricated third item | `test_household_period_scope_empty_and_missing` |
| CS38-04 | Exact money; reject invalid/nonfinite values | `test_large_money_stays_exact_json_number`, snapshot-money tests |
| CS38-05 | No pending/essential/negative-gap advice | `test_pending_essential_and_no_positive_gap_are_not_advice` |
| CS38-06 | Caller authentication + selected household/period scope | `test_protected_routes_reject_missing_wrong_and_unicode_keys`, scope tests |
| CS38-07 | Persistent, retry-safe offer/decision tracking | restart, duplicate, stale-offer and concurrency tests |
| CS38-08 | Explicit exposure + acceptance denominator | `test_acceptance_has_explicit_display_unanswered_denominator_and_no_duplicates` |
| CS38-09 | Honest failures and no cached/echoed financial inputs | malformed/invalid input and storage-failure tests |
| CS38-10 | Standalone demo with visible state/errors | `tests/demo.test.cjs` and health/demo route test |

The server credential is not a test of authorization in the external platform.
The demo tests use a small simulated DOM, not a real browser or screen reader.
Its labelled inputs, live status, keyboard-native buttons and text-only rendering
are implemented; full assistive-technology certification is not claimed.

## Evaluation and acceptance evidence

The committed eight-record fixture deliberately includes protected categories,
a second household and a known empty month. It is hand-authored synthetic data,
not a sampled population. The main June household has four eligible positive
gaps: KES1,500, 600, 400 and 200. The output is the highest three, KES2,500 total.
This is a reproducible **functional baseline** with expected answers; it does not
estimate recommendation usefulness, affordability or economic impact.

Automated feedback checks issue three unique offers, show one, accept one and
leave two unanswered. `acceptRate=0.3333`, `shownAcceptRate=1.0000`; after an
explicit decline, accepted count becomes zero without adding denominator rows.
Restart/repeated calls retain decisions; changed content does not inherit them.
Synthetic decisions demonstrate the acceptance-rate mechanism, **not an observed
human acceptance rate**. Acceptance and realized savings are different outcomes.

No model-selection experiment, chronological holdout or learned-model improvement
is asserted. A genuine prospective evaluation would require actions and budgets
known at decision time, an agreed temporal split and measured later outcomes.
Spendly's weekly LSTM WAPE and Isolation Forest F1 are not recommendation metrics.
Existing research is preserved upstream; no training or data-generator changes
were required to deliver this bounded U-CS38 service.

## Handoff and remaining external gates

Deliverable: source, executable synthetic demo, documented contract, persistent
acceptance accounting, tests, Docker recipe and scoped CI in a reviewable U-CS38
PR. No team-37/team-46 implementation is part of this delivery.

Not supplied or claimed by this PR: a hosted URL, real authenticated Wasaa data
access, platform household authorization, human adoption, model superiority,
deployment/production readiness or institutional sign-off. A maintainer must
review/merge the PR. Hosting and any public data/feedback rollout need explicit
approval and appropriate credentials/storage. A merged PR alone is not proof
of those external acceptance outcomes.
