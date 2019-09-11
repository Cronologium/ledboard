def hex2tuple(hexstring):
    if hexstring[0] == '#':
        hexstring = hexstring[1:]
    return (
        int(hexstring[:2], 16),
        int(hexstring[2:4], 16),
        int(hexstring[4:], 16)
    )