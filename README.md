# airfold-llm-observability

## Getting Started

### 1. Create a Virtual Environment (Optional)

To isolate dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

Install all required Python packages:

```bash
python3 -m pip install -r requirements.txt
```

### 3. Configure Airfold

Run the following to configure Airfold:

```bash
af config
```

Paste your Airfold API key when prompted.

### 4. Set Data Generation Parameters

Open `src/main.py` and configure the following:

- `batch`: Number of rows per batch
- `no_of_rows`: Total number of rows to generate

Adjust these as per your data generation needs.

### 5. Run the Program

You can run the generator with different modes:

- **Generate Historical Data**

  ```bash
  python src/main.py --old
  ```

  This will generate data with random dates from `2024-01-01` to today.  
  **Recommended config**: `batch=1000`

- **Generate Streaming Data**
  ```bash
  python src/main.py --stream
  ```
  This simulates streaming ingestion of data.  
  **Recommended config**: `batch=1000`
