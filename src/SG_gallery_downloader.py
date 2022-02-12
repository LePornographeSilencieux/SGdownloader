#! /usr/bin/python3

# OS functions
import os
import sys

import string

# Parse arguments
import argparse

# My own SG library
from LibSG import *

# Useful filename library
#from to_filename import *

# Make the processing for one gallery (extract girl's name, large image, lower images, ...)
def ProcessGallery(NbURL, GalleryURL, cj, username, password):
    if (not validators.url(GalleryURL)):
        print("Invalid URL [arg n°" + str(NbURL) + "]: " + GalleryURL)
        return (-1)

    useful_cookies = ""
    for cookie in cj:
        useful_cookies = useful_cookies + "; " + cookie.name + "=" + cookie.value
        #if (cookie.name == "sessid"):
        #    cookie_sessid = cookie.value
        #if (cookie.name == "sgcsrftoken"):
        #    cookie_sgcsrftoken = cookie.value
        #print(cookie.name + " " + cookie.value + " " + cookie.domain)

    cookieproc = urllib.request.HTTPCookieProcessor(cj)

    # Prepare URL builder
    URLopener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

    response = GetGalleryWebPage(NbURL, GalleryURL, URLopener)

    ## DEBUG write response in a file
    #f = open("demofile2.txt", "a")
    ##f.write("Now the file has more content!")
    #f.write(response)
    #f.close()

    ## DEBUG read response from file
    #f = open("demofile2.txt", "r")
    #response = f.read()
    #f.close()

    GalleryGirlName = GetGalleryGirlNameByURL(GalleryURL)
    GalleryTitle = GetGalleryTitleByURL(GalleryURL)
    GalleryAlbumID = GetGalleryAlbumIDByURL(GalleryURL)

    OriginalImageTitle = GalleryGirlName + " - " + GalleryTitle + " [large]"
    OriginalImagePath = "./" + OriginalImageTitle + "/"

    FilteredImageTitle = GalleryGirlName + " - " + GalleryTitle
    FilteredImagePath = "./" + FilteredImageTitle + "/"

    if (not os.path.exists(OriginalImagePath)):
        # Create a new directory because it does not exist
        os.makedirs(OriginalImagePath)

    if (not os.path.exists(FilteredImagePath)):
        # Create a new directory because it does not exist
        os.makedirs(FilteredImagePath)

    # Check if logged or not, and try to connect if required
    if (not (IsLoggedOn(response))):
        print("!!!!!!!!!!!!!!!!!!!!!!!")
        print("!! Login is required !!")
        print("!!!!!!!!!!!!!!!!!!!!!!!")
        hidden_hash_tags = GetLoginHiddenHash(response)
        hidden_hash_name = hidden_hash_tags[0]
        hidden_hash_value = hidden_hash_tags[1]

        username_name = GetLoginUsernameName(response)
        password_name = GetLoginPasswordName(response)
        form_login_action = GetLoginAPIurl(response)

        # form_login_method    ### method="post"
        # form_login_action    ### action="https://api.suicidegirls.com/v3/auth/login/"
        # hidden_hash_name   ### name=token name
        # hidden_hash_value   ### value=tok en value
        # username_name   ### name="username"
        # password_name   ### name="password"


        headers = { hidden_hash_name : hidden_hash_value ,
                    username_name : username ,
                    password_name : password }
        login_request = urllib.request.Request(form_login_action,
                                               headers=headers,
                                               method='POST')
        login_response = urllib.request.urlopen(login_request)

        useful_cookies = ""
        for cookie in cj:
            useful_cookies = useful_cookies + "; " + cookie.name + "=" + cookie.value
            #print(cookie.name + " " + cookie.value + " " + cookie.domain)
    else:
        print("Logged on")

    # cookie "sessid" = cookie_sessid
    # cookie "sgcsrftoken" = cookie_sgcsrftoken
    #gallery_cookies = { "Cookie" : "sessid=" + cookie_sessid + "; " + \
    #                   "sgcsrftoken" + cookie_sgcsrftoken }
    #gallery_cookies = "sessid=" + cookie_sessid + "; sgcsrftoken" + cookie_sgcsrftoken
    gallery_cookies = useful_cookies

    gallery_API_url = "https://www.suicidegirls.com/api/get_album_info/" + \
        GalleryAlbumID + "/"
    gallery_API_body = { }

    json_send_data = json.dumps(gallery_API_body)
    json_send_data_as_bytes = json_send_data.encode('utf-8')

    gallery_headers = { 'Content-Type' : 'application/json; charset=utf-8',
                        'Content-Length' : len(json_send_data_as_bytes),
                        'Cookie' : gallery_cookies }

    gallery_req = urllib.request.Request(url=gallery_API_url,
                                         method='GET',
                                         data=json_send_data_as_bytes,
                                         headers=gallery_headers)
    gallery_response = urllib.request.urlopen(gallery_req)

    JSON_data = json.loads(gallery_response.read().decode(gallery_response.info().get_param('charset') or 'utf-8'))

    #print(JSON_data)
    #for key in JSON_data:
        #print(str(key) + " : " + str(JSON_data[key]))

    nb_pics = len(JSON_data['photos'])
    nb_digit = len(str(nb_pics))
    digit_format = "{:0" + str(nb_digit) + "d}"
    img_counter = 0
    for pic in JSON_data['photos']:
        pic_urls = pic['urls']
        img_nb = digit_format.format(img_counter + 1)
        original_pic_url = pic_urls['original']
        img_url_tmp = urllib.parse.urlparse(original_pic_url).path
        img_ext = os.path.splitext(img_url_tmp)[1]
        img_filename = img_nb + img_ext
        img_filepath = OriginalImagePath + img_filename
        print(str(img_counter) + " : " + img_url_tmp)
        urllib.request.urlretrieve(original_pic_url, img_filepath)
        filtered_format = ChooseBestFilteredPicture(pic_urls)
        filtered_pic_url = pic_urls[str(filtered_format)]
        img_url_tmp = urllib.parse.urlparse(filtered_pic_url).path
        img_ext = os.path.splitext(img_url_tmp)[1]
        img_filename = img_nb + img_ext
        img_filepath = FilteredImagePath + img_filename
        print("[" + str(filtered_format) + "] : " + img_url_tmp)
        urllib.request.urlretrieve(filtered_pic_url, img_filepath)
        img_counter += 1

    # Rename folders with the correct name
    GalleryGirlsRealNames = GetGalleryGirlNameByJSON(JSON_data)
    #GalleryGirlsRealNames = clean_filename(GalleryGirlsRealNames)
    GalleryGirlsRealNames = GalleryGirlsRealNames.strip(" /.#")
    if (GalleryGirlsRealNames == ""):
        GalleryGirlsRealNames = GalleryGirlName
    # Capitalize 1st letter at least
    GalleryGirlsRealNames = GalleryGirlsRealNames[:1].upper() + GalleryGirlsRealNames[1:]
    # Remove the exceeding spaces
    GalleryGirlsRealNames = ' '.join(GalleryGirlsRealNames.split())

    GalleryRealTitle = JSON_data['name']
    #GalleryRealTitle = clean_filename(GalleryRealTitle)
    GalleryRealTitle = GalleryRealTitle.strip(" /.#")
    if (GalleryRealTitle == ""):
        GalleryRealTitle = GalleryTitle
    # Capitalize 1st letter at least
    GalleryRealTitle = GalleryRealTitle[:1].upper() + GalleryRealTitle[1:]
    # Remove the exceeding spaces
    GalleryRealTitle = ' '.join(GalleryRealTitle.split())

    OriginalImageRealTitle = GalleryGirlsRealNames + " - " + GalleryRealTitle + " [large]"
    OriginalImageRealPath = "./" + OriginalImageRealTitle + "/"

    FilteredImageRealTitle = GalleryGirlsRealNames + " - " + GalleryRealTitle
    FilteredImageRealPath = "./" + FilteredImageRealTitle + "/"

    os.rename(OriginalImagePath, OriginalImageRealPath)
    os.rename(FilteredImagePath, FilteredImageRealPath)

    return (0)

