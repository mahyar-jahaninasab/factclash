# System 

## Input 

Below is the complete text fed into the LLM, formatted using Markdown diff markers (`+` for positive assertions $P$, `-` for negative assertions $\neg P$) and inline text highlighting to visually pinpoint where strict contradictions collide across the **History**, **Retrieved Information**, and **Prompt**.

```diff
================================= CONTEXT WINDOW START =================================

--- [SECTION 1: CHAT HISTORY] ---
User: What is the current status of server `srv-prod-01` and its SSL certificate?
Assistant: I checked the last status update.
+ [Fact P1] Server `srv-prod-01` IS RUNNING.

--- [SECTION 2: RETRIEVED INFORMATION (RAG Context)] ---
Document ID: doc_live_telemetry_2026
Timestamp: 2026-10-21 09:30:00 UTC
- [Fact ¬P1] Server `srv-prod-01` IS NOT RUNNING. (System State: Terminated)
+ [Fact P2]  SSL Certificate #402 IS VALID. (Expiration: 90 days remaining)

--- [SECTION 3: USER PROMPT] ---
User: Since server `srv-prod-01` is running, why are you reporting that SSL Certificate #402 IS NOT VALID?
+ [Fact P1]  Premise: Server `srv-prod-01` IS RUNNING.
- [Fact ¬P2] Premise: SSL Certificate #402 IS NOT VALID.

================================== CONTEXT WINDOW END ==================================
```

## Detection 

### Contradiction Type: Strict Contradiction

#### Fact 1: Operational Status of Server `srv-prod-01`
* **Fact Subject:** Operational State of Server `srv-prod-01`
* **Logical Representation:** $P_1 \land \neg P_1$
* **Claims:**
  * **Claim 1.1:**
    * **Source:** Chat History
    * **Statement:** `"Server srv-prod-01 IS RUNNING."`
    * **Logical State:** $P_1$
  * **Claim 1.2:**
    * **Source:** Retrieved Information (RAG Context)
    * **Statement:** `"Server srv-prod-01 IS NOT RUNNING. (System State: Terminated)"`
    * **Logical State:** $\neg P_1$
  * **Claim 1.3:**
    * **Source:** User Prompt
    * **Statement:** `"Since server srv-prod-01 is running..."`
    * **Logical State:** $P_1$
* **Conflict Analysis:** Claims 1.1 and 1.3 ($P_1$) directly contradict Claim 1.2 ($\neg P_1$). A binary system operational state cannot be simultaneously running ($1$) and not running ($0$).

#### Fact 2: Validity Status of SSL Certificate #402
* **Fact Subject:** Validity State of Certificate #402
* **Logical Representation:** $P_2 \land \neg P_2$
* **Claims:**
  * **Claim 2.1:**
    * **Source:** Retrieved Information (RAG Context)
    * **Statement:** `"SSL Certificate #402 IS VALID. (Expiration: 90 days remaining)"`
    * **Logical State:** $P_2$
  * **Claim 2.2:**
    * **Source:** User Prompt
    * **Statement:** `"...why are you reporting that SSL Certificate #402 IS NOT VALID?"`
    * **Logical State:** $\neg P_2$
* **Conflict Analysis:** Claim 2.1 ($P_2$) directly contradicts Claim 2.2 ($\neg P_2$). A digital certificate's validation status is strictly boolean; it cannot be valid and invalid at the same time.

## output

Below is the structured output categorizing each detected contradiction into its domain field, along with the detection confidence score and supportive rationale.

Example 1:
| Contradiction Type | Score | Primary Conflict Sources | Supporting Claims (Group 1) | Contradicting Claims (Group 2) |
| --- | --- | --- | --- | --- |
| Strict Contradiction | 0.98 | Chat History / User Prompt vs. RAG Context | • **Chat History:** *"Server srv-prod-01 IS RUNNING."* ($P_1$); **User Prompt:** *"Since server srv-prod-01 is running..."* ($P_1$) | • **RAG Context:** *"Server srv-prod-01 IS NOT RUNNING. (System State: Terminated)"* ($\neg P_1$) |
| Strict Contradiction | 0.95 | RAG Context vs. User Prompt | • **RAG Context:** *"SSL Certificate #402 IS VALID. (Expiration: 90 days remaining)"* ($P_2$) | • **User Prompt:** *"...why are you reporting that SSL Certificate #402 IS NOT VALID?"* ($\neg P_2$) |
| Contrary Contradiction | None| None | None | None |
| Quantification Contradiction | None | None | None | None |
| Lexical Contradiction | None | None | None | None |
| Temporal Contradiction | None | None | None | None |
| Pragmatic Contradiction | None | None | None | None |
---

> **Score**: Measuring the confidence in detected Contradiction Type. 
- The high score is an indicator that LLM can make the final call. 
- The low score is an indicator that a human in the loop should approve the process. 
- The medium score is an indicator that more context or reasoning is needed to improve the decision making process. 
- The range for each decision should be tuned based on the importance of the decision in a specific domain. 
- If the score is `None`, it means that we did not detect the specific type of contradictions. 