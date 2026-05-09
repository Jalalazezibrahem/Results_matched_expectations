"""
Manual Rule-Based Expert System for Football Match Result Forecasting
This module defines the knowledge base, inference engine, and score estimation
using only user-provided inputs.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class MatchResult(Enum):
    """Possible match outcomes."""
    HOME_WIN = "Home Win"
    DRAW = "Draw"
    AWAY_WIN = "Away Win"


@dataclass
class TeamProfile:
    """Manual team profile input from the user."""
    name: str
    league_position: int
    recent_form: List[str]
    goals_scored_avg: float
    goals_conceded_avg: float
    strength: int
    injuries: int
    motivation: int

    def form_score(self) -> int:
        """Convert the last five results to a numeric form score."""
        return sum(3 if result == "W" else 1 if result == "D" else 0 for result in self.recent_form)

    def form_summary(self) -> str:
        """Return a compact representation of recent form."""
        return "".join(self.recent_form)


@dataclass
class HeadToHeadSummary:
    """Head-to-head summary data provided by the user."""
    home_wins: int
    draws: int
    away_wins: int

    @property
    def total_matches(self) -> int:
        return self.home_wins + self.draws + self.away_wins

    @property
    def home_win_rate(self) -> float:
        return self.home_wins / self.total_matches if self.total_matches else 0.0

    @property
    def away_win_rate(self) -> float:
        return self.away_wins / self.total_matches if self.total_matches else 0.0

    @property
    def draw_rate(self) -> float:
        return self.draws / self.total_matches if self.total_matches else 0.0


@dataclass
class RuleEvaluation:
    """Result of a single rule evaluation."""
    rule_name: str
    weight: float
    condition: str
    explanation: str
    prob_home: float
    prob_draw: float
    prob_away: float
    confidence: float
    impact: float = 0.0


@dataclass
class MatchPrediction:
    """Complete match prediction and reasoning."""
    result: MatchResult
    confidence: float
    prob_home: float
    prob_draw: float
    prob_away: float
    expected_home_goals: int
    expected_away_goals: int
    rule_evaluations: List[RuleEvaluation] = field(default_factory=list)
    summary: str = ""


class ExpertSystemRule:
    """Abstract base class for all expert system rules."""

    def __init__(self, name: str, weight: float):
        self.name = name
        self.weight = weight

    def evaluate(self, home: TeamProfile, away: TeamProfile, h2h: HeadToHeadSummary) -> RuleEvaluation:
        raise NotImplementedError


class RecentFormRule(ExpertSystemRule):
    def __init__(self):
        super().__init__("Recent Form", weight=0.18)

    def evaluate(self, home: TeamProfile, away: TeamProfile, h2h: HeadToHeadSummary) -> RuleEvaluation:
        home_score = home.form_score()
        away_score = away.form_score()
        diff = home_score - away_score
        condition = f"Home form {home.form_summary()} vs away form {away.form_summary()}"

        if diff >= 8:
            explanation = "Home team is in excellent recent form compared to away."
            probs = (0.60, 0.25, 0.15)
        elif diff >= 4:
            explanation = "Home team has significantly better recent form."
            probs = (0.52, 0.30, 0.18)
        elif diff >= 1:
            explanation = "Home team has slightly better recent form."
            probs = (0.45, 0.35, 0.20)
        elif diff <= -8:
            explanation = "Away team is in excellent recent form compared to home."
            probs = (0.15, 0.25, 0.60)
        elif diff <= -4:
            explanation = "Away team has significantly better recent form."
            probs = (0.18, 0.30, 0.52)
        elif diff <= -1:
            explanation = "Away team has slightly better recent form."
            probs = (0.20, 0.35, 0.45)
        else:
            explanation = "Recent form is balanced between the two teams."
            probs = (0.35, 0.35, 0.30)

        return RuleEvaluation(
            rule_name=self.name,
            weight=self.weight,
            condition=condition,
            explanation=explanation,
            prob_home=probs[0],
            prob_draw=probs[1],
            prob_away=probs[2],
            confidence=0.92,
            impact=diff / 12.0,
        )


class HomeAdvantageRule(ExpertSystemRule):
    def __init__(self):
        super().__init__("Home Advantage", weight=0.15)

    def evaluate(self, home: TeamProfile, away: TeamProfile, h2h: HeadToHeadSummary) -> RuleEvaluation:
        diff = home.strength - away.strength
        condition = f"Home strength {home.strength} vs away strength {away.strength}."

        if diff >= 4:
            explanation = "Strong home advantage from superior home performance."
            probs = (0.60, 0.25, 0.15)
        elif diff >= 1:
            explanation = "Slight home advantage from stronger home strength."
            probs = (0.48, 0.32, 0.20)
        elif diff <= -4:
            explanation = "Away team has a strong away strength advantage."
            probs = (0.15, 0.25, 0.60)
        elif diff <= -1:
            explanation = "Away team has a slight away strength advantage."
            probs = (0.22, 0.33, 0.45)
        else:
            explanation = "Home and away strength are balanced."
            probs = (0.35, 0.35, 0.30)

        return RuleEvaluation(
            rule_name=self.name,
            weight=self.weight,
            condition=condition,
            explanation=explanation,
            prob_home=probs[0],
            prob_draw=probs[1],
            prob_away=probs[2],
            confidence=0.84,
            impact=diff / 9.0,
        )


class LeaguePositionRule(ExpertSystemRule):
    def __init__(self):
        super().__init__("League Position", weight=0.14)

    def evaluate(self, home: TeamProfile, away: TeamProfile, h2h: HeadToHeadSummary) -> RuleEvaluation:
        diff = away.league_position - home.league_position
        condition = f"Home position #{home.league_position} vs away position #{away.league_position}."

        if diff >= 8:
            explanation = "Home team is much higher in the league standings."
            probs = (0.58, 0.25, 0.17)
        elif diff >= 4:
            explanation = "Home team has a clear league position advantage."
            probs = (0.50, 0.30, 0.20)
        elif diff <= -8:
            explanation = "Away team is much higher in the league standings."
            probs = (0.17, 0.25, 0.58)
        elif diff <= -4:
            explanation = "Away team has a clear league position advantage."
            probs = (0.20, 0.30, 0.50)
        else:
            explanation = "League positions are relatively close."
            probs = (0.35, 0.35, 0.30)

        return RuleEvaluation(
            rule_name=self.name,
            weight=self.weight,
            condition=condition,
            explanation=explanation,
            prob_home=probs[0],
            prob_draw=probs[1],
            prob_away=probs[2],
            confidence=0.88,
            impact=diff / 10.0,
        )


class OffensiveStrengthRule(ExpertSystemRule):
    def __init__(self):
        super().__init__("Offensive Strength", weight=0.13)

    def evaluate(self, home: TeamProfile, away: TeamProfile, h2h: HeadToHeadSummary) -> RuleEvaluation:
        home_value = home.goals_scored_avg + home.strength * 0.08 + home.motivation * 0.02
        away_value = away.goals_scored_avg + away.strength * 0.08 + away.motivation * 0.02
        diff = home_value - away_value
        condition = f"Home scoring {home.goals_scored_avg:.2f} vs away scoring {away.goals_scored_avg:.2f}."

        if diff >= 1.0:
            explanation = "Home team has a much stronger attacking profile."
            probs = (0.55, 0.28, 0.17)
        elif diff >= 0.4:
            explanation = "Home attack is stronger than away."
            probs = (0.48, 0.32, 0.20)
        elif diff <= -1.0:
            explanation = "Away team has a much stronger attack."
            probs = (0.17, 0.28, 0.55)
        elif diff <= -0.4:
            explanation = "Away attack is stronger than home."
            probs = (0.20, 0.32, 0.48)
        else:
            explanation = "Offensive strength is balanced."
            probs = (0.35, 0.35, 0.30)

        return RuleEvaluation(
            rule_name=self.name,
            weight=self.weight,
            condition=condition,
            explanation=explanation,
            prob_home=probs[0],
            prob_draw=probs[1],
            prob_away=probs[2],
            confidence=0.76,
            impact=diff / 3.0,
        )


class DefensiveStrengthRule(ExpertSystemRule):
    def __init__(self):
        super().__init__("Defensive Strength", weight=0.12)

    def evaluate(self, home: TeamProfile, away: TeamProfile, h2h: HeadToHeadSummary) -> RuleEvaluation:
        home_value = 4.0 - home.goals_conceded_avg + (10 - home.injuries) * 0.04
        away_value = 4.0 - away.goals_conceded_avg + (10 - away.injuries) * 0.04
        diff = home_value - away_value
        condition = f"Home conceded {home.goals_conceded_avg:.2f} vs away conceded {away.goals_conceded_avg:.2f}."

        if diff >= 1.0:
            explanation = "Home defense is clearly stronger than away defense."
            probs = (0.52, 0.28, 0.20)
        elif diff >= 0.3:
            explanation = "Home defense is slightly stronger than away."
            probs = (0.45, 0.33, 0.22)
        elif diff <= -1.0:
            explanation = "Away defense is clearly stronger than home defense."
            probs = (0.20, 0.28, 0.52)
        elif diff <= -0.3:
            explanation = "Away defense is slightly stronger than home."
            probs = (0.22, 0.33, 0.45)
        else:
            explanation = "Defensive strength is fairly balanced."
            probs = (0.35, 0.35, 0.30)

        return RuleEvaluation(
            rule_name=self.name,
            weight=self.weight,
            condition=condition,
            explanation=explanation,
            prob_home=probs[0],
            prob_draw=probs[1],
            prob_away=probs[2],
            confidence=0.80,
            impact=diff / 3.0,
        )


class InjuriesRule(ExpertSystemRule):
    def __init__(self):
        super().__init__("Injuries & Absences", weight=0.10)

    def evaluate(self, home: TeamProfile, away: TeamProfile, h2h: HeadToHeadSummary) -> RuleEvaluation:
        diff = away.injuries - home.injuries
        condition = f"Home injuries {home.injuries} vs away injuries {away.injuries}."

        if diff >= 4:
            explanation = "Home team has a significant fitness advantage."
            probs = (0.55, 0.28, 0.17)
        elif diff >= 1:
            explanation = "Home team has fewer injuries than away."
            probs = (0.48, 0.32, 0.20)
        elif diff <= -4:
            explanation = "Away team has a significant fitness advantage."
            probs = (0.17, 0.28, 0.55)
        elif diff <= -1:
            explanation = "Away team has fewer injuries than home."
            probs = (0.20, 0.32, 0.48)
        else:
            explanation = "Injury influence is balanced."
            probs = (0.35, 0.35, 0.30)

        return RuleEvaluation(
            rule_name=self.name,
            weight=self.weight,
            condition=condition,
            explanation=explanation,
            prob_home=probs[0],
            prob_draw=probs[1],
            prob_away=probs[2],
            confidence=0.72,
            impact=diff / 6.0,
        )


class MotivationRule(ExpertSystemRule):
    def __init__(self):
        super().__init__("Motivation", weight=0.10)

    def evaluate(self, home: TeamProfile, away: TeamProfile, h2h: HeadToHeadSummary) -> RuleEvaluation:
        diff = home.motivation - away.motivation
        condition = f"Home motivation {home.motivation}/10 vs away motivation {away.motivation}/10."

        if diff >= 4:
            explanation = "Home team is far more motivated."
            probs = (0.55, 0.28, 0.17)
        elif diff >= 1:
            explanation = "Home team has a motivation edge."
            probs = (0.48, 0.32, 0.20)
        elif diff <= -4:
            explanation = "Away team is far more motivated."
            probs = (0.17, 0.28, 0.55)
        elif diff <= -1:
            explanation = "Away team has a motivation edge."
            probs = (0.20, 0.32, 0.48)
        else:
            explanation = "Motivation levels are even."
            probs = (0.35, 0.35, 0.30)

        return RuleEvaluation(
            rule_name=self.name,
            weight=self.weight,
            condition=condition,
            explanation=explanation,
            prob_home=probs[0],
            prob_draw=probs[1],
            prob_away=probs[2],
            confidence=0.77,
            impact=diff / 9.0,
        )


class HeadToHeadRule(ExpertSystemRule):
    def __init__(self):
        super().__init__("Head-to-Head", weight=0.08)

    def evaluate(self, home: TeamProfile, away: TeamProfile, h2h: HeadToHeadSummary) -> RuleEvaluation:
        condition = f"Head-to-head record {h2h.home_wins}-{h2h.draws}-{h2h.away_wins}."

        if h2h.total_matches == 0:
            explanation = "No head-to-head history available, so this rule remains neutral."
            probs = (0.35, 0.35, 0.30)
            impact = 0.0
        else:
            home_rate = h2h.home_win_rate
            away_rate = h2h.away_win_rate
            if home_rate >= 0.6:
                explanation = "Home team has dominated head-to-head history."
                probs = (0.55, 0.25, 0.20)
            elif home_rate >= 0.4:
                explanation = "Home team has a slight head-to-head advantage."
                probs = (0.45, 0.30, 0.25)
            elif away_rate >= 0.6:
                explanation = "Away team has dominated head-to-head history."
                probs = (0.20, 0.25, 0.55)
            elif away_rate >= 0.4:
                explanation = "Away team has a slight head-to-head advantage."
                probs = (0.25, 0.30, 0.45)
            else:
                explanation = "Head-to-head history is balanced."
                probs = (0.33, 0.34, 0.33)
            impact = home_rate - away_rate

        return RuleEvaluation(
            rule_name=self.name,
            weight=self.weight,
            condition=condition,
            explanation=explanation,
            prob_home=probs[0],
            prob_draw=probs[1],
            prob_away=probs[2],
            confidence=0.70,
            impact=impact,
        )


class ExpertSystem:
    """Inference engine combining the manual knowledge base."""

    def __init__(self):
        self.rules = [
            RecentFormRule(),
            HomeAdvantageRule(),
            LeaguePositionRule(),
            OffensiveStrengthRule(),
            DefensiveStrengthRule(),
            InjuriesRule(),
            MotivationRule(),
            HeadToHeadRule(),
        ]
        total_weight = sum(rule.weight for rule in self.rules)
        if abs(total_weight - 1.0) > 1e-6:
            raise ValueError(f"Rule weights must sum to 1.0 but sum to {total_weight}")

    def predict(self, home: TeamProfile, away: TeamProfile, h2h: HeadToHeadSummary) -> MatchPrediction:
        evaluations = []
        total_home = total_draw = total_away = 0.0

        for rule in self.rules:
            evaluation = rule.evaluate(home, away, h2h)
            evaluations.append(evaluation)
            total_home += evaluation.prob_home * evaluation.weight
            total_draw += evaluation.prob_draw * evaluation.weight
            total_away += evaluation.prob_away * evaluation.weight

        total = total_home + total_draw + total_away
        if total <= 0:
            total_home, total_draw, total_away = 0.33, 0.33, 0.34
        else:
            total_home /= total
            total_draw /= total
            total_away /= total

        probs = [total_home, total_draw, total_away]
        index = probs.index(max(probs))
        result = [MatchResult.HOME_WIN, MatchResult.DRAW, MatchResult.AWAY_WIN][index]
        confidence = max(probs) * 100
        expected_home_goals, expected_away_goals = self._estimate_scoreline(result, home, away)
        summary = self._build_summary(result, confidence, home, away, evaluations)

        return MatchPrediction(
            result=result,
            confidence=confidence,
            prob_home=total_home,
            prob_draw=total_draw,
            prob_away=total_away,
            expected_home_goals=expected_home_goals,
            expected_away_goals=expected_away_goals,
            rule_evaluations=evaluations,
            summary=summary,
        )

    def _estimate_scoreline(self, result: MatchResult, home: TeamProfile, away: TeamProfile) -> (int, int):
        home_base = (home.goals_scored_avg + away.goals_conceded_avg) / 2
        away_base = (away.goals_scored_avg + home.goals_conceded_avg) / 2

        home_modifier = (home.strength - away.strength) * 0.07
        away_modifier = (away.strength - home.strength) * 0.07
        home_modifier += (away.injuries - home.injuries) * 0.05
        away_modifier += (home.injuries - away.injuries) * 0.05
        home_modifier += (home.motivation - away.motivation) * 0.03
        away_modifier += (away.motivation - home.motivation) * 0.03

        if result == MatchResult.HOME_WIN:
            home_modifier += 0.35
            away_modifier -= 0.20
        elif result == MatchResult.AWAY_WIN:
            away_modifier += 0.35
            home_modifier -= 0.20
        else:
            home_modifier += 0.10
            away_modifier += 0.10

        home_goals = int(round(max(0.0, home_base + home_modifier)))
        away_goals = int(round(max(0.0, away_base + away_modifier)))

        if result == MatchResult.DRAW:
            average = int(round((home_goals + away_goals) / 2))
            return average, average
        if result == MatchResult.HOME_WIN and home_goals <= away_goals:
            home_goals = away_goals + 1
        if result == MatchResult.AWAY_WIN and away_goals <= home_goals:
            away_goals = home_goals + 1

        return max(home_goals, 0), max(away_goals, 0)

    def _build_summary(self, result: MatchResult, confidence: float, home: TeamProfile, away: TeamProfile, evaluations: List[RuleEvaluation]) -> str:
        top_rules = sorted(evaluations, key=lambda r: abs(r.impact), reverse=True)[:3]
        lines = [
            f"Prediction: {result.value} ({confidence:.1f}% confidence)",
            f"{home.name} vs {away.name}",
            "Top influences:"
        ]
        for rule in top_rules:
            lines.append(f"- {rule.rule_name}: {rule.explanation}")
        return "\n".join(lines)
