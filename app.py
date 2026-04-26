import re
import streamlit as st
import ollama
import PyPDF2
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from pydantic import BaseModel

# Pydantic model for structured output
class LoanDetails(BaseModel):
    loan_amount: float
    interest_rate: float
    tenure_months: int
    emi: float

st.set_page_config(page_title="Smart Loan EMI Advisor", layout="wide")

st.title("💰 Smart Loan EMI Advisor")

st.caption("AI Powered Loan Decision Assistant")

# Document upload
st.subheader("📄 Upload Document for Q&A")
uploaded_file = st.file_uploader("Upload a document (PDF or TXT) to ask questions about", type=["pdf", "txt"])

if uploaded_file is not None:
    try:
        if uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        else:
            text = str(uploaded_file.read(), "utf-8")
        
        # Chunk the document
        chunk_size = 1000
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        
        # Generate embeddings
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model.encode(chunks)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        
        # Store in session
        st.session_state['chunks'] = chunks
        st.session_state['index'] = index
        st.session_state['embedding_model'] = model
        st.session_state['full_document'] = text
        
        st.success("Document uploaded and indexed! You can now ask questions about it.")
        
        # Extract structured data
        if st.button("Extract Loan Details"):
            try:
                schema = LoanDetails.model_json_schema()
                prompt = f"Extract loan details from this document in JSON format matching this schema: {schema}\n\nDocument: {text[:4000]}..."
                response = ollama.chat(model='llama3.2:1b', messages=[{"role": "user", "content": prompt}])
                json_str = response['message']['content']
                # Parse JSON
                import json
                data = json.loads(json_str)
                details = LoanDetails(**data)
                st.json(details.dict())
            except Exception as e:
                st.error(f"Could not extract details: {str(e)}")
    except Exception as e:
        st.error(f"Error processing document: {str(e)}")

# EMI function
def calculate_emi(principal: float, annual_rate: float, months: int) -> float:
    """
    Calculate monthly EMI for a loan.

    Args:
      principal: Loan amount.
      annual_rate: Annual interest rate in percent.
      months: Number of months to repay.

    Returns:
      float: Monthly EMI rounded to two decimals.
    """
    r = annual_rate / 12 / 100
    emi = principal * r * (1 + r) ** months / ((1 + r) ** months - 1)
    return round(emi, 2)


def parse_tool_argument(value):
    if isinstance(value, str):
        cleaned = re.sub(r'[^\d\.\-]', '', value)
        if cleaned == '':
            return value
        if '.' in cleaned:
            return float(cleaned)
        return int(cleaned)
    return value


