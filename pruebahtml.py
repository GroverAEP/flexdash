# from weasyprint import HTML
from weasyprint import HTML

html_content = """
<html>
<head>
    <style>
        h1 { color: blue; }
    </style>
</head>
<body>
    <h1>Hola Mundo</h1>
    <p>Este es un PDF generado desde HTML.</p>
</body>
</html>
"""

HTML(string=html_content).write_pdf("output.pdf")