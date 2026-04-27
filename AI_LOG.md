# AI_LOG.md

## Project Duration
Work completed from **Thursday, 23 April 2026** to **Sunday, 26 April 2026 (yesterday)**

## Tools used
- ChatGPT – used for project planning, debugging, code generation, explanations, and documentation help  
- GitHub Copilot – used for inline code suggestions and autocomplete in Visual Studio Code  

---

## Significant prompts

### 1. Date: Thursday, 23 April 2026  
### Prompt:
"Create a Loan EMI Advisor project using HTML, CSS, JavaScript, and Python backend."

**What AI produced:**  
Generated a project structure with frontend pages, EMI input form, calculator logic, and backend connection ideas.

**What I kept / rejected and why:**  
- Kept the EMI calculator form, frontend layout, and backend workflow.  
- Rejected advanced features like login system and database because the project needed to stay simple.  

---

### 2. Date: Friday, 24 April 2026  
### Prompt:
"Give 100+ loan related questions for chatbot training."

**What AI produced:**  
A list of common loan-related questions such as EMI, interest rate, tenure, eligibility, foreclosure, and repayment topics.

**What I kept / rejected and why:**  
- Kept useful and common customer questions.  
- Rejected repeated and overly technical banking questions to keep responses clear.  

---

### 3. Date: Saturday, 25 April 2026  
### Prompt:
"Fix my Python backend code error."

**What AI produced:**  
Suggested corrected indentation, missing colons, proper function definitions, and variable usage fixes.

**What I kept / rejected and why:**  
- Kept syntax and indentation fixes after testing.  
- Rejected one suggested variable rename because it would affect other connected parts of the code.  

---

### 4. Date: Saturday, 25 April 2026  
### Prompt:
"How to connect frontend with localhost backend?"

**What AI produced:**  
Explained localhost, ports, running a local server, and using fetch() API requests from frontend to backend.

**What I kept / rejected and why:**  
- Kept localhost explanation and API connection steps.  
- Rejected deployment-related steps because only local testing was required.  

---

### 5. Date: Sunday, 26 April 2026  
### Prompt:
"Improve my EMI Advisor UI using CSS."

**What AI produced:**  
Suggested better colors, spacing, buttons, card layout, and responsive design improvements.

**What I kept / rejected and why:**  
- Kept clean card design, button styling, and spacing improvements.  
- Rejected heavy animations because simple performance was preferred.  

---

## A bug your AI introduced

**Date: Sunday, 26 April 2026**

AI once suggested JavaScript EMI calculation code without converting input values from text to numbers.  
This caused incorrect EMI output.

**How I caught it:**  
I tested sample values and the result was wrong.

**Fix:**  
Used `parseFloat()` / `Number()` before calculation.

---

## A design choice you made against AI suggestion

**Date: Sunday, 26 April 2026**

AI suggested adding dashboards, charts, and user login features.

I ignored that suggestion and kept the project as a simple Loan EMI Advisor.

**Why:**  
The project requirement was a basic, easy-to-use student project. Simplicity was better than unnecessary complexity.

---

## Time split

- Writing code: 35%  
- Prompting AI tools: 20%  
- Reviewing AI output: 15%  
- Debugging: 15%  
- Testing: 10%  
- Reading documentation: 5%
