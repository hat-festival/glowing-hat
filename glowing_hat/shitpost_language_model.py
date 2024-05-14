from pathlib import Path

import markovify


class ShitPostLanguageModel:
    """Markov those Tweets."""

    def __init__(self, corpus="tweets.txt"):
        """Construct."""
        self.text_model = markovify.NewlineText(
            Path("markov", corpus).read_text(encoding="utf-8")
        )

    def generate(self, sentences=1):
        """Generate some rubbish."""
        rubbish_bin = []

        for _ in range(sentences):
            rubbish = self.text_model.make_sentence(tries=100)
            if rubbish[-1] not in ["?", "!", "."]:
                rubbish += "."
            rubbish_bin.append(rubbish[0].upper() + rubbish[1:])

        return " ".join(rubbish_bin)
