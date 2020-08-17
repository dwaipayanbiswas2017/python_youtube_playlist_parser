import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse
import json

# update the working directory
root_dir = "<working_dir>"


url = input("Enter youtube playlist id : ")
query = parse_qs(urlparse(url).query, keep_blank_values=True)
playlist_id = query["list"][0]

print(f'get all playlist items links from {playlist_id}')

# Update your Google API-KEY with the developerKey
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = "API-KEY")

request = youtube.playlistItems().list(
	part = "snippet",
	playlistId = playlist_id,
	maxResults = 50
)
response = request.execute()

playlist_items = []
while request is not None:
	response = request.execute()
	playlist_items += response["items"]
	request = youtube.playlistItems().list_next(request, response)

print("\n")
count = 1

youtube_playlist = dict()
video_list = list()

for t in playlist_items:
	if(t['snippet']['title'] != "Deleted video"):
		print(count,") Title : ",t['snippet']['title'],"\n\tLink : https://www.youtube.com/watch?v=",t['snippet']['resourceId']['videoId'])
		video_dict = dict()
		video_dict['video_number'] = count
		video_dict['title'] = t['snippet']['title']
		video_dict['link'] = "https://www.youtube.com/watch?v="+t['snippet']['resourceId']['videoId']
		video_list.append(video_dict)
		count += 1

youtube_playlist['video_list'] = video_list
youtube_playlist['total_videos'] = count

json_object = json.dumps(youtube_playlist, indent = 4)

with open(root_dir+"youtube_playlist.json", "w") as outfile:
	outfile.write(json_object)

print("Json file dump completed...")