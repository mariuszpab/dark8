"""Unit tests for NLP module"""

from dark8_core.nlp import IntentClassifier, EntityExtractor, PolishParser, NLPEngine


class TestIntentClassifier:

    def test_build_intent(self):
        intent, conf = IntentClassifier.classify("zbuduj aplikację todo")
        assert intent == "BUILD_APP"
        assert conf > 0.5

    def test_search_intent(self):
        intent, conf = IntentClassifier.classify("szukaj informacji")
        assert intent == "SEARCH"

    def test_unknown_intent(self):
        intent, conf = IntentClassifier.classify("xyzabc")
        assert intent == "UNKNOWN"
        assert conf == 0.0


class TestEntityExtractor:

    def test_framework_extraction(self):
        entities = EntityExtractor.extract("zbuduj aplikację w Django")
        assert "FRAMEWORK" in entities
        assert "django" in entities["FRAMEWORK"]

    def test_language_extraction(self):
        entities = EntityExtractor.extract("napisz kod w Python")
        assert "LANGUAGE" in entities
        assert "python" in entities["LANGUAGE"]


class TestPolishParser:

    def test_tokenization(self):
        tokens = PolishParser.tokenize("Cześć, jak się masz?")
        assert len(tokens) > 0
        lowered = [t.lower() for t in tokens]
        assert ("cześć" in lowered) or ("czesc" in lowered) or ("Cześć" in tokens)

    def test_normalization(self):
        text = PolishParser.normalize("  Cześć   świecie  ")
        assert text == "cześć świecie"


class TestNLPEngine:

    def test_full_pipeline(self):
        nlp = NLPEngine()
        result = nlp.understand("zbuduj aplikację todo w Django z bazą danych")

        assert result['intent'] == "BUILD_APP"
        assert result['confidence'] > 0.5
        assert 'django' in str(result['entities']).lower()
        assert len(result['tokens']) > 0

    def test_is_valid_command(self):
        nlp = NLPEngine()
        assert nlp.is_valid_command("zbuduj aplikację", min_confidence=0.3)
        assert not nlp.is_valid_command("xyzabc sdfgh")
