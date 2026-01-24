"""
Coreus Workflow Orchestrator (Reference Implementation)
-------------------------------------------------------
Demonstrates the agent chaining interface.

ARCHITECTURAL NOTE:
This implementation runs a linear execution chain for demonstration.
The production engine utilizes a Cyclic Graph State Machine 
supporting parallel branches, dynamic rerouting, and self-healing loops.
"""

from typing import List, Dict, Any, Callable
import time

class ReferenceWorkflowEngine:
    """
    Linear workflow executor for functional verification.
    """
    
    def __init__(self):
        self._steps: List[Dict[str, Any]] = []

    def add_step(self, name: str, function: Callable[[str], str]):
        self._steps.append({
            "name": name,
            "func": function
        })

    def execute(self, initial_input: str) -> Dict[str, Any]:
        context = {"input": initial_input, "history": []}
        current_data = initial_input
        
        print(f"\n--- Executing Linear Chain ({len(self._steps)} steps) ---")
        
        for step in self._steps:
            step_name = step["name"]
            print(f"> Step: {step_name}")
            
            try:
                start_time = time.time()
                result = step["func"](current_data)
                duration = time.time() - start_time
                
                context["history"].append({
                    "step": step_name,
                    "output": result,
                    "latency": f"{duration:.3f}s"
                })
                current_data = result
                
            except Exception as e:
                context["error"] = str(e)
                break
                
        context["final_output"] = current_data
        return context
