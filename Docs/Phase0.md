# PHASE 0 - RESEARCH & VALIDATION

## Objective

Validate whether bank downtime is a significant enough problem to justify building Paytm Smart Reserve AI.

No product development should happen during this phase.

The output of this phase is a research report and structured dataset.

---

## Research Questions

### Bank Reliability

1. Which banks experience the highest downtime?
2. Which banks have the highest technical decline rates?
3. Which banks experience recurring maintenance windows?
4. What are the most common outage durations?

### Customer Impact

1. How many transactions are likely affected?
2. What customer segments are affected most?
3. What payment categories are affected most?

### UPI Lite Opportunity

1. Can UPI Lite serve as a reserve mechanism?
2. What transaction limits apply?
3. What user segments would benefit most?

---

## Data Sources

### NPCI

Collect:

* Technical Decline (TD)
* Business Decline (BD)
* Success Rates
* Bank Statistics

### Banks

Monitor:

* SBI
* HDFC
* ICICI
* Axis
* Kotak
* PNB
* BOB
* Canara

Collect:

* Maintenance notices
* Scheduled outages
* Downtime announcements

### Public Sources

Collect:

* News reports
* Press releases
* Bank notices

---

## Data Model

### banks.csv

Fields:

bank_name

bank_type

upi_enabled

---

### outages.csv

Fields:

bank_name

incident_date

start_time

end_time

duration_minutes

planned_or_unplanned

source

---

### maintenance_notices.csv

Fields:

bank_name

announcement_date

maintenance_start

maintenance_end

description

---

## Analytics Required

Generate:

### Top Banks By Downtime

Rank all banks.

### Downtime Heatmap

Analyze:

Day of week

Hour of day

Month

### Incident Frequency

Count:

Incidents per bank

Incidents per month

### Duration Analysis

Average outage duration

Longest outage

Median outage

### Planned vs Unplanned

Percentage breakdown

---

## Expected Outputs

### Executive Summary

Answer:

Is Smart Reserve needed?

### Findings Report

Top affected banks

Top outage windows

Estimated customer impact

### Recommendation

Proceed

Do Not Proceed

Need More Data

---

## Success Criteria

The phase is successful if we can prove:

1. Bank downtime is measurable.
2. Users are impacted.
3. UPI Lite can help mitigate the issue.
4. There is sufficient business value for Paytm.

No UI.

No AI.

No Dashboard Product.

Research only.
