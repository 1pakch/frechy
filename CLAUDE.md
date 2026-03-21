# Instructions for Claude

## Commit Message Style

**First line (summary):**
- lowercase
- concise (ideally <50 chars, not a hard limit)
- Mark AI involvement:
  - **(ai)** - straightforward AI work, reproducible
  - **(ai+h)** - AI work after deliberations/discussions with human, less reproducible due to user decisions

**Body:**
- Focus on substance, not numbers (e.g., "modular architecture" not "8 phases")
- Be concise
- AI-assisted commits always end with:
  ```
  Co-Authored-By: Claude <noreply@anthropic.com>
  ```

**Examples:**

User commit (no AI):
```
initial project idea for french pronoun trainer
```

Straightforward AI work (reproducible):
```
implement database schema (ai)

- sessions, exercises, attempts tables
- SQLite with proper foreign keys

Co-Authored-By: Claude <noreply@anthropic.com>
```

AI work with human deliberations (less reproducible):
```
add technical specification after deliberations (ai+h)

- Detailed architecture and database schema
- Implementation plan with 8 phases
- All 12 pronoun topics defined
- Decisions on PracticeMode enum, topic structure, supported modes

Co-Authored-By: Claude <noreply@anthropic.com>
```
