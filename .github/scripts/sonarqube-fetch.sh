#!/bin/bash

# Variables
SONAR_HOST_URL=$1
SONAR_TOKEN=$2
PROJECT_KEY=$3

# Fetch metrics for both overall and new code
METRICS="coverage,bugs,vulnerabilities,code_smells,security_hotspots,new_coverage,new_bugs,new_vulnerabilities,new_code_smells,new_security_hotspots,new_lines_to_cover"

# Fetching the project metrics
RESPONSE=$(curl -s -u "$SONAR_TOKEN:" "$SONAR_HOST_URL/api/measures/component?component=$PROJECT_KEY&metricKeys=$METRICS")

# Echo the response for debugging
echo "$RESPONSE" | jq .

# Fetch the Quality Gate statuses
QUALITY_GATE_ALL=$(curl -s -u "$SONAR_TOKEN:" "$SONAR_HOST_URL/api/qualitygates/project_status?projectKey=$PROJECT_KEY" | jq -r '.projectStatus.status')
QUALITY_GATE_NEW=$(curl -s -u "$SONAR_TOKEN:" "$SONAR_HOST_URL/api/qualitygates/project_status?projectKey=$PROJECT_KEY&newCode=true" | jq -r '.projectStatus.status')

# Initialize an empty associative array
declare -A METRIC_VALUES

# Extract the overall metrics
for metric in coverage bugs vulnerabilities code_smells security_hotspots; do
  VALUE=$(echo "$RESPONSE" | jq -r ".component.measures[] | select(.metric==\"$metric\") | .value // \"N/A\"")
  METRIC_VALUES[$metric]=$VALUE
done

# Extract the new code metrics
for metric in new_coverage new_bugs new_vulnerabilities new_code_smells new_security_hotspots new_lines_to_cover; do
  VALUE=$(echo "$RESPONSE" | jq -r ".component.measures[] | select(.metric==\"$metric\") | .period.value // \"N/A\"")
  METRIC_VALUES[$metric]=$VALUE
done

# Create the final comment by replacing placeholders in the template
TEMPLATE=$(cat .github/assets/sonarqube-template.md)
for key in "${!METRIC_VALUES[@]}"; do
  TEMPLATE=$(echo "$TEMPLATE" | sed "s|{{${key}}}|${METRIC_VALUES[$key]}|g")
done

# Add the Quality Gate values to the template
TEMPLATE=$(echo "$TEMPLATE" | sed "s|{{quality_gate_all}}|$QUALITY_GATE_ALL|g" | sed "s|{{quality_gate_new}}|$QUALITY_GATE_NEW|g")

# Output the final comment to stdout
echo "$TEMPLATE"
