# multiple rounds of hashing and combo of byte source and system entropy

import json
import hashlib


def hashed_bytes():
    bytes = list()
    bytes1 = list()

    with open("color_data.json", "r+") as infile:
        parsed_data = json.load(infile) # parse color data file
        # print(parsed_data)

        print("---------------------------")

        for i in parsed_data:
            # bytes.extend(i.split())
            # splitting by comma every 21 values for 7 dominant colors
            i = i.split(",")
            # print(i)
            for j in i:
                #     # print(j)
                encoded_str = j.encode('utf-8')  # need to encode b4 hash
                hash = hashlib.sha256(encoded_str).hexdigest() # sha 256 hash
                bytes1.append(j)
                bytes.append(hash) #appending the hash to list will use for seed later

        print("++++++++++++++++++++++++++++++++++++++")

    print(bytes)
    print(bytes1)


hashed_bytes()
