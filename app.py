# import dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, render_template, redirect, jsonify

#database setup
# Configure settings for RDS
from config import sandy_RDS_username
from config import sandy_RDS_password
from config import sandy_RDS_endpoint
from sqlalchemy import create_engine
rds_connection_string = f'{sandy_RDS_username}:{sandy_RDS_password}@{sandy_RDS_endpoint}:5432/predict_salary_db'
engine = create_engine(f'postgresql://{rds_connection_string}')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
salary_data1 = Base.classes.salary_data1
# salary_data2 = Base.classes.salary_data2

# Flask Setup
app = Flask(__name__)

# Flask Routes

# home page to render index.html
@app.route("/")
def home():
    return render_template("index.html")

# about page to render about.html
@app.route("/about")
def about():
    return render_template("about.html")

# methodology page to render methodology.html
@app.route("/methodology")
def methodology():
    return render_template("methodology.html")

# tools of the trade page to render tools.html
@app.route("/tools")
def tools():
    return render_template("tools.html")


# api route to obtain the name and overall ranking of each state
@app.route("/salary_data1")
def all_salary_data1():
    session = Session(engine)

    # query to obtain state name and rank
    all_data = session.query(salary_data1.salaryusd, salary_data1.country, salary_data1.primarydatabase, salary_data1.yearswiththisdatabase, salary_data1.employmentstatus, salary_data1.jobtitle, salary_data1.managestaff, salary_data1.yearswiththistypeofjob, salary_data1.otherpeopleonyourteam, salary_data1. databaseservers, salary_data1.education, salary_data1.educationiscomputerrelated, salary_data1.certifications, salary_data1.hoursworkedperweek, salary_data1.telecommutedaysperweek, salary_data1.employmentsector, salary_data1.region).all()
    session.close()

    # adds data into a dictionary to be jsonified
    data_list = []
    for salary, country, database, years_database, status, title, manager, years_job, team, servers, education, education_comp, certs, hours, telecommute, sector, region in all_data:
        data_list_dict = {}
        data_list_dict["salary"] = salary
        data_list_dict["country"] = country
        data_list_dict["primary_database"] = database
        data_list_dict["years_with_this_database"] = years_database
        data_list_dict["employment_status"] = status
        data_list_dict["job_title"] = title
        data_list_dict["manager"] = manager
        data_list_dict["years_with_this_type_of_job"] = years_job
        data_list_dict["other_people_on_your_team"] = team
        data_list_dict["database_servers"] = servers
        data_list_dict["education"] = education
        data_list_dict["education_is_computer_related"] = education_comp
        data_list_dict["certifications"] = certs
        data_list_dict["years_with_this_type_of_job"] = hours
        data_list_dict["telecommute_days_per_week"] = telecommute
        data_list_dict["employment_sector"] = sector
        data_list_dict["region"] = region
        data_list.append(data_list_dict)
    
    return jsonify(data_list)





# import re
# import time
# import nltk
# import pickle
# from ast import literal_eval as le
# # load category model
# filename = 'Question_Classification_LinearSVM_model.pkl'
# tuned_category_model = pickle.load(open(filename, 'rb'))
# # load topic model
# topic_filename = 'Question_Classification_LinearSVM_topic_model.pkl'
# tuned_topic_model = pickle.load(open(filename, 'rb'))
# # load vectorizer
# vector_filename = 'Question_Classification_vectorizer.pkl'
# vectorizer = pickle.load(open(vector_filename, 'rb'))
# # load categories and class names
# categories, topics = {},{}
# with open('category_labels.txt','r') as f:
#     categories = le(f.read())
# with open('topic_labels.txt','r') as f:
#     topics = le(f.read())

# @app.route('/prediction.html')
# def go_to_prediction():
# 	return render_template('prediction.html')

# @app.route('/prediction', methods=['POST','GET'])
# def predict(category_model = tuned_category_model,
#             topic_model = tuned_topic_model,
#             vectorizer = vectorizer,
#             categories = categories,
#             topics = topics):

# 	#get question from the html form
# 	text = request.form['question']

# 	#convert text to lowercase
# 	text = text.lower()

# 	#form feature vectors
# 	features = vectorizer.transform([text])

# 	#predict result category
# 	print('Using best category model : {}'.format(category_model))
# 	pred = category_model.predict(features)

# 	category = lookup(categories, pred[0])
# 	print('Category : {}'.format(category))

# 	#predict result topic
# 	print('\n\nUsing best topic model : {}'.format(topic_model))
# 	pred = topic_model.predict(features)

# 	topic = lookup(topics, pred[0])
# 	print('Topic : {}'.format(topic))
  
#   #show results on the HTML page
# 	return render_template('prediction.html', prediction_string='Predictions :', category='Category : {}'.format(category), topic='Topic : {}'.format(topic))

# if __name__ == '__main__':
# 	app.run()







# dynamic state page
# api route to obtain detailed information for each state, depending on which state is passed into the  url
# @app.route("/<state>")
# def dynamic(state):
#     # Create a session
#     session = Session(engine)

#     # query to obtain overall data of the state, such as amount of each type of attraction
#     travel_num = session.query(combined_table.state, combined_table.abbr).\
#         filter(combined_table.state == state).all()
#     session.close()

#     # query to obtain all the amusement parks in the state
#     amusement_query = session.query(amusement_table.amusementpark_name).\
#         filter(amusement_table.state == state).all()
#     session.close()

#     # query to obtain all the aquariums in the state
#     aquarium_query = session.query(aquarium_table.aquarium_name).\
#         filter(aquarium_table.state == state).all()
#     session.close()

#      # add all data into a list to be jsonified
#     start_list = []
#     # start_list_dict = {}
#     for state, abbr in travel_num:
#         start_list_dict = {}
#         start_list_dict["state"] = state
#         start_list_dict["abbreviation"] = abbr
#         start_list.append(start_list_dict)
    
#     amusement_list = []
#     aquarium_list = []

#     attraction_dict = {}

#     # for each type of attraction, if the state contains any of that type, add it to a list and then a dictionary,
#     if amusement_query:
#         for amusement in amusement_query:
#             for item in amusement:
#                 amusement_list.append(item)
#             attraction_dict["amusement_park_list"] = amusement_list
    
#     if beach_query:
#         for beach in beach_query:
#             for item in beach:
#                 beach_list.append(item)
#             attraction_dict["beach_list"] = beach_list

#     # add the dictionary to the same list that was previously used
#     start_list.append(attraction_dict)

#     # return the jsonified verision of the list when 
#     return jsonify(start_list)

if __name__ == "__main__":
    app.run(debug=True)
