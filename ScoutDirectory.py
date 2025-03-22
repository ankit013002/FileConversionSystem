import os


class Scout:
    noncompatible_file_types = set([
        "heic", "HEIC", "WEBP", "CR2", "mov", "MOV"])
    noncompatible_video_file_types = set(["mov", "MOV"])

    def __init__(self, check_sub_directories):
        self.check_sub_directories = check_sub_directories
        self.file_types = set()
        self.number_of_files = 0

    def scout_directory(self, folder_path):
        for filename in os.listdir(folder_path):
            print(filename)
            if self.check_sub_directories and os.path.isdir(os.path.join(folder_path, filename)):
                self.scout_directory(os.path.join(folder_path, filename))
            else:
                if filename.split(".")[-1] != "json":
                    self.number_of_files += 1
                if filename.split(".")[-1] not in self.noncompatible_file_types:
                    self.file_types.add("." + filename.split(".")[-1])


def main():
    folder_path = input("Please enter your directory to scout: ")
    scout = Scout(True)
    scout.scout_directory(folder_path)

    print(f"File types: {scout.file_types}")
    print(f"Non-compatible file types: {scout.noncompatible_file_types}")
    print(f"Number of files: {scout.number_of_files}")


if __name__ == "__main__":
    main()
