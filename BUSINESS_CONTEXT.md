# Business Context: DesignSpace — Smart Workspace for Designers

Project — Task #1

## 1. Project overview

DesignSpace is a proposed IoT system that helps designers understand and adjust the conditions around their workspace. A desk-mounted sensor measures ambient light, temperature, and humidity. A web dashboard displays current conditions, shows historical trends, and compares measurements with the designer's saved preferences for different activities.

The project connects IoT with design practice: a designer can select a profile for digital design, sketching, or reviewing physical samples and receive an indication when measured conditions fall outside their chosen ranges.

**Project status:** This document defines a proposed MVP, not an implemented product. The concept follows the project owner's interest in design; the specific design discipline, hardware, and preferred conditions still require validation.

## 2. Business problem and value proposition

Designers may work in rooms where daylight, artificial lighting, temperature, and humidity change throughout the day. Without measurements, it can be difficult to recognize these changes or reproduce a personally preferred working environment.

DesignSpace makes these conditions visible and connects them to a designer's workflow. Instead of repeatedly checking separate instruments, the designer can review one dashboard, select an activity profile, and decide whether to adjust desk lighting, blinds, or room conditions.

The expected value is better awareness and easier reproduction of preferred workspace conditions. Improvements in comfort, productivity, or design quality are hypotheses to test with users, not guaranteed outcomes. An ambient light sensor does not measure display calibration or certify conditions for color-critical work.

## 3. Stakeholders and users

| Stakeholder | Main need |
| --- | --- |
| Freelance designer | Understand changing conditions at a home workspace and save personal preferences. |
| Design student | Use an accessible tool to explore how workspace conditions vary between creative activities. |
| Small design studio owner | Evaluate whether a simple monitoring tool is useful before adopting it for more desks. |
| Project owner and development team | Deliver a demonstrable IoT prototype tied to a practical design workflow. |
| Course evaluator | Assess the relationship between business needs, use cases, and verifiable requirements. |

The primary MVP user is an individual designer with one monitored workspace. Shared studio administration and multiple users per workspace are future possibilities.

## 4. Business objectives and proposed success criteria

| Objective | Proposed validation measure |
| --- | --- |
| Make workspace conditions visible | During a controlled test, at least 95% of valid readings appear within 60 seconds of server receipt. |
| Support different design activities | A user can create, edit, and activate profiles for digital design, sketching, and physical sample review. |
| Help users recognize changes | Five consecutive minutes of readings outside an active profile's range produce one in-app alert for the affected measurement. |
| Make the prototype understandable | At least four of five pilot users can select a profile and identify an out-of-range measurement without assistance. |
| Establish relevance to design work | At least three of five pilot users can describe one practical workspace adjustment informed by the dashboard. |

Pilot targets are proposed evaluation criteria. They are not completed results or proof of general productivity gains.

## 5. MVP scope

Included features:

- Account authentication and ownership of one workspace per account.
- Pairing one compatible sensor device with the workspace.
- Measurement of ambient illuminance in lux, temperature in degrees Celsius, and relative humidity in percent.
- Dashboard with current readings, timestamps, connectivity status, and a 24-hour history.
- User-defined activity profiles with preferred minimum and maximum values for each measurement.
- Manual profile selection and in-app alerts for sustained deviations.
- Explicit indicators for missing readings and offline devices.

Excluded from the MVP:

- Automatic control of lamps, heating, air conditioning, or other electrical equipment.
- Display calibration, color-temperature measurement, and certification for print or color proofing.
- Medical advice or promises about health, comfort, or productivity.
- Cameras, microphones, occupancy tracking, or monitoring an employee's performance.
- Shared studio accounts, multiple desks per account, mobile push notifications, and subscriptions.

## 6. Main use cases

### UC-01 — Set up a designer's workspace

**Actor:** Designer.
**Preconditions:** The user is authenticated and has a compatible device and its pairing credential.

1. The designer names the workspace and enters the pairing credential.
2. The system validates the credential and checks device ownership.
3. The designer places the sensor near the working area according to device guidance.
4. The dashboard displays the first valid readings and their timestamps.

**Outcome:** The designer has a monitored workspace. Invalid credentials and devices already owned by another account are rejected. If no readings arrive, the dashboard shows a waiting state rather than fabricated measurements.

### UC-02 — Choose conditions for a design activity

**Actor:** Designer.
**Preconditions:** The workspace exists.

1. The designer creates a profile, such as “Sketching,” and enters preferred ranges.
2. The system validates and saves the ranges.
3. The designer activates the profile before starting work.
4. The dashboard compares current readings with the selected ranges.

**Outcome:** The workspace is evaluated against the designer's own preferences. Profiles represent personal choices, not universal professional standards.

### UC-03 — Respond to changing conditions

**Actor:** Designer.
**Preconditions:** A profile is active and the sensor is reporting valid readings.

1. A measurement remains outside the selected range for five consecutive minutes.
2. The system creates an in-app alert identifying the measurement, observed value, preferred range, and time.
3. The designer reviews the alert and decides whether to adjust lighting, blinds, or room conditions.
4. Once readings return to the selected range, the system resolves the active condition.

**Outcome:** The designer receives useful feedback without repeated alerts for the same continuous deviation. Physical adjustments remain the user's decision.

### UC-04 — Review a day's workspace conditions

**Actor:** Designer.
**Preconditions:** Historical readings are available.

1. The designer opens the 24-hour history.
2. The system displays separate time-series views for light, temperature, and humidity.
3. The designer examines when conditions changed and considers adjustments for future work sessions.

**Outcome:** The designer can interpret recorded changes. Missing intervals are shown as gaps, and the system does not attribute changes to a cause it has not measured.

### UC-05 — Diagnose an offline sensor

