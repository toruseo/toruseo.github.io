#coding:shift-jis

import re
import datetime
import os

for lang in ["jp", "en"]:
	print("--------------------------------------------\nHTML:", lang, "\n--------------------------------------------")
	
	### .tex ###
	tex_f = open("tex_%s/cv_%s.tex"%(lang, lang), "r", encoding="utf-8")
	tex = []
	for l in tex_f:
		if l[0] != "%" and len(l) > 1 and l[:2] != "\t%":
			tex.append(l)
	tex_f.close()


	### .bbl ###
	bib_f = open("tex_%s/cv_%s.bbl"%(lang, lang), "r", encoding="utf-8")
	bib = {}
	bib_pdf = {}
	for l in bib_f:
		if l[:7] != "\\begin{" and l[:5] != "\\end{" and l != "\n":
			m = re.search(r"\\bibitem\{(.*?)\}", l)
			if m:
				key = m.group(1)
				bib[key] = ""
				continue
			m = re.search(r"(.*)(\d{4})\.\n", l)
			if m:
				l = m.group(1)+""+m.group(2)+"."+"\n"
			bib[key] += l[:-1]+" "
	bib_f.close()

	for key in bib.keys():
		b = bib[key][:]
		
		b = b.replace("瀬尾亨", "<u>瀬尾亨</u>", 3)
		b = b.replace("Seo,~T.", "<u>Seo,~T.</u>", 3)
		b = b.replace("\\_", "_", len(b))
		
		m = re.search(r"(.*?) \\newblock(.*?) \\newblock(.*)", b)
		if m:
			b = m.group(1)+" "+m.group(2)+" "+m.group(3)
			
		m = re.search(r"(.*)\\href\{(.*?)\}\{(.*?)\}\.(.*)", b)
		if m:
			b = m.group(1)+'<a href="'+m.group(2)+'" target="_blank">'+m.group(3)+"</a>."+m.group(4)
		
		m = re.search(r"(.*)\{\\em (.*?)\}(.*)", b)
		if m:
			b = m.group(1)+"<i>"+m.group(2)+"</i>"+m.group(3)
		bib[key] = b
		
		paperpath = "out/toruseo.github.io/paper/"
		if os.path.exists(paperpath+key+".pdf"):
			bib_pdf[key] = ' <a href="paper/'+key+'.pdf" target="_blank">[PDF]</a>'


	### main processes ###

	html = []

	f_start = 0

	for i,ll in enumerate(tex):
		l = ll[:-1]
		if f_start == 1:
			### pre-process ###
			m = re.search(r"\\cvitem\{(.*)\}\{\\href\{(.*?)\}\{(.*?)\}\}", l)
			if m:
				#print(i, "Pre.href")
				html.append("<li>"+'<b><a href="'+m.group(2)+'" target="_blank">'+m.group(1)+"</a></b>"+"</li>")
				continue
			
			while 1:
				m = re.search(r"(.*)\\href\{(.*?)\}\{(.*?)\}(.*)", l)
				if m:
					#print(i, "Pre.href")
					l = m.group(1)+'<a href="'+m.group(2)+'" target="_blank">'+m.group(3)+"</a>"+m.group(4)
				else:
					break

			m = re.search(r"(.*)\{\\hfill\\footnotesize\\sffamily\\bfseries (.*)\}", l)
			if m:
				#print(i, "Pre.award")
				l = m.group(1)+'<b><font color="red">'+m.group(2)+"</font></b>"
			
			m = re.search(r"(.*)\{\\it (.*)\}(.*)", l)
			if m:
				#print(i, "Pre.award")
				l = m.group(1)+'<i>'+m.group(2)+"</i>"+m.group(3)
			
			l = l.replace("\\{", "(", len(l))
			l = l.replace("\\}", ")", len(l))
			
			m = re.search(r"(.*)\\underline\{(.*?)\}(.*)", l)
			if m:
				#print(i, "Pre.underline")
				l = m.group(1)+'<u>'+m.group(2)+"</u>"+m.group(3)
			### process ###
