# -*- coding: utf-8 -*-
"""
Premium English Mastery Telegram Bot
100 Advanced English Questions with Detailed Explanations
FAST & STABLE - Auto-Clearing Explanations
"""

import logging
import asyncio
import nest_asyncio
import os
import sys
import threading
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# 1. Fix for Google Colab/Jupyter
nest_asyncio.apply()

# 2. Setup Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# 3. Get Bot Token from Environment Variable
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    logger.error("❌ BOT_TOKEN not found! Please set BOT_TOKEN environment variable.")
    sys.exit(1)

logger.info("✅ Bot token loaded successfully")

# 4. Keep Alive Function for GitHub Actions
def keep_alive():
    while True:
        time.sleep(300)
        logger.info("💓 Bot heartbeat - still running")

heartbeat_thread = threading.Thread(target=keep_alive, daemon=True)
heartbeat_thread.start()

# ==================== COMPLETE 100 QUESTIONS DATABASE ====================

questions = [
    # ==================== SECTION 1: READING PASSAGE COMPLETION (1-15) ====================
    {
        "question": "Read the passage and choose the correct verb form:\n\n'The ancient manuscript, which ______ in a monastery for centuries, was finally discovered in 2019.'",
        "options": ["A) had been hidden", "B) was hidden", "C) has been hidden", "D) is hidden"],
        "answer": "A",
        "explanation": "Past Perfect Passive 'had been hidden' is used because the hiding occurred before the discovery in 2019 (past perfect for the earlier action)."
    },
    {
        "question": "Passage completion:\n\n'By the time the rescue team arrived, the survivors ______ for over 48 hours.'",
        "options": ["A) waited", "B) have been waiting", "C) had been waiting", "D) were waiting"],
        "answer": "C",
        "explanation": "Past Perfect Continuous 'had been waiting' emphasizes the duration of waiting that was ongoing before another past action (the arrival)."
    },
    {
        "question": "Passage completion:\n\n'Currently, the new bridge ______, and it's expected to open next spring.'",
        "options": ["A) is constructing", "B) is being constructed", "C) has constructed", "D) was constructed"],
        "answer": "B",
        "explanation": "Present Continuous Passive 'is being constructed' indicates an ongoing action in the present with the focus on the bridge, not the builders."
    },
    {
        "question": "Passage completion:\n\n'By 2030, scientists predict that renewable energy ______ fossil fuels as the primary power source.'",
        "options": ["A) will replace", "B) will have replaced", "C) replaces", "D) is replacing"],
        "answer": "B",
        "explanation": "Future Perfect 'will have replaced' is used for actions that will be completed by a specific future time (by 2030)."
    },
    {
        "question": "Passage completion:\n\n'After the CEO ______ the company for 20 years, he announced his retirement.'",
        "options": ["A) led", "B) was leading", "C) had been leading", "D) has led"],
        "answer": "C",
        "explanation": "Past Perfect Continuous 'had been leading' emphasizes the duration of leadership before the announcement."
    },
    {
        "question": "Passage completion:\n\n'Climate change, which ______ a global crisis for decades, requires immediate action.'",
        "options": ["A) was", "B) had been", "C) has been", "D) is"],
        "answer": "C",
        "explanation": "Present Perfect 'has been' connects a past situation (for decades) to the present reality."
    },
    {
        "question": "Passage completion:\n\n'By the time you read this, the spacecraft ______ on Mars for three days.'",
        "options": ["A) will land", "B) will have landed", "C) will have been landing", "D) lands"],
        "answer": "C",
        "explanation": "Future Perfect Continuous 'will have been landing' emphasizes the duration of the action up to a future point."
    },
    {
        "question": "Passage completion:\n\n'The artifacts, which ______ in the tomb since 3000 BCE, provided invaluable historical insights.'",
        "options": ["A) were buried", "B) had been buried", "C) have been buried", "D) are buried"],
        "answer": "B",
        "explanation": "Past Perfect Passive 'had been buried' indicates the state before the discovery, with a time reference (since 3000 BCE) up to that point."
    },
    {
        "question": "Passage completion:\n\n'As we speak, negotiations ______ between the two countries to resolve the conflict.'",
        "options": ["A) hold", "B) are held", "C) are being held", "D) have held"],
        "answer": "C",
        "explanation": "Present Continuous Passive 'are being held' indicates ongoing action at the moment of speaking."
    },
    {
        "question": "Passage completion:\n\n'The professor, along with her research team, ______ on this project since 2015.'",
        "options": ["A) work", "B) has been working", "C) have been working", "D) worked"],
        "answer": "B",
        "explanation": "Present Perfect Continuous 'has been working' emphasizes duration from past to present. 'Along with' doesn't change singular subject agreement."
    },
    {
        "question": "Passage completion:\n\n'Before the internet revolutionized communication, information ______ primarily through print media.'",
        "options": ["A) was disseminated", "B) is disseminated", "C) has been disseminated", "D) disseminates"],
        "answer": "A",
        "explanation": "Past Simple Passive 'was disseminated' describes a completed past state before the internet age."
    },
    {
        "question": "Passage completion:\n\n'The suspect ______ to have fled the country before the warrant was issued.'",
        "options": ["A) believes", "B) is believed", "C) believed", "D) has believed"],
        "answer": "B",
        "explanation": "Impersonal passive 'is believed' with reporting verb. Common structure: 'It is believed that...' or 'S + is believed to...'"
    },
    {
        "question": "Passage completion:\n\n'By next December, I ______ as a software engineer for a decade.'",
        "options": ["A) will work", "B) will have been working", "C) work", "D) am working"],
        "answer": "B",
        "explanation": "Future Perfect Continuous 'will have been working' emphasizes the duration of an action up to a specific future point."
    },
    {
        "question": "Passage completion:\n\n'The documentary, which ______ by millions worldwide, won multiple awards.'",
        "options": ["A) has been viewed", "B) had been viewed", "C) was viewed", "D) is viewed"],
        "answer": "A",
        "explanation": "Present Perfect Passive 'has been viewed' connects the past viewing to present recognition (won awards)."
    },
    {
        "question": "Passage completion:\n\n'During the summit, it ______ that the trade agreement would be signed by year-end.'",
        "options": ["A) announced", "B) was announced", "C) has announced", "D) is announcing"],
        "answer": "B",
        "explanation": "Past Simple Passive 'was announced' for a reported event in the past with no ongoing relevance needed."
    },

    # ==================== SECTION 2: MODAL AUXILIARIES IN CONVERSATIONS (16-25) ====================
    {
        "question": "Conversation:\n\nA: 'Someone's at the door. Who ______ it be at this hour?'\nB: 'I'm not sure. It ______ be the delivery person.'",
        "options": ["A) can / might", "B) must / should", "C) will / can", "D) shall / would"],
        "answer": "A",
        "explanation": "'Can' expresses possibility in questions; 'might' expresses possibility in statements. Both indicate uncertainty."
    },
    {
        "question": "Conversation:\n\nA: 'I'm exhausted. I ______ have stayed up so late.'\nB: 'You're right. You ______ have gone to bed earlier.'",
        "options": ["A) shouldn't / should", "B) mustn't / must", "C) couldn't / could", "D) wouldn't / would"],
        "answer": "A",
        "explanation": "'Shouldn't have' expresses regret about a past action; 'should have' gives advice about a better past choice."
    },
    {
        "question": "Conversation:\n\nA: 'Look at that car! It ______ have cost a fortune.'\nB: 'Definitely. Only a millionaire ______ afford that.'",
        "options": ["A) can / must", "B) must / could", "C) might / should", "D) would / may"],
        "answer": "B",
        "explanation": "'Must have' for strong deduction about the past; 'could' for possibility/ability in hypothetical situations."
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
        "explanation": "'Might' expresses possibility; 'must' expresses strong deduction based on visual evidence."
    },
    {
        "question": "Conversation:\n\nA: 'You ______ have seen the look on his face when I told him!'\nB: 'I wish I ______ have been there. It sounds hilarious.'",
        "options": ["A) should / should", "B) must / could", "C) could / would", "D) might / might"],
        "answer": "B",
        "explanation": "'Must have' expresses strong deduction about a past event; 'could have' expresses unrealized past possibility."
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
        "explanation": "'Must' for logical deduction; 'could' for polite expression of need/desire."
    },

    # ==================== SECTION 3: ALL CONDITIONALS WITH MEANING (26-40) ====================
    {
        "question": "Zero Conditional (General Truth):\n\n'If you ______ water to 100°C, it ______.'",
        "options": ["A) heat / boils", "B) will heat / boils", "C) heat / will boil", "D) heated / boiled"],
        "answer": "A",
        "explanation": "Zero Conditional expresses scientific facts/general truths: If + Present Simple, Present Simple."
    },
    {
        "question": "First Conditional (Real Future):\n\n'If she ______ the exam, she ______ medical school next year.'",
        "options": ["A) passes / will enter", "B) will pass / enters", "C) passed / would enter", "D) had passed / would have entered"],
        "answer": "A",
        "explanation": "First Conditional expresses real possibility: If + Present Simple, will + infinitive."
    },
    {
        "question": "Second Conditional (Unreal Present):\n\n'If I ______ you, I ______ that job offer immediately.'",
        "options": ["A) am / will accept", "B) were / would accept", "C) had been / would have accepted", "D) was / accept"],
        "answer": "B",
        "explanation": "Second Conditional expresses hypothetical/unreal present: If + Past Simple, would + infinitive. 'Were' is used for all subjects in formal English."
    },
    {
        "question": "Third Conditional (Unreal Past):\n\n'If they ______ the warning, the accident ______.'",
        "options": ["A) heeded / wouldn't happen", "B) had heeded / wouldn't have happened", "C) heeded / wouldn't have happened", "D) had heeded / didn't happen"],
        "answer": "B",
        "explanation": "Third Conditional expresses impossible past conditions: If + Past Perfect, would have + past participle."
    },
    {
        "question": "Mixed Conditional (Past Condition → Present Result):\n\n'If she ______ harder in college, she ______ a better job now.'",
        "options": ["A) studied / would have", "B) had studied / would have", "C) had studied / would be", "D) studied / would be"],
        "answer": "C",
        "explanation": "Mixed Conditional: Past condition (had studied) affects present result (would be). Shows how past actions influence current situations."
    },
    {
        "question": "Mixed Conditional (Present Condition → Past Result):\n\n'If I ______ more confident, I ______ for that promotion last year.'",
        "options": ["A) am / would apply", "B) were / would have applied", "C) had been / would apply", "D) was / would apply"],
        "answer": "B",
        "explanation": "Mixed Conditional: Present state (were confident) would have changed a past outcome (would have applied)."
    },
    {
        "question": "Inverted Conditional (Formal - Third):\n\n'______ earlier, the disaster could have been prevented.'",
        "options": ["A) Had they evacuated", "B) If they evacuated", "C) Were they to evacuate", "D) They evacuated"],
        "answer": "A",
        "explanation": "Inverted Third Conditional: 'Had + subject + past participle' = 'If + subject + had + past participle'. Used in formal writing."
    },
    {
        "question": "Inverted Conditional (Formal - Second):\n\n'______ to win the lottery, what would you do?'",
        "options": ["A) Had you", "B) Were you", "C) If you", "D) Should you"],
        "answer": "B",
        "explanation": "Inverted Second Conditional: 'Were + subject + to + infinitive' = 'If + subject + were to + infinitive'. Formal structure for hypotheticals."
    },
    {
        "question": "Conditional with 'unless' (Negative Condition):\n\n'The project will succeed ______ everyone contributes fully.'",
        "options": ["A) unless", "B) if", "C) provided that", "D) only if"],
        "answer": "A",
        "explanation": "'Unless' means 'if not'. The sentence means: The project will fail if not everyone contributes."
    },
    {
        "question": "Conditional with 'provided that' (Stipulation):\n\n'You can borrow the car ______ you return it by 10 PM.'",
        "options": ["A) unless", "B) even if", "C) provided that", "D) as long as"],
        "answer": "C",
        "explanation": "'Provided that' introduces a condition that must be met. Similar to 'if' but more formal and stipulative."
    },
    {
        "question": "Complex Conditional with 'but for':\n\n'______ your support, I would have given up long ago.'",
        "options": ["A) Without", "B) But for", "C) Except for", "D) Aside from"],
        "answer": "B",
        "explanation": "'But for' means 'if it were not for' or 'without'. Used in formal English to express hypothetical conditions."
    },
    {
        "question": "Conditional with 'even if' (Concession):\n\n'I wouldn't marry him ______ he were the last man on Earth.'",
        "options": ["A) even if", "B) only if", "C) unless", "D) provided that"],
        "answer": "A",
        "explanation": "'Even if' introduces a hypothetical condition that doesn't change the outcome. Expresses strong conviction."
    },
    {
        "question": "Complex Conditional with 'supposing':\n\n'______ you inherited a million dollars, how would you spend it?'",
        "options": ["A) Unless", "B) Supposing", "C) Provided", "D) Even if"],
        "answer": "B",
        "explanation": "'Supposing' introduces a hypothetical scenario for consideration. Similar to 'imagine if'."
    },
    {
        "question": "Complex Conditional with 'were it not for':\n\n'______ his quick thinking, the company would have collapsed.'",
        "options": ["A) Were it not for", "B) If it wasn't for", "C) Had it not been for", "D) But for"],
        "answer": "C",
        "explanation": "Both 'Had it not been for' and 'Were it not for' are correct. 'Had it not been for' is third conditional; 'Were it not for' is mixed. This sentence requires third conditional for past event."
    },
    {
        "question": "Conditional with 'as long as' (Condition):\n\n'You'll succeed ______ you never give up.'",
        "options": ["A) unless", "B) as long as", "C) even if", "D) whereas"],
        "answer": "B",
        "explanation": "'As long as' introduces a necessary condition for the result. Emphasizes that the result depends entirely on the condition."
    },

    # ==================== SECTION 4: REPORTED SPEECH (41-50) ====================
    {
        "question": "Reported Speech - Statement:\n\nDirect: 'I will finish the project by Friday,' she said.\nReported: She said that she ______ the project by Friday.",
        "options": ["A) will finish", "B) would finish", "C) finishes", "D) finished"],
        "answer": "B",
        "explanation": "'Will' changes to 'would' in reported speech when the reporting verb is in past tense."
    },
    {
        "question": "Reported Speech - Question:\n\nDirect: 'Where did you buy that jacket?' he asked.\nReported: He asked me where I ______ that jacket.",
        "options": ["A) bought", "B) had bought", "C) buy", "D) have bought"],
        "answer": "B",
        "explanation": "Past Simple changes to Past Perfect in reported questions. Time shift: did buy → had bought."
    },
    {
        "question": "Reported Speech - Command:\n\nDirect: 'Don't touch the artifacts,' the curator said.\nReported: The curator warned us ______ the artifacts.",
        "options": ["A) not to touch", "B) to not touch", "C) don't touch", "D) didn't touch"],
        "answer": "A",
        "explanation": "Negative commands use 'not to + infinitive'. 'Told/warned + object + not to + verb' is the standard structure."
    },
    {
        "question": "Reported Speech - Request:\n\nDirect: 'Could you help me with this?' she asked.\nReported: She asked me ______ help her with that.",
        "options": ["A) that I could", "B) if I could", "C) could I", "D) I could"],
        "answer": "B",
        "explanation": "Polite requests with 'could' become 'asked if + subject + could' in reported speech."
    },
    {
        "question": "Reported Speech - Time Change:\n\nDirect: 'I'll see you tomorrow,' he said.\nReported: He said he would see me ______.",
        "options": ["A) tomorrow", "B) the next day", "C) on tomorrow", "D) the following tomorrow"],
        "answer": "B",
        "explanation": "Time expressions shift: tomorrow → the next day / the following day."
    },
    {
        "question": "Reported Speech - Place Change:\n\nDirect: 'I'm staying here,' she said.\nReported: She said she was staying ______.",
        "options": ["A) there", "B) here", "C) at here", "D) in there"],
        "answer": "A",
        "explanation": "Place references shift: here → there when the location changes in reported context."
    },
    {
        "question": "Reported Speech - Modal Change:\n\nDirect: 'You must finish this tonight,' he said.\nReported: He said I ______ finish that that night.",
        "options": ["A) must", "B) had to", "C) must have", "D) would"],
        "answer": "B",
        "explanation": "'Must' often changes to 'had to' in reported speech when expressing obligation."
    },
    {
        "question": "Reported Speech - Imperative:\n\nDirect: 'Please arrive on time,' the manager said.\nReported: The manager asked us ______ on time.",
        "options": ["A) arrive", "B) to arrive", "C) arriving", "D) that we arrive"],
        "answer": "B",
        "explanation": "Imperatives (requests/commands) use 'ask/tell + object + to + infinitive'."
    },
    {
        "question": "Reported Speech - Universal Truth:\n\nDirect: 'The Earth orbits the Sun,' the teacher said.\nReported: The teacher said that the Earth ______ the Sun.",
        "options": ["A) orbited", "B) orbits", "C) had orbited", "D) was orbiting"],
        "answer": "B",
        "explanation": "Universal truths, scientific facts, and general truths don't change tense in reported speech."
    },
    {
        "question": "Reported Speech - Mixed Reporting:\n\nDirect: 'I was waiting when you called,' he explained.\nReported: He explained that he ______ when I ______.",
        "options": ["A) waited / called", "B) was waiting / had called", "C) had been waiting / called", "D) had been waiting / had called"],
        "answer": "D",
        "explanation": "Past Continuous (was waiting) becomes Past Perfect Continuous (had been waiting); Past Simple (called) becomes Past Perfect (had called)."
    },

    # ==================== SECTION 5: ADVANCED VOCABULARY IN CONTEXT (51-65) ====================
    {
        "question": "Vocabulary in Context:\n\nThe CEO's ______ speech inspired the entire company to work toward the ambitious goals.",
        "options": ["A) lackluster", "B) mundane", "C) rousing", "D) tedious"],
        "answer": "C",
        "explanation": "'Rousing' means exciting, stirring, and inspiring. It matches the context of inspiring employees toward ambitious goals."
    },
    {
        "question": "Vocabulary in Context:\n\nDespite their ______ differences, the two leaders managed to reach a historic agreement.",
        "options": ["A) trivial", "B) profound", "C) superficial", "D) negligible"],
        "answer": "B",
        "explanation": "'Profound' means deep, significant, and far-reaching. It contrasts with the achievement of reaching an agreement despite major differences."
    },
    {
        "question": "Vocabulary in Context:\n\nThe investigation was ______ by the sudden disappearance of key evidence.",
        "options": ["A) facilitated", "B) expedited", "C) hampered", "D) accelerated"],
        "answer": "C",
        "explanation": "'Hampered' means hindered, obstructed, or made difficult. The disappearance of evidence would impede the investigation."
    },
    {
        "question": "Vocabulary in Context:\n\nHer argument was so ______ that even her opponents had to admit she was right.",
        "options": ["A) tenuous", "B) flimsy", "C) compelling", "D) weak"],
        "answer": "C",
        "explanation": "'Compelling' means convincing, persuasive, and irrefutable. It explains why opponents had to concede."
    },
    {
        "question": "Vocabulary in Context:\n\nThe company's ______ growth has attracted investors from around the world.",
        "options": ["A) stagnant", "B) meteoric", "C) gradual", "D) modest"],
        "answer": "B",
        "explanation": "'Meteoric' means rapid, spectacular, and swift, like a meteor. It describes the kind of growth that attracts global investors."
    },
    {
        "question": "Vocabulary in Context:\n\nHe's known for his ______ personality, always seeing the positive side of every situation.",
        "options": ["A) cynical", "B) pessimistic", "C) sanguine", "D) morose"],
        "answer": "C",
        "explanation": "'Sanguine' means optimistic, cheerful, and positive. It directly matches the description of always seeing the positive side."
    },
    {
        "question": "Vocabulary in Context:\n\nThe diplomat's ______ response avoided committing to either side of the conflict.",
        "options": ["A) candid", "B) forthright", "C) equivocal", "D) explicit"],
        "answer": "C",
        "explanation": "'Equivocal' means ambiguous, unclear, and deliberately vague to avoid commitment. Perfect for diplomatic language."
    },
    {
        "question": "Vocabulary in Context:\n\nThe project's failure was ______; warning signs had appeared months earlier.",
        "options": ["A) unforeseeable", "B) inevitable", "C) fortuitous", "D) serendipitous"],
        "answer": "B",
        "explanation": "'Inevitable' means unavoidable and certain to happen. The warning signs made the failure predictable."
    },
    {
        "question": "Vocabulary in Context:\n\nHer ______ knowledge of ancient languages made her invaluable to the research team.",
        "options": ["A) superficial", "B) rudimentary", "C) encyclopedic", "D) limited"],
        "answer": "C",
        "explanation": "'Encyclopedic' means comprehensive, vast, and all-encompassing knowledge, like an encyclopedia."
    },
    {
        "question": "Vocabulary in Context:\n\nThe artist's work was ______ by critics who dismissed it as meaningless.",
        "options": ["A) lauded", "B) celebrated", "C) vilified", "D) acclaimed"],
        "answer": "C",
        "explanation": "'Vilified' means harshly criticized, denounced, or spoken of as evil. It contrasts with positive terms like lauded or acclaimed."
    },
    {
        "question": "Vocabulary in Context:\n\nAfter years of economic decline, the country is finally showing signs of ______.",
        "options": ["A) stagnation", "B) recession", "C) rejuvenation", "D) deterioration"],
        "answer": "C",
        "explanation": "'Rejuvenation' means restoration, revival, and renewal after a period of decline. Matches 'finally showing signs' of improvement."
    },
    {
        "question": "Vocabulary in Context:\n\nThe lawyer presented a ______ case that left no doubt about his client's innocence.",
        "options": ["A) weak", "B) tenuous", "C) ironclad", "D) dubious"],
        "answer": "C",
        "explanation": "'Ironclad' means unbreakable, solid, and incontrovertible. A case that leaves no doubt must be ironclad."
    },
    {
        "question": "Vocabulary in Context:\n\nHer ______ remarks during the meeting offended several colleagues.",
        "options": ["A) tactful", "B) diplomatic", "C) brusque", "D) considerate"],
        "answer": "C",
        "explanation": "'Brusque' means abrupt, blunt, and rude to the point of being offensive. It explains why colleagues were offended."
    },
    {
        "question": "Vocabulary in Context:\n\nThe company's ______ into new markets proved to be highly profitable.",
        "options": ["A) retreat", "B) withdrawal", "C) foray", "D) hesitation"],
        "answer": "C",
        "explanation": "'Foray' means an initial attempt or venture into a new area or activity. It specifically refers to entering new markets."
    },
    {
        "question": "Vocabulary in Context:\n\nThe government's ______ approach to reform frustrated those who wanted immediate change.",
        "options": ["A) radical", "B) drastic", "C) incremental", "D) revolutionary"],
        "answer": "C",
        "explanation": "'Incremental' means gradual, step-by-step, and slow. It frustrates those wanting immediate, drastic change."
    },

    # ==================== SECTION 6: READING COMPREHENSION (66-80) ====================
    {
        "question": "Reading Comprehension:\n\n'Despite the company's efforts to diversify, its fortunes remained inextricably linked to the volatile oil market.'\n\nWhat does 'inextricably linked' mean in this context?",
        "options": ["A) Completely separated", "B) Unavoidably connected", "C) Temporarily associated", "D) Superficially related"],
        "answer": "B",
        "explanation": "'Inextricably linked' means impossible to separate or disconnect. The company's fortunes cannot be separated from the oil market."
    },
    {
        "question": "Reading Comprehension:\n\n'The novel's protagonist is a quintessential antihero: brilliant but morally ambiguous, driven by self-interest yet capable of unexpected altruism.'\n\nBased on this, the protagonist is described as:",
        "options": ["A) A perfect hero", "B) A complex character with contradictions", "C) A purely villainous figure", "D) A simple, predictable character"],
        "answer": "B",
        "explanation": "The description shows contradictions (brilliant but morally ambiguous, self-interested yet altruistic), making the character complex, not simple or purely heroic/villainous."
    },
    {
        "question": "Reading Comprehension:\n\n'The new policy, which took effect last month, has been met with a groundswell of opposition from both employees and management alike—a rare convergence of interests that underscores the policy's fundamental flaws.'\n\nWhat does 'groundswell' suggest about the opposition?",
        "options": ["A) It's minor and insignificant", "B) It's growing rapidly from grassroots", "C) It's organized by management only", "D) It's temporary and will pass"],
        "answer": "B",
        "explanation": "'Groundswell' refers to a rapidly growing movement, especially from the grassroots level. The rare convergence of employees and management shows broad-based growth."
    },
    {
        "question": "Reading Comprehension:\n\n'While the initial results were promising, subsequent trials failed to replicate the findings, casting doubt on the original study's validity.'\n\nWhat does this imply about the original study?",
        "options": ["A) It was definitely correct", "B) Its findings may be unreliable", "C) It was never published", "D) It was immediately accepted"],
        "answer": "B",
        "explanation": "The inability to replicate results (failed to replicate) casts doubt on validity, meaning the original findings may be unreliable."
    },
    {
        "question": "Reading Comprehension:\n\n'The CEO's resignation sent shockwaves through the industry, precipitating a cascade of executive departures from competitor firms.'\n\nWhat does 'precipitating' mean in this context?",
        "options": ["A) Preventing", "B) Delaying", "C) Causing suddenly", "D) Ignoring"],
        "answer": "C",
        "explanation": "'Precipitating' means causing something to happen suddenly or unexpectedly. The CEO's resignation triggered a cascade of departures."
    },
    {
        "question": "Reading Comprehension:\n\n'Although the treaty was lauded as a diplomatic breakthrough, its implementation has been stymied by bureaucratic inertia and conflicting national interests.'\n\nWhat has happened to the treaty's implementation?",
        "options": ["A) It progressed quickly", "B) It was fully implemented", "C) It was obstructed", "D) It was celebrated"],
        "answer": "C",
        "explanation": "'Stymied' means prevented, obstructed, or blocked from progressing. Bureaucratic inertia and conflicts have obstructed implementation."
    },
    {
        "question": "Reading Comprehension:\n\n'The candidate's oratorical skills were on full display as she held the audience spellbound for over two hours, weaving complex policy details into a compelling narrative.'\n\nWhat does 'spellbound' indicate about the audience?",
        "options": ["A) They were bored", "B) They were confused", "C) They were captivated", "D) They were angry"],
        "answer": "C",
        "explanation": "'Spellbound' means completely captivated, fascinated, and unable to look away, like under a spell."
    },
    {
        "question": "Reading Comprehension:\n\n'The region's economy is predicated on tourism, making it particularly vulnerable to fluctuations in global travel patterns.'\n\nWhat does 'predicated on' mean?",
        "options": ["A) Independent of", "B) Based on", "C) Unrelated to", "D) Harmful to"],
        "answer": "B",
        "explanation": "'Predicated on' means based on, founded upon, or dependent on. The economy depends on tourism."
    },
    {
        "question": "Reading Comprehension:\n\n'His argument was so replete with logical fallacies that even his staunchest allies found it difficult to defend.'\n\nWhat does 'replete with' suggest about the argument?",
        "options": ["A) It lacked fallacies", "B) It was filled with fallacies", "C) It had few fallacies", "D) It ignored fallacies"],
        "answer": "B",
        "explanation": "'Replete with' means full of, abundantly supplied with, or filled with. The argument was full of logical fallacies."
    },
    {
        "question": "Reading Comprehension:\n\n'The discovery of the ancient manuscript was serendipitous; researchers had been searching for something entirely different when they stumbled upon it.'\n\nWhat does 'serendipitous' mean?",
        "options": ["A) Planned", "B) Expected", "C) Accidental but fortunate", "D) Disappointing"],
        "answer": "C",
        "explanation": "'Serendipitous' means occurring by chance in a happy or beneficial way. The discovery was accidental but fortunate."
    },
    {
        "question": "Reading Comprehension:\n\n'Despite the CEO's sanguine projections, the company's quarterly report revealed a starkly different reality, with profits plummeting by 40%.'\n\nWhat does 'sanguine' describe about the CEO's projections?",
        "options": ["A) Pessimistic", "B) Realistic", "C) Overly optimistic", "D) Accurate"],
        "answer": "C",
        "explanation": "'Sanguine' means optimistic or positive, especially in a situation where optimism may be unwarranted. The contrast with plummeting profits shows the projections were overly optimistic."
    },
    {
        "question": "Reading Comprehension:\n\n'The committee's decision was a fait accompli by the time the public became aware of the proposal, leaving no room for input or debate.'\n\nWhat does 'fait accompli' mean?",
        "options": ["A) An ongoing discussion", "B) An already completed fact", "C) A future possibility", "D) A rejected idea"],
        "answer": "B",
        "explanation": "'Fait accompli' is French for 'accomplished fact' — something already done and irreversible before others learn of it."
    },
    {
        "question": "Reading Comprehension:\n\n'Her research was characterized by a meticulous attention to detail, which both explained her slow progress and ensured the accuracy of her findings.'\n\nWhat does 'meticulous' suggest about her work?",
        "options": ["A) Careless", "B) Extremely careful", "C) Quick", "D) Superficial"],
        "answer": "B",
        "explanation": "'Meticulous' means showing great attention to detail; very careful and precise. This explains both slow progress and high accuracy."
    },
    {
        "question": "Reading Comprehension:\n\n'The company's attempts to rebrand were largely cosmetic, changing the packaging and logo while leaving the core product unchanged.'\n\nWhat does 'cosmetic' mean in this context?",
        "options": ["A) Fundamental", "B) Superficial", "C) Innovative", "D) Successful"],
        "answer": "B",
        "explanation": "'Cosmetic' changes are superficial, affecting appearance but not substance. The changes were only to packaging and logo, not the product itself."
    },
    {
        "question": "Reading Comprehension:\n\n'His taciturn nature was often mistaken for hostility, when in reality he was simply shy and introverted.'\n\nWhat does 'taciturn' describe?",
        "options": ["A) Talkative", "B) Reserved and silent", "C) Friendly", "D) Aggressive"],
        "answer": "B",
        "explanation": "'Taciturn' means reserved, uncommunicative, and inclined to silence. It's often misinterpreted as hostility when it's actually shyness."
    },

    # ==================== SECTION 7: COMPLEX READING COMPREHENSION (81-90) ====================
    {
        "question": "Complex Reading:\n\n'The juxtaposition of opulence and squalor in the city's central district serves as a potent metaphor for the widening chasm between the socioeconomic strata.'\n\nWhat does 'juxtaposition' mean in this context?",
        "options": ["A) Separation", "B) Blending", "C) Side-by-side placement", "D) Confusion"],
        "answer": "C",
        "explanation": "'Juxtaposition' means placing two things side by side for contrast. The contrast between opulence (wealth) and squalor (poverty) illustrates economic inequality."
    },
    {
        "question": "Complex Reading:\n\n'Her magnum opus, a sprawling 1,200-page novel that took two decades to complete, cemented her legacy as one of the preeminent literary voices of her generation.'\n\nWhat is a 'magnum opus'?",
        "options": ["A) A minor work", "B) A masterpiece", "C) An unfinished project", "D) A failed attempt"],
        "answer": "B",
        "explanation": "'Magnum opus' (Latin for 'great work') refers to an artist's greatest, most important, or most renowned work."
    },
    {
        "question": "Complex Reading:\n\n'The negotiations reached an impasse when neither side would concede on the issue of border controls, leaving the future of the agreement in jeopardy.'\n\nWhat does 'impasse' mean?",
        "options": ["A) Breakthrough", "B) Deadlock", "C) Compromise", "D) Agreement"],
        "answer": "B",
        "explanation": "'Impasse' means a situation where no progress is possible, a deadlock. Neither side conceding creates an impasse."
    },
    {
        "question": "Complex Reading:\n\n'Despite the company's espoused commitment to sustainability, internal documents revealed a flagrant disregard for environmental regulations.'\n\nWhat does 'espoused' suggest about the commitment?",
        "options": ["A) Genuine", "B) Secret", "C) Claimed but possibly insincere", "D) Recent"],
        "answer": "C",
        "explanation": "'Espoused' means claimed, professed, or advocated. The contrast with internal documents showing disregard suggests the claimed commitment may be insincere."
    },
    {
        "question": "Complex Reading:\n\n'The historian's work was lauded for its evenhanded treatment of controversial figures, eschewing hagiography in favor of nuanced analysis.'\n\nWhat does 'eschewing hagiography' mean?",
        "options": ["A) Avoiding uncritical praise", "B) Embracing criticism", "C) Writing biography", "D) Focusing on flaws"],
        "answer": "A",
        "explanation": "'Eschewing' means avoiding deliberately; 'hagiography' is idealized, uncritical biography. The historian avoids idealized praise for balanced analysis."
    },
    {
        "question": "Complex Reading:\n\n'The new software promised to revolutionize workflow efficiency, but early adopters found it to be more of a hindrance than a help, fraught with bugs and counterintuitive features.'\n\nWhat does 'fraught with' mean?",
        "options": ["A) Lacking", "B) Filled with problems", "C) Improved by", "D) Enhanced by"],
        "answer": "B",
        "explanation": "'Fraught with' means filled with, accompanied by, or characterized by (usually something negative). The software was full of bugs."
    },
    {
        "question": "Complex Reading:\n\n'The CEO's mercurial temperament made him difficult to work with; his moods could shift from jubilant to wrathful in a matter of minutes.'\n\nWhat does 'mercurial' describe?",
        "options": ["A) Stable", "B) Predictable", "C) Volatile", "D) Calm"],
        "answer": "C",
        "explanation": "'Mercurial' means subject to sudden, unpredictable changes of mood. The rapid shift from jubilant to wrathful exemplifies this."
    },
    {
        "question": "Complex Reading:\n\n'The company's fiduciary duty to its shareholders often conflicted with its stated commitment to ethical sourcing, creating a perennial tension between profit and principle.'\n\nWhat is 'fiduciary duty'?",
        "options": ["A) Ethical responsibility", "B) Legal obligation", "C) Financial trust responsibility", "D) Social commitment"],
        "answer": "C",
        "explanation": "'Fiduciary duty' is a legal obligation to act in the best financial interest of another party (shareholders), including trust, loyalty, and good faith."
    },
    {
        "question": "Complex Reading:\n\n'The film's denouement, in which the protagonist finally confronts her childhood trauma, provides a cathartic release that resonates long after the credits roll.'\n\nWhat does 'denouement' refer to?",
        "options": ["A) The beginning", "B) The climax", "C) The resolution", "D) The conflict"],
        "answer": "C",
        "explanation": "'Denouement' (French for 'untying') is the final resolution or outcome of a story, after the climax."
    },
    {
        "question": "Complex Reading:\n\n'His argument was predicated on a specious assumption that crumbled under the slightest scrutiny, rendering his entire thesis untenable.'\n\nWhat does 'specious' mean?",
        "options": ["A) Valid", "B) Superficially plausible but false", "C) Well-reasoned", "D) Proven"],
        "answer": "B",
        "explanation": "'Specious' means superficially plausible but actually false. The assumption seemed reasonable but collapsed under scrutiny."
    },

    # ==================== SECTION 8: ALL TENSES IN CONTEXT (91-100) ====================
    {
        "question": "Tense Mastery:\n\n'By the time she arrives at the conference tomorrow, the keynote speaker ______ for over an hour.'",
        "options": ["A) will speak", "B) will have spoken", "C) will have been speaking", "D) speaks"],
        "answer": "C",
        "explanation": "Future Perfect Continuous emphasizes the duration of an action (for over an hour) that will be ongoing up to a future point."
    },
    {
        "question": "Tense Mastery:\n\n'I ______ to contact you several times last week, but your phone was constantly busy.'",
        "options": ["A) try", "B) have tried", "C) tried", "D) had tried"],
        "answer": "C",
        "explanation": "Past Simple for completed actions at a specific time (last week). The focus is on the action itself, not its present relevance."
    },
    {
        "question": "Tense Mastery:\n\n'For the past decade, the company ______ its market share steadily, but recent competition has reversed this trend.'",
        "options": ["A) increased", "B) has been increasing", "C) had increased", "D) was increasing"],
        "answer": "B",
        "explanation": "Present Perfect Continuous emphasizes the ongoing nature of the increase over the past decade until recently."
    },
    {
        "question": "Tense Mastery:\n\n'When I arrived at the station, I realized that I ______ my ticket at home.'",
        "options": ["A) left", "B) have left", "C) had left", "D) was leaving"],
        "answer": "C",
        "explanation": "Past Perfect for an action completed before another past action (realized). The leaving happened before the realization."
    },
    {
        "question": "Tense Mastery:\n\n'Next week at this time, we ______ on a beach in Thailand.'",
        "options": ["A) will relax", "B) will be relaxing", "C) relax", "D) are relaxing"],
        "answer": "B",
        "explanation": "Future Continuous describes an action that will be in progress at a specific future time (next week at this time)."
    },
    {
        "question": "Tense Mastery:\n\n'She ______ as a nurse for fifteen years before she decided to pursue medicine.'",
        "options": ["A) worked", "B) has worked", "C) had been working", "D) was working"],
        "answer": "C",
        "explanation": "Past Perfect Continuous emphasizes the duration (for fifteen years) of an action that happened before another past action (decided)."
    },
    {
        "question": "Tense Mastery:\n\n'This is the third time you ______ that excuse this week.'",
        "options": ["A) use", "B) used", "C) have used", "D) are using"],
        "answer": "C",
        "explanation": "'This is the + ordinal number + time' structure requires present perfect to emphasize repeated experiences up to now."
    },
    {
        "question": "Tense Mastery:\n\n'By 2030, experts predict that autonomous vehicles ______ conventional cars on our roads.'",
        "options": ["A) will replace", "B) will have replaced", "C) replace", "D) are replacing"],
        "answer": "B",
        "explanation": "Future Perfect for actions that will be completed by a specific future time (by 2030)."
    },
    {
        "question": "Tense Mastery:\n\n'I ______ to call you when you walked through the door.'",
        "options": ["A) was about", "B) am about", "C) have been about", "D) had about"],
        "answer": "A",
        "explanation": "'Was about to' expresses an action that was going to happen but was interrupted. Perfect for expressing near-past intention."
    },
    {
        "question": "Tense Mastery:\n\n'It's high time we ______ action on climate change before it's too late.'",
        "options": ["A) take", "B) took", "C) have taken", "D) are taking"],
        "answer": "B",
        "explanation": "'It's (high) time' is followed by past simple to express that something should be done now or in the immediate future."
    }
]

