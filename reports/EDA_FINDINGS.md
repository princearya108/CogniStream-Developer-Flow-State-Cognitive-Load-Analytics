# CogniStream EDA Findings

## Dataset validation

- 500 records and 9 columns were analyzed.
- No missing cells were found.
- No duplicate rows were found.
- `task_success` contains 303 successful and 197 unsuccessful records.
- The observed task-success rate is 60.6%.

## Productivity comparison

Successful records have these averages:

- Coding hours: 5.98
- Commits: 5.35
- Bugs reported: 0.70
- AI-tool usage: 1.72 hours
- Cognitive load: 4.20

Unsuccessful records have these averages:

- Coding hours: 3.53
- Commits: 3.47
- Bugs reported: 1.10
- AI-tool usage: 1.19 hours
- Cognitive load: 4.96

These are associations in the available data, not proof that any individual
behavior causes success or failure.

## Cognitive-load comparison

The cognitive-load groups were defined as:

- Low: 1–3
- Medium: 4–6
- High: 7–10

The high-load group has 106 records, a 36.8% task-success rate and 1.25
average reported bugs. The medium-load group has 277 records, a 68.2%
task-success rate and 0.86 average reported bugs. The low-load group has 117
records, a 64.1% task-success rate and 0.51 average reported bugs.

## Recommended dashboard story

The dashboard should focus on:

1. Overall task-success rate and record volume.
2. Cognitive-load group success rate.
3. Bugs and distractions as early-warning indicators.
4. Coding hours, commits and AI-tool usage as productivity context.

The dataset does not contain dates, developer IDs or team IDs. Therefore, the
current analysis cannot measure individual trends over time, compare teams, or
support longitudinal workforce decisions. A future version should collect
dated, anonymized observations before making operational decisions.
