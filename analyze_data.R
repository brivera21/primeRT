# Prime Number RT Experiment - Data Analysis Script
# R version
#
# This script analyzes data from the Prime Number RT experiment
# Usage: Rscript analyze_data.R <data_file.csv>

# Load required libraries
if (!require("tidyverse")) install.packages("tidyverse")
library(tidyverse)

# Function to analyze a single participant's data
analyze_participant <- function(data_file) {

  cat("======================================\n")
  cat("Prime Number RT Experiment Analysis\n")
  cat("======================================\n\n")

  # Load data
  cat("Loading data from:", data_file, "\n\n")
  data <- read.csv(data_file)

  # Basic info
  cat("Participant ID:", unique(data$participantId), "\n")
  cat("Total trials:", nrow(data), "\n")
  cat("Blocks completed:", max(data$block), "\n\n")

  # Overall accuracy
  accuracy <- mean(data$accuracy) * 100
  cat("Overall Accuracy:", round(accuracy, 2), "%\n\n")

  # Filter to correct trials for RT analysis
  correct_data <- data %>% filter(accuracy == 1)

  # Overall RT
  cat("--- Reaction Time Analysis (Correct Trials Only) ---\n")
  cat("Mean RT:", round(mean(correct_data$reactionTime), 1), "ms\n")
  cat("Median RT:", round(median(correct_data$reactionTime), 1), "ms\n")
  cat("SD RT:", round(sd(correct_data$reactionTime), 1), "ms\n\n")

  # RT by response type
  cat("--- RT by Number Type ---\n")
  rt_by_type <- correct_data %>%
    group_by(correctResponse) %>%
    summarise(
      n = n(),
      mean_rt = mean(reactionTime),
      sd_rt = sd(reactionTime),
      median_rt = median(reactionTime)
    )
  print(rt_by_type, n = Inf)

  # Prime effect
  prime_rt <- rt_by_type %>% filter(correctResponse == "prime") %>% pull(mean_rt)
  not_prime_rt <- rt_by_type %>% filter(correctResponse == "not_prime") %>% pull(mean_rt)
  prime_effect <- prime_rt - not_prime_rt
  cat("\nPrime Effect (Prime - Not Prime):", round(prime_effect, 1), "ms\n\n")

  # Magnitude effect (for primes only)
  cat("--- RT by Prime Magnitude ---\n")
  prime_magnitude <- correct_data %>%
    filter(correctResponse == "prime") %>%
    mutate(magnitude = ifelse(stimulus < 20, "small (<20)", "large (≥20)")) %>%
    group_by(magnitude) %>%
    summarise(
      n = n(),
      mean_rt = mean(reactionTime),
      sd_rt = sd(reactionTime),
      median_rt = median(reactionTime)
    )
  print(prime_magnitude, n = Inf)

  # Magnitude effect
  if (nrow(prime_magnitude) == 2) {
    small_rt <- prime_magnitude %>% filter(magnitude == "small (<20)") %>% pull(mean_rt)
    large_rt <- prime_magnitude %>% filter(magnitude == "large (≥20)") %>% pull(mean_rt)
    magnitude_effect <- large_rt - small_rt
    cat("\nMagnitude Effect (Large - Small):", round(magnitude_effect, 1), "ms\n\n")
  }

  # Accuracy by number type
  cat("--- Accuracy by Number Type ---\n")
  acc_by_type <- data %>%
    group_by(correctResponse) %>%
    summarise(
      n = n(),
      accuracy = mean(accuracy) * 100
    )
  print(acc_by_type, n = Inf)
  cat("\n")

  # Block-by-block performance
  cat("--- Performance by Block ---\n")
  block_performance <- data %>%
    filter(block != "practice") %>%
    group_by(block) %>%
    summarise(
      n = n(),
      accuracy = mean(accuracy) * 100,
      mean_rt = mean(reactionTime[accuracy == 1])
    )
  print(block_performance, n = Inf)
  cat("\n")

  # Individual stimulus analysis
  cat("--- Performance by Stimulus ---\n")
  stimulus_performance <- correct_data %>%
    group_by(stimulus, correctResponse) %>%
    summarise(
      n = n(),
      mean_rt = mean(reactionTime),
      sd_rt = sd(reactionTime)
    ) %>%
    arrange(correctResponse, stimulus)
  print(stimulus_performance, n = Inf)

  # Statistical tests
  cat("\n--- Statistical Tests ---\n")

  # t-test for prime effect
  prime_rts <- correct_data %>% filter(correctResponse == "prime") %>% pull(reactionTime)
  not_prime_rts <- correct_data %>% filter(correctResponse == "not_prime") %>% pull(reactionTime)

  t_test_result <- t.test(prime_rts, not_prime_rts)
  cat("\nPrime vs Not Prime (t-test):\n")
  cat("  t =", round(t_test_result$statistic, 3), "\n")
  cat("  df =", round(t_test_result$parameter, 1), "\n")
  cat("  p =", format.pval(t_test_result$p.value, digits = 3), "\n")

  # t-test for magnitude effect (primes only)
  small_prime_rts <- correct_data %>%
    filter(correctResponse == "prime", stimulus < 20) %>%
    pull(reactionTime)
  large_prime_rts <- correct_data %>%
    filter(correctResponse == "prime", stimulus >= 20) %>%
    pull(reactionTime)

  if (length(small_prime_rts) > 0 && length(large_prime_rts) > 0) {
    t_test_magnitude <- t.test(large_prime_rts, small_prime_rts)
    cat("\nSmall vs Large Primes (t-test):\n")
    cat("  t =", round(t_test_magnitude$statistic, 3), "\n")
    cat("  df =", round(t_test_magnitude$parameter, 1), "\n")
    cat("  p =", format.pval(t_test_magnitude$p.value, digits = 3), "\n")
  }

  cat("\n======================================\n")
  cat("Analysis Complete\n")
  cat("======================================\n")

  # Return results invisibly for further analysis
  invisible(list(
    data = data,
    correct_data = correct_data,
    rt_by_type = rt_by_type,
    prime_effect = prime_effect,
    prime_magnitude = prime_magnitude,
    stimulus_performance = stimulus_performance
  ))
}

# Main execution
if (interactive()) {
  cat("This script analyzes Prime Number RT data.\n")
  cat("Usage: analyze_participant('your_data_file.csv')\n")
} else {
  # Command line usage
  args <- commandArgs(trailingOnly = TRUE)
  if (length(args) == 0) {
    cat("Error: No data file specified\n")
    cat("Usage: Rscript analyze_data.R <data_file.csv>\n")
    quit(status = 1)
  }

  data_file <- args[1]
  if (!file.exists(data_file)) {
    cat("Error: File not found:", data_file, "\n")
    quit(status = 1)
  }

  analyze_participant(data_file)
}
