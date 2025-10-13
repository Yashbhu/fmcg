# run_workflow.py
import pandas as pd
from typing import TypedDict, Optional

# LangGraph is the engine for our workflow
from langgraph.graph import StateGraph, END

# Import the logic functions from our other files
from sales_agent_logic import scrape_all_tenders as scan_and_select_rfp

from technical_agent_logic import analyze_rfp_specs
from pricing_agent_logic import calculate_pricing

# Step 1: Define the state that will be passed between agents
class RfpWorkflowState(TypedDict):
    """Represents the shared memory of our RFP workflow."""
    # We no longer need rfp_source_file, so it has been removed.
    selected_rfp: Optional[dict]
    technical_analysis: Optional[pd.DataFrame]
    final_pricing: Optional[pd.DataFrame]
    error: str = None

# Step 2: Create the nodes for each agent in our graph
def sales_node(state):
    print("\n--- [Node: Sales Agent] ---")
    # This function no longer needs an argument since it scrapes a live URL.
    rfp = scan_and_select_rfp() # <-- CHANGED
    return {"selected_rfp": rfp} if rfp else {"error": "No actionable RFP found."}

def technical_node(state):
    print("\n--- [Node: Technical Agent] ---")
    analysis = analyze_rfp_specs(state["selected_rfp"])
    return {"technical_analysis": analysis} if analysis is not None else {"error": "Technical analysis failed."}

def pricing_node(state):
    print("\n--- [Node: Pricing Agent] ---")
    pricing = calculate_pricing(state["technical_analysis"])
    return {"final_pricing": pricing} if pricing is not None else {"error": "Pricing calculation failed."}

# Step 3: Define the conditional logic (edges) for the graph
def should_continue(state):
    """If an error is present in the state, end the workflow. Otherwise, continue."""
    return "end" if state.get("error") else "continue"

# Step 4: Build the graph
# This is where we wire everything together.
workflow = StateGraph(RfpWorkflowState)

# Add the nodes
workflow.add_node("sales", sales_node)
workflow.add_node("technical", technical_node)
workflow.add_node("pricing", pricing_node)

# Set the entry point
workflow.set_entry_point("sales")

# Add the conditional edges
workflow.add_conditional_edges("sales", should_continue, {"continue": "technical", "end": END})
workflow.add_conditional_edges("technical", should_continue, {"continue": "pricing", "end": END})

# The pricing node is the last step, so it connects to the end
workflow.add_edge("pricing", END)

# Compile the graph into a runnable application
app = workflow.compile()

# --- RUN THE WORKFLOW ---
print("🚀🚀🚀 Workflow Starting... 🚀🚀🚀")

# We no longer need to provide an initial state with a filename.
# We invoke the graph with an empty dictionary.
final_state = app.invoke({}) # <-- CHANGED

print("\n\n--- ✨ FINAL RFP RESPONSE SUMMARY ✨ ---")
if final_state.get("error"):
    print(f"\n❗️ Workflow Halted with Error: {final_state['error']}")
else:
    print("\n✅ Workflow Completed Successfully!")
    print("\n📋 Final Pricing and Product Recommendation:")
    # Neatly print the final result
    print(final_state['final_pricing'][['RFP_Item', 'Recommended_SKU', 'Total_Cost']].to_string(index=False))