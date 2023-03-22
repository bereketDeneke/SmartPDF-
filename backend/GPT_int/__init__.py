import openai
openai.organization = "org-IQZQVAmBXlFmTlaJAiRzXGYx"
openai.api_key ="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"

class Summarizer:
    def __init__(self):
        self.__groups = []
        self.__iter = 0
        self.__summary = ''#[]
        self.__max_word_len = 3000 # word length limit
        self.__chunk_len = 150 # summarization of each 3000 word would be 100 words
    
    def __process(self, customPrompt):
        
        defaultPrompt = f"Summarize the following contents in just {self.__chunk_len} words only:"
        # defaultPrompt = f"generate imagery description for the following contents in just {self.__chunk_len} words only:"
        if customPrompt is not None:
            defaultPrompt = f"{customPrompt}. write your response in just {self.__chunk_len} words only: "

        prompt = f"""{defaultPrompt} {self.__summary}...{self.__groups[self.__iter]}"""

        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content":prompt}
                ]
            )

            result = completion.choices[0].message
            self.__summary = result.content
        except Exception as e:
            print("Warning: ", str(e))
            if "This model's maximum context length is " in str(e):
                b = [word for word in str(e).split() if word.isdigit()]
                limit, currVal = b
                diff = currVal - limit
                self.__summary = self.__summary[:-diff]
                # self.__max_word_len -= 800
                # self.__groups = [' '.join(self.__words[i:i+self.__max_word_len]) for i in range(0, len(self.__words), self.__max_word_len)]
                self.__process(customPrompt)
 
    
    def run(self, content, LANGUAGE='eng', wordLimit = 150, customPrompt=None, callback=None):
        self.__words = content.split()
        self.__chunk_len = wordLimit
        
        # 500 is a normalizer incase the summary goes beyond the limit which happens most often
        normalizer = 500
        if LANGUAGE != 'eng':
            normalizer = 700
        
        self.__max_word_len -= self.__chunk_len + normalizer

        self.__groups = [' '.join(self.__words[i:i+self.__max_word_len]) for i in range(0, len(self.__words), self.__max_word_len)]
        for i in range(len(self.__groups)):
            self.__process(customPrompt)
            if callback is not None:
                callback(self.__summary)

            self.__iter += 1
    
    def getResult(self):
        return self.__summary
