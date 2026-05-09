# ⚽ Football Match Predictor - Rule-Based Expert System

A professional, production-quality **Rule-Based Expert System** for predicting football match outcomes. This system analyzes team statistics and applies weighted rules to generate deterministic, explainable predictions.

## 🎯 Key Features

✅ **Pure Rule-Based System** (NOT Machine Learning)
- No ML models, neural networks, or black-box algorithms
- 100% deterministic - same input always produces same output
- Fully explainable predictions with clear reasoning

✅ **Real Data Processing**
- Loads historical match data from CSV
- Automatically calculates team statistics
- Supports any football league/season with proper data format

✅ **Weighted Expert Rules**
- 7 domain-based rules with explicit weights
- Weights sum to exactly 1.0
- Transparent rule impact visualization

✅ **Professional Streamlit UI**
- Beautiful, modern interface
- CSV upload capability
- Real-time team selection and prediction
- Comprehensive statistics display
- Educational content included

✅ **Production Quality Code**
- Modular architecture with separate concerns
- Comprehensive error handling
- Type hints throughout
- Clear documentation
- Easy to modify and extend

## 📊 System Architecture

```
app.py (Streamlit UI)
├── data_loader.py (CSV Loading & Validation)
├── team_stats.py (Statistics Calculation)
└── expert_system.py (Rule-Based Inference)
```

### Data Flow

```
CSV File → DataLoader → TeamStatsCalculator → Expert System → Prediction + Explanation
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone or navigate to the project directory
cd expert_system_project

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📈 Expert System Rules

The system evaluates 7 weighted rules:

| Rule | Weight | Purpose |
|------|--------|---------|
| Recent Form | 20% | Last 5 matches strong predictor |
| League Position | 18% | Better-ranked teams typically win |
| Goal Statistics | 17% | Offensive/defensive metrics |
| Home Advantage | 15% | Home teams historical edge |
| Defensive Strength | 12% | How well teams defend |
| Offensive Efficiency | 8% | Scoring capability |
| Head-to-Head History | 10% | Direct matchup records |

**Total Weight: 100%**

## 📁 Project Structure

```
expert_system_project/
├── app.py                  # Main Streamlit application
├── data_loader.py         # CSV loading and validation
├── team_stats.py          # Statistics calculation engine
├── expert_system.py       # Rule-based inference engine
├── sample_data.csv        # Sample Premier League 2023-24 data
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## 📝 Data Format

Your CSV file must contain these columns:

```
Date,HomeTeam,AwayTeam,FTHG,FTAG,FTR
2023-08-12,Manchester City,Burnley,3,0,H
2023-08-12,Arsenal,Nottingham Forest,2,1,H
...
```

**Column Definitions:**
- `Date`: Match date (YYYY-MM-DD)
- `HomeTeam`: Home team name
- `AwayTeam`: Away team name
- `FTHG`: Full-time home goals (integer)
- `FTAG`: Full-time away goals (integer)
- `FTR`: Result - H (Home Win), D (Draw), A (Away Win)

## 🎓 Understanding Expert Systems

### What makes this NOT Machine Learning?

| Aspect | Expert System | Machine Learning |
|--------|---------------|------------------|
| Knowledge | Explicit rules | Implicit patterns |
| Learning | Rule modification | Data training |
| Explainability | Full transparency | Black-box (often) |
| Determinism | 100% deterministic | Probabilistic |
| Maintenance | Expert-driven | Data-driven |

### How the Inference Engine Works

1. **Load Match Data**: Parse CSV with historical matches
2. **Calculate Statistics**: Compute team metrics from match history
3. **Evaluate Rules**: Each rule independently evaluates team strengths
4. **Weight Results**: Combine rule outputs using assigned weights
5. **Generate Prediction**: Select outcome with highest probability
6. **Explain Result**: Provide full reasoning for the prediction

## 💡 Example Prediction

```
Match: Arsenal vs Manchester City

Rule Evaluations:
├─ Recent Form (20%): Arsenal excellent (WWWD), City mixed (WDWW) → 60% Arsenal
├─ League Position (18%): Arsenal #3, City #1 → 40% City
├─ Goal Stats (17%): City strong (2.5 avg), Arsenal good (2.0 avg) → 50% City
├─ Home Advantage (15%): Arsenal at home → 55% Arsenal
├─ Defensive Strength (12%): Both strong → 35/35/30
├─ Offensive Efficiency (8%): City efficient → 50% City
└─ Head-to-Head (10%): Balanced → 33/34/33

Combined Result:
Probability: 45% Arsenal Win, 32% Draw, 23% City Win
Prediction: Arsenal Win (45% confidence)
Reasoning: Home advantage + recent form momentum + playing at home
```

