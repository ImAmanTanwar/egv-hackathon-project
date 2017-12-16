from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
import datetime,traceback
from hackproject.models import Categories,SubCategories,Complains
import json,requests
import oauth2
import os
# Create your views here.

@api_view(['POST'])
def send(request):
    twitter_auth_token_key = os.environ['CLIENT_TWITTER_TOKEN_KEY']
    twitter_auth_token_secret = os.environ['CLIENT_TWITTER_TOKEN_SECRET']
    tweet = request.data['tweet_text']
    user_id = request.data['user_id']
    hashtags = request.data['hashtags']
    user_name = request.data['user_name']
    handle = request.data['handle']
    cat=check(hashtags)
    print cat
    category = Categories.objects.get(c_id=str(cat))
    categories = SubCategories.objects.filter(group_id=category)
    post_body="text=Select from below codes"+"\n"
    for c in categories:
        print c.service_name
        post_body+=c.service_name+" - "+c.service_code+"\n"
    post_body+="Please reply as <Phone Number>:<Status Code>:<Address>;screen_name="+handle
    try:
        lat=str(request.data['user_lat'])
    except:
        lat=""
    try:
        lon = str(request.data['user_lon'])
    except:
        lon=""
    obj = Complains(tweet=tweet,user_id=user_id,user_name=user_name,lat=lat,lon=lon)
    obj.save()
    #post_body = "status=@"+data["handle"]+" Please reply with your phone and email in Direct Message;in_reply_to_status_id="+data["tweet_id"]
    home_timeline = oauth_req( 'https://api.twitter.com/1.1/direct_messages/new.json', twitter_auth_token_key, twitter_auth_token_secret,post_body)
    post_body="user_id="+user_id+";follow=true"
    home_timeline = oauth_req( 'https://api.twitter.com/1.1/friendships/create.json', twitter_auth_token_key, twitter_auth_token_secret,post_body )
    print post_body

    return Response('{"status":"ok"}',status=status.HTTP_201_CREATED)

@api_view(['POST'])
def view(request):
    user_id = request.data["user_id"]
    message = request.data["message"]
    if "status" in message:
        code,srn_status=message.split()
        stat = get_srn_status(srn_status)
        post_body="user_id="+user_id+";text=Your Status is REGISTERED"
        home_timeline = oauth_req( 'https://api.twitter.com/1.1/direct_messages/new.json', twitter_auth_token_key, twitter_auth_token_secret,post_body)
    else:
        if ":" in message:
            phone, service_code,address = message.split(":")
        else:
            phone="0000000000"
            service_code="DEFAULT"
            address="Bangalore"
        print phone,service_code
        user = Complains.objects.filter(user_id=user_id,mobile_no="",service_code="")
        service_name=SubCategories.objects.get(service_code=service_code).service_name
        srn_num=""
        for u in user:
            u.mobile_no = phone
            u.service_code = service_code
            u.save()
            srn_num = getsrn(service_code,service_name,u.lat,u.lon,address,u.user_name,phone,u.tweet)
        print srn_num
        post_body="text=Complaint Registered successfully. SRN Number: "+srn_num+";user_id="+user_id
        home_timeline = oauth_req( 'https://api.twitter.com/1.1/direct_messages/new.json', twitter_auth_token_key, twitter_auth_token_secret,post_body)

        with open("srn.txt", "a") as myfile:
            myfile.write(srn_num+"\n")
    return Response('{"status":"ok"}',status=status.HTTP_201_CREATED)



def oauth_req(url, key, secret, post_body, http_method="POST", http_headers=None):
    twitter_key = os.environ['TWITTER_KEY']
    twitter_secret = os.environ['TWITTER_SECRET']
    consumer = oauth2.Consumer(key=twitter_key, secret=twitter_secret)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content

def check(st):
    a=['default','streetlight','engineering','health','administration','townplanning','revenue','watersupply']
    for i,j in enumerate(a):
        if j==st.lower():
            return i+1;

def getsrn(service_code,service_name,lat,lon,address,name,phone,tweet):
    print service_code+" "+service_name+" "+lat+" "+lon+" "+address+" "+name+" "+phone
    url=os.environ["EG_API_URL"]+"?jurisdiction_id=default"
    headers={"Content-Type":"application/json"}
    data={
   "RequestInfo":{
      "api_id":"org.egov.pgr",
      "ver":"1.0",
      "ts":"21-04-2017 15:55:37",
      "action":"POST",
      "did":"4354648646",
      "key":"xyz",
      "msg_id":"654654",
      "requester_id":"61",
      "auth_token":None
   },
   "ServiceRequest":{
      "service_code":service_code,
      "description":tweet,
      "address_id":"258",
      "lat":lat,
      "lng":lon,
      "address":"Near Central area",
      "service_request_id":"",
      "first_name":name,
      "phone":phone,
      "email":"kumar@ccc.com",
      "status":True,
      "service_name":service_name,
      "requested_datetime":"",
      "media_url":"",
      "tenantId":"default",
      "values":{
         "receivingMode":"Website",
         "receivingCenter":"",
         "status":"REGISTERED",
         "complainantAddress":"Near central bus stop"
      }
   }
}
    r = requests.post(url,data=json.dumps(data),headers=headers)
    print r
    return r.json()["service_requests"][0]["service_request_id"]

def get_srn_status(srn_num):
    url = os.environ["EG_API_URL"]
    params={"jurisdiction_id":"2",
            "service_request_id":srn_num
            }
    headers={
    "api_id":"org.egov.pgr",
    "ver":"1.0",
    "ts":"28-03-2016 10:22:33",
    "action":"GET",
    "did":"4354648646",
    "msg_id":"03447364-19c8-4ad0-a59d-ab2a385b19d5",
    "requester_id":"61",
    "auth_token":"null"
    }
    r=requests.get(url,headers=headers,params=params)
    print r.json()
