#! /usr/bin/python3

import string

# URL validator
import validators

# HTTP requests
import urllib.request

# URL parser
import urllib.parse

# Cookies
import http.cookiejar

# XPath analyzer
from lxml import etree

# JSON analyzer
import json


def strdup(string):
    tmp_str = " " + string
    out_str = tmp_str[1:]
    return (out_str)

# Load cookies from a file
def LoadCookiesFromFile(CookieFilePath):
    # Prepare CookieJar for file reading (FileCookieJar -> MozillaCookieJar)
    cj = http.cookiejar.MozillaCookieJar(CookieFilePath)
    cj.load()
    return (cj)

# Extract the URL attributes
def url_parser(url):
    parts = urllib.parse.urlparse(url)
    directories = parts.path.strip('/').split('/')
    queries = parts.query.strip('&').split('&')

    elements = {
        'scheme': parts.scheme,
        'netloc': parts.netloc,
        'path': parts.path,
        'params': parts.params,
        'query': parts.query,
        'fragment': parts.fragment,
        'directories': directories,
        'queries': queries,
    }
    return (elements)

# Search if the request has been made with a profile recognized or not (is logged or not)
def IsLoggedOn(urllib_response):
    ### Just check the presence of the "Login" button
    # requests_html XPath
    login_button_xpath = "body > div.full-bleed.top-head > div.layout-inner > " + \
        "aside.user-info.embossed > div#login > a.button_login"

    # Another XPath format
    login_button_xpath = "/html/body/div.full-bleed.top-head/div.layout-inner/" + \
        "aside.user-info.embossed/div#login/a.button_login"

    # lxml XPath
    login_button_xpath = "/html/body/div[@class='full-bleed top-head']/" + \
        "div[@class='layout-inner']/aside[@class='user-info embossed']/" + \
        "div[@id='login']/a[@class='button login']"

    tree = etree.HTML(urllib_response)
    login_button_tags = tree.xpath(login_button_xpath)
    if (len(login_button_tags) == 0):
        return (True)
    else:
        return (False)

# Get the XPath of the login form
def GetLoginFormXPath():
    # requests_html XPath
    login_form_xpath = "body > div.full-bleed.top-head > div.layout-inner > " + \
        "aside.user-info.embossed > div#login > div#login-wrapper > " + \
        "div.login-form-wrapper > div#login-options > div#direct-login > " + \
        "form#login-form "

    # lxml XPath
    login_form_xpath = "/html/body/div[@class='full-bleed top-head']/" + \
        "div[@class='layout-inner']/aside[@class='user-info embossed']/" + \
        "div[@id='login']/div[@id='login-wrapper']/div[@class='login-form-wrapper']/" + \
        "div[@id='login-options']/div[@id='direct-login']/form[@id='login-form']"

    return (login_form_xpath)

# Get the name of the field and the value of the hidden hash for logging
def GetLoginHiddenHash(urllib_response):
    login_form_xpath = GetLoginFormXPath()

    # requests_html XPath
    hidden_hash_xpath = login_form_xpath + " > input[type=hidden]"

    # lxml XPath
    hidden_hash_xpath = login_form_xpath + "/input[@type='hidden']"

    tree = etree.HTML(urllib_response)
    hidden_hash_tags = tree.xpath(hidden_hash_xpath)
    if (len(hidden_hash_tags) < 1):
        print("!!! Can't find the form for hidden name and value")
        return ("")

    #test_xpath = "/html/body/div[@class='full-bleed top-head']/" + \
    #    "div[@class='layout-inner']/aside[@class='user-info embossed']"
    #test_tags =  tree.xpath(test_xpath)
    #for node in test_tags:
        #print(node.attrib)
        #for name in node.attrib:
            #print(name, "->", node.attrib[name])

    hidden_hash_tag = hidden_hash_tags[0]
    for attr in hidden_hash_tag.attrib:
        if (attr == 'name'):
            hidden_hash_name = hidden_hash_tag.attrib[attr]
        if (attr == 'value'):
            hidden_hash_value = hidden_hash_tag.attrib[attr]

    return ([hidden_hash_name, hidden_hash_value])

# Get the name of the field for the username
def GetLoginUsernameName(urllib_response):
    login_form_xpath = GetLoginFormXPath()

    # requests_html XPath
    username_name_xpath = login_form_xpath + " > input#username"

    # lxml XPath
    username_name_xpath = login_form_xpath + "/input[@id='username']"

    tree = etree.HTML(urllib_response)
    username_name_tags = tree.xpath(username_name_xpath)
    if (len(username_name_tags) < 1):
        print("!!! Can't find the form for username tag name")
        return ("")

    username_name_tag = username_name_tags[0]
    for attr in username_name_tag.attrib:
        if (attr == 'name'):
            username_name = username_name_tag.attrib[attr]

    return (username_name)

