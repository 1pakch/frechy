"""Pronoun-specific prompt templates for LLM interactions."""

from ..topics.base import TopicConfig


def generate_exercise_prompt(topic_config: TopicConfig) -> str:
    """Generate prompt for creating a new exercise.

    Args:
        topic_config: Configuration for the current topic

    Returns:
        Formatted prompt string for LLM
    """
    return f"""You are a French language teacher creating exercises for intermediate learners.

Topic: {topic_config.name}
Grammar Focus: {', '.join(topic_config.grammar_focus)}

{topic_config.prompt_hints}

Generate ONE exercise that tests this specific grammar point.

Requirements:
- Natural, conversational sentence (like something you'd say to a friend)
- Clear usage of the target grammar concept
- Appropriate vocabulary for intermediate learners
- Avoid overly complex vocabulary or idioms
- Keep sentences concise (under 15 words)

Return ONLY valid JSON with this exact structure:
{{
  "english": "English sentence here",
  "correct_french": "Correct French sentence with proper grammar"
}}

Do not include any explanations or additional text, just the JSON."""


def validate_answer_prompt(topic_config: TopicConfig, correct: str, user: str) -> str:
    """Generate prompt for validating a user's answer.

    Args:
        topic_config: Configuration for the current topic
        correct: The correct answer
        user: The user's answer

    Returns:
        Formatted prompt string for LLM validation
    """
    return f"""You are evaluating a French learner's answer for grammar accuracy.

Topic: {topic_config.name}
Grammar Focus: {', '.join(topic_config.grammar_focus)}

Correct answer: {correct}
User's answer: {user}

Evaluate the grammar and word order, especially focusing on the target grammar point.

Be LENIENT with:
- Minor spelling errors (e.g., "vois" vs "voit")
- Missing or incorrect accent marks (é vs e, à vs a, etc.)
- Capitalization
- Extra spaces or punctuation

Be STRICT with:
- Word order (especially pronoun placement)
- Missing or extra words
- Wrong pronouns or verb forms

Return ONLY valid JSON:
{{
  "is_correct": true,
  "feedback": "Brief explanation if incorrect (max 50 words)"
}}

If correct, set feedback to empty string ""."""


def generate_hint_prompt(topic_config: TopicConfig, english: str, correct: str, user: str) -> str:
    """Generate prompt for creating a helpful hint.

    Args:
        topic_config: Configuration for the current topic
        english: The English sentence to translate
        correct: The correct French answer
        user: The user's incorrect attempt

    Returns:
        Formatted prompt string for LLM hint generation
    """
    return f"""A French learner is struggling with this exercise.

Topic: {topic_config.name}
English: {english}
Correct French: {correct}
User's attempt: {user}

Provide a helpful, encouraging hint about the grammar without giving away the full answer.

DO:
- Be specific about the grammar rule (e.g., "In compound tenses, pronouns come before the auxiliary verb")
- Point to the specific mistake (e.g., "Check the position of 'le' relative to the verb")
- Be encouraging and supportive
- Keep it brief (2-3 sentences maximum)

DO NOT:
- Give away the complete answer
- Use discouraging language
- Use technical linguistic jargon
- Explain unrelated grammar

Return only the hint text, no JSON or additional formatting."""
