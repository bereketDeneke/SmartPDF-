from backend.Google import Translate
from test_cont import content
from backend.GPT_int import Summarizer
def grouping(groups):
    # f =  open('groups.txt', 'w', encoding="utf-8")
    # for group in groups:
    #     f.write(group)
    # f.close()
    pass

# pattern = re.compile("[\u1200-\u137F\s]+")
# Remove unknown characters from the Amharic text
# clean_text = content.replace('\n', ' ') #"".join([char for char in content if re.match(pattern, char)])
# clean_text = clean_text.split(' ')
# clean_text = " ".join([text.strip(' ') for text in clean_text if text !=' '])
translate = Translate()
f= open("test.txt", "w", encoding="utf-8")
translate.run(content['english'], grouping)

def update(summary):
  f.write(summary)

b = translate.getTranslation()
prompt = "Write essay based on the thesis statement,\"The impact of the Santorini eruption on Minoan Crete illustrates the importance of infrastructure and societal resilience in disaster preparedness\",from the content provided below and use APA inline citation to support your argument."
prompt = "why is the following code always start the zoom Level from 1 instead of the current zoom level:"
summary = Summarizer()
summary.run(content=content['code'], LANGUAGE='amharic', wordLimit=1000, callback=update, customPrompt=prompt)#"Bullet point important points for making argument regarding airport service quality: ")
summary_c = summary.getResult()

f.write(summary_c)
f.close()
