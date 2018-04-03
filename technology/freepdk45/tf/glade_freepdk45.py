import os
CWD = os.environ.get("OPENRAM_TECH") + "/freepdk45/tf"
ui().importCds("default", CWD+"/display.drf", CWD+"/FreePDK45.tf", 1000, 1, CWD+"/layers.map")




