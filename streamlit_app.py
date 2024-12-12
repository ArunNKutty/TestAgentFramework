import streamlit as st
from router.agent_router import AgentRouter
from agents.agent_factory import AgentFactory

st.set_page_config(
    page_title="Tinno QA Agents",
    page_icon="🤖",
    layout="wide"
)

st.title("Tinno QA 🤖")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "router" not in st.session_state:
    st.session_state.router = AgentRouter()

# Sidebar for available agents
with st.sidebar:
    st.header("Available Agents")
    st.write("Currently available specialized agents:")
    for agent_type in AgentFactory.get_available_agents():
        st.write(f"- {agent_type.title()} Agent")
    
    st.markdown("""
    ---
    **How it works:**
    1. Your query is analyzed by the Router
    2. Complex queries are broken down into sub-tasks
    3. Each sub-task is sent to the appropriate agent
    4. Results are combined into a comprehensive response
    """)
    
    st.write("Made with ❤️ by CBI Team")
    st.write("Contact Vignesh if the Agents go rogue as he is training them")

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask anything..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Process query through router
        result = st.session_state.router.process_query(prompt)
        
        if result["status"] == "clarification_needed":
            response = f"🤔 I need some clarification: {result['message']}"
        else:
            # Format the response with decomposition info
            response_parts = []
            
            # Add decomposition info if more than one sub-query
            if len(result["results"]) > 1:
                response_parts.append("I've broken down your query into parts:\n")
                for i, decomp in enumerate(result["decomposition"], 1):
                    response_parts.append(f"{i}. {decomp['sub_query']} ({decomp['agent'].title()} Agent)")
                response_parts.append("\nHere are the answers:\n")
            
            # Add results
            for i, res in enumerate(result["results"], 1):
                if len(result["results"]) > 1:
                    response_parts.append(f"\n**Part {i}** (via {res['agent'].title()} Agent):")
                response_parts.append(res["response"])
            
            response = "\n".join(response_parts)
        
        message_placeholder.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})