from PyPDF2 import PdfReader
import pyttsx3
import os 

class PDfreader: 
    def __init__(self, file: str, size=50, audio_rate=200, multithread=False) -> None:
        self.file = file
        try:
            self.new_dir = os.path.join(os.getcwd(), f"{file.strip('.pdf')} audio") 
            os.mkdir(self.new_dir) # create new directory to store audio files 
        except: 
            pass 
        self.reader = PdfReader(file) # create reader object
        self.audioSpeaker(audio_rate) # create audio speaker object 
        self.loadPages() # load pages from pdf 
        self.run(size, multithread)
        
    def loadPages(self) -> None: 
        self.pages = []
        for i in range(len(self.reader.pages)): 
            self.pages.append(self.reader.pages[i].extract_text())
        self.page_length = len(self.pages)
        
    def audioSpeaker(self, rate: int) -> None: 
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('voice', 1.0)
        
    def saveAudio(self, text: str, audio_file: str) -> None: 
        self.engine.save_to_file(text, audio_file)
        
    def mergePages(self, file: list, start: int, length: int) -> None:
        self.merged_pages = ""
        for i in range(length): 
            try:
                self.merged_pages += file[start + i]
            except IndexError: 
                break 
        self.merged_pages = self.merged_pages.replace("\n", " ")
        
    def saveTextFile(self, file: str, text_file: str) -> None:
        with open(text_file, 'w') as txt_file: 
            txt_file.write(file)
            
    def replaceFileLocation(self, file_name: str) -> None: 
        current_path = os.path.join(os.getcwd(), file_name)
        new_path = os.path.join(self.new_dir, file_name)
        os.replace(current_path, new_path)
    
    def run(self, size: int, multithread: bool) -> None: 
        try:
            for i in range(0, self.page_length, size): 
                self.mergePages(self.pages, i, size) # merge pages together into a str
                file_path = f"Pages {i} - {i+size} {self.file.strip('.pdf')}.mp3"
                self.saveAudio(self.merged_pages, file_path) # str -> .mp3
                self.engine.runAndWait()
                self.replaceFileLocation(file_path) # move .mp3 to new dir
                print(f"Sucessfully translate pages: {i} - {i+size} ")
        except Exception as error: 
            print(f"Cannot complete task\n{error}")
            exit()
            
            
if __name__ == "__main__": 
    transcibe = PDfreader("The_intelligent_investor.pdf") 
    print('abc')
