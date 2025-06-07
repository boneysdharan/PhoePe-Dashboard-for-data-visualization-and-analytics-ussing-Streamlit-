# 📊 PhonePe India Data Analysis Dashboard

This is an interactive **Streamlit dashboard** for analyzing **PhonePe** data across Indian states. It visualizes insights related to transactions, user engagement, device preferences, and insurance penetration.

## 🔍 Overview

The dashboard allows users to:

- Explore PhonePe transaction trends across states and time
- Understand user registration vs engagement dynamics
- Analyze insurance adoption and growth opportunities
- Examine mobile brand usage patterns
- Identify market expansion opportunities for PhonePe

## 🛠️ Features

- **Dynamic Dropdown Selector**: Choose a topic to view customized visualizations.
- **Interactive Charts**: Built using Plotly for smooth zoom, hover, and pan.
- **State-wise Analysis**: Includes top and bottom performing states.
- **Growth Trends**: Line charts depicting multi-year growth for states.
- **Data Tables**: Easy-to-read summaries of key metrics.

## 📊 Business Case Studies Taken

- **Device Dominance and User Engagement Analysis**
- **Insurance Penetration and Growth Potential Analysis**
- **Decoding Transaction Dynamics on PhonePe**
- **User Engagement and Growth Strategy**
- **Transaction Analysis for Market Expansion**
- **Insurance Engagement Analysis**

## ▶️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/phonepe-dashboard.git
cd phonepe-dashboard

2. Install Requirements
bash
Copy
Edit
pip install -r requirements.txt
Ensure Python 3.8+ is installed.

3. Run the Dashboard
bash
Copy
Edit
streamlit run streamlit_app.py
🧩 Dependencies
streamlit

plotly

pandas

os, sys (standard Python libraries)

Install all required packages using:

bash
Copy
Edit
pip install streamlit plotly pandas
📌 Notes
Ensure the extract_data module contains the appropriate pre-processed data and visualizations.

Make sure you're running the script from the project root to allow correct relative imports.

----------------------------------------------------


Before going to dashboard, it is important to extract data, clean it and store in MYSQL.
Here we choose the data present in "data" folder of this project.
for example, let us consider Map Insurance Hover State Data present in map/insurance/hover/state

See map_insurance.ipynb for reference where we extract data containing columns

- State name
- Year and Quarter
- Insurance name
- Insurance count and amount

The data is pulled from hover tooltips visible in PhonePe's map-based insurance analytics.

## 🛠️ Features

- Recursively traverses nested folders for each state, year, and quarter.
- Parses JSON data from PhonePe's hover map format.
- Extracts metrics like insurance count and amount.
- Stores the cleaned and processed data in a single Pandas DataFrame.

---

## ▶️ How It Works

### ✅ Input Format

- The input files are structured as JSONs inside:
data/map/insurance/hover/country/india/state/<state>/<year>/<quarter>.json

- Each JSON contains:
```json
{
  "data": {
    "hoverDataList": [
      {
        "name": "ICICI",
        "metric": [
          {
            "type": "insurance",
            "count": 1000,
            "amount": 500000.0
          }
        ]
      }
    ]
  }
}
🧾 Output
The resulting DataFrame has columns:

State

Year

Quater

Insurance

Insurance_count

Insurance_amount

🐍 Example Output
python
Copy
Edit
       State  Year  Quater Insurance  Insurance_count  Insurance_amount
0      delhi  2018       1    ICICI             1000          500000.0
1      delhi  2018       1      HDFC              800          300000.0


Make sure to have python and install required libraries like pandas, os and json
----------------------------------------

Next step is to store the data in MySQL.


Connects to a MySQL database using `mysql-connector-python`.
- Creates a table named `Map_Insurance_State`.
- Converts a DataFrame into a list of tuples.
- Performs bulk insert using `executemany()`.

---

## 🛠️ Requirements

- Python 3.8+
- MySQL Server
- Python Libraries:
  - `mysql-connector-python`
  - `pandas`

Install the required connector:

```bash
pip install mysql-connector-python (for python 3 its pip3)
🧾 Table Schema
sql
Copy
Edit
CREATE TABLE Map_Insurance_State (
  State VARCHAR(100),
  Year INT,
  Quater INT,
  Insurance_Type VARCHAR(100),
  Insurance_count FLOAT,
  Insurance_amount FLOAT
);


