#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2015-06-28 14:22:20
# @Last Modified by:   codykochmann
# @Last Modified time: 2015-06-28 16:45:05

saved_shows=["silicon_valley"]

show_name_in_url=raw_input("what's the name of the show in the watch-series-tv url?\n")

def grep(link):
    import urllib2
    return urllib2.urlopen(link).read()

def find_all_matches(input_string,pattern):
  import re
  return re.findall(pattern, input_string)

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
    "episode_id":find_all_matches(episode_url, "s[0-9]_e[0-9]{1,2}")[0]
  }
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

import json
database_name=show_name_in_url+".json"
print "Generating database: %s" % database_name

with open(database_name,'w') as f:
  file_output = json.dumps(episodes, sort_keys=True, indent=2, separators=(',', ': '))
  f.write(file_output)

print "process complete."

season_number = raw_input("which season do you need?\n")
episode_number = raw_input("which episode number?\n")

for e in episodes:
  if "s"+season_number in e['episode_id']:
    if "e"+episode_number in e['episode_id']:
      for p in e['providers']:
        try:
          print find_all_matches(grep(p['url']), "(http://daclips.in/[a-z0-9]{12})|(http://vodlocker.com/[a-z0-9]{12})")
        except:
          pass



