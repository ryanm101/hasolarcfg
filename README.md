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
```

* Copy the packages dir from this repo to `/config` on your home assistant installation


## Notes

* Check https://github.com/ryanm101/hasolarcfg/blob/actiontest/packages/energy_utilities.yaml as I use Tariffs with some non-standard billing cycles (monthly)
* Check https://github.com/ryanm101/hasolarcfg/blob/actiontest/packages/electricity_tarriff_automations.yaml as you many not want all the tariffs I do, (notably the `household_*` are old ones i need that I'm deprecating in my own code elsewhere)
* Check https://github.com/ryanm101/hasolarcfg/blob/actiontest/packages/energy_automations.yaml I change the battery during MY offpeak period yours may be different. This ideally should be a sensor for where i have specific times, but that is on the TODO. Also BEWARE I have an automation that Discharges the battery IF I can import cheaper than I export, if so I cycle between charge and discharge. THIS COULD COST YOU MONEY!!!!!!!!!