🗃️ Script Breakdown
🔗 1. Establish MySQL Connection
python
Copy
Edit
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="xxxxx",
    database="xxx"
)
Replace xxxxx and xxx with your actual MySQL password and database name.
🔐 Security Tip
Never commit your database password or credentials directly in code. Use environment variables or configuration files.

🏗️ 2. Create Table
python
Copy
Edit
query1 = """
    CREATE TABLE Map_Insurance_State (
        State VARCHAR(100),
        Year INT,
        Quater INT,
        Insurance_Type VARCHAR(100),
        Insurance_count FLOAT,
        Insurance_amount FLOAT
    )
"""
cursor.execute(query1)
🧱 3. Prepare Data for Insertion
python
Copy
Edit
data = []
for index in Map_Insu_state.index:
    row = Map_Insu_state.loc[index]
    data.append((
        row[0],                # State
        int(row[1]),           # Year
        int(row[2]),           # Quarter
        row[3],                # Insurance Type
        int(row[4]),           # Insurance Count
        float(row[5])          # Insurance Amount
    ))
📥 4. Insert Data into MySQL
python
Copy
Edit
query2 = "INSERT INTO Map_Insurance_State VALUES (%s, %s, %s, %s, %s, %s)"
cursor.executemany(query2, data)
connection.commit()
✅ Output
All records from the DataFrame are inserted into your MySQL table.

Use SQL queries to explore or join this data with other analytics.

🧪 Example Query
sql
Copy
Edit
SELECT State, SUM(Insurance_amount) AS Total_Insurance
FROM Map_Insurance_State
GROUP BY State
ORDER BY Total_Insurance DESC;

-------------------------------------------------------------------
Once this is done, now we need to clean the data present in the Dataframe

The script includes:

1. **Missing value check**
2. **Label encoding for categorical values**
3. **One-hot encoding for multiple features**
4. **Outlier detection and removal

State` (e.g., Tamil Nadu, Gujarat)
- `Year` (e.g., 2018–2022)
- `Quater` (1, 2, 3, 4)
- `Insurance` (insurance provider/type)
- `Insurance_count` (number of users who purchased insurance)
- `Insurance_amount` (total premium amount)

---

## 🧪 Cleaning Steps

### ✅ Step 1: Check for Nulls

```python
Map_Insu_state.isna().sum()
Map_Insu_state.info()
Ensures there are no NaN values.

Confirms data types before transformation.

🧬 Step 2: Encoding
➤ Label Encoding
Encodes the Insurance column into integer codes.

python
from sklearn.preprocessing import LabelEncoder

encoder = LabelEncoder()
Map_Insu_state['encoded_insurance'] = encoder.fit_transform(Map_Insu_state['Insurance'])
➤ One-Hot Encoding
Applies one-hot encoding on State, Year, and Quater to convert them into binary features:

python
Map_Insu_state = pd.get_dummies(Map_Insu_state, columns=['Year', 'State', 'Quater'], dtype=int)
⚠️ Step 3: Outlier Removal
Outliers are detected using the z-score method (±3 standard deviations):

python
Copy
Edit
Map_Insu_state['insurance_count_std'] = (
    Map_Insu_state['Insurance_count'] - Map_Insu_state['Insurance_count'].mean()
) / Map_Insu_state['Insurance_count'].std()

Map_Insu_state['insurance_amount_std'] = (
    Map_Insu_state['Insurance_amount'] - Map_Insu_state['Insurance_amount'].mean()
) / Map_Insu_state['Insurance_amount'].std()
Then rows outside the ±3 range are filtered out:

python
Copy
Edit
Map_Insu_state = Map_Insu_state[
    (Map_Insu_state['insurance_count_std'] <= 3) &
    (Map_Insu_state['insurance_count_std'] >= -3) &
    (Map_Insu_state['insurance_amount_std'] <= 3) &
    (Map_Insu_state['insurance_amount_std'] >= -3)
]
📦 Output
A cleaned and encoded Pandas DataFrame, ready for:

Statistical analysis

Machine learning modeling

Visualization dashboards (e.g., Streamlit, Power BI)

-----------------------------------------------------------
Now we can visualize our data using streamlit. 
Do data extraction before streamlit and do data cleaning as it is really important.
Have fun with this. Try out new data visualization of your choice.

THANK YOU.