# ==================== BOT FUNCTIONS ====================

user_sessions = {}

def get_level(percentage):
    if percentage >= 95:
        return ("🏆 GRAND MASTER", "🌟 LEGENDARY! You're in the top 1% of English masters!")
    elif percentage >= 85:
        return ("🥇 ADVANCED EXPERT", "🎉 EXCELLENT! You've demonstrated superior mastery!")
    elif percentage >= 75:
        return ("🥈 PROFICIENT", "📚 VERY GOOD! You have strong command of advanced English!")
    elif percentage >= 65:
        return ("🥉 COMPETENT", "💪 GOOD EFFORT! You have solid skills!")
    elif percentage >= 50:
        return ("📘 INTERMEDIATE", "📖 KEEP PRACTICING! You're building a strong foundation!")
    else:
        return ("🌱 DEVELOPING", "🌟 EVERY MASTER WAS ONCE A BEGINNER! Review and try again!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "Unknown"
    
    user_sessions[user_id] = {"index": 0, "score": 0}
    
    logger.info(f"📱 User {username} ({user_id}) started the bot")
    
    await update.message.reply_text(
        "<b>🏆 PREMIUM ENGLISH MASTERY SUITE</b>\n\n"
        "<b>📚 100 Expert-Level Questions:</b>\n"
        "✓ Reading Passage Completion\n"
        "✓ Modal Auxiliaries in Conversations\n"
        "✓ All Conditionals (Zero-Mixed)\n"
        "✓ Reported Speech Mastery\n"
        "✓ Advanced Vocabulary in Context\n"
        "✓ Reading Comprehension\n"
        "✓ All Tenses Mastery\n\n"
        "<b>✨ Feature:</b>\n"
        "✓ Explanations auto-clear after 3 seconds\n"
        "✓ Clean, fast, and stable\n\n"
        "<b>🎯 Let's begin!</b>",
        parse_mode="HTML"
    )
    await send_question(update, context)

async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = user_sessions.get(user_id)
    
    if session and session["index"] < len(questions):
        idx = session["index"]
        q = questions[idx]
        
        keyboard = [[InlineKeyboardButton(opt, callback_data=opt[0])] for opt in q["options"]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        total_blocks = 10
        filled_blocks = int((idx / len(questions)) * total_blocks)
        progress = "█" * filled_blocks + "░" * (total_blocks - filled_blocks)
        percent_complete = (idx / len(questions)) * 100
        
        if idx < 15:
            section = "📖 Reading Completion"
        elif idx < 25:
            section = "💬 Modal Conversations"
        elif idx < 40:
            section = "🔄 Conditionals"
        elif idx < 50:
            section = "🗣️ Reported Speech"
        elif idx < 65:
            section = "📚 Advanced Vocabulary"
        elif idx < 90:
            section = "📖 Reading Comprehension"
        else:
            section = "⏰ Tense Mastery"
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"<b>{section}</b>\n"
                 f"<b>📝 Question {idx + 1}/{len(questions)}</b>\n"
                 f"<code>[{progress}]</code> <i>{percent_complete:.0f}% Complete</i>\n\n"
                 f"{q['question']}",
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
    else:
        score = session['score'] if session else 0
        percentage = (score / len(questions)) * 100
        level, feedback_msg = get_level(percentage)
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"<b>🏆 QUIZ COMPLETE!</b>\n\n"
                 f"📊 <b>Final Score:</b> {score}/{len(questions)}\n"
                 f"📈 <b>Percentage:</b> {percentage:.1f}%\n"
                 f"⭐ <b>Level:</b> {level}\n\n"
                 f"{feedback_msg}\n\n"
                 f"<i>Type /start to challenge yourself again! 🔄</i>",
            parse_mode="HTML"
        )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    
    if user_id not in user_sessions:
        return
    
    session = user_sessions[user_id]
    idx = session["index"]
    
    if idx >= len(questions):
        return
    
    user_choice = query.data
    q = questions[idx]
    
    # Store the message ID of the question message
    question_message_id = query.message.message_id
    
    if user_choice == q["answer"]:
        session["score"] += 1
        result_text = f"✅ <b>CORRECT!</b> 🎯\n\n"
    else:
        correct_letter = q["answer"]
        correct_text = next(opt for opt in q["options"] if opt.startswith(correct_letter))
        result_text = f"❌ <b>INCORRECT</b>\n\n<b>✓ Correct Answer:</b> {correct_text}\n\n"
    
    full_text = result_text + f"<b>📖 Explanation:</b>\n{q['explanation']}\n\n<i>⏰ Moving to next question in 2 seconds...</i>"
    
    # Edit the message to show the explanation
    await query.edit_message_text(
        text=full_text,
        parse_mode="HTML"
    )
    
    # Wait 2 seconds
    await asyncio.sleep(2)
    
    # Move to next question and send it
    session["index"] += 1
    await send_question(update, context)
    
    # After sending the new question, delete the old explanation message
    try:
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=question_message_id
        )
    except Exception as e:
        pass  # Message might already be gone

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    
    logger.info("=" * 70)
    logger.info("🤖 PREMIUM ENGLISH MASTERY BOT - FAST & STABLE")
    logger.info(f"📚 Total Questions: {len(questions)}")
    logger.info("✨ FEATURE: Explanations auto-clear after 2 seconds!")
    logger.info("=" * 70)
    logger.info("✅ Bot is running and waiting for messages...")
    
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"❌ Bot stopped: {e}")
        time.sleep(10)
