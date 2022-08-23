#!/usr/bin/env python
from pick import pick
import datetime
import os

series = set([])

def getInfo(file_dir):
    f = open(file_dir)
    f.readline()
    while(True):
        line = f.readline()
        if "series" in line:
            s = line.split("\"")[1]
            series.add(s)
        if(line == "---\n"): break
    f.close()

## get Series already Exist
def findSeries():
    find_dir = os.path.join(os.getcwd(), "contents","posts")
    for dir in os.listdir(find_dir):
        file_name = os.path.join(find_dir,dir,"index.md")
        try:
            getInfo(file_name)
        except:
            print("no file")

## main part
if __name__ == "__main__":
    findSeries()
    # get title
    print("INPUT POST TITLE : ", end="")
    title = input()

    # get description
    print("DESCRIPT POST : ", end="")
    desc = input()

    # get series
    out_message = "Select Series"
    if series:
        series.add("none")
        option, idx = pick(list(series), out_message, indicator="=>", default_index=0)

    # add Date data
    date = str(datetime.datetime.today()).split()[0]
    update = date

    # get dir
    cwd = os.getcwd()
    dir_path = os.path.join(cwd,"contents","posts",title)
    file_dir = os.path.join(dir_path,"index.md")


    # write md file
    os.mkdir(dir_path)
    f = open(file_dir,"w")
    f.write("---\n")
    f.write(f"title : {title}\n")
    f.write(f"description : {desc}\n")
    f.write(f"date : {date}\n")
    f.write(f"update : {update}\n")
    f.write(f"tags : \n\t- \n")
    if(option != "none"):
        f.write(f"series : {option}\n")
    f.write("---\n")