def clean_response(text):
    """Remove tool parameter JSON blocks and technical details from response text."""
    # Remove JSON blocks like {"name": "calculate_emi", "parameters": {...}}
    text = re.sub(r'\{\s*"name"\s*:\s*"[^"]+"\s*,\s*"parameters"\s*:\s*\{.*?\}\s*\}', '', text, flags=re.DOTALL)
    # Remove lines that are pure code/function examples
    lines = text.split('\n')
    filtered_lines = []
    for line in lines:
        # Skip lines that are pure code/function calls
        if re.match(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*\(.*\)\s*$', line):
            continue
        filtered_lines.append(line)
    result = '\n'.join(filtered_lines).strip()
    # Remove excessive newlines
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result

# Sidebar
st.sidebar.header("Loan Calculator")

loan = st.sidebar.number_input("Loan Amount ₹", 10000, 10000000, 500000)
rate = st.sidebar.number_input("Interest Rate %", 1.0, 25.0, 10.0)
months = st.sidebar.number_input("Months", 1, 360, 60)

# Affordability inputs
st.sidebar.header("Loan Affordability Check")
monthly_salary = st.sidebar.number_input("Monthly Salary ₹", 10000, 1000000, 50000)
monthly_expenses = st.sidebar.number_input("Monthly Expenses ₹", 0, 500000, 20000)

if st.sidebar.button("Calculate EMI"):
    emi = calculate_emi(loan, rate, months)
    total = round(emi * months, 2)
    interest = round(total - loan, 2)

    st.success(f"Monthly EMI: ₹{emi}")
    st.write(f"Total Payment: ₹{total}")
    st.write(f"Total Interest: ₹{interest}")

    # Affordability check
    disposable = monthly_salary - monthly_expenses
    if disposable > 0:
        emi_percentage = (emi / disposable) * 100
        if emi_percentage < 30:
            st.write(f"✅ EMI is {emi_percentage:.1f}% of disposable income - Affordable!")
        elif emi_percentage < 50:
            st.write(f"⚠️ EMI is {emi_percentage:.1f}% of disposable income - Manageable but tight")
        else:
            st.write(f"❌ EMI is {emi_percentage:.1f}% of disposable income - Not recommended")
    else:
        st.write("❌ Expenses exceed salary - Review your budget first")

# Chat section
st.subheader("Ask Loan AI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# System prompt
system_prompt = """You are a loan EMI advisor. Answer questions about loans, EMI, interest rates, principal, tenure, and affordability.

RULES:
- Definition questions (what is loan, what is principal, etc): Answer in 1-2 sentences directly. No extra context.
- EMI/calculation questions: Use the calculate_emi tool. NEVER show tool parameters or function details to the user.
- Non-loan questions: Say "Invalid - This is not a loan/finance question."

IMPORTANT: NEVER show tool calls, function parameters, JSON, or code to the user. Only show final answers.
Be brief. Answer immediately without asking for more details."""

# Chat input
if prompt := st.chat_input("Ask me about loans and EMI..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response using Ollama
    try:
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add document context if available
        if 'index' in st.session_state:
            query_emb = st.session_state['embedding_model'].encode([prompt])
            D, I = st.session_state['index'].search(query_emb, k=3)  # top 3 chunks
            context = "\n".join([st.session_state['chunks'][i] for i in I[0]])
            messages.append({"role": "system", "content": f"Use this document context to answer: {context}"})
        
        messages += st.session_state.messages

        tools = [calculate_emi]
        response = ollama.chat(model='llama3.2:1b', tools=tools, messages=messages)

        # If Ollama chooses a tool, execute it locally and continue the chat with the tool result
        if response.message.tool_calls:
            tool_map = {calculate_emi.__name__: calculate_emi}
            for tool_call in response.message.tool_calls:
                function_name = tool_call.function.name
                if function_name in tool_map:
                    # Extract only the expected parameters for the function
                    import inspect
                    sig = inspect.signature(tool_map[function_name])
                    raw_args = dict(tool_call.function.arguments)
                    arguments = {
                        k: parse_tool_argument(raw_args[k])
                        for k in sig.parameters.keys()
                        if k in raw_args
                    }
                    try:
                        tool_result = tool_map[function_name](**arguments)
                        messages.append({
                            "role": "tool",
                            "name": function_name,
                            "content": str(tool_result),
                        })
                    except Exception as e:
                        messages.append({
                            "role": "tool",
                            "name": function_name,
                            "content": f"Error executing tool: {str(e)}",
                        })
                else:
                    messages.append({
                        "role": "tool",
                        "name": function_name,
                        "content": f"Error: unknown tool {function_name}",
                    })

            response = ollama.chat(model='llama3.2:1b', tools=tools, messages=messages)

        ai_response = response.message.content
        # Clean any remaining tool parameters or technical details
        if ai_response:
            ai_response = clean_response(ai_response)
            # If response is empty after cleaning, handle gracefully
            if not ai_response or ai_response.isspace():
                ai_response = "I was unable to generate a proper response. Please try again."
    except Exception as e:
        ai_response = f"Sorry, I'm having trouble connecting to the AI. Error: {str(e)}. Please try again later."
    
    # Add AI response to history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    
    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(ai_response)