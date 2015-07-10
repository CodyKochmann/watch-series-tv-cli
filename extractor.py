#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2015-06-28 14:22:20
# @Last Modified by:   codykochmann
# @Last Modified time: 2015-07-01 10:51:57

def find_all_matches(input_string,pattern):
  import re
  return re.findall(pattern, input_string)

SAVED_SHOW_IDENTIFIER="$SAVED_SHOW"
WORKSPACE_FILE='extractor.workspace'

def read_file(path):
  with open(path,'r') as f:
    out = f.read()
    return out

def save_show(show_id):
  global WORKSPACE_FILE
  from os import listdir
  if WORKSPACE_FILE not in listdir("./"):
    with open(WORKSPACE_FILE,'w') as f:
      f.write("#this is a workspace file for extractor.py in the watch-series-tv-cli\n")

  if show_id not in read_file(WORKSPACE_FILE):
    with open('extractor.workspace','a') as f:
      f.write(SAVED_SHOW_IDENTIFIER + " " + show_id +"\n")

saved_shows = find_all_matches(read_file(WORKSPACE_FILE), "\$SAVED_SHOW\s[a-z_]{1,30}")
t=[]
for i in saved_shows:
  t.append(i.split(" ")[1])
saved_shows=t
del t

print "your show history:\n  %s" % ('  \n'.join(saved_shows))
show_name_in_url=raw_input("what's the name of the show in the watch-series-tv url?\n")

save_show(show_name_in_url)

def grep(link):
    import urllib2
    return urllib2.urlopen(link).read()



silicon_valley_url = "http://watch-series-tv.to/serie/"+show_name_in_url
watch_series_url="http://watch-series-tv.to"

episode_regex = "/episode/%s_s[0-9]_e[1-9][0-9]?.html" % (show_name_in_url)
provider_regex = "/open/cale/[0-9]{6,10}.html"

our_prefered_providers='/open/cale/[0-9]{6,10}.html["\sa-z=\.]{0,64}(vodlocker\.com|daclips\.in)'
our_prefered_providers='/open/cale/[0-9]{6,10}.html["\sa-z=\.]{0,128}'
provider_name_regex="""(vodlocker\.com|daclips\.in)"""

video_hosts_regex=[
  "http://daclips.in/[a-z0-9]{12}",
  "http://vodlocker.com/[a-z0-9]{12}"
]

def extract_host(link):
  global video_hosts_regex
  output = []
  for i in video_hosts_regex:
    links=find_all_matches(grep(link), i)
    if len(links) >0:
      print links[0]
  print output

episode_links = list(set(find_all_matches(grep(silicon_valley_url),episode_regex)))

tmp = []
for i in episode_links:
  tmp.append(watch_series_url+i)
episode_links = sorted(tmp)

def announce_episodes(episode_links):
  seasons = find_all_matches("\n".join(episode_links), "s[0-9]{1,2}")
  s={}
  print "Episodes found:"
  for i in seasons:
    s[i]=[]
  for i in s:
    o=i+":"
    for x in range(len(find_all_matches("\n".join(episode_links), i))):
      o+= " "+str(x+1)
    print(o)

announce_episodes(episode_links)

season_number = raw_input("which season do you need?\n")
episode_number = raw_input("which episode number?\n")

#exit()

episodes=[]

def create_episode_object(episode_url):
  global watch_series_url
  global episodes
  global provider_regex
  tmp = find_all_matches(grep(episode_url), our_prefered_providers)
  output = []
  for i in tmp:
    url = find_all_matches(i, provider_regex)
    name= find_all_matches(i, provider_name_regex)
    if len(name) > 0 and len(url) > 0:
      output.append({"name":name[0],"url":watch_series_url+url[0]})
  output = {
    "episode":episode_url,
    "providers":output,
    "episode_id":find_all_matches(episode_url, "s[0-9]{1,2}_e[0-9]{1,2}")[0]
  }
  output["episode_number"]=find_all_matches(output["episode_id"].split("_")[1], "[0-9]{1,2}")[0]
  output["season_number"]=find_all_matches(output["episode_id"].split("_")[0], "[0-9]{1,2}")[0]
  episodes.append(output)
  return [output['episode_id'],"providers found: %s"%(len(output["providers"]))]

progress=0.0
for i in episode_links:
  try:
    progress+=1.0
    report = create_episode_object(i)
    report = [str(int(100.0*(progress/len(episode_links))))+"%",report[0],report[1]] 
    print " ---- ".join(report) 
  except:
    pass

def save_local_json_db(database_name="db.json",json_data={}):
  import json
  print "Generating database: %s" % database_name
  with open(database_name,'w') as f:
    file_output = json.dumps(json_data, sort_keys=True, indent=2, separators=(',', ': '))
    f.write(file_output)

SAVE_LOCAL_DATABASE=False

if SAVE_LOCAL_DATABASE:
  # holding this code off for a little later.
  database_name=show_name_in_url+".json"
  save_local_json_db(database_name,episodes)

print "process complete."


for e in episodes:
  if "s"+season_number in e['episode_id']:
    if "e"+episode_number in e['episode_id']:
      for p in e['providers']:
        try:
          tmp= str(find_all_matches(grep(p['url']), "(http://daclips.in/[a-z0-9]{12})|(http://vodlocker.com/[a-z0-9]{12})"))
          print find_all_matches(tmp, "http://[a-z\.]{1,20}/[a-z0-9A-Z\.]{1,20}")[0]
        except:
          pass



