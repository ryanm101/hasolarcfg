# Solaredge Homeassistant Modbus integration config

This is effectively a copy of: https://community.home-assistant.io/t/solaredge-modbus-configuration-for-single-inverter-and-battery/464084 with some additions of my own such as tariffs. All credit for the inital work goes to https://community.home-assistant.io/u/remko/summary I've just added to what was done by remko. 

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
