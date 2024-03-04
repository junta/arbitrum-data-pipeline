import re

urls = [
    "https://forum.arbitrum.foundation/t/aip-arbos-version-20-atlas/20957",
    "https://forum.arbitrum.foundation/t/procurement-committee-application-elections-on-snapshot/20536?u=dk3",
    "https://forum.arbitrum.foundation/t/final-arbitrum-stable-treasury-endowment-program/20139/33",
    "https://forum.arbitrum.foundation/t/arbitrums-short-term-incentive-program-arbitrum-improvement-proposal/16131/",
]

# Regular expression to match the Forum ID in the URL
pattern = r"/(\d{5})/?"

# Extracting IDs using the regular expression
ids = [int(re.search(pattern, url).group(1)) for url in urls if re.search(pattern, url)]

print(ids)
