import tempfile, zipfile
import os

def fix_xlsx(in_file):
    tmpfd, tmp = tempfile.mkstemp(dir=os.path.dirname(in_file))
    os.close(tmpfd)
    filename = '[Content_Types].xml'
    data = ''
    with zipfile.ZipFile(in_file, 'r') as zin:
        with zipfile.ZipFile(tmp, 'w') as zout:
            for item in zin.infolist():
                if item.filename != filename:
                    zout.writestr(item, zin.read(item.filename))
                else:
                    data = zin.read(filename).decode()
    os.remove(in_file)
    os.rename(tmp, in_file)
    data = data.replace('/xl/sharedStrings.xml', '/xl/SharedStrings.xml')
    with zipfile.ZipFile(in_file, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(filename, data)