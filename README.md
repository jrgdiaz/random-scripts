# random-scripts

massdirb is a simple dirb wrap to bruteforce webserver directories massively

massdirb.py takes a .nessus file, parses out the webservers and then runs dirb on the background for earch webserver.
* Modify dirb binary arguments on script as needed
* To kill dirb processes use kill -KILL $(pgrep dirb)
* Writes all dirb output to the massdirb/ directory
