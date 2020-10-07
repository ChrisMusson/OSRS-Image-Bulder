import cv2
import json
import numpy as np
from osrsbox import items_api


def main(remove_duplicates=True):
    """Creates a .json file that contains the RGB values for all item icons"""

    if remove_duplicates:
        # remove all duplicate items to lower search space for later colour-matching
        # most duplicate items are just noted items so make little difference in the final image
        # this step improves runtime of later colour-matching by ~50%
        items = [x for x in items_api.load() if not x.duplicate]
    else:
        items = items_api.load()

    # you can add/remove banned item IDs as you wish if for example one item always seems to dominate
    banned_IDs = [
        7586,  # Plain cream colour that fills entire icon - makes white areas of final image look bad
        9974,  # Giant eagle - matches too many pale tones
        22704,  # Portal nexus - matches lots of colours that often aren't visually similar
    ]
    # + list(range(3869, 3893))  # board game pieces - red versions of runes, red pixels always go to red fire rune

    rgb_dict = {}
    for item in items:
        try:
            myimg = cv2.imread(f"images/{item.id}.png")
            avg_color = np.average(np.average(myimg, axis=0), axis=0).tolist()
            if item.id not in banned_IDs:
                rgb_dict[item.id] = avg_color

        except np.AxisError:
            # some images that downloaded 'successfully' are still corrupt
            # print(item.id, item.name)
            pass

    with open("RGB_values.json", "w") as f:
        json.dump(rgb_dict, f)

if __name__ == "__main__":
    main(remove_duplicates=False)
