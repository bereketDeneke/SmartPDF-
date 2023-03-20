from googletrans import Translator
class Translate:
    def __init__(self):
        self.__translation = ""
        self.__max_length = 1500
    
    def group_text_content(self, content):
        groups = []
        while len(content) > self.__max_length:
            # Find the last space before the max length
            last_space_index = content.rfind(" ", 0, self.__max_length)
            
            if last_space_index == -1:
                # If no space is found, split the word
                groups.append(content[:self.__max_length])
                content = content[self.__max_length:]
            else:
                # If a space is found, split the content at the space
                groups.append(content[:last_space_index])
                content = content[last_space_index+1:]
        
        # Add the remaining content as the last group
        groups.append(content)
        return groups


    def run(self, content:str, __callback=None)->None:
        clean_text = content.replace('\n', ' ').split(' ')
        clean_text_list = [text.strip(' ') for text in clean_text if text !=' ']
        clean_text = " ".join(clean_text_list)
        self.__groups = self.group_text_content(clean_text)
        
        #[content[i:i+self.__max_length] for i in range(0, len(content), self.__max_length) if i+self.__max_length >= len(content) or content[i+self.__max_length].isspace()]

        for group in self.__groups:
            self.__translator = Translator()
            res = self.__translator.translate(group, dest='en')
            self.__translation += res.text

        if __callback is not None:
            __callback(self.__groups)
    
    def getTranslation(self)->str:
        return self.__translation