## 🛠️ Customization

### Modifying Rule Weights

Edit `expert_system.py`:

```python
class ExpertSystem:
    def __init__(self):
        self.rules: List[ExpertSystemRule] = [
            RecentFormRule(),           # weight=0.20
            LeaguePositionRule(),       # weight=0.18
            GoalStatisticsRule(),       # weight=0.17
            HomeAdvantageRule(),        # weight=0.15
            DefensiveStrengthRule(),    # weight=0.12
            OffensiveEfficiencyRule(),  # weight=0.08
            HeadToHeadRule()            # weight=0.10
        ]
        # Weights must sum to 1.0!
```

### Adding New Rules

1. Create a new rule class inheriting from `ExpertSystemRule`
2. Implement the `evaluate()` method
3. Return a `RuleEvaluation` with probabilities
4. Add to `ExpertSystem.rules` list

Example:

```python
class InjuriesRule(ExpertSystemRule):
    def __init__(self):
        super().__init__("Injuries & Suspensions", weight=0.05)
    
    def evaluate(self, home: TeamStats, away: TeamStats) -> RuleEvaluation:
        # Your logic here
        # Return RuleEvaluation with prob_home, prob_draw, prob_away
        pass
```

## 📊 Expected Outputs

### Prediction Results Include:

1. **Match Outcome**
   - Home Win / Draw / Away Win
   - Confidence percentage

2. **Probabilities**
   - P(Home Win)
   - P(Draw)
   - P(Away Win)

3. **Expected Score**
   - Expected home goals
   - Expected away goals

4. **Rule Explanations**
   - What each rule concluded
   - Why each rule matters
   - Impact on final prediction

5. **Team Statistics**
   - League position
   - Recent form
   - Goals statistics
   - Defensive/Offensive metrics

## ⚠️ Limitations

- Cannot account for **live information** (injuries, suspensions announced day-of-match)
- Cannot predict **tactical surprises** (unexpected formations, strategies)
- Cannot account for **managerial changes**
- Cannot predict **individual brilliance** (star player performance)
- Football inherently has **random elements** no system can fully predict
- System is calibrated on **English Premier League 2023-24** - may not generalize to other leagues/seasons

## 🧪 Testing

The project includes sample data from English Premier League 2023-24. To test:

1. Run `streamlit run app.py`
2. Click "Load Sample Data"
3. Select any two teams
4. Click "Predict Match"
5. Review prediction and rule explanations

## 📈 Performance Notes

- **Prediction Time**: <1 second per match
- **Data Loading**: Depends on CSV size (100+ matches handled instantly)
- **Memory Usage**: Minimal (all data in memory)
- **Scalability**: Designed for single-season, single-league datasets

## 🔄 Workflow

### First-Time Users:
1. App auto-loads sample data
2. Select two teams
3. Click predict
4. Review probabilities and explanations

### Using Custom Data:
1. Prepare CSV in required format
2. Upload via "Upload CSV" option
3. Select teams and predict

### Developers:
1. Modify rule weights in `expert_system.py`
2. Add new rules as needed
3. Update UI in `app.py`
4. Test with your data

## 📚 Educational Value

This project demonstrates:
- ✅ Expert system architecture
- ✅ Rule-based inference
- ✅ Modular Python design
- ✅ Data processing and statistics
- ✅ Professional UI development
- ✅ Production-quality code structure

## 📄 License

This project is provided as-is for educational purposes.

## 🤝 Contributing

Contributions welcome! Areas for enhancement:
- Additional rules (e.g., manager experience, player quality)
- Multi-league support
- Historical accuracy reporting
- Performance metrics dashboard
- Advanced visualization

## ❓ FAQ

**Q: Why not use machine learning?**
A: Expert systems are more interpretable and don't require large training datasets.

**Q: Can I modify the rules?**
A: Yes! Edit the rule classes in `expert_system.py`. Remember weights must sum to 1.0.

**Q: What if I have different data?**
A: As long as your CSV matches the required format, it should work.

**Q: How accurate is this?**
A: Like all prediction systems, accuracy varies. Football is inherently unpredictable.

**Q: Can I add more teams/leagues?**
A: Yes! Just ensure your CSV contains all relevant matches.

---

**Created**: 2024
**Type**: Rule-Based Expert System
**Purpose**: Educational & Demonstration
**Language**: Python 3.8+
