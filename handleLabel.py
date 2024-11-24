def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Split the line into image name and text
            parts = line.strip().split('\t')
            if len(parts) != 2:
                continue  # Skip malformed lines
            
            image_name, text = parts

            # Generate 378 new lines with the specified postfixes
            for resize_idx in range(7):  # 0 to 6
                for aug_idx in range(1, 55):  # 1 to 54
                    new_image_name = f"{image_name.split('.')[0]}_resize{resize_idx}_aug{aug_idx}.jpg"
                    outfile.write(f"augment/{new_image_name}\t{text}\n")

    print(f"Processing complete. Output written to {output_file}")


# Example usage
input_file = "all.txt"  # Replace with your input file name
output_file = "imgs/augment_label.txt"  # Replace with your desired output file name
process_file(input_file, output_file)
