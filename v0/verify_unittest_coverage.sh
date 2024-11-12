#!/bin/bash

# Check if a code coverage threshold is provided as an argument
if [ -z "$1" ]; then
  echo "Error: Code coverage threshold percentage must be provided as an argument."
  echo "Usage: $0 <CODE_COVERAGE_PERCENT>"
  exit 1
fi

# Use the first argument as the code coverage threshold
CODE_COVERAGE_PERCENT=$1

# Convert the threshold percentage to a decimal
threshold=$(echo "$CODE_COVERAGE_PERCENT" | awk '{print $1 / 100}')

# Extract class names and line-rates using xmllint and sed (instead of grep -P)
class_info=$(xmllint --xpath '//packages/package/classes/class[@line-rate]' coverage.xml | sed -n 's/.*name="\([^"]*\)".*line-rate="\([0-9.]*\)".*/\1 \2/p')

# Initialize variables
result="false"
below_threshold_classes=()

# Loop through each class name and line-rate
while read -r class_name line_rate; do
  if (( $(echo "$line_rate < $threshold" | bc -l) )); then
      result="true"
      below_threshold_classes+=("$class_name")
  fi
done <<< "$class_info"

# If any class is below threshold, output the class names and fail the build
if [ "$result" = "true" ]; then
  echo "Code coverage is below threshold for the following classes:"
  printf '%s\n' "${below_threshold_classes[@]}"
  exit 1
else
  echo "All classes meet the code coverage threshold."
fi
