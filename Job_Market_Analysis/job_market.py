# ============================================================
# PRDA-04 JOB MARKET ANALYSIS
# Complete Python Analysis
# ============================================================

import os
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 1. MYSQL DATABASE CONNECTION
# ============================================================

connection = mysql.connector.connect(
    host="your_host",
    user="ur_username",
    password="ur_password",   # <-- PUT YOUR MYSQL PASSWORD HERE
    database="project_job_market_analysis"
)



# ============================================================
# 2. LOAD DATA FROM MYSQL
# ============================================================

query = "SELECT * FROM Market"

df = pd.read_sql(query, connection)

print("\nDataset loaded successfully!")
print("Dataset shape:", df.shape)


# ============================================================
# 3. CLOSE MYSQL CONNECTION
# ============================================================

connection.close()

print("MySQL connection closed.")


# ============================================================
# 4. CREATE OUTPUT FOLDERS
# ============================================================

os.makedirs("output", exist_ok=True)
os.makedirs("output/charts", exist_ok=True)
os.makedirs("output/analysis_tables", exist_ok=True)


# ============================================================
# 5. SAVE ORIGINAL DATASET
# ============================================================

df.to_csv("output/job_market_data.csv", index=False)

print("\nOriginal dataset saved.")


# ============================================================
# 6. BASIC DATASET INFORMATION
# ============================================================

print("\n========== DATASET INFORMATION ==========")

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)


# ============================================================
# 7. DATA QUALITY CHECK
# ============================================================

print("\n========== DATA QUALITY CHECK ==========")

# Replace -1 with NaN for analysis
df_clean = df.replace(-1, pd.NA)

missing_values = df_clean.isnull().sum()

missing_table = pd.DataFrame({
    "Column": missing_values.index,
    "Missing_Values": missing_values.values
})

missing_table = missing_table.sort_values(
    by="Missing_Values",
    ascending=False
)

print(missing_table)

missing_table.to_csv(
    "output/analysis_tables/missing_values.csv",
    index=False
)


# ============================================================
# 8. TOTAL JOB POSTINGS
# ============================================================

total_jobs = len(df)

print("\n========== TOTAL JOB POSTINGS ==========")
print("Total Jobs:", total_jobs)


# ============================================================
# 9. JOB POSTINGS BY LOCATION
# ============================================================

location_analysis = (
    df[df["Job_Location"].notna() & (df["Job_Location"] != "-1")]
    .groupby("Job_Location")
    .size()
    .reset_index(name="Job_Postings")
    .sort_values("Job_Postings", ascending=False)
)

print("\n========== TOP JOB LOCATIONS ==========")
print(location_analysis.head(10))

location_analysis.to_csv(
    "output/analysis_tables/location_analysis.csv",
    index=False
)


# Chart: Top 10 Locations

top_locations = location_analysis.head(10)

plt.figure(figsize=(10, 6))

plt.barh(
    top_locations["Job_Location"][::-1],
    top_locations["Job_Postings"][::-1]
)

plt.xlabel("Number of Job Postings")
plt.ylabel("Location")
plt.title("Top 10 Locations by Data Science Job Postings")

plt.tight_layout()

plt.savefig(
    "output/charts/top_10_locations.png",
    dpi=300
)

plt.close()


# ============================================================
# 10. SALARY BY LOCATION
# ============================================================

salary_location = (
    df[
        (df["Job_Location"].notna()) &
        (df["Job_Location"] != "-1")
    ]
    .groupby("Job_Location")
    .agg(
        Job_Postings=("ID", "count"),
        Average_Minimum_Salary_K=("Lower_Salary", "mean"),
        Average_Maximum_Salary_K=("Upper_Salary", "mean"),
        Average_Salary_K=("Avg_SalaryK", "mean")
    )
    .reset_index()
)

salary_location[
    [
        "Average_Minimum_Salary_K",
        "Average_Maximum_Salary_K",
        "Average_Salary_K"
    ]
] = salary_location[
    [
        "Average_Minimum_Salary_K",
        "Average_Maximum_Salary_K",
        "Average_Salary_K"
    ]
].replace(-1, pd.NA)

salary_location = salary_location.dropna(
    subset=["Average_Salary_K"]
)

salary_location = salary_location.sort_values(
    "Average_Salary_K",
    ascending=False
)

salary_location.to_csv(
    "output/analysis_tables/salary_by_location.csv",
    index=False
)

print("\n========== HIGHEST AVERAGE SALARY LOCATIONS ==========")
print(salary_location.head(10))


# ============================================================
# 11. TOP 5 INDUSTRIES
# ============================================================

