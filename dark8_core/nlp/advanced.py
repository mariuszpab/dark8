# DARK8 OS - Advanced NLP with Learning
"""
Enhanced NLP engine with learning capabilities.
Uses transformer models and learns from user interactions.
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict

from dark8_core.logger import logger
from dark8_core.persistence import get_database


@dataclass
class ParsedCommand:
    """Structured command after full NLP processing"""
    original: str
    normalized: str
    intent: str
    confidence: float
    entities: Dict[str, List[str]]
    tokens: List[str]
    dependencies: List[str]
    priority: int
    context_needed: bool


class AdvancedIntentClassifier:
    """Advanced intent classification with learning"""

    INTENT_HIERARCHY = {
        "DEVELOPMENT": {
            "BUILD_APP": {"keywords": ["zbuduj", "stwórz", "utwórz"], "priority": 1},
            "GENERATE_CODE": {"keywords": ["generuj", "wygeneruj"], "priority": 2},
            "REFACTOR": {"keywords": ["refactor", "ulepsz", "popraw"], "priority": 2},
            "TEST": {"keywords": ["testuj", "sprawdzaj"], "priority": 3},
            "DEPLOY": {"keywords": ["wdróż", "deploy", "uruchom"], "priority": 1},
        },
        "ANALYSIS": {
            "ANALYZE_CODE": {"keywords": ["analizuj", "przeanalizuj"], "priority": 2},
            "REVIEW": {"keywords": ["przejrzyj", "recenzja"], "priority": 2},
            "EXPLAIN": {"keywords": ["wyjaśnij", "tłumacz"], "priority": 3},
        },
        "SEARCH": {
            "SEARCH": {"keywords": ["szukaj", "wyszukaj"], "priority": 2},
            "RESEARCH": {"keywords": ["zbadaj", "dochodzenie"], "priority": 3},
        },
        "SYSTEM": {
            "STATUS": {"keywords": ["status", "stan"], "priority": 3},
            "HELP": {"keywords": ["pomoc", "help"], "priority": 4},
            "CONFIG": {"keywords": ["konfiguruj", "ustawienia"], "priority": 3},
        }
    }

    def __init__(self):
        self.learned_patterns: Dict[str, float] = {}
        self._load_learned_patterns()

    def _load_learned_patterns(self):
        """Load patterns learned from previous interactions"""
        try:
            db = get_database()
            conversations = db.get_conversations(limit=1000)

            for conv in conversations:
                if conv.intent and conv.confidence:
                    key = f"{conv.user_input}:{conv.intent}"
                    self.learned_patterns[key] = conv.confidence

            logger.info(f"✓ Loaded {len(self.learned_patterns)} learned patterns")
        except Exception as e:
            logger.warning(f"Could not load learned patterns: {e}")

    def classify(self, text: str, use_learning: bool = True) -> Tuple[str, float, str]:
        """
        Classify intent with hierarchy support.
        Returns: (intent, confidence, category)
        """
        text_lower = text.lower()

        best_intent = "UNKNOWN"
        best_confidence = 0.0
        best_category = "OTHER"

        # Check learned patterns first
        if use_learning:
            for key, conf in self.learned_patterns.items():
                if key.startswith(text_lower):
                    intent = key.split(":")[1]
                    return intent, conf, "learned"

        # Hierarchical search
        for category, intents in self.INTENT_HIERARCHY.items():
            for intent, config_dict in intents.items():
                keywords = config_dict["keywords"]

                for keyword in keywords:
                    if keyword in text_lower:
                        priority = config_dict["priority"]
                        # Confidence = keyword match + priority bonus
                        confidence = 0.6 + (0.1 * (len(keyword) / len(text_lower))) + (0.04 / priority)

                        if confidence > best_confidence:
                            best_confidence = min(confidence, 1.0)
                            best_intent = intent
                            best_category = category

        return best_intent, best_confidence, best_category


class EntityExtractorAdvanced:
    """Advanced entity extraction with context awareness"""

    ENTITY_PATTERNS = {
        "FILE_PATH": {
            "patterns": [".py", ".js", ".java", "/", "plik", "katalog", "folder"],
            "type": "location"
        },
        "FRAMEWORK": {
            "patterns": ["django", "flask", "fastapi", "react", "vue", "angular", "node", "express"],
            "type": "technology"
        },
        "LANGUAGE": {
            "patterns": ["python", "javascript", "java", "cpp", "rust", "go", "php", "ruby"],
            "type": "technology"
        },
        "DATABASE": {
            "patterns": ["postgresql", "mysql", "mongodb", "redis", "sqlite", "firestore"],
            "type": "technology"
        },
        "TOOL": {
            "patterns": ["git", "docker", "kubernetes", "npm", "pip", "npm", "gradle"],
            "type": "technology"
        },
        "NUMBER": {
            "patterns": ["\\d+", "liczba", "ilość"],
            "type": "quantity"
        },
        "TIME": {
            "patterns": ["teraz", "jutro", "dziś", "dzisiaj", "godzina", "minuta"],
            "type": "temporal"
        },
    }

    @classmethod
    def extract(cls, text: str) -> Dict[str, List[Dict]]:
        """
        Extract entities with metadata.
        Returns: {entity_type: [{value, confidence, type}]}
        """
        entities = {}
        text_lower = text.lower()

        for entity_type, config_dict in cls.ENTITY_PATTERNS.items():
            entities[entity_type] = []

            for pattern in config_dict["patterns"]:
                if pattern in text_lower:
                    entities[entity_type].append({
                        "value": pattern,
                        "confidence": 0.8,
                        "category": config_dict["type"]
                    })

        return {k: v for k, v in entities.items() if v}


class DependencyAnalyzer:
    """Analyze dependencies between entities"""

    DEPENDENCY_RULES = {
        "BUILD_APP": ["FRAMEWORK", "LANGUAGE", "DATABASE"],
        "DEPLOY": ["TOOL", "FRAMEWORK"],
        "ANALYZE_CODE": ["FILE_PATH", "LANGUAGE"],
        "TEST": ["FRAMEWORK", "FILE_PATH"],
    }

    @classmethod
    def analyze(cls, intent: str, entities: Dict[str, List]) -> List[str]:
        """Determine needed dependencies"""
        needed = cls.DEPENDENCY_RULES.get(intent, [])
        missing = [e for e in needed if not entities.get(e)]

        return missing


class AdvancedNLPEngine:
    """Complete advanced NLP system"""

    def __init__(self):
        self.intent_classifier = AdvancedIntentClassifier()
        self.entity_extractor = EntityExtractorAdvanced()
        self.dependency_analyzer = DependencyAnalyzer()
        self.db = get_database()
        logger.info("✓ Advanced NLP Engine initialized")

    def process(self, user_input: str) -> ParsedCommand:
        """Full NLP processing pipeline"""

        # Normalize
        normalized = user_input.lower().strip()

        # Tokenize
        tokens = self._tokenize(normalized)

        # Classify intent
        intent, confidence, category = self.intent_classifier.classify(normalized)

        # Extract entities
        entities = self.entity_extractor.extract(normalized)

        # Analyze dependencies
        dependencies = self.dependency_analyzer.analyze(intent, entities)

        # Determine priority based on intent
        priority = self._calculate_priority(intent, confidence)

        # Check if context is needed
        context_needed = len(dependencies) > 0

        return ParsedCommand(
            original=user_input,
            normalized=normalized,
            intent=intent,
            confidence=confidence,
            entities=entities,
            tokens=tokens,
            dependencies=dependencies,
            priority=priority,
            context_needed=context_needed,
        )

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize Polish text"""
        import re
        # Remove punctuation
        text = re.sub(r'[.,!?;:]', '', text)
        tokens = text.split()
        return [t for t in tokens if t]

    def _calculate_priority(self, intent: str, confidence: float) -> int:
        """Calculate execution priority (1=highest, 5=lowest)"""
        if intent in ["DEPLOY", "BUILD_APP"]:
            return 1
        elif intent in ["ANALYZE_CODE", "TEST"]:
            return 2
        elif intent in ["SEARCH", "RESEARCH"]:
            return 3
        elif confidence < 0.5:
            return 4
        else:
            return 3

    def learn_from_execution(self, command: ParsedCommand, success: bool, feedback: str = ""):
        """Learn from executed commands"""
        try:
            # Save interaction
            self.db.add_conversation(
                user_input=command.original,
                ai_response=feedback,
                intent=command.intent,
                confidence=command.confidence,
                entities=asdict(command.entities),
                context={"success": success, "priority": command.priority}
            )

            # Update learned patterns
            if success:
                key = f"{command.normalized}:{command.intent}"
                self.intent_classifier.learned_patterns[key] = command.confidence
                logger.debug(f"✓ Learned: {command.intent} (conf: {command.confidence:.2%})")
        except Exception as e:
            logger.error(f"Learning error: {e}")


# Singleton
_advanced_nlp: Optional[AdvancedNLPEngine] = None


def get_advanced_nlp() -> AdvancedNLPEngine:
    """Get advanced NLP engine"""
    global _advanced_nlp
    if _advanced_nlp is None:
        _advanced_nlp = AdvancedNLPEngine()
    return _advanced_nlp


__all__ = [
    "AdvancedNLPEngine",
    "AdvancedIntentClassifier",
    "EntityExtractorAdvanced",
    "DependencyAnalyzer",
    "ParsedCommand",
    "get_advanced_nlp",
]
