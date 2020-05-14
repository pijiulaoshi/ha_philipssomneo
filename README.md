# ha_philipssomneo
Custom component for controlling Philips Somneo Light settings and getting sensor data in Home Assistant


Config.yaml:

```yaml
philips_somneo:
  name: PhilipsSomneo
  host: <somneo_ip>
  port: <port> optional (I think it is always the same)
  sensors:
    - temperature
    - humidity
    - light
    - noise
```
