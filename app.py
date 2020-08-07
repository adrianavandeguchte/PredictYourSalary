# import dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, render_template, redirect, jsonify

# database setup
# Configure settings for RDS
rds_connection_string = "root:RamNivas08@predictyoursalary.cruwlreaual5.us-east-2.rds.amazonaws.com:5432/predictyoursalary"
engine = create_engine(f'postgresql://{rds_connection_string}')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
salary_data1 = Base.classes.salary_data1
salary_data2 = Base.classes.salary_data2

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

# tools of the trade page to render tools.html
@app.route("/tools_data/<tool_category>")
def tools_data(tool_category):
    session = Session(engine)

    # query to obtain totals of each type within chosen tool category
    if (tool_category == "course_platform"):
        tool_data = session.query(func.sum(salary_data2.udacity), func.sum(salary_data2.coursera), func.sum(salary_data2.edx),\
            func.sum(salary_data2.datacamp), func.sum(salary_data2.dataquest), func.sum(salary_data2.kaggle),\
            func.sum(salary_data2.fastai), func.sum(salary_data2.udemy), func.sum(salary_data2.linkedin),\
            func.sum(salary_data2.university), func.sum(salary_data2.plat_none), func.sum(salary_data2.plat_other)).all()
    elif (tool_category == "text_editor"):
        tool_data = session.query(func.sum(salary_data2.jupyter),\
            func.sum(salary_data2.rstudio), func.sum(salary_data2.pycharm), func.sum(salary_data2.atom),\
            func.sum(salary_data2.matlab), func.sum(salary_data2.vsc), func.sum(salary_data2.spyder),\
            func.sum(salary_data2.vim_emacs), func.sum(salary_data2.notepad_plusplus), func.sum(salary_data2.sublime),\
            func.sum(salary_data2.env_none), func.sum(salary_data2.env_other)).all()
    elif (tool_category == "language"):
        tool_data = session.query(func.sum(salary_data2.python),\
            func.sum(salary_data2.r), func.sum(salary_data2.sql), func.sum(salary_data2.c), func.sum(salary_data2.c_plusplus),\
            func.sum(salary_data2.java), func.sum(salary_data2.javascript), func.sum(salary_data2.typescript),\
            func.sum(salary_data2.bash), func.sum(salary_data2.lan_matlab), func.sum(salary_data2.lan_none),\
            func.sum(salary_data2.lan_other)).all()
    elif (tool_category == "library"):
        tool_data = session.query(func.sum(salary_data2.ggplot),\
            func.sum(salary_data2.matplotlib), func.sum(salary_data2.altair), func.sum(salary_data2.shiny),\
            func.sum(salary_data2.d3), func.sum(salary_data2.plotly), func.sum(salary_data2.bokeh),\
            func.sum(salary_data2.seaborn), func.sum(salary_data2.geoplotlib), func.sum(salary_data2.leaflet),\
            func.sum(salary_data2.vis_none), func.sum(salary_data2.vis_other)).all()
    elif (tool_category == "ml_model"):
        tool_data = session.query(func.sum(salary_data2.regression),\
            func.sum(salary_data2.tree_forest), func.sum(salary_data2.gradient_boost), func.sum(salary_data2.bayesian),\
            func.sum(salary_data2.evolutionary), func.sum(salary_data2.dnn), func.sum(salary_data2.cnn),\
            func.sum(salary_data2.gan), func.sum(salary_data2.rnn), func.sum(salary_data2.bert), func.sum(salary_data2.mach_none),\
            func.sum(salary_data2.mach_other)).all()
    elif (tool_category == "database"):
        tool_data = session.query(func.sum(salary_data2.mysql),\
            func.sum(salary_data2.postgres), func.sum(salary_data2.sql_lite), func.sum(salary_data2.sqlserver),\
            func.sum(salary_data2.oracle), func.sum(salary_data2.micro_acess), func.sum(salary_data2.aws_data),\
            func.sum(salary_data2.aws_dynamo), func.sum(salary_data2.azure_sql), func.sum(salary_data2.google_sql),\
            func.sum(salary_data2.database_none), func.sum(salary_data2.database_other)).all()
    
    session.close()

    # adds data into a dictionary to be jsonified
    data_list = []
    if (tool_category == "course_platform"):
        for udacity, coursera, edx, datacamp, dataquest, kaggle, fastai, udemy, linkedin, university, plat_none, plat_other in tool_data:
            data_list_dict = {}
            data_list_dict["udacity"] = udacity
            data_list_dict["coursera"] = coursera
            data_list_dict["edx"] = edx
            data_list_dict["datacamp"] = datacamp
            data_list_dict["dataquest"] = dataquest
            data_list_dict["kaggle"] = kaggle
            data_list_dict["fastai"] = fastai
            data_list_dict["udemy"] = udemy
            data_list_dict["linkedin"] = linkedin
            data_list_dict["university"] = university
            data_list_dict["none"] = plat_none
            data_list_dict["other"] = plat_other
            data_list.append(data_list_dict)
    elif (tool_category == "text_editor"):
        for jupyter, rstudio, pycharm, atom, matlab, vsc, spyder, vim_emacs, notepad, sublime, env_none, env_other in tool_data:
            data_list_dict = {}
            data_list_dict["jupyter"] = jupyter
            data_list_dict["rstudio"] = rstudio
            data_list_dict["pycharm"] = pycharm
            data_list_dict["atom"] = atom
            data_list_dict["matlab"] = matlab
            data_list_dict["vsc"] = vsc
            data_list_dict["spyder"] = spyder
            data_list_dict["vim_emacs"] = vim_emacs
            data_list_dict["notepad++"] = notepad
            data_list_dict["sublime"] = sublime
            data_list_dict["none"] = env_none
            data_list_dict["other"] = env_other
            data_list.append(data_list_dict)
    elif (tool_category == "language"):
        for python, r, sql, c, c_plusplus, java, javascript, typescript, bash, lan_matlab, lan_none, lan_other in tool_data:
            data_list_dict = {}
            data_list_dict["python"] = python
            data_list_dict["r"] = r
            data_list_dict["sql"] = sql
            data_list_dict["c"] = c
            data_list_dict["c++"] = c_plusplus
            data_list_dict["java"] = java
            data_list_dict["javascript"] = javascript
            data_list_dict["typescript"] = typescript
            data_list_dict["bash"] = bash
            data_list_dict["matlab_language"] = lan_matlab
            data_list_dict["none"] = lan_none
            data_list_dict["other"] = lan_other
            data_list.append(data_list_dict)
    elif (tool_category == "library"):
        for ggplot, matplotlib, altair, shiny, d3, plotly, bokeh, seaborn, geoplotlib, leaflet, vis_none, vis_other in tool_data:
            data_list_dict = {}
            data_list_dict["ggplot"] = ggplot
            data_list_dict["matplotlib"] = matplotlib
            data_list_dict["altair"] = altair
            data_list_dict["shiny"] = shiny
            data_list_dict["d3"] = d3
            data_list_dict["plotly"] = plotly
            data_list_dict["bokeh"] = bokeh
            data_list_dict["seaborn"] = seaborn
            data_list_dict["geoplotlib"] = geoplotlib
            data_list_dict["leaflet"] = leaflet
            data_list_dict["none"] = vis_none
            data_list_dict["other"] = vis_other
            data_list.append(data_list_dict)
    elif (tool_category == "ml_model"):
        for regression, tree_forest, gradient_boost, bayesian, evolutionary, dnn, cnn, gan, rnn, bert, mach_none, mach_other in tool_data:
            data_list_dict = {}
            data_list_dict["regression"] = regression
            data_list_dict["tree_forest"] = tree_forest
            data_list_dict["gradient_boost"] = gradient_boost
            data_list_dict["bayesian"] = bayesian
            data_list_dict["evolutionary"] = evolutionary
            data_list_dict["dnn"] = dnn
            data_list_dict["cnn"] = cnn
            data_list_dict["gan"] = gan
            data_list_dict["rnn"] = rnn
            data_list_dict["bert"] = bert
            data_list_dict["none"] = mach_none
            data_list_dict["other"] = mach_other
            data_list.append(data_list_dict)
    elif (tool_category == "database"):
        for mysql, postgres, sql_lite, sqlserver, oracle, micro_aces, aws_data, aws_dynamo, azure_sql, google_sql, database_none, database_other in tool_data:
            data_list_dict = {}
            data_list_dict["mysql"] = mysql
            data_list_dict["postgres"] = postgres
            data_list_dict["sql_lite"] = sql_lite
            data_list_dict["sqlserver"] = sqlserver
            data_list_dict["oracle"] = oracle
            data_list_dict["micro_aces"] = micro_aces
            data_list_dict["micro_aces"] = micro_aces
            data_list_dict["aws_data"] = aws_data
            data_list_dict["aws_dynamo"] = aws_dynamo
            data_list_dict["azure_sql"] = azure_sql
            data_list_dict["google_sql"] = google_sql
            data_list_dict["none"] = database_none
            data_list_dict["other"] = database_other
            data_list.append(data_list_dict)

    return jsonify(data_list)


