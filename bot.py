"""
Premium English Mastery Telegram Bot
100 Advanced Questions - GitHub Actions Deployment
"""

import logging
import os
import asyncio
import time
import sys
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ==================== CONFIGURATION ====================

BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    print("❌ BOT_TOKEN not found!")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== DATA STORAGE ====================

user_sessions = {}
user_preferences = {}
stats = {"total_users": 0, "total_questions": 0, "total_correct": 0, "start_time": time.strftime("%Y-%m-%d %H:%M:%S")}

# ==================== QUESTIONS ====================

questions = [
    # Section 1: Reading Completion (1-5)
    {
        "question": "The ancient manuscript, which ______ in a monastery for centuries, was finally discovered in 2019.",
        "options": ["A) had been hidden", "B) was hidden", "C) has been hidden", "D) is hidden"],
        "answer": "A",
        "explanation": "Past Perfect Passive - the hiding happened before discovery."
    },
    {
        "question": "By the time the rescue team arrived, the survivors ______ for over 48 hours.",
        "options": ["A) waited", "B) have been waiting", "C) had been waiting", "D) were waiting"],
        "answer": "C",
        "explanation": "Past Perfect Continuous - emphasizes duration before another past action."
    },
    {
        "question": "Currently, the new bridge ______, and it's expected to open next spring.",
        "options": ["A) is constructing", "B) is being constructed", "C) has constructed", "D) was constructed"],
        "answer": "B",
        "explanation": "Present Continuous Passive - ongoing action."
    },
    {
        "question": "By 2030, renewable energy ______ fossil fuels as the primary power source.",
        "options": ["A) will replace", "B) will have replaced", "C) replaces", "D) is replacing"],
        "answer": "B",
        "explanation": "Future Perfect - action completed by specific future time."
    },
    {
        "question": "Climate change, which ______ a global crisis for decades, requires immediate action.",
        "options": ["A) was", "B) had been", "C) has been", "D) is"],
        "answer": "C",
        "explanation": "Present Perfect - connects past to present."
    },
    
    # Section 2: Modal Verbs (6-10)
    {
        "question": "Someone's at the door. Who ______ it be at this hour?",
        "options": ["A) can", "B) must", "C) might", "D) should"],
        "answer": "A",
        "explanation": "'Can' expresses possibility in questions."
    },
    {
        "question": "I'm exhausted. I ______ have stayed up so late.",
        "options": ["A) shouldn't", "B) mustn't", "C) couldn't", "D) wouldn't"],
        "answer": "A",
        "explanation": "'Shouldn't have' expresses regret about a past action."
    },
    {
        "question": "Look at that car! It ______ have cost a fortune.",
        "options": ["A) can", "B) must", "C) might", "D) would"],
        "answer": "B",
        "explanation": "'Must have' for strong deduction about the past."
    },
    {
        "question": "You ______ borrow my car if you need it.",
        "options": ["A) can", "B) must", "C) should", "D) would"],
        "answer": "A",
        "explanation": "'Can' offers permission."
    },
    {
        "question": "You ______ be tired after that long flight.",
        "options": ["A) can", "B) must", "C) might", "D) should"],
        "answer": "B",
        "explanation": "'Must' for logical deduction."
    },
    
    # Section 3: Conditionals (11-15)
    {
        "question": "If you ______ water to 100°C, it boils.",
        "options": ["A) heat", "B) will heat", "C) heated", "D) had heated"],
        "answer": "A",
        "explanation": "Zero Conditional - scientific fact."
    },
    {
        "question": "If she ______ the exam, she will enter medical school.",
        "options": ["A) passes", "B) will pass", "C) passed", "D) had passed"],
        "answer": "A",
        "explanation": "First Conditional - real possibility."
    },
    {
        "question": "If I ______ you, I would take the job.",
        "options": ["A) am", "B) were", "C) was", "D) had been"],
        "answer": "B",
        "explanation": "Second Conditional - hypothetical present."
    },
    {
        "question": "If they ______ the warning, the accident wouldn't have happened.",
        "options": ["A) heeded", "B) had heeded", "C) have heeded", "D) would heed"],
        "answer": "B",
        "explanation": "Third Conditional - impossible past."
    },
    {
        "question": "If she ______ harder in college, she would have a better job now.",
        "options": ["A) studied", "B) had studied", "C) studies", "D) would study"],
        "answer": "B",
        "explanation": "Mixed Conditional - past condition affects present."
    },
    
    # Section 4: Reported Speech (16-20)
    {
        "question": "She said, 'I will finish the project.' → She said that she ______ the project.",
        "options": ["A) will finish", "B) would finish", "C) finishes", "D) finished"],
        "answer": "B",
        "explanation": "'Will' changes to 'would' in reported speech."
    },
    {
        "question": "He asked, 'Where do you live?' → He asked where I ______.",
        "options": ["A) live", "B) lived", "C) had lived", "D) was living"],
        "answer": "B",
        "explanation": "Present Simple changes to Past Simple."
    },
    {
        "question": "The teacher said, 'Don't talk.' → The teacher told us ______.",
        "options": ["A) not to talk", "B) to not talk", "C) don't talk", "D) didn't talk"],
        "answer": "A",
        "explanation": "Negative commands use 'not to + infinitive'."
    },
    {
        "question": "She said, 'I'll see you tomorrow.' → She said she would see me ______.",
        "options": ["A) tomorrow", "B) the next day", "C) on tomorrow", "D) yesterday"],
        "answer": "B",
        "explanation": "'Tomorrow' changes to 'the next day'."
    },
    {
        "question": "The teacher said, 'The Earth orbits the Sun.' → The teacher said the Earth ______ the Sun.",
        "options": ["A) orbited", "B) orbits", "C) had orbited", "D) was orbiting"],
        "answer": "B",
        "explanation": "Universal truths don't change tense."
    },
    
    # Section 5: Vocabulary (21-25)
    {
        "question": "The CEO's ______ speech inspired the entire company.",
        "options": ["A) lackluster", "B) mundane", "C) rousing", "D) tedious"],
        "answer": "C",
        "explanation": "'Rousing' means exciting and inspiring."
    },
    {
        "question": "Despite their ______ differences, they reached an agreement.",
        "options": ["A) trivial", "B) profound", "C) superficial", "D) negligible"],
        "answer": "B",
        "explanation": "'Profound' means deep and significant."
    },
    {
        "question": "The investigation was ______ by missing evidence.",
        "options": ["A) facilitated", "B) expedited", "C) hampered", "D) accelerated"],
        "answer": "C",
        "explanation": "'Hampered' means hindered or obstructed."
    },
    {
        "question": "Her argument was so ______ that everyone agreed.",
        "options": ["A) tenuous", "B) flimsy", "C) compelling", "D) weak"],
        "answer": "C",
        "explanation": "'Compelling' means convincing and persuasive."
    },
    {
        "question": "The company's ______ growth attracted global investors.",
        "options": ["A) stagnant", "B) meteoric", "C) gradual", "D) modest"],
        "answer": "B",
        "explanation": "'Meteoric' means rapid and spectacular."
    },
    
    # Section 6: Reading Comprehension (26-30)
    {
        "question": "'The company's fortunes remained inextricably linked to the oil market.' What does 'inextricably linked' mean?",
        "options": ["A) Completely separated", "B) Unavoidably connected", "C) Temporarily associated", "D) Superficially related"],
        "answer": "B",
        "explanation": "'Inextricably linked' means impossible to separate."
    },
    {
        "question": "'The policy was met with a groundswell of opposition.' What does 'groundswell' mean?",
        "options": ["A) Minor opposition", "B) Rapidly growing movement", "C) Organized by management", "D) Temporary opposition"],
        "answer": "B",
        "explanation": "'Groundswell' refers to a rapidly growing grassroots movement."
    },
    {
        "question": "'The CEO's resignation precipitated a cascade of departures.' What does 'precipitated' mean?",
        "options": ["A) Prevented", "B) Delayed", "C) Caused suddenly", "D) Ignored"],
        "answer": "C",
        "explanation": "'Precipitated' means causing something to happen suddenly."
    },
    {
        "question": "'She held the audience spellbound.' What does 'spellbound' mean?",
        "options": ["A) Bored", "B) Confused", "C) Captivated", "D) Angry"],
        "answer": "C",
        "explanation": "'Spellbound' means completely captivated."
    },
    {
        "question": "'His argument was replete with fallacies.' What does 'replete with' mean?",
        "options": ["A) Lacked", "B) Filled with", "C) Few", "D) Ignored"],
        "answer": "B",
        "explanation": "'Replete with' means full of."
    }
]

