import requests
import logging
import hmac
import codecs
import hashlib
import json
import time
import copy
import urllib3
from urllib.parse import urlparse
from flask import Flask,request,make_response,redirect,Response,jsonify
urllib3.disable_warnings()

class Aynaott():
	def __init__(self,api_products,api_channels_list,stream_referer):
		self.api_products=api_products
		self.api_channels_list=api_channels_list
		self.stream_referer=stream_referer
		self.host='https://'+urlparse(self.api_products).netloc
	def get_akamai_key(self) -> str:
		req=requests.get(self.api_products,verify=False)
		try:
			akamai_key=req.json()['player']['token']['akamai_key']
			return True,akamai_key
		except Exception as error:
			return False,error
	def get_all_channels(self) -> list:
		req=requests.get(self.api_channels_list,verify=False)
		try:
			all_data_list=[]
			data=req.json()['data'][0]
			for category in data['categories']:
				if 'ALL' in json.dumps(category):
					None
				else:
					continue
				for channel in category['channels']:
					channel_data={
					'name':channel['name'],
					'id':channel['_id'],
					'logo':self.host+'/'+channel['images']['square'],
					'referer':self.stream_referer,
					'stream_url':channel['streams']['channels']['urls']['ios_tvos']
					}
					all_data_list.append(channel_data)
			return True,all_data_list
		except Exception as error:
			return False,str(error)
	@staticmethod
	def hmac_hash_sign(stream_url,signature,ip_address,akamai_key) -> str:
		#Generate Hmac Hash
		qwery_paramiter_data=f"st={int(time.time())}~exp={int(time.time())+43200}~acl=/{signature}/*~data={ip_address}-WEB"
		hmac_sha256 = hmac.new(codecs.decode(akamai_key,'hex'),qwery_paramiter_data.encode(), hashlib.sha256)
		hmac_hash = hmac_sha256.hexdigest()
		final_stream_url=stream_url+"?hdnts="+qwery_paramiter_data+"~hmac="+hmac_hash
		return final_stream_url
		

				
		

def hybrid_playlist_converter(data:dict) -> str:
	playlist_text="#EXTM3U\n"
	for channel in data:
		category=channel.get('category','')
		channel_id=channel.get('id')
		name=channel.get('name','')
		logo=channel.get('logo','')
		stream_url=channel.get('link','')
		host=channel.get('host',False)
		cookie=channel.get('cookie',False)
		referer=channel.get('referer',False)
		playlist_text+=f'#EXTINF:-1 group-title="{category}" tvg-chno="{channel_id}" tvg-id="{channel_id}" tvg-logo="{logo}", {name}'
		headers_data={}
		if cookie !=False:
		      headers_data["cookie"]=cookie
		if referer !=False:
			headers_data["referer"]=referer
			playlist_text+='\n'+'#EXTVLCOPT:http-referrer='+referer
			if len(headers_data) !=0:
			     playlist_text+='\n'+'#EXTHTTP:'+json.dumps(headers_data)
		playlist_text+='\n'+stream_url+'\n'
	try:
		with open("hybrid_playlist.m3u","w") as w:
		   w.write(playlist_text)
		return playlist_text
	except:return playlist_text
def ns_player_playlist_converter(output_file_name:str,json_data:dict) -> str:
    import json
    all_data_ns=[]
    for channel in json_data:
        data={
        "name":channel.get('name',''),
        "link":channel.get('link',''),
        "logo":channel.get('logo',''),
        "referer":channel.get('referer',""),
        "referrer":channel.get('referer',""),
        "userAgent":"(Linux;Telegram:https://t.me/J_9X_H_9X_N) Github:https://github.com/byte-capsule AndroidXMedia3/1.1.1/64103898/4d2ec9b8c7534adc",
         }
        all_data_ns.append(data)
    try:
    	with open(output_file_name,"w") as w:
    		json.dump(all_data_ns,w,indent=2)
    	return all_data_ns
    except:
    	return all_data_ns




#Aynaott Latest Script
#Made by : Byte Capsule  | https://github.com/byte-capsule
#Date : 16 Dec 2024


#___________________________________API SETUP___________________________________
#API - ALL CHANNEL FROM AYNAOTT
api_channel='https://cloudtv.akamaized.net/AynaOTT/BDcontent/channels/bundles/652fcf82a2649538da6fc6e3_bundle.json'
#API -FOR AKAMAI KEY
api_key='https://cloudtv.akamaized.net/AynaOTT/BDcontent/BD/products/66e88378c4ae462999bf0159_product.json'
#REFRER URL FOR STREAM M3U8
strem_referer_url='https://cloudtv.akamaized.net/'
#_________________________________________________________________________________


aynaott=Aynaott(api_key,api_channel,strem_referer_url)
app=Flask(__name__)

