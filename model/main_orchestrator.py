# main_orchestrator.py
from model.sales_agent_logic import scan_and_select_rfp

class MainOrchestrator:
    def __init__(self, rfp_source_file):
        self.rfp_source = rfp_source_file
        self.selected_rfp = None
        self.technical_response = None
        self.pricing_response = None

    def run_workflow(self):
        """
        Executes the entire RFP response workflow step-by-step.
        """
        print("""
## 🚀 Starting New RFP Response Workflow... ##
""") # <-- CHANGED

        # Step 1: Call Sales Agent to find an RFP
        print("--- [Step 1: Sales Agent] ---")
        self.selected_rfp = scan_and_select_rfp(self.rfp_source)

        # If Sales Agent finds nothing, the workflow stops.
        if not self.selected_rfp:
            print("""
##  Workflow ENDED: No actionable RFP found. ##
""") # <-- CHANGED
            return

        print("""
📬 Orchestrator: Received RFP from Sales Agent.
""") # <-- CHANGED
        print(f"   - RFP Title: {self.selected_rfp['title']}")

        # --- Future Steps (We will build these next) ---

        # Step 2: Delegate to Technical Agent
        print("""
--- [Step 2: Technical Agent] ---""") # <-- CHANGED
        print("   - Task: Analyze technical specs and match products.")
        print("   - Status: PENDING...")
        # self.technical_response = technical_agent.analyze(self.selected_rfp)

        # Step 3: Delegate to Pricing Agent
        print("""
--- [Step 3: Pricing Agent] ---""") # <-- CHANGED
        print("   - Task: Calculate material and service costs.")
        print("   - Status: PENDING...")
        # self.pricing_response = pricing_agent.calculate(self.technical_response)

        # Step 4: Consolidate final response
        print("""
--- [Step 4: Final Consolidation] ---""") # <-- CHANGED
        print("   - Task: Combine all agent responses into a final summary.")
        print("   - Status: PENDING...")
        # final_summary = self.consolidate_responses()
        
        print("""
## ✅ Workflow Paused: Waiting for Technical & Pricing Agents to be built. ##
""") # <-- CHANGED


# --- Main execution ---
if __name__ == "__main__":
    # The orchestrator is the entry point for the entire process.
    orchestrator = MainOrchestrator(rfp_source_file='rfp_page_1.html')
    orchestrator.run_workflow()