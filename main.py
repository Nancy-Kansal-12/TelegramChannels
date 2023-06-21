import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from html_content import html_content_list

# Scraping data from website : https://telegramchannels.me/category/cryptocurrencies

def convert_to_int(string) :
    """This function takes string as an input(e.g. "13.2K") and returns integer value(e.g. 13200)"""
    
    # if condition for handling bots
    if ("bot" in string) :
        return 0 
    
    multiplier_dict = {"K":1000, "M":1000000}
    multiplier = ""
    
    if "K" in string :
        string = string.replace("K", "")
        multiplier = "K"       
    elif "M" in string :
        string = string.replace("M", "")
        multiplier = "M"
        
    number = float(string)
    
    if (multiplier!="") :
        number *= multiplier_dict[multiplier]
        
    return int(number)

def get_channels_list() :
    """ This function returns list of all telegram channels"""
    
    all_channels = []
    
    # stores channel names and corresponding index in channels list
    all_channels_name = dict()

    for html in html_content_list :
        data = BeautifulSoup(html, 'html.parser')
        divs = data.find_all('div', attrs = {"class":"column is-full"})
        
        base_url = "tg://resolve?domain="
        class_name_a = "is-clickable is-block has-text-grey-darker"
        
        for div in divs :
            for each in div.find_all('a', attrs = {"class":class_name_a }) :
                if "More about" in each['title'] :
                    channel_name = each['title'].split("More about ")[1]
                    channel_link = base_url + each['href'][37:]              
                    participants = list(each.find("div", attrs = {"class" : "subtitle is-size-7 has-text-grey"}).strings)
                    
                    # # if condition for discarding bots
                    if (len(participants) > 2 or "bot" in participants[1]) :    
                        continue 
                                                                 
                    number_of_participants = convert_to_int(participants[1].strip())
                    
                    # To avoid repetition of channels
                    if (channel_name in all_channels_name) :    
                        index = all_channels_name[channel_name]
                        channel_list = all_channels[index]
                        channel_list[2] = max(number_of_participants, channel_list[2] )
                    else :
                        all_channels.append([channel_name, channel_link, number_of_participants])  
                        all_channels_name[channel_name] = len(all_channels) - 1
      
                    
    return all_channels

def sort_by_participants(value) :
    return value[2]

def get_csv_file(filename) : 
    """ This function creates a csv file of channels in the same folder where script is running with the given filename """
    
    all_channels = get_channels_list()
    all_channels.sort(key = sort_by_participants, reverse = True)
    
    df = pd.DataFrame(all_channels, columns = ['Name', 'Link', 'Participants'])
    df.to_csv(filename + ".csv", index = False)


# filename is the name with which csv file would be saved
filename = input("Enter the name with which you want to save the file: ")
get_csv_file(filename)