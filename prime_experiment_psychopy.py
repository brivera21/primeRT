"""
PRIME NUMBER JUDGMENT EXPERIMENT - PsychoPy Version

INSTRUCTIONS FOR RUNNING IN SPYDER:
1. Make sure PsychoPy is installed: pip install psychopy
2. Open this file in Spyder
3. Run the script (F5 or click Run button)
4. Enter participant ID when prompted
5. The experiment will run in fullscreen mode
6. Press ESC at any time to quit
7. Data will be saved as CSV in the same directory as this script

EXPERIMENT OVERVIEW:
- Participants judge whether numbers are prime or not
- Response keys: F and J (assignment counterbalanced by participant ID)
- 20 practice trials followed by 4 blocks of 150 trials (600 total)
- Data saved with millisecond precision reaction times

AUTHOR: Created for cognitive psychology research
DATE: October 2025
"""

from psychopy import visual, core, event, gui, data
import random
import csv
import os
from datetime import datetime

# ============================================================================
# EXPERIMENT PARAMETERS
# ============================================================================

# Stimuli
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
NON_PRIMES = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26,
              27, 28, 30, 32, 33, 34, 35, 36, 38]

# Repetitions (to achieve 600 trials total)
REPS_PER_PRIME = 25      # 12 primes × 25 = 300 trials
REPS_PER_NONPRIME = 12   # 25 non-primes × 12 = 300 trials

# Timing (in seconds)
FIXATION_DURATION = 0.5
FEEDBACK_DURATION = 0.3

# Block structure
PRACTICE_TRIALS = 20
TRIALS_PER_BLOCK = 150
NUM_BLOCKS = 4

# Response keys
PRIME_KEY = None  # Will be set based on counterbalancing
NOT_PRIME_KEY = None  # Will be set based on counterbalancing
QUIT_KEY = 'escape'

# ============================================================================
# SETUP FUNCTIONS
# ============================================================================

def get_participant_info():
    """Get participant ID and determine key counterbalancing."""
    dlg = gui.Dlg(title="Prime Number Experiment")
    dlg.addText('Prime Number Judgment Task')
    dlg.addField('Participant ID:', '')
    dlg.show()

    if dlg.OK:
        participant_id = dlg.data[0]
        if not participant_id:
            participant_id = "UNKNOWN"
        return participant_id
    else:
        core.quit()

def determine_key_mapping(participant_id):
    """Counterbalance key assignment based on participant ID hash."""
    global PRIME_KEY, NOT_PRIME_KEY

    # Use hash of participant ID to determine counterbalancing
    id_hash = hash(participant_id)

    if id_hash % 2 == 0:
        # Even: F = NOT PRIME, J = PRIME
        PRIME_KEY = 'j'
        NOT_PRIME_KEY = 'f'
    else:
        # Odd: F = PRIME, J = NOT PRIME
        PRIME_KEY = 'f'
        NOT_PRIME_KEY = 'j'

    return PRIME_KEY, NOT_PRIME_KEY

def create_trial_list(is_practice=False):
    """Create randomized list of trials."""
    trials = []

    if is_practice:
        # Practice: subset of stimuli
        practice_primes = random.sample(PRIMES, min(6, len(PRIMES)))
        practice_nonprimes = random.sample(NON_PRIMES, min(14, len(NON_PRIMES)))

        for num in practice_primes:
            trials.append({'stimulus': num, 'is_prime': True})
        for num in practice_nonprimes:
            trials.append({'stimulus': num, 'is_prime': False})

        random.shuffle(trials)
        return trials[:PRACTICE_TRIALS]

    else:
        # Main experiment: all stimuli with repetitions
        for num in PRIMES:
            for _ in range(REPS_PER_PRIME):
                trials.append({'stimulus': num, 'is_prime': True})

        for num in NON_PRIMES:
            for _ in range(REPS_PER_NONPRIME):
                trials.append({'stimulus': num, 'is_prime': False})

        random.shuffle(trials)
        return trials

