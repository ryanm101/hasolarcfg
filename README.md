# Solaredge Homeassistant Modbus integration config

This is effectively a copy of: https://community.home-assistant.io/t/solaredge-modbus-configuration-for-single-inverter-and-battery/464084 with some additions of my own such as tariffs. All credit for the inital work goes to https://community.home-assistant.io/u/remko/summary I've just added to what was done by remko. 

## WARNING

DO NOT just blindly use this, there are some bits that might need tweaking for your setup. Please See Notes section below for bits I have thought of.. BEWARE the automations CHECK that they do what YOU want them to.

## Pre-Req

### Additional Installations:
* HACS - https://hacs.xyz/
  * Integrations:
    * https://github.com/WillCodeForCats/solaredge-modbus-multi
  * Frontend Cards:
    * power-distribution-card
    * tesla-style-solar-power-card
    * apexcharts-card
    * Power Flow Card
    * template-entity-row

### On HA installation
* Edit Configuration.yaml
```yaml
homeassistant:
  packages: !include_dir_named packages
  customize:
    sensor.solar_imported_power_kwh:
      device_class: energy
    sensor.solar_exported_power_kwh:
      device_class: energy
    sensor.solar_panel_production_kwh:
      device_class: energy
    sensor.solar_panel_to_house_kwh:
      device_class: energy
    sensor.solar_panel_to_battery_kwh:
      device_class: energy
    sensor.solar_grid_to_battery_kwh:
      device_class: energy
    sensor.solar_battery_out_kwh:
      device_class: energy
    sensor.solar_battery_in_kwh:
      device_class: energy
    sensor.solar_house_consumption_kwh:
      device_class: energy
    sensor.solar_battery_to_grid_kwh:
      device_class: energy
```

* Copy the packages dir from this repo to `/config` on your home assistant installation


## Notes

* Check https://github.com/ryanm101/hasolarcfg/blob/master/packages/energy_utilities.yaml as I use Tariffs with some non-standard billing cycles (monthly)
* Check https://github.com/ryanm101/hasolarcfg/blob/master/packages/electricity_tarriff_automations.yaml as you many not want all the tariffs I do, (notably the `household_*` are old ones i need that I'm deprecating in my own code elsewhere)
* Check https://github.com/ryanm101/hasolarcfg/blob/master/packages/energy_automations.yaml I change the battery during MY offpeak period yours may be different. This ideally should be a sensor for where i have specific times, but that is on the TODO. Also BEWARE I have an automation that Discharges the battery IF I can import cheaper than I export, if so I cycle between charge and discharge. THIS COULD COST YOU MONEY!!!!!!!!!


## Helper scripts (NOT Homeassistant scripts)

* tariffSwitchGen.py - This script reads the file containing all the utilities `utility_meter:` and then it will create yaml for the automation to switch your tariffs
`python3 ./tariffSwitchGen.py packages/energy_utilities.yaml packages/electricity_tarriff_automations.yaml`


# **** NEW **** Formula - NOT Implemented yet

# Battery Energy Share Value Model

## Overview

This model treats stored battery energy as "shares" with an associated cost basis.

- Battery capacity: **10 kWh**
- Grid charge cost: **X (off-peak)**
- Solar charge cost: **0**
- Goal: Track the **average cost per kWh** of energy stored in the battery over time.

---

## Core Variables

- `E` = Energy stored in battery (kWh)
- `C` = Total cost of stored energy
- `S` = Cost per kWh (share value)

### Share Value Formula

```
S = C / E   (if E > 0)
S = 0       (if E == 0)
```

---

## Operations

### 1. Charge from Grid

```
E_new = E_old + E_charge
C_new = C_old + (X * E_charge)
```

---

### 2. Charge from Solar

```
E_new = E_old + E_solar
C_new = C_old
```

---

### 3. Discharge (Use Energy)

```
E_new = E_old - E_use
C_new = C_old - (S * E_use)
```

Where:

```
S = C_old / E_old
```

---

## Key Behaviour

- Solar reduces average cost (adds energy, no cost)
- Grid increases cost proportionally
- Discharge preserves weighted average
- No division-by-zero (handled explicitly)

---

# Worked Examples

Assume:

- `X = 0.10` (off-peak grid cost per kWh)
- `Y = 0.30` (peak grid cost — not used in battery calc directly)

---

## Scenario 1: No Solar (Grid Only)

| Step | Action                | E (kWh) | C ($) | S ($/kWh) |
|------|----------------------|--------|------|-----------|
| 1    | Start                | 0      | 0    | 0         |
| 2    | Charge 10 (grid)     | 10     | 1.00 | 0.10      |
| 3    | Use 5                | 5      | 0.50 | 0.10      |
| 4    | Charge 5 (grid)      | 10     | 1.00 | 0.10      |

---

## Scenario 2: Solar + Grid Mix

| Step | Action                | E (kWh) | C ($) | S ($/kWh) |
|------|----------------------|--------|------|-----------|
| 1    | Start                | 0      | 0    | 0         |
| 2    | Charge 5 (grid)      | 5      | 0.50 | 0.10      |
| 3    | Charge 5 (solar)     | 10     | 0.50 | 0.05      |
| 4    | Use 5                | 5      | 0.25 | 0.05      |
| 5    | Charge 5 (grid)      | 10     | 0.75 | 0.075     |

---

## Scenario 3: Solar Only

| Step | Action                | E (kWh) | C ($) | S ($/kWh) |
|------|----------------------|--------|------|-----------|
| 1    | Start                | 0      | 0    | 0         |
| 2    | Charge 10 (solar)    | 10     | 0    | 0         |
| 3    | Use 5                | 5      | 0    | 0         |
| 4    | Charge 5 (solar)     | 10     | 0    | 0         |

---

## Scenario 4: Mixed 5-Day Example

| Day | Action                | E (kWh) | C ($) | S ($/kWh) |
|-----|----------------------|--------|------|-----------|
| 1   | Start                | 0      | 0    | 0         |
| 1   | Charge 4 (grid)      | 4      | 0.40 | 0.10      |
| 1   | Charge 6 (solar)     | 10     | 0.40 | 0.04      |
| 1   | Use 3                | 7      | 0.28 | 0.04      |
| 2   | Charge 3 (grid)      | 10     | 0.58 | 0.058     |
| 2   | Use 5                | 5      | 0.29 | 0.058     |
| 3   | Charge 5 (solar)     | 10     | 0.29 | 0.029     |
| 3   | Use 8                | 2      | 0.23 | 0.115     |
| 4   | Charge 8 (grid)      | 10     | 1.03 | 0.103     |
| 4   | Use 5                | 5      | 0.52 | 0.103     |
| 5   | Charge 5 (solar)     | 10     | 0.52 | 0.052     |

---

## Summary

This model:

- Tracks cost basis of stored energy accurately
- Handles mixed charging sources
- Maintains correct weighted average pricing
- Avoids divide-by-zero issues

