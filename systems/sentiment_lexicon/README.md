# Lexicon-based sentiment classifier

Classify short text as positive, negative, or neutral using a small hand-built word list. No model, no training data.

**Level:** starter · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.sentiment_lexicon.app "This product is great and the support team is fantastic."
```

## Evaluate and test

```bash
python3 -m systems.sentiment_lexicon.evaluate
python3 -m unittest systems.sentiment_lexicon.test_sentiment
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

See [`eval/results.json`](eval/results.json) for current accuracy on 5 synthetic sentences, including one mixed-sentiment case that intentionally ties and falls back to neutral.

## Known limitations

- The lexicon has no negation handling ("not good" scores as positive) and no stemming, so inflections outside the hard-coded list are invisible to it.
- Ties between positive and negative word counts always resolve to neutral, which is a crude tie-break, not a confidence-aware decision.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
