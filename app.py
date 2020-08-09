# import dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, render_template, redirect, jsonify, request
import pandas as pd

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

@app.route("/demographics")
def demographics():
    return render_template("demog.html")

@app.route("/audit")
def audit():
    return render_template("audit.html")

# tools of the trade page to render tools.html
@app.route("/tools")
def tools():
    return render_template("tools.html")

# tools of the trade page to render tools.html
@app.route("/tools_data")
def tools_data():
    session = Session(engine)

    # query to obtain totals of each type within tool category
    course_platform_data = session.query(func.sum(salary_data2.udacity), func.sum(salary_data2.coursera), func.sum(salary_data2.edx),\
            func.sum(salary_data2.datacamp), func.sum(salary_data2.dataquest), func.sum(salary_data2.kaggle),\
            func.sum(salary_data2.fastai), func.sum(salary_data2.udemy), func.sum(salary_data2.linkedin),\
            func.sum(salary_data2.university), func.sum(salary_data2.plat_none), func.sum(salary_data2.plat_other)).all()
    text_editor_data = session.query(func.sum(salary_data2.jupyter),\
            func.sum(salary_data2.rstudio), func.sum(salary_data2.pycharm), func.sum(salary_data2.atom),\
            func.sum(salary_data2.matlab), func.sum(salary_data2.vsc), func.sum(salary_data2.spyder),\
            func.sum(salary_data2.vim_emacs), func.sum(salary_data2.notepad_plusplus), func.sum(salary_data2.sublime),\
            func.sum(salary_data2.env_none), func.sum(salary_data2.env_other)).all()
    language_data = session.query(func.sum(salary_data2.python),\
            func.sum(salary_data2.r), func.sum(salary_data2.sql), func.sum(salary_data2.c), func.sum(salary_data2.c_plusplus),\
            func.sum(salary_data2.java), func.sum(salary_data2.javascript), func.sum(salary_data2.typescript),\
            func.sum(salary_data2.bash), func.sum(salary_data2.lan_matlab), func.sum(salary_data2.lan_none),\
            func.sum(salary_data2.lan_other)).all()
    library_data = session.query(func.sum(salary_data2.ggplot),\
            func.sum(salary_data2.matplotlib), func.sum(salary_data2.altair), func.sum(salary_data2.shiny),\
            func.sum(salary_data2.d3), func.sum(salary_data2.plotly), func.sum(salary_data2.bokeh),\
            func.sum(salary_data2.seaborn), func.sum(salary_data2.geoplotlib), func.sum(salary_data2.leaflet),\
            func.sum(salary_data2.vis_none), func.sum(salary_data2.vis_other)).all()
    ml_model_data = session.query(func.sum(salary_data2.regression),\
            func.sum(salary_data2.tree_forest), func.sum(salary_data2.gradient_boost), func.sum(salary_data2.bayesian),\
            func.sum(salary_data2.evolutionary), func.sum(salary_data2.dnn), func.sum(salary_data2.cnn),\
            func.sum(salary_data2.gan), func.sum(salary_data2.rnn), func.sum(salary_data2.bert), func.sum(salary_data2.mach_none),\
            func.sum(salary_data2.mach_other)).all()
    database_data = session.query(func.sum(salary_data2.mysql),\
            func.sum(salary_data2.postgres), func.sum(salary_data2.sql_lite), func.sum(salary_data2.sqlserver),\
            func.sum(salary_data2.oracle), func.sum(salary_data2.micro_acess), func.sum(salary_data2.aws_data),\
            func.sum(salary_data2.aws_dynamo), func.sum(salary_data2.azure_sql), func.sum(salary_data2.google_sql),\
            func.sum(salary_data2.database_none), func.sum(salary_data2.database_other)).all()
    
    session.close()

    # adds data into a dictionaries to be jsonified
    data_list = []
    for udacity, coursera, edx, datacamp, dataquest, kaggle, fastai, udemy, linkedin, university, plat_none, plat_other in course_platform_data:
        course_platform_dict = {}
        course_platform_dict["udacity"] = udacity
        course_platform_dict["coursera"] = coursera
        course_platform_dict["edx"] = edx
        course_platform_dict["datacamp"] = datacamp
        course_platform_dict["dataquest"] = dataquest
        course_platform_dict["kaggle"] = kaggle
        course_platform_dict["fastai"] = fastai
        course_platform_dict["udemy"] = udemy
        course_platform_dict["linkedin"] = linkedin
        course_platform_dict["university"] = university
        course_platform_dict["none"] = plat_none
        course_platform_dict["other"] = plat_other
        course_platform_dict_with_name = {"course_platforms":course_platform_dict}
        data_list.append(course_platform_dict_with_name)
    for jupyter, rstudio, pycharm, atom, matlab, vsc, spyder, vim_emacs, notepad, sublime, env_none, env_other in text_editor_data:
        text_editor_dict = {}
        text_editor_dict["jupyter"] = jupyter
        text_editor_dict["rstudio"] = rstudio
        text_editor_dict["pycharm"] = pycharm
        text_editor_dict["atom"] = atom
        text_editor_dict["matlab"] = matlab
        text_editor_dict["vsc"] = vsc
        text_editor_dict["spyder"] = spyder
        text_editor_dict["vim_emacs"] = vim_emacs
        text_editor_dict["notepad++"] = notepad
        text_editor_dict["sublime"] = sublime
        text_editor_dict["none"] = env_none
        text_editor_dict["other"] = env_other
        text_editor_dict_with_name = {"text_editors":text_editor_dict}
        data_list.append(text_editor_dict_with_name)
    for python, r, sql, c, c_plusplus, java, javascript, typescript, bash, lan_matlab, lan_none, lan_other in language_data:
        language_dict = {}
        language_dict["python"] = python
        language_dict["r"] = r
        language_dict["sql"] = sql
        language_dict["c"] = c
        language_dict["c++"] = c_plusplus
        language_dict["java"] = java
        language_dict["javascript"] = javascript
        language_dict["typescript"] = typescript
        language_dict["bash"] = bash
        language_dict["matlab_language"] = lan_matlab
        language_dict["none"] = lan_none
        language_dict["other"] = lan_other
        language_dict_with_name = {"languages":language_dict}
        data_list.append(language_dict_with_name)
    for ggplot, matplotlib, altair, shiny, d3, plotly, bokeh, seaborn, geoplotlib, leaflet, vis_none, vis_other in library_data:
        library_dict = {}
        library_dict["ggplot"] = ggplot
        library_dict["matplotlib"] = matplotlib
        library_dict["altair"] = altair
        library_dict["shiny"] = shiny
        library_dict["d3"] = d3
        library_dict["plotly"] = plotly
        library_dict["bokeh"] = bokeh
        library_dict["seaborn"] = seaborn
        library_dict["geoplotlib"] = geoplotlib
        library_dict["leaflet"] = leaflet
        library_dict["none"] = vis_none
        library_dict["other"] = vis_other
        library_dict_with_name = {"libraries":library_dict}
        data_list.append(library_dict_with_name)
    for regression, tree_forest, gradient_boost, bayesian, evolutionary, dnn, cnn, gan, rnn, bert, mach_none, mach_other in ml_model_data:
        ml_model_dict = {}
        ml_model_dict["regression"] = regression
        ml_model_dict["tree_forest"] = tree_forest
        ml_model_dict["gradient_boost"] = gradient_boost
        ml_model_dict["bayesian"] = bayesian
        ml_model_dict["evolutionary"] = evolutionary
        ml_model_dict["dnn"] = dnn
        ml_model_dict["cnn"] = cnn
        ml_model_dict["gan"] = gan
        ml_model_dict["rnn"] = rnn
        ml_model_dict["bert"] = bert
        ml_model_dict["none"] = mach_none
        ml_model_dict["other"] = mach_other
        ml_model_dict_with_name = {"ml_models":ml_model_dict}
        data_list.append(ml_model_dict_with_name)
    for mysql, postgres, sql_lite, sqlserver, oracle, micro_aces, aws_data, aws_dynamo, azure_sql, google_sql, database_none, database_other in database_data:
        database_dict = {}
        database_dict["mysql"] = mysql
        database_dict["postgres"] = postgres
        database_dict["sql_lite"] = sql_lite
        database_dict["sqlserver"] = sqlserver
        database_dict["oracle"] = oracle
        database_dict["micro_aces"] = micro_aces
        database_dict["aws_data"] = aws_data
        database_dict["aws_dynamo"] = aws_dynamo
        database_dict["azure_sql"] = azure_sql
        database_dict["google_sql"] = google_sql
        database_dict["none"] = database_none
        database_dict["other"] = database_other
        database_dict_with_name = {"databases":database_dict}
        data_list.append(database_dict_with_name)

    return jsonify(data_list)


