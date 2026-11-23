"""Explainable issue triage on review data. No external API or customer data required."""
from dataclasses import dataclass, asdict
import re
from typing import List

ISSUES = {
    'service_delay': {'team': 'Operations', 'keywords': ['wait','waiting','slow','delay','late','queue','hours','minutes','service took','appointment']},
    'staff_behavior': {'team': 'Customer Experience', 'keywords': ['rude','staff','unhelpful','impolite','behavior','behaviour','courteous','employee','team member']},
    'billing': {'team': 'Finance', 'keywords': ['bill','billing','overcharge','charged','refund','payment','price','invoice','double charge','hidden fee']},
    'product_quality': {'team': 'Quality Assurance', 'keywords': ['broken','defective','damaged','poor quality','quality','faulty','stopped working','product']},
    'cleanliness': {'team': 'Facilities', 'keywords': ['dirty','unclean','hygiene','cleanliness','smell','dust','washroom','clean']},
    'digital_experience': {'team': 'Engineering', 'keywords': ['app','website','login','crash','bug','checkout','error','loading','page']},
}
NEGATIVE = {'bad','terrible','awful','poor','rude','slow','late','broken','damaged','dirty','unhelpful','disappointed','refund','crash','error','overcharged','overcharge','delay','waiting','worst','faulty','horrible','unclean','failed','issue','problem'}
POSITIVE = {'great','excellent','amazing','friendly','fast','quick','clean','helpful','perfect','love','loved','smooth','wonderful','good','satisfied','resolved','easy','pleasant','thank','thanks'}
NEGATORS = {'not','never','no','hardly'}
INTENSIFIERS = {'very','extremely','really','so'}

@dataclass
class Result:
    sentiment: str
    issue: str
    team: str
    priority: str
    confidence: float
    evidence: str
    reply: str
    action: str
    needs_review: bool


def sentiment_score(text: str) -> int:
    """Transparent lexical baseline; not a trained sentiment model."""
    tokens = re.findall(r"[a-z']+", text.lower())
    total = 0
    for i, token in enumerate(tokens):
        weight = 1 if token in POSITIVE else -1 if token in NEGATIVE else 0
        if weight and i and tokens[i-1] in NEGATORS:
            weight *= -1
        if weight and i and tokens[i-1] in INTENSIFIERS:
            weight *= 2
        total += weight
    return total


def classify(text: str, rating: int = 3) -> Result:
    if not text or not text.strip():
        raise ValueError('Review must not be empty.')
    if not isinstance(rating, int) or not 1 <= rating <= 5:
        raise ValueError('Rating must be an integer from 1 to 5.')
    normalized = re.sub(r'\s+', ' ', text.lower()).strip()
    matches = {}
    evidence = {}
    for issue, info in ISSUES.items():
        terms = [term for term in info['keywords'] if re.search(r'(?<!\w)' + re.escape(term) + r'(?!\w)', normalized)]
        matches[issue] = len(terms)
        evidence[issue] = terms
    best = max(matches, key=matches.get)
    score = matches[best]
    issue = best if score else 'other'
    team = ISSUES[issue]['team'] if score else 'Human Review'
    lex = sentiment_score(text)
    rating_sign = -1 if rating <= 2 else 1 if rating >= 4 else 0
    combined = lex + rating_sign
    sentiment = 'negative' if combined < 0 else 'positive' if combined > 0 else 'neutral'
    # Heuristic evidence-strength score, NOT a calibrated probability.
    runner_up = sorted(matches.values(), reverse=True)[1] if len(matches) > 1 else 0
    confidence = round(min(0.95, 0.35 + 0.15 * score + 0.1 * max(0, score-runner_up)), 2) if score else 0.0
    urgent = bool(re.search(r'\b(safety|unsafe|fraud|scam|injury|threat|discrimination|harass(?:ment|ed)?|data breach)\b', normalized))
    priority = 'critical' if urgent else 'high' if sentiment == 'negative' and rating <= 2 else 'medium' if sentiment == 'negative' else 'low'
    needs_review = bool(urgent or issue == 'other' or confidence < 0.55 or (rating <= 2 and sentiment == 'positive') or (rating >= 4 and sentiment == 'negative'))
    actions = {
        'service_delay': 'Review staffing and wait-time logs for the affected location.',
        'staff_behavior': 'Escalate to the customer-experience lead for a respectful review.',
        'billing': 'Check the transaction and billing records; do not request card details in public.',
        'product_quality': 'Open a quality investigation and check comparable complaints.',
        'cleanliness': 'Request a facilities audit and verify cleaning checklists.',
        'digital_experience': 'Create an engineering bug ticket and check error logs.',
        'other': 'Route to a human agent to determine the root cause.',
    }
    if sentiment == 'negative':
        reply = ('Thank you for raising this concern. We are sorry about your experience. '
                 'Our team will review the issue. Please contact us through a private support channel '
                 'with the relevant details so we can investigate. We will not ask for sensitive information publicly.')
    elif sentiment == 'positive':
        reply = 'Thank you for sharing your feedback. We appreciate your support and will pass it along to our team.'
    else:
        reply = 'Thank you for your feedback. We appreciate you taking the time to share your experience.'
    return Result(sentiment, issue, team, priority, confidence,
                  ', '.join(evidence[issue]) if score else 'No matching issue terms',
                  reply, actions[issue], needs_review)


def analyze_reviews(rows: List[dict]) -> List[dict]:
    analyzed = []
    for row in rows:
        result = classify(str(row.get('review', '')), int(row.get('rating', 3)))
        analyzed.append({**row, **asdict(result)})
    return analyzed
