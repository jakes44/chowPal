import os
import random
from string import ascii_letters

from PIL import Image, ImageDraw

LINE_LV = '4'
WORD_LV = '5'

def get_text_info(img):
    filename = "".join([random.choice(ascii_letters) for _ in range(10)]) + ".png"
    out_loc = os.path.join("/tmp/", filename)
    img.save(out_loc)
    os.system("tesseract %s -psm 1 %s tsv" % (out_loc, out_loc))

    output = [] # [(this is a sentence, (top, left, bottom right))]

    sent_words = []
    left, top, width, height = -1, -1, -1, -1
    
    with open(out_loc + ".tsv", 'r') as in_file:
        for line in in_file:
            parts = in_file.split("\t")

            if parts[0] == 'level':
                continue
            elif parts[0] == LINE_LV:
                if top != -1:
                    sent = " ".join(sent_words)
                    sent_words = []
                    output.append((sent, (left, top, width, height)))

                left = int(parts[6])
                top = int(parts[7])
                width = int(parts[8])
                height = int(parts[9])

            elif parts[0] == WORD_LV:
                sent_words.append(parts[-1])

        sent = " ".join(sent_words)
        sent_words = []
        output.append((sent, (left, top, width, height)))

    return output


if __name__ == '__main__':
    image = Image.open("IMG_20180120_104252.jpg")
    output = get_text_info(image)

    draw = PIL.ImageDraw.Draw(image)

    for (sent, (l, t, w, h)) in output:
        print sent
        draw.rectangle([l, t, l+w, t+h], outline=128)

    image.show()
    

