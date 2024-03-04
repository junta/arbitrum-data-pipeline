# Arbitrum Governance Data Pipeline

This is a [Dagster](https://dagster.io/) project gathering Arbitrum Governance-related data

Output files(CSV&Parquet) on 2024 March 3rd are available on Ocean Protocol
https://market.oceanprotocol.com/asset/did:op:a2b08c506e0d857db49d9252a6eaadffa03364b9bc2bf1fdb2498014b82dece4

## Data Sources

### 1. Forum 
https://forum.arbitrum.foundation/

Data format/description: https://docs.discourse.org
- Topics
- Posts
- Categories
- Users

### 2. Snapshot
https://snapshot.org/#/arbitrumfoundation.eth

Data format/description: https://docs.snapshot.org/tools/api

- Proposals
- Votes

Also pre-processing(extract forum_topic_id from raw URL, etc.) for following analytics work.

### 3. Karma
https://arbitrum.karmahq.xyz/

Data format/description: https://documenter.getpostman.com/view/26295147/2s93RTPrfg#72d3c26b-d30b-4d42-9af9-9fa6bc63c0d5

- Delegates

### 4. Tally
https://www.tally.xyz/gov/arbitrum

Data format/description: https://docs.tally.xyz/user-guides/welcome

They require API KEY, so [get it here](https://docs.tally.xyz/user-guides/welcome#how-to-use-the-tally-api) and fill TALLY_API_KEY in .env file

- Proposals


## How to run and export the latest data
With Docker
```bash
docker build -t arbitrum-dagster .
docker run -p 3000:3000 -d arbitrum-dagster
```

Without Docker
```bash
pip install -r requirements.txt
dagster dev
```

Open http://localhost:3000 with your browser to see the project.

Then, select Asset and click "Materialize"

![Dagster Image](https://raw.githubusercontent.com/junta/arbitrum-data-pipeline/main/images/sample_dagster_lineage.png)

Output files are exported under /output_data as CSV and Parquet format.