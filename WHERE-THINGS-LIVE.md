# Where things live (Paul, 25 Nov 2026 - same file in every Claude project)

| Work | Claude project | GitHub repo | Live at |
|---|---|---|---|
| AI Office Flow system (CTI master copy + Keena demo) | Service Graph Ai | Polishedtrader/ai-office-flow | officeflow.measureflow.com.au |
| MeasureFlow Ecosystem website (the only marketing site) | Measureflow Ecosystem | Polishedtrader/measureflow-ecosystem-site | ecosystem.measureflow.com.au |
| AI Office Flow marketing (email campaign, leads, agents) | AI Office Flow - Marketing | Polishedtrader/aof-marketing | (no site) |
| Northern Beaches Kitchens system | its own project | its own repo | officeflow.nbkitchens.com.au |

## Rules for Claude
1. Check which project this chat is in. Only change the repo that belongs to this project (see the map).
2. If the request needs another project's code, do not change it. Write a short brief Paul can paste into that project's chat.
3. If the work doesn't match this project at all, say "this looks like the wrong chat for <work>" and wait for Paul's yes.
4. Never add another project's repo to this chat.
5. Start of each chat: git pull first, and tell Paul in one line if another chat pushed changes.

## Rules for Paul
- Open the project that matches the work before you start a chat.
- New business = new Claude project + new repo + new row in this table (update this file in every project).

## For the marketing team
- Work only in Polishedtrader/aof-marketing. Never attach ai-office-flow or measureflow-ecosystem-site.
- What the product and sites say is captured in strategy/product-knowledge.md, strategy/business-facts.md and
  strategy/business-review-*.md. Changes needed elsewhere go as briefs in strategy/briefs/ for Paul to paste
  into "Service Graph Ai" (officeflow) or "Measureflow Ecosystem" (ecosystem site).
