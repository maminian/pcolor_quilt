def export_patch(filename,real_parts, imag_parts, answers, cmname, attribution=""):
    '''
    Purpose: export essential information to duplicate your neato pcolor picture 
        to a file from which another person can load up the same image.
    
    Inputs:
        filename: string, must end in ".json" . Will save on your computer.
        real_parts: numpy array, x-coordinates (real parts used in your pcolor)
        imag_parts: numpy array, y-coordinates (real parts used in your pcolor)
        answers: 2D numpy array (counts, used in your pcolor)
        cmname: string, the name of the pyplot colormap you used.
            This should *exactly match* the final piece of the "cmap=..." argument.
            For example, if you used 
                cmap=plt.cm.viridis,
            you would type **in quotes**, "viridis", nothing more. This must 
            EXACTLY MATCH what you typed (upper/lower case and underscores are important)
        attribution: If you would like a small piece of text to appear in the image 
            to attribute your work to you, put it here as a string. This could be 
            your first name and last initial, first initial last name, 
            a nickname, your dog's name, etc. Keep it short, though (less than 15 chars).
            This will be embedded in the image when the patch is made.
            
            If you want to remain anonymous, you can put an empty string here.
            
    Example:
        export_patch("moo.json", real_parts, imag_parts, answers, "cividis", "Manuchehr A.")
    
    NOTE: 
        The patches will be *square* whether or not your viewing window was square. 
        Understand that if your viewing window is not square, your image will get smushed
        in the final quilt!
        
        "Square" means that yr - yl == xr - xl. 
        
        I will not be checking to see whether or not you have done this.
    '''
    import json
    
    obj = {
        'reals': real_parts.tolist(),
        'imags': imag_parts.tolist(),
        'array': answers.tolist(),
        'colormap_name': cmname,
        'attribution': attribution
        }
    with open(filename, 'w') as f:
        json.dump(obj,f)
    return 

def import_patch(filename):
    '''
    Purpose: load a json file assuming the file came from the result 
        of export_patch(...). This has enough information to produce a 
        "patch" in the quilt.
    Inputs: 
        filename: string, name of the json file.
    Outputs:
        obj: Python dictionary with the essentials to replicate the pcolor.
    '''
    import json
    import numpy as np
    
    with open(filename, 'r') as f:
        obj = json.load(f)
    obj['reals'] = np.array(obj['reals'], dtype=float)
    obj['imags'] = np.array(obj['imags'], dtype=float)
    obj['array'] = np.array(obj['array'], dtype=float)
    
    return obj

###############

if __name__=="__main__":
    import numpy as np
    from matplotlib import pyplot as plt
    
    thing = import_patch("moo.json") # if you exported your file already, replace the filename to test loading.
    fig,ax = plt.subplots()
    ax.pcolor(thing['reals'], thing['imags'], thing['array'], cmap=getattr(plt.cm, thing['colormap_name']))
    ax.text(0.02, 0.02, thing['attribution'], c='w', fontsize=10, transform=ax.transAxes)
    ax.set_aspect('equal')
    
    fig.show()