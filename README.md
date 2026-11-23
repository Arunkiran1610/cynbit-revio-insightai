# Revio InsightAI — AI/ML Engineer Intern Assessment (Cynbit)

**Independent concept proposal, not an official Cynbit product.**

A self-contained, transparent customer-feedback intelligence prototype inspired by Cynbit's publicly described **Revio** SaaS product. It turns customer reviews into categorized issues, escalation priority, suggested owning teams, suggested actions and editable response drafts. The operational dashboard aggregates trends across multiple locations.

## Quickstart

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Run automated tests (stdlib only):

```bash
python -m unittest discover -s tests -v
```

## What to show in a 2-minute demo

1. Open **Review triage** and analyze a low-rating billing complaint.
2. Observe Finance routing, evidence phrase, priority and reply suggestion.
3. Enter `This is unsafe` to demonstrate critical human escalation.
4. Open **Operational dashboard** with the included 20 **synthetic** sample reviews.
5. Show issue frequencies, the priority queue, and CSV export.

## Architecture

`CSV/manual review → validation → transparent rules baseline → issue/team routing → risk flag → suggested action + approval-gated response → dashboard / CSV export`

Current prototype deliberately avoids API keys, external data sharing, and unverified model accuracy claims. This is **not a trained ML model**; see the technical plan for a trainable production replacement.

## Public research

- https://www.cynbit.in/
- https://www.cynbit.in/services
- https://www.cynbit.in/products
- https://www.cynbit.in/careers/ai-ml-engineer-intern
- https://www.cynbit.in/case-studies

## Limitations

- Keyword taxonomy misses paraphrases, sarcasm, negation across distant tokens, Hindi/code-switching, multi-label complaints, and nuanced urgency.
- Evidence strength is heuristic, **not** calibrated probability.
- No actual connections to Google Reviews, CRM, or Cynbit APIs; only demo CSV.
- Safety-critical, legal, protected-class, and ambiguous content is for human handling.
- Never automatically publish AI-suggested replies.
- Evaluation on independently labeled real reviews is required before any product claims.

## Structure

- `app.py`: Streamlit UI and download
- `src/engine.py`: explainable routing baseline
- `data/synthetic_reviews.csv`: fictional input examples
- `tests/`: functional checks
- `reports/`: opportunity assessment, technical approach, and demo notes
