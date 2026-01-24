"""
Coreus Framework - Showcase Demo
--------------------------------
This script demonstrates how to build a scalable multi-agent pipeline 
using the Coreus structure.

Scenario: A 'Writer Agent' generates content, and a 'Critic Agent' 
validates it against specific keyword constraints.
"""

import sys
import os

# Path hack to import local 'core'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.memory import MemoryManager
from core.orchestration.workflow import ReferenceWorkflowEngine as WorkflowManager
from core.evaluation.evaluator import Evaluator

def main():
    print("==========================================")
    print("   COREUS FRAMEWORK - SHOWCASE DEMO       ")
    print("   Agentic Infrastructure Framework       ")
    print("==========================================\n")

    # 1. Initialize Components
    memory = MemoryManager()
    workflow = WorkflowManager()
    
    # Configure Evaluator with specific heuristic rules
    # This demonstrates detailed control over quality gates
    evaluator = Evaluator(
        required_keywords=["AI", "optimizing"], 
        min_length=20
    )

    # 2. Define Agents 
    def writer_agent(input_text: str) -> str:
        print(f"   [Agent:Writer] Processing request: '{input_text}'...")
        # Simulate creative work
        return "The AI agent is optimizing the pathfinding algorithm logic."

    def critic_agent(input_text: str) -> str:
        print(f"   [Agent:Critic] Auditing content...")
        result = evaluator.evaluate(input_text)
        
        if result["status"] == "FAIL":
            print(f"   [Review] REJECTED. Feedback: {result['feedback']}")
            return f"REJECTED: {result['feedback']}"
            
        print(f"   [Review] APPROVED. Score: {result['score']}")
        return f"APPROVED CONTENT: {input_text}"

    # 3. Build Pipeline
    workflow.add_step("Content Generation", writer_agent)
    workflow.add_step("Quality Audit", critic_agent)

    # 4. Simulate User Request
    user_id = "demo_session_01"
    user_query = "Write a technical sentence."
    
    # Store context
    memory.add_message(user_id, "user", user_query)

    # Run Workflow
    result = workflow.execute(user_query)

    # Store result
    if "final_output" in result:
        memory.add_message(user_id, "assistant", str(result["final_output"]))

    print("\n[Pipeline Result Metadata]:")
    print(f"Steps Executed: {len(result.get('history', []))}")
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print("Status: SUCCESS")

if __name__ == "__main__":
    main()
