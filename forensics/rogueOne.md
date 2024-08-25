# RogueOne
- This is a memory forensics based ctf, as per the description we are given a memory dump from a compromized system.
- We'll be using Volatilty for this purpose. A good [cheatsheet](https://blog.onfvp.com/post/volatility-cheatsheet/).
- Starting by base information of the file
```sh
file 20230810.mem 
20230810.mem: Windows Event Trace Log
```
- Question 1 wants us to give the process id of the malicious process, it's mentioned in the description as during the time of memory dump the connection wit c2 was persent so it's good to take a look at netstat results.
```sh
python3 vol.py -f 20230810.mem windows.netstat.NetStat

Offset	        Proto	LocalAddr	 LocalPort	ForeignAddr	ForeignPort	State	PID	Owner	Created

0x9e8b90fe82a0	TCPv4	172.17.79.131	64263	20.54.24.148	443	ESTABLISHED	6136	svchost.exe	2023-08-10 11:31:18.000000 UTC
0x9e8b8aedeab0	TCPv4	172.17.79.131	64239	192.229.221.95	80	CLOSE_WAIT	8224	SearchApp.exe	2023-08-10 11:28:48.000000 UTC
0x9e8b8cb58010	TCPv4	172.17.79.131	64254	13.127.155.166	8888	ESTABLISHED	6812	svchost.exe	2023-08-10 11:30:03.000000 UTC
0x9e8b905ed260	TCPv4	172.17.79.131	64217	23.215.7.17	443	CLOSE_WAIT	8224	SearchApp.exe	2023-08-10 11:28:45.000000 UTC
0x9e8b9045f8a0	TCPv4	172.17.79.131	63823	20.198.119.84	443	ESTABLISHED	3404	svchost.exe	2023-08-10 11:14:21.000000 UTC
0x9e8b8cee4010	TCPv4	172.17.79.131	64237	13.107.213.254	443	CLOSE_WAIT	8224	SearchApp.exe	2023-08-10 11:28:47.000000 UTC
0x9e8b8b2e4a20	TCPv4	172.17.79.131	64218	20.198.118.190	443	ESTABLISHED	3404	svchost.exe	2023-08-10 11:28:45.000000 UTC
```
- These top process looks a little suspicious other information just includes general services listening for connection.
- Next step is to check more about these processes, we can do that using pstree command.
```sh
python3 vol.py -f 20230810.mem windows.pstree.PsTree
** 3404	788	svchost.exe	0x9e8b8a562080	7	-	0	False	2023-08-10 11:13:44.000000 UTC	N/A	\Device\HarddiskVolume3\Windows\System32\svchost.exe	C:\WINDOWS\system32\svchost.exe -k netsvcs -p -s WpnService	C:\WINDOWS\system32\svchost.exe
*** 8224	928	SearchApp.exe	0x9e8b89d92080	55	-	1	False	2023-08-10 11:14:14.000000 UTC	N/A	\Device\HarddiskVolume3\Windows\SystemApps\Microsoft.Windows.Search_cw5n1h2txyewy\SearchApp.exe	"C:\WINDOWS\SystemApps\Microsoft.Windows.Search_cw5n1h2txyewy\SearchApp.exe" -ServerName:CortanaUI.AppX8z9r6jm96hw4bsbneegw0kyxx296wr9t.mca	C:\WINDOWS\SystemApps\Microsoft.Windows.Search_cw5n1h2txyewy\SearchApp.exe
** 6136	788	svchost.exe	0x9e8b8b34a080	11	-	0	False	2023-08-10 11:13:53.000000 UTC	N/A	\Device\HarddiskVolume3\Windows\System32\svchost.exe	C:\WINDOWS\System32\svchost.exe -k NetworkService -p -s DoSvc	C:\WINDOWS\System32\svchost.exe
*** 6812	7436	svchost.exe	0x9e8b87762080	3	-	1	False	2023-08-10 11:30:03.000000 UTC	N/A	\Device\HarddiskVolume3\Users\simon.stark\Downloads\svchost.exe	"C:\Users\simon.stark\Downloads\svchost.exe" 	C:\Users\simon.stark\Downloads\svchost.exe
**** 4364	6812	cmd.exe	0x9e8b8b6ef080	1	-	1	False	2023-08-10 11:30:57.000000 UTC	N/A	\Device\HarddiskVolume3\Windows\System32\cmd.exe	C:\WINDOWS\system32\cmd.exe	C:\WINDOWS\system32\cmd.exe
```
- We can see that the process 6812 is a parent process for cmd.exe, this looks suspicious, we can check the process list what is the 7436 pid for.
```sh
python3 vol.py -f 20230810.mem windows.pslist.PsList | grep 7436
7436	7400	explorer.exe	0x9e8b8c4d2080	75	-	1	False	2023-08-10 11:14:07.000000 UTC	N/A	Disabled
9580	7436	SecurityHealth	0x9e8b90135340	1	-	1	False	2023-08-10 11:14:25.000000 UTC	N/A	Disabled
9712	7436	vmtoolsd.exe	0x9e8b8cbd5080	9	-	1	False	2023-08-10 11:14:26.000000 UTC	N/A	Disabled
5864	7436	WinRAR.exe	0x9e8b92bdb0c0	5	-	1	False	2023-08-10 11:20:21.000000 UTC	N/A	Disabled
936	7436	svchost.exe	0x9e8b8cd89080	0	-	1	False	2023-08-10 11:22:31.000000 UTC	2023-08-10 11:27:51.000000 UTC	Disabled
6812	7436	svchost.exe	0x9e8b87762080	3	-	1	False	2023-08-10 11:30:03.000000 UTC	N/A	Disabled
2776	7436	RamCapture64.e	0x9e8b8aa66080	5	-	1	False	2023-08-10 11:31:52.000000 UTC	N/A	Disabled
```
- We can see that 7436 is for File Explorer, this confirms our suspicion.
- Question 2 asks about sub process that the malicious process created, we already identified this information.
- Question 3 is asking for hash of the malicious process. For this we have dump the process executable, for this purpose we use procdump.
- We have to take md5sum of the executable.
```sh
python3 vol.py -f 20230810.mem -o dump/ windows.dumpfiles.DumpFiles --pid 6812
ls
file.0x9e8b878da570.0x9e8b88576bf0.ImageSectionObject.nsi.dll.img
file.0x9e8b878da700.0x9e8b88562c20.ImageSectionObject.kernel32.dll.img
file.0x9e8b878da890.0x9e8b885b7bf0.ImageSectionObject.shlwapi.dll.img
file.0x9e8b878daed0.0x9e8b878d7ca0.ImageSectionObject.sechost.dll.img
file.0x9e8b878db1f0.0x9e8b878d6920.ImageSectionObject.gdi32.dll.img
file.0x9e8b882ca920.0x9e8b882e4010.ImageSectionObject.ntdll.dll.img
file.0x9e8b884f70c0.0x9e8b884b3a20.ImageSectionObject.rpcrt4.dll.img
file.0x9e8b884f7570.0x9e8b884bacc0.ImageSectionObject.user32.dll.img
file.0x9e8b884f8ce0.0x9e8b88488a90.DataSectionObject.imm32.dll.dat
file.0x9e8b884f8ce0.0x9e8b884baa20.ImageSectionObject.imm32.dll.img
file.0x9e8b8851f890.0x9e8b88560d00.ImageSectionObject.ole32.dll.img
file.0x9e8b8851f890.0x9e8b8856fa90.DataSectionObject.ole32.dll.dat
file.0x9e8b885201f0.0x9e8b88164d40.ImageSectionObject.msvcrt.dll.img
file.0x9e8b88520380.0x9e8b8853ebb0.ImageSectionObject.oleaut32.dll.img
file.0x9e8b88520380.0x9e8b8856e7d0.DataSectionObject.oleaut32.dll.dat
file.0x9e8b885206a0.0x9e8b8855fd00.ImageSectionObject.ws2_32.dll.img
file.0x9e8b88520830.0x9e8b8855bc10.ImageSectionObject.combase.dll.img
file.0x9e8b885f4250.0x9e8b88576990.ImageSectionObject.psapi.dll.img
file.0x9e8b885f4570.0x9e8b87cbe3b0.ImageSectionObject.bcrypt.dll.img
file.0x9e8b885f4d40.0x9e8b885764d0.ImageSectionObject.bcryptprimitives.dll.img
file.0x9e8b885f5510.0x9e8b885c4ce0.ImageSectionObject.gdi32full.dll.img
file.0x9e8b885f56a0.0x9e8b88576010.ImageSectionObject.win32u.dll.img
file.0x9e8b885f5b50.0x9e8b881a9c00.ImageSectionObject.advapi32.dll.img
file.0x9e8b886c3d40.0x9e8b886726e0.ImageSectionObject.crypt32.dll.img
file.0x9e8b886c4830.0x9e8b88680d20.ImageSectionObject.msvcp_win.dll.img
file.0x9e8b886c4b50.0x9e8b88677b20.ImageSectionObject.KernelBase.dll.img
file.0x9e8b886e03e0.0x9e8b88575990.ImageSectionObject.ucrtbase.dll.img
file.0x9e8b886f89d0.0x9e8b88a5ada0.DataSectionObject.locale.nls.dat
file.0x9e8b893990e0.0x9e8b882f9d30.ImageSectionObject.profapi.dll.img
file.0x9e8b89399400.0x9e8b88af3d30.ImageSectionObject.sspicli.dll.img
file.0x9e8b893998b0.0x9e8b88ac1d30.ImageSectionObject.userenv.dll.img
file.0x9e8b894b3860.0x9e8b88a9ad80.ImageSectionObject.msasn1.dll.img
file.0x9e8b894b4b20.0x9e8b8941bcc0.ImageSectionObject.cryptsp.dll.img
file.0x9e8b894b4cb0.0x9e8b8943ba20.ImageSectionObject.cryptbase.dll.img
file.0x9e8b894b5de0.0x9e8b894c9220.DataSectionObject.SortDefault.nls.dat
file.0x9e8b894d2850.0x9e8b89442cf0.ImageSectionObject.IPHLPAPI.DLL.img
file.0x9e8b894d2d00.0x9e8b8943da20.ImageSectionObject.mswsock.dll.img
file.0x9e8b894d3980.0x9e8b89442a20.ImageSectionObject.dnsapi.dll.img
file.0x9e8b894d50f0.0x9e8b89491a20.ImageSectionObject.wkscli.dll.img
file.0x9e8b894d69f0.0x9e8b89492d20.ImageSectionObject.rsaenh.dll.img
file.0x9e8b89de1740.0x9e8b89daf7f0.ImageSectionObject.dhcpcsvc.dll.img
file.0x9e8b89de26e0.0x9e8b89e02050.ImageSectionObject.dhcpcsvc6.dll.img
file.0x9e8b89f9e870.0x9e8b889f3a70.ImageSectionObject.winhttp.dll.img
file.0x9e8b8a4de640.0x9e8b8a6062b0.ImageSectionObject.netapi32.dll.img
file.0x9e8b8a4e3460.0x9e8b8a60d920.ImageSectionObject.winmm.dll.img
file.0x9e8b8a4e4270.0x9e8b8a656d00.ImageSectionObject.mpr.dll.img
file.0x9e8b8ae25140.0x9e8b8a7e5a20.ImageSectionObject.cscapi.dll.img
file.0x9e8b8b0708b0.0x9e8b8a2a3d20.ImageSectionObject.wininet.dll.img
file.0x9e8b91ec0140.0x9e8b90819750.DataSectionObject.svchost.exe.dat
file.0x9e8b91ec0140.0x9e8b957f24c0.ImageSectionObject.svchost.exe.img

md5sum file.0x9e8b91ec0140.0x9e8b957f24c0.ImageSectionObject.svchost.exe.img
5bd547c6f5bfc4858fe62c8867acfbb5  file.0x9e8b91ec0140.0x9e8b957f24c0.ImageSectionObject.svchost.exe.img
```
- Question 4 wants us to identify the IP and port of the C2 server and Question 5 wants the time when the connection was established. We can obtain these information we can see from the response of the netstat command.
```sh
0x9e8b8cb58010	TCPv4	172.17.79.131	64254	13.127.155.166	8888	ESTABLISHED	6812	svchost.exe	2023-08-10 11:30:03.000000 UTC
```
- Question 6 asks us about the memory offset of the malicious process. This information can be taken from the result of pslist command.
```sh
6812	7436	svchost.exe	0x9e8b87762080	3	-	1	False	2023-08-10 11:30:03.000000 UTC	N/A	Disabled
```
- Question 7 wants us to tell the time when the details about this malware was first updated on virustotal, for this go to [virustotal](https://www.virustotal.com/gui) uplaod the file and check the history section under details tab.

**COMPLETE**
