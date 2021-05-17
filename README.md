# ha_philipssomneo
Custom component for controlling Philips Somneo Light settings and getting sensor data in Home Assistant


Config.yaml:

```yaml
philips_somneo:
  name: PhilipsSomneo
  host: <somneo_ip>
  scan_interval: <min. time between sensor updates (optional)>
  sensors:
    - temperature
    - humidity
    - light
    - noise
```
