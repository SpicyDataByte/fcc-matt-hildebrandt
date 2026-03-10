
---

## 🚀 How It Works

The ETL process runs in the following order:

1. **Test Phase**: Automatically runs all unit tests in `/tests` before starting.
2. **Extract**: Loads raw CSV files from the local `data/` directory.
3. **Transform**:
   - Calculates session durations
   - Cleans payment methods
   - Merges datasets into a denormalized table
   - Aggregates metrics
5. **Validate**: Ensures data integrity using custom validators.
6. **Load**: Saves final and intermediate DataFrames to CSV files in the `output/` directory.
7.  **Insights**
     - Track minutes played by month to tell marketing which months to increase ad spend. 
     - Forecast: Applies a forecasting model to predict future registrations by payment method. Let's us target the fastest growing platforms.

---

## 🧪 Running the Pipeline
### Using Docker
install Docker: https://docs.docker.com/get-started/get-docker/

```bash
docker-compose up --build
```
### Locally

```bash
python -m venv venv
```
#### Windows
```
.\venv\Scripts\Activate.ps1

```
#### macOS/Linux
```
source venv/bin/activate

```
```
pip install -r requirements.txt

```
```
python main.py
```