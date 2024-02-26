from dagster import Definitions, load_assets_from_modules

from . import forum
from . import snapshot

all_assets = load_assets_from_modules([forum, snapshot])

defs = Definitions(
    assets=all_assets,
)
