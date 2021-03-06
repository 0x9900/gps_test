
# GPS Info

This program run on linux and reads the information from the GPS
through the gps service daemon (gpsd).

# Python packages

The program `gps_test` depends on the python `gps` package. Use the
following command to install this package.

```
sudo pip install gps
```

### Example

     GPS readings
    ------------------------------------------------------------
    time utc     2019-12-29T22:38:22.000Z
    latitude     37.458263928
    longitude    -122.248755217
    altitude (m) 85.55
    eps          17.13
    epx          7.517
    epv          24.035
    ept          0.005
    speed (m/s)  0.0
    climb        0.0
    track        0.0
    mode         3
    grid         CM87vl
    satellites
            PRN:  16  E:  28  Az:  43  Ss:  39  Used: y
            PRN:  30  E:  22  Az: 262  Ss:  23  Used: y
            PRN:   9  E:  80  Az:  16  Ss:  39  Used: y
            PRN:   7  E:  53  Az: 283  Ss:  42  Used: y
            PRN:  23  E:  63  Az: 105  Ss:  44  Used: y
            PRN:   3  E:  17  Az: 174  Ss:  30  Used: y
            PRN:  26  E:   4  Az:  39  Ss:  20  Used: y
            PRN: 193  E:   2  Az: 307  Ss:  23  Used: y
            PRN:   8  E:  17  Az: 124  Ss:  13  Used: y
            PRN:  27  E:  20  Az:  90  Ss:  34  Used: y
            PRN: 131  E:  46  Az: 171  Ss:  34  Used: y
            PRN:   4  E:  42  Az: 313  Ss:   0  Used: n
    ------------------------------------------------------------
     Press [ Q ] to quit, [ Space ] Refresh
