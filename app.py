"""
Matches Results Forecasting
Manual-input Rule-Based Expert System for football match prediction.
This app uses a knowledge base of weighted rules and inputs provided directly by the user.
"""

import streamlit as st
import plotly.graph_objects as go
from expert_system import ExpertSystem, HeadToHeadSummary, TeamProfile, MatchResult

PAGE_CONFIG = {
    "page_title": "Matches Results Forecasting",
    "page_icon": "⚽",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

COMPETITIONS_TEAMS = {
    "English Premier League": [
        "Arsenal",
        "Aston Villa",
        "Bournemouth",
        "Brentford",
        "Brighton",
        "Burnley",
        "Chelsea",
        "Crystal Palace",
        "Everton",
        "Fulham",
        "Liverpool",
        "Luton Town",
        "Manchester City",
        "Manchester United",
        "Newcastle United",
        "Nottingham Forest",
        "Sheffield United",
        "Tottenham Hotspur",
        "West Ham United",
        "Wolverhampton Wanderers",
    ],
    "Spanish La Liga": [
        "Alaves",
        "Almeria",
        "Athletic Bilbao",
        "Atletico Madrid",
        "Barcelona",
        "Cadiz",
        "Celta Vigo",
        "Getafe",
        "Girona",
        "Granada",
        "Las Palmas",
        "Mallorca",
        "Osasuna",
        "Rayo Vallecano",
        "Real Betis",
        "Real Madrid",
        "Real Sociedad",
        "Sevilla",
        "Valencia",
        "Villarreal",
    ],
    "German Bundesliga": [
        "Augsburg",
        "Bayer Leverkusen",
        "Bayern Munich",
        "Bochum",
        "Borussia Dortmund",
        "Borussia Monchengladbach",
        "Darmstadt",
        "Eintracht Frankfurt",
        "Freiburg",
        "Heidenheim",
        "Hoffenheim",
        "Koln",
        "Mainz",
        "RB Leipzig",
        "Stuttgart",
        "Union Berlin",
        "Werder Bremen",
        "Wolfsburg",
        "Schalke 04",
        "Hamburg",
    ],
    "Italian Serie A": [
        "Atalanta",
        "Bologna",
        "Cagliari",
        "Empoli",
        "Fiorentina",
        "Frosinone",
        "Genoa",
        "Inter Milan",
        "Juventus",
        "Lazio",
        "Lecce",
        "AC Milan",
        "Monza",
        "Napoli",
        "Roma",
        "Salernitana",
        "Sassuolo",
        "Torino",
        "Udinese",
        "Verona",
    ],
    "French Ligue 1": [
        "Brest",
        "Clermont Foot",
        "Le Havre",
        "Lens",
        "Lille",
        "Lorient",
        "Lyon",
        "Marseille",
        "Metz",
        "Monaco",
        "Montpellier",
        "Nantes",
        "Nice",
        "Paris Saint-Germain",
        "Reims",
        "Rennes",
        "Strasbourg",
        "Toulouse",
        "Auxerre",
        "Saint-Etienne",
    ],
    "UEFA Champions League": [
        "Ajax",
        "PSV Eindhoven",
        "Club Brugge",
        "Borussia Dortmund",
        "Bayer Leverkusen",
        "Bayern Munich",
        "Paris Saint-Germain",
        "Marseille",
        "Monaco",
        "Lyon",
        "Inter Milan",
        "AC Milan",
        "Juventus",
        "Roma",
        "Atalanta",
        "Napoli",
        "Real Madrid",
        "Atletico Madrid",
        "Barcelona",
        "Real Betis",
        "Villarreal",
        "Olympiacos",
        "Tottenham Hotspur",
        "Manchester City",
        "Manchester United",
        "Liverpool",
        "Arsenal",
        "Chelsea",
        "Newcastle United",
        "Aston Villa",
    ],
}

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
body, .streamlit-expanderHeader, .css-18e3th9 { font-family: 'Inter', sans-serif; }
h1, h2, h3, h4, h5 { font-weight: 700; }
.section-box { background: #ffffff; border-radius: 14px; padding: 20px; box-shadow: 0 16px 40px rgba(38, 78, 118, 0.08); margin-bottom: 20px; }
.card-highlight { background: linear-gradient(135deg, #304ffe 0%, #1de9b6 100%); color: white; border-radius: 16px; padding: 24px; }
.rule-card { background: #f8fbff; border: 1px solid #d9e8ff; border-radius: 12px; padding: 16px; margin-bottom: 14px; }
.rule-header { font-weight: 700; margin-bottom: 8px; }
.rule-meta { color: #617d98; font-size: 13px; margin-bottom: 12px; }
.summary-box { background: #ffffff; border: 1px solid #e8eef4; border-radius: 14px; padding: 20px; }
</style>
"""


def get_teams_for_competition(competition: str) -> list:
    return COMPETITIONS_TEAMS.get(competition, [])


def get_prediction_display_name(result: MatchResult, home_name: str, away_name: str) -> str:
    if result == MatchResult.HOME_WIN:
        return home_name
    if result == MatchResult.AWAY_WIN:
        return away_name
    return "Draw"


def initialize_session_state():
    if "competition" not in st.session_state:
        st.session_state.competition = "English Premier League"

    teams = get_teams_for_competition(st.session_state.competition)

    if "home_team" not in st.session_state or st.session_state.home_team not in teams:
        st.session_state.home_team = teams[0] if teams else ""

    if "away_team" not in st.session_state or st.session_state.away_team not in teams or st.session_state.away_team == st.session_state.home_team:
        valid_away = [team for team in teams if team != st.session_state.home_team]
        st.session_state.away_team = valid_away[0] if valid_away else teams[1] if len(teams) > 1 else teams[0] if teams else ""

    if "prediction" not in st.session_state:
        st.session_state.prediction = None


def render_header():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-box" style="background: linear-gradient(135deg, #2c54ff, #00c0ff); color: white;">
            <h1>Matches Results Forecasting</h1>
            <p style="font-size: 16px; margin-top: 10px; line-height: 1.6;">
                Manual entry Rule-Based Expert System for football match prediction. No CSV, no datasets, no machine learning.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def collect_recent_form(prefix: str) -> list:
    form = []
    cols = st.columns(5)
    for index, col in enumerate(cols):
        with col:
            form.append(st.selectbox(f"Match {index + 1}", ["W", "D", "L"], key=f"{prefix}_form_{index}"))
    return form


def collect_team_profile(prefix: str, title: str, selected_name: str, position_label: str, is_home: bool) -> TeamProfile:
    st.subheader(title)
    st.markdown(f"**Team:** {selected_name}")
    league_position = st.number_input(position_label, min_value=1, max_value=20, value=10, step=1, key=f"{prefix}_league_position")
    st.markdown("**Recent Form (last 5 matches)**")
    recent_form = collect_recent_form(prefix)
    goals_scored_avg = st.number_input("Average Goals Scored", min_value=0.0, max_value=5.0, value=1.5, step=0.1, key=f"{prefix}_scored")
    goals_conceded_avg = st.number_input("Average Goals Conceded", min_value=0.0, max_value=5.0, value=1.2, step=0.1, key=f"{prefix}_conceded")
    strength_label = "Home Strength" if is_home else "Away Strength"
    strength = st.slider(strength_label, min_value=1, max_value=10, value=6, key=f"{prefix}_strength")
    injuries = st.number_input("Injuries / Absences", min_value=0, max_value=10, value=1, step=1, key=f"{prefix}_injuries")
    motivation = st.slider("Motivation Level", min_value=1, max_value=10, value=6, key=f"{prefix}_motivation")

    return TeamProfile(
        name=selected_name,
        league_position=league_position,
        recent_form=recent_form,
        goals_scored_avg=goals_scored_avg,
        goals_conceded_avg=goals_conceded_avg,
        strength=strength,
        injuries=injuries,
        motivation=motivation,
    )


def render_head_to_head_section() -> HeadToHeadSummary:
    st.subheader("Head-to-Head History")
    cols = st.columns(3)
    with cols[0]:
        home_wins = st.number_input("Home team wins", min_value=0, max_value=20, value=0, step=1, key="h2h_home_wins")
    with cols[1]:
        draws = st.number_input("Draws", min_value=0, max_value=20, value=0, step=1, key="h2h_draws")
    with cols[2]:
        away_wins = st.number_input("Away team wins", min_value=0, max_value=20, value=0, step=1, key="h2h_away_wins")
    return HeadToHeadSummary(home_wins=home_wins, draws=draws, away_wins=away_wins)


def validate_profiles(home: TeamProfile, away: TeamProfile, competition: str) -> str:
    if not competition:
        return "Please select a competition."
    if not home.name:
        return "Please select the home team."
    if not away.name:
        return "Please select the away team."
    if home.name == away.name:
        return "Home and away team names must be different."
    teams = get_teams_for_competition(competition)
    if home.name not in teams or away.name not in teams:
        return "Both teams must belong to the selected competition."
    return ""


def render_prediction_section():
    st.markdown(
        """
        <div class="section-box">
            <h2>Manual Match Input</h2>
            <p>Enter all match details directly. The system uses a knowledge base of weighted rules to produce a prediction.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Competition and Team Selection outside the form
    competition = st.selectbox(
        "Competition",
        options=list(COMPETITIONS_TEAMS.keys()),
        index=list(COMPETITIONS_TEAMS.keys()).index(st.session_state.competition),
        key="competition",
    )

    st.markdown(
        "<div style='padding: 10px 0; color: #33475b;'>"
        "The selected competition affects the available team names only. The prediction still depends on the manually entered expert system inputs."
        "</div>",
        unsafe_allow_html=True,
    )

    teams = get_teams_for_competition(competition)
    home_team = st.selectbox("Home Team", options=teams, index=teams.index(st.session_state.home_team) if st.session_state.home_team in teams else 0, key="home_team")

    away_options = [team for team in teams if team != home_team]
    away_team = st.selectbox(
        "Away Team",
        options=away_options,
        index=away_options.index(st.session_state.away_team) if st.session_state.away_team in away_options else 0,
        key="away_team",
    )

    # Manual inputs inside the form
    with st.form("match_form"):
        if competition == "UEFA Champions League":
            position_label = "Competition Ranking / Seed"
        else:
            position_label = "League Position"

        col1, col2 = st.columns(2)
        with col1:
            home_profile = collect_team_profile(
                "home",
                "Home Team Inputs",
                home_team,
                position_label,
                is_home=True,
            )
        with col2:
            away_profile = collect_team_profile(
                "away",
                "Away Team Inputs",
                away_team,
                position_label,
                is_home=False,
            )

        h2h_summary = render_head_to_head_section()
        submit = st.form_submit_button("🔮 Predict Match")

    if submit:
        error_message = validate_profiles(home_profile, away_profile, competition)
        if error_message:
            st.error(error_message)
            return
        expert_system = ExpertSystem()
        prediction = expert_system.predict(home_profile, away_profile, h2h_summary)
        st.session_state.prediction = {
            "prediction": prediction,
            "competition": competition,
            "home": home_profile,
            "away": away_profile,
            "h2h": h2h_summary,
        }

    if st.session_state.prediction:
        render_prediction_results()


def render_prediction_results():
    prediction = st.session_state.prediction["prediction"]
    result_icons = {
        MatchResult.HOME_WIN: "🏠",
        MatchResult.DRAW: "⚖️",
        MatchResult.AWAY_WIN: "✈️",
    }

    home_name = st.session_state.prediction["home"].name
    away_name = st.session_state.prediction["away"].name
    result_display = get_prediction_display_name(prediction.result, home_name, away_name)
    scoreline_display = f"{home_name} {prediction.expected_home_goals} - {prediction.expected_away_goals} {away_name}"

    st.markdown(
        f"""
        <div class="section-box">
            <div class="card-highlight">
                <h2>Prediction Result</h2>
                <p style="font-size: 18px; margin-top: 8px;">{result_icons[prediction.result]}</p>
                <p style="font-size: 24px; font-weight: 700; margin: 12px 0;">{result_display}</p>
                <p style="font-size: 18px;">Expected score: {scoreline_display}</p>
                <p style="font-size: 16px;">Confidence: {prediction.confidence:.1f}%</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    fig = go.Figure(
        data=[
            go.Bar(
                x=["Home Win", "Draw", "Away Win"],
                y=[prediction.prob_home * 100, prediction.prob_draw * 100, prediction.prob_away * 100],
                marker_color=["#1c7dff", "#f4b400", "#d32f2f"],
                text=[f"{prediction.prob_home*100:.1f}%", f"{prediction.prob_draw*100:.1f}%", f"{prediction.prob_away*100:.1f}%"],
                textposition="auto",
            )
        ]
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        yaxis_title="Probability (%)",
        xaxis_title="Result",
        template="plotly_white",
        height=320,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Rule Explanations")
    for evaluation in prediction.rule_evaluations:
        st.markdown(
            f"""
            <div class="rule-card">
                <div class="rule-header">{evaluation.rule_name} — Weight {evaluation.weight * 100:.0f}%</div>
                <div class="rule-meta">Condition: {evaluation.condition}</div>
                <div>{evaluation.explanation}</div>
                <div class="rule-meta">Probabilities: Home {evaluation.prob_home*100:.0f}% • Draw {evaluation.prob_draw*100:.0f}% • Away {evaluation.prob_away*100:.0f}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Prediction Summary")
    st.text(prediction.summary)


def render_education_section():
    st.markdown("---")
    with st.expander("🧠 What is an Expert System?", expanded=False):
        st.write(
            "An expert system is a knowledge-driven application that uses a set of rules to reach a conclusion. "
            "This app models football match forecasting through a clearly defined rule base and manual inputs."
        )
    with st.expander("📚 Knowledge Base and Inference Engine", expanded=False):
        st.write(
            "The knowledge base is the collection of rules, each with a name, weight, condition, and explanation. "
            "The inference engine evaluates all rules and combines their weighted probabilities into a final result."
        )
    with st.expander("⚖️ Why this is NOT Machine Learning", expanded=False):
        st.write(
            "This application does not learn from data. It is deterministic and explainable, using explicit domain rules only."
        )
    with st.expander("🧾 Technical Report Support", expanded=False):
        st.markdown(
            "### Architecture\n"
            "1. User provides match factors manually.\n"
            "2. Each rule evaluates those factors and emits a probability distribution.\n"
            "3. Weighted probabilities are combined into a final prediction.\n"
            "4. The highest-probability outcome is selected as the forecast.\n\n"
            "### Rule Structure\n"
            "Every rule includes a weight, a human-readable condition, and a short explanation.\n\n"
            "### Example Scenarios\n"
            "- Strong home form, superior league position, and fewer injuries tends to favor a Home Win.\n"
            "- Very balanced teams with similar metrics and head-to-head history often produce a Draw.\n"
            "- High away motivation, strong away strength, and weak home defense can push toward an Away Win.\n"
        )


def main():
    st.set_page_config(**PAGE_CONFIG)
    initialize_session_state()
    render_header()
    render_prediction_section()
    render_education_section()


if __name__ == "__main__":
    main()
