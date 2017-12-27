# -*- coding : utf8 -*-
# Author: waheida
# Description: check dnslog from ceye.io.
# Uage: Just replace your API token and run it.
# Bug: There is still a adaptive bug in my code. If the output data is too long, the printed form will be messy. >_<
import urllib2
import json


def check_input(string,max_num):
    '''
    Check input number is correct or not.
    '''
    while True:
        if string.isdigit() and string <= str(max_num):
            return int(string)
        else:
            string = raw_input("\nPlease input correct number:\n\n$>")

def align(data):
    '''
    Pretty the print form.
    '''
    for i in data:
        if i["name"]:
            if len(i["name"]) < 30:
                   for x in range(30-len(i["name"])):
                        i["name"] += " "
        if i["remote_addr"]:
            if len(i["remote_addr"]) < 15:
                for x in range(15-len(i["remote_addr"])):
                    i["remote_addr"] += " "
        if i.has_key("method"):
            if len(i["method"]) < 6:
                for x in range(6-len(i["method"])):
                    i["method"] += " "
        if i.has_key("data"):
            if len(i["data"]) < 30:
                for x in range(30-len(i["data"])):
                    i["data"] += " "
    return data

def mode_print(method,mode,data):
    '''
    Different mode different print.
    '''
    data = align(data)
    if method == "dns":
        print "\n######################################################################################\n"
        print " DNS Results:\n"
        print " ---------------------------------------------------------------------------------"
        print "|   id   |              name              |  remote_addr    |      created_at     |"
        print " ---------------------------------------------------------------------------------"
        for i in data:
            print "|",i['id'],"|",i['name'],"|",i['remote_addr'],"|",i["created_at"],"|"
            print " ---------------------------------------------------------------------------------"
    else:
        print "\n######################################################################################\n"
        print "REQUEST Result:\n"
        if mode == 1:
            print " ---------------------------------------------------------------------------------------------------------------------"
            print "|   id   |               name             |  remote_addr    | method |             data               |    user agent   |    content type    |      created_at     |"
            print " ---------------------------------------------------------------------------------------------------------------------"
            for i in data:
                print "|",i['id'],"|",i['name'],"|",i['remote_addr'],"|",i["method"],"|",i["data"],"|",i["user_agent"],"|",i["content_type"],"|",i["created_at"],"|"
                print " ----------------------------------------------------------------------------------------------------------------------"
        elif mode == 2:
            print " ---------------------------------------------------------------------------------"
            print "|   id   |              name              |  remote_addr    |      created_at     |"
            print " ---------------------------------------------------------------------------------"
            for i in data:
                print "|",i['id'],"|",i['name'],"|",i['remote_addr'],"|",i["created_at"],"|"
                print " ---------------------------------------------------------------------------------"
        elif mode == 3:
            print " ---------------------------------------------------------------------------------------------------------------------------"
            print "|   id   |              name              |  remote_addr    | method |             data               |      created_at     |"
            print " ------------------------------------------------------------------------------------------------------------------------ --"
            for i in data:
                print "|",i['id'],"|",i['name'],"|",i['remote_addr'],"|",i["method"],"|",i["data"],"|",i["created_at"],"|"
                print " ---------------------------------------------------------------------------------------------------------------------------"

def Search(Token,Method,FilterString):
    '''
    Choose different mode to get data.
    '''
    try:
        url = "http://api.ceye.io/v1/records?token=" + Token + "&type=" + Method + "&filter=" + FilterString
        req = urllib2.urlopen(url)
        res = json.loads(req.read())
        data = res['data']
        while True:
            if Method == "dns":
                Mode = 1
            else:
                Mode = raw_input("\nPlease choose Mode:\n 1 ----> Get All Datas\n 2 ----> Get [ id , url , ip , time ]\n 3 ----> Get [ id , url , ip , method , data , time ]\n\n$>")
                Mode = check_input(Mode,3)
            mode_print(Method, Mode , data)
            next_step = raw_input("Please choose next step:\n 1 ----> Return Previous Step to choose Mode\n 2 ----> Return Previous Level to choose Method\n 3 ----> Exit\n\n$>")
            next_step = check_input(next_step,3)

            if next_step == 2:
                return
            elif next_step == 3:
                exit(0)
    except Exception as e:
        print e
        
def main(Token):
    '''
    Choose different method and do search.
    '''
    while True:
        flag = True
        num = raw_input("\nPlease input Method number:\n 1 ----> dns\n 2 ----> request\n 3 ----> Exit\n\n$>")
        num = check_input(num,3)
        if num == 1:
            Method = "dns"
        elif num == 2:
            Method = "request"
        elif num == 3:
            return
        else:
            print "\nUnknown Method Number! Please input Method num again!\n"
            flag = False
        if flag:
            FilterString = raw_input("\nPlease input Filter String(Default is null):[Only String in URL]\n\n$>")
            Search(Token, Method, FilterString)

if __name__ == "__main__":
    Token = "your API token"
    main(Token)
