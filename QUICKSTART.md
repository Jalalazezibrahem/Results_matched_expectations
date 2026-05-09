# ⚡ Quick Start Guide

## 🚀 Run the Application in 2 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the App
```bash
streamlit run app.py
```

✅ **Done!** The app will open at `http://localhost:8501`

---

## 📖 First-Time Use

1. **Open the app** (it auto-loads sample data)
2. **Select** two teams from the sidebar
3. **Click** "🔮 Predict Match"
4. **View** predictions and explanations

---

## 📊 What You'll See

### Prediction Results:
- **Match Outcome** (Home Win / Draw / Away Win)
- **Confidence Level** (0-100%)
- **Probabilities** for each outcome
- **Expected Score** (goals prediction)

### Analysis:
- **Team Statistics** comparison
- **Rule Evaluations** showing what influenced the prediction
- **Educational Content** explaining how it works

---

## 📂 Project Files

```
✅ app.py              - Main Streamlit application
✅ data_loader.py      - CSV data handling
✅ team_stats.py       - Statistics calculation
✅ expert_system.py    - Rule-based prediction engine
✅ sample_data.csv     - Real EPL 2023-24 data
✅ requirements.txt    - Python dependencies
✅ README.md           - Full documentation
✅ test_system.py      - Testing script
```

---

## 🔧 Test the System

```bash
python test_system.py
```

This validates all components and shows a sample prediction.

---

## 📚 Learn More

- **Full Documentation**: See `README.md`
- **Technical Details**: See `PROJECT_COMPLETION_SUMMARY.md`
- **Inside the App**: Click "📚 Learn More About Expert Systems"

---

## ⚙️ Customization

### Upload Your Own Data:
1. Prepare CSV with columns: Date, HomeTeam, AwayTeam, FTHG, FTAG, FTR
2. In app, select "Upload CSV"
3. Upload your file
4. Predict with your data

### Modify Rules:
Edit weights in `expert_system.py`:
- Recent Form: 20%
- League Position: 18%
- Goal Statistics: 17%
- Home Advantage: 15%
- Defensive Strength: 12%
- Offensive Efficiency: 8%
- Head-to-Head: 10%

---

## ❓ FAQ

**Q: What if I get an import error?**
A: Run `pip install -r requirements.txt` again

**Q: Can I use different data?**
A: Yes! Upload your CSV in the required format

**Q: Is this accurate?**
A: It's a demonstration system. Football is unpredictable!

**Q: How do I add new rules?**
A: Create a class in `expert_system.py` inheriting from `ExpertSystemRule`

---

## 🎯 Example Flow

```
1. Open app
   ↓
2. Load sample data (automatic)
   ↓
3. Select: Manchester City (Home) vs Arsenal (Away)
   ↓
4. Click "Predict Match"
   ↓
5. See:
   - Result: Home Win
   - Confidence: 44.2%
   - Probabilities shown as bars
   - All rules evaluated with impact
   ↓
6. Explore team statistics and learn about the system
```

---

## ✨ Key Features

✅ **Rule-Based** (not machine learning)
✅ **Deterministic** (same input = same output)
✅ **Explainable** (see WHY for every prediction)
✅ **Data-Driven** (loads from CSV)
✅ **Professional UI** (beautiful Streamlit interface)
✅ **Educational** (learn expert systems)

---

**Ready?** Run: `streamlit run app.py`

**Questions?** Check `README.md` for comprehensive documentation
