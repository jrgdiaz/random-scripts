# random-scripts

massdirb

massdirb.py takes a .nessus file, parses out the webservers and then runs dirb on the background for earch webserver.
* To kill dirb processes use kill -KILL $(pgrep dirb)
* Writes all dirb output to the massdirb/ directory
