# -*- coding: utf-8 -*-

import struct
import sys
from phone import Phone


# build txt record from phone.dat
def build_record():
    self = Phone()
    start_offset = 8
    offset_map = {}
    records = []
    while start_offset < self.first_phone_record_offset:
        end_offset = self.buf.find(b'\x00', start_offset)
        record = self.buf[start_offset:end_offset]
        records.append(record)
        offset_map[start_offset] = record
        start_offset = end_offset + 1
    records.sort()
    offset_index = {}
    for k, v in offset_map.items():
        offset_index[k] = records.index(v)
    with open("record.txt", "wb") as f:
        for i, record in enumerate(records):
            f.write(str(i).encode())
            f.write(b',')
            f.write(record)
            f.write(b'\n')
    with open("phone.index", "wb") as f:
        current_offset = self.first_phone_record_offset
        while current_offset < len(self.buf):
            buffer = self.buf[current_offset: current_offset +
                              self.phone_fmt_length]
            cur_phone, record_offset, phone_type = struct.unpack(self.phone_fmt,
                                                                 buffer)
            f.write(str(cur_phone).encode())
            f.write(b',')
            f.write(str(offset_index[record_offset]).encode())
            f.write(b',')
            f.write(str(phone_type).encode())
            f.write(b'\n')
            current_offset += self.phone_fmt_length


def build_dat(version=b"2312"):
    self = Phone()
    index_offset = dict()
    init_offset = 8
    records = []
    record_length = 0
    with open("record.txt", "rb") as f:
        for line in f:
            index, record = line.strip().split(b",")
            index_offset[int(index.decode())] = init_offset
            init_offset += len(record) + 1
            record_length += len(record) + 1
            records.append(record)

    phones = []
    uniq_no = dict()
    with open("phone.index", "rb") as f:
        for line in f:
            phone_no, index, phone_type = [
                int(i.decode()) for i in line.split(b",")]
            if phone_no not in uniq_no:
                uniq_no[phone_no] = 1
                phones.append((phone_no, index_offset[index], phone_type))

    phones.sort(key=lambda x: x[0])

    with open("phone.dat2", "wb") as f:
        f.write(struct.pack(self.head_fmt, version, record_length+8))
        for record in records:
            f.write(record)
            f.write(b'\x00')
        for phone in phones:
            f.write(struct.pack(self.phone_fmt, *phone))


def test():
    phone1 = Phone()
    phone2 = Phone(dat_file="phone.dat2")
    phone1.get_phone_dat_msg()
    phone2.get_phone_dat_msg()
    for n in (131, 132, 133, 134, 135, 136, 137, 138, 139, 152, 153, 154, 155, 186, 188, 192, 193, 195, 199):
        for i in range(n*10000, n*10000+10000):
            assert phone1.find(i) == phone2.find(i)


def get_phone_type(phone_no):
    if phone_no.startswith("192"):
        return 7


def add_phone_no():

    city_code_index = {}
    with open("record.txt", "rb") as f:
        for line in f:
            index, record = line.strip().split(b",")
            city_code = record.decode().split("|")[3]
            city_code_index[city_code] = int(index.decode())
    for line in sys.stdin:
        line = line.strip().split()
        if not line:
            continue
        phone_no, city_code = line
        phone_type = get_phone_type(phone_no)
        index = city_code_index[city_code]
        print(f"{phone_no},{index},{phone_type}".format())


if __name__ == "__main__":
    if len(sys.argv) > 1:
        locals()[sys.argv[1]]()
    else:
        build_record()