**Actor:** Designer.
**Preconditions:** A paired sensor has previously sent readings.

1. The system receives no valid reading for five minutes.
2. It marks the device offline and displays the time of the last valid reading.
3. The designer checks the device's power and connectivity.
4. A new valid reading restores online status.

**Outcome:** The designer can distinguish stale readings from current conditions. Missing data cannot trigger an environmental alert.

## 7. User stories and acceptance criteria

| ID | User story | Acceptance criteria |
| --- | --- | --- |
| US-01 | As a designer, I want to pair a sensor with my desk so that I can monitor my workspace. | A valid unassigned device can be paired; invalid credentials or another user's device are rejected; the workspace shows the paired device. |
| US-02 | As a designer, I want to see current conditions so that I can decide whether to adjust my surroundings. | The dashboard shows lux, degrees Celsius, and relative humidity with timestamps; unavailable readings are labeled; readings are never presented as current after the device is marked offline. |
| US-03 | As a designer, I want to save profiles for different activities so that I can reuse my preferred settings. | Profiles support a name and a range for each measurement; minimum values must be lower than maximum values; humidity is limited to 0–100% and light values cannot be negative. |
| US-04 | As a designer, I want to activate a profile so that the dashboard reflects my current task. | Exactly one profile is active at a time; switching profiles updates comparisons and resets pending deviation timers. |
| US-05 | As a designer, I want alerts for sustained deviations so that brief fluctuations do not interrupt my work. | Five consecutive minutes outside a range create one alert per measurement; no repeat is created until that measurement returns to range and later exceeds it again; a data gap resets the pending timer. |
| US-06 | As a designer, I want to inspect a day's measurements so that I can recognize changes over time. | The last 24 hours can be viewed for each measurement with units and local times; gaps remain visible rather than being filled with zero values. |
| US-07 | As a designer, I want to know when my sensor is offline so that I can restore monitoring. | Five minutes without valid readings marks the device offline; the last valid timestamp is visible; receiving a new valid reading restores online status. |
| US-08 | As a designer, I want my workspace data to remain private so that other accounts cannot access my routines. | Unauthenticated access is rejected; changing a workspace or device identifier does not expose another user's readings, profiles, or configuration. |

## 8. Business rules and data requirements

- One account owns one workspace and one paired sensor in the MVP.
- Each reading includes a device identifier, a unique reading identifier, a measurement timestamp, and values with defined units.
- The proposed reporting interval is 30 seconds. Values must be validated against the selected sensor's supported measurement ranges.
- Duplicate readings do not create duplicate history entries or advance alert timers. Out-of-order readings can fill historical gaps but do not trigger current-condition alerts.
- Alert evaluation uses consecutive, fresh measurement timestamps. An interval longer than 60 seconds between readings interrupts continuity and resets pending deviation timers.
- An active deviation closes when a valid measurement returns to range. A profile switch clears active conditions and starts evaluation against the newly selected profile.
- Offline status is based on elapsed time since service receipt of the last valid, fresh reading. Old buffered readings must not make an offline device appear current.
- Timestamps are stored consistently and displayed in the workspace's selected time zone.
- Profile ranges are user preferences. Example profile names may be supplied, but the user must set ranges before activating a profile.
- The proposed raw-reading retention period is 30 days, with the last 24 hours available in the MVP dashboard. Retention and account deletion behavior must be finalized before a real-user pilot.

## 9. Quality expectations and constraints

The dashboard should work on laptop and mobile screens, use readable labels, and indicate status with text as well as color. User and device communication should be authenticated and encrypted. Credentials must not be committed to the repository or included in logs.

Sensor placement affects measurements: a sensor near a lamp or heat source may not represent the whole workspace. The interface and setup guidance should explain that measurements describe the sensor's location. Affordable hardware and straightforward setup are priorities; the exact component cost remains to be established after hardware selection.

If hardware is unavailable, a clearly labeled simulator can demonstrate profiles, charts, and alerts. Such a demonstration does not complete the hardware integration milestone.

## 10. Risks and responses

| Risk | Planned response |
| --- | --- |
| The concept does not match the owner's specific design discipline | Confirm whether the initial focus is digital, graphic, product, interior, or another type of design before implementation. |
| Readings are inaccurate or placement is misleading | Document placement guidance and compare prototype readings with a reference instrument. |
| Users interpret light readings as proof of color accuracy | State that lux measurements do not provide display calibration or color-proofing certification. |
| Frequent alerts distract from creative work | Require sustained deviations, suppress duplicates, and allow users to edit their preferred ranges. |
| Network interruptions create misleading history | Mark gaps and stale readings explicitly; pause environmental evaluation during missing data. |
| Users see little value beyond a basic sensor display | Validate activity profiles and historical review with designers before expanding the feature set. |

## 11. Validation and future development

Demonstrate pairing, live readings, profile creation and switching, a sustained deviation, recovery, a connectivity outage, and historical review. Use a known dataset to check duplicate handling, out-of-order readings, alert timing, and missing intervals. Verify account isolation through unauthorized access attempts.

Run a small usability pilot with five designers or design students, using the proposed success criteria above. Record whether users understand the readings and can identify a useful action. The pilot should determine whether profiles solve a meaningful problem before adding features.

Potential later extensions include multiple workspaces, supported smart-light integration with explicit user control, and exportable session reports. They remain outside the initial delivery.

## 12. Open decisions

1. Confirm the owner's design discipline and most relevant creative activities.
2. Choose the microcontroller, sensors, and communication protocol.
3. Select the pairing and authentication mechanism.
4. Agree on the hardware budget, pilot participants, retention, and deletion policy.
5. Validate whether the proposed reporting interval and alert delay suit actual workflows.
