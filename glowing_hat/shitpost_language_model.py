from pathlib import Path

import markovify


class ShitPostLanguageModel:
    """Markov those Tweets."""

    def __init__(self):
        """Construct."""
        self.text_model = markovify.NewlineText(
            Path("markov", "tweets.txt").read_text(encoding="utf-8")
        )

    def generate(self):
        """Generate some rubbish."""
        rubbish = self.text_model.make_sentence(tries=100)
        if rubbish[-1] not in ["?", "!", "."]:
            rubbish += "."

        return rubbish[0].upper() + rubbish[1:]
