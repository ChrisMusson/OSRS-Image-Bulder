import argparse
import asyncio
import cv2
import json
import numpy as np
from datetime import datetime
from memoization import cached
from osrsbox import items_api


async def main():
    parser = argparse.ArgumentParser(description="Build an image from OSRS item icons")
    parser.add_argument("-in", required=True, dest="in_f", help="The name of the file you want to build.")
    parser.add_argument("-ou", dest="out_f", help="The name of the finished file")
    parser.add_argument("-wi", dest="num_boxes_w", help="The number of boxes to split the image into along its width.")
    parser.add_argument("-he", dest="num_boxes_h", help="The number of boxes to split the image into along its height.")

    args = parser.parse_args()
    args.out_f = args.out_f if args.out_f else args.in_f
    num_boxes_w = int(args.num_boxes_w) if args.num_boxes_w else 100
    num_boxes_h = int(args.num_boxes_h) if args.num_boxes_h else 80

    @cached
    async def get_pixels(item_ID):
        return cv2.imread(f"images/{item_ID}.png")

    @cached
    async def closest(colours, colour):
        distances = np.sqrt(np.sum((colours - colour) ** 2, axis=1))
        index_of_smallest = np.where(distances == np.amin(distances))
        best_match = colours[index_of_smallest].tolist()[0]
        return next((k for k, v in data.items() if v == best_match), None)
    
    img = cv2.imread(f"examples/original/{args.in_f}")
    img_w = len(img[0])
    img_h = len(img)
    box_w, box_h = img_w // num_boxes_w, img_h // num_boxes_h

    box_colours = []
    for j in range(num_boxes_h):
        row_data = []
        for k in range(num_boxes_w):
            pixels = [
                img[i][box_w * k : box_w * (k + 1)]
                for i in range(box_h * j, box_h * (j + 1))
            ]
            av = np.average(np.average(pixels, axis=0), axis=0)
            row_data.append(av)
        box_colours.append(row_data)

    with open("RGB_values.json", "r") as f:
        data = json.load(f)

    colours = np.array([tuple(x) for x in data.values()])

    tasks = [closest(colours, box) for row in box_colours for box in row]
    a = await asyncio.gather(*tasks)

    tasks2 = [get_pixels(x) for x in a]
    a2 = await asyncio.gather(*tasks2)
    
    final = np.concatenate(
        [
            np.concatenate(
                [x for x in a2[num_boxes_w * i : num_boxes_w * (i + 1)]], axis=1
            )
            for i in range(num_boxes_h)
        ],
        axis=0,
    )
    cv2.imwrite(f"examples/built/{args.out_f}", final)


if __name__ == "__main__":
    startTime = datetime.now()
    asyncio.get_event_loop().run_until_complete(main())
    print(f"Time taken: {datetime.now() - startTime}")