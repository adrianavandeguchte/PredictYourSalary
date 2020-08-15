# Predict Your Salary in the Data Professional World 

## Summary: 
As most of the Bootcamp graduates will be looking for a new job, our group developed an app to explore the data professional world job market. Through our app, you can see a salary prediction based on your region, years of experience and primary tools used in a specific job title. We also explore the different tools used in the field and the expectations that each of these data jobs possess. By using our page, you can estimate how much you can expect to earn with the current skills you have as well as compare your expertise to those in the field. For a more detailed development description, please visit our Development link on the webpage. 

### Group: 
* [Sandra Froonjian](https://www.linkedin.com/in/sandrafroonjian/) 
* [Katarzyna (Kasia) Kalemba](https://www.linkedin.com/in/katarzynakalemba/)
* [Solito Reyes III](https://www.linkedin.com/in/solitoreyesiii/) 
* [Adriana van de Guchte](https://www.linkedin.com/in/adriana-van-de-guchte-6096791a3/) 
* [Shrilekha Vijayakanthan](https://www.linkedin.com/in/shrilekha-vijayakanthan-1986601b/) 

## Motivation: 
At the end of the Data Science Bootcamp, our group wanted to create a tool to see how our newly acquired skills compare to the current industry standard. By using industry data, we creating a machine learning model that would predict how much money we can expect to make based on the selected factors. Looking at the job titles, skills, years of experience, programming languages, databases and many other factors valued in the data professional world, we explored the potential salaries within this field and the expectations of knowing certain skills. We created visuals that further explored the differences in job titles, gender pay gaps, age differences, looking at data from all over the world. 

## Usage 
### Local: 
* Make sure all the requirements from requirements.txt are up to date:
* Run app.py 
* Access at http://localhost:8000/

### Remote Access
* [Heroku](https://predictyoursalaryy.herokuapp.com/)

## Data 
### Dataset 1: Kaggle Survey: 
This data set was collected from 171 countries as a survey for a Kaggle Competition. The survey responders were data professionals who are currently working in the field. We used their responses for the visuals for salary, gender, country, age and multiple data tools that they use in their current jobs. 
[Kaggle](https://www.kaggle.com/c/kaggle-survey-2019)

### Dataset 2: Brent Ozar Data
This dataset was used to develop our machine learning model for the salary prediction. We used factors such as location, title, primary database use, management level, education and year experience to predict a salary for a data professional. 
[Brent Ozar](https://www.brentozar.com/archive/2019/01/the-2019-data-professional-salary-survey-results/)


## Overview of Development Steps 
### Data Preparation
#### Cleaning Dataset 1 Kaggle Survey: 
* The original CSV file was loaded in Jupyter Notebook and consisted of 246 columns and 19718 rows and was narrowed down to 109 columns and 19718 rows. 
* A clean CSV was exported for the remaining work. 


#### Cleaning Dataset 2 Brent Ozar Data: 
* The original CSV file was loaded in Jupyter Notebook and consisted of 6893 rows and 29 columns and was narrowed down to 6893 rows and 17 columns. 
* A clean CSV was exported for the remaining work. 

### Visualizations 
#### Tableau 
* The cleaned CSV file 1 was loaded into Tableau Desktop. 
* The following visualizations were made based on factors affecting salary: gender, age, location, education level, certificates and computer science background were all analyzed for how they played a role in the salary amount. 
* We also compare what we learned in the bootcamp compared to the expectations of the field. 
* The final dashboard was published in Tableau Public and finally embedded into our html page.

#### D3 
* Word cloud of the recommended first language to learn was built using a d3 version 3 base code and expanded upon to filter out values and repopulate only on changing inputs. Bubble chart of tool and language use in industry was built using d3 version 5 and d3.force was used to build movement animation.

### Machine Learning 
* Our Scikit-Learn Model machine learning model involved using a RandomForestClassifier and feature importance to narrow down the features for our model. We selected 10 features for our model, which are, in order: country, primary database, years with this database, region, manage staff, education is computer related, years with this type of job, telecommute days per week, employment sector, and job title. Because most of these features are categorical, and the model needs them to be numerical, pd.get_dummies was then used to convert categories to binary.


### Natural Language Processing 
* To see if we have the skills employers are looking for in the data science profession, we decided to look from the employer vantage point by analyzing the data science jobs available on indeed.com. In this approach, we scraped job descriptions (Beautiful Soup) for all data science jobs available on indeed.com. We processed those job descriptions through a TSNE Visualizer in order to identify evident clusters within the dataset and ran a TF-IDF Vectorizer to see the most common words used in each cluster.

### Flask App 
* /tools_data/ route focuses on the popularities of different technologies of the data world
* /tools_data/ does the same as the route above, except there is an added filter to it that allows the user to add a job title to the URL
* /recommendations_data provides a count on the most recommended technologies to start with as a data professional.
* /recommendations_data/ does the same as the route above, except there is an added filter to it that allows the user to add a job title to the URL
* /education_data provides a breakdown of the count of each education level of each job title and also provides the average salary of each job title
* /country_region_data provides a list of all the unique country names of the dataset and its corresponding region
* /predictions is the route where the user’s response from the form is sent to. Their response is then processed to fit the model, and a prediction is returned. That response is sent back to that page to be used with Jinja.
* The rest of the routes are just simple routes that render html pages.
 
### Webpage 
* The HTML page was built with Javascript, CSS and Bootstrap features. 
* Our story-telling focuses on the tools of the trade and how these relate to expected salaries in the field. 

### Tools Used in this Project 
* Python: pandas, numpy, Flask, SKlearn 
* Javascript: interactions and D3 visualizations 
* Webpage Design: HTML, CSS, Bootstrap 
* Tableau 








