import requests
import sqlite3
import xml.etree.ElementTree as ET

# Step 1: Download the Unimod XML file
url = "https://www.unimod.org/xml/unimod.xml"
response = requests.get(url)
if response.status_code == 200:
    with open("unimod.xml", "wb") as f:
        f.write(response.content)
else:
    print("Failed to download Unimod XML")
    exit()

# Step 2: Parse the XML file
tree = ET.parse("unimod.xml")
root = tree.getroot()

# Step 3: Create SQLite database
conn = sqlite3.connect("unimod.db")
cursor = conn.cursor()

# Create table for modifications
cursor.execute("""
CREATE TABLE IF NOT EXISTS modifications (
    id INTEGER PRIMARY KEY,
    title TEXT,
    full_name TEXT,
    mass FLOAT,
    specificity TEXT
)
""")

# Step 4: Extract relevant data from XML and insert into SQLite
# I was only interested in the modification names and their monoisotopic masses, so I retrieved information accordingly.
for mod in root.find("modifications").findall("modifications_row"):
    unimod_id = int(mod.get("record_id")) if mod.get("record_id") else None
    full_name = mod.get("full_name")
    composition = mod.get("composition")
    mono_mass = float(mod.get("mono_mass")) if mod.get("mono_mass") else None
    avge_mass = float(mod.get("avge_mass")) if mod.get("avge_mass") else None

    # Insert into database
    cursor.execute("INSERT INTO modifications (unimod_id, full_name, composition, mono_mass, avge_mass) VALUES (?, ?, ?, ?, ?)",
                   (unimod_id, full_name, composition, mono_mass, avge_mass))

# Commit and close
conn.commit()
conn.close()

print("Modifications successfully stored in unimod_modifications.db")
