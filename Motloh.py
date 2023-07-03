from pathlib import Path
import re
from concurrent import futures


class Sorter:

    def __init__(self) -> None:

        self.MY_OTHER = []

        self.REGISTER_EXTENSION = {
            'JPEG': [[], 'images'],
            'JPG': [[], 'images'],
            'PNG': [[], 'images'],
            'SVG': [[], 'images'],
            'AVI': [[], 'video'],
            'MP4': [[], 'video'],
            'MOV': [[], 'video'],
            'MKV': [[], 'video'],
            'DOC': [[], 'documents'],
            'DOCX': [[], 'documents'],
            'TXT': [[], 'documents'],
            'PDF': [[], 'documents'],
            'XLSX': [[], 'documents'],
            'PPTX': [[], 'documents'],
            'MP3': [[], 'audio'],
            'OGG': [[], 'audio'],
            'WAV': [[], 'audio'],
            'AMR': [[], 'audio'],
            'ZIP': [[], 'archives'],
            'GZ': [[], 'archives'],
            'TAR': [[], 'archives']
        }

        self.FOLDERS = []
        self.EXTENTIONS = set()
        self.UNKNOWN = set()

    def cyrillic_symbols(self):
        return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'

    def transcription(self):
        return ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", 'i', "ji", "g")

    def trans(self):

        TRANSLATION = {}
        for cyrillic, latin in zip(self.cyrillic_symbols(), self.transcription()):
            TRANSLATION[ord(cyrillic)] = latin
            TRANSLATION[ord(cyrillic.upper())] = latin.upper()
        return TRANSLATION

    def normalize(self, name: str) -> str:

        el_name = name.translate(self.trans())
        el_name = re.sub(r'\W', '_', el_name)

        return el_name

    def get_extention(self, filename: str) -> str:
        return Path(filename).suffix[1:].upper()

    def scan(self, folder: Path):
        with futures.ThreadPoolExecutor() as executor:
            for item in folder.iterdir():
                if item.is_dir() and item.name not in ('archives', 'video', 'audio', 'documents', 'other' ):
                    self.FOLDERS.append(item)
                    executor.submit(self.scan, item)
                    continue


                ext = self.get_extention(item.name)
                full_name = folder / item.name
                if not ext:
                    self.MY_OTHER.append(full_name)
                else:
                    try:
                        container = self.REGISTER_EXTENSION[ext][0]
                        self.EXTENTIONS.add(ext)
                        container.append(full_name)
                    except KeyError:
                        self.UNKNOWN.add(ext)
                        self.MY_OTHER.append(full_name)

    def handle_file(self, filename: Path, target_folder: Path) -> None:
        target_folder.mkdir(exist_ok=True, parents=True)
        new_file_name = self.normalize(filename.stem) + filename.suffix
        filename.replace(
            target_folder / new_file_name)

    def handle_folder(self, folder: Path) -> None:
        try:
            folder.rmdir()
        except OSError:
            print(f'Sorry, we can not delate folder: {folder}')

    def mover(self, folder: Path) -> None:
        self.scan(folder)

        with concurrent.futures.ThreadPoolExecutor() as executor:

            futures = []
            for type, value in self.REGISTER_EXTENSION.items():
                folder_list, folder_name = value
                for file in folder_list:
                    target_folder = folder / folder_name / type
                    futures.append(executor.submit(self.handle_file, file, target_folder))

            for file in self.MY_OTHER:
                target_folder = folder / 'MY_OTHERS'
                futures.append(executor.submit(self.handle_file, file, target_folder))


            concurrent.futures.wait(futures)

        for folder in self.FOLDERS[::-1]:
            self.handle_folder(folder)


        self.data_cleaner()




    def data_cleaner(self):
        for value in self.REGISTER_EXTENSION.values():
            value[0] = []
        self.MY_OTHER = []
        self.FOLDERS = []
        self.EXTENTIONS = set()
        self.UNKNOWN = set()

    def sort(self, folder_for_scan):

        self.folder_for_scan = Path(folder_for_scan)
        self.mover(self.folder_for_scan.resolve())
        self.data_cleaner()

        return (
            f'The "{self.folder_for_scan.name}" had been successfully sorted!\n'
            f'Path: {self.folder_for_scan}'
        )



