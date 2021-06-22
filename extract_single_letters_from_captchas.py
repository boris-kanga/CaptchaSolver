import os
import os.path
import cv2
import glob
import imutils


CAPTCHA_IMAGE_FOLDER = "generated_captcha_images"
OUTPUT_FOLDER = "extracted_letter_images"


# Get a list of all the captcha images we need to process
captcha_image_files = glob.glob(os.path.join(CAPTCHA_IMAGE_FOLDER, "*"))
counts = {}

# loop over the image paths
for (i, captcha_image_file) in enumerate(captcha_image_files):
    print("[INFO] processing image {}/{}".format(i + 1, len(captcha_image_files)))

    # Since the filename contains the captcha text (i.e. "2A2X.png" has the text "2A2X"),
    # grab the base filename as the text
    filename = os.path.basename(captcha_image_file)
    captcha_correct_text = os.path.splitext(filename)[0].split()[0]
    print(captcha_correct_text)

    image = cv2.imread(captcha_image_file)
    gray = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
    gray = cv2.copyMakeBorder(gray, 8, 8, 8, 8, cv2.BORDER_REPLICATE)
    thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)[1]
    #cv2.imwrite('output_masked.png', thresh)
    cnts = cv2.findContours(thresh, 1, 2)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    h_min = 20
    w_min = 20
    crops_regions = []
    for c in cnts[:-1]:
        x, y, w, h = cv2.boundingRect(c)
        if h >= h_min and w >= w_min:
            crops_regions.append((x, y, w, h))


    final = sorted(crops_regions, key=lambda region: region[0])

    # If we found more or less than 4 letters in the captcha, our letter extraction
    # didn't work correcly. Skip the image instead of saving bad training data!
    if len(final) != len(captcha_correct_text):
        print("fail")
        continue

    # Save out each letter as a single image
    for letter_bounding_box, letter_text in zip(final, captcha_correct_text):
        # Grab the coordinates of the letter in the image
        x, y, w, h = letter_bounding_box

        # Extract the letter from the original image with a 2-pixel margin around the edge
        letter_image = gray[y - 2:y + h + 2, x - 2:x + w + 2]

        # Get the folder to save the image in
        save_path = os.path.join(OUTPUT_FOLDER, letter_text)

        # if the output directory does not exist, create it
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # write the letter image to a file
        count = counts.get(letter_text, 1)
        p = os.path.join(save_path, "{}.png".format(str(count).zfill(6)))
        try:
            cv2.imwrite(p, letter_image)
        except:
            pass

        # increment the count for the current key
        counts[letter_text] = count + 1
    print("FINISH")
