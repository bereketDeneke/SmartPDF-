# import os
# import zlib
import base64
# from flask import make_response, send_file
from backend.Google import Translate
from backend.basic import *
from config import *
from backend.GPT_int import Summarizer

def lang_mapping(lang):
    dic = {'amharic': 'amh', 'arabic': 'ara', 'english': 'eng','spanish': 'spa'}
    return dic[lang]

def File_Handler(language, req_type, file, word_limit):
    try:
        LANGUAGE = lang_mapping(language)
        PDF = PDFWriter()
        inputImages = extract(file)
        imageSize =  len(inputImages)
        content = []

        for i in range(imageSize): 
            try:
                content.append(INIT(inputImages[i], req_type, LANGUAGE, PDF))
            except Exception as e:
                raise Exception(e)

        if req_type == 'summary':
            Summary = Summarizer()
            textContent = " ".join(content)
            if LANGUAGE != 'eng':
                GTranslate = Translate()
                GTranslate.run(textContent)
                textContent = GTranslate.getTranslation()
                
            Summary.run(textContent, LANGUAGE, int(word_limit))
            return {'success': True, 'data':{'content': Summary.getResult()}}

        PDF.saveTheFIle()
        PDF.FILE_STREAM.seek(0)
        # response = zlib.compress(PDF.FILE_STREAM.getvalue())
        response = base64.b64encode(PDF.FILE_STREAM.getvalue())
        return response
    
    except Exception as e:
        # traceback.print_exc()
        return {'status':f'Error >> {str(e)}'}