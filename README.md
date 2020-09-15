# Features
- Convert CVAT format to YOLO format and vice versa
- Convert CVAT format to WPOD format and vice versa
- Convert CVAT format to Cloud9 solution format

# CVAT format example for polygon box
```xml
<?xml version="1.0" encoding="utf-8"?>
<annotations>
    <image id="0" name="images_car_069 (1)_0.jpg" width="201" height="137">
        <polygon label="license_plate" occluded="0" source="manual" points="16.50,91.00;38.60,90.80;38.10,106.50;16.30,106.60">
        </polygon>
    </image>
    <image id="1" name="images_car_069 (1)_1.jpg" width="272" height="162">
        <polygon label="license_plate" occluded="0" source="manual" points="41.30,109.70;79.20,110.40;89.50,130.20;47.80,131.10">
        </polygon>
    </image>
</annotations>
```

# CVAT format example for rectangle box
```xml
<annotations>
        <image id="8" name="7+Japanese+4x4+Mini+truck++container1105.png" width="1280" height="720">
        <box label="truck" occluded="0" source="manual" xtl="211.36" ytl="32.45" xbr="1280.00" ybr="543.30">
        </box>
        <box label="license_plate" occluded="0" source="manual" xtl="283.78" ytl="451.67" xbr="331.78" ybr="489.85">
        </box>
    </image>
    <image id="9" name="7+Japanese+4x4+Mini+truck++container1312.png" width="1280" height="720">
        <box label="license_plate" occluded="0" source="manual" xtl="208.51" ytl="460.40" xbr="261.96" ybr="505.13">
        </box>
        <box label="truck" occluded="0" source="manual" xtl="133.45" ytl="0.00" xbr="1280.00" ybr="580.50">
        </box>
    </image>
</annotations>
```

# YOLO format example
```bash
# class_index center_x center_y width_box height_box
# a.txt
2 0.799844 0.595833 0.174531 0.236111
2 0.660273 0.554792 0.084609 0.09875
7 0.176797 0.528472 0.185781 0.148611
2 0.897879 0.559667 0.054867 0.097222
# b.txt
1 0.05975 0.515996 0.1195 0.51928
2 0.80725 0.505297 0.3855 0.391949
0 0.47305 0.541451 0.6154 0.470911
```

# WPOD format
```bash
# N,tlx,tly,trx,try,brx,bry,blx,bly,LABEL,
# where:
#	    - N = number or corners (fixed in 4)
#    	- tl[x,y] = top left corner
#	    - tr[x,y] = top right corner
#	    - br[x,y] = bottom right corner
#	    - bl[x,y] = bottom left corner
#       - all values are normalized between 0 and 1.

# a.txt
4,0.283884,0.437185,0.441072,0.287771,0.556470,0.557144,0.687160,0.686486,,
4,0.839851,0.890071,0.895865,0.845645,0.030926,0.017160,0.072296,0.086062,,
# b.txt
4,0.658657,0.811692,0.813814,0.660779,0.606070,0.561978,0.661459,0.705551,,
```