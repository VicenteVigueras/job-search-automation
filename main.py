# Import dependencies
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Job title and location for search
title = "Software Developer"  # Job title
location = "Wilmington, Delaware"  # Job location (adjusted for Wilmington, Delaware)
radius = 50  # 50 miles radius for job search

# Initialize an empty list to store job information
job_list = []

# Number of pages to scrape (adjust based on your needs)
num_pages = 5  # Modify this to the number of pages you want to scrape

# Loop through pages
for page in range(num_pages):
    start = page * 25  # LinkedIn typically shows 25 results per page, adjust if needed

    # Construct the URL for LinkedIn job search with the 50-mile radius
    list_url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={title}&location={location}&start={start}&radius={radius}"

    # Send a GET request to the URL and store the response
    response = requests.get(list_url)

    # Parse the response to find job listings
    list_data = response.text
    list_soup = BeautifulSoup(list_data, "html.parser")
    page_jobs = list_soup.find_all("li")

    # Iterate through job postings to extract job IDs and URLs
    for job in page_jobs:
        base_card_div = job.find("div", {"class": "base-card"})
        if base_card_div:
            job_id = base_card_div.get("data-entity-urn").split(":")[3]
            job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
            print(f"Job ID: {job_id}, Job URL: {job_url}")

            # Send a GET request to the job URL and parse the response
            job_response = requests.get(job_url)
            job_soup = BeautifulSoup(job_response.text, "html.parser")

            # Create a dictionary to store job details
            job_post = {"job_url": job_url}  # Add URL to the job data

            # Try to extract and store the job title
            try:
                job_post["job_title"] = job_soup.find("h2", {"class": "top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title"}).text.strip()
            except:
                job_post["job_title"] = None

            # Try to extract and store the company name
            try:
                job_post["company_name"] = job_soup.find("a", {"class": "topcard__org-name-link topcard__flavor--black-link"}).text.strip()
            except:
                job_post["company_name"] = None

            # Try to extract and store the time posted
            try:
                job_post["time_posted"] = job_soup.find("span", {"class": "posted-time-ago__text topcard__flavor--metadata"}).text.strip()
            except:
                job_post["time_posted"] = None

            # Try to extract and store the number of applicants
            try:
                job_post["num_applicants"] = job_soup.find("span", {"class": "num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet"}).text.strip()
            except:
                job_post["num_applicants"] = None

            # Append the job details to the job_list
            job_list.append(job_post)

# Convert the job list to a DataFrame and print it
df = pd.DataFrame(job_list)

# Save the DataFrame to a CSV file
df.to_csv('linkedin_jobs_wilmington_50_miles.csv', index=False)

# Print the saved data
print("Job listings have been saved to 'linkedin_jobs_wilmington_50_miles.csv'")
