import pandas as pd
import random
import re
import sys
import subprocess
import time

flags = {'errored_out': False}

def main(infile_csv, outfile_csv):
    df = pd.read_csv(infile_csv)
    df = df.dropna(how="all")
    df[['lat', 'lon']] = df['URL'].apply(get_latlon)
    df.to_csv(outfile_csv)

def get_latlon(url):
    # If the wget calls have failed, return a default (graceful failure)
    if flags['errored_out']:
        return pd.Series([None, None])
    
    # use the wget package to return the webpage associated with the url, allow redirection
    cmd = [
        "wget",
        "--max-redirect=5",
        "--server-response",
        "-O", "-",
        url
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if "ERROR 429" in result.stderr:
        print(f"Pinged the google server too many times, returning null lat/lons for urls starting at {url}")
        print(f"You can try again later for the remaining ones")
        flags['errored_out'] = True
        return pd.Series([None, None])

    # If it didn't error out, lat/lon is hidden somewhere in the html
    html = result.stdout
    print(f"Returned {len(html)} html lines for {url}, sleeping")

    # Sleep for a few seconds to avoid ERROR 429 - increase values if you get the error a lot
    time.sleep(random.choice(range(2,5)))

    # Find and return the lat/lon
    pattern = re.compile("@(\d\d\.\d+),(-\d\d.\d+),")
    try:
        coords = re.search(pattern, html).groups()
        return pd.Series([coords[0], coords[1]])
    except:
        return pd.Series([None, None])


if __name__ == '__main__':
    if not len(sys.argv) == 3:
        print(f"Usage: python add_latlon.py infile_csv outfile_csv")
    else:
        main(sys.argv[1], sys.argv[2])
