# clean_data_normality.R
# ---------------------
# Purpose: Check normality for all numeric variables (except randomization), generate histograms with density,
#          Q-Q plots, run Shapiro-Wilk tests, apply Box-Cox transformations if needed, 
#          re-check normality, and save updated dataset.
# Language: R
# Dependencies: ggplot2, car, MASS, rio
# Notes: Replace "raw/data_placeholder.csv" with your actual data; do not commit confidential data.

# Load necessary libraries
library(ggplot2)
library(car)
library(MASS)
library(rio)

# Load the dataset
data <- import("raw/data_placeholder.csv", na.strings = c("", "NA"))  # set empty strings and "NA" as missing

# Ensure 'randomization' is treated as factor
if("randomization" %in% names(data)) data$randomization <- as.factor(data$randomization)

# Function to check normality: histogram + density + Q-Q plot + Shapiro-Wilk test
check_normality <- function(data, var_name) {
  cat("\nNormality Check for", var_name, ":\n")
  
  # Histogram with density
  print(
    ggplot(data, aes_string(x = var_name)) +
      geom_histogram(aes(y = ..density..), bins = 30, fill = "skyblue", color = "black") +
      geom_density(color = "red") +
      labs(title = paste("Histogram and Density of", var_name))
  )
  
  # Q-Q Plot
  qqnorm(data[[var_name]], main = paste("Q-Q Plot of", var_name))
  qqline(data[[var_name]], col = "red")
  
  # Shapiro-Wilk Test
  shapiro_test <- shapiro.test(data[[var_name]])
  print(shapiro_test)
  cat("Interpretation: If p-value > 0.05, data is normally distributed (suitable for parametric testing).\n")
}

# Identify numeric variables, excluding 'randomization'
variables_to_check <- names(data)[sapply(data, is.numeric) & names(data) != "randomization"]

# Loop over each variable
for (var in variables_to_check) {
  
  # Check normality
  check_normality(data, var)
  
  # Apply Box-Cox transformation if not normally distributed
  if (shapiro.test(data[[var]])$p.value <= 0.05) {
    cat("\nTransforming", var, "to improve normality using Box-Cox transformation.\n")
    
    # Prepare intercept-only model for Box-Cox
    formula_var <- as.formula(paste(var, "~ 1"))
    boxcox_result <- boxcox(lm(formula_var, data = data), lambda = seq(-3, 3, by = 0.1))
    best_lambda <- boxcox_result$x[which.max(boxcox_result$y)]
    cat("Best lambda for Box-Cox transformation:", best_lambda, "\n")
    
    # Apply the transformation
    if (best_lambda == 0) {
      data[[paste0(var, "_transformed")]] <- log(data[[var]])
    } else {
      data[[paste0(var, "_transformed")]] <- (data[[var]]^best_lambda - 1) / best_lambda
    }
    
    # Re-check normality on transformed variable
    check_normality(data, paste0(var, "_transformed"))
  }
}

# Save the updated dataset
export(data, "output/data_transformed.csv")
cat("\nUpdated dataset saved to 'output/data_transformed.csv'.\n")
