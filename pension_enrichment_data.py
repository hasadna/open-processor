import re
import urllib3
import shutil
import json

"""
get back a link from given site
the link is identified by a regex
"""
def get_html_request(site, regex):
    #we need to change the user-agent, since if the site identifies python, it will be blocked
    http = urllib3.PoolManager(headers={'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0)'})
    response = http.request('GET', site, preload_content=False)
    if response.status != 200:
        print ('Error: {}\n was unable to reach {}'.format(response.status, site))
        exit(1)
 
    url = regex.findall(response.data)
    if len(url) == 0:
        print('was unable to find the necesary link. Existing')
        exit(2)
    return url[0].decode()

"""
parse the securities info csv into a json file
"""
def parse_securities_info_data(file_path,output_path):
    json_data = ''
    with open(file_path,'r',encoding = 'cp1255') as f:
        header = []
        json_record = {}
        for line in f:
            record =  line.split(',')
            if len(record) > 1 and len(header) == 0:
                header = record
                continue
            index = 0
            for item in header:
                if record[index].startswith('"'):
                    start = index
                    while not record[index].endswith('"'):
                        index += 1
                    json_record[item] = ','.join(record[start:index])
                    index += 1
                else: 
                    json_record[item] = record[index]
                    index += 1
            if len(json_record) > 1:
                json_data = json_data + json.dumps(json_record) + ','

    with open(output_path,'w') as f:
        f.write(json_data)

def main():
    #this is the address we will start from, looking for the link to download the file
    site = 'https://info.tase.co.il/heb/marketdata/securitiesinfo/Pages/SecuritiesInfo.aspx'
    #we will use this regex to find the link to open the link to the table we whish to parse
    regex = re.compile(b'customWindowOpen\(\'(/.*?)\'.*?' + re.escape('עמודות נוספות'.encode('utf-8')))
    # this is the address of the page with additional columns
    url = get_html_request(site, regex)
    regex2 = re.compile(b'customWindowOpen\(\'(/.*?)\'.*?\s.*CSV</a>\s')
    # this is the address of the link to download the file
    url2 = get_html_request('https://info.tase.co.il' + url, regex2)
    http = urllib3.PoolManager(headers={'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0)'})
    response = http.request('GET','https://info.tase.co.il' + url2, preload_content=False)
    if response.status != 200:
        print ('Error: {}\n was unable to reach {}'.format(response.status, site))
        exit(1)
    with open('/tmp/pension.csv','wb') as f:
        shutil.copyfileobj(response, f)
    print('file was downloaded\n')

    parse_securities_info_data('/tmp/pension.csv', '/tmp/pension.csv')
    
if __name__ == "__main__":
    main()