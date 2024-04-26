import os
DEBUG                   = True
HOST                    = "0.0.0.0"
PORT                    = 5000

SINGLE_REPO_PATH        = r"C:\\BIOS\\firmware.boot.uefi.iafw.intel"
SPARSE_CHECKOUT_PATH    = r"C:\\BIOS\\sparse_checkout_generator"
DATABASE_PATH            = r"C:\\PCMD\\database"
TOOL_STATS_FILE         = os.path.join("instance","tool_statistics.json")
REPO_STATS_FILE         = os.path.join("instance","repo_statistics.json")  
AVAILABLE_TAGS_FILE     = os.path.join("instance","available_tags.json")
SUPPORTED_PROJECTS_FILE = os.path.join(os.getcwd(),"pcmd_app","json_data","supported_projects.json")
INSTANCE_PATH           = os.path.join(os.getcwd(),"instance")
CACHED_DOCS_FILE        = os.path.join("instance","cached_docs.json")
CACHED_DOCS_PATH        = os.path.join(os.getcwd(),"templates","Generated")
CONFIG_FILE_PATH        = os.path.join("config_files")
