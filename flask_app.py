
# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request
from googlesearch import search
from bs4 import BeautifulSoup
import urllib # We'll still need this to download webpages
import requests
import re

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World'


def mc_get_details(names_c):

    players_data={}

    for i in names_c:
        response = requests.get('https://www.google.com/search?q={0}+espncricinfo&oq={0}+espncricinfo&aqs=chrome.0.69i59j69i60.5143j0j1&sourceid=chrome&ie=UTF-8'.format(i))
        data = BeautifulSoup(response.text,'html.parser')
        for i in data.find_all('a'):
            if i['href'].find('q=https://www.espncricinfo.com/player/')!=-1:
                url = i['href'][i['href'].find('=')+1:i['href'].find('&')]
                break

        # query = i +' cricketer details espncricinfo'
        # for j in search(query):
        #     if 'espncricinfo.com' in j:
        #         url = j
        #         break





        # This just downloads the html text with full markdown
        webpage_content = urllib.request.urlopen(url).read()

        # We want a markdown-interpreted (structured) version of the html using BeautifulSoup:
        data = BeautifulSoup(webpage_content, 'html.parser')

        # # # Bio data about virat

        name_c = data.find_all("p",string="Full Name")[0]

        r_name= list(name_c.next_sibling.children)


        players_data[r_name[0].text]={}

        # print(players_data)

        # print(name_c,end='\n\n\n')

        bio_data_c = name_c.parent

        players_data[r_name[0].text]['bio_data'] = {}
        players_data[r_name[0].text]['bio_data']['Full Name'] = r_name[0].text
        for i in bio_data_c.next_siblings:
            players_data[r_name[0].text]['bio_data'][i.find('p').text]=i.find('span').text

        # print(players_data)
        # # # Bio data about virat

        # # # Teams of virat

        teams = data.find_all("p",string="TEAMS")


        players_data[r_name[0].text]['teams'] = []
        for i in teams[0].next_sibling.children:
        #     print(list(i.children)[1],end='\n\n\n')
            players_data[r_name[0].text]['teams'].append(list(list(i.children)[1].children)[0].text)

        # # # Teams of virat


        # print(players_data)

        # # # Description about virat

        desc_c = data.find('div',{'class':"ci-player-bio-content"})

        players_data[r_name[0].text]['Description'] = ''

        if desc_c:
            for i in desc_c.children:
            #     print(i,end='\n\n\n')
                players_data[r_name[0].text]['Description']+=i.text

        # # # Description about virat
        # print(players_data)


        # # # Career Averages

        carrer_avg = data.find("span",string="Career Averages")
        # print(carrer_avg)
        carrer_avg = carrer_avg.parent.parent.next_sibling
        print('\n\n\n\n\n')
        # print(carrer_avg)
        carrer_avg = carrer_avg.find_all("table")
        # print(carrer_avg)


        # Batting Career

        batting_cn = []
        players_data[r_name[0].text]['Batting_Career'] = {}

        for i in carrer_avg[0].find_all('th'):
            batting_cn.append(i.text)

        for i in carrer_avg[0].find_all('tr'):
            for j,k in enumerate(i.find_all('td')):
                if j==0:
                    format_m=k.find('span').text
                    players_data[r_name[0].text]['Batting_Career'][format_m] = {}
                else:
                    players_data[r_name[0].text]['Batting_Career'][format_m][batting_cn[j]]=k.find('span').text

        # print(batting_cn)

        # print(players_data)


        # Batting Career


        # Bowling Career

        bowling_cn = []
        players_data[r_name[0].text]['Bowling_Career'] = {}

        for i in carrer_avg[1].find_all('th'):
            bowling_cn.append(i.text)


        for i in carrer_avg[1].find_all('tr'):
            for j,k in enumerate(i.find_all('td')):
                if j==0:
                    format_m=k.find('span').text
                    players_data[r_name[0].text]['Bowling_Career'][format_m] = {}
                else:
                    players_data[r_name[0].text]['Bowling_Career'][format_m][bowling_cn[j]]=k.find('span').text

        # print(bowling_cn)

        # print(players_data)

    return players_data


    # Bowling Career



    #     print(i.find('thead'))
    #     print(i.find('tbody'))

    # # # Career Averages

