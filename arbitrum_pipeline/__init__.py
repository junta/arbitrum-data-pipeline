from dagster import Definitions, load_assets_from_modules

from . import forum
from . import snapshot
from . import karma
from . import tally

all_assets = load_assets_from_modules([forum, snapshot, karma, tally])

defs = Definitions(
    assets=all_assets,
)
