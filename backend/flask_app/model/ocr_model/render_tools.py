
punctuation_dict = {
    "，": ",",
    "。": ".",

}
translation_table = str.maketrans(punctuation_dict)
 
def svg_to_html(svg_content, output_filename):

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SVG Embedded in HTML</title>
    </head>
    <body>
        <svg width="2100" height="15000" xmlns="http://www.w3.org/2000/svg">
            {svg_content}
        </svg>
    </body>
    </html>
    """

    with open(output_filename, 'w') as file:
        file.write(html_content)
 


content_mmd_to_html = """<!DOCTYPE html>
<html lang="en" data-lt-installed="true"><head>
  <meta charset="UTF-8">
  <title>Title</title>
  <script>
    const text = 
  </script>
  <style>
    #content {
      max-width: 800px;
      margin: auto;
    }
  </style>
  <script>
    let script = document.createElement('script');
    script.src = "https://cdn.jsdelivr.net/npm/mathpix-markdown-it@1.3.6/es5/bundle.js";
    document.head.append(script);

    script.onload = function() {
      const isLoaded = window.loadMathJax();
      if (isLoaded) {
        console.log('Styles loaded!')
      }

      const el = window.document.getElementById('content-text');
      if (el) {
        const options = {
          htmlTags: true
        };
        const html = window.render(text, options);
        el.outerHTML = html;
      }
    };
  </script>
</head>
<body>
  <div id="content"><div id="content-text"></div></div>
</body>
</html>
"""



tik_html = """
<!DOCTYPE html>

<html>

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Document</title>
<link rel="stylesheet" type="text/css" href="https://tikzjax.com/v1/fonts.css">
<script src="https://tikzjax.com/v1/tikzjax.js"></script>
</head>
<body>
<script type="text/tikz">
const text =
</script>
</body>
</html>"""



# print(tik_html)