industry_analysis = (
    df[
        (df["Industry"].notna()) &
        (df["Industry"] != "-1")
    ]
    .groupby("Industry")
    .size()
    .reset_index(name="Job_Postings")
    .sort_values("Job_Postings", ascending=False)
)

top_5_industries = industry_analysis.head(5)

print("\n========== TOP 5 INDUSTRIES ==========")
print(top_5_industries)

top_5_industries.to_csv(
    "output/analysis_tables/top_5_industries.csv",
    index=False
)


# Chart: Top 5 Industries

plt.figure(figsize=(10, 6))

plt.bar(
    top_5_industries["Industry"],
    top_5_industries["Job_Postings"]
)

plt.xlabel("Industry")
plt.ylabel("Job Postings")
plt.title("Top 5 Industries by Data Science Job Postings")

plt.xticks(rotation=45, ha="right")

plt.tight_layout()

plt.savefig(
    "output/charts/top_5_industries.png",
    dpi=300
)

plt.close()


# ============================================================
# 12. TOP COMPANIES
# ============================================================

company_analysis = (
    df[
        (df["Company_Name"].notna()) &
        (df["Company_Name"] != "-1")
    ]
    .groupby("Company_Name")
    .size()
    .reset_index(name="Job_Openings")
    .sort_values("Job_Openings", ascending=False)
)

top_companies = company_analysis.head(10)

print("\n========== TOP COMPANIES ==========")
print(top_companies)

top_companies.to_csv(
    "output/analysis_tables/top_companies.csv",
    index=False
)


# Chart: Top Companies

plt.figure(figsize=(10, 6))

plt.barh(
    top_companies["Company_Name"][::-1],
    top_companies["Job_Openings"][::-1]
)

plt.xlabel("Job Openings")
plt.ylabel("Company")
plt.title("Top 10 Companies by Data Science Job Openings")

plt.tight_layout()

plt.savefig(
    "output/charts/top_10_companies.png",
    dpi=300
)

plt.close()


# ============================================================
# 13. TOP JOB TITLES
# ============================================================

job_title_analysis = (
    df[
        (df["Job_Title"].notna()) &
        (df["Job_Title"] != "-1")
    ]
    .groupby("Job_Title")
    .size()
    .reset_index(name="Job_Postings")
    .sort_values("Job_Postings", ascending=False)
)

top_job_titles = job_title_analysis.head(10)

print("\n========== TOP JOB TITLES ==========")
print(top_job_titles)

top_job_titles.to_csv(
    "output/analysis_tables/top_job_titles.csv",
    index=False
)


# Chart: Top Job Titles

plt.figure(figsize=(10, 6))

plt.barh(
    top_job_titles["Job_Title"][::-1],
    top_job_titles["Job_Postings"][::-1]
)

plt.xlabel("Job Postings")
plt.ylabel("Job Title")
plt.title("Top 10 Data Science Job Titles")

plt.tight_layout()

plt.savefig(
    "output/charts/top_10_job_titles.png",
    dpi=300
)

plt.close()


# ============================================================
# 14. SALARY BY TOP JOB TITLES
# ============================================================

job_salary_analysis = (
    df[
        (df["Job_Title"].notna()) &
        (df["Job_Title"] != "-1")
    ]
    .groupby("Job_Title")
    .agg(
        Job_Postings=("ID", "count"),
        Average_Minimum_Salary_K=("Lower_Salary", "mean"),
        Average_Maximum_Salary_K=("Upper_Salary", "mean"),
        Average_Salary_K=("Avg_SalaryK", "mean")
    )
    .reset_index()
)

job_salary_analysis = job_salary_analysis.sort_values(
    "Job_Postings",
    ascending=False
)

top_job_salary = job_salary_analysis.head(10)

top_job_salary.to_csv(
    "output/analysis_tables/salary_by_top_job_titles.csv",
    index=False
)


# ============================================================
# 15. SKILL DEMAND ANALYSIS
# ============================================================

skill_columns = {
    "Python": "Python",
    "Spark": "spark",
    "AWS": "aws",
    "Excel": "excel",
    "SQL": "sql_",
    "SAS": "sas",
    "Keras": "keras",
    "PyTorch": "pytorch",
    "Scikit-learn": "scikit",
    "TensorFlow": "tensor",
    "Hadoop": "hadoop",
    "Tableau": "tableau",
    "BI": "bi",
    "Flink": "flink",
    "MongoDB": "mongo",
    "Google Analytics": "google_an"
}

skill_results = []

