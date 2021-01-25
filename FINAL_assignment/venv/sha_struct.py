import hashlib
import struct


def genhash(file):
    # does what it says on the tin...

    with open(file, "br") as f:
        l = f.read()
        sha = hashlib.sha256()
        sha.update(l)
        sha256 = sha.hexdigest()
        return sha256


def checkhash(hash, file):
    # this checks an already known has for equivalence to hash of a file

    sha256 = ""
    with open(file, "br") as f:
        l = f.read()
        sha = hashlib.sha256()
        sha.update(l)
        sha256 = sha.hexdigest()

    return sha256 == hash


def packdata(data, packedsize=None):
    datatype = str(type(data)).split("\'")[1]
    if "bytearray"!= datatype:
        # convert to bytearray so we can unpack it easily
        data = bytearray(data, "utf-8")

    if packedsize:
        if packedsize % 4 != 0:
            print("cannot pack with required size, please input packedsize value that is divisible by 4")
            return None
    elif len(data) > int(packedsize/4):
        print("Cannot pack to desired size, data to be backed is over the packed_size parameter")


    structpack = ""
    addon = bytearray()
    if not packedsize:
        structpack = struct.Struct('i' * len(data))
    else:
        # 33 converts to "!" with utf-8
        addon.append(33)
        while len(addon) + len(data) < int(packedsize/4):
            addon.append(33)
        length = len(addon) + len(data)
        structpack = struct.Struct('i' * length)
        # data.append(*addon)
        data = (*data, *addon)
    packed = structpack.pack(*data)
    return packed, len(data)
    # len(packed is returned so we can send exactly that through socket...
    # it is actually an uniform value with GFTP as we always return two letters and sha256


def unpackdata(p_data, length):
    # this function only accepts class struct objects as a p_data value, length must be the length of the data before
    # ... it was packed.

    # the length conversion for length of packed objects below may not hold true in another projects, but it holds
    # ... true for GFTP. Let's require users know the correct length to unpack from (it's a required parameter)
    """ length = int(length / 4) """
    structpack = struct.Struct("= " + "i" * length)
    bt = structpack.unpack(p_data)
    restored = b""
    for val in bt:
        val = int.to_bytes(val, 1, "big")
        restored += val
    return restored


# example code:
"""
pgploc = "./M2296_public_key.asc"
command = "dl\r\n"
hash = genhash(pgploc)
truelen = len(hash)
hash = bytearray(hash, "utf-8")
command = bytearray(command, "utf-8")
values = command + hash
truelen = len(values)
#input(truelen)
packed, length = packdata(values, 348)
print(length)
unpacked = unpackdata(packed, length)
print(unpacked.decode("utf-8"))
"""
"""
bytetest = bytes("!", "utf-8")
test = int.from_bytes(bytetest, "big")
print(test)
"""