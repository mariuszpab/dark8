# DARK8 OS - NLP Engine (Polish Natural Language Processing)
"""
NLP module for Polish language understanding.
Handles intent classification, entity extraction, and semantic parsing.
"""

from pathlib import Path
import json
from typing import Dict, List, Tuple, Optional
import pickle

from dark8_core.logger import logger
from dark8_core.config import config


class IntentClassifier:
    """Classify user intent from Polish text"""
    
    # Polish intents (expandable)
    INTENTS = {
        "BUILD_APP": ["zbuduj", "stwórz", "utwórz", "napisz aplikację"],
        "SEARCH": ["szukaj", "wyszukaj", "znajdź", "przeszukaj"],
        "OPEN_BROWSER": ["otwórz", "przejdź", "odwiedź", "zwizytuj stronę"],
        "LIST_FILES": ["wyświetl", "pokaż", "lista", "zawartość"],
        "READ_FILE": ["czytaj", "przeczytaj", "pokaż zawartość"],
        "WRITE_FILE": ["zapisz", "utwórz plik", "edytuj"],
        "DELETE": ["usuń", "skasuj", "wymaż"],
        "EXECUTE_COMMAND": ["uruchom", "spuść", "wykonaj", "zapal"],
        "ANALYZE_CODE": ["analizuj", "przeanalizuj kod", "sprawdź"],
        "GIT_OPERATION": ["commituj", "push", "pull", "merguj", "version control"],
        "INSTALL": ["zainstaluj", "pobierz", "instaluj pakiet"],
        "HELP": ["pomoc", "przydatne", "jak używać"],
        "STATUS": ["status", "stan", "jak się masz"],
        "EXIT": ["wyjdź", "koniec", "wyłącz", "Stop"],
    }
    
    @classmethod
    def classify(cls, text: str) -> Tuple[str, float]:
        """
        Classify intent from Polish text.
        Returns: (intent_name, confidence_score)
        """
        text_lower = text.lower()
        
        # Simple keyword matching (will be upgraded to BERT-based)
        for intent, keywords in cls.INTENTS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    # Simple confidence scoring
                    confidence = 0.7 + (0.3 * (len(keyword) / len(text_lower)))
                    return intent, min(confidence, 1.0)
        
        return "UNKNOWN", 0.0


class EntityExtractor:
    """Extract entities from Polish text"""
    
    # Polish entity patterns
    ENTITY_TYPES = {
        "FILE_PATH": [".py", ".js", ".java", "/", "plik", "katalog"],
        "FRAMEWORK": ["django", "flask", "fastapi", "react", "vue", "angular"],
        "LANGUAGE": ["python", "javascript", "java", "cpp", "rust", "go"],
        "DATABASE": ["postgresql", "mysql", "mongodb", "redis"],
        "TOOL": ["git", "docker", "kubernetes", "npm", "pip"],
    }
    
    @classmethod
    def extract(cls, text: str) -> Dict[str, List[str]]:
        """
        Extract entities from Polish text.
        Returns: {entity_type: [values]}
        """
        entities = {}
        text_lower = text.lower()
        
        for entity_type, patterns in cls.ENTITY_TYPES.items():
            entities[entity_type] = []
            for pattern in patterns:
                if pattern in text_lower:
                    entities[entity_type].append(pattern)
        
        return {k: v for k, v in entities.items() if v}


class PolishParser:
    """Parse Polish sentence structure"""
    
    @staticmethod
    def tokenize(text: str) -> List[str]:
        """Simple tokenization for Polish text"""
        # Replace Polish characters
        replacements = {
            'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l',
            'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new).replace(old.upper(), new.upper())
        
        # Split on whitespace and punctuation
        tokens = text.replace(".", " ").replace(",", " ").replace("!", " ").split()
        return [t for t in tokens if t]
    
    @staticmethod
    def normalize(text: str) -> str:
        """Normalize Polish text"""
        # Remove extra whitespace
        text = " ".join(text.split())
        # Lowercase
        return text.lower()


class NLPEngine:
    """Main NLP Engine for Polish language"""
    
    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.entity_extractor = EntityExtractor()
        self.parser = PolishParser()
        logger.info("✓ NLP Engine initialized")
    
    def understand(self, user_input: str) -> Dict:
        """
        Full NLP pipeline: tokenize, intent, entities, parse
        Returns: {
            'original_text': str,
            'normalized_text': str,
            'tokens': [str],
            'intent': str,
            'confidence': float,
            'entities': {entity_type: [values]},
        }
        """
        # Normalize
        normalized = self.parser.normalize(user_input)
        
        # Tokenize
        tokens = self.parser.tokenize(normalized)
        
        # Classify intent
        intent, confidence = self.intent_classifier.classify(normalized)
        
        # Extract entities
        entities = self.entity_extractor.extract(normalized)
        
        result = {
            'original_text': user_input,
            'normalized_text': normalized,
            'tokens': tokens,
            'intent': intent,
            'confidence': confidence,
            'entities': entities,
        }
        
        return result
    
    def is_valid_command(self, user_input: str, min_confidence: float = 0.5) -> bool:
        """Check if input is a valid command"""
        result = self.understand(user_input)
        return result['confidence'] >= min_confidence and result['intent'] != 'UNKNOWN'


# Singleton instance
_nlp_engine: Optional[NLPEngine] = None


def get_nlp_engine() -> NLPEngine:
    """Get or create NLP engine singleton"""
    global _nlp_engine
    if _nlp_engine is None:
        _nlp_engine = NLPEngine()
    return _nlp_engine


__all__ = [
    "NLPEngine",
    "IntentClassifier",
    "EntityExtractor",
    "PolishParser",
    "get_nlp_engine",
]
