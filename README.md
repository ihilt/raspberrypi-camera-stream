### Setup
Connect to wifi via `raspi-config`.

The `wpa_supplicant.conf` file could also be edited and copied over to
`/etc/wpa_supplicant/`.

Install libav-tools
```
sudo apt-get install libav-tools
```
and enable the camera through `raspi-config`.

`IgnoreSIGHUP=false` was needed in raspivid.service to get raspivid to work
under systemd.

Put the last part of the url `rtmp://a.rtmp.youtube.com/live2/XXXXX` in `/home/pi/.env`.

Install python-dotenv
`sudo pip install python-dotenv`

After copying the systemd service files over, run the following command
`sudo systemctl enable dispense.service`