@app.route("/tools_data/<jobtitle>")
def tools_data_by_title(jobtitle):
    session = Session(engine)

    # query to obtain totals of each type within tool category
    course_platform_data = session.query(func.sum(salary_data2.udacity), func.sum(salary_data2.coursera), func.sum(salary_data2.edx),\
            func.sum(salary_data2.datacamp), func.sum(salary_data2.dataquest), func.sum(salary_data2.kaggle),\
            func.sum(salary_data2.fastai), func.sum(salary_data2.udemy), func.sum(salary_data2.linkedin),\
            func.sum(salary_data2.university), func.sum(salary_data2.plat_none), func.sum(salary_data2.plat_other)).\
            filter(salary_data2.title == jobtitle).all()
    text_editor_data = session.query(func.sum(salary_data2.jupyter),\
            func.sum(salary_data2.rstudio), func.sum(salary_data2.pycharm), func.sum(salary_data2.atom),\
            func.sum(salary_data2.matlab), func.sum(salary_data2.vsc), func.sum(salary_data2.spyder),\
            func.sum(salary_data2.vim_emacs), func.sum(salary_data2.notepad_plusplus), func.sum(salary_data2.sublime),\
            func.sum(salary_data2.env_none), func.sum(salary_data2.env_other)).\
            filter(salary_data2.title == jobtitle).all()
    language_data = session.query(func.sum(salary_data2.python),\
            func.sum(salary_data2.r), func.sum(salary_data2.sql), func.sum(salary_data2.c), func.sum(salary_data2.c_plusplus),\
            func.sum(salary_data2.java), func.sum(salary_data2.javascript), func.sum(salary_data2.typescript),\
            func.sum(salary_data2.bash), func.sum(salary_data2.lan_matlab), func.sum(salary_data2.lan_none),\
            func.sum(salary_data2.lan_other)).filter(salary_data2.title == jobtitle).all()
    library_data = session.query(func.sum(salary_data2.ggplot),\
            func.sum(salary_data2.matplotlib), func.sum(salary_data2.altair), func.sum(salary_data2.shiny),\
            func.sum(salary_data2.d3), func.sum(salary_data2.plotly), func.sum(salary_data2.bokeh),\
            func.sum(salary_data2.seaborn), func.sum(salary_data2.geoplotlib), func.sum(salary_data2.leaflet),\
            func.sum(salary_data2.vis_none), func.sum(salary_data2.vis_other)).\
            filter(salary_data2.title == jobtitle).all()
    ml_model_data = session.query(func.sum(salary_data2.regression),\
            func.sum(salary_data2.tree_forest), func.sum(salary_data2.gradient_boost), func.sum(salary_data2.bayesian),\
            func.sum(salary_data2.evolutionary), func.sum(salary_data2.dnn), func.sum(salary_data2.cnn),\
            func.sum(salary_data2.gan), func.sum(salary_data2.rnn), func.sum(salary_data2.bert), func.sum(salary_data2.mach_none),\
            func.sum(salary_data2.mach_other)).filter(salary_data2.title == jobtitle).all()
    database_data = session.query(func.sum(salary_data2.mysql),\
            func.sum(salary_data2.postgres), func.sum(salary_data2.sql_lite), func.sum(salary_data2.sqlserver),\
            func.sum(salary_data2.oracle), func.sum(salary_data2.micro_acess), func.sum(salary_data2.aws_data),\
            func.sum(salary_data2.aws_dynamo), func.sum(salary_data2.azure_sql), func.sum(salary_data2.google_sql),\
            func.sum(salary_data2.database_none), func.sum(salary_data2.database_other)).\
            filter(salary_data2.title == jobtitle).all()
    
    session.close()

    # adds data into a dictionaries to be jsonified
    data_list = []
    for udacity, coursera, edx, datacamp, dataquest, kaggle, fastai, udemy, linkedin, university, plat_none, plat_other in course_platform_data:
        course_platform_dict = {}
        course_platform_dict["udacity"] = udacity
        course_platform_dict["coursera"] = coursera
        course_platform_dict["edx"] = edx
        course_platform_dict["datacamp"] = datacamp
        course_platform_dict["dataquest"] = dataquest
        course_platform_dict["kaggle"] = kaggle
        course_platform_dict["fastai"] = fastai
        course_platform_dict["udemy"] = udemy
        course_platform_dict["linkedin"] = linkedin
        course_platform_dict["university"] = university
        course_platform_dict["none"] = plat_none
        course_platform_dict["other"] = plat_other
        course_platform_dict_with_name = {"course_platforms":course_platform_dict}
        data_list.append(course_platform_dict_with_name)
    for jupyter, rstudio, pycharm, atom, matlab, vsc, spyder, vim_emacs, notepad, sublime, env_none, env_other in text_editor_data:
        text_editor_dict = {}
        text_editor_dict["jupyter"] = jupyter
        text_editor_dict["rstudio"] = rstudio
        text_editor_dict["pycharm"] = pycharm
        text_editor_dict["atom"] = atom
        text_editor_dict["matlab"] = matlab
        text_editor_dict["vsc"] = vsc
        text_editor_dict["spyder"] = spyder
        text_editor_dict["vim_emacs"] = vim_emacs
        text_editor_dict["notepad++"] = notepad
        text_editor_dict["sublime"] = sublime
        text_editor_dict["none"] = env_none
        text_editor_dict["other"] = env_other
        text_editor_dict_with_name = {"text_editors":text_editor_dict}
        data_list.append(text_editor_dict_with_name)
    for python, r, sql, c, c_plusplus, java, javascript, typescript, bash, lan_matlab, lan_none, lan_other in language_data:
        language_dict = {}
        language_dict["python"] = python
        language_dict["r"] = r
        language_dict["sql"] = sql
        language_dict["c"] = c
        language_dict["c++"] = c_plusplus
        language_dict["java"] = java
        language_dict["javascript"] = javascript
        language_dict["typescript"] = typescript
        language_dict["bash"] = bash
        language_dict["matlab_language"] = lan_matlab
        language_dict["none"] = lan_none
        language_dict["other"] = lan_other
        language_dict_with_name = {"languages":language_dict}
        data_list.append(language_dict_with_name)
    for ggplot, matplotlib, altair, shiny, d3, plotly, bokeh, seaborn, geoplotlib, leaflet, vis_none, vis_other in library_data:
        library_dict = {}
        library_dict["ggplot"] = ggplot
        library_dict["matplotlib"] = matplotlib
        library_dict["altair"] = altair
        library_dict["shiny"] = shiny
        library_dict["d3"] = d3
        library_dict["plotly"] = plotly
        library_dict["bokeh"] = bokeh
        library_dict["seaborn"] = seaborn
        library_dict["geoplotlib"] = geoplotlib
        library_dict["leaflet"] = leaflet
        library_dict["none"] = vis_none
        library_dict["other"] = vis_other
        library_dict_with_name = {"libraries":library_dict}
        data_list.append(library_dict_with_name)
    for regression, tree_forest, gradient_boost, bayesian, evolutionary, dnn, cnn, gan, rnn, bert, mach_none, mach_other in ml_model_data:
        ml_model_dict = {}
        ml_model_dict["regression"] = regression
        ml_model_dict["tree_forest"] = tree_forest
        ml_model_dict["gradient_boost"] = gradient_boost
        ml_model_dict["bayesian"] = bayesian
        ml_model_dict["evolutionary"] = evolutionary
        ml_model_dict["dnn"] = dnn
        ml_model_dict["cnn"] = cnn
        ml_model_dict["gan"] = gan
        ml_model_dict["rnn"] = rnn
        ml_model_dict["bert"] = bert
        ml_model_dict["none"] = mach_none
        ml_model_dict["other"] = mach_other
        ml_model_dict_with_name = {"ml_models":ml_model_dict}
        data_list.append(ml_model_dict_with_name)
    for mysql, postgres, sql_lite, sqlserver, oracle, micro_aces, aws_data, aws_dynamo, azure_sql, google_sql, database_none, database_other in database_data:
        database_dict = {}
        database_dict["mysql"] = mysql
        database_dict["postgres"] = postgres
        database_dict["sql_lite"] = sql_lite
        database_dict["sqlserver"] = sqlserver
        database_dict["oracle"] = oracle
        database_dict["micro_aces"] = micro_aces
        database_dict["aws_data"] = aws_data
        database_dict["aws_dynamo"] = aws_dynamo
        database_dict["azure_sql"] = azure_sql
        database_dict["google_sql"] = google_sql
        database_dict["none"] = database_none
        database_dict["other"] = database_other
        database_dict_with_name = {"databases":database_dict}
        data_list.append(database_dict_with_name)

    return jsonify(data_list)


