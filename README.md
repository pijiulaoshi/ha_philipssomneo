# ha_philipssomneo
Custom component for controlling Philips Somneo Light settings and getting sensor data in Home Assistant


Config.yaml:

```yaml
philips_somneo:
  name: PhilipsSomneo
  host: <somneo_ip>
  scan_interval: <min. time in seconds between sensor updates (optional, default = 60)>
  sensors:
    - temperature
    - humidity
    - light
    - noise
```
