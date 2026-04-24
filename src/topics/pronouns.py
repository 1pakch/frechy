"""Pronoun topic definitions."""

from .base import TopicConfig
from . import TopicRegistry
from ..models import PracticeMode


PRONOUN_TOPICS = [
    # Level 1: Single Pronouns (Present Tense)
    TopicConfig(
        category="pronouns",
        key="direct-object",
        name="Direct Object Pronouns",
        description="Practice using le, la, les in present tense",
        grammar_focus=[
            "direct object pronouns (le, la, les)",
            "present tense",
            "placement before conjugated verb",
            "contraction to l' before vowels",
        ],
        prompt_hints=(
            "Direct object pronouns (le, la, les) replace direct objects and are "
            "placed directly before the conjugated verb. Example: 'Je vois Pierre' "
            "becomes 'Je le vois'. Remember that le/la contract to l' before vowels."
        ),
        supported_modes=[PracticeMode.TRANSLATION, PracticeMode.WORD_ORDER],
    ),
    TopicConfig(
        category="pronouns",
        key="indirect-object",
        name="Indirect Object Pronouns",
        description="Practice using lui, leur in present tense",
        grammar_focus=[
            "indirect object pronouns (lui, leur)",
            "present tense",
            "placement before conjugated verb",
        ],
        prompt_hints=(
            "Indirect object pronouns (lui, leur) replace indirect objects "
            "(à + person) and are placed directly before the conjugated verb. "
            "Example: 'Je parle à Marie' becomes 'Je lui parle'."
        ),
        supported_modes=[PracticeMode.TRANSLATION, PracticeMode.WORD_ORDER],
    ),
    TopicConfig(
        category="pronouns",
        key="reflexive",
        name="Reflexive Pronouns",
        description="Practice using me, te, se, nous, vous in present tense",
        grammar_focus=[
            "reflexive pronouns (me, te, se, nous, vous)",
            "present tense",
            "placement before conjugated verb",
        ],
        prompt_hints=(
            "Reflexive pronouns indicate that the subject performs an action on itself. "
            "They are placed directly before the conjugated verb. "
            "Example: 'Je me lave' (I wash myself)."
        ),
        supported_modes=[PracticeMode.TRANSLATION, PracticeMode.WORD_ORDER],
    ),
    # Level 2: Negations (Present Tense)
    TopicConfig(
        category="pronouns",
        key="negation-direct",
        name="Negation with Direct Object Pronouns",
        description="Practice ne...pas with direct pronouns in present tense",
        grammar_focus=[
            "direct object pronouns (le, la, les)",
            "negation (ne...pas)",
            "present tense",
            "word order: ne + pronoun + verb + pas",
        ],
        prompt_hints=(
            "In negations, the structure is: ne + pronoun + verb + pas. "
            "Example: 'Je ne le vois pas' (I don't see him). The pronoun stays "
            "between 'ne' and the verb."
        ),
        supported_modes=[PracticeMode.TRANSLATION, PracticeMode.WORD_ORDER],
    ),
    TopicConfig(
        category="pronouns",
        key="negation-indirect",
        name="Negation with Indirect Object Pronouns",
        description="Practice ne...pas with indirect pronouns in present tense",
        grammar_focus=[
            "indirect object pronouns (lui, leur)",
            "negation (ne...pas)",
            "present tense",
            "word order: ne + pronoun + verb + pas",
        ],
        prompt_hints=(
            "In negations, the structure is: ne + pronoun + verb + pas. "
            "Example: 'Je ne lui parle pas' (I don't speak to him). The pronoun "
            "stays between 'ne' and the verb."
        ),
        supported_modes=[PracticeMode.TRANSLATION, PracticeMode.WORD_ORDER],
    ),
    TopicConfig(
        category="pronouns",
        key="negation-reflexive",
        name="Negation with Reflexive Pronouns",
        description="Practice ne...pas with reflexive pronouns in present tense",
        grammar_focus=[
            "reflexive pronouns (me, te, se, nous, vous)",
            "negation (ne...pas)",
            "present tense",
            "word order: ne + pronoun + verb + pas",
        ],
        prompt_hints=(
            "In negations, the structure is: ne + pronoun + verb + pas. "
            "Example: 'Je ne me lave pas' (I don't wash myself). The reflexive "
            "pronoun stays between 'ne' and the verb."
        ),
        supported_modes=[PracticeMode.TRANSLATION, PracticeMode.WORD_ORDER],
    ),
    # Level 3: Compound Tenses (Passé Composé)
    TopicConfig(
        category="pronouns",
        key="direct-passe-compose",
        name="Direct Object Pronouns with Passé Composé",
        description="Practice le/la/les with passé composé",
        grammar_focus=[
            "direct object pronouns (le, la, les)",
            "passé composé",
            "placement before auxiliary verb",
            "past participle agreement",
        ],
        prompt_hints=(
            "In passé composé, pronouns come before the auxiliary verb (avoir/être). "
            "Example: 'Je l'ai vu' (I saw him). Note: Past participle may agree "
            "with the direct object pronoun."
        ),
        supported_modes=[PracticeMode.TRANSLATION, PracticeMode.WORD_ORDER],
    ),
    TopicConfig(
        category="pronouns",
        key="indirect-passe-compose",
        name="Indirect Object Pronouns with Passé Composé",
        description="Practice lui/leur with passé composé",
        grammar_focus=[
            "indirect object pronouns (lui, leur)",
            "passé composé",
            "placement before auxiliary verb",
        ],
        prompt_hints=(
            "In passé composé, pronouns come before the auxiliary verb. "
            "Example: 'Je lui ai parlé' (I spoke to him). The pronoun goes before "
            "'ai', not after 'parlé'."
        ),
        supported_modes=[PracticeMode.TRANSLATION, PracticeMode.WORD_ORDER],
    ),
    TopicConfig(
        category="pronouns",
        key="reflexive-passe-compose",
        name="Reflexive Pronouns with Passé Composé",
        description="Practice reflexive pronouns with passé composé",
        grammar_focus=[
            "reflexive pronouns (me, te, se, nous, vous)",
            "passé composé",
            "use of être as auxiliary",
            "past participle agreement",
        ],
        prompt_hints=(
            "Reflexive verbs use être in passé composé. The reflexive pronoun goes "
            "before être. Example: 'Je me suis lavé' (I washed myself). "
            "Past participle agrees with the subject."
        ),
        supported_modes=[PracticeMode.TRANSLATION, PracticeMode.WORD_ORDER],
    ),
    # Level 4: Negations + Compound Tenses
    TopicConfig(
        category="pronouns",
        key="negation-passe-compose",
        name="Negation with Passé Composé",
        description="Practice ne...pas with passé composé and pronouns",
        grammar_focus=[
            "object pronouns",
            "passé composé",
            "negation (ne...pas)",
            "word order: ne + pronoun + auxiliary + pas + participle",
        ],
        prompt_hints=(
            "In negations with passé composé: ne + pronoun + auxiliary + pas + participle. "
            "Example: 'Je ne l'ai pas vu' (I didn't see him). The 'ne...pas' wraps "
            "around pronoun + auxiliary."
        ),
        supported_modes=[PracticeMode.TRANSLATION, PracticeMode.WORD_ORDER],
    ),
    # Level 5: Advanced Combinations
    TopicConfig(
        category="pronouns",
        key="double",
        name="Double Object Pronouns",
        description="Practice combining COD + COI pronouns",
        grammar_focus=[
            "double object pronouns",
            "word order: COI before COD or vice versa",
            "present tense",
            "proper sequencing (me/te/se/nous/vous before le/la/les before lui/leur)",
        ],
        prompt_hints=(
            "When combining pronouns, follow the order: me/te/se/nous/vous, then "
            "le/la/les, then lui/leur. Example: 'Je le lui donne' (I give it to him). "
            "Both pronouns go before the verb."
        ),
        supported_modes=[PracticeMode.TRANSLATION, PracticeMode.WORD_ORDER],
    ),
    TopicConfig(
        category="pronouns",
        key="double-passe-compose",
        name="Double Object Pronouns with Passé Composé",
        description="Practice combining COD + COI pronouns with passé composé",
        grammar_focus=[
            "double object pronouns",
            "passé composé",
            "word order before auxiliary verb",
            "past participle agreement",
        ],
        prompt_hints=(
            "In passé composé with double pronouns, both go before the auxiliary "
            "in the same order. Example: 'Je le lui ai donné' (I gave it to him). "
            "Past participle may agree with preceding direct object."
        ),
        supported_modes=[PracticeMode.TRANSLATION, PracticeMode.WORD_ORDER],
    ),
    # Level 6: Advanced Combinations with Negations
    TopicConfig(
        category="pronouns",
        key="double-negation",
        name="Double Object Pronouns with Negation",
        description="Practice COD + COI with ne...pas in present tense",
        grammar_focus=[
            "double object pronouns",
            "negation (ne...pas)",
            "present tense",
            "word order: ne + pronouns + verb + pas",
        ],
        prompt_hints=(
            "With negation and double pronouns: ne + both pronouns + verb + pas. "
            "Example: 'Je ne le lui donne pas' (I don't give it to him). "
            "Both pronouns stay between 'ne' and the verb."
        ),
        supported_modes=[PracticeMode.TRANSLATION, PracticeMode.WORD_ORDER],
    ),
    TopicConfig(
        category="pronouns",
        key="double-negation-passe-compose",
        name="Double Object Pronouns with Negation and Passé Composé",
        description="Practice COD + COI with ne...pas and passé composé",
        grammar_focus=[
            "double object pronouns",
            "passé composé",
            "negation (ne...pas)",
            "word order: ne + pronouns + auxiliary + pas + participle",
        ],
        prompt_hints=(
            "Combining everything: ne + both pronouns + auxiliary + pas + participle. "
            "Example: 'Je ne le lui ai pas donné' (I didn't give it to him). "
            "This is the most complex pronoun structure."
        ),
        supported_modes=[PracticeMode.TRANSLATION, PracticeMode.WORD_ORDER],
    ),
]


# Register all topics on module import
for topic in PRONOUN_TOPICS:
    TopicRegistry.register(topic)