# salary_visuals page to render salary_visuals.html
@app.route("/recommendations")
def recommendations():
    return render_template("recommendations.html")


@app.route("/recommendations_data")
def recommendations_data():
    session = Session(engine)

    recommendation_data = session.query(salary_data2.first_program, func.count(salary_data2.first_program)).\
        group_by(salary_data2.first_program).all()
    session.close()
    
    data_list = []
    for language, count in recommendation_data:
        if (language != "0"):
            recommendation_dict = {}
            recommendation_dict["recommended_first_language"] = language
            recommendation_dict["count"] = count
            data_list.append(recommendation_dict)

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
    
    elif (filter_choice == "country_region_dataset1"):
        visuals_data = session.query(salary_data1.country.distinct(), salary_data1.region).all()
        session.close()

        for country, region in visuals_data:
            data_list_dict = {}
            data_list_dict["country"] = country
            data_list_dict["region"] = region
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
@app.route("/salary_data1/<title>")
def all_salary_data1(title):
    session = Session(engine)

    # query to obtain state name and rank
    all_data = session.query(salary_data1.salaryusd, salary_data1.primarydatabase,\
        salary_data1.yearswiththisdatabase, salary_data1.employmentstatus,\
            salary_data1.jobtitle, salary_data1.managestaff, salary_data1.yearswiththistypeofjob,\
            salary_data1.otherpeopleonyourteam, salary_data1.databaseservers,\
            salary_data1.education, salary_data1.educationiscomputerrelated,\
            salary_data1.certifications, salary_data1.hoursworkedperweek, salary_data1.telecommutedaysperweek,\
            salary_data1.employmentsector, salary_data1.region).\
            filter(salary_data1.jobtitle == title).all()
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


