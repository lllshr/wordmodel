from django.shortcuts import render
import segword
import event

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render,HttpResponse
@csrf_exempt
def wordmodel(request):
    try:
        with open('master-public.pem', 'rb') as f:
            key = f.read()
            rsakey = RSA.importKey(key)
            cipher = Cipher_pkcs1_v1_5.new(rsakey)
            jsonfrom = json.loads(request.body)
            id = jsonfrom['UUID']
            cipher_text = base64.b64encode(cipher.encrypt(id.encode('utf-8')))
            with open('log.log', 'a', encoding='utf-8-sig') as log:
                log.write(cipher_text+'\n')
            allContent = jsonfrom['allContent']
            json_data = process(id, allContent)
    except Exception as e:
        json_data ="{'info':" + e + "}"
    return HttpResponse(json_data,content_type='application/text');


def process(id, allContent):
    sw = segword.SegWord()
    words = sw.get_words(allContent)
    eve = event.Event()
    eve.loadmodel()
    eve_res = eve.classify(allContent.replace('\n', ''))
    json_data={"UUID":id,"separatedWords":','.join(words), "hotpointWords":eve_res}
    return str(json_data)