# Get the name of the field for the password
def GetLoginPasswordName(urllib_response):
    login_form_xpath = GetLoginFormXPath()

    # requests_html XPath
    password_name_xpath = login_form_xpath + " > input[type=password]"

    # lxml XPath
    password_name_xpath = login_form_xpath + "/input[@type='password']"

    tree = etree.HTML(urllib_response)
    password_name_tags = tree.xpath(password_name_xpath)
    if (len(password_name_tags) < 1):
        print("!!! Can't find the form for password tag name")
        return ("")

    password_name_tag = password_name_tags[0]
    for attr in password_name_tag.attrib:
        if (attr == 'name'):
            password_name = password_name_tag.attrib[attr]

    return (password_name)

# Get the URL of the authentification API
def GetLoginAPIurl(urllib_response):
    login_form_xpath = GetLoginFormXPath()

    tree = etree.HTML(urllib_response)
    form_login_tags = tree.xpath(login_form_xpath)
    if (len(form_login_tags) < 1):
        print("!!! Can't find the form for API url")
        return ("")

    form_login_tag = form_login_tags[0]
    for attr in form_login_tag.attrib:
        if (attr == 'method'):
            form_login_method = form_login_tag.attrib[attr]
        if (attr == 'action'):
            form_login_action = form_login_tag.attrib[attr]

    return (form_login_action)

# Get the ID of the album's gallery
def GetGalleryAlbumIDByURL(GalleryURL):
    #parts = urlparse(GalleryURL)
    URLelements = url_parser(GalleryURL)
    URLdirectories = URLelements['directories']
    #print(URLdirectories[3])
    AlbumID = URLdirectories[3]
    return (AlbumID)

# Get the girl's name from the URL
def GetGalleryGirlNameByURL(GalleryURL):
    #parts = urlparse(GalleryURL)
    URLelements = url_parser(GalleryURL)
    URLdirectories = URLelements['directories']
    #print(URLdirectories[1])
    InitGirlName = URLdirectories[1]
    GirlName = string.capwords(InitGirlName)
    return (GirlName)

# Get the gallery's title from the URL
def GetGalleryTitleByURL(GalleryURL):
    URLelements = url_parser(GalleryURL)
    URLdirectories = URLelements['directories']
    #print(URLdirectories[4])
    #print(URLdirectories)
    #print(len(URLdirectories))
    if (len(URLdirectories) <= 4):
        Title = "NO-TITLE"
    else:
        InitTitle = URLdirectories[4]
        SpaceTitle = InitTitle.replace("-", " ")
        Title = string.capwords(SpaceTitle)
    return (Title)

# Get all the girls present in the set from the JSON
def GetGalleryGirlNameByJSON(JSON_data):
    Girls = []
    for girl in JSON_data['tip_recipients']:
        Girls.append(str(girl))

    GalleryGirlsRealNames = ""
    counter = 0
    for girl in Girls:
        if (counter == 0):
            GalleryGirlsRealNames = string.capwords(girl)
        else :
            GalleryGirlsRealNames = GalleryGirlsRealNames + " & " + string.capwords(girl)
        counter += 1
    return (GalleryGirlsRealNames)

# Get the web page of the gallery (give a number for the debugging trace)
def GetGalleryWebPage(NbURL, GalleryURL, URLopener):
    response = None
    # Ask for an URL
    #response = URLopener.open(GalleryURL)
    try:
        # we can't use helpers.retrieve_url because of redirects
        # we need the cookie processor to handle redirects
        response = URLopener.open(GalleryURL).read().decode('utf-8')
    except urllib_request.HTTPError as e:
        # if the page returns a magnet redirect, used in download_torrent
        if e.code == 302:
            response = e.url
    except Exception:
        pass

    if (response == None):
        print("Failure in URL [arg n°" + str(NbURL) + "]: " + GalleryURL)
        return (None)

    return(response)

# Choose the biggest picture "before" original pictures (best quality for filtered ones)
def ChooseBestFilteredPicture(ArrayOfFormats):
    tab = []
    for name in ArrayOfFormats:
        if ((name.find('original') == -1) and (name.find('x') == -1)):
            tab.append(int(name))
    return (max(tab))
