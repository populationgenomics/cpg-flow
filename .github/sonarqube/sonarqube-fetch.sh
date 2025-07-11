#!/bin/bash

# Variables
SONAR_HOST_URL=$1
SONAR_TOKEN=$2
PROJECT_KEY=$3
MAIN_PROJECT_KEY=$4

# Function to return the appropriate emoji based on Quality Gate status
get_quality_gate_emoji() {
  local status=$1
  local emoji

  if [[ "$status" == "OK" ]]; then
    emoji="✅"
  elif [[ "$status" == "ERROR" ]]; then
    emoji="❌"
  elif [[ "$status" == "WARN" ]]; then
    emoji="⚠️"
  else
    emoji="🔲"
  fi

  # Prepend the emoji to the status
  echo "$emoji $status"
}

# Fetch metrics for both overall and new code
ISSUES="new_accepted_issues new_software_quality_blocker_issues new_software_quality_high_issues new_software_quality_info_issues new_software_quality_low_issues new_software_quality_maintainability_issues new_software_quality_medium_issues new_software_quality_reliability_issues new_software_quality_security_issues"
METRICS="coverage bugs vulnerabilities code_smells security_hotspots $ISSUES"
METRICS_JOINED=$(echo "$METRICS" | tr ' ' ',')

# Fetching the project metrics for PR
RESPONSE_PR=$(curl -s -u "$SONAR_TOKEN:" "$SONAR_HOST_URL/api/measures/component?component=$PROJECT_KEY&metricKeys=$METRICS_JOINED")

# Fetching the project metrics for the main project
RESPONSE_MAIN=$(curl -s -u "$SONAR_TOKEN:" "$SONAR_HOST_URL/api/measures/component?component=$MAIN_PROJECT_KEY&metricKeys=$METRICS_JOINED")

# Fetch the Quality Gate statuses for PR and Main projects
QUALITY_GATE_PR=$(curl -s -u "$SONAR_TOKEN:" "$SONAR_HOST_URL/api/qualitygates/project_status?projectKey=$PROJECT_KEY" | jq -r '.projectStatus.status')
QUALITY_GATE_MAIN=$(curl -s -u "$SONAR_TOKEN:" "$SONAR_HOST_URL/api/qualitygates/project_status?projectKey=$MAIN_PROJECT_KEY" | jq -r '.projectStatus.status')

QUALITY_GATE_PR=$(get_quality_gate_emoji "$QUALITY_GATE_PR")
QUALITY_GATE_MAIN=$(get_quality_gate_emoji "$QUALITY_GATE_MAIN")

# Initialize an empty associative array for both main and PR project metrics
declare -A METRIC_VALUES_PR
declare -A METRIC_VALUES_MAIN

# Function to extract metrics and sum issues
extract_metrics() {
  local RESPONSE="$1"
  local -n METRIC_VALUES=$2  # Use nameref for associative array
  METRIC_VALUES["new_issues"]=0

  local index=0
  for metric in $METRICS; do
    VALUE=$(echo "$RESPONSE" | jq -r ".component.measures[] | select(.metric==\"$metric\") | .value // empty" || echo "")
    # Treat empty or null as zero, and ensure numeric
    if [[ -z "$VALUE" || "$VALUE" == "null" ]]; then
      VALUE=0
    fi
    if ! [[ "$VALUE" =~ ^-?[0-9]+([.][0-9]+)?$ ]]; then
      VALUE=0
    fi

    # Save metric value, sum the ones in $ISSUES into one key
    if [[ " $ISSUES " =~ [[:space:]]$metric[[:space:]] ]]; then
      VALUE=$(echo "$RESPONSE" | jq -r ".component.measures[] | select(.metric==\"$metric\") | .period.value // empty" || echo "")
      # Treat empty or null as zero, and ensure numeric
      if [[ -z "$VALUE" || "$VALUE" == "null" ]]; then
        VALUE=0
      fi
      if ! [[ "$VALUE" =~ ^-?[0-9]+([.][0-9]+)?$ ]]; then
        VALUE=0
      fi

      NEW_VALUE=$(echo "${METRIC_VALUES["new_issues"]} + $VALUE" | bc)
      METRIC_VALUES["new_issues"]=$NEW_VALUE
    else
      METRIC_VALUES[$metric]=$VALUE
    fi

    ((index++))
  done
}

# Extract the overall metrics for PR
extract_metrics "$RESPONSE_PR" METRIC_VALUES_PR
extract_metrics "$RESPONSE_MAIN" METRIC_VALUES_MAIN

# Load the template from the file (make sure you have a .github/sonarqube/sonarqube-template.md file)
TEMPLATE=$(cat .github/sonarqube/sonarqube-template.md)

# Replace the placeholders for PR metrics
for key in "${!METRIC_VALUES_PR[@]}"; do
  TEMPLATE=$(echo "$TEMPLATE" | sed "s|{{${key}_pr}}|${METRIC_VALUES_PR[$key]}|g")
done

# Replace the placeholders for Main project metrics
for key in "${!METRIC_VALUES_MAIN[@]}"; do
  TEMPLATE=$(echo "$TEMPLATE" | sed "s|{{${key}_main}}|${METRIC_VALUES_MAIN[$key]}|g")
done

# Add the Quality Gate values to the template
TEMPLATE=$(echo "$TEMPLATE" | sed "s|{{quality_gate_pr}}|$QUALITY_GATE_PR|g" | sed "s|{{quality_gate_main}}|$QUALITY_GATE_MAIN|g")

# Add the SONAR_HOST_URL, PROJECT_KEY and MAIN_PROJECT_KEY to the template
TEMPLATE=$(echo "$TEMPLATE" | sed "s|{{SONAR_HOST_URL}}|$SONAR_HOST_URL|g" | sed "s|{{PROJECT_KEY}}|$PROJECT_KEY|g" | sed "s|{{MAIN_PROJECT_KEY}}|$MAIN_PROJECT_KEY|g")

# Output the final comment to stdout
echo "$TEMPLATE"
