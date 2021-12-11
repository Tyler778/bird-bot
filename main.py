import os
import discord
import requests
import json
from random import randrange
#from replit import db





def get_coords(place):
  url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + place + '&key=' + geo_key
  response = requests.request("GET", url)
  json_d = json.loads(response.text)
  return json_d['results'][0]['geometry']['location']

headers = {
  'X-eBirdApiToken': ebird_key
}

client = discord.Client()

def get_nearby(place, count):
  payload={}
  lng = get_coords(place)['lng']
  lat = get_coords(place)['lat']

  url = 'https://api.ebird.org/v2/data/obs/geo/recent/notable?lat=' + str(lat) + '&lng=' + str(lng) + '&maxResults=' + str(count) + '&sppLocale=en&dist=50'
  response = requests.request("GET", url, headers=headers, data=payload)
  response.raise_for_status()
  generate_string(response.json(), count)
  if response.status_code != 204:
    return response.json()


def generate_string(json, count):
  statement = ''
  e = 0
  try:
    
    while e < int(count):
      statement = statement + '\n' + json[e]['comName']
      e+=1

    if int(count) == 1:
      statement = statement + '\nhas been observed nearby!'
    else:
      statement = statement + '\nhave been observed nearby!'
  
  except:
    statement = "There's not enough notable sightings for your request!"
  return statement
#change

@client.event

async def on_ready():
  print('We have logged in')


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith('$bird'):
    await message.channel.send('I am Bird Bot.\nPlease use command $help for commands!')
  if message.content.startswith('$help'):
    await message.channel.send('$ <COMMAND>\n'
                                  'nearby <{location}> <{count}> #returns count notable observations nearby the location#\n'
                                  'random <{count}> #returns random bird of count#\n'
                                  'where <{location}> #returns coordinates of location#')

  if message.content.startswith('$nearby'):
    cnt = 1
    try:
      cnt = message.content.split()[2]
    except:
      pass
    try:
      loc = message.content.split()[1]
    except:
      await message.channel.send("Maybe you should put a location?")
    await message.channel.send(generate_string(get_nearby(loc, cnt),cnt))

  if message.content.startswith('$random'):
    cnt = 1
    try:
      cnt = message.content.split()[1]
    except:
      pass

    for x in range(0, int(cnt)):
      ran = randrange(2059)
      val = db[str(ran)]
      await message.channel.send(val)
  if message.content.startswith('$imagetest'):
    url = 'https://i.imgur.com/P7pxzQm.jpeg'
    await message.channel.send(url)

  if message.content.startswith('$where'):
    loc = message.content.split()[1]
    await message.channel.send(get_coords(loc))



client.run(my_secret)
