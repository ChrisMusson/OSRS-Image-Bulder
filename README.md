## OSRS Image Builder
Given an initial image, this repository contains a `build.py` file that aims to build said image out of items found in Old School RuneScape. It does this by splitting the original image into 'boxes', finding the average colour of each box, choosing the item image that has the closest average colour to the colour that has just been found, and finally pasting these together to make an image.

### Examples
<img src="/examples/original/pocketwatch.png" width="300"/> <img src="/examples/built/pocketwatch.png" width="300"/>  
<img src="/examples/original/pool.png" width="300"/> <img src="/examples/built/pool.png" width="300"/>  
<img src="/examples/original/serrano.png" width="200"/> <img src="/examples/built/serrano.png" width="200"/>  
<img src="/examples/original/mandrill.jpg" width="300"/> <img src="/examples/built/mandrill.jpg" width="300"/>  
<img src="/examples/original/ash.jpg" width="300"/> <img src="/examples/built/ash.jpg" width="300"/>  

### Usage
1. Fork this repository
1. Clone this repository
1. `cd` into the cloned repository
1. Download an image you want to build and save it as `<name>.<extension>` in the `examples/original/` folder.
1. run `build.py`, specifying the name of the downloaded file and optionally the number of boxes to split your image into horizontally and vertically (default is 100x80). e.g. `python build.py -in pool.png -wi 150 -he 100`. The image, when built, will appear in the `examples/built/` folder.