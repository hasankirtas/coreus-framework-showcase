"""
Coreus Evaluator (Showcase Implementation)
------------------------------------------
Demonstrates the 'Quality Gate' interface.

In the Coreus architecture, evaluation is a pluggable strategy.
While this reference implementation uses deterministic heuristics 
(keyword density, length checks), production systems inject 
LLM-based critics or domain-specific rule engines dynamically.
"""

from typing import Dict, Any, List, Optional

class Evaluator:
    """
    heuristic-based output validator.
    Evaluate content based on predefined criteria constraints.
    """
    
    def __init__(self, required_keywords: Optional[List[str]] = None, min_length: int = 10):
        self.required_keywords = required_keywords or []
        self.min_length = min_length
    
    def evaluate(self, content: str) -> Dict[str, Any]:
        """
        Audit the content against scoring rules.
        """
        score = 0.0
        feedback = []
        
        # Criterion 1: Length check (30% weight)
        if len(content) >= self.min_length:
            score += 0.3
        else:
            feedback.append(f"Content length ({len(content)}) below minimum ({self.min_length})")
            
        # Criterion 2: Keyword presence (70% weight)
        # Simple simulation of semantic relevance check
        if not self.required_keywords:
            score += 0.7 # No specific keywords required
        else:
            matches = [kw for kw in self.required_keywords if kw.lower() in content.lower()]
            match_ratio = len(matches) / len(self.required_keywords)
            score += (0.7 * match_ratio)
            
            if match_ratio < 1.0:
                missing = set(self.required_keywords) - set(matches)
                feedback.append(f"Missing required concepts: {', '.join(missing)}")
        
        # Decision Logic
        is_passing = score >= 0.7
        
        return {
            "status": "PASS" if is_passing else "FAIL",
            "score": round(score, 2),
            "feedback": "; ".join(feedback) if feedback else "Content meets quality standards.",
            "metrics": {
                "length": len(content),
                "keyword_matches": len(matches) if self.required_keywords else "N/A"
            }
        }
