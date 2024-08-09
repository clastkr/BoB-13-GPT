import struct

class GptHeader:
    def __init__(self, data):
        self.sign = data[0:8]
        self.revision = data[8:12]
        self.h_size = data[12:16]
        self.crc = data[16:20]
        self.rev = data[20:24]
        self.cur_lba = data[24:32]
        self.bkup_lba = data[32:40]
        self.start_part_lba = data[40:48]
        self.end_part_lba = data[48:56]
        self.disk_guid = data[56:72]

class GptPartEntry:
    def __init__(self, data):
        self.part_type = data[0:16]
        self.part_guid = data[16:32]
        self.first_lba, self.last_lba = struct.unpack('<QQ', data[32:48])
        self.attr_flags = data[48:56]
        self.part_name = data[56:128]

def print_info(entry):
    print("partition type GUID: ", " ".join(f"{x:02x}" for x in entry.part_type))
    print("unique partition GUID: ", " ".join(f"{x:02x}" for x in entry.part_guid))
    print("first LBA: ", f"{entry.first_lba:x}")
    print("last LBA: ", f"{entry.last_lba:x}")
    fsize = (entry.last_lba - entry.first_lba) * 512
    print("file size: ", f"{fsize:d}")

def main():
    try:
        with open("gpt_128.dd", "rb") as source:
            source.seek(0x400)
            entries = []

            for i in range(128):
                entry_data = source.read(128)
                if entry_data[0] == 0x00:
                    break
                entry = GptPartEntry(entry_data)
                entries.append(entry)

            for i, entry in enumerate(entries):
                print(f"partition {i+1}")
                print("\n")
                print_info(entry)

                real_offset = entry.first_lba * 512
                print("real offset: ", f"{real_offset:x}")
                source.seek(real_offset + 3)
                file_sys = source.read(4).decode('utf-8', errors='ignore')
                print("file system: ", file_sys)
                print("\n\n")

    except FileNotFoundError:
        print("파일 열기 오류")

if __name__ == "__main__":
    main()
