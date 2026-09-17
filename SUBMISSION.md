# Submission kit

## LinkedIn post: short

I built Veridian Service Agent, an internal IT desk agent designed around the decisions it should refuse. It spots the laptop-policy conflict in REQ-01, stops active phishing forwarding in REQ-08, and says no when REQ-10 asks for server access outside policy. The implementation runs offline with deterministic rules and an audit trail. [Repository link]. It refuses to invent authority, approvals, or policies.

## LinkedIn post: medium

I built Veridian Service Agent to test a simple question: can an IT agent show good judgment when the answer is not obvious? The project retrieves from a fixed policy set, then uses a deterministic policy engine before any optional language model can write a reply.

Three cases shaped the design. A laptop at 3.5 years sits between conflicting refresh policies, so the agent surfaces both and routes it. A phishing email being forwarded gets an immediate containment instruction. A request for finance-server admin access has no supporting policy, so the agent asks for human review instead of reasoning by analogy.

The no-key evaluation gets 19/19 expected decisions and records each trace in JSONL. [Repository link]. It refuses to invent authority, approvals, or policies.

## LinkedIn post: technical

Veridian Service Agent is a small FastAPI project that treats a language model as an optional editor, not the decision maker. Local BM25 retrieval produces cited evidence. A deterministic engine applies policy rules. Guardrails reject uncited decisions, detect policy conflicts, enforce authority boundaries, and downgrade low confidence. SQLite and JSONL preserve each input, retrieval set, trace, and final verdict.

The offline rule engine reproduces 19 golden decisions. The UI makes the hard cases inspectable: conflict diff, phishing containment banner, and no-coverage state. [Repository link]. It refuses to invent authority, approvals, or policies.

Hashtags: #AIEngineering #FastAPI #ResponsibleAI #AgenticAI #ITOperations #LLMOps #Python #ProductDesign

## Demo video script

| Time | Say | Click |
| --- | --- | --- |
| 0:00 | “IT agents earn trust by knowing when not to act.” | Open the console |
| 0:40 | “Policy retrieval feeds a deterministic decision engine and hard guards.” | Open architecture diagram |
| 1:20 | “I will process the fixed queue in offline mode.” | Click Run all cases |
| 2:10 | “REQ-01 shows the 3-year and 4-year conflict. The agent exposes both and routes.” | Select REQ-01 |
| 3:10 | “REQ-08 is more urgent: forwarding phishing is actively unsafe.” | Select REQ-08, show checklist |
| 4:00 | “REQ-10 has no policy coverage. Urgency does not create authority.” | Select REQ-10 |
| 4:45 | “The deterministic evaluator scores all 19 expected decisions.” | Show eval report |
| 5:20 | “This demo does not take production actions. Integrations and policy versioning come next.” | Show architecture and close |

## Submission checklist

- [ ] GitHub repository public and README rendered
- [ ] Six-minute screen capture uploaded to Drive
- [ ] Verify the Drive link in an incognito browser
- [ ] Paste repository, deck, video, and LinkedIn links into the form

## Repo setup

```bash
git init
git add .
git commit -m "Build Veridian Service Agent"
git branch -M main
git remote add origin https://github.com/your-account/veridian-service-agent.git
git push -u origin main
```

Replace `your-account` in the remote command with the GitHub account that owns the repository. Description: `Policy-grounded internal IT service desk agent with deterministic guardrails.`

Topics: `fastapi`, `python`, `responsible-ai`, `agentic-ai`, `llmops`, `it-operations`
