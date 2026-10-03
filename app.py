import csv
import os
import random
from datetime import datetime

import streamlit as st

st.set_page_config(page_title="5-Minute Self Check", page_icon="🪞", layout="centered")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stFooter"] {display: none;}
    [data-testid="stStatusWidget"] {visibility: hidden;}
    [data-testid="stAppViewBlockContainer"] {padding-top: 0;}
    a[href*="streamlit.io"] {display: none;}
</style>
""", unsafe_allow_html=True)

G, P, I = "Goodness", "Passion", "Ignorance"
CSV_FILE = "responses.csv"

# ---------------------------------------------------------------------------
# Scored questions: (label, [(option text, guna), ...])
# Edit the option texts / mapping freely to match your session material.
# ---------------------------------------------------------------------------
QUESTIONS = [
    ("Speech", [
        ("Calm, gentle and beneficial to others", G),
        ("Fast, loud or aimed at impressing people", P),
        ("Harsh, careless or hurtful", I)]),
    ("Cleaning Surroundings", [
        ("I keep my space clean daily, happily", G),
        ("I clean only when guests are coming or I'm in the mood", P),
        ("I leave it messy and avoid cleaning", I)]),
    ("Work", [
        ("I do my duty without being attached to results", G),
        ("I work hard mainly for recognition and rewards", P),
        ("I delay, avoid or do it carelessly", I)]),
    ("Anger", [
        ("Rarely angry; I calm down quickly", G),
        ("Often irritated when things don't go my way", P),
        ("Gets intense, long-lasting or leads to confusion", I)]),
    ("I forgive", [
        ("Easily and sincerely", G),
        ("Only if I get something in return, like an apology", P),
        ("Rarely; I hold grudges", I)]),
    ("I speak the truth", [
        ("Always, even when it is difficult", G),
        ("When it suits me", P),
        ("I often hide or twist facts", I)]),
    ("General mindset", [
        ("Peaceful, positive and content", G),
        ("Restless, ambitious and always wanting more", P),
        ("Dull, confused or negative", I)]),
    ("I wash clothes", [
        ("Regularly, I like fresh and clean clothes", G),
        ("Only when I need to impress or go out", P),
        ("Late, only when absolutely necessary", I)]),
    ("Food Likings", [
        ("Fresh, simple, wholesome food", G),
        ("Spicy, salty, sour or very hot food", P),
        ("Stale, oily, heavy or leftover food", I)]),
    ("I like to", [
        ("Learn, reflect and serve others", G),
        ("Compete, achieve and be seen", P),
        ("Sleep, laze around or escape reality", I)]),
    ("Eating habits", [
        ("Regular times, moderate portions", G),
        ("Rushed, irregular, eating for taste", P),
        ("Overeating or eating when not hungry", I)]),
    ("While getting up from bed in the morning", [
        ("I wake up early, fresh and grateful", G),
        ("I wake up with a rush of thoughts and to-dos", P),
        ("I snooze repeatedly and feel heavy", I)]),
    ("On a chill Sunday, what would you do?", [
        ("Read, spend time in nature or do something uplifting", G),
        ("Go out, shop, party or plan the next big thing", P),
        ("Sleep all day or binge-watch for hours", I)]),
    ("When will you prepare for exams?", [
        ("Steadily, well in advance", G),
        ("In intense bursts, a few days before", P),
        ("The night before, or not at all", I)]),
    ("Hairstyle", [
        ("Simple, neat and practical", G),
        ("Trendy, stylish and attention-seeking", P),
        ("Untidy, neglected or careless", I)]),
    ("Approach towards life", [
        ("Purposeful and service-oriented", G),
        ("Achievement and enjoyment oriented", P),
        ("Go with the flow, with no real direction", I)]),
    ("Controlling one's mind and emotions", [
        ("I can usually stay balanced", G),
        ("I can for a while, but it takes effort", P),
        ("I get overwhelmed and struggle to control it", I)]),
    ("Nature while conversing with others", [
        ("Respectful, a good listener", G),
        ("Dominating, wanting to prove a point", P),
        ("Disinterested, sarcastic or rude", I)]),
    ("When I feel out of control", [
        ("I pause, reflect and seek guidance", G),
        ("I get more active and push harder", P),
        ("I withdraw, sleep or numb myself", I)]),
    ("I feel interested in searching and asking basic questions about life and also about the next life.", [
        ("Yes, very much", G),
        ("Sometimes, when I have time", P),
        ("Not really", I)]),
    ("Studying the Holy Scriptures", [
        ("I study regularly and enjoy it", G),
        ("Occasionally, mostly out of curiosity or duty", P),
        ("Hardly ever, it feels boring", I)]),
    ("It is pleasing to me to pray and I feel calm after doing so.", [
        ("Strongly agree", G),
        ("Sometimes", P),
        ("Not really", I)]),
]

SLEEP_OPTIONS = [("6-8 hrs", G), ("less than 5 hrs", P), ("more than 8 hrs", I)]


# Shuffle option order once per session so the 'good' option isn't always first
if "order" not in st.session_state:
    rng = random.Random()
    st.session_state.order = {
        i: rng.sample(range(3), 3) for i in range(len(QUESTIONS))
    }

st.title("The 5-Minute Self Check 🪞")
st.subheader("A Mirror of Your Everyday Choices")
st.write(
    "How do your everyday choices reflect your state of mind? Take a few minutes "
    "to reflect on your habits, thoughts, reactions, and choices.\n\n"
    "There are no right or wrong answers, just choose what honestly describes you. "
    "**Be honest. Be curious. Look within.** 🙏"
)
st.caption("* Required")

with st.form("self_check"):
    email = st.text_input("Email *")
    name = st.text_input("Name *")
    department = st.text_input("Department *")

    st.markdown("---")
    sleep_choice = st.radio("Total sleep in a day *",
                            [t for t, _ in SLEEP_OPTIONS], index=None)
    sleep_guna = next((g for t, g in SLEEP_OPTIONS if t == sleep_choice), None)
    answers = {}
    for idx, (label, options) in enumerate(QUESTIONS):
        shuffled = [options[j] for j in st.session_state.order[idx]]
        texts = [t for t, _ in shuffled]
        choice = st.radio(f"{label} *", texts, index=None, key=f"q{idx}")
        answers[idx] = next((g for t, g in shuffled if t == choice), None)

    st.markdown("---")
    rating = st.slider("Please rate the session on the scale of 1-10 (10 being the highest)",
                       min_value=1, max_value=10, value=10)
    liked = st.text_area("Share a few points from today's session that you liked or found meaningful *")
    more = st.radio("Would you like to attend more sessions like this? *",
                    ["Yes", "Maybe"], index=None, horizontal=True)
    comments = st.text_area("Any comments or suggestions?")

    submitted = st.form_submit_button("Submit")

if submitted:
    errors = []
    if not email.strip() or "@" not in email:
        errors.append("a valid email")
    if not name.strip():
        errors.append("your name")
    if not department.strip():
        errors.append("your department")
    unanswered = [QUESTIONS[i][0] for i, g in answers.items() if g is None]
    if unanswered:
        errors.append(f"{len(unanswered)} unanswered question(s)")
    if not liked.strip():
        errors.append("what you liked from the session")
    if sleep_guna is None:
        errors.append("your total sleep")
    if more is None:
        errors.append("whether you'd like to attend more sessions")

    if errors:
        st.error("Please complete: " + ", ".join(errors) + ".")
        if unanswered:
            with st.expander("Unanswered questions"):
                for q in unanswered:
                    st.write("• " + q)
    else:
        gunas = [sleep_guna] + list(answers.values())
        total = len(gunas)
        pct = {k: round(100 * gunas.count(k) / total, 1) for k in (G, P, I)}

        st.success(f"Thank you, {name}! Here is your reflection 🙏")
        c1, c2, c3 = st.columns(3)
        c1.metric("Goodness 🌿", f"{pct[G]}%")
        c2.metric("Passion 🔥", f"{pct[P]}%")
        c3.metric("Ignorance 🌑", f"{pct[I]}%")

        for k in (G, P, I):
            st.write(f"**{k}**")
            st.progress(int(pct[k]))

        st.bar_chart({"Percentage": pct})

        dominant = max(pct, key=pct.get)
        messages = {
            G: "Your choices lean towards clarity, balance and calmness. Keep nurturing it.",
            P: "Your choices lean towards activity, ambition and restlessness. "
               "Try adding moments of stillness.",
            I: "Your choices lean towards inertia or confusion. Small, consistent "
               "steps like waking early, eating fresh food and prayer can help.",
        }
        st.info(f"**Dominant quality: {dominant}.** {messages[dominant]}")
        st.caption("This is a reflective exercise, not a diagnosis.")

        # Save the response
        row = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "email": email, "name": name, "department": department,
            "sleep": sleep_choice,
            **{f"q{i+1}_{QUESTIONS[i][0][:30]}": g for i, g in answers.items()},
            "session_rating": rating, "liked": liked, "more_sessions": more, "comments": comments,
            "goodness_pct": pct[G], "passion_pct": pct[P], "ignorance_pct": pct[I],
        }
        new_file = not os.path.exists(CSV_FILE)
        with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(row.keys()))
            if new_file:
                w.writeheader()
            w.writerow(row)

        # Email each response if secrets are configured
        if "email" in st.secrets:
            import smtplib
            from email.message import EmailMessage
            try:
                msg = EmailMessage()
                body = "\n".join(f"{k}: {v}" for k, v in row.items())
                msg.set_content(body)
                msg["Subject"] = f"GPI response - {name}"
                msg["From"] = st.secrets["email"]["sender"]
                msg["To"] = st.secrets["email"]["to"]
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login(st.secrets["email"]["sender"],
                               st.secrets["email"]["password"])
                    smtp.send_message(msg)
            except Exception as e:
                st.warning(f"Could not email the response: {e}")

        # Persist to Google Sheets if secrets are configured
        if "gspread" in st.secrets:
            import gspread
            gc = gspread.service_account_from_dict(st.secrets["gspread"])
            sh = gc.open(st.secrets["gspread"]["sheet_name"])
            try:
                ws = sh.sheet1
                ws.append_row([row[k] for k in list(row.keys())])
            except Exception:
                pass
