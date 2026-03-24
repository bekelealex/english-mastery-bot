# -*- coding: utf-8 -*-
"""
PREMIUM ENGLISH MASTERY TELEGRAM BOT
PRODUCTION READY - ULTRA FAST - NO LAG - NO FREEZE
100 Advanced English Questions with Auto-Clearing Explanations
"""

import logging
import os
import sys
import asyncio
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode
from asyncio import Lock

# ==================== CONFIGURATION ====================

BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    print("❌ BOT_TOKEN not found!")
    sys.exit(1)

# Setup minimal logging for speed
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING,
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ==================== COMPLETE 100 QUESTIONS DATABASE ====================

questions = [
    # ==================== SECTION 1: READING PASSAGE COMPLETION (1-15) ====================
    {
        "question": "Read the passage and choose the correct verb form:\n\n'The ancient manuscript, which ______ in a monastery for centuries, was finally discovered in 2019.'",
        "options": ["A) had been hidden", "B) was hidden", "C) has been hidden", "D) is hidden"],
        "answer": "A",
        "explanation": "Past Perfect Passive 'had been hidden' - the hiding occurred before discovery."
    },
    {
        "question": "Passage completion:\n\n'By the time the rescue team arrived, the survivors ______ for over 48 hours.'",
        "options": ["A) waited", "B) have been waiting", "C) had been waiting", "D) were waiting"],
        "answer": "C",
        "explanation": "Past Perfect Continuous 'had been waiting' - duration before another past action."
    },
    {
        "question": "Passage completion:\n\n'Currently, the new bridge ______, and it's expected to open next spring.'",
        "options": ["A) is constructing", "B) is being constructed", "C) has constructed", "D) was constructed"],
        "answer": "B",
        "explanation": "Present Continuous Passive 'is being constructed' - ongoing action in present."
    },
    {
        "question": "Passage completion:\n\n'By 2030, scientists predict that renewable energy ______ fossil fuels as the primary power source.'",
        "options": ["A) will replace", "B) will have replaced", "C) replaces", "D) is replacing"],
        "answer": "B",
        "explanation": "Future Perfect 'will have replaced' - action completed by specific future time."
    },
    {
        "question": "Passage completion:\n\n'After the CEO ______ the company for 20 years, he announced his retirement.'",
        "options": ["A) led", "B) was leading", "C) had been leading", "D) has led"],
        "answer": "C",
        "explanation": "Past Perfect Continuous 'had been leading' - duration before announcement."
    },
    {
        "question": "Passage completion:\n\n'Climate change, which ______ a global crisis for decades, requires immediate action.'",
        "options": ["A) was", "B) had been", "C) has been", "D) is"],
        "answer": "C",
        "explanation": "Present Perfect 'has been' - connects past situation to present reality."
    },
    {
        "question": "Passage completion:\n\n'By the time you read this, the spacecraft ______ on Mars for three days.'",
        "options": ["A) will land", "B) will have landed", "C) will have been landing", "D) lands"],
        "answer": "C",
        "explanation": "Future Perfect Continuous 'will have been landing' - duration up to future point."
    },
    {
        "question": "Passage completion:\n\n'The artifacts, which ______ in the tomb since 3000 BCE, provided invaluable historical insights.'",
        "options": ["A) were buried", "B) had been buried", "C) have been buried", "D) are buried"],
        "answer": "B",
        "explanation": "Past Perfect Passive 'had been buried' - state before discovery."
    },
    {
        "question": "Passage completion:\n\n'As we speak, negotiations ______ between the two countries to resolve the conflict.'",
        "options": ["A) hold", "B) are held", "C) are being held", "D) have held"],
        "answer": "C",
        "explanation": "Present Continuous Passive 'are being held' - ongoing action at the moment."
    },
    {
        "question": "Passage completion:\n\n'The professor, along with her research team, ______ on this project since 2015.'",
        "options": ["A) work", "B) has been working", "C) have been working", "D) worked"],
        "answer": "B",
        "explanation": "Present Perfect Continuous 'has been working' - duration from past to present."
    },
    {
        "question": "Passage completion:\n\n'Before the internet revolutionized communication, information ______ primarily through print media.'",
        "options": ["A) was disseminated", "B) is disseminated", "C) has been disseminated", "D) disseminates"],
        "answer": "A",
        "explanation": "Past Simple Passive 'was disseminated' - completed past state."
    },
    {
        "question": "Passage completion:\n\n'The suspect ______ to have fled the country before the warrant was issued.'",
        "options": ["A) believes", "B) is believed", "C) believed", "D) has believed"],
        "answer": "B",
        "explanation": "Impersonal passive 'is believed' with reporting verb."
    },
    {
        "question": "Passage completion:\n\n'By next December, I ______ as a software engineer for a decade.'",
        "options": ["A) will work", "B) will have been working", "C) work", "D) am working"],
        "answer": "B",
        "explanation": "Future Perfect Continuous 'will have been working' - duration up to future point."
    },
    {
        "question": "Passage completion:\n\n'The documentary, which ______ by millions worldwide, won multiple awards.'",
        "options": ["A) has been viewed", "B) had been viewed", "C) was viewed", "D) is viewed"],
        "answer": "A",
        "explanation": "Present Perfect Passive 'has been viewed' - past viewing connects to present recognition."
    },
    {
        "question": "Passage completion:\n\n'During the summit, it ______ that the trade agreement would be signed by year-end.'",
        "options": ["A) announced", "B) was announced", "C) has announced", "D) is announcing"],
        "answer": "B",
        "explanation": "Past Simple Passive 'was announced' - reported event in past."
    },

    # ==================== SECTION 2: MODAL AUXILIARIES IN CONVERSATIONS (16-25) ====================
    {
        "question": "Conversation:\n\nA: 'Someone's at the door. Who ______ it be at this hour?'\nB: 'I'm not sure. It ______ be the delivery person.'",
        "options": ["A) can / might", "B) must / should", "C) will / can", "D) shall / would"],
        "answer": "A",
        "explanation": "'Can' expresses possibility in questions; 'might' expresses possibility in statements."
    },
    {
        "question": "Conversation:\n\nA: 'I'm exhausted. I ______ have stayed up so late.'\nB: 'You're right. You ______ have gone to bed earlier.'",
        "options": ["A) shouldn't / should", "B) mustn't / must", "C) couldn't / could", "D) wouldn't / would"],
        "answer": "A",
        "explanation": "'Shouldn't have' expresses regret; 'should have' gives advice about better past choice."
    },
    {
        "question": "Conversation:\n\nA: 'Look at that car! It ______ have cost a fortune.'\nB: 'Definitely. Only a millionaire ______ afford that.'",
        "options": ["A) can / must", "B) must / could", "C) might / should", "D) would / may"],
        "answer": "B",
        "explanation": "'Must have' for strong deduction about the past; 'could' for possibility in hypotheticals."
    },
    {
        "question": "Conversation:\n\nA: 'You ______ have told me you were coming! I would have prepared dinner.'\nB: 'I'm sorry. I ______ have let you know, but it was a last-minute decision.'",
        "options": ["A) should / should", "B) must / must", "C) could / could", "D) might / might"],
        "answer": "A",
        "explanation": "'Should have' expresses criticism/regret about a past action in both sentences."
    },
    {
        "question": "Conversation:\n\nA: 'The museum ______ be closed today. It's a national holiday.'\nB: 'Actually, I think it ______ be open. I saw people inside.'",
        "options": ["A) must / might", "B) can / should", "C) might / must", "D) should / can"],
        "answer": "C",
        "explanation": "'Might' expresses possibility; 'must' expresses strong deduction based on evidence."
    },
    {
        "question": "Conversation:\n\nA: 'You ______ have seen the look on his face when I told him!'\nB: 'I wish I ______ have been there. It sounds hilarious.'",
        "options": ["A) should / should", "B) must / could", "C) could / would", "D) might / might"],
        "answer": "B",
        "explanation": "'Must have' expresses strong deduction; 'could have' expresses unrealized past possibility."
    },
    {
        "question": "Conversation:\n\nA: 'I'm not feeling well. I ______ have eaten that seafood.'\nB: 'You're right. You ______ avoid street food in the future.'",
        "options": ["A) shouldn't / should", "B) mustn't / must", "C) couldn't / could", "D) wouldn't / would"],
        "answer": "A",
        "explanation": "'Shouldn't have' expresses regret; 'should' gives future advice."
    },
    {
        "question": "Conversation:\n\nA: 'You ______ borrow my car if you need it.'\nB: 'Really? You ______ be so generous!'",
        "options": ["A) can / must", "B) may / might", "C) will / would", "D) could / should"],
        "answer": "A",
        "explanation": "'Can' offers permission; 'must' expresses strong appreciation/surprise."
    },
    {
        "question": "Conversation:\n\nA: 'The instructions say we ______ not open the package until Christmas.'\nB: 'We ______ better follow the rules then.'",
        "options": ["A) must / had", "B) should / would", "C) can / might", "D) may / could"],
        "answer": "A",
        "explanation": "'Must not' expresses prohibition; 'had better' gives strong advice with implied consequence."
    },
    {
        "question": "Conversation:\n\nA: 'You ______ be tired after that long flight.'\nB: 'I am. I ______ really use some sleep.'",
        "options": ["A) can / could", "B) must / could", "C) might / should", "D) would / may"],
        "answer": "B",
        "explanation": "'Must' for logical deduction; 'could' for polite expression of need."
    },

    # ==================== SECTION 3: ALL CONDITIONALS WITH MEANING (26-40) ====================
    {
        "question": "Zero Conditional (General Truth):\n\n'If you ______ water to 100°C, it ______.'",
        "options": ["A) heat / boils", "B) will heat / boils", "C) heat / will boil", "D) heated / boiled"],
        "answer": "A",
        "explanation": "Zero Conditional: If + Present Simple, Present Simple (scientific facts)."
    },
    {
        "question": "First Conditional (Real Future):\n\n'If she ______ the exam, she ______ medical school next year.'",
        "options": ["A) passes / will enter", "B) will pass / enters", "C) passed / would enter", "D) had passed / would have entered"],
        "answer": "A",
        "explanation": "First Conditional: If + Present Simple, will + infinitive (real possibility)."
    },
    {
        "question": "Second Conditional (Unreal Present):\n\n'If I ______ you, I ______ that job offer immediately.'",
        "options": ["A) am / will accept", "B) were / would accept", "C) had been / would have accepted", "D) was / accept"],
        "answer": "B",
        "explanation": "Second Conditional: If + Past Simple, would + infinitive (hypothetical present)."
    },
    {
        "question": "Third Conditional (Unreal Past):\n\n'If they ______ the warning, the accident ______.'",
        "options": ["A) heeded / wouldn't happen", "B) had heeded / wouldn't have happened", "C) heeded / wouldn't have happened", "D) had heeded / didn't happen"],
        "answer": "B",
        "explanation": "Third Conditional: If + Past Perfect, would have + past participle (impossible past)."
    },
    {
        "question": "Mixed Conditional (Past Condition → Present Result):\n\n'If she ______ harder in college, she ______ a better job now.'",
        "options": ["A) studied / would have", "B) had studied / would have", "C) had studied / would be", "D) studied / would be"],
        "answer": "C",
        "explanation": "Mixed Conditional: Past condition affects present result."
    },
    {
        "question": "Mixed Conditional (Present Condition → Past Result):\n\n'If I ______ more confident, I ______ for that promotion last year.'",
        "options": ["A) am / would apply", "B) were / would have applied", "C) had been / would apply", "D) was / would apply"],
        "answer": "B",
        "explanation": "Mixed Conditional: Present state would have changed past outcome."
    },
    {
        "question": "Inverted Conditional (Formal - Third):\n\n'______ earlier, the disaster could have been prevented.'",
        "options": ["A) Had they evacuated", "B) If they evacuated", "C) Were they to evacuate", "D) They evacuated"],
        "answer": "A",
        "explanation": "Inverted Third Conditional: 'Had + subject + past participle' = 'If + subject + had + past participle'."
    },
    {
        "question": "Inverted Conditional (Formal - Second):\n\n'______ to win the lottery, what would you do?'",
        "options": ["A) Had you", "B) Were you", "C) If you", "D) Should you"],
        "answer": "B",
        "explanation": "Inverted Second Conditional: 'Were + subject + to + infinitive' for hypotheticals."
    },
    {
        "question": "Conditional with 'unless' (Negative Condition):\n\n'The project will succeed ______ everyone contributes fully.'",
        "options": ["A) unless", "B) if", "C) provided that", "D) only if"],
        "answer": "A",
        "explanation": "'Unless' means 'if not'."
    },
    {
        "question": "Conditional with 'provided that' (Stipulation):\n\n'You can borrow the car ______ you return it by 10 PM.'",
        "options": ["A) unless", "B) even if", "C) provided that", "D) as long as"],
        "answer": "C",
        "explanation": "'Provided that' introduces a necessary condition."
    },
    {
        "question": "Complex Conditional with 'but for':\n\n'______ your support, I would have given up long ago.'",
        "options": ["A) Without", "B) But for", "C) Except for", "D) Aside from"],
        "answer": "B",
        "explanation": "'But for' means 'if it were not for' or 'without'."
    },
    {
        "question": "Conditional with 'even if' (Concession):\n\n'I wouldn't marry him ______ he were the last man on Earth.'",
        "options": ["A) even if", "B) only if", "C) unless", "D) provided that"],
        "answer": "A",
        "explanation": "'Even if' introduces condition that doesn't change outcome."
    },
    {
        "question": "Complex Conditional with 'supposing':\n\n'______ you inherited a million dollars, how would you spend it?'",
        "options": ["A) Unless", "B) Supposing", "C) Provided", "D) Even if"],
        "answer": "B",
        "explanation": "'Supposing' introduces a hypothetical scenario."
    },
    {
        "question": "Complex Conditional with 'were it not for':\n\n'______ his quick thinking, the company would have collapsed.'",
        "options": ["A) Were it not for", "B) If it wasn't for", "C) Had it not been for", "D) But for"],
        "answer": "C",
        "explanation": "'Had it not been for' is third conditional for past events."
    },
    {
        "question": "Conditional with 'as long as' (Condition):\n\n'You'll succeed ______ you never give up.'",
        "options": ["A) unless", "B) as long as", "C) even if", "D) whereas"],
        "answer": "B",
        "explanation": "'As long as' introduces necessary condition for result."
    },

    # ==================== SECTION 4: REPORTED SPEECH (41-50) ====================
    {
        "question": "Reported Speech - Statement:\n\nDirect: 'I will finish the project by Friday,' she said.\nReported: She said that she ______ the project by Friday.",
        "options": ["A) will finish", "B) would finish", "C) finishes", "D) finished"],
        "answer": "B",
        "explanation": "'Will' changes to 'would' in reported speech."
    },
    {
        "question": "Reported Speech - Question:\n\nDirect: 'Where did you buy that jacket?' he asked.\nReported: He asked me where I ______ that jacket.",
        "options": ["A) bought", "B) had bought", "C) buy", "D) have bought"],
        "answer": "B",
        "explanation": "Past Simple changes to Past Perfect in reported questions."
    },
    {
        "question": "Reported Speech - Command:\n\nDirect: 'Don't touch the artifacts,' the curator said.\nReported: The curator warned us ______ the artifacts.",
        "options": ["A) not to touch", "B) to not touch", "C) don't touch", "D) didn't touch"],
        "answer": "A",
        "explanation": "Negative commands use 'not to + infinitive'."
    },
    {
        "question": "Reported Speech - Request:\n\nDirect: 'Could you help me with this?' she asked.\nReported: She asked me ______ help her with that.",
        "options": ["A) that I could", "B) if I could", "C) could I", "D) I could"],
        "answer": "B",
        "explanation": "Polite requests become 'asked if + subject + could'."
    },
    {
        "question": "Reported Speech - Time Change:\n\nDirect: 'I'll see you tomorrow,' he said.\nReported: He said he would see me ______.",
        "options": ["A) tomorrow", "B) the next day", "C) on tomorrow", "D) the following tomorrow"],
        "answer": "B",
        "explanation": "Time expressions shift: tomorrow → the next day."
    },
    {
        "question": "Reported Speech - Place Change:\n\nDirect: 'I'm staying here,' she said.\nReported: She said she was staying ______.",
        "options": ["A) there", "B) here", "C) at here", "D) in there"],
        "answer": "A",
        "explanation": "Place references shift: here → there."
    },
    {
        "question": "Reported Speech - Modal Change:\n\nDirect: 'You must finish this tonight,' he said.\nReported: He said I ______ finish that that night.",
        "options": ["A) must", "B) had to", "C) must have", "D) would"],
        "answer": "B",
        "explanation": "'Must' often changes to 'had to' for obligation."
    },
    {
        "question": "Reported Speech - Imperative:\n\nDirect: 'Please arrive on time,' the manager said.\nReported: The manager asked us ______ on time.",
        "options": ["A) arrive", "B) to arrive", "C) arriving", "D) that we arrive"],
        "answer": "B",
        "explanation": "Imperatives use 'ask/tell + object + to + infinitive'."
    },
    {
        "question": "Reported Speech - Universal Truth:\n\nDirect: 'The Earth orbits the Sun,' the teacher said.\nReported: The teacher said that the Earth ______ the Sun.",
        "options": ["A) orbited", "B) orbits", "C) had orbited", "D) was orbiting"],
        "answer": "B",
        "explanation": "Universal truths don't change tense."
    },
    {
        "question": "Reported Speech - Mixed Reporting:\n\nDirect: 'I was waiting when you called,' he explained.\nReported: He explained that he ______ when I ______.",
        "options": ["A) waited / called", "B) was waiting / had called", "C) had been waiting / called", "D) had been waiting / had called"],
        "answer": "D",
        "explanation": "Past Continuous → Past Perfect Continuous; Past Simple → Past Perfect."
    },

    # ==================== SECTION 5: ADVANCED VOCABULARY IN CONTEXT (51-65) ====================
    {
        "question": "Vocabulary in Context:\n\nThe CEO's ______ speech inspired the entire company to work toward the ambitious goals.",
        "options": ["A) lackluster", "B) mundane", "C) rousing", "D) tedious"],
        "answer": "C",
        "explanation": "'Rousing' means exciting, stirring, and inspiring."
    },
    {
        "question": "Vocabulary in Context:\n\nDespite their ______ differences, the two leaders managed to reach a historic agreement.",
        "options": ["A) trivial", "B) profound", "C) superficial", "D) negligible"],
        "answer": "B",
        "explanation": "'Profound' means deep, significant, and far-reaching."
    },
    {
        "question": "Vocabulary in Context:\n\nThe investigation was ______ by the sudden disappearance of key evidence.",
        "options": ["A) facilitated", "B) expedited", "C) hampered", "D) accelerated"],
        "answer": "C",
        "explanation": "'Hampered' means hindered, obstructed, or made difficult."
    },
    {
        "question": "Vocabulary in Context:\n\nHer argument was so ______ that even her opponents had to admit she was right.",
        "options": ["A) tenuous", "B) flimsy", "C) compelling", "D) weak"],
        "answer": "C",
        "explanation": "'Compelling' means convincing, persuasive, and irrefutable."
    },
    {
        "question": "Vocabulary in Context:\n\nThe company's ______ growth has attracted investors from around the world.",
        "options": ["A) stagnant", "B) meteoric", "C) gradual", "D) modest"],
        "answer": "B",
        "explanation": "'Meteoric' means rapid, spectacular, and swift."
    },
    {
        "question": "Vocabulary in Context:\n\nHe's known for his ______ personality, always seeing the positive side of every situation.",
        "options": ["A) cynical", "B) pessimistic", "C) sanguine", "D) morose"],
        "answer": "C",
        "explanation": "'Sanguine' means optimistic, cheerful, and positive."
    },
    {
        "question": "Vocabulary in Context:\n\nThe diplomat's ______ response avoided committing to either side of the conflict.",
        "options": ["A) candid", "B) forthright", "C) equivocal", "D) explicit"],
        "answer": "C",
        "explanation": "'Equivocal' means ambiguous, unclear, and deliberately vague."
    },
    {
        "question": "Vocabulary in Context:\n\nThe project's failure was ______; warning signs had appeared months earlier.",
        "options": ["A) unforeseeable", "B) inevitable", "C) fortuitous", "D) serendipitous"],
        "answer": "B",
        "explanation": "'Inevitable' means unavoidable and certain to happen."
    },
    {
        "question": "Vocabulary in Context:\n\nHer ______ knowledge of ancient languages made her invaluable to the research team.",
        "options": ["A) superficial", "B) rudimentary", "C) encyclopedic", "D) limited"],
        "answer": "C",
        "explanation": "'Encyclopedic' means comprehensive, vast, and all-encompassing."
    },
    {
        "question": "Vocabulary in Context:\n\nThe artist's work was ______ by critics who dismissed it as meaningless.",
        "options": ["A) lauded", "B) celebrated", "C) vilified", "D) acclaimed"],
        "answer": "C",
        "explanation": "'Vilified' means harshly criticized or denounced."
    },
    {
        "question": "Vocabulary in Context:\n\nAfter years of economic decline, the country is finally showing signs of ______.",
        "options": ["A) stagnation", "B) recession", "C) rejuvenation", "D) deterioration"],
        "answer": "C",
        "explanation": "'Rejuvenation' means restoration and revival after decline."
    },
    {
        "question": "Vocabulary in Context:\n\nThe lawyer presented a ______ case that left no doubt about his client's innocence.",
        "options": ["A) weak", "B) tenuous", "C) ironclad", "D) dubious"],
        "answer": "C",
        "explanation": "'Ironclad' means unbreakable, solid, and incontrovertible."
    },
    {
        "question": "Vocabulary in Context:\n\nHer ______ remarks during the meeting offended several colleagues.",
        "options": ["A) tactful", "B) diplomatic", "C) brusque", "D) considerate"],
        "answer": "C",
        "explanation": "'Brusque' means abrupt, blunt, and rude."
    },
    {
        "question": "Vocabulary in Context:\n\nThe company's ______ into new markets proved to be highly profitable.",
        "options": ["A) retreat", "B) withdrawal", "C) foray", "D) hesitation"],
        "answer": "C",
        "explanation": "'Foray' means an initial attempt or venture into new area."
    },
    {
        "question": "Vocabulary in Context:\n\nThe government's ______ approach to reform frustrated those who wanted immediate change.",
        "options": ["A) radical", "B) drastic", "C) incremental", "D) revolutionary"],
        "answer": "C",
        "explanation": "'Incremental' means gradual, step-by-step, and slow."
    },

    # ==================== SECTION 6: READING COMPREHENSION (66-80) ====================
    {
        "question": "Reading Comprehension:\n\n'Despite the company's efforts to diversify, its fortunes remained inextricably linked to the volatile oil market.'\n\nWhat does 'inextricably linked' mean?",
        "options": ["A) Completely separated", "B) Unavoidably connected", "C) Temporarily associated", "D) Superficially related"],
        "answer": "B",
        "explanation": "'Inextricably linked' means impossible to separate or disconnect."
    },
    {
        "question": "Reading Comprehension:\n\n'The novel's protagonist is a quintessential antihero: brilliant but morally ambiguous, driven by self-interest yet capable of unexpected altruism.'\n\nThe protagonist is described as:",
        "options": ["A) A perfect hero", "B) A complex character with contradictions", "C) A purely villainous figure", "D) A simple, predictable character"],
        "answer": "B",
        "explanation": "The description shows contradictions, making the character complex."
    },
    {
        "question": "Reading Comprehension:\n\n'The new policy has been met with a groundswell of opposition from both employees and management alike.'\n\nWhat does 'groundswell' suggest?",
        "options": ["A) Minor opposition", "B) Rapidly growing grassroots movement", "C) Organized by management only", "D) Temporary opposition"],
        "answer": "B",
        "explanation": "'Groundswell' refers to a rapidly growing movement from grassroots."
    },
    {
        "question": "Reading Comprehension:\n\n'While initial results were promising, subsequent trials failed to replicate the findings.'\n\nWhat does this imply?",
        "options": ["A) Definitely correct", "B) Findings may be unreliable", "C) Never published", "D) Immediately accepted"],
        "answer": "B",
        "explanation": "Inability to replicate results casts doubt on validity."
    },
    {
        "question": "Reading Comprehension:\n\n'The CEO's resignation precipitated a cascade of executive departures.'\n\nWhat does 'precipitating' mean?",
        "options": ["A) Preventing", "B) Delaying", "C) Causing suddenly", "D) Ignoring"],
        "answer": "C",
        "explanation": "'Precipitating' means causing something to happen suddenly."
    },
    {
        "question": "Reading Comprehension:\n\n'Implementation has been stymied by bureaucratic inertia.'\n\nWhat happened to implementation?",
        "options": ["A) Progressed quickly", "B) Fully implemented", "C) Obstructed", "D) Celebrated"],
        "answer": "C",
        "explanation": "'Stymied' means prevented, obstructed, or blocked."
    },
    {
        "question": "Reading Comprehension:\n\n'She held the audience spellbound for over two hours.'\n\nWhat does 'spellbound' indicate?",
        "options": ["A) Bored", "B) Confused", "C) Captivated", "D) Angry"],
        "answer": "C",
        "explanation": "'Spellbound' means completely captivated and fascinated."
    },
    {
        "question": "Reading Comprehension:\n\n'The economy is predicated on tourism.'\n\nWhat does 'predicated on' mean?",
        "options": ["A) Independent of", "B) Based on", "C) Unrelated to", "D) Harmful to"],
        "answer": "B",
        "explanation": "'Predicated on' means based on, founded upon, or dependent on."
    },
    {
        "question": "Reading Comprehension:\n\n'His argument was replete with logical fallacies.'\n\nWhat does 'replete with' suggest?",
        "options": ["A) Lacked fallacies", "B) Filled with fallacies", "C) Few fallacies", "D) Ignored fallacies"],
        "answer": "B",
        "explanation": "'Replete with' means full of, abundantly supplied with."
    },
    {
        "question": "Reading Comprehension:\n\n'The discovery was serendipitous.'\n\nWhat does 'serendipitous' mean?",
        "options": ["A) Planned", "B) Expected", "C) Accidental but fortunate", "D) Disappointing"],
        "answer": "C",
        "explanation": "'Serendipitous' means occurring by chance in a happy way."
    },
    {
        "question": "Reading Comprehension:\n\n'Despite sanguine projections, profits plummeted.'\n\nWhat does 'sanguine' describe?",
        "options": ["A) Pessimistic", "B) Realistic", "C) Overly optimistic", "D) Accurate"],
        "answer": "C",
        "explanation": "'Sanguine' means optimistic, especially when unwarranted."
    },
    {
        "question": "Reading Comprehension:\n\n'The decision was a fait accompli.'\n\nWhat does 'fait accompli' mean?",
        "options": ["A) Ongoing discussion", "B) Already completed fact", "C) Future possibility", "D) Rejected idea"],
        "answer": "B",
        "explanation": "'Fait accompli' is French for 'accomplished fact'."
    },
    {
        "question": "Reading Comprehension:\n\n'Her research was characterized by meticulous attention to detail.'\n\nWhat does 'meticulous' suggest?",
        "options": ["A) Careless", "B) Extremely careful", "C) Quick", "D) Superficial"],
        "answer": "B",
        "explanation": "'Meticulous' means showing great attention to detail."
    },
    {
        "question": "Reading Comprehension:\n\n'The rebranding was largely cosmetic.'\n\nWhat does 'cosmetic' mean?",
        "options": ["A) Fundamental", "B) Superficial", "C) Innovative", "D) Successful"],
        "answer": "B",
        "explanation": "'Cosmetic' changes are superficial, affecting appearance only."
    },
    {
        "question": "Reading Comprehension:\n\n'His taciturn nature was mistaken for hostility.'\n\nWhat does 'taciturn' describe?",
        "options": ["A) Talkative", "B) Reserved and silent", "C) Friendly", "D) Aggressive"],
        "answer": "B",
        "explanation": "'Taciturn' means reserved, uncommunicative, and inclined to silence."
    },

    # ==================== SECTION 7: COMPLEX READING COMPREHENSION (81-90) ====================
    {
        "question": "Complex Reading:\n\n'The juxtaposition of opulence and squalor illustrates the widening chasm between socioeconomic strata.'\n\nWhat does 'juxtaposition' mean?",
        "options": ["A) Separation", "B) Blending", "C) Side-by-side placement", "D) Confusion"],
        "answer": "C",
        "explanation": "'Juxtaposition' means placing two things side by side for contrast."
    },
    {
        "question": "Complex Reading:\n\n'Her magnum opus cemented her legacy as a preeminent literary voice.'\n\nWhat is a 'magnum opus'?",
        "options": ["A) Minor work", "B) Masterpiece", "C) Unfinished project", "D) Failed attempt"],
        "answer": "B",
        "explanation": "'Magnum opus' (Latin) refers to an artist's greatest work."
    },
    {
        "question": "Complex Reading:\n\n'The negotiations reached an impasse.'\n\nWhat does 'impasse' mean?",
        "options": ["A) Breakthrough", "B) Deadlock", "C) Compromise", "D) Agreement"],
        "answer": "B",
        "explanation": "'Impasse' means a situation where no progress is possible."
    },
    {
        "question": "Complex Reading:\n\n'Despite espoused commitment, documents revealed disregard for regulations.'\n\nWhat does 'espoused' suggest?",
        "options": ["A) Genuine", "B) Secret", "C) Claimed but possibly insincere", "D) Recent"],
        "answer": "C",
        "explanation": "'Espoused' means claimed or professed, possibly insincere."
    },
    {
        "question": "Complex Reading:\n\n'The work eschewed hagiography in favor of nuanced analysis.'\n\nWhat does 'eschewing hagiography' mean?",
        "options": ["A) Avoiding uncritical praise", "B) Embracing criticism", "C) Writing biography", "D) Focusing on flaws"],
        "answer": "A",
        "explanation": "'Eschewing' means avoiding; 'hagiography' is idealized biography."
    },
    {
        "question": "Complex Reading:\n\n'The software was fraught with bugs.'\n\nWhat does 'fraught with' mean?",
        "options": ["A) Lacking", "B) Filled with problems", "C) Improved by", "D) Enhanced by"],
        "answer": "B",
        "explanation": "'Fraught with' means filled with (usually something negative)."
    },
    {
        "question": "Complex Reading:\n\n'His mercurial temperament made him difficult to work with.'\n\nWhat does 'mercurial' describe?",
        "options": ["A) Stable", "B) Predictable", "C) Volatile", "D) Calm"],
        "answer": "C",
        "explanation": "'Mercurial' means subject to sudden, unpredictable mood changes."
    },
    {
        "question": "Complex Reading:\n\n'The company's fiduciary duty to shareholders conflicted with ethical sourcing.'\n\nWhat is 'fiduciary duty'?",
        "options": ["A) Ethical responsibility", "B) Legal obligation", "C) Financial trust responsibility", "D) Social commitment"],
        "answer": "C",
        "explanation": "'Fiduciary duty' is a legal obligation to act in financial interest."
    },
    {
        "question": "Complex Reading:\n\n'The film's denouement provides cathartic release.'\n\nWhat does 'denouement' refer to?",
        "options": ["A) Beginning", "B) Climax", "C) Resolution", "D) Conflict"],
        "answer": "C",
        "explanation": "'Denouement' (French) is the final resolution of a story."
    },
    {
        "question": "Complex Reading:\n\n'His argument was predicated on a specious assumption.'\n\nWhat does 'specious' mean?",
        "options": ["A) Valid", "B) Superficially plausible but false", "C) Well-reasoned", "D) Proven"],
        "answer": "B",
        "explanation": "'Specious' means superficially plausible but actually false."
    },

    # ==================== SECTION 8: ALL TENSES IN CONTEXT (91-100) ====================
    {
        "question": "Tense Mastery:\n\n'By the time she arrives, the speaker ______ for over an hour.'",
        "options": ["A) will speak", "B) will have spoken", "C) will have been speaking", "D) speaks"],
        "answer": "C",
        "explanation": "Future Perfect Continuous emphasizes duration up to future point."
    },
    {
        "question": "Tense Mastery:\n\n'I ______ to contact you several times last week.'",
        "options": ["A) try", "B) have tried", "C) tried", "D) had tried"],
        "answer": "C",
        "explanation": "Past Simple for completed actions at a specific time."
    },
    {
        "question": "Tense Mastery:\n\n'For the past decade, the company ______ its market share steadily.'",
        "options": ["A) increased", "B) has been increasing", "C) had increased", "D) was increasing"],
        "answer": "B",
        "explanation": "Present Perfect Continuous emphasizes ongoing action up to now."
    },
    {
        "question": "Tense Mastery:\n\n'When I arrived, I realized I ______ my ticket at home.'",
        "options": ["A) left", "B) have left", "C) had left", "D) was leaving"],
        "answer": "C",
        "explanation": "Past Perfect for action completed before another past action."
    },
    {
        "question": "Tense Mastery:\n\n'Next week at this time, we ______ on a beach.'",
        "options": ["A) will relax", "B) will be relaxing", "C) relax", "D) are relaxing"],
        "answer": "B",
        "explanation": "Future Continuous for action in progress at specific future time."
    },
    {
        "question": "Tense Mastery:\n\n'She ______ as a nurse for fifteen years before she decided to pursue medicine.'",
        "options": ["A) worked", "B) has worked", "C) had been working", "D) was working"],
        "answer": "C",
        "explanation": "Past Perfect Continuous emphasizes duration before another past action."
    },
    {
        "question": "Tense Mastery:\n\n'This is the third time you ______ that excuse this week.'",
        "options": ["A) use", "B) used", "C) have used", "D) are using"],
        "answer": "C",
        "explanation": "'This is the + ordinal number + time' requires present perfect."
    },
    {
        "question": "Tense Mastery:\n\n'By 2030, autonomous vehicles ______ conventional cars.'",
        "options": ["A) will replace", "B) will have replaced", "C) replace", "D) are replacing"],
        "answer": "B",
        "explanation": "Future Perfect for actions completed by a specific future time."
    },
    {
        "question": "Tense Mastery:\n\n'I ______ to call you when you walked through the door.'",
        "options": ["A) was about", "B) am about", "C) have been about", "D) had about"],
        "answer": "A",
        "explanation": "'Was about to' expresses an action that was going to happen but was interrupted."
    },
    {
        "question": "Tense Mastery:\n\n'It's high time we ______ action on climate change.'",
        "options": ["A) take", "B) took", "C) have taken", "D) are taking"],
        "answer": "B",
        "explanation": "'It's (high) time' is followed by past simple."
    }
]

