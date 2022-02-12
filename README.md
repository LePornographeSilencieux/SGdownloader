# SGdownloader
SuicideGirls' mass downloader in Python 3

Just give a cookie file in parameter, and the set you wish to download

Requirements (NO-JS):
- python3
- urllib
- cookiejar
- json
- validators
- argsparser
- lxml


Usage:
python3 src/SG_gallery_downloader.py [-l|--login username -p|--password pass]
                                     [-c|--cookie cookie] -u|--url SG-Gallery-URL [...]

Examples:

python3 src/SG_gallery_downloader.py -c cookie.txt -u https://www.suicidegirls.com/girls/plum/album/975937/whip-it/

python3 src/SG_gallery_downloader.py -l MyName -p MyPass -c cookie.txt -u https://www.suicidegirls.com/girls/plum/album/975937/whip-it/



Scripts are useful for easier mass download:

# 1-Girls_Album_mass_downloader.sh - put one album URL per line in album01.txt
./1-Girls_Album_mass_downloader.sh cookie.txt albums01.txt

# 2-SearchSmallFolders.sh - searches for "small" sets (those with less than 30 pics)
./2-SearchSmallFolders.sh .
