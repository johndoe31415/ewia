# ewia
[![Build Status](https://travis-ci.com/johndoe31415/ewia.svg?branch=master)](https://travis-ci.com/johndoe31415/ewia)

Ewia is a tool to calculate the apparent sky position (i.e., azimuth and
elevation) of astronomical objects such as stars or planets. It's an ancient
project of mine (dates back to 2009) and was almost completely rewritten in
2017. It's quite easy to use:

```
usage: ewia [-h] [--json] [-c filename] [--no-system-catalog] -l location
            [-t timestamp] [-z tzone]
            object [object ...]

positional arguments:
  object                Object under observation. Must refer to the catalog.

optional arguments:
  -h, --help            show this help message and exit
  --json                Output data in JSON format.
  -c filename, --user-catalog filename
                        Specifies user catalogs to read after system catalogs
                        have been read.
  --no-system-catalog   Do not read system catalogs (by default,
                        ~/.config/ewia/catalog.json and ./.catalog.json are
                        tried)
  -l location, --observer-location location
                        Observer location on earth. Can be either a reference
                        to the catalog or actual coordinates.
  -t timestamp, --observation-time timestamp
                        Time at which the observation is conducted. Accepts
                        the special argument 'now', which reflects the current
                        time. Otherwise, must be in format YYYY-mm-dd
                        HH:MM:SS.
  -z tzone, --observation-timezone tzone
                        When a timestamp is given, this parameter influences
                        at which timezone the timestamp is interpreted to be
                        in. Can either be a timezone definition such as
                        'Europe/Berlin' or a static timezone such as 'utc' or
                        'Etc/GMT+8'. Alternatively, can be set to 'auto' in
                        order to take the timezone that has been specified in
                        the catalog for the observing location. Defaults to
                        auto.
```

Catalogs are given in JSON format and an example is included in the
.catalog.json file. You can easily dump positions of objects:

```
$ ./ewia -l Böblingen Saturn
Observer location: Böblingen (N48°41′16″, E9°0′17″), at time 2017-08-16 22:40:42 (Europe/Berlin)
    Saturn: Altitude 16.1°, Azimuth 203.4° (SSW)
```

...or more objects at once...

```
$ ./ewia -l Böblingen Saturn Jupiter Venus Mars "Helix Nebula"
Observer location: Böblingen (N48°41′16″, E9°0′17″), at time 2017-08-16 22:41:18 (Europe/Berlin)
    Saturn: Altitude 16.1°, Azimuth 203.6° (SSW)
    Jupiter: Altitude -2.5°, Azimuth 263.0° (W)
    Venus: Altitude -19.6°, Azimuth 354.7° (N)
    Mars: Altitude -17.4°, Azimuth 324.6° (NW)
    Helix Nebula: Altitude 6.2°, Azimuth 131.7° (SE)
```

and also of course dump everything as JSON:

```
$ ./ewia -l Bamberg --json M17
{'observer': {'lat': 49.884559, 'lon': 10.888149, 'tz': 'Europe/Berlin'},
'timezone': 'Europe/Berlin', 'timestamps': [{'timet': 1535186887, 'ts_utc':
'2018-08-25 08:48:07', 'ts_local': '2018-08-25 10:48:07'}], 'observations':
[{'obj_name': 'M17', 'positions': [{'apparent': {'altitide': {'deg':
-52.158318500088335, 'pretty': '-52°9′30″'}, 'azimuth': {'deg':
34.639970963487116, 'pretty': '+34°38′24″'}}, 'equatorial': {'ra': {'hrs':
18.346666666666668, 'deg': 275.2, 'pretty': '18:20:48'}, 'dec': {'deg':
-16.183333333333334, 'pretty': '-16°11′0″'}}}]}]}
```

It can also calculate the position of the sun:

```
./ewia -l Böblingen Sol
Observer location: Böblingen (N48°41′16″, E9°0′17″), at time 2018-08-25 10:48:43 (Europe/Berlin)
    Sol: Altitude 39.9°, Azimuth 125.7° (SE)
```

# Author and License
Ewia was written by Johannes Bauer <JohannesBauer@gmx.de> and is released under
the terms of the GNU General Public License v2 (included in the LICENSE file).
