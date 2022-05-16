# Connect your Pi to your phone's hotspot

The easiest way to connect to your Pi from your laptop while you're at EMF is via a phone hotspot (maybe?)

## `/etc/wpa_supplicant/wpa_supplicant.conf`

You can set multiple networks, with different priorities:

```
country=GB
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
ap_scan=1

update_config=1
network={
	ssid="my_home_network"
	psk=somebighexstring
	priority=10
}

network={
	ssid="my_phone_hotspot"
	psk="some_password"
	proto=RSN
	key_mgmt=WPA-PSK
	pairwise=CCMP
	auth_alg=OPEN
	priority=20
}
```

It seems to connect to the highest-priority network I can see when it boots - you can force it to do rediscovery with

```
sudo wpa_cli -i wlan0 reconfigure
```
