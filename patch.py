import os
import math
from functions import *

def create_patch_files(patch_folder, ratio_value, scaling_factor, visual_fixes):

    visual_fixesa = visual_fixes[0]
    scaling_factor = float(scaling_factor)
    ratio_value = float(ratio_value)
    print(f"The scaling factor is {scaling_factor}.")
    reversed_hex, hex_value = zla_hex23(ratio_value)
    version_variables = ["1.0.1"]
    for version_variable in version_variables:
        file_name = f"main-{version_variable}.pchtxt"
        file_path = os.path.join(patch_folder, file_name)

        if version_variable == "1.0.1":
            nsobidid = "909E904AF78AC1B8DEEFE97AB2CCDB51968F0EC7"
            visual_fix = visual_fixesa

        patch_content = f'''@nsobid-{nsobidid}

@flag print_values
@flag offset_shift 0x100

@enabled
016af7d0 {reversed_hex}
0001092c 20D147BD
00852AD8 {hex_value}
@disabled

{visual_fix}

// Generated using ZLA-AAR by Fayaz (github.com/fayaz12g/zla-aar)
// Made possible by Fl4sh_#9174'''
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as patch_file:
            patch_file.write(patch_content)
        print(f"Patch file created: {file_path}")