def create_output_file(participant_id):
    """Create CSV file for data output."""
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'primeRT_{participant_id}_{timestamp}.csv'

    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)

    # Create CSV with headers
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'participant_ID',
            'trial_number',
            'stimulus',
            'correct_response',
            'participant_response',
            'RT',
            'accuracy',
            'block_number',
            'timestamp'
        ])

    return filepath

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def show_instructions(win, prime_key, not_prime_key):
    """Display instruction screen."""
    instructions_text = f"""PRIME NUMBER JUDGMENT TASK

In this experiment, you will see numbers on the screen.
Your task is to judge whether each number is PRIME or NOT PRIME.

A PRIME number is only divisible by 1 and itself.
Examples: 2, 3, 5, 7, 11, 13...

A NOT PRIME number has other divisors.
Examples: 4, 6, 8, 9, 10, 12...

RESPONSE KEYS:
Press '{prime_key.upper()}' if the number is PRIME
Press '{not_prime_key.upper()}' if the number is NOT PRIME

Each trial:
1. You'll see a + sign (get ready)
2. Then a number appears
3. Respond as quickly and accurately as possible
4. You'll get brief feedback (Correct/Incorrect)

You'll start with 20 practice trials, then complete
4 blocks of 150 trials each with breaks between blocks.

Respond as quickly AND accurately as you can!

Press SPACE to begin practice trials."""

    instr = visual.TextStim(win, text=instructions_text, height=0.05,
                           wrapWidth=1.8, color='white')
    instr.draw()
    win.flip()

    event.waitKeys(keyList=['space', QUIT_KEY])

def show_block_break(win, block_num, total_blocks, accuracy=None, mean_rt=None):
    """Display break screen between blocks."""
    if accuracy is not None and mean_rt is not None:
        perf_text = f"\n\nYour performance in the last block:\nAccuracy: {accuracy:.1f}%\nAverage RT: {mean_rt:.0f} ms"
    else:
        perf_text = ""

    if block_num <= total_blocks:
        break_text = f"""End of Block {block_num-1} of {total_blocks}{perf_text}

Take a short break if you need it.

Press SPACE when you're ready to continue."""
    else:
        break_text = f"""Experiment Complete!{perf_text}

Thank you for participating!

Your data has been saved.

Press SPACE to exit."""

    break_stim = visual.TextStim(win, text=break_text, height=0.06,
                                 wrapWidth=1.8, color='white')
    break_stim.draw()
    win.flip()

    event.waitKeys(keyList=['space', QUIT_KEY])

def show_practice_complete(win):
    """Display message after practice block."""
    practice_text = """Practice Complete!

Now you'll begin the main experiment.

There will be 4 blocks of 150 trials each.
You can take breaks between blocks.

Remember:
- Respond as quickly AND accurately as possible
- Use the same finger positions throughout

Press SPACE to begin the main experiment."""

    prac_stim = visual.TextStim(win, text=practice_text, height=0.06,
                                wrapWidth=1.8, color='white')
    prac_stim.draw()
    win.flip()

    event.waitKeys(keyList=['space', QUIT_KEY])

# ============================================================================
# TRIAL FUNCTION
# ============================================================================

def run_trial(win, trial_info, fixation, stimulus_text, feedback_text,
              trial_num, block_num, participant_id, output_file):
    """Run a single trial and save data."""

    # Show fixation cross
    fixation.draw()
    win.flip()
    core.wait(FIXATION_DURATION)

    # Show stimulus and wait for response
    stimulus_text.text = str(trial_info['stimulus'])
    stimulus_text.draw()
    win.flip()

    # Start timer and get response
    timer = core.Clock()
    keys = event.waitKeys(keyList=[PRIME_KEY, NOT_PRIME_KEY, QUIT_KEY],
                         timeStamped=timer)

    if not keys:
        return False

    key_pressed, rt = keys[0]

    # Check if quit
    if key_pressed == QUIT_KEY:
        return False

    # Determine response and accuracy
    participant_response = 'prime' if key_pressed == PRIME_KEY else 'not_prime'
    correct_response = 'prime' if trial_info['is_prime'] else 'not_prime'
    accuracy = 1 if participant_response == correct_response else 0

    # Show feedback
    if accuracy == 1:
        feedback_text.text = "Correct"
        feedback_text.color = 'green'
    else:
        feedback_text.text = "Incorrect"
        feedback_text.color = 'red'

    feedback_text.draw()
    win.flip()
    core.wait(FEEDBACK_DURATION)

    # Save data
    timestamp = datetime.now().isoformat()
    rt_ms = rt * 1000  # Convert to milliseconds

    with open(output_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            participant_id,
            trial_num,
            trial_info['stimulus'],
            correct_response,
            participant_response,
            f'{rt_ms:.3f}',
            accuracy,
            block_num,
            timestamp
        ])

    return True

