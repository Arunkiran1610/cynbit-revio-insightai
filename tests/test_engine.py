import unittest
from src.engine import classify, analyze_reviews

class TestTriage(unittest.TestCase):
    def test_billing_route(self):
        r = classify('My invoice has a hidden fee and billing problem', 1)
        self.assertEqual(r.issue, 'billing')
        self.assertEqual(r.team, 'Finance')
        self.assertEqual(r.priority, 'high')
    def test_safety_escalation(self):
        r = classify('This was unsafe', 3)
        self.assertEqual(r.priority, 'critical')
        self.assertTrue(r.needs_review)
    def test_unknown_escalates(self):
        self.assertTrue(classify('Some vague feedback', 3).needs_review)
    def test_bad_rating(self):
        with self.assertRaises(ValueError): classify('test', 0)
    def test_empty_review(self):
        with self.assertRaises(ValueError): classify('  ', 4)
    def test_positive(self):
        self.assertEqual(classify('Amazing and excellent service', 5).sentiment, 'positive')
    def test_batch(self):
        self.assertEqual(len(analyze_reviews([{'review':'broken product','rating':1}])), 1)
    def test_no_payment_details_in_reply(self):
        self.assertIn('private support', classify('overcharged payment', 1).reply)

if __name__ == '__main__': unittest.main()
