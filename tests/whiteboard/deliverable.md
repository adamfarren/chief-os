# Whiteboard Test Results

## Test 1: Flowchart with Brand Colors

**Prompt:** "Draw a flowchart showing how a customer gets onboarded to the ledger: they start at the signup form, go through data source verification (which can fail or pass), then schedule an implementation call, and finally receive a confirmation."

**Style guide read:** `chief-style/SKILL.md` — extracted Meridian Ledger brand tokens (example palette from the template):
- primary: `#4F8EF7`, secondary: `#7FB7FF`
- base02: `#14171F`, base03: `#1E222C`
- accent info: `#4FD1E7`, success green: `#5DD39E`, warning orange: `#F5A04B`
- textBody: `#E6EAF2`

**Diagram type selected:** `flowchart LR` — correct for a linear process with a decision branch.

**Mermaid syntax generated:**

```
flowchart LR
  classDef primary fill:#4F8EF7,stroke:#7FB7FF,color:#FFFFFF
  classDef node fill:#14171F,stroke:#4F8EF7,color:#E6EAF2
  classDef decision fill:#1E222C,stroke:#4FD1E7,color:#4FD1E7
  classDef success fill:#14171F,stroke:#5DD39E,color:#5DD39E
  classDef warn fill:#14171F,stroke:#F5A04B,color:#F5A04B

  A["Signup Form"]:::primary --> B{"Data Source Verification"}:::decision
  B -->|"Pass"| C["Schedule Implementation"]:::node
  B -->|"Fail"| D["Notify Customer"]:::warn
  C --> E["Confirmation Sent"]:::success
```

**Color assignment:**
- `Signup Form` → `primary` (entry point, hero node)
- `Data Source Verification` → `decision` (fork with two exits)
- `Schedule Implementation` → `node` (standard process step)
- `Notify Customer` → `warn` (failure/attention path, orange stroke)
- `Confirmation Sent` → `success` (positive terminal, green stroke)

**FigJam URL:** https://www.figma.com/online-whiteboard/create-diagram/00c5d9c3-65c6-46d1-af34-54685f3ab0f8?utm_source=other&utm_content=edit_in_figjam

---

## Test 2: Sequence Diagram (No Color)

**Prompt:** "Draw a sequence diagram for API authentication — client logs in, gets a JWT, then makes an authenticated request."

**Style guide read:** `chief-style/SKILL.md` — brand colors extracted but not applied (sequence diagrams don't support color styling).

**Diagram type selected:** `sequenceDiagram` — correct for time-ordered system interactions.

**Mermaid syntax generated:**

```
sequenceDiagram
  participant Client
  participant API
  participant Auth
  participant DB

  Client->>API: POST /login
  API->>Auth: Validate credentials
  Auth->>DB: Lookup user
  DB-->>Auth: User record
  Auth-->>API: Token issued
  API-->>Client: 200 OK + JWT
  Client->>API: GET /resource (Bearer token)
  API->>Auth: Verify token
  Auth-->>API: Valid
  API-->>Client: 200 OK + data
```

**FigJam URL:** https://www.figma.com/online-whiteboard/create-diagram/f5bb10ee-c67c-48a9-bcf9-158359fdf036?utm_source=other&utm_content=edit_in_figjam
