# Demo & Submission Guide

## 90-second walkthrough
1. **Context (15s):** Revio already offers sentiment and response automation; I propose an added issue-to-action intelligence layer.
2. **Triage (25s):** Enter `I was overcharged and the refund has been delayed`, rating 1; show Finance, priority, evidence and editable draft response.
3. **Safety (15s):** Enter `I felt unsafe at this location`, rating 3; show critical flag and human review.
4. **Operational dashboard (25s):** Use sample CSV to compare issues and show routing/priority queue + export.
5. **Technical honesty (10s):** transparent rule-based baseline today, next steps labeled dataset, multilabel transformer classifier and evaluation.

## Publish the project yourself
```bash
git init
git add .
git commit -m "feat: implement explainable review triage MVP"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/cynbit-revio-insightai.git
git push -u origin main
```
Create an empty GitHub repository named `cynbit-revio-insightai` before pushing. For clean history, make meaningful follow-up commits on testing and docs as you refine the project; do not fabricate past development commits. Deploy in Streamlit Community Cloud by selecting the GitHub repository and `app.py`.

## Submission checklist
- [ ] Run local tests and inspect all demo screens
- [ ] Put real GitHub link or live Streamlit URL in portal
- [ ] Include report markdown files in public repository
- [ ] Replace `YOUR_USERNAME` with your own GitHub name
- [ ] Verify repository is public and demo opens incognito
- [ ] Submit before **Wednesday, 25 November 2026 at 03:11 AM IST** (deadline supplied in invitation)

Submit only to the official link supplied in the assessment. This package does not submit automatically.