#			if l[:8] == "\\section":
#				html.append("</ul>\n\n<h3>"+l[9:-1]+"</h3>\n<ul>\n")
#				continue
			if l[:8] == "\\section":
				html.append("""</ul></div>\n\n<div onclick="obj=document.getElementById('"""+l[9:-1]+"""').style;obj.display=(obj.display=='none')?'block':'none';">
				<a style="cursor:pointer;"><h3>"""+l[9:-1]+"""</h3></a></div>\n"""+"""<div id='"""+l[9:-1]+"""' style="display:none;clear:both;">"""+"""<ul>\n""")
				continue
			
			#色：hex(int(0xff-(0xff-0x96)/10))
			if l[:11] == "\\subsection":
				html.append("</ul>\n\n<h4>"+l[12:-1]+"</h4>\n<ul>\n")
				continue
			
			m = re.search(r"\\cvitem\{(.*)\}\{(.*)\}", l)
			if m:
				if m.group(1) != "":
					html.append("<li>"+"<b>"+m.group(1)+"</b>: "+m.group(2)+"</li>")
				else:
					html.append("<li>"+m.group(2)+"</li>")
				continue
			
			m = re.search(r"\\cventry\{(.*)\}\{(.*)\}\{(.*)\}\{(.*)\}\{(.*)\}\{(.*)\}", l)
			if m:
				if m.group(1) == "":
					cm = {}
					for j in range(3, 7):
						if m.group(j) != "":
							cm[j] = ", "+m.group(j)
						else:
							cm[j] = " "
					html.append("<li>"+m.group(2)+"<i>"+cm[3]+cm[4]+cm[5]+cm[6]+"</i></li>")
				else:
					for j in range(3, 7):
						if m.group(j) != "":
							cm[j] = ", "+m.group(j)
						else:
							cm[j] = " "
					html.append("<li>"+"<b>["+m.group(1)+"]</b> "+m.group(2)+"<i>"+cm[3]+"</i>"+cm[4]+cm[5]+cm[6]+"</li>")
				continue
			
			if l == "\\begin{etaremune}":
				eta_counter = 0
				for lll in tex[i:]:
					if re.search(r"\\item", lll):
						eta_counter += 1
					if re.search(r"\\end\{etaremune\}", lll):
						break
				#print(i, "etaremune", eta_counter)
				continue
			
			m = re.search(r"\\item \\bibentry{(.*?)}(.*)", l+" ")
			if m:
				if m.group(1) in bib_pdf:
					pdf_txt = bib_pdf[m.group(1)]
				else:
					pdf_txt = ""
				
				html.append("<dt>"+"%2d"%eta_counter+"</dt><dd>"+bib[m.group(1)]+"&nbsp;"+m.group(2)+pdf_txt+"</dd>")
				eta_counter -= 1
				continue
			
			m = re.search(r"\t\\begin{description}", l)
			if m:
				html.append("<ul>")
				continue
			m = re.search(r"\t\\end{description}}", l)
			if m:
				html.append("</ul>")
				continue
			m = re.search(r"\t\t\\item -(.*)", l)
			if m:
				html.append("<li>"+m.group(1)+"</li>")
				continue
			m = re.search(r"\t\t\\item \\textsf{(.*):} (.*)", l)
			if m:
				html.append("<li>"+m.group(1)+": "+m.group(2)+"</li>")
				continue
			
			if l == "\\end{document}" or l == "\\end{etaremune}":
				continue
			
			#html.append(l+"<br>")
			print("\t", i, "UNK", l)
		
		if l == "\\makecvtitle":
			f_start = 1
	
	
	
	### post-process ###
	html_c = "\n".join(html)
	html_c = html_c.replace("<ul>\n\n<dt>", '<dl class="etaremuneList">\n\n<dt>', len(html_c))
	html_c = html_c.replace("</dd>\n</ul>", '</dd></dl>', len(html_c))
	html_c = html_c.replace("</dd></ul>", '</dd></dl>', len(html_c))
	
	html_c = html_c.replace("\\htmlonly{", "", len(html_c))
	
	html_c = html_c.replace("{", "", len(html_c))
	html_c = html_c.replace("}", "", len(html_c))
	
	html_c = html_c.replace("---", "&mdash;", len(html_c))
	html_c = html_c.replace("--", "&ndash;", len(html_c))
	
	html_c = html_c.replace("``", '"', len(html_c))
	html_c = html_c.replace("''", '"', len(html_c))
	html_c = html_c.replace("`", "'", len(html_c))
	html_c = html_c.replace("'", "'", len(html_c))
	html_c = html_c.replace('\\"u', "&uuml;", len(html_c))
	html_c = html_c.replace('\\_', '_', len(html_c))
	html_c = html_c.replace('\\#', '#', len(html_c))
	
	
	html_c = html_c.replace("~", " ", len(html_c))
	html_c = html_c.replace("\\hspace0.25em", " ", len(html_c))
	html_c = html_c.replace("\\&", "&", len(html_c))
	html_c = html_c.replace("&nbsp;% ", "&nbsp; ", len(html_c))
	html_c = html_c.replace("&nbsp;%% ", "&nbsp; ", len(html_c))
	html_c = html_c.replace("%", "", len(html_c))
	html_c = html_c.replace("\\newblock", "", len(html_c))
	html_c = html_c.replace(" , %", "", len(html_c))
	html_c = html_c.replace("%</li>", "</li>", len(html_c))
	html_c = html_c.replace(". &nbsp;, ", ". ", len(html_c))
	html_c = html_c.replace(" &nbsp; </dd>", "</dd>", len(html_c))
	html_c = html_c.replace("</i>  , </li>", "</i></li>", len(html_c))
	
	f = open("shortbio_jp.txt", "r", encoding="utf-8")
	shortbio_jp = f.read()
	f.close()
	
	f = open("shortbio_en.txt", "r", encoding="utf-8")
	shortbio_en = f.read()
	f.close()
	
	f = open("head.txt", "r", encoding="utf-8")
	head = f.read()
	f.close()
	
	### HTML-lize ###
	n = datetime.datetime.now()
	if lang == "jp":
		lang_dependent = (
			"ja",
			"瀬尾亨 - 東京大学",
			"瀬尾亨",
			"履歴書（%4d-%02d-%02d現在）"%(n.year, n.month, n.day),
			"jp",
			"版",
			"index_en",
			"English version",
			"略歴",
			shortbio_jp,
		)
		
		f = open("end_jp.txt", "r", encoding="utf-8")
		lang_dependent_end = f.read()
		f.close()
		
	else:
		lang_dependent = (
			"en",
			"Toru Seo, The University of Tokyo",
			"Toru Seo",
			"Curriculum Vitae (as of %4d-%02d-%02d)"%(n.year, n.month, n.day),
			"en",
			" version",
			"index",
			"日本語版",
			"Short Bio",
			shortbio_en,
		)
		
		f = open("end_en.txt", "r", encoding="utf-8")
		lang_dependent_end = f.read()
		f.close()
		

	#<meta name="Keywords" content="東大,社基,UTokyo">
	
	html_c = """<!DOCTYPE html>
	<html lang="%s">
	<head>"""%lang_dependent[0] + head + """
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<meta http-equiv="Pragma" content="no-cache">
	<meta http-equiv="Cache-Control" content="no-cache">
	<meta http-equiv="Expires" content="0">
	<meta name="Author" content="Toru Seo">
	<meta name="viewport" content="width=device-width">
	<link rel="stylesheet" type="text/css" href="css/cv.css">
	<title>%s</title>
	</head>
	
	<body>
	<h1>%s</h1>
	<h2>%s</h2>
	<p align="center">
	<a href="cv_%s.pdf" target="_blank">PDF%s</a>&nbsp;<a href="%s.html">%s</a>
	</p>
	<h3>%s</h3>
	<p style="margin-left:1em;margin-right:1em;">
		%s
	</p>
	<ul>
	"""%lang_dependent[1:] + html_c + "</ul></div>\n" + lang_dependent_end + "</body>\n</html>"
	html_c = html_c.replace("</dd></ul>", '</dd></dl>', len(html_c))
	
	if lang=="jp":
		html_f = open("out/index.html", "w", encoding="utf-8")
	elif lang=="en":
		html_f = open("out/index_en.html", "w", encoding="utf-8")
	html_f.write(html_c)
	html_f.close()