# salary_visuals page to render salary_visuals.html
@app.route("/salary_visuals")
def salary_visuals():
    return render_template("salary_visuals.html")


@app.route("/salary_visuals_data/<filter_choice>")
def salary_visuals_data(filter_choice):
    session = Session(engine)

    data_list = []

    # query to obtain salaries of each chosen filter
    if (filter_choice == "job_title_dataset2"):
        visuals_data = session.query(salary_data2.title, func.count(salary_data2.title), func.avg(salary_data2.salary)).\
            group_by(salary_data2.title).all()    
        session.close()
        
        # adds data into a dictionary to be jsonified
        for title, count, salary in visuals_data:
            data_list_dict = {}
            data_list_dict["job_title"] = title
            data_list_dict["count"] = count
            data_list_dict["salary"] = salary
            data_list.append(data_list_dict)

    elif (filter_choice == "gender"):
        visuals_data = session.query(salary_data2.gender, func.count(salary_data2.gender), func.avg(salary_data2.salary)).\
            group_by(salary_data2.gender).all()
        session.close()

        for gender, count, salary in visuals_data:
            data_list_dict = {}
            data_list_dict["gender"] = gender
            data_list_dict["count"] = count
            data_list_dict["salary"] = salary
            data_list.append(data_list_dict)
    
    elif (filter_choice == "education_dataset2"):
        visuals_data = session.query(salary_data2.education, func.count(salary_data2.education), func.avg(salary_data2.salary)).\
            group_by(salary_data2.education).all()
        session.close()

        for education, count, salary in visuals_data:
            data_list_dict = {}
            data_list_dict["education"] = education
            data_list_dict["count"] = count
            data_list_dict["salary"] = salary
            data_list.append(data_list_dict)

    elif (filter_choice == "country_dataset2"):
        visuals_data = session.query(salary_data2.country, func.count(salary_data2.country), func.avg(salary_data2.salary)).\
            group_by(salary_data2.country).all()
        session.close()

        for country, count, salary in visuals_data:
            data_list_dict = {}
            data_list_dict["country"] = country
            data_list_dict["count"] = count
            data_list_dict["salary"] = salary
            data_list.append(data_list_dict)

    elif (filter_choice == "job_title_dataset1"):
        visuals_data = session.query(salary_data1.jobtitle, func.count(salary_data1.jobtitle), func.avg(salary_data1.salaryusd)).\
            group_by(salary_data1.jobtitle).all()
        session.close()

        for title, count, salary in visuals_data:
            data_list_dict = {}
            data_list_dict["job_title"] = title
            data_list_dict["count"] = count
            data_list_dict["salary"] = salary
            data_list.append(data_list_dict)

    elif (filter_choice == "education_dataset1"):
        visuals_data = session.query(salary_data1.education, func.count(salary_data1.education), func.avg(salary_data1.salaryusd)).\
            group_by(salary_data1.education).all()
        session.close()

        for education, count, salary in visuals_data:
            data_list_dict = {}
            data_list_dict["education"] = education
            data_list_dict["count"] = count
            data_list_dict["salary"] = salary
            data_list.append(data_list_dict)

    elif (filter_choice == "comp_education"):
        visuals_data = session.query(salary_data1.educationiscomputerrelated, func.count(salary_data1.educationiscomputerrelated), func.avg(salary_data1.salaryusd)).\
            group_by(salary_data1.educationiscomputerrelated).all()
        session.close()

        for comp_education, count, salary in visuals_data:
            data_list_dict = {}
            data_list_dict["is_education_comp_related"] = comp_education
            data_list_dict["count"] = count
            data_list_dict["salary"] = salary
            data_list.append(data_list_dict)

    elif (filter_choice == "certifications"):
        visuals_data = session.query(salary_data1.certifications, func.count(salary_data1.certifications), func.avg(salary_data1.salaryusd)).\
            group_by(salary_data1.certifications).all()
        session.close()

        for certifications, count, salary in visuals_data:
            data_list_dict = {}
            data_list_dict["certifications"] = certifications
            data_list_dict["count"] = count
            data_list_dict["salary"] = salary
            data_list.append(data_list_dict)

    elif (filter_choice == "country_dataset1"):
        visuals_data = session.query(salary_data1.country, func.count(salary_data1.country), func.avg(salary_data1.salaryusd)).\
            group_by(salary_data1.country).all()
        session.close()

        for country, count, salary in visuals_data:
            data_list_dict = {}
            data_list_dict["country"] = country
            data_list_dict["count"] = count
            data_list_dict["salary"] = salary
            data_list.append(data_list_dict)
    
    return jsonify(data_list)