@app.route('/predictions', methods=['GET','POST'])
def go_to_prediction():
	# return render_template('predictions.html')

    import joblib
    from sklearn.preprocessing import StandardScaler

    # import csv to df
    X_encoded = pd.read_csv("exported_data/X_encoded_df.csv")
    X_encoded_empty = X_encoded[0:0]

    if request.method == 'POST':
        salary_model = joblib.load('notebooks/salary_model_trained.sav')

        X_scaler = joblib.load('notebooks/X_scaler.sav')
        y_scaler = joblib.load('notebooks/y_scaler.sav')

        #get question from the html form
        years_db = request.form['years_db']
        years_job = request.form['years_job']
        country = request.form['country']
        region = request.form['region']
        comp_ed = request.form['comp_ed']
        primary_db = request.form['primary_db']
        employ_sector = request.form['employ_sector']
        telecommute = request.form['telecommute']
        manager = request.form['manager']
        title = request.form["title"]

        yearswiththisdatabase_header = "yearswiththisdatabase"
        yearswiththistypeofjob_header = "yearswiththistypeofjob"
        country_header = "country_" + country
        primarydatabase_header = "primarydatabase_" + primary_db
        employmentsector_header = "employmentsector_" + employ_sector
        region_header = "region_" + region
        telecommutedaysperweek_header = "telecommutedaysperweek_" + telecommute
        managestaff_header = "managestaff_" + manager
        educationiscomputerrelated_header = "educationiscomputerrelated_" + comp_ed
        jobtitle = "jobtitle_" + title

        user_response_row = {yearswiththisdatabase_header:years_db, yearswiththistypeofjob_header:years_job, country_header:1, primarydatabase_header:1, employmentsector_header:1, region_header:1, telecommutedaysperweek_header:1, managestaff_header:1, educationiscomputerrelated_header:1, jobtitle:1}
        combined_df = X_encoded_empty.append(user_response_row, ignore_index=True)
        combined_df = combined_df.fillna(0)
        del combined_df["Unnamed: 0"]
        del combined_df["index"]

        user_response_transformed = X_scaler.transform(combined_df)
        prediction = salary_model.predict(user_response_transformed)
        prediction_untransformed = y_scaler.inverse_transform(prediction)

        print("PREDICTION")
        print(prediction_untransformed)

        return render_template('predictions.html', salary_prediction=prediction_untransformed)

    else:
        return render_template("predictions.html")

if __name__ == "__main__":
    app.run(debug=True)
