import os, sys


MAIN_PATHS: list[str] = [
        "src",
        "src/lib",
        "src/lib/lib_core",
        "src/lib/lib_app",
        "src/plugins",
        "src/plugins/amino",
        "src/plugins/google"
    ]

ADDITIONAL_PATHS: list[str] = [
        "src/lib/init",
        "src/lib/lib_plugins", 
        "src/lib/lib_plugins/amino",
        "src/lib/lib_plugins/amino/chat_notify_guard",
        "src/lib/lib_plugins/google",
        "src/lib/lib_plugins/google/sheets"
    ]

for path in MAIN_PATHS:
    if os.path.isdir(path) == False:
        sys.exit(str(f"[PATH]: {path}  -  DOESN'T EXIST"))

for path in ADDITIONAL_PATHS:
    if os.path.isdir(path) == False:
        os.mkdir(path)