# ==================== OPTIMIZED DATA STRUCTURES ====================

user_sessions = {}
user_locks = {}
session_lock = Lock()

# ==================== HELPER FUNCTIONS ====================

def get_user_lock(user_id):
    """Get or create a lock for a user"""
    if user_id not in user_locks:
        user_locks[user_id] = Lock()
    return user_locks[user_id]

def get_progress_bar(current, total, width=10):
    filled = int((current / total) * width)
    return "█" * filled + "░" * (width - filled)

def get_category(index):
    if index < 15:
        return "📖 Reading Completion"
    elif index < 25:
        return "💬 Modal Conversations"
    elif index < 40:
        return "🔄 Conditionals"
    elif index < 50:
        return "🗣️ Reported Speech"
    elif index < 65:
        return "📚 Advanced Vocabulary"
    elif index < 90:
        return "📖 Reading Comprehension"
    else:
        return "⏰ Tense Mastery"

def get_level(percentage):
    if percentage >= 95:
        return "🏆 GRAND MASTER"
    elif percentage >= 85:
        return "🥇 ADVANCED EXPERT"
    elif percentage >= 75:
        return "🥈 PROFICIENT"
    elif percentage >= 65:
        return "🥉 COMPETENT"
    elif percentage >= 50:
        return "📘 INTERMEDIATE"
    else:
        return "🌱 DEVELOPING"

