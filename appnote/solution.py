from zipfile import ZipFile
from io import BytesIO
import sys

if __name__ == "__main__":
    zf = ZipFile(sys.argv[1])
    inner_data = zf.getinfo("hello.txt").comment

    flag = b""
    for n in range(19):
        wz = ZipFile(BytesIO(inner_data[: len(inner_data) - 22 * (18 - n)]))
        flag += wz.read(wz.filelist[0].filename)

    print(flag.decode())
