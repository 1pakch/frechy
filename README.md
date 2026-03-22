# Frechy

French grammar practice CLI with LLM-generated exercises.

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
   python src/main.py --list-topics
   ```

4. Start practicing:
   ```bash
   python src/main.py -t pronouns.direct-object -m translation
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