@app.route("/")
def home():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            "endpoint": rule.endpoint,
            "methods": ', '.join(rule.methods - {'HEAD', 'OPTIONS'}),
            "url": request.url_root.strip('/') + rule.rule  # Prepend request.url_root
        })
    
    table_html = """
    <html>
        <head>
            <title>Flask Routes</title>
            <style>
                table {
                    width: 60%;
                    border-collapse: collapse;
                    margin: 20px auto;
                }
                th, td {
                    padding: 10px;
                    border: 1px solid #ddd;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
                }
                tr:nth-child(even) {
                    background-color: #f9f9f9;
                }
                h1 {
                    text-align: center;
                }
                footer {
                    margin-top: 20px;
                    text-align: center;
                    font-size: 14px;
                    color: #555;
                }
                footer a {
                    color: #007BFF;
                    text-decoration: none;
                }
                footer a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <h1>Available Flask Routes</h1>
            <table>
                <tr>
                    <th>Endpoint</th>
                    <th>Methods</th>
                    <th>Full URL</th>
                </tr>
    """
    for route in routes:
        table_html += f"""
            <tr>
                <td>{route['endpoint']}</td>
                <td>{route['methods']}</td>
                <td>{route['url']}</td>
            </tr>
        """
    table_html += """
            </table>
            <footer>
                ♥️ Made BY <a href="https://github.com/byte-capsule" target="_blank">BYTE Capsule</a>
            </footer>
        </body>
    </html>
    """
    return table_html
	
@app.route("/api/aynaott/hybrid.m3u")
def generate_hybrid_playlist():
    #DETERMINE USER IP ADDRESS
    if request.host.startswith('127.0.0.1') or request.host.startswith('localhost'):
    	user_ip_addr=requests.get('http://ip-api.com/json/').json()['query']
    else:user_ip_addr=request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr).split(',')[0]
    #FETCH ALL CHANNELS INFO FROM AYNAOTT
    fetch_success,channels_data_list=aynaott.get_all_channels()
    if not fetch_success:return jsonify({'error': 'Failed to fetch channel data','message':'Check The Api Please','details': channels_data_list}), 500
    #SIGN CHANNEL USING	 HMC HASH (AKAMAI_KEY)
    fetch_success,akamai_key=aynaott.get_akamai_key()
    if not fetch_success:return jsonify({'error': 'Failed to fetch Akamai Key','message':'Check The Api Please','details': akamai_key}), 500	
    channel_data_list_signed = copy.deepcopy(channels_data_list)
    for channel in channel_data_list_signed:
    	channel['link']=aynaott.hmac_hash_sign(channel["stream_url"],'byte-capsule',user_ip_addr,akamai_key)
    return hybrid_playlist_converter(channel_data_list_signed)

@app.route("/api/aynaott/ns_player.m3u")
def generate_ns_player_playlist():
    #DETERMINE USER IP ADDRESS
    if request.host.startswith('127.0.0.1') or request.host.startswith('localhost'):
    	user_ip_addr=requests.get('http://ip-api.com/json/').json()['query']
    else:user_ip_addr=request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr).split(',')[0]
    #FETCH ALL CHANNELS INFO FROM AYNAOTT
    fetch_success,channels_data_list=aynaott.get_all_channels()
    if not fetch_success:return jsonify({'error': 'Failed to fetch channel data','message':'Check The Api Please','details': channels_data_list}), 500
    #SIGN CHANNEL USING	 HMC HASH (AKAMAI_KEY)
    fetch_success,akamai_key=aynaott.get_akamai_key()
    if not fetch_success:return jsonify({'error': 'Failed to fetch Akamai Key','message':'Check The Api Please','details': akamai_key}), 500	
    channel_data_list_signed = copy.deepcopy(channels_data_list)
    for channel in channel_data_list_signed:
    	channel['link']=aynaott.hmac_hash_sign(channel["stream_url"],'byte-capsule',user_ip_addr,akamai_key)
    return ns_player_playlist_converter('NS_player.m3u',channel_data_list_signed)

@app.route("/api/aynaott/channel.json")
def generate_json():
	 #FETCH ALL CHANNELS INFO FROM AYNAOTT
    fetch_success,channels_data_list=aynaott.get_all_channels()
    if not fetch_success:return jsonify({'error': 'Failed to fetch channel data','message':'Check The Api Please','details': channels_data_list}), 500
    all_data=[]
    count=0
    for channel in channels_data_list:
    	data={'id':count,'name':channel['name'],'logo':channel['logo'],'link':request.url_root+'/api/aynaott/play.m3u8?channel_id='+str(count)}
    	all_data.append(data)
    	count+=1
    return jsonify(all_data)

@app.route("/api/aynaott/play.m3u8")
def generate_stream_url():
    #GET THE CHANNEL ID
    channel_id=request.args.get('channel_id',0)
    #DETERMINE USER IP ADDRESS
    if request.host.startswith('127.0.0.1') or request.host.startswith('localhost'):
    	user_ip_addr=requests.get('http://ip-api.com/json/').json()['query']
    else:user_ip_addr=request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr).split(',')[0]
    #FETCH ALL CHANNELS INFO FROM AYNAOTT
    fetch_success,channels_data_list=aynaott.get_all_channels()
    if not fetch_success:return jsonify({'error': 'Failed to fetch channel data','message':'Check The Api Please','details': channels_data_list}), 500
    #SIGN CHANNEL USING	 HMC HASH (AKAMAI_KEY)
    fetch_success,akamai_key=aynaott.get_akamai_key()
    if not fetch_success:return jsonify({'error': 'Failed to fetch Akamai Key','message':'Check The Api Please','details': akamai_key}), 500
    try:
    	stream_url=channels_data_list[int(channel_id)]['stream_url']
    except:
    	return 'Channnel Not Found ',500
    stream_url_signed=aynaott.hmac_hash_sign(stream_url,'byte-capsule',user_ip_addr,akamai_key)
    #REDIRECT TO STREAM URL
    response = Response(status=302)
    response.headers['Location'] =stream_url_signed
    return response


if __name__ == '__main__':
    app.run(debug=False)
    