for skill_name, column_name in skill_columns.items():

    skill_count = df[column_name].sum()

    skill_results.append({
        "Skill": skill_name,
        "Job_Postings": skill_count
    })

skill_analysis = pd.DataFrame(skill_results)

skill_analysis = skill_analysis.sort_values(
    "Job_Postings",
    ascending=False
)

print("\n========== MOST DEMANDED SKILLS ==========")
print(skill_analysis)

skill_analysis.to_csv(
    "output/analysis_tables/skill_demand.csv",
    index=False
)


# Chart: Skill Demand

plt.figure(figsize=(10, 7))

plt.barh(
    skill_analysis["Skill"][::-1],
    skill_analysis["Job_Postings"][::-1]
)

plt.xlabel("Job Postings Requiring Skill")
plt.ylabel("Skill")
plt.title("Demand for Data Science Skills")

plt.tight_layout()

plt.savefig(
    "output/charts/skill_demand.png",
    dpi=300
)

plt.close()


# ============================================================
# 16. EDUCATION VS SALARY
# ============================================================

education_salary = (
    df[
        (df["Degree"].notna()) &
        (df["Degree"] != "-1")
    ]
    .groupby("Degree")
    .agg(
        Job_Count=("ID", "count"),
        Average_Salary_K=("Avg_SalaryK", "mean"),
        Average_Minimum_Salary_K=("Lower_Salary", "mean"),
        Average_Maximum_Salary_K=("Upper_Salary", "mean")
    )
    .reset_index()
)

education_salary = education_salary.sort_values(
    "Average_Salary_K",
    ascending=False
)

print("\n========== EDUCATION VS SALARY ==========")
print(education_salary)

education_salary.to_csv(
    "output/analysis_tables/education_vs_salary.csv",
    index=False
)


# Chart: Education vs Salary

plt.figure(figsize=(8, 5))

plt.bar(
    education_salary["Degree"],
    education_salary["Average_Salary_K"]
)

plt.xlabel("Education Level")
plt.ylabel("Average Salary ($K)")
plt.title("Average Salary by Education Level")

plt.tight_layout()

plt.savefig(
    "output/charts/education_vs_salary.png",
    dpi=300
)

plt.close()


# ============================================================
# 17. SENIORITY VS SALARY
# ============================================================

seniority_salary = (
    df[
        (df["seniority_by_title"].notna()) &
        (df["seniority_by_title"] != "-1")
    ]
    .groupby("seniority_by_title")
    .agg(
        Job_Postings=("ID", "count"),
        Average_Salary_K=("Avg_SalaryK", "mean")
    )
    .reset_index()
)

seniority_salary = seniority_salary.sort_values(
    "Job_Postings",
    ascending=False
)

print("\n========== SENIORITY VS SALARY ==========")
print(seniority_salary)

seniority_salary.to_csv(
    "output/analysis_tables/seniority_vs_salary.csv",
    index=False
)


# ============================================================
# 18. INDUSTRY VS SALARY
# ============================================================

industry_salary = (
    df[
        (df["Industry"].notna()) &
        (df["Industry"] != "-1")
    ]
    .groupby("Industry")
    .agg(
        Job_Postings=("ID", "count"),
        Average_Salary_K=("Avg_SalaryK", "mean")
    )
    .reset_index()
)

industry_salary = industry_salary[
    industry_salary["Job_Postings"] >= 5
]

industry_salary = industry_salary.sort_values(
    "Average_Salary_K",
    ascending=False
)

industry_salary.to_csv(
    "output/analysis_tables/industry_vs_salary.csv",
    index=False
)


# ============================================================
# 19. SECTOR VS SALARY
# ============================================================

sector_salary = (
    df[
        (df["Sector"].notna()) &
        (df["Sector"] != "-1")
    ]
    .groupby("Sector")
    .agg(
        Job_Postings=("ID", "count"),
        Average_Salary_K=("Avg_SalaryK", "mean")
    )
    .reset_index()
)

sector_salary = sector_salary[
    sector_salary["Job_Postings"] >= 5
]

sector_salary = sector_salary.sort_values(
    "Job_Postings",
    ascending=False
)

sector_salary.to_csv(
    "output/analysis_tables/sector_vs_salary.csv",
    index=False
)


# ============================================================
# 20. COMPANY SIZE VS SALARY
# ============================================================

size_salary = (
    df[
        (df["Size"].notna()) &
        (df["Size"] != "-1")
    ]
    .groupby("Size")
    .agg(
        Job_Postings=("ID", "count"),
        Average_Salary_K=("Avg_SalaryK", "mean")
    )
    .reset_index()
)

