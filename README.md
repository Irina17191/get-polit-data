# Crawler for collecting and storing data from API


Crawler for collecting structured data from the open PolitData API. 

The project implements an automated ETL pipeline that retrieves, parses, validates, and stores data from official public API endpoints. 

The processed data (including real estate assets, financial data, and other disclosures) is loaded into a structured database and used for further analytics and reporting.


## end-to-end data pipeline: 

✅ API ingestion  
✅ modular crawler  
✅ orchestration (main.py)   
✅ raw storage (Postgres)  
✅ BI layer (Superset)  


```
politdata_pipeline/
│
├── crawler/
│   ├── step_1.py
│   ├── step_2.py
│
├── main.py
├── load_to_postgres.py
├── requirements.txt
└── README.md
```




