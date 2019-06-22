import re
import urllib3
import shutil
import json
from selenium import webdriver
import time

"""
get back a link from given site
the link is identified by a regex
"""
def get_html_request(site, regex):
    #we need to change the user-agent, since if the site identifies python, it will be blocked
    http = urllib3.PoolManager(headers={'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0)'})
    response = http.request('GET', site, preload_content=False)
    if response.status != 200:
        print('Error: {}\n was unable to reach {}'.format(response.status, site))
        exit(1)
    
    cookies = response.headers['Set-Cookie']
    url = regex.findall(response.data)
    if len(url) == 0:
        print('was unable to find the necesary link. Exiting')
        exit(2)
    return url[0].decode(), cookies

'''
download csv file using site's api
site - the url of the site
post_data - the data to pass in the post request
'''
def get_csv_file_from_api(site, post_data):
    http = urllib3.PoolManager(headers={'user-agent':'Mozilla/5.0 (Windows NT 6.3; rv:36.0)', 'Accept':'text/csv',
     'Content-Type':'application/json;charset=UTF-8',"Referer": "https://maya.tase.co.il/funds?view=etf", 
     "X-Maya-With": "allow"})
    data = json.dumps(post_data).encode('utf-8')
    response = http.request('POST', site, body=data)
    if response.status != 200:
        print ('Error: {}\n was unable to reach {}'.format(response.status, site))
        exit(1)
    print('funds file was downloaded\n')
    with open('/tmp/funds.csv', 'w') as f:
        f.write(response.data.decode('utf-8'))


def parse_securities_info_data(file_path, output_path, encoding_type = 'cp1255'):
    """
    parse the securities info csv into a json file
    file_path - file path to read from
    output_path - file path to write json file to
    encoding_type - type of encoding to use
    """

    json_data = ''
    with open(file_path, 'r', encoding = encoding_type) as f:
        header = []
        json_record = {}
        for line in f:
            record =  line.split(',')
            if len(record) > 1 and len(header) == 0 and record[2] != '':
                header = record
                continue
            index = 0
            if len(record) == len(header):
                for item in header:
                    if record[index].startswith('"'):
                        start = index
                        while not record[index].endswith('"'):
                            index += 1
                        json_record[item.strip('\n')] = ','.join(record[start:index].strip('\n'))
                        index += 1
                    else: 
                        json_record[item.strip('\n')] = record[index].strip('\n')
                        index += 1
                if len(json_record) > 1:
                    json_data = json_data + json.dumps(json_record) + ','

    with open(output_path,'w') as f:
        f.write(json_data)


def main():
    #this is the address we will start from, looking for the link to download the file
    site = 'https://info.tase.co.il/heb/marketdata/securitiesinfo/Pages/SecuritiesInfo.aspx'
    #we will use this regex to find the link to open the link to the table we wish to parse
    regex = re.compile(b'customWindowOpen\(\'(/.*?)\'.*?' + re.escape('עמודות נוספות'.encode('utf-8')))
    # this is the address of the page with additional columns
    url, cookies = get_html_request(site, regex)
    regex2 = re.compile(b'customWindowOpen\(\'(/.*?)\'.*?\s.*CSV</a>\s')
    # this is the address of the link to download the file
    url2, cookies = get_html_request('https://info.tase.co.il' + url, regex2)
    http = urllib3.PoolManager(headers={'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0)'})
    response = http.request('GET', 'https://info.tase.co.il' + url2, preload_content=False)
    if response.status != 200:
        print('Error: {}\n was unable to reach {}'.format(response.status, site))
        exit(1)
    with open('/tmp/pension.csv', 'wb') as f:
        shutil.copyfileobj(response, f)
    print('options file was downloaded\n')

    parse_securities_info_data('/tmp/pension.csv', '/tmp/pension.json')
    ####################################
    api_url = 'https://mayaapi.tase.co.il/api/download/funds'
    post_data = {"taxRouteData": {}, "props": {}, "fundType": 2, "classificationType": 2}

    get_csv_file_from_api(api_url, post_data)

    parse_securities_info_data('/tmp/funds.csv', '/tmp/funds.json', 'utf-8')
    ####################################
    options = webdriver.ChromeOptions()
    options.binary_location = '/usr/bin/chromium-browser'
    options.add_argument("--no-sandbox") 
    options.add_argument("--no-default-browser-check")
    options.add_argument("--no-first-run")
    options.add_argument("--disable-default-apps") 
    options.add_experimental_option("prefs", {
    "download.default_directory" : "/tmp/"})

    browser = webdriver.Chrome(chrome_options=options)
    site = 'https://info.tase.co.il/heb/marketdata/derivativesmarket/pages/derivatives.aspx?action=991&subaction=1&type=99'
    browser.get(site)
    browser.find_element_by_id('tblCloseBtnucGridTA25ExportButtonUC1').click()
    browser.find_element_by_link_text('CSV').click()
   
    securities_file_name = "Data_{}.csv".format(time.strftime("%Y%m%d",time.gmtime()))
    print('derivatives file was downloaded\n')
    parse_securities_info_data('/tmp/{}'.format(securities_file_name), '/tmp/securities.json')

if __name__ == "__main__":
    main()