# tools of the trade page to render tools.html
@app.route("/salary_visuals_data/<filter_choice>/<country>")
def salary_visuals_data_by_country(filter_choice, country):
    session = Session(engine)

    data_list = []
    # query to obtain salaries of each chosen filter
    if (filter_choice == "job_title_dataset2"):
        visuals_data = session.query(salary_data2.title, func.count(salary_data2.title), func.avg(salary_data2.salary)).\
            filter(salary_data2.country == country).\
            group_by(salary_data2.title).all()    
        session.close()
        
        # adds data into a dictionary to be jsonified
        for title, count, salary in visuals_data:
            data_list_dict = {}
            data_list_dict["job_title"] = title
            data_list_dict["count"] = count
            data_list_dict["salary"] = salary
            data_list.append(data_list_dict)

    elif (filter_choice == "gender"):
        visuals_data = session.query(salary_data2.gender, func.count(salary_data2.gender), func.avg(salary_data2.salary)).\
            filter(salary_data2.country == country).\
            group_by(salary_data2.gender).all()
        session.close()

        for gender, count, salary in visuals_data:
            data_list_dict = {}
            data_list_dict["gender"] = gender
            data_list_dict["count"] = count
            data_list_dict["salary"] = salary
            data_list.append(data_list_dict)
    
    elif (filter_choice == "education_dataset2"):
        visuals_data = session.query(salary_data2.education, func.count(salary_data2.education), func.avg(salary_data2.salary)).\
            filter(salary_data2.country == country).\
            group_by(salary_data2.education).all()
        session.close()

        for education, count, salary in visuals_data:
            data_list_dict = {}
            data_list_dict["education"] = education
            data_list_dict["count"] = count
            data_list_dict["salary"] = salary
            data_list.append(data_list_dict)

    elif (filter_choice == "job_title_dataset1"):
        visuals_data = session.query(salary_data1.jobtitle, func.count(salary_data1.jobtitle), func.avg(salary_data1.salaryusd)).\
            filter(salary_data1.country == country).\
            group_by(salary_data1.jobtitle).all()
        session.close()

        for title, count, salary in visuals_data:
            data_list_dict = {}
            data_list_dict["job_title"] = title
            data_list_dict["count"] = count
            data_list_dict["salary"] = salary
            data_list.append(data_list_dict)

    elif (filter_choice == "education_dataset1"):
        visuals_data = session.query(salary_data1.education, func.count(salary_data1.education), func.avg(salary_data1.salaryusd)).\
            filter(salary_data1.country == country).\
            group_by(salary_data1.education).all()
        session.close()

        for education, count, salary in visuals_data:
            data_list_dict = {}
            data_list_dict["education"] = education
            data_list_dict["count"] = count
            data_list_dict["salary"] = salary
            data_list.append(data_list_dict)

    elif (filter_choice == "comp_education"):
        visuals_data = session.query(salary_data1.educationiscomputerrelated, func.count(salary_data1.educationiscomputerrelated), func.avg(salary_data1.salaryusd)).\
            filter(salary_data1.country == country).\
            group_by(salary_data1.educationiscomputerrelated).all()
        session.close()

        for comp_education, count, salary in visuals_data:
            data_list_dict = {}
            data_list_dict["is_education_comp_related"] = comp_education
            data_list_dict["count"] = count
            data_list_dict["salary"] = salary
            data_list.append(data_list_dict)

    elif (filter_choice == "certifications"):
        visuals_data = session.query(salary_data1.certifications, func.count(salary_data1.certifications), func.avg(salary_data1.salaryusd)).\
            filter(salary_data1.country == country).\
            group_by(salary_data1.certifications).all()
        session.close()

        for certifications, count, salary in visuals_data:
            data_list_dict = {}
            data_list_dict["certifications"] = certifications
            data_list_dict["count"] = count
            data_list_dict["salary"] = salary
            data_list.append(data_list_dict)
    
    return jsonify(data_list)


