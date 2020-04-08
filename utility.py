
def read_keys(file):
    with open('keys.txt', 'r') as fp:
        pk = fp.readline().rstrip()
        sk = fp.readline().rstrip()
        return pk, sk


def write_html(data, file):
    header = """ 
    <html><head><link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" 
    integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    </head><body>
            """

    footer = "</body></html>"

    data = data.replace("<table>", "<table class='table'")

    data = header + data + footer

    with open(file, 'w+') as fp:
        fp.write(data)
        fp.close()
