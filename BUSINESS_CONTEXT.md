# Business Context: IoT Smart Home Energy Monitoring

Project — Task #1

## 1. Project definition and assumptions

This project proposes an Internet of Things (IoT) system that helps residents understand household electricity consumption and identify opportunities to reduce waste. Connected meters or smart plugs send consumption readings to a service that presents them in a dashboard and notifies users when configured limits are exceeded.

**Planning assumption:** Smart home energy monitoring is the proposed topic because the repository did not contain an existing project specification. The scope and success targets below are proposals to validate with stakeholders, not claims about an implemented product.

## 2. Business problem and value

Household electricity bills show total charges but often provide limited insight into when energy was consumed or which appliances contributed most. Residents may therefore struggle to identify unnecessary usage or understand the effect of changing their habits.

The proposed system makes consumption visible at the level supported by installed devices. It helps residents compare usage over time, investigate unusual consumption, and evaluate potential savings. Any cost shown is an estimate based on a user-supplied fixed electricity rate; the utility bill remains the authoritative source of charges.

## 3. Stakeholders and intended users

| Stakeholder | Need or interest |
| --- | --- |
| Homeowner or tenant | Understand consumption, identify waste, and manage an electricity budget. |
| Household administrator | Register devices, assign room or appliance labels, and configure alerts. |
| Invited household member | View the household dashboard without changing configuration. |
| System maintainer | Diagnose data ingestion and device connectivity problems while limiting access to household data. |
| Project team or evaluator | Assess whether the prototype solves the stated problem through demonstrable user workflows. |

The primary customer is a household with compatible metering devices and internet access. The prototype supports one household per account; shared access uses administrator and viewer roles.

## 4. Objectives and proposed success criteria

| Objective | Proposed acceptance measure |
| --- | --- |
| Make recent consumption visible | During a controlled connectivity test, at least 95% of valid readings appear in the dashboard within 60 seconds of service receipt. |
| Support comparisons | A user can compare daily consumption across a selected seven-day period for each monitored device. |
| Identify threshold exceedances | A qualifying reading creates an in-app alert within 60 seconds of receipt, with one alert per device per configured daily threshold period. |
| Make missing data clear | A device is marked offline after five minutes without a valid reading; affected totals are marked incomplete. |
| Protect household access | Access-control checks demonstrate that users cannot read or modify another household's devices, readings, or alerts. |

The project aims to support better decisions, but does not promise a particular reduction in electricity usage or bills. Actual savings would require a longer pilot and a baseline for comparison.

## 5. Scope

### Minimum viable product

- Account authentication and household administrator/viewer permissions.
- Registration and labeling of compatible meters or smart plugs.
- Collection of timestamped energy readings and device connectivity status.
- Dashboard showing recent consumption and daily historical totals by device.
- Estimated variable energy costs using a manually entered fixed rate and currency.
- User-configured daily energy thresholds and in-app notifications.
- Clear display of stale readings and incomplete reporting periods.

### Outside the initial scope

- Remote switching of appliances or automatic control of electrical equipment.
- Utility billing, payment processing, or revenue-grade metering certification.
- Dynamic tariffs, taxes, standing charges, or automatic tariff imports.
- Automatic identification of individual appliances from whole-home readings.
- Solar generation, battery optimization, and commercial multi-building management.
- Email, SMS, or push notifications and predictive recommendations.

## 6. Main use cases

### UC-01 — Register a monitoring device

**Actor:** Household administrator.  
**Preconditions:** The administrator is signed in and has a compatible device with proof of ownership or a pairing credential.

1. The administrator starts device registration and supplies the pairing information.
2. The system validates the device and checks that it is not assigned to another household.
3. The administrator assigns a room or appliance label.
4. The system displays the device and its connection status.

**Outcome:** The device belongs to the household and can contribute readings. Invalid pairing information or an existing assignment produces a clear error without creating a duplicate device.

### UC-02 — Review consumption and estimated costs

**Actor:** Administrator or household viewer.  
**Preconditions:** At least one device is registered.

1. The user opens the dashboard and selects a device and date range.
2. The system displays available consumption in kWh, daily totals, and the time of the latest reading.
3. If a fixed rate is configured, the system displays an estimated variable cost.
4. The user compares daily totals to identify high-consumption periods.

**Outcome:** The user can understand recorded usage. Empty periods, stale readings, and gaps are explicitly identified; missing readings are not presented as zero consumption.

### UC-03 — Receive a daily consumption alert

**Actor:** Household administrator.  
**Preconditions:** A device has a positive daily energy threshold configured.

1. The system receives and validates a new energy reading.
2. It updates the device's daily consumption using the household's configured time zone.
3. When consumption exceeds the threshold, it creates an in-app alert.
4. The administrator reviews the device, measured consumption, threshold, and event time.

**Outcome:** The administrator is informed of the exceedance. Further readings during the same local day do not create duplicate alerts for that device and threshold.

### UC-04 — Investigate an offline device

**Actor:** Household administrator.  
**Preconditions:** A registered device has previously reported readings.

