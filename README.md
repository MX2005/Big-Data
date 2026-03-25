# Crime Data Analysis & Clustering

## Team Members
### - Mahmoud Khaled : 231000616
### - Youssef Alaa   : 231000861
### - Youssef Kandil : 231000562
### - Ziad Khaled    : 231000621


##  Overview
This project performs exploratory data analysis and clustering on crime data.  
It includes:
- Distribution analysis (Histogram)
- Feature relationships (Pairplot)
- Correlation analysis (Heatmap)
- Clustering insights with top features per cluster

---

##  Docker Setup

### Build Docker Image
```bash
docker build -t crime-analysis .
```

### Run Container
```bash
docker run -it --rm crime-analysis
```

### Run with Mounted Volume (optional)
```bash
docker run -it --rm -v $(pwd):/app crime-analysis
```

---

##  Execution Flow

1. Load dataset  
2. Perform preprocessing:
   - Handle missing values
   - Encode categorical features
3. Exploratory Data Analysis (EDA):
   - Histogram of crime distribution by hour
   - Pairplot for relationships
   - Correlation matrix
4. Apply clustering algorithm (e.g., K-Means)
5. Extract top features for each cluster
6. Visualize results

---

##  Sample Outputs

### 1. Distribution of Crimes by Hour
![Histogram](Screenshot 2026-03-24 002816.png)

---

### 2. Pairplot Analysis
![Pairplot](Screenshot 2026-03-24 002848.png)

---

### 3. Correlation Matrix
![Correlation](Screenshot 2026-03-24 002920.png)

---

##  Clustering Results

### Cluster 0 - Key Features
Year: 2009.164276  
Beat: 383.263083  
Latitude: 41.768830  
Community Area: 37.981949  
Ward: 24.798343  
Hour: 13.230013  
Month: 5.378595  
District: 3.617633  
DayOfWeek: 3.043039  
Loc_Residential: 0.408163  
Loc_Public: 0.351384  
Arrest: 0.262410  
Top Crimes: THEFT, BATTERY, CRIMINAL DAMAGE  

---

### Cluster 1 - Key Features
Year: 2008.329786  
Beat: 1652.500079  
Latitude: 41.923034  
Ward: 38.314138  
Community Area: 20.680778  
District: 16.235187  
Hour: 12.941779  
Month: 4.936934  
DayOfWeek: 3.102621  
Loc_Public: 0.376092  
Loc_Residential: 0.336219  
Arrest: 0.262351  
Top Crimes: THEFT, BATTERY, NARCOTICS  

---

### Cluster 2 - Key Features
Year: 2009.046356  
Beat: 957.460293  
Latitude: 41.826289  
Community Area: 37.022778  
Ward: 28.326828  
Hour: 13.234856  
District: 9.346590  
Month: 5.339141  
DayOfWeek: 3.098929  
Loc_Public: 0.427850  
Loc_Residential: 0.377001  
Arrest: 0.309653  
Top Crimes: BATTERY, THEFT, NARCOTICS  

---

### Cluster 3 - Key Features
Beat: 2338.073706  
Year: 2007.190077  
Latitude: 41.891083  
Ward: 38.840125  
Community Area: 28.686122  
District: 20.996045  
Hour: 13.220038  
Month: 4.350551  
DayOfWeek: 3.097795  
Loc_Residential: 0.398011  
Loc_Public: 0.381592  
Arrest: 0.294703  
Top Crimes: THEFT, BATTERY, CRIMINAL DAMAGE  

---

## 📈 Key Insights

- Crime peaks during afternoon and evening hours  
- Weak correlation between most features  
- Strong negative correlation between Ward and Community Area  
