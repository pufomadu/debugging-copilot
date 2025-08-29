import streamlit as st
import logging
from tiered_helper import answer  # Your helper that routes the request

# === Setup logging ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Streamlit Page Setup ===
st.set_page_config(
    page_title="Debugging Copilot",
    page_icon="🐞",
    layout="wide"
)

# === Page Title & Instructions ===
st.title("🐍 Debugging Copilot: Tiered Python Help")
st.markdown("""
Welcome to the **Debugging Copilot**!  
Drop your Python error message, code snippet or general question, and select the help tier you want.

Tiers:
- **1** – Quick nudge or where to look  
- **2** – Step-by-step guidance  
- **3** – Near-solution with outline  
- **4** – Full fix (only if needed or asked)
""")

# === Sidebar: Tier Selection ===
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

# === Input Section ===
error_msg = st.text_area("🛑 Paste your Python message here:", height=150)
code_snippet = st.text_area("🧾 Paste your code snippet (optional):", height=200)

# === Action Button ===
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
                st.text(f"[DEBUG] Type: {type(result)} — Raw Output:\n{result}")

                st.success("✅ Response Generated!")
                logger.info("✅ Displaying result")

                # Display raw result in debug block
                st.text("[DEBUG] Raw result:")
                st.code(result)

                # Display structured result if JSON format is returned
                if isinstance(result, dict):
                    st.markdown(f"### 🧩 Tier {result.get('tier', '?')} Help")
                    st.markdown(f"**Message:** {result.get('message', '')}")

                    if "steps" in result and isinstance(result["steps"], list):
                        st.markdown("**Steps:**")
                        for step in result["steps"]:
                            st.markdown(f"- {step}")

                    if result.get("code_hint"):
                        st.markdown("**Code Hint:**")
                        st.code(result["code_hint"])

                    if "citations" in result and result["citations"]:
                        st.markdown("**📚 Citations:**")
                        for c in result["citations"]:
                            st.markdown(f"- {c['source']} ({c['anchor']})")

                elif isinstance(result, str):
                    st.markdown("**📝 Answer:**")
                    st.markdown(f"```python\n{result}\n```")

                else:
                    st.warning("⚠️ Unexpected result format. Please try again.")

            except Exception as e:
                logger.error(f"❌ Error in Streamlit app: {e}")
                st.error(f"Something went wrong: {e}")

# === Footer ===
st.markdown("---")
st.markdown("Made with ❤️ by The Knowledge House · Debugging Copilot Project")
