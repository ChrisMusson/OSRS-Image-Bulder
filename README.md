## OSRS Image Builder
Given an initial image, this repository contains a `build.py` file that aims to build said image out of items found in Old School RuneScape. It does this by splitting the original image into 'boxes', finding the average colour of each box, choosing the item image that has the closest average colour to the colour that has just been found, and finally pasting these together to make an image.

### Examples
<img src="/examples/original/pocketwatch.png" width="300"/> <img src="/examples/built/pocketwatch.png" width="300"/>