size_salary = size_salary.sort_values(
    "Job_Postings",
    ascending=False
)

size_salary.to_csv(
    "output/analysis_tables/company_size_vs_salary.csv",
    index=False
)


# ============================================================
# 21. OWNERSHIP VS SALARY
# ============================================================

ownership_salary = (
    df[
        (df["Type_of_ownership"].notna()) &
        (df["Type_of_ownership"] != "-1")
    ]
    .groupby("Type_of_ownership")
    .agg(
        Job_Postings=("ID", "count"),
        Average_Salary_K=("Avg_SalaryK", "mean")
    )
    .reset_index()
)

ownership_salary = ownership_salary.sort_values(
    "Job_Postings",
    ascending=False
)

ownership_salary.to_csv(
    "output/analysis_tables/ownership_vs_salary.csv",
    index=False
)


# ============================================================
# 22. RATING VS SALARY
# ============================================================

rating_salary = (
    df[
        (df["Rating"].notna()) &
        (df["Rating"] != -1)
    ]
    .groupby("Rating")
    .agg(
        Job_Postings=("ID", "count"),
        Average_Salary_K=("Avg_SalaryK", "mean")
    )
    .reset_index()
)

rating_salary = rating_salary.sort_values(
    "Rating",
    ascending=True
)

rating_salary.to_csv(
    "output/analysis_tables/rating_vs_salary.csv",
    index=False
)


# ============================================================
# 23. REVENUE VS SALARY
# ============================================================

revenue_salary = (
    df[
        (df["Revenue"].notna()) &
        (df["Revenue"] != "-1")
    ]
    .groupby("Revenue")
    .agg(
        Job_Postings=("ID", "count"),
        Average_Salary_K=("Avg_SalaryK", "mean")
    )
    .reset_index()
)

revenue_salary = revenue_salary.sort_values(
    "Job_Postings",
    ascending=False
)

revenue_salary.to_csv(
    "output/analysis_tables/revenue_vs_salary.csv",
    index=False
)


# ============================================================
# 24. EMPLOYER PROVIDED SALARY
# ============================================================

employer_salary = (
    df.groupby("Employer_provided")
    .agg(
        Job_Postings=("ID", "count"),
        Average_Salary_K=("Avg_SalaryK", "mean")
    )
    .reset_index()
)

employer_salary.to_csv(
    "output/analysis_tables/employer_provided_salary.csv",
    index=False
)


# ============================================================
# 25. HOURLY VS NON-HOURLY
# ============================================================

hourly_salary = (
    df.groupby("Hourly")
    .agg(
        Job_Postings=("ID", "count"),
        Average_Salary_K=("Avg_SalaryK", "mean")
    )
    .reset_index()
)

hourly_salary.to_csv(
    "output/analysis_tables/hourly_vs_salary.csv",
    index=False
)


# ============================================================
# 26. COMPANY AGE GROUP ANALYSIS
# ============================================================

def age_group(age):

    if age < 10:
        return "0-9 Years"
    elif age < 20:
        return "10-19 Years"
    elif age < 30:
        return "20-29 Years"
    elif age < 50:
        return "30-49 Years"
    else:
        return "50+ Years"


age_df = df[
    (df["Age"].notna()) &
    (df["Age"] != -1)
].copy()

age_df["Company_Age_Group"] = age_df["Age"].apply(age_group)

age_analysis = (
    age_df.groupby("Company_Age_Group")
    .agg(
        Job_Postings=("ID", "count"),
        Average_Salary_K=("Avg_SalaryK", "mean")
    )
    .reset_index()
)

age_analysis.to_csv(
    "output/analysis_tables/company_age_analysis.csv",
    index=False
)


# ============================================================
# 27. FINAL SUMMARY
# ============================================================

print("\n============================================")
print("       PRDA-04 PYTHON ANALYSIS COMPLETE")
print("============================================")

print("\nTotal Jobs:", len(df))
print("Total Features:", len(df.columns))

print("\nTop Location:")
print(location_analysis.iloc[0]["Job_Location"])

print("\nTop Industry:")
print(top_5_industries.iloc[0]["Industry"])

print("\nTop Company:")
print(top_companies.iloc[0]["Company_Name"])

print("\nTop Job Title:")
print(top_job_titles.iloc[0]["Job_Title"])

print("\nMost Demanded Skill:")
print(skill_analysis.iloc[0]["Skill"])

print("\nAll analysis tables saved in:")
print("output/analysis_tables/")

print("\nAll charts saved in:")
print("output/charts/")

print("\n============================================")
print("              PROJECT READY")
print("============================================")