from dotenv import load_dotenv
from requests import post, get
import os, base64, json, random, string, csv, time

#Program generates a random song id and outputs that song's audio features. 

#Next Steps: 
#Plan on optimizing it so that the audio features are outputted and parsed into a .csv file



load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers= headers, data= data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}



def search_for_track(token):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    # query = f"?q={track_name}&type=track&limit=1"

    
    character = random.choice(string.ascii_letters)
    i = random.randint(0,1)
    random_search = ""
    if(i == 0):
        random_search = character + "%"
    else:
        random_search = "%" + character + "%"

    offset = random.randint(0, 950)
    query = f"?q={random_search}&type=track&offset={offset}&markets=US&limit=50"

    query_url = url + query
    result = get(query_url, headers= headers)
    json_result = json.loads(result.content)["tracks"]["items"]
    if(len(json_result) == 0):
        print("No Track With This Name")
        return None
    
    idx = random.randint(0,49)
    return json_result[idx]
    
def get_audio_features(token, track_id):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_auth_header(token)
    result = get(url, headers= headers)
    json_result = json.loads(result.content)
    return json_result




token = get_token()
with open("ouput.csv", mode="a") as csvfile:
    fieldnames = ["Song Title", "Artist", "Popularity", "Duration", "Energy", "Instrumentalness", "Key", "Liveness", "Loudness", "Tempo", "Speechiness", "Time_Signature", "Danceability"]
    writer = csv.DictWriter(csvfile, fieldnames= fieldnames)
    for index in range(1, 5000):
        track = search_for_track(token)
        if(track == None):
            break
        else:
            if(index % 150 == 0):
                time.sleep(180)
            features = get_audio_features(token, track["id"])
            # print(features)
            artist = track["artists"][0]["name"]

            writer.writerow({"Song Title": track["name"], "Artist": artist, "Popularity": track["popularity"], "Duration": features["duration_ms"], "Energy": features["energy"], 
                            "Instrumentalness": features["instrumentalness"], "Key": features["key"], "Liveness": features["liveness"], "Loudness": features["loudness"], 
                            "Tempo": features['tempo'], "Speechiness": features["speechiness"], "Time_Signature": features["time_signature"], "Danceability": features["danceability"]})


