# -*- coding:utf-8 -*-
# Author: RubanSeven

import os
import cv2
import imageio
from augment import distort, stretch, perspective

def save_images(img_list, folder, prefix, base_name, resize_idx, augmentation_idx):
    if not os.path.exists(folder):
        os.makedirs(folder)  # Create the folder if it doesn't exist
    for idx, img in enumerate(img_list):
        filename = os.path.join(folder, f"{base_name}_resize{resize_idx}_aug{augmentation_idx + idx + 1}.jpg")
        cv2.imwrite(filename, img)
        print(f"Saved: {filename}")

# Function to process all images in a folder
def process_images(input_folder, output_folder):
    # Get a list of all image files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    resize_factors = [1 + 0.1 * k for k in range(-3, 4)]  # 7 factors: 1 original, 3 increased, 3 decreased

    for image_file in image_files:
        # Load the image
        image_path = os.path.join(input_folder, image_file)
        im = cv2.imread(image_path)
        if im is None:
            print(f"Failed to load image: {image_path}")
            continue

        # Get the original dimensions
        orig_h, orig_w = im.shape[:2]


        # Prepare to save augmented images
        base_name = os.path.splitext(image_file)[0]  # Extract the base name without extension

        # Process for each resize factor
        for resize_idx, factor in enumerate(resize_factors):
            # Calculate the new dimensions
            new_w = int(orig_w * factor)
            new_h = int(orig_h * factor)
            resized_im = cv2.resize(im, (new_w, new_h))

            # Prepare lists for augmentation
            distort_img_list = []
            stretch_img_list = []
            perspective_img_list = []

            # Apply augmentations
            for i in range(24):  # 24 distortions
                distort_img = distort(resized_im, 5)
                distort_img_list.append(distort_img)

            for i in range(24):  # 24 stretches
                stretch_img = stretch(resized_im, 4)
                stretch_img_list.append(stretch_img)

            for i in range(6):  # 6 perspectives
                perspective_img = perspective(resized_im)
                perspective_img_list.append(perspective_img)

            # Save augmented images
            save_images(distort_img_list, output_folder, "distort", base_name, resize_idx, 0)
            save_images(stretch_img_list, output_folder, "stretch", base_name, resize_idx, 24)
            save_images(perspective_img_list, output_folder, "perspective", base_name, resize_idx, 48)

if __name__ == '__main__':
    # Input and output folders
    input_folder = "imgs"  # Folder containing input images
    output_folder = "imgs/augment"  # Folder to save augmented images

    # Process all images in the input folder
    process_images(input_folder, output_folder)
