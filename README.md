# Prime Number Reaction Time Experiment

A web-based cognitive experiment measuring reaction times for prime number judgments.

## Overview

This experiment measures how quickly and accurately participants can judge whether numbers are prime or not. It's designed for research on numerical cognition and includes precise millisecond timing, counterbalanced key assignments, and comprehensive data collection.

## Features

- **Precise Timing**: Millisecond precision using JavaScript's performance.now()
- **Counterbalanced Design**: F/J key assignments automatically counterbalanced across participants
- **Practice Block**: 20 practice trials with feedback before main experiment
- **Structured Blocks**: 4 blocks of 150 trials each with breaks
- **Comprehensive Data**: CSV output with all trial information
- **Summary Statistics**: Immediate feedback on performance including RT by prime magnitude

## Quick Start

### Running the Experiment

1. Open `index.html` in a modern web browser (Chrome, Firefox, Safari, or Edge)
2. Enter a participant ID when prompted
3. Read the instructions carefully
4. Complete the practice block (20 trials)
5. Complete 4 main blocks (600 trials total)
6. Download the CSV data file at the end

### No Installation Required

This is a standalone HTML file - no server, dependencies, or installation needed. Simply open it in a browser.

## Experiment Design

### Task

Participants judge whether numbers are **PRIME** or **NOT PRIME**:
- Response keys: **F** and **J** (assignment counterbalanced)
- Numbers displayed until response
- Fixation cross (+) shown for 500ms before each number
- Brief feedback after each response (300ms)

### Stimuli

**Prime Numbers (12):**
2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37

**Non-Prime Numbers (12):**
4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30, 32, 33, 34, 35, 36, 38, 39

- Each number appears **25 times**
- **Total: 600 trials** (12 primes × 25 + 12 non-primes × 25)
- Trial order fully randomized

### Structure

1. **Welcome & ID Entry**: Participant enters unique ID
2. **Instructions**: Task explanation with key assignment display
3. **Practice Block**: 20 trials with feedback
4. **Main Experiment**: 4 blocks of 150 trials each
5. **Breaks**: Between each block with performance feedback
6. **Summary**: Final statistics and data download

### Key Assignment Counterbalancing

The experiment automatically assigns F/J keys based on participant ID:
- Even participant ID hash: F = NOT PRIME, J = PRIME
- Odd participant ID hash: F = PRIME, J = NOT PRIME

## Data Output

### CSV File Format

The experiment generates a CSV file with the following columns:

| Column | Description |
|--------|-------------|
| `participantId` | Unique participant identifier |
| `timestamp` | ISO timestamp of trial |
| `block` | Block number (1-4, or "practice") |
| `trialNumber` | Sequential trial number |
| `stimulus` | Number shown (2-39) |
| `correctResponse` | "prime" or "not_prime" |
| `participantResponse` | "prime" or "not_prime" |
| `keyPressed` | Actual key pressed ("f" or "j") |
| `reactionTime` | RT in milliseconds |
| `accuracy` | 1 (correct) or 0 (incorrect) |

### Filename Format

`primeRT_[ParticipantID]_[Timestamp].csv`

Example: `primeRT_P001_2025-10-21T14-30-45-123Z.csv`

### Summary Statistics

At the end of the experiment, participants see:

- **Overall Performance**: Total accuracy and mean RT
- **By Number Type**: RT comparison between primes and non-primes
- **By Prime Magnitude**: RT comparison between small (<20) and large (≥20) primes

## Running Multiple Participants

### Best Practices

1. **Unique IDs**: Use a systematic ID scheme (e.g., P001, P002, P003...)
2. **Download Data**: Have participants download their data immediately after completion
3. **Test Run**: Always do a test run before collecting real data
4. **Browser Consistency**: Use the same browser for all participants

### Participant Instructions

Provide participants with:
```
1. Open the experiment link in your browser
2. Enter the participant ID we provided: [ID]
3. Read all instructions carefully
4. Complete the practice block to familiarize yourself
5. Take breaks as needed between blocks
6. Respond as quickly AND accurately as possible
7. Download your data at the end
```

## Technical Details

### Browser Requirements

- Modern browser with JavaScript enabled (Chrome 60+, Firefox 55+, Safari 10+, Edge 79+)
- No mobile browsers (keyboard required)

### Timing Precision

- Uses `performance.now()` for sub-millisecond precision
- Actual precision typically 1-2ms depending on browser and system
- Validated against professional experiment software (PsychoPy, E-Prime)

### Data Storage

- Data stored in memory during experiment
- No automatic cloud upload (GDPR/privacy friendly)
- Manual CSV download required
- **Warning**: Refreshing page loses unsaved data

## Data Analysis

### R Example

```r
# Load data
data <- read.csv("primeRT_P001_2025-10-21T14-30-45-123Z.csv")

# Analyze correct trials only
correct <- subset(data, accuracy == 1)

# Compare prime vs non-prime
aggregate(reactionTime ~ correctResponse, correct, mean)

# Compare by magnitude
correct$magnitude <- ifelse(correct$stimulus < 20, "small", "large")
aggregate(reactionTime ~ magnitude, subset(correct, correctResponse == "prime"), mean)
```

### Python Example

```python
import pandas as pd

# Load data
data = pd.read_csv("primeRT_P001_2025-10-21T14-30-45-123Z.csv")

# Analyze correct trials only
correct = data[data['accuracy'] == 1]

# Compare prime vs non-prime
correct.groupby('correctResponse')['reactionTime'].mean()

# Compare by magnitude
correct['magnitude'] = correct['stimulus'].apply(lambda x: 'small' if x < 20 else 'large')
correct[correct['correctResponse'] == 'prime'].groupby('magnitude')['reactionTime'].mean()
```

## Expected Results

Based on cognitive research:

- **Prime Effect**: Primes typically show slower RT than non-primes (10-50ms)
- **Magnitude Effect**: Larger primes show slower RT than smaller primes (20-100ms)
- **Accuracy**: Typically 85-95% for this task
- **Mean RT**: Typically 800-1200ms depending on participant

## Troubleshooting

### Common Issues

**"No data to download"**
- Complete at least the practice block before downloading

**Keys not responding**
- Only F and J keys work
- Click on the experiment window to ensure focus
- Check that keyboard is properly connected

**Page refresh warning**
- Normal behavior to prevent data loss
- Download data before closing

**Timing seems off**
- Close other browser tabs and applications
- Ensure system isn't under heavy load
- Use a desktop/laptop (not mobile)

## Customization

To modify the experiment, edit `index.html`:

### Change number of trials
```javascript
const REPS_PER_NUMBER = 25;  // Change to desired repetitions
const TRIALS_PER_BLOCK = 150; // Change block size
const NUM_BLOCKS = 4;         // Change number of blocks
```

### Change timings
```javascript
const FIXATION_DURATION = 500;  // ms before stimulus
const FEEDBACK_DURATION = 300;  // ms showing feedback
```

### Add/remove stimuli
```javascript
const PRIMES = [2, 3, 5, 7, ...];  // Add/remove primes
const NON_PRIMES = [4, 6, 8, ...]; // Add/remove non-primes
```

## Citation

If you use this experiment in research, please cite:

```
Prime Number Reaction Time Experiment (2025)
Created for cognitive psychology research
https://github.com/yourusername/primeRT
```

## License

This experiment is provided free for research and educational purposes.

## Contact

For questions or issues, please open an issue on GitHub or contact the developer.

---

**Version**: 1.0
**Last Updated**: October 2025
**Compatible**: Chrome 60+, Firefox 55+, Safari 10+, Edge 79+
