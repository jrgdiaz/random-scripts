import requests, sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

if len(sys.argv) != 5:

    print("[~] Usage : python nessus_tool.py [url] [username] [password] [folderid]")
    exit()

url = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
folderid = sys.argv[4]
folder_param = {'folder_id': folderid}

def nessus_login(username, password):
        params = {"username": username, "password": password}
        authtoken = requests.post(url+"/session", data=params, verify=False)
        return  {"X-Cookie": "token="+authtoken.json().get("token")}

def get_scans(folder):
        cookie = nessus_login(username, password)
        scans = requests.get(url+"/scans", params=folder_param ,headers=cookie, verify=False)
        listOfScans = scans.json()
        for scan in listOfScans['scans']:
                download_scan(cookie, scan['id'], scan['name'])

def download_scan(cookie, scan_id, scan_name):
        format = {"format": "nessus"}
        file_id = requests.post(url+"/scans/"+str(scan_id)+"/export", data = format, headers=cookie, verify=False)
        file_id =  file_id.json().get("file")

        while True:

                resp = check_available(cookie, file_id, scan_id)
                if resp:
                        data = requests.get(url+"/scans/"+str(scan_id)+"/export/"+str(file_id)+"/download", params=folder_param ,headers=cookie, verify=False)
                        print "writing: "+scan_name
                        open("NESSUS-SCANS/"+scan_name + ".nessus", 'wb').write(data.content)
                        break

def check_available(cookie, file_id, scan_id):
         resp = requests.get(url+"/scans/"+str(scan_id)+"/export/"+str(file_id)+"/status", params=folder_param ,headers=cookie, verify=False)
         resp = resp.json().get("status")
         if resp != "ready":
                return False
         else:
                return True

get_scans(folderid)
