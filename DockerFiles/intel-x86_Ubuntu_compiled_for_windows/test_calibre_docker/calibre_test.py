import subprocess

def convert_to_epub(input_path, output_path):
    try:
        subprocess.run(['ebook-convert', input_path, output_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while converting the eBook: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
    return True

input_path = "/content/w.txt"
output_path = "/content/w.epub"

# Time to test it out!
if convert_to_epub(input_path, output_path):
    print("Conversion successful!")
else:
    print("Conversion failed.")
