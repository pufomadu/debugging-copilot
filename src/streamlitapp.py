import streamlit as st
import logging
from tiered_helper import answer  # The helper function for tiered responses

# Setup logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Streamlit page configuration
st.set_page_config(
    page_title="Debugging Copilot",
    page_icon="🐞",
    layout="wide"
)

# Page title and description
st.title("🐍 Debugging Copilot: Tiered Python Help")
st.markdown("""
Welcome to the **Debugging Copilot**!  
Drop your Python error message, code snippet or general question, and select the help tier you want.

Tiers:
- **1** – Quick hint or where to look  
- **2** – Step-by-step guidance  
- **3** – Near-solution with outline  
- **4** – Full fix (only if needed or asked)
""")

# Sidebar for tier selection
st.sidebar.header("🧠 Select Help Tier")
tier_label = st.sidebar.radio(
    "Pick a help level:",
    ["1 - Nudge", "2 - Guided Steps", "3 - Near-solution", "4 - Full Solution"]
)

tier_map = {
    "1 - Nudge": 1,
    "2 - Guided Steps": 2,
    "3 - Near-solution": 3,
    "4 - Full Solution": 4
}
selected_tier = tier_map[tier_label]

# Input areas for error message and code snippet
error_msg = st.text_area("🛑 Paste your Python message here:", height=150)
code_snippet = st.text_area("🧾 Paste your code snippet (optional):", height=200)

# Button to generate help
if st.button("🚀 Generate Help"):
    if not error_msg.strip():
        st.warning("Please provide a message first.")
    else:
        with st.spinner("Analyzing your issue..."):
            try:
                # 🔍 Call the helper function
                result = answer(
                    query=error_msg.strip(),
                    code_snippet=code_snippet.strip(),
                    explicit_request=selected_tier
                )

                st.success("✅ Response Generated!")
                logger.info("✅ Displaying result")

                # Display structured result if JSON format is returned
                if isinstance(result, dict):
                    st.markdown(f"### 🧩 Tier {result.get('tier', '?')} Help")
                    st.markdown(f"**Message:** {result.get('message', '')}")

                    if result.get("steps"):
                        st.markdown("**Steps:**")
                        for step in result["steps"]:
                            st.markdown(f"- {step}")

                    if result.get("code_hint"):
                        st.markdown("**Code Hint:**")
                        st.code(result["code_hint"])

                    if result.get("citations"):
                        st.markdown("**📚 Citations:**")
                        for c in result["citations"]:
                            st.markdown(f"- {c['source']} ({c['anchor']})")

                # Fallback for plain string responses
                elif isinstance(result, str):
                    st.markdown("**📝 Answer:**")
                    st.markdown(result)

                else:
                    st.warning("⚠️ Unexpected result format. Please try again.")

            except Exception as e:
                logger.error(f"❌ Error in Streamlit app: {e}")
                st.error(f"Something went wrong: {e}")

# Footer
st.markdown("---")
st.markdown("The Bug-A-Boo-Team· Debugging Copilot Project")
