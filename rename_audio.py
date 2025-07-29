import os
import csv
import re


def rename_audio_files(csv_file, audio_dir):
    """
    Renames audio files based on data in a CSV file and updates the CSV.

    Args:
        csv_file (str): Path to the CSV file.
        audio_dir (str): Path to the directory containing audio files.
    """

    # Create a dictionary to store audio file names without extensions
    audio_files = {
        os.path.splitext(f)[0]: f for f in os.listdir(audio_dir) if f.endswith(".mp3")
    }

    # Read the CSV file
    rows = []
    with open(csv_file, "r", encoding="utf-8") as infile:
        reader = csv.reader(infile, delimiter="|")
        for row in reader:
            if len(row) >= 2:
                id_col, name_col = row[0], row[1]
                new_filename = f"{id_col}_{name_col}.mp3"
                if name_col in audio_files:
                    old_filename = os.path.join(
                        audio_dir, audio_files[name_col])
                    new_filename_with_path = os.path.join(
                        audio_dir, new_filename)

                    # Rename the file
                    os.rename(old_filename, new_filename_with_path)
                    print(
                        f"Renamed '{old_filename}' to '{new_filename_with_path}'")

                    # Append the new filename to the row
                    row.append(f"[sound:{new_filename}]")
                else:
                    # Add an empty string if no audio file is found
                    print(f"No audio file found for {name_col}")
                    row.append("")
            else:
                row.append("")  # default value

            rows.append(row)

    # Write the updated data back to the CSV file
    with open(csv_file, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile, delimiter="|")
        writer.writerows(rows)
    print(f"Updated CSV file: {csv_file}")


if __name__ == "__main__":
    topic = "02_植物研究"
    csv_file_path = f"chapters/{topic}.csv"
    audio_directory = f"audioes/{topic}"  # 使用相对路径
    rename_audio_files(csv_file_path, audio_directory)
