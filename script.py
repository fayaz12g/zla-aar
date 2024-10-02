import os
import struct
from functions import *

def patch_blarc(aspect_ratio, HUD_pos, unpacked_folder, cutscene_zoomed):
    unpacked_folder = str(unpacked_folder)
    aspect_ratio = float(aspect_ratio)
    print(f"Aspect ratio is {aspect_ratio}")
    HUD_pos = str(HUD_pos)

    file_paths = {}

    def patch_blyt(filename, pane, operation, value):
        if operation in ["scale_x", "scale_y"]:
            if value < 1:
                command = "Squishing"
            elif value > 1:
                command = "Stretching"
            else:
                command = "Ignoring"
        elif operation in ["shift_x", "shift_y"]:
            command = "Shifting"
        
        print(f"{command} {pane} of {filename}")
        
        offset_dict = {'shift_x': 0x40, 'shift_y': 0x48, 'scale_x': 0x70, 'scale_y': 0x78}
        modified_name = filename + "_name"
        
        # Get all paths for the given filename
        paths = file_paths.get(modified_name, [])
        if not paths:
            # If no paths are found, create a default path and add it to the list
            default_path = os.path.join(unpacked_folder, "region_common", "ui", "Game", "blyt", f"{filename}.bflyt")
            paths.append(default_path)
        
        for full_path_of_file in paths:
            with open(full_path_of_file, 'rb') as f:
                content = f.read().hex()
            
            start_rootpane = content.index(b'RootPane'.hex())
            pane_hex = str(pane).encode('utf-8').hex()
            start_pane = content.index(pane_hex, start_rootpane)
            idx = start_pane + offset_dict[operation]
            content_new = content[:idx] + float2hex(value) + content[idx+8:]
            
            with open(full_path_of_file, 'wb') as f:
                f.write(bytes.fromhex(content_new))


    def patch_anim(source, filename, offset, value):
        modified_name = filename + "_name"
        
        # Get all paths for the given filename
        paths = anim_file_paths.get(modified_name, [])
        if not paths:
            # If no paths are found, create a default path and add it to the list
            default_path = os.path.join(unpacked_folder, "Layout", f"{source}.Nin_NX_NVN", "anim", f"{filename}.bflan")
            paths.append(default_path)
        
        # Iterate over each path and patch the corresponding file
        for anim_path in paths:
            with open(anim_path, 'rb') as f:
                content = f.read().hex()
            
            idx = offset
            content_new = content[:idx] + float2hex(value) + content[idx+8:]
            
            with open(anim_path, 'wb') as f:
                f.write(bytes.fromhex(content_new))

            
    blyt_folder = os.path.abspath(os.path.join(unpacked_folder))
    
    do_not_scale_rootpane = ["Ld_Fade"]
   
    rootpane_by_y = []

    if cutscene_zoomed:
        rootpane_by_y = rootpane_by_y + ["Movie"]
        do_not_scale_rootpane = do_not_scale_rootpane + ["Movie"]

    # Initialize a dictionary to store lists of paths
    file_paths = {}
    file_names_stripped = []

    for root, dirs, files in os.walk(blyt_folder):
        for file_name in files:
            if file_name.endswith(".bflyt"):
                stripped_name = file_name.strip(".bflyt")
                file_names_stripped.append(stripped_name)
                full_path = os.path.join(root, file_name)
                modified_name = stripped_name + "_name"
                if modified_name not in file_paths:
                    file_paths[modified_name] = []
                file_paths[modified_name].append(full_path)

    # Initialize a dictionary to store lists of paths
    anim_file_paths = {}
    anim_file_names_stripped = []

    for root, dirs, files in os.walk(blyt_folder):
        for file_name in files:
            if file_name.endswith(".bflan"):
                stripped_name = file_name.strip(".bflan")
                anim_file_names_stripped.append(stripped_name)
                full_path = os.path.join(root, file_name)
                modified_name = stripped_name + "_name"
                if modified_name not in anim_file_paths:
                    anim_file_paths[modified_name] = []
                anim_file_paths[modified_name].append(full_path)

    
    if aspect_ratio >= 16/9:
        s1 = (16/9)  / aspect_ratio
        print(f"Scaling factor is set to {s1}")
        s2 = 1-s1
        s3 = s2/s1
        s4 = (16/10) / aspect_ratio
        
        for name in file_names_stripped:
            if name in do_not_scale_rootpane:
                    print(f"Skipping RootPane scaling of {name}")
            if name not in do_not_scale_rootpane:
                patch_blyt(name, 'RootPane', 'scale_x', s1)
            if name in rootpane_by_y:
                patch_blyt(name, 'RootPane', 'scale_y', 1/s1)
                patch_blyt(name, 'RootPane', 'scale_x', 1)

        
        patch_blyt('Tl_Title', 'P_Movie_00', 'scale_x', 1/s1)   
        patch_blyt('Tl_Title', 'P_Movie_00', 'scale_y', 1/s1)  

        if HUD_pos == 'corner':
            print("Shifitng elements for corner HUD")
            patch_blyt('Cm_HUD', 'P_pict_00', 'shift_x', adjust_x(-618, s1))          
            patch_blyt('Cm_HUD', 'P_pict_01', 'shift_x', adjust_x(617, s1))     
            patch_blyt('Cm_HUD', 'P_pict_02', 'shift_x', adjust_x(-808, s1))   
            patch_blyt('Cm_HUD', 'N_Item_01', 'shift_x', adjust_x(4, s1))     
            patch_blyt('Cm_HUD', 'N_Item_01', 'shift_x', adjust_x(4, s1))      
            patch_blyt('Cm_HUD', 'N_Life_00', 'shift_x', adjust_x(-602, s1))      
            patch_blyt('Cm_HUD', 'N_Key_00', 'shift_x', adjust_x(-610, s1))      
            patch_blyt('Cm_HUD', 'N_SetItem_00', 'shift_x', adjust_x(4, s1))        
            patch_blyt('Cm_HUD', 'N_Item_00', 'shift_x', adjust_x(4, s1))      
            
            patch_blyt('Gm_HUDRupee', 'N_Rupee_00', 'shift_x', adjust_x(80, s1))    

            patch_blyt('Tl_Title', 'P_Logo_00', 'shift_x', adjust_x(-234, s1))    
            patch_blyt('Tl_Title', 'P_Logo_01', 'shift_x', adjust_x(-234, s1))   
            patch_blyt('Tl_Title', 'P_Logo_02', 'shift_x', adjust_x(-234, s1))   

            patch_blyt('Ld_ThrobberSave', 'A_alignment_00', 'shift_x', adjust_x(501, s1))   
            patch_blyt('Ld_Throbber', 'A_alignment_00', 'shift_x', adjust_x(501, s1))   

        # To mirror an object, do -x scale, and 180 roate y. For example, if we want to mirror something that is 

    else:
        s1 = aspect_ratio / (16/9)
        s2 = 1-s1
        s3 = s2/s1
        
        for name in file_names_stripped:
            if name in do_not_scale_rootpane:
                print(f"Skipping root pane scaling of {name}")
            if name not in do_not_scale_rootpane:
                print(f"Scaling root pane vertically for {name}")
                patch_blyt(name, 'RootPane', 'scale_y', s1)
             
    

        # if HUD_pos == 'corner':
        #     print("Shifitng elements for corner HUD")
