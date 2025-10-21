# Quick Start Guide

## For Researchers

### 1. Running a Single Participant

1. Open `index.html` in a web browser
2. Enter participant ID (e.g., "P001")
3. Follow on-screen instructions
4. Download CSV file at the end

### 2. Running Multiple Participants

```bash
# Option 1: Provide unique links with IDs pre-filled
# (requires simple modification to index.html)

# Option 2: Maintain a participant log
# ID    Date       Time     Status     Notes
# P001  2025-10-21 10:00   Complete   No issues
# P002  2025-10-21 10:30   Complete   Asked questions during break
# P003  2025-10-21 11:00   Complete   No issues
```

### 3. Analyzing Data

#### Using Python:
```bash
python analyze_data.py primeRT_P001_2025-10-21T10-15-30-456Z.csv
```

#### Using R:
```bash
Rscript analyze_data.R primeRT_P001_2025-10-21T10-15-30-456Z.csv
```

#### Or in R console:
```r
source("analyze_data.R")
analyze_participant("primeRT_P001_2025-10-21T10-15-30-456Z.csv")
```

## For Participants

### Your Task
Judge whether numbers are **PRIME** or **NOT PRIME** as quickly and accurately as possible.

### Keys
- One key for PRIME
- One key for NOT PRIME
- (Keys shown on screen at start)

### Structure
1. Practice: 20 trials
2. Main experiment: 600 trials in 4 blocks
3. Breaks after each block
4. ~20-30 minutes total

### Tips
- Focus on accuracy first, speed second
- Take breaks when offered
- Stay focused during each block
- Ask questions before starting

## Expected Timeline

| Phase | Duration | Trials |
|-------|----------|--------|
| Instructions | 2-3 min | - |
| Practice | 1-2 min | 20 |
| Block 1 | 4-5 min | 150 |
| Break 1 | 1 min | - |
| Block 2 | 4-5 min | 150 |
| Break 2 | 1 min | - |
| Block 3 | 4-5 min | 150 |
| Break 3 | 1 min | - |
| Block 4 | 4-5 min | 150 |
| Results & Download | 1 min | - |
| **Total** | **20-30 min** | **600** |

## Troubleshooting

**Keys not working?**
- Only F and J keys work
- Click on browser window first
- Make sure CAPS LOCK is off

**Experiment frozen?**
- Refresh and start over (data will be lost if not downloaded)
- Close other tabs/programs
- Try a different browser

**Data not downloading?**
- Complete at least practice block
- Check browser's download folder
- Check pop-up blocker settings

## Data Files

Each participant generates one CSV file:
```
primeRT_[ID]_[Timestamp].csv
```

Example:
```
primeRT_P001_2025-10-21T10-15-30-456Z.csv
```

## Need Help?

See full `README.md` for detailed information.
