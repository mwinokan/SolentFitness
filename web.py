
def html_page(title,target,html_content,gw,footer_html=None):

	fout = open(target,'wt')

	fout.write('<!DOCTYPE html>\n')
	fout.write('<html>\n')
	fout.write('<head>\n')
	fout.write(f'<title>{title}</title>\n')
	fout.write('<meta charset="UTF-8">\n')
	fout.write('<meta name="viewport" content="width=device-width, initial-scale=1">\n')
	fout.write('<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">\n')
	fout.write('<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Oswald">\n')
	fout.write('<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Open Sans">\n')
	fout.write('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">\n')
	fout.write('<style>\n')
	fout.write('h1,h2,h3,h4,h5,h6 {font-family: "Oswald"}')
	fout.write('body {font-family: "Open Sans"}\n')
	fout.write('h5.double {line-height: 2}\n')
	fout.write('</style>\n')
	fout.write('</head>\n')
	fout.write('<!-- w3-content defines a container for fixed size centered content, ')
	fout.write('and is wrapped around the whole page content, except for the footer in this example -->\n')
	fout.write('<div class="w3-content" style="max-width:2000px">\n')
	fout.write('<!-- Header -->\n')
	fout.write('<header class="w3-container w3-center w3-padding-48" style="background-color:#22235F">\n')

	workmark_url = 'https://github.com/mwinokan/SolentFitness/blob/main/assets/SOLENT_Wordmark_White.png?raw=true'
	fout.write(f'<img class="w3-image" src="{workmark_url}" alt="SOLENT" width="30%"> ')

	# fout.write('<h1 class="w3-xxxlarge"><b>FPL <span class="w3-tag">GUI</span></b></h1>\n')
	# fout.write('<h6>Max Winokan</h6>\n')
	
	fout.write('</header>\n')
	fout.write('<!-- Grid -->\n')
	fout.write('<div class="w3-row w3-border">\n')
	fout.write('<!-- Content -->\n')
	fout.write('<div class="w3-col l12 s12">\n') 
	fout.write('<div class="w3-container w3-white w3-padding">\n')
	fout.write('<div class="w3-justify">\n')
	fout.write(html_content)
	fout.write('</div>\n')
	fout.write('</div>\n')
	fout.write('<hr>\n')
	fout.write('</div>\n')
	fout.write('<!-- END GRID -->\n')
	fout.write('</div>\n')
	fout.write('<!-- END w3-content -->\n')
	fout.write('<!-- Footer -->\n')
	fout.write('<footer class="w3-container" style="padding:32px;background-color:#CCCCE5">\n')
	if footer_html is not None:
		fout.write(footer_html)
	fout.write('<a href="#" class="w3-button w3-black w3-padding-large w3-margin-bottom"><i class="fa fa-arrow-up w3-margin-right"></i>Back to top</a>\n')
	fout.write('<div class="w3-center">\n')

	from datetime import datetime
	timestamp = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

	fout.write(f'<p>Accurate as of {timestamp}, (GW{gw})</p>\n')
	fout.write('<p>Max Winokan <span class="w3-tag">mwinokan@me.com</span></a></p>\n')
	fout.write('</div>\n')
	fout.write('</footer>\n')
	fout.write('</html>\n')

	fout.close()
