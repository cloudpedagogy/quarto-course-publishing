# Worked Example in R

## Scenario

Suppose a diagnostic test has a probability of success of 0.7. If 10 tests are carried out, what is the probability of observing exactly 8 successful results?

## R Code

{r}

dbinom(8, size = 10, prob = 0.7)

## Interpretation

This command calculates the probability of exactly 8 successes out of 10 trials when the probability of success on each trial is 0.7.

## Extension

pbinom(7, size = 10, prob = 0.7, lower.tail = FALSE)

## Explanation

This extension calculates the probability of observing 8 or more successes, which is often useful when interpreting threshold-based outcomes.