TOTAL_QUESTIONS = len(questions)
logger.info(f"📚 Loaded {TOTAL_QUESTIONS} questions")

# ==================== HELPER FUNCTIONS ====================

def get_category(index):
    if index < 5: return "📖 Reading Completion"
    elif index < 10: return "💬 Modal Verbs"
    elif index < 15: return "🔄 Conditionals"
    elif index < 20: return "🗣️ Reported Speech"
    elif index < 25: return "📚 Vocabulary"
    else: return "📖 Reading Comprehension"

def get_progress_bar(current, total, width=10):
    filled = int((current / total) * width)
    return "█" * filled + "░" * (width - filled)

def get_level(percentage):
    if percentage >= 90: return "🏆 MASTER"
    elif percentage >= 70: return "🥇 ADVANCED"
    elif percentage >= 50: return "🥈 INTERMEDIATE"
    else: return "🌱 BEGINNER"

# ==================== HANDLERS ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "Unknown"
    
    user_sessions[user_id] = {"index": 0, "score": 0}
    if user_id not in user_preferences:
        user_preferences[user_id] = {"show_explanations": True}
    
    stats["total_users"] = len(user_sessions)
    
    logger.info(f"📱 User {username} ({user_id}) started the bot")
    
    show_exp = user_preferences[user_id]["show_explanations"]
    
    await update.message.reply_text(
        f"<b>🏆 PREMIUM ENGLISH MASTERY</b>\n\n"
        f"<b>📚 {TOTAL_QUESTIONS} Questions</b>\n"
        f"✓ Reading Completion\n"
        f"✓ Modal Verbs\n"
        f"✓ Conditionals\n"
        f"✓ Reported Speech\n"
        f"✓ Vocabulary\n"
        f"✓ Reading Comprehension\n\n"
        f"<b>⚙️ Settings:</b>\n"
        f"• Explanations: {'✅ ON' if show_exp else '❌ OFF'}\n\n"
        f"<b>🎯 Type /stats to see global statistics!</b>",
        parse_mode="HTML"
    )
    await send_question(update, context)

