# Frechy

A minimal LLM-based app to practice word order with French pronouns. Examples of rules being trained:

- "Je lui ai parlé" (correct) vs "J'ai lui parlé" (wrong) — indirect object pronoun, passé composé
- "Je le lui donne" (correct) vs "Je lui le donne" (wrong) — double pronouns (direct + indirect)
- "Je le lui ai donné" (correct) vs "J'ai le lui donné" (wrong) — double pronouns, passé composé
- "Je ne le lui ai pas donné" (correct) vs "Je l'ai ne pas lui donné" (wrong) — double pronouns, passé composé with negation

Developed with Claude using spec-driven approach. I typed the initial [idea](specs/idea-v1) and then asked it to develop it into a [spec](specs/spec-v1) providing [feedback](specs/spec-v1-feedback-1) (Claude's [response](specs/spec-v1-feedback-1-response)) until the spec was to my liking. After I asked Claude Code with Sonnet 4.6 to develop the app and tested it providing test feedback ([1](specs/test-v1-comments-1), [2](specs/test-v1-comments-2)) which prompted further code changes. Overall, it worked quite terms of functionality if some of the intermediate results were quite disappointing. The code quality was rather poor including obvious `import` hacks that should have been announced and addressed in a structured manner.

## Setup

1. Enter dev environment:
   ```bash
   nix develop
   ```

2. Create `.env` file:
   ```bash
   OPENROUTER_API_KEY=your_key_here
   ```

3. List available topics:
   ```bash
   python -m src.main --list-topics
   ```

4. Start practicing:
   ```bash
   python -m src.main -t pronouns.direct-object -m translation
   ```

## Practice Modes

- `translation`: Translate English to French
- `word-order`: Arrange numbered French words correctly

## During Practice

- Type your answer and press Enter
- If incorrect:
  - `R`: Retry
  - `H`: Get a hint
  - `S`: Show answer
  - `Q`: Quit session
- Press Ctrl+C anytime to end and see stats
