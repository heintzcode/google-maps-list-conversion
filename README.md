*Converting the URLs in a Google Maps Saved List into their map coordinates for upload into a Google MyMap*

What's this for?

You've spent a lot of time creating a list of places in a Google Map. Helpful! Now you want to change the colors by type of place or add in other sorts of customizations, but... you can't. 
What you've created is a list of places, not a custom map. You go to your laptop and find "Saved", and the tab for "Maps"... ah, that's what you need. 

You create a Google MyMap, and naturally look for an "Import List" option. No such luck. A search on the internet tells you that you have to export your Saved List using Google Takeout, which will give you a CSV file you can import it into your MyMap. 

Closer, but no. Your CSV does not include map coordinates, only Google Place URLs. No coordinates hidden in the URL, either.

Here is a script that will help you bridge this step. It automatically queries Google Maps for each of the URLs in your list, finds the lat/lon coordinates associated with each of those places, and adds them as new columns to your CSV.

Now you can upload your list into the MyMap and make all the customizations you were hoping for.

**Requirements**: A terminal that can run `python` with `pandas` and also the `wget` utility.
**Limitations**: This uses `wget` rather than the Google API, and is therefore subject to Google's limits on how many requests you can make from the same IP address. If your list is long, you may find that it errors out. I've tried to make the script fail gracefully so that you can keep the ones it succeeded on and try again with the remainder. The script is slow (waits a few seconds between queries) in order to avoid the error. The script is for occasional personal use, and will not be effective if you are trying to do this at scale.
**Usage**: > python add_latlon.py <infilename> <outfilename>
