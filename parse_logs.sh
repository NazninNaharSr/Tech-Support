#!/usr/bin/env bash
# parse_logs.sh
# -------------
# Quickly extract errors, warnings, and key events from application logs.
# Usage: ./parse_logs.sh <logfile> [--errors-only]
#
# Example: ./parse_logs.sh app.log --errors-only

LOG_FILE="$1"
MODE="$2"

if [[ -z "$LOG_FILE" ]]; then
  echo "Usage: $0 <logfile> [--errors-only]"
  exit 1
fi

if [[ ! -f "$LOG_FILE" ]]; then
  echo "❌ File not found: $LOG_FILE"
  exit 1
fi

echo "============================================"
echo " Log Analysis: $LOG_FILE"
echo " $(wc -l < "$LOG_FILE") total lines"
echo "============================================"

echo ""
echo "📊 Summary:"
echo "  ERRORs   : $(grep -ci "error" "$LOG_FILE")"
echo "  WARNINGs : $(grep -ci "warn" "$LOG_FILE")"
echo "  CRITICALs: $(grep -ci "critical\|fatal" "$LOG_FILE")"

echo ""
if [[ "$MODE" == "--errors-only" ]]; then
  echo "🔴 Errors & Criticals:"
  grep -iE "error|critical|fatal" "$LOG_FILE" | tail -50
else
  echo "🟡 Warnings:"
  grep -i "warn" "$LOG_FILE" | tail -20

  echo ""
  echo "🔴 Errors:"
  grep -i "error" "$LOG_FILE" | tail -20

  echo ""
  echo "💡 Last 10 log lines:"
  tail -10 "$LOG_FILE"
fi

echo ""
echo "============================================"
echo " Analysis complete."
echo "============================================"