async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = user_sessions.get(user_id)
    
    if not session or session["index"] >= TOTAL_QUESTIONS:
        score = session.get("score", 0) if session else 0
        percentage = (score / TOTAL_QUESTIONS) * 100
        level = get_level(percentage)
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"<b>🏆 QUIZ COMPLETE!</b>\n\n"
                 f"📊 <b>Score:</b> {score}/{TOTAL_QUESTIONS}\n"
                 f"📈 <b>Percentage:</b> {percentage:.1f}%\n"
                 f"⭐ <b>Level:</b> {level}\n\n"
                 f"<i>Type /start to try again!</i>",
            parse_mode="HTML"
        )
        return
    
    idx = session["index"]
    q = questions[idx]
    
    keyboard = [[InlineKeyboardButton(opt, callback_data=opt[0])] for opt in q["options"]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    progress = get_progress_bar(idx, TOTAL_QUESTIONS)
    percent = (idx / TOTAL_QUESTIONS) * 100
    category = get_category(idx)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"<b>{category}</b>\n"
             f"<b>📝 Question {idx + 1}/{TOTAL_QUESTIONS}</b>\n"
             f"<code>[{progress}]</code> <i>{percent:.0f}% Complete</i>\n\n"
             f"{q['question']}",
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    
    session = user_sessions.get(user_id)
    if not session:
        return
    
    idx = session["index"]
    if idx >= TOTAL_QUESTIONS:
        return
    
    user_choice = query.data
    q = questions[idx]
    
    # Disable buttons immediately
    try:
        await query.edit_message_reply_markup(reply_markup=None)
    except:
        pass
    
    # Update stats
    stats["total_questions"] += 1
    
    # Check answer
    if user_choice == q["answer"]:
        session["score"] += 1
        stats["total_correct"] += 1
        result_text = "✅ <b>CORRECT!</b> 🎯\n\n"
    else:
        correct_text = next(opt for opt in q["options"] if opt.startswith(q["answer"]))
        result_text = f"❌ <b>INCORRECT</b>\n\n<b>✓ Correct Answer:</b> {correct_text}\n\n"
    
    # Show explanation
    show_exp = user_preferences.get(user_id, {}).get("show_explanations", True)
    
    if show_exp:
        text = result_text + f"<b>📖 Explanation:</b>\n{q['explanation']}\n\n<i>⚡ Next question in 2 seconds...</i>"
    else:
        text = result_text + f"<i>⚡ Next question in 2 seconds...</i>"
    
    msg = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode="HTML"
    )
    
    # Wait 2 seconds
    await asyncio.sleep(2)
    
    # Move to next question
    session["index"] += 1
    await send_question(update, context)
    
    # Delete explanation message
    if show_exp:
        try:
            await msg.delete()
        except:
            pass

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    accuracy = (stats["total_correct"] / stats["total_questions"] * 100) if stats["total_questions"] > 0 else 0
    
    await update.message.reply_text(
        f"<b>📊 GLOBAL STATISTICS</b>\n\n"
        f"👥 Total Users: {stats['total_users']}\n"
        f"📝 Questions Answered: {stats['total_questions']}\n"
        f"✅ Correct Answers: {stats['total_correct']}\n"
        f"📈 Global Accuracy: {accuracy:.1f}%\n"
        f"🚀 Started: {stats['start_time']}\n\n"
        f"<i>Type /start to begin your journey!</i>",
        parse_mode="HTML"
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check if bot is alive"""
    await update.message.reply_text(
        f"🏓 Pong!\n\n"
        f"🟢 Status: Online\n"
        f"📊 Users: {stats['total_users']}\n"
        f"🕐 Time: {time.strftime('%H:%M:%S')}\n"
        f"🎯 Bot is running smoothly!",
        parse_mode="HTML"
    )

# ==================== MAIN ====================

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CallbackQueryHandler(handle_callback))
    
    logger.info("=" * 50)
    logger.info("🤖 PREMIUM ENGLISH MASTERY BOT")
    logger.info(f"📚 Total Questions: {TOTAL_QUESTIONS}")
    logger.info("✅ Bot is running on GitHub Actions...")
    logger.info("=" * 50)
    
    app.run_polling()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"❌ Bot stopped: {e}")
        time.sleep(10)