def extract_players_sc(urls,team_name):
    team_name = team_name
    players=[]
    for i in urls:
        response = requests.get(i)
        data = BeautifulSoup(response.text,'html.parser')
        tables = data.find_all('table', {'class':'ci-scorecard-table'})
        for j in tables:
            for k in j.parent.previous_sibling.find_all('span'):
                if k.text.lower().find(team_name.lower())!=-1:
                    for z in j.find_all('tr'):
                        if z.find('a'):
                            if z.find('a').has_attr('title'):
                                temp= z.find('a')['title']
                                if temp not in players:
                                    players.append(temp)
                    dn_bat_data = j.find('strong',string='Did not bat: ')
                    if dn_bat_data:
                        for y in dn_bat_data.next_siblings:

                            if y.find('span').text.find('\xa0')!=-1:
                                temp = y.find('span').text[:y.find('span').text.index('\xa0')].strip()
                                if temp.find(',')!=-1:
                                    temp=temp[:temp.find(',')].strip()
                                    if temp not in players:
                                        players.append(temp)
                                elif temp not in players:
                                    players.append(temp)
                                    temp=''
                            else:
                                temp = y.find('span').text.strip()
                                if temp not in players:
                                    players.append(temp)
                                    temp=''
    return players




@app.route('/cricketer_details',methods=['GET'])        #Cricketer Basic Profile with description
def get_details():

    # players_data={'player name':{different data}}
    text=''
    try:
        text = request.args.get('text')
    except:
        pass

    if not text:
            if request.args.get('name').find(',')!=-1:
                names_c = request.args.get('name').split(',')
            else:
                names_c=[request.args.get('name')]

            data = mc_get_details(names_c)

    else:

        query = text +' full score card espncricinfo'
        for j in search(query):
            if 'espncricinfo.com' in j:
                url = j
                break

        urls=[url]
        team_name=text[:text.find('vs')].strip()
        names_c = extract_players_sc(urls,team_name)

        data= mc_get_details(names_c)

    return data



@app.route('/cricketer_details_bt',methods=['GET'])        #Details by Tour
def get_details_by_tour():

    text = request.args.get('text')
    team_name = request.args.get('team_name')
    format_m= request.args.get('format')

    query = text + format_m +' format '+' squad espncricinfo'
    for j in search(query):
        if 'espncricinfo.com' in j:
            url = j
            break


    url = url+'/match-schedule-fixtures-and-results'

    response = requests.get(url)
    data = BeautifulSoup(response.text , 'html.parser')

    filt_data = data.find_all('span',string='RESULT')

    urls=[]
    for i in filt_data:
        temp = i.next_sibling
        if temp.name == 'div' and temp.text.lower().find(format_m.lower())!=-1:
            for i in temp.parents:
                if i.name=='a' and i['href'].find('full-scorecard')!=-1:
                        urls.append('https://www.espncricinfo.com/'+i['href'])

    # print(urls)

    names_c = extract_players_sc(urls,team_name)

    return mc_get_details(names_c)


@app.route('/cricketer_fcareer',methods=['GET'])      #Cricketer Detailed career stats
def get_career():

    players_data = {}

    name_c = request.args.get('name')

    required = request.args.get('required')


    players_data[name_c]={}

    query = name_c +' cricketer bowling batting stats espncricinfo '
    for j in search(query):
        if 'espncricinfo.com' in j:
            url = j
            break

    # This just downloads the html text with full markdown
    webpage_content = urllib.request.urlopen(url).read()

    # We want a markdown-interpreted (structured) version of the html using BeautifulSoup:
    data = BeautifulSoup(webpage_content, 'html.parser')

    if required=='all':
        required=[]
        for i in data.find_all("h5",{'class':'ds-text-title-subtle-s'}):
            required.append(i.text)
    else:
        required=required.split(',')

    # Stats
    def scraping_table(table_name,table):
        temp = []
    #     bowling_cn = []
        players_data[name_c][table_name] = {}

        for i in table.find_all('th'):
            temp.append(i.text)


        for i in table.find_all('tr'):
            for j,k in enumerate(i.find_all('td')):
                if j==0:
                    format_m=k.find('span').text
                    players_data[name_c][table_name][format_m] = {}
                else:
                    players_data[name_c][table_name][format_m][temp[j]]=k.find('span').text

    required=['vs Team','By Season','Toss and Batting Sequence']

    for i in required:
    #     print(data.find("h5",string=i))
        table = data.find("h5",string=i).parent.find("table")
        scraping_table(i,table)
    #     print(players_data)

    return players_data



# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