# ==================== HANDLERS ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    async with session_lock:
        user_sessions[user_id] = {"index": 0, "score": 0}
    
    await update.message.reply_text(
        "<b>🏆 PREMIUM ENGLISH MASTERY</b>\n\n"
        f"<b>📚 {len(questions)} Expert Questions</b>\n"
        "✓ Reading | ✓ Modals | ✓ Conditionals\n"
        "✓ Reported | ✓ Vocabulary | ✓ Comprehension | ✓ Tenses\n\n"
        "<b>⚡ ULTRA FAST</b>\n"
        "✓ Instant responses | ✓ 1-second auto-clear\n\n"
        "<b>🎯 Let's begin!</b>",
        parse_mode=ParseMode.HTML
    )
    await send_question(update, context)

async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    async with session_lock:
        session = user_sessions.get(user_id)
    
    if not session or session["index"] >= len(questions):
        if session:
            score = session["score"]
            percentage = (score / len(questions)) * 100
            level = get_level(percentage)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"<b>🏆 QUIZ COMPLETE!</b>\n\n"
                     f"📊 <b>Score:</b> {score}/{len(questions)}\n"
                     f"📈 <b>Percentage:</b> {percentage:.1f}%\n"
                     f"⭐ <b>Level:</b> {level}\n\n"
                     f"<i>Type /start to try again!</i>",
                parse_mode=ParseMode.HTML
            )
        return
    
    idx = session["index"]
    q = questions[idx]
    
    keyboard = [[InlineKeyboardButton(opt, callback_data=opt[0])] for opt in q["options"]]
    
    progress = get_progress_bar(idx, len(questions))
    percent = (idx / len(questions)) * 100
    category = get_category(idx)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"<b>{category}</b>\n"
             f"<b>📝 Q{idx + 1}/{len(questions)}</b>\n"
             f"<code>[{progress}]</code> <i>{percent:.0f}%</i>\n\n"
             f"{q['question']}",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    
    await query.answer()
    
    user_lock = get_user_lock(user_id)
    
    async with user_lock:
        async with session_lock:
            session = user_sessions.get(user_id)
            if not session:
                return
            idx = session["index"]
            if idx >= len(questions):
                return
            current_q = questions[idx]
        
        user_choice = query.data
        
        try:
            await query.edit_message_reply_markup(reply_markup=None)
        except:
            pass
        
        if user_choice == current_q["answer"]:
            async with session_lock:
                session["score"] += 1
            result_text = "✅ <b>CORRECT!</b> 🎯\n\n"
        else:
            correct_letter = current_q["answer"]
            correct_text = next(opt for opt in current_q["options"] if opt.startswith(correct_letter))
            result_text = f"❌ <b>INCORRECT</b>\n\n<b>✓ Answer:</b> {correct_text}\n\n"
        
        explanation_text = result_text + f"<b>📖 Explanation:</b>\n{current_q['explanation']}"
        
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=explanation_text,
            parse_mode=ParseMode.HTML
        )
        
        async with session_lock:
            session["index"] += 1
        
        await send_question(update, context)
        
        asyncio.create_task(delete_message_after_delay(context, update.effective_chat.id, msg.message_id, 1))

async def delete_message_after_delay(context, chat_id, message_id, delay):
    await asyncio.sleep(delay)
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except:
        pass

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with session_lock:
        total_users = len(user_sessions)
    
    await update.message.reply_text(
        f"<b>📊 STATISTICS</b>\n\n"
        f"👥 Users: {total_users}\n"
        f"📚 Questions: {len(questions)}",
        parse_mode=ParseMode.HTML
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Error: {context.error}")

# ==================== MAIN ====================

def main():
    app = Application.builder() \
        .token(BOT_TOKEN) \
        .concurrent_updates(True) \
        .build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_error_handler(error_handler)
    
    logger.info("=" * 60)
    logger.info("🤖 PREMIUM ENGLISH MASTERY BOT - PRODUCTION")
    logger.info(f"📚 Questions: {len(questions)}")
    logger.info("⚡ FEATURES: Concurrency | Locking | 1-Second Auto-Clear")
    logger.info("=" * 60)
    logger.info("✅ Bot is running...")
    
    app.run_polling(
        drop_pending_updates=True,
        allowed_updates=["message", "callback_query"]
    )

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"❌ Bot stopped: {e}")
        time.sleep(10)
