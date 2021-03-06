from xml.dom import minidom
import subprocess
import sys

def get_webservers_list(nessus_xml_file):

        xmldoc = minidom.parse(nessus_xml_file)
        hosts = xmldoc.getElementsByTagName('ReportHost')
        webservers = set()
        for ip in hosts:
                ip_report_items = ip.getElementsByTagName('ReportItem')
                for report_item in ip_report_items:
                        if report_item.attributes['pluginName'].value == "Nessus SYN scanner" \
                        and \
                                (report_item.attributes['svc_name'].value =="www" or report_item.attributes['svc_name'].value=="https?" or report_item.attributes['svc_name'].value=="http?"):

                                webservers.add("http://"+ip.attributes['name'].value+":"+report_item.attributes['port'].value)
                                webservers.add("https://"+ip.attributes['name'].value+":"+report_item.attributes['port'].value)
        return webservers

def run_dirb(webserver):
        print webserver
        subprocess.Popen(["/usr/bin/dirb " + webserver+" -w  -o "+"massdirb/"+webserver[6:].strip('://')+".log"+" -X '',.txt"], shell=True)
x = raw_input('Enter your .nessus filename\n')
webservers = get_webservers_list(x)
subprocess.Popen(["rm "+"-rf "+"massdirb/"],shell=True)
subprocess.Popen(["mkdir "+"massdirb"],shell=True)
option = raw_input("Do you want to run dirb for each of these webservers or just output to list?: [type run or list] ")

if option == "list":
        f=open("massdirb/parsed_webservers.txt","w+")
        for webserver in webservers:
                f.write(webserver+"\n")
        f.close
        sys.exit(0)

elif option == "run":
        if len(sys.argv) == 2:
                webservers = set()
                webservers = set(line.strip() for line in open(sys.argv[1]))
        for webserver in webservers:
                run_dirb(webserver)
        sys.exit(0)
else:
        print "Unknown option, try again"
        sys.exit(0)