1. The system detects that no valid reading has arrived for five minutes.
2. The dashboard marks the device offline and shows its last reading time.
3. The administrator checks device power and network connectivity.
4. When valid readings resume, the system updates the connection status.

**Outcome:** The user can distinguish a connection problem from low energy use. Historical gaps remain marked unless recovered readings fill them.

## 7. User stories and acceptance criteria

| ID | User story | Acceptance criteria |
| --- | --- | --- |
| US-01 | As an administrator, I want to register and label a device so that I know which appliance or room it monitors. | Valid pairing creates one household device; invalid or already assigned devices are rejected; the label appears in the dashboard. |
| US-02 | As a resident, I want to see recent consumption so that I can understand current household activity. | Each device shows available consumption, units, and the latest reading time; stale data is visibly marked. |
| US-03 | As a resident, I want to compare daily energy use so that I can identify changes in my habits. | A seven-day selection shows daily kWh totals; aggregation follows the household time zone; periods with gaps are marked incomplete. |
| US-04 | As an administrator, I want to enter my electricity rate so that residents can see approximate energy costs. | Only a nonnegative numeric rate with a currency is accepted; estimated cost equals recorded kWh multiplied by the configured rate; the display states that fixed charges and taxes are excluded. |
| US-05 | As an administrator, I want daily consumption alerts so that I can investigate unexpectedly high usage. | A positive threshold can be saved per device; exceeding it creates an in-app alert with the device, time, usage, and threshold; repeated readings do not duplicate that day's alert. |
| US-06 | As an administrator, I want to recognize offline devices so that I can restore monitoring. | Five minutes without valid readings produces an offline status; the last reading time remains visible; a new valid reading restores online status. |
| US-07 | As a household viewer, I want to inspect consumption without changing settings so that I can participate in energy-saving decisions. | A viewer can read household readings and alerts but cannot register devices, edit rates, or change thresholds; these restrictions are enforced by the service. |
| US-08 | As a resident, I want my household data to remain private so that unrelated users cannot observe my habits. | Unauthenticated requests are rejected; authenticated users cannot access another household's data by changing a resource identifier. |

## 8. Business rules and data requirements

- Each device belongs to one household at a time. Only its household administrator can change its configuration.
- Each accepted reading identifies a device, measurement time, unit, and energy quantity. The ingestion design must define whether the device supplies cumulative counters or interval energy before aggregation is implemented.
- Power in watts and energy in kWh are distinct quantities and must not be displayed interchangeably.
- Duplicate readings must not increase consumption totals. Invalid readings must not enter aggregates; late readings must update the correct historical period.
- Household summaries must avoid double-counting overlapping meters, such as a whole-home meter and its appliance submeters. Until coverage is configured, show per-device totals instead of an assumed household total.
- Daily totals and threshold periods follow the household's selected time zone. Threshold edits take effect on the next local day.
- In the prototype, the current fixed rate is applied to any selected reporting period. Changing it recalculates displayed estimates and does not reconstruct historical tariffs.
- The proposed retention period is 90 days of readings for prototype reporting; deletion and retention behavior must be agreed before a pilot with real household data.

## 9. Quality expectations and constraints

The dashboard should work on desktop and mobile screens, use clear units and readable labels, and indicate status with text rather than color alone. Device-to-service and user-to-service communications should be authenticated and encrypted, with credentials excluded from source control and logs.

The prototype depends on compatible hardware, reliable timestamps, and network connectivity. If physical hardware is unavailable, a simulator may demonstrate the workflows, but simulated readings must be labeled and hardware integration must remain an explicit unfinished milestone.

Consumption patterns can reveal household routines. Collect only information needed for monitoring, restrict access by household and role, and define account deletion and data handling before real users participate.

## 10. Risks and validation plan

| Risk | Planned response |
| --- | --- |
| Inaccurate or incompatible device readings | Validate units and meter behavior against known sample readings before interpreting results. |
| Connectivity gaps distort comparisons | Show missing intervals and incomplete totals; support recovered readings where hardware permits. |
| Too many notifications reduce usefulness | Use explicit user thresholds and suppress repeated alerts within the daily period. |
| Cost estimates are mistaken for bills | Label estimates and show the rate, currency, and excluded charges. |
| Users expect whole-home coverage from a few smart plugs | Show which devices are monitored and describe coverage limits. |
| The proposed topic does not match stakeholder expectations | Confirm the project concept and MVP scope before implementation. |

Validate the prototype with a walkthrough covering registration, a seven-day consumption comparison, a threshold exceedance, a device outage, and unauthorized access attempts. Use a known dataset to verify totals, duplicate handling, missing intervals, and cost calculations. Ask prospective users whether the dashboard helps them identify a concrete action; use their feedback to prioritize subsequent development.

## 11. Open decisions

1. Confirm the proposed smart home energy monitoring topic and target households.
2. Select supported hardware, communication protocol, and expected reporting interval.
3. Confirm the pairing method, account invitation flow, and data deletion policy.
4. Agree on the pilot size and validate the proposed success targets.