# Read each URL and launch the processing for each of them
def Processing(NbUrls, urls, username="", password="", cookie=""):
    if (len(cookie) > 0):
        CookieFile = cookie
        if (not os.path.isfile(CookieFile)):
            print("Error: Cookie file '" + CookieFile + "' does not exist")
            exit (-1)
        cj = LoadCookiesFromFile(CookieFile)
    else:
        cj = cj = http.cookiejar.MozillaCookieJar()

    UrlCounter = 0
    for url in urls:
        UrlCounter += 1

        # Real processing
        print(url)
        ProcessGallery(UrlCounter, url, cj, username, password)


def printHelp():
    print("Format of parameters : ")
    print(sys.argv[0] + " [-u|--username username -p|--password password] " + \
          "[-c|--cookie CookieFile.txt] -u|--url Gallery-URL ...")
    print("")
    print("Choose between 'Username + Password' or 'Cookie' method")

def main():
    NbArgs = len(sys.argv);
    ArgParser = argparse.ArgumentParser()

    # Let's recognize : username
    ArgParser.add_argument("-l", "--login", required=False,
                           dest="username", type=str, nargs="?", default="",
                           help="Login/Username for SG login")

    # Let's recognize : password
    ArgParser.add_argument("-p", "--password", required=False,
                           dest="password", type=str, nargs="?", default="",
                           help="Password for SG login")

    # Let's recognize : cookie
    ArgParser.add_argument("-c", "--cookie", required=False,
                           dest="cookie", type=str, nargs="?", default="",
                           help="Cookie file instead of login")

    # Let's recognize : URL
    ArgParser.add_argument("-u", "--url", required=True,
                           dest="urls", type=str, nargs="+",
                           help="URL of the gallery to download (might put multiple)")

    args = ArgParser.parse_args()

    if not (((len(args.username) > 0) and (len(args.password) > 0)) or
        (len(args.cookie) > 0)):
        print("ERROR: No cookie file given, nor username + password (or one is missing)")
        print("")
        printHelp()
        exit (-1)

    NbUrls = len(args.urls)
    if (NbUrls < 1):
        print("ERROR: No url given")
        print("")
        printHelp()
        exit (-2)

    # If only cookie given
    if ((len(args.cookie) > 0) and
        (len(args.username) < 1) and (len(args.password) < 1)):
        #Processing_Cookie(args.cookie, args.urls)
        Processing(NbUrls, args.urls, cookie=args.cookie)
        exit (0)

    # If only username and password given
    if (((len(args.username) > 0) and (len(args.password) > 0)) and
        (len(args.cookie) < 1)):
        #Processing_UsernamePassword(args.username, args.password, args.urls)
        Processing(NbUrls, args.urls, username=args.username, password=args.password)
        exit (0)

    # If username, password, and cookie given
    if ((len(args.username) > 0) and (len(args.password) > 0) and (len(args.cookie) > 0)):
        #Processing_UsernamePasswordCookie(args.username, args.password, args.cookie, args.urls)
        Processing(NbUrls, args.urls, args.username, args.password, args.cookie)
        exit (0)

    # Unknown case
    print("ERROR: Unknown case.")
    print("")
    printHelp()
    exit(-1)

main()