# ============================================================================
# MAIN EXPERIMENT
# ============================================================================

def run_experiment():
    """Main experiment function."""

    # Get participant info
    participant_id = get_participant_info()
    prime_key, not_prime_key = determine_key_mapping(participant_id)

    # Create output file
    output_file = create_output_file(participant_id)
    print(f"Data will be saved to: {output_file}")

    # Create window
    win = visual.Window(
        fullscr=True,
        color='black',
        units='height',
        allowGUI=False
    )

    # Create stimuli
    fixation = visual.TextStim(win, text='+', height=0.1, color='white')
    stimulus_text = visual.TextStim(win, text='', height=0.15, color='white')
    feedback_text = visual.TextStim(win, text='', height=0.08, color='white')

    # Show instructions
    show_instructions(win, prime_key, not_prime_key)

    # ========================================================================
    # PRACTICE BLOCK
    # ========================================================================

    practice_trials = create_trial_list(is_practice=True)
    trial_counter = 1

    for trial_info in practice_trials:
        continue_exp = run_trial(
            win, trial_info, fixation, stimulus_text, feedback_text,
            trial_counter, 'practice', participant_id, output_file
        )

        if not continue_exp:
            win.close()
            core.quit()

        trial_counter += 1

    # Practice complete
    show_practice_complete(win)

    # ========================================================================
    # MAIN EXPERIMENT BLOCKS
    # ========================================================================

    # Create all trials for main experiment
    all_trials = create_trial_list(is_practice=False)

    # Split into blocks
    trial_counter = 1

    for block_num in range(1, NUM_BLOCKS + 1):
        start_idx = (block_num - 1) * TRIALS_PER_BLOCK
        end_idx = start_idx + TRIALS_PER_BLOCK
        block_trials = all_trials[start_idx:end_idx]

        # Track block performance
        block_accuracy = []
        block_rts = []

        for trial_info in block_trials:
            continue_exp = run_trial(
                win, trial_info, fixation, stimulus_text, feedback_text,
                trial_counter, block_num, participant_id, output_file
            )

            if not continue_exp:
                win.close()
                core.quit()

            # Read last line to get accuracy and RT for block stats
            with open(output_file, 'r') as f:
                lines = f.readlines()
                if len(lines) > 1:
                    last_line = lines[-1].strip().split(',')
                    block_accuracy.append(int(last_line[6]))
                    block_rts.append(float(last_line[5]))

            trial_counter += 1

        # Calculate block statistics
        mean_accuracy = (sum(block_accuracy) / len(block_accuracy)) * 100
        mean_rt = sum(block_rts) / len(block_rts)

        # Show break (except after last block)
        if block_num < NUM_BLOCKS:
            show_block_break(win, block_num + 1, NUM_BLOCKS, mean_accuracy, mean_rt)
        else:
            show_block_break(win, block_num + 1, NUM_BLOCKS, mean_accuracy, mean_rt)

    # Cleanup
    win.close()
    print(f"\nExperiment complete! Data saved to: {output_file}")

# ============================================================================
# RUN
# ============================================================================

if __name__ == "__main__":
    try:
        run_experiment()
    except Exception as e:
        print(f"Error: {e}")
        core.quit()
