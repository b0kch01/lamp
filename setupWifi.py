#!/usr/bin/env python

import sys
import os

args = sys.argv[1:]
print(args)

with open("/etc/wpa_supplicant/wpa_supplicant.conf", "r+") as config:
    new_network = os.popen("wpa_passphrase " + "'" + args[0] + "' " + "'" + args[1] + "'").read()

    # If command above is a success, it would also include a comment
    # so we can use that to check if it has completed succesfully or not

    if "#psk=" in new_network:
        new_network_split = new_network.split("\n")
        removed_plaintext_password = new_network_split[0:2] + ["\tpriority=1"] + new_network_split[3:5]
        final_network_data = "\n" + "\n".join(removed_plaintext_password) + "\n"

        if final_network_data not in config.read():
            config.write(final_network_data)
    
        print("Everything went well--NICE!")

    else:
        print("Something went wrong! (Contact us about this please!) Generated wifi data: ", new_network)

    config.close()
