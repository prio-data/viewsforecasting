#small function to import SAR_logo
from Tools.visualization_assetts.external_imports_all import*

def import_SAR_logo():
    this_dir = os.path.dirname(__file__)
    SAR_logo_path = os.path.join(this_dir, 'SAR_logo.png')
    output = plt.imread(SAR_logo_path)
    print(f'{user}, logo imported')
    return output