# api route to obtain the name data from salary_data1
@app.route("/salary_data1")
def all_salary_data1():
    session = Session(engine)

    # query to obtain state name and rank
    all_data = session.query(salary_data1.salaryusd, salary_data1.primarydatabase, salary_data1.yearswiththisdatabase, salary_data1.employmentstatus, salary_data1.jobtitle, salary_data1.managestaff, salary_data1.yearswiththistypeofjob, salary_data1.otherpeopleonyourteam, salary_data1.databaseservers, salary_data1.education, salary_data1.educationiscomputerrelated, salary_data1.certifications, salary_data1.hoursworkedperweek, salary_data1.telecommutedaysperweek, salary_data1.employmentsector, salary_data1.region).all()
    session.close()

    # adds data into a dictionary to be jsonified
    data_list = []
    for salary, database, years_database, status, title, manager, years_job, team, servers, education, education_comp, certs, hours, telecommute, sector, region in all_data:
        data_list_dict = {}
        data_list_dict["salary"] = salary
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


@app.route('/prediction.html')
def go_to_prediction():
	return render_template('prediction.html')


@app.route('/prediction', methods=['POST','GET'])
def predict():

    import joblib
    salary_model = joblib.load('salary_model_trained.sav')

    from sklearn.preprocessing import StandardScaler
    X_scaler = joblib.load('X_scaler.sav')

	#get question from the html form
    user_response = request.form.to_dict(flat=False)

    user_response_list = [[user_response['country'][0],
                    user_response['region'][0],
                    user_response['education'][0],
                    user_response['comp_ed'][0],
                    user_response['primary_db'][0],
                    user_response['years_db'][0],
                    user_response['years_job'][0],
                    user_response['employ_sector'][0],
                    user_response['other_people'][0],
                    user_response['employ_status'][0],
                    user_response['telecommute'][0],
                    user_response['manager'][0]]]

    user_response_transformed = X_scaler.transform(user_response_list[0])

    prediction = salary_model.predict(user_response_transformed)

    prediction_string = 'Salary Prediction: $' + prediction

    #show results on the HTML page
    return render_template('prediction.html', salary_prediction= prediction_string)


if __name__ == "__main__":
    app.run(debug=True)
