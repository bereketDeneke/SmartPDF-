import os
from flask import render_template,send_file
from backend.Google import Translate
from backend.basic import *
from config import *
from backend.GPT_int import Summarizer
import traceback


def lang_mapping(lang):
    dic = {'amharic': 'amh', 'arabic': 'ara', 'english': 'eng','spanish': 'spa'}
    return dic[lang]

def File_Handler(language, req_type, file, word_limit):
    try:
        LogFile = open("LOG.txt", 'w', encoding="utf-8")
        LANGUAGE = lang_mapping(language)
        PAGES_INIT = "asset0001-"

        DeleteAllImageFiles('./Output')
        DeleteAllImageFiles('./Assets')
        DeleteAllImageFiles('./Result')
        images = extract(file)
        NUMBER_OF_FILES =  len(images) + 1 #len([name for name in os.listdir('/Assets') if os.path.isfile(os.path.join('./Assets', name))])
        NUMBER_OF_DIGITS = len(str(NUMBER_OF_FILES))

        LOWER_BOUND = 1
        UPPER_BOUND = NUMBER_OF_FILES
        content = []

        for i in range(LOWER_BOUND, UPPER_BOUND): 
            inputFilePath = f'./Assets/{PAGES_INIT}{i:0{NUMBER_OF_DIGITS}d}.png'
            outputFilePath = f'./Output/{PAGES_INIT}{i:01d}.png'
            
            try:
                content.append(INIT(inputFilePath, outputFilePath, req_type, LANGUAGE))
            except Exception as e:
                LogFile.write(inputFilePath + ': ' + str(e)+'\n')
                raise Exception(e)

        if req_type == 'transcription':
            saveTheFIle()
        else:
            Summary = Summarizer()
            textContent = " ".join(content)
            if LANGUAGE != 'eng':
                # result = open("./Result/translation.txt", 'w', encoding='utf-8')
                # result.write(f"Original Data:\n {textContent}")
                GTranslate = Translate()
                GTranslate.run(textContent)
                textContent = GTranslate.getTranslation()
                # result.write(f"Translated Data:\n{textContent}")
                # result.close()
                
            Summary.run(textContent, LANGUAGE, int(word_limit))
            return {'success': True, 'data':{'content': Summary.getResult()}}
            
        LogFile.close()
        return send_file(FILE_NAME, as_attachment=True)
    except Exception as e:
        traceback.print_exc()
        return {'status':f'Error >> {str(e)}'}