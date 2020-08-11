# import dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, cast, Integer
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
    course_platform_data = session.query(cast(func.sum(salary_data2.udacity), Integer), cast(func.sum(salary_data2.coursera), Integer), cast(func.sum(salary_data2.edx), Integer),\
            cast(func.sum(salary_data2.datacamp), Integer), cast(func.sum(salary_data2.dataquest), Integer), cast(func.sum(salary_data2.kaggle), Integer),\
            cast(func.sum(salary_data2.fastai), Integer), cast(func.sum(salary_data2.udemy), Integer), cast(func.sum(salary_data2.linkedin), Integer),\
            cast(func.sum(salary_data2.university), Integer), cast(func.sum(salary_data2.plat_none), Integer), cast(func.sum(salary_data2.plat_other), Integer)).all()
    text_editor_data = session.query(cast(func.sum(salary_data2.jupyter), Integer),\
            cast(func.sum(salary_data2.rstudio), Integer), cast(func.sum(salary_data2.pycharm), Integer), cast(func.sum(salary_data2.atom), Integer),\
            cast(func.sum(salary_data2.matlab), Integer), cast(func.sum(salary_data2.vsc), Integer), cast(func.sum(salary_data2.spyder), Integer),\
            cast(func.sum(salary_data2.vim_emacs), Integer), cast(func.sum(salary_data2.notepad_plusplus), Integer), cast(func.sum(salary_data2.sublime), Integer),\
            cast(func.sum(salary_data2.env_none), Integer), cast(func.sum(salary_data2.env_other), Integer)).all()
    language_data = session.query(cast(func.sum(salary_data2.python), Integer),\
            cast(func.sum(salary_data2.r), Integer), cast(func.sum(salary_data2.sql), Integer), cast(func.sum(salary_data2.c), Integer), cast(func.sum(salary_data2.c_plusplus), Integer),\
            cast(func.sum(salary_data2.java), Integer), cast(func.sum(salary_data2.javascript), Integer), cast(func.sum(salary_data2.typescript), Integer),\
            cast(func.sum(salary_data2.bash), Integer), cast(func.sum(salary_data2.lan_matlab), Integer), cast(func.sum(salary_data2.lan_none), Integer),\
            cast(func.sum(salary_data2.lan_other), Integer)).all()
    library_data = session.query(cast(func.sum(salary_data2.ggplot), Integer),\
            cast(func.sum(salary_data2.matplotlib), Integer), cast(func.sum(salary_data2.altair), Integer), cast(func.sum(salary_data2.shiny), Integer),\
            cast(func.sum(salary_data2.d3), Integer), cast(func.sum(salary_data2.plotly), Integer), cast(func.sum(salary_data2.bokeh), Integer),\
            cast(func.sum(salary_data2.seaborn), Integer), cast(func.sum(salary_data2.geoplotlib), Integer), cast(func.sum(salary_data2.leaflet), Integer),\
            cast(func.sum(salary_data2.vis_none), Integer), cast(func.sum(salary_data2.vis_other), Integer)).all()
    ml_model_data = session.query(cast(func.sum(salary_data2.regression), Integer),\
            cast(func.sum(salary_data2.tree_forest), Integer), cast(func.sum(salary_data2.gradient_boost), Integer), cast(func.sum(salary_data2.bayesian), Integer),\
            cast(func.sum(salary_data2.evolutionary), Integer), cast(func.sum(salary_data2.dnn), Integer), cast(func.sum(salary_data2.cnn), Integer),\
            cast(func.sum(salary_data2.gan), Integer), cast(func.sum(salary_data2.rnn), Integer), cast(func.sum(salary_data2.bert), Integer), cast(func.sum(salary_data2.mach_none), Integer),\
            cast(func.sum(salary_data2.mach_other), Integer)).all()
    database_data = session.query(cast(func.sum(salary_data2.mysql), Integer),\
            cast(func.sum(salary_data2.postgres), Integer), cast(func.sum(salary_data2.sql_lite), Integer), cast(func.sum(salary_data2.sqlserver), Integer),\
            cast(func.sum(salary_data2.oracle), Integer), cast(func.sum(salary_data2.micro_acess), Integer), cast(func.sum(salary_data2.aws_data), Integer),\
            cast(func.sum(salary_data2.aws_dynamo), Integer), cast(func.sum(salary_data2.azure_sql), Integer), cast(func.sum(salary_data2.google_sql), Integer),\
            cast(func.sum(salary_data2.database_none), Integer), cast(func.sum(salary_data2.database_other), Integer)).all()

    session.close()

    # adds data into a dictionaries to be jsonified
    data_list = []
    for udacity, coursera, edx, datacamp, dataquest, kaggle, fastai, udemy, linkedin, university, plat_none, plat_other in course_platform_data:
        udacity_dict = {}
        udacity_dict["type"] = "course_platform"
        udacity_dict["tool"] = "Udacity"
        udacity_dict["count"] = udacity
        coursera_dict = {}
        coursera_dict["type"] = "course_platform"
        coursera_dict["tool"] = "Coursera"
        coursera_dict["count"] = coursera
        edx_dict = {}
        edx_dict["type"] = "course_platform"
        edx_dict["tool"] = "edX"
        edx_dict["count"] = edx
        datacamp_dict = {}
        datacamp_dict["type"] = "course_platform"
        datacamp_dict["tool"] = "Datacamp"
        datacamp_dict["count"] = datacamp
        dataquest_dict = {}
        dataquest_dict["type"] = "course_platform"
        dataquest_dict["tool"] = "Dataquest"
        dataquest_dict["count"] = dataquest
        kaggle_dict = {}
        kaggle_dict["type"] = "course_platform"
        kaggle_dict["tool"] = "Kaggle"
        kaggle_dict["count"] = kaggle
        fastai_dict = {}
        fastai_dict["type"] = "course_platform"
        fastai_dict["tool"] = "fast.ai"
        fastai_dict["count"] = fastai
        udemy_dict = {}
        udemy_dict["type"] = "course_platform"
        udemy_dict["tool"] = "Udemy"
        udemy_dict["count"] = udemy
        linkedin_dict = {}
        linkedin_dict["type"] = "course_platform"
        linkedin_dict["tool"] = "LinkedIn"
        linkedin_dict["count"] = linkedin
        university_dict = {}
        university_dict["type"] = "course_platform"
        university_dict["tool"] = "University"
        university_dict["count"] = university
        plat_none_dict = {}
        plat_none_dict["type"] = "course_platform"
        plat_none_dict["tool"] = "None"
        plat_none_dict["count"] = plat_none
        plat_other_dict = {}
        plat_other_dict["type"] = "course_platform"
        plat_other_dict["tool"] = "Other"
        plat_other_dict["count"] = plat_other

        data_list.append(udacity_dict)
        data_list.append(coursera_dict)
        data_list.append(edx_dict)
        data_list.append(datacamp_dict)
        data_list.append(dataquest_dict)
        data_list.append(kaggle_dict)
        data_list.append(fastai_dict)
        data_list.append(udemy_dict)
        data_list.append(linkedin_dict)
        data_list.append(university_dict)
        data_list.append(plat_none_dict)
        data_list.append(plat_other_dict)

    for jupyter, rstudio, pycharm, atom, matlab, vsc, spyder, vim_emacs, notepad, sublime, env_none, env_other in text_editor_data:
        jupyter_dict = {}
        jupyter_dict["type"] = "text_editor"
        jupyter_dict["tool"] = "Jupyter Notebook"
        jupyter_dict["count"] = jupyter
        rstudio_dict = {}
        rstudio_dict["type"] = "text_editor"
        rstudio_dict["tool"] = "RStudio"
        rstudio_dict["count"] = rstudio
        pycharm_dict = {}
        pycharm_dict["type"] = "text_editor"
        pycharm_dict["tool"] = "PyCharm"
        pycharm_dict["count"] = pycharm
        atom_dict = {}
        atom_dict["type"] = "text_editor"
        atom_dict["tool"] = "Atom"
        atom_dict["count"] = atom
        matlab_dict = {}
        matlab_dict["type"] = "text_editor"
        matlab_dict["tool"] = "MATLAB"
        matlab_dict["count"] = matlab
        vsc_dict = {}
        vsc_dict["type"] = "text_editor"
        vsc_dict["tool"] = "Visual Studio Code"
        vsc_dict["count"] = vsc
        spyder_dict = {}
        spyder_dict["type"] = "text_editor"
        spyder_dict["tool"] = "Spyder"
        spyder_dict["count"] = spyder
        vim_emacs_dict = {}
        vim_emacs_dict["type"] = "text_editor"
        vim_emacs_dict["tool"] = "Vim/Emacs"
        vim_emacs_dict["count"] = vim_emacs
        notepad_dict = {}
        notepad_dict["type"] = "text_editor"
        notepad_dict["tool"] = "Notepad++"
        notepad_dict["count"] = notepad
        sublime_dict = {}
        sublime_dict["type"] = "text_editor"
        sublime_dict["tool"] = "Sublime"
        sublime_dict["count"] = sublime
        env_none_dict = {}
        env_none_dict["type"] = "text_editor"
        env_none_dict["tool"] = "None"
        env_none_dict["count"] = env_none
        env_other_dict = {}
        env_other_dict["type"] = "text_editor"
        env_other_dict["tool"] = "Other"
        env_other_dict["count"] = env_other

        data_list.append(jupyter_dict)
        data_list.append(rstudio_dict)
        data_list.append(pycharm_dict)
        data_list.append(atom_dict)
        data_list.append(matlab_dict)
        data_list.append(vsc_dict)
        data_list.append(spyder_dict)
        data_list.append(vim_emacs_dict)
        data_list.append(notepad_dict)
        data_list.append(sublime_dict)
        data_list.append(env_none_dict)
        data_list.append(env_other_dict)

    for python, r, sql, c, c_plusplus, java, javascript, typescript, bash, lan_matlab, lan_none, lan_other in language_data:
        python_dict = {}
        python_dict["type"] = "language"
        python_dict["tool"] = "Python"
        python_dict["count"] = python
        r_dict = {}
        r_dict["type"] = "language"
        r_dict["tool"] = "R"
        r_dict["count"] = r
        sql_dict = {}
        sql_dict["type"] = "language"
        sql_dict["tool"] = "SQL"
        sql_dict["count"] = sql
        c_dict = {}
        c_dict["type"] = "language"
        c_dict["tool"] = "C"
        c_dict["count"] = c
        c_plusplus_dict = {}
        c_plusplus_dict["type"] = "language"
        c_plusplus_dict["tool"] = "C++"
        c_plusplus_dict["count"] = c_plusplus
        java_dict = {}
        java_dict["type"] = "language"
        java_dict["tool"] = "Java"
        java_dict["count"] = java
        javascript_dict = {}
        javascript_dict["type"] = "language"
        javascript_dict["tool"] = "JavaScript"
        javascript_dict["count"] = javascript
        typescript_dict = {}
        typescript_dict["type"] = "language"
        typescript_dict["tool"] = "TypeScript"
        typescript_dict["count"] = typescript
        bash_dict = {}
        bash_dict["type"] = "language"
        bash_dict["tool"] = "Bash"
        bash_dict["count"] = bash
        lan_matlab_dict = {}
        lan_matlab_dict["type"] = "language"
        lan_matlab_dict["tool"] = "MATLAB"
        lan_matlab_dict["count"] = lan_matlab
        lan_none_dict = {}
        lan_none_dict["type"] = "language"
        lan_none_dict["tool"] = "None"
        lan_none_dict["count"] = lan_none
        lan_other_dict = {}
        lan_other_dict["type"] = "language"
        lan_other_dict["tool"] = "Other"
        lan_other_dict["count"] = lan_other

        data_list.append(python_dict)
        data_list.append(r_dict)
        data_list.append(sql_dict)
        data_list.append(c_dict)
        data_list.append(c_plusplus_dict)
        data_list.append(java_dict)
        data_list.append(javascript_dict)
        data_list.append(typescript_dict)
        data_list.append(bash_dict)
        data_list.append(lan_matlab_dict)
        data_list.append(lan_none_dict)
        data_list.append(lan_other_dict)

    for ggplot, matplotlib, altair, shiny, d3, plotly, bokeh, seaborn, geoplotlib, leaflet, vis_none, vis_other in library_data:
        ggplot_dict = {}
        ggplot_dict["type"] = "visualization_library"
        ggplot_dict["tool"] = "ggplot"
        ggplot_dict["count"] = ggplot
        matplotlib_dict = {}
        matplotlib_dict["type"] = "visualization_library"
        matplotlib_dict["tool"] = "Matplotlib"
        matplotlib_dict["count"] = matplotlib
        altair_dict = {}
        altair_dict["type"] = "visualization_library"
        altair_dict["tool"] = "Altair"
        altair_dict["count"] = altair
        shiny_dict = {}
        shiny_dict["type"] = "visualization_library"
        shiny_dict["tool"] = "Shiny"
        shiny_dict["count"] = shiny
        d3_dict = {}
        d3_dict["type"] = "visualization_library"
        d3_dict["tool"] = "d3"
        d3_dict["count"] = d3
        plotly_dict = {}
        plotly_dict["type"] = "visualization_library"
        plotly_dict["tool"] = "Plotly"
        plotly_dict["count"] = plotly
        bokeh_dict = {}
        bokeh_dict["type"] = "visualization_library"
        bokeh_dict["tool"] = "Bokeh"
        bokeh_dict["count"] = bokeh
        seaborn_dict = {}
        seaborn_dict["type"] = "visualization_library"
        seaborn_dict["tool"] = "Seaborn"
        seaborn_dict["count"] = seaborn
        geoplotlib_dict = {}
        geoplotlib_dict["type"] = "visualization_library"
        geoplotlib_dict["tool"] = "geoplotlib"
        geoplotlib_dict["count"] = geoplotlib
        leaflet_dict = {}
        leaflet_dict["type"] = "visualization_library"
        leaflet_dict["tool"] = "Leaflet"
        leaflet_dict["count"] = leaflet
        vis_none_dict = {}
        vis_none_dict["type"] = "visualization_library"
        vis_none_dict["tool"] = "None"
        vis_none_dict["count"] = vis_none
        vis_other_dict = {}
        vis_other_dict["type"] = "visualization_library"
        vis_other_dict["tool"] = "Other"
        vis_other_dict["count"] = vis_other

        data_list.append(ggplot_dict)
        data_list.append(matplotlib_dict)
        data_list.append(altair_dict)
        data_list.append(shiny_dict)
        data_list.append(d3_dict)
        data_list.append(plotly_dict)
        data_list.append(bokeh_dict)
        data_list.append(seaborn_dict)
        data_list.append(geoplotlib_dict)
        data_list.append(leaflet_dict)
        data_list.append(vis_none_dict)
        data_list.append(vis_other_dict)

    for regression, tree_forest, gradient_boost, bayesian, evolutionary, dnn, cnn, gan, rnn, bert, mach_none, mach_other in ml_model_data:
        regression_dict = {}
        regression_dict["type"] = "ml_model"
        regression_dict["tool"] = "Regression"
        regression_dict["count"] = regression
        tree_forest_dict = {}
        tree_forest_dict["type"] = "ml_model"
        tree_forest_dict["tool"] = "Random Forest"
        tree_forest_dict["count"] = tree_forest
        gradient_boost_dict = {}
        gradient_boost_dict["type"] = "ml_model"
        gradient_boost_dict["tool"] = "Gradient Boost"
        gradient_boost_dict["count"] = gradient_boost
        bayesian_dict = {}
        bayesian_dict["type"] = "ml_model"
        bayesian_dict["tool"] = "Bayesian"
        bayesian_dict["count"] = bayesian
        evolutionary_dict = {}
        evolutionary_dict["type"] = "ml_model"
        evolutionary_dict["tool"] = "Evolutionary"
        evolutionary_dict["count"] = evolutionary
        dnn_dict = {}
        dnn_dict["type"] = "ml_model"
        dnn_dict["tool"] = "DNN"
        dnn_dict["count"] = dnn
        cnn_dict = {}
        cnn_dict["type"] = "ml_model"
        cnn_dict["tool"] = "CNN"
        cnn_dict["count"] = cnn
        gan_dict = {}
        gan_dict["type"] = "ml_model"
        gan_dict["tool"] = "GAN"
        gan_dict["count"] = gan
        rnn_dict = {}
        rnn_dict["type"] = "ml_model"
        rnn_dict["tool"] = "RNN"
        rnn_dict["count"] = rnn
        bert_dict = {}
        bert_dict["type"] = "ml_model"
        bert_dict["tool"] = "BERT"
        bert_dict["count"] = bert
        mach_none_dict = {}
        mach_none_dict["type"] = "ml_model"
        mach_none_dict["tool"] = "None"
        mach_none_dict["count"] = mach_none
        mach_other_dict = {}
        mach_other_dict["type"] = "ml_model"
        mach_other_dict["tool"] = "Other"
        mach_other_dict["count"] = mach_other

        data_list.append(regression_dict)
        data_list.append(tree_forest_dict)
        data_list.append(gradient_boost_dict)
        data_list.append(bayesian_dict)
        data_list.append(evolutionary_dict)
        data_list.append(dnn_dict)
        data_list.append(cnn_dict)
        data_list.append(gan_dict)
        data_list.append(rnn_dict)
        data_list.append(bert_dict)
        data_list.append(mach_none_dict)
        data_list.append(mach_other_dict)

    for mysql, postgres, sql_lite, sqlserver, oracle, micro_aces, aws_data, aws_dynamo, azure_sql, google_sql, database_none, database_other in database_data:
        mysql_dict = {}
        mysql_dict["type"] = "database"
        mysql_dict["tool"] = "MySQL"
        mysql_dict["count"] = mysql
        postgres_dict = {}
        postgres_dict["type"] = "database"
        postgres_dict["tool"] = "PostgreSQL"
        postgres_dict["count"] = postgres
        sql_lite_dict = {}
        sql_lite_dict["type"] = "database"
        sql_lite_dict["tool"] = "SQLite"
        sql_lite_dict["count"] = sql_lite
        sqlserver_dict = {}
        sqlserver_dict["type"] = "database"
        sqlserver_dict["tool"] = "SQL Server"
        sqlserver_dict["count"] = sqlserver
        oracle_dict = {}
        oracle_dict["type"] = "database"
        oracle_dict["tool"] = "Oracle"
        oracle_dict["count"] = oracle
        micro_aces_dict = {}
        micro_aces_dict["type"] = "database"
        micro_aces_dict["tool"] = "Micro Access"
        micro_aces_dict["count"] = micro_aces
        aws_data_dict = {}
        aws_data_dict["type"] = "database"
        aws_data_dict["tool"] = "AWS"
        aws_data_dict["count"] = aws_data
        aws_dynamo_dict = {}
        aws_dynamo_dict["type"] = "database"
        aws_dynamo_dict["tool"] = "DynamoDB"
        aws_dynamo_dict["count"] = aws_dynamo
        azure_sql_dict = {}
        azure_sql_dict["type"] = "database"
        azure_sql_dict["tool"] = "Azure"
        azure_sql_dict["count"] = azure_sql
        google_sql_dict = {}
        google_sql_dict["type"] = "database"
        google_sql_dict["tool"] = "Google SQL"
        google_sql_dict["count"] = google_sql
        database_none_dict = {}
        database_none_dict["type"] = "database"
        database_none_dict["tool"] = "None"
        database_none_dict["count"] = database_none
        database_other_dict = {}
        database_other_dict["type"] = "database"
        database_other_dict["tool"] = "Other"
        database_other_dict["count"] = database_other

        data_list.append(mysql_dict)
        data_list.append(postgres_dict)
        data_list.append(sql_lite_dict)
        data_list.append(sqlserver_dict)
        data_list.append(oracle_dict)
        data_list.append(micro_aces_dict)
        data_list.append(aws_data_dict)
        data_list.append(aws_dynamo_dict)
        data_list.append(azure_sql_dict)
        data_list.append(google_sql_dict)
        data_list.append(database_none_dict)
        data_list.append(database_other_dict)

    return jsonify(data_list)


@app.route("/tools_data/<jobtitle>")
def tools_data_by_title(jobtitle):
    session = Session(engine)

    # query to obtain totals of each type within tool category
    course_platform_data = session.query(cast(func.sum(salary_data2.udacity), Integer), cast(func.sum(salary_data2.coursera), Integer), cast(func.sum(salary_data2.edx), Integer),\
            cast(func.sum(salary_data2.datacamp), Integer), cast(func.sum(salary_data2.dataquest), Integer), cast(func.sum(salary_data2.kaggle), Integer),\
            cast(func.sum(salary_data2.fastai), Integer), cast(func.sum(salary_data2.udemy), Integer), cast(func.sum(salary_data2.linkedin), Integer),\
            cast(func.sum(salary_data2.university), Integer), cast(func.sum(salary_data2.plat_none), Integer), cast(func.sum(salary_data2.plat_other), Integer)).\
            filter(salary_data2.title == jobtitle).all()
    text_editor_data = session.query(cast(func.sum(salary_data2.jupyter), Integer),\
            cast(func.sum(salary_data2.rstudio), Integer), cast(func.sum(salary_data2.pycharm), Integer), cast(func.sum(salary_data2.atom), Integer),\
            cast(func.sum(salary_data2.matlab), Integer), cast(func.sum(salary_data2.vsc), Integer), cast(func.sum(salary_data2.spyder), Integer),\
            cast(func.sum(salary_data2.vim_emacs), Integer), cast(func.sum(salary_data2.notepad_plusplus), Integer), cast(func.sum(salary_data2.sublime), Integer),\
            cast(func.sum(salary_data2.env_none), Integer), cast(func.sum(salary_data2.env_other), Integer)).\
            filter(salary_data2.title == jobtitle).all()
    language_data = session.query(cast(func.sum(salary_data2.python), Integer),\
            cast(func.sum(salary_data2.r), Integer), cast(func.sum(salary_data2.sql), Integer), cast(func.sum(salary_data2.c), Integer), cast(func.sum(salary_data2.c_plusplus), Integer),\
            cast(func.sum(salary_data2.java), Integer), cast(func.sum(salary_data2.javascript), Integer), cast(func.sum(salary_data2.typescript), Integer),\
            cast(func.sum(salary_data2.bash), Integer), cast(func.sum(salary_data2.lan_matlab), Integer), cast(func.sum(salary_data2.lan_none), Integer),\
            cast(func.sum(salary_data2.lan_other), Integer)).filter(salary_data2.title == jobtitle).all()
    library_data = session.query(cast(func.sum(salary_data2.ggplot), Integer),\
            cast(func.sum(salary_data2.matplotlib), Integer), cast(func.sum(salary_data2.altair), Integer), cast(func.sum(salary_data2.shiny), Integer),\
            cast(func.sum(salary_data2.d3), Integer), cast(func.sum(salary_data2.plotly), Integer), cast(func.sum(salary_data2.bokeh), Integer),\
            cast(func.sum(salary_data2.seaborn), Integer), cast(func.sum(salary_data2.geoplotlib), Integer), cast(func.sum(salary_data2.leaflet), Integer),\
            cast(func.sum(salary_data2.vis_none), Integer), cast(func.sum(salary_data2.vis_other), Integer)).\
            filter(salary_data2.title == jobtitle).all()
    ml_model_data = session.query(cast(func.sum(salary_data2.regression), Integer),\
            cast(func.sum(salary_data2.tree_forest), Integer), cast(func.sum(salary_data2.gradient_boost), Integer), cast(func.sum(salary_data2.bayesian), Integer),\
            cast(func.sum(salary_data2.evolutionary), Integer), cast(func.sum(salary_data2.dnn), Integer), cast(func.sum(salary_data2.cnn), Integer),\
            cast(func.sum(salary_data2.gan), Integer), cast(func.sum(salary_data2.rnn), Integer), cast(func.sum(salary_data2.bert), Integer), cast(func.sum(salary_data2.mach_none), Integer),\
            cast(func.sum(salary_data2.mach_other), Integer)).filter(salary_data2.title == jobtitle).all()
    database_data = session.query(cast(func.sum(salary_data2.mysql), Integer),\
            cast(func.sum(salary_data2.postgres), Integer), cast(func.sum(salary_data2.sql_lite), Integer), cast(func.sum(salary_data2.sqlserver), Integer),\
            cast(func.sum(salary_data2.oracle), Integer), cast(func.sum(salary_data2.micro_acess), Integer), cast(func.sum(salary_data2.aws_data), Integer),\
            cast(func.sum(salary_data2.aws_dynamo), Integer), cast(func.sum(salary_data2.azure_sql), Integer), cast(func.sum(salary_data2.google_sql), Integer),\
            cast(func.sum(salary_data2.database_none), Integer), cast(func.sum(salary_data2.database_other), Integer)).\
            filter(salary_data2.title == jobtitle).all()

    session.close()

     # adds data into a dictionaries to be jsonified
    data_list = []
    for udacity, coursera, edx, datacamp, dataquest, kaggle, fastai, udemy, linkedin, university, plat_none, plat_other in course_platform_data:
        udacity_dict = {}
        udacity_dict["type"] = "course_platform"
        udacity_dict["tool"] = "udacity"
        udacity_dict["count"] = udacity
        coursera_dict = {}
        coursera_dict["type"] = "course_platform"
        coursera_dict["tool"] = "coursera"
        coursera_dict["count"] = coursera
        edx_dict = {}
        edx_dict["type"] = "course_platform"
        edx_dict["tool"] = "edx"
        edx_dict["count"] = edx
        datacamp_dict = {}
        datacamp_dict["type"] = "course_platform"
        datacamp_dict["tool"] = "datacamp"
        datacamp_dict["count"] = datacamp
        dataquest_dict = {}
        dataquest_dict["type"] = "course_platform"
        dataquest_dict["tool"] = "dataquest"
        dataquest_dict["count"] = dataquest
        kaggle_dict = {}
        kaggle_dict["type"] = "course_platform"
        kaggle_dict["tool"] = "kaggle"
        kaggle_dict["count"] = kaggle
        fastai_dict = {}
        fastai_dict["type"] = "course_platform"
        fastai_dict["tool"] = "fastai"
        fastai_dict["count"] = fastai
        udemy_dict = {}
        udemy_dict["type"] = "course_platform"
        udemy_dict["tool"] = "udemy"
        udemy_dict["count"] = udemy
        linkedin_dict = {}
        linkedin_dict["type"] = "course_platform"
        linkedin_dict["tool"] = "linkedin"
        linkedin_dict["count"] = linkedin
        university_dict = {}
        university_dict["type"] = "course_platform"
        university_dict["tool"] = "university"
        university_dict["count"] = university
        plat_none_dict = {}
        plat_none_dict["type"] = "course_platform"
        plat_none_dict["tool"] = "none"
        plat_none_dict["count"] = plat_none
        plat_other_dict = {}
        plat_other_dict["type"] = "course_platform"
        plat_other_dict["tool"] = "other"
        plat_other_dict["count"] = plat_other

        data_list.append(udacity_dict)
        data_list.append(coursera_dict)
        data_list.append(edx_dict)
        data_list.append(datacamp_dict)
        data_list.append(dataquest_dict)
        data_list.append(kaggle_dict)
        data_list.append(fastai_dict)
        data_list.append(udemy_dict)
        data_list.append(linkedin_dict)
        data_list.append(university_dict)
        data_list.append(plat_none_dict)
        data_list.append(plat_other_dict)

    for jupyter, rstudio, pycharm, atom, matlab, vsc, spyder, vim_emacs, notepad, sublime, env_none, env_other in text_editor_data:
        jupyter_dict = {}
        jupyter_dict["type"] = "text_editor"
        jupyter_dict["tool"] = "jupyter_notebook"
        jupyter_dict["count"] = jupyter
        rstudio_dict = {}
        rstudio_dict["type"] = "text_editor"
        rstudio_dict["tool"] = "rstudio"
        rstudio_dict["count"] = rstudio
        pycharm_dict = {}
        pycharm_dict["type"] = "text_editor"
        pycharm_dict["tool"] = "pycharm"
        pycharm_dict["count"] = pycharm
        atom_dict = {}
        atom_dict["type"] = "text_editor"
        atom_dict["tool"] = "atom"
        atom_dict["count"] = atom
        matlab_dict = {}
        matlab_dict["type"] = "text_editor"
        matlab_dict["tool"] = "matlab"
        matlab_dict["count"] = matlab
        vsc_dict = {}
        vsc_dict["type"] = "text_editor"
        vsc_dict["tool"] = "visual_studio_code"
        vsc_dict["count"] = vsc
        spyder_dict = {}
        spyder_dict["type"] = "text_editor"
        spyder_dict["tool"] = "spyder"
        spyder_dict["count"] = spyder
        vim_emacs_dict = {}
        vim_emacs_dict["type"] = "text_editor"
        vim_emacs_dict["tool"] = "vim_emacs"
        vim_emacs_dict["count"] = vim_emacs
        notepad_dict = {}
        notepad_dict["type"] = "text_editor"
        notepad_dict["tool"] = "notepad++"
        notepad_dict["count"] = notepad
        sublime_dict = {}
        sublime_dict["type"] = "text_editor"
        sublime_dict["tool"] = "sublime"
        sublime_dict["count"] = sublime
        env_none_dict = {}
        env_none_dict["type"] = "text_editor"
        env_none_dict["tool"] = "none"
        env_none_dict["count"] = env_none
        env_other_dict = {}
        env_other_dict["type"] = "text_editor"
        env_other_dict["tool"] = "other"
        env_other_dict["count"] = env_other

        data_list.append(jupyter_dict)
        data_list.append(rstudio_dict)
        data_list.append(pycharm_dict)
        data_list.append(atom_dict)
        data_list.append(matlab_dict)
        data_list.append(vsc_dict)
        data_list.append(spyder_dict)
        data_list.append(vim_emacs_dict)
        data_list.append(notepad_dict)
        data_list.append(sublime_dict)
        data_list.append(env_none_dict)
        data_list.append(env_other_dict)

    for python, r, sql, c, c_plusplus, java, javascript, typescript, bash, lan_matlab, lan_none, lan_other in language_data:
        python_dict = {}
        python_dict["type"] = "language"
        python_dict["tool"] = "python"
        python_dict["count"] = python
        r_dict = {}
        r_dict["type"] = "language"
        r_dict["tool"] = "r"
        r_dict["count"] = r
        sql_dict = {}
        sql_dict["type"] = "language"
        sql_dict["tool"] = "sql"
        sql_dict["count"] = sql
        c_dict = {}
        c_dict["type"] = "language"
        c_dict["tool"] = "c"
        c_dict["count"] = c
        c_plusplus_dict = {}
        c_plusplus_dict["type"] = "language"
        c_plusplus_dict["tool"] = "c++"
        c_plusplus_dict["count"] = c_plusplus
        java_dict = {}
        java_dict["type"] = "language"
        java_dict["tool"] = "java"
        java_dict["count"] = java
        javascript_dict = {}
        javascript_dict["type"] = "language"
        javascript_dict["tool"] = "javascript"
        javascript_dict["count"] = javascript
        typescript_dict = {}
        typescript_dict["type"] = "language"
        typescript_dict["tool"] = "typescript"
        typescript_dict["count"] = typescript
        bash_dict = {}
        bash_dict["type"] = "language"
        bash_dict["tool"] = "bash"
        bash_dict["count"] = bash
        lan_matlab_dict = {}
        lan_matlab_dict["type"] = "language"
        lan_matlab_dict["tool"] = "matlab_language"
        lan_matlab_dict["count"] = lan_matlab
        lan_none_dict = {}
        lan_none_dict["type"] = "language"
        lan_none_dict["tool"] = "none"
        lan_none_dict["count"] = lan_none
        lan_other_dict = {}
        lan_other_dict["type"] = "language"
        lan_other_dict["tool"] = "other"
        lan_other_dict["count"] = lan_other

        data_list.append(python_dict)
        data_list.append(r_dict)
        data_list.append(sql_dict)
        data_list.append(c_dict)
        data_list.append(c_plusplus_dict)
        data_list.append(java_dict)
        data_list.append(javascript_dict)
        data_list.append(typescript_dict)
        data_list.append(bash_dict)
        data_list.append(lan_matlab_dict)
        data_list.append(lan_none_dict)
        data_list.append(lan_other_dict)

    for ggplot, matplotlib, altair, shiny, d3, plotly, bokeh, seaborn, geoplotlib, leaflet, vis_none, vis_other in library_data:
        ggplot_dict = {}
        ggplot_dict["type"] = "visualization_library"
        ggplot_dict["tool"] = "ggplot"
        ggplot_dict["count"] = ggplot
        matplotlib_dict = {}
        matplotlib_dict["type"] = "visualization_library"
        matplotlib_dict["tool"] = "matplotlib"
        matplotlib_dict["count"] = matplotlib
        altair_dict = {}
        altair_dict["type"] = "visualization_library"
        altair_dict["tool"] = "altair"
        altair_dict["count"] = altair
        shiny_dict = {}
        shiny_dict["type"] = "visualization_library"
        shiny_dict["tool"] = "shiny"
        shiny_dict["count"] = shiny
        d3_dict = {}
        d3_dict["type"] = "visualization_library"
        d3_dict["tool"] = "d3"
        d3_dict["count"] = d3
        plotly_dict = {}
        plotly_dict["type"] = "visualization_library"
        plotly_dict["tool"] = "plotly"
        plotly_dict["count"] = plotly
        bokeh_dict = {}
        bokeh_dict["type"] = "visualization_library"
        bokeh_dict["tool"] = "bokeh"
        bokeh_dict["count"] = bokeh
        seaborn_dict = {}
        seaborn_dict["type"] = "visualization_library"
        seaborn_dict["tool"] = "seaborn"
        seaborn_dict["count"] = seaborn
        geoplotlib_dict = {}
        geoplotlib_dict["type"] = "visualization_library"
        geoplotlib_dict["tool"] = "geoplotlib"
        geoplotlib_dict["count"] = geoplotlib
        leaflet_dict = {}
        leaflet_dict["type"] = "visualization_library"
        leaflet_dict["tool"] = "leaflet"
        leaflet_dict["count"] = leaflet
        vis_none_dict = {}
        vis_none_dict["type"] = "visualization_library"
        vis_none_dict["tool"] = "none"
        vis_none_dict["count"] = vis_none
        vis_other_dict = {}
        vis_other_dict["type"] = "visualization_library"
        vis_other_dict["tool"] = "other"
        vis_other_dict["count"] = vis_other

        data_list.append(ggplot_dict)
        data_list.append(matplotlib_dict)
        data_list.append(altair_dict)
        data_list.append(shiny_dict)
        data_list.append(d3_dict)
        data_list.append(plotly_dict)
        data_list.append(bokeh_dict)
        data_list.append(seaborn_dict)
        data_list.append(geoplotlib_dict)
        data_list.append(leaflet_dict)
        data_list.append(vis_none_dict)
        data_list.append(vis_other_dict)

    for regression, tree_forest, gradient_boost, bayesian, evolutionary, dnn, cnn, gan, rnn, bert, mach_none, mach_other in ml_model_data:
        regression_dict = {}
        regression_dict["type"] = "ml_model"
        regression_dict["tool"] = "regression"
        regression_dict["count"] = regression
        tree_forest_dict = {}
        tree_forest_dict["type"] = "ml_model"
        tree_forest_dict["tool"] = "tree_forest"
        tree_forest_dict["count"] = tree_forest
        gradient_boost_dict = {}
        gradient_boost_dict["type"] = "ml_model"
        gradient_boost_dict["tool"] = "gradient_boost"
        gradient_boost_dict["count"] = gradient_boost
        bayesian_dict = {}
        bayesian_dict["type"] = "ml_model"
        bayesian_dict["tool"] = "bayesian"
        bayesian_dict["count"] = bayesian
        evolutionary_dict = {}
        evolutionary_dict["type"] = "ml_model"
        evolutionary_dict["tool"] = "evolutionary"
        evolutionary_dict["count"] = evolutionary
        dnn_dict = {}
        dnn_dict["type"] = "ml_model"
        dnn_dict["tool"] = "dnn"
        dnn_dict["count"] = dnn
        cnn_dict = {}
        cnn_dict["type"] = "ml_model"
        cnn_dict["tool"] = "cnn"
        cnn_dict["count"] = cnn
        gan_dict = {}
        gan_dict["type"] = "ml_model"
        gan_dict["tool"] = "gan"
        gan_dict["count"] = gan
        rnn_dict = {}
        rnn_dict["type"] = "ml_model"
        rnn_dict["tool"] = "rnn"
        rnn_dict["count"] = rnn
        bert_dict = {}
        bert_dict["type"] = "ml_model"
        bert_dict["tool"] = "bert"
        bert_dict["count"] = bert
        mach_none_dict = {}
        mach_none_dict["type"] = "ml_model"
        mach_none_dict["tool"] = "none"
        mach_none_dict["count"] = mach_none
        mach_other_dict = {}
        mach_other_dict["type"] = "ml_model"
        mach_other_dict["tool"] = "other"
        mach_other_dict["count"] = mach_other

        data_list.append(regression_dict)
        data_list.append(tree_forest_dict)
        data_list.append(gradient_boost_dict)
        data_list.append(bayesian_dict)
        data_list.append(evolutionary_dict)
        data_list.append(dnn_dict)
        data_list.append(cnn_dict)
        data_list.append(gan_dict)
        data_list.append(rnn_dict)
        data_list.append(bert_dict)
        data_list.append(mach_none_dict)
        data_list.append(mach_other_dict)

    for mysql, postgres, sql_lite, sqlserver, oracle, micro_aces, aws_data, aws_dynamo, azure_sql, google_sql, database_none, database_other in database_data:
        mysql_dict = {}
        mysql_dict["type"] = "database"
        mysql_dict["tool"] = "mysql"
        mysql_dict["count"] = mysql
        postgres_dict = {}
        postgres_dict["type"] = "database"
        postgres_dict["tool"] = "postgres"
        postgres_dict["count"] = postgres
        sql_lite_dict = {}
        sql_lite_dict["type"] = "database"
        sql_lite_dict["tool"] = "sql_lite"
        sql_lite_dict["count"] = sql_lite
        sqlserver_dict = {}
        sqlserver_dict["type"] = "database"
        sqlserver_dict["tool"] = "sqlserver"
        sqlserver_dict["count"] = sqlserver
        oracle_dict = {}
        oracle_dict["type"] = "database"
        oracle_dict["tool"] = "oracle"
        oracle_dict["count"] = oracle
        micro_aces_dict = {}
        micro_aces_dict["type"] = "database"
        micro_aces_dict["tool"] = "micro_aces"
        micro_aces_dict["count"] = micro_aces
        aws_data_dict = {}
        aws_data_dict["type"] = "database"
        aws_data_dict["tool"] = "aws_data"
        aws_data_dict["count"] = aws_data
        aws_dynamo_dict = {}
        aws_dynamo_dict["type"] = "database"
        aws_dynamo_dict["tool"] = "aws_dynamo"
        aws_dynamo_dict["count"] = aws_dynamo
        azure_sql_dict = {}
        azure_sql_dict["type"] = "database"
        azure_sql_dict["tool"] = "azure_sql"
        azure_sql_dict["count"] = azure_sql
        google_sql_dict = {}
        google_sql_dict["type"] = "database"
        google_sql_dict["tool"] = "google_sql"
        google_sql_dict["count"] = google_sql
        database_none_dict = {}
        database_none_dict["type"] = "database"
        database_none_dict["tool"] = "none"
        database_none_dict["count"] = database_none
        database_other_dict = {}
        database_other_dict["type"] = "database"
        database_other_dict["tool"] = "other"
        database_other_dict["count"] = database_other

        data_list.append(mysql_dict)
        data_list.append(postgres_dict)
        data_list.append(sql_lite_dict)
        data_list.append(sqlserver_dict)
        data_list.append(oracle_dict)
        data_list.append(micro_aces_dict)
        data_list.append(aws_data_dict)
        data_list.append(aws_dynamo_dict)
        data_list.append(azure_sql_dict)
        data_list.append(google_sql_dict)
        data_list.append(database_none_dict)
        data_list.append(database_other_dict)

    return jsonify(data_list)


# salary_visuals page to render salary_visuals.html
@app.route("/recommendations")
def recommendations():
    return render_template("recommendations.html")


@app.route("/recommendations_data")
def recommendations_data():
    session = Session(engine)

    recommendation_data = session.query(salary_data2.first_program, cast(func.count(salary_data2.first_program), Integer)).\
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


@app.route("/recommendations_data/<jobtitle>")
def recommendations_data_by_title(jobtitle):
    session = Session(engine)

    recommendation_data = session.query(salary_data2.first_program, cast(func.count(salary_data2.first_program), Integer)).\
        filter(salary_data2.title == jobtitle).\
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


@app.route("/education_data")
def education_data():
    session = Session(engine)

    salary_data = session.query(salary_data2.title, cast(func.avg(salary_data2.salary), Integer)).\
        group_by(salary_data2.title, salary_data2.education).all()
    session.close()

    education_data = session.query(salary_data2.title, salary_data2.education, cast(func.count(salary_data2.education), Integer)).\
        group_by(salary_data2.title, salary_data2.education).all()
    session.close()

    for title, salary in salary_data:
        if title == "Business Analyst":
            business_analyst_salary = salary
        elif title == "Data Analyst":
            data_analyst_salary = salary
        elif title == "Data Engineer":
            data_engineer_salary = salary
        elif title == "DBA/Database Engineer":
            dba_salary = salary
        elif title == "Software Engineer":
            software_engineer_salary = salary
        elif title == "Research Scientist":
            research_scientist_salary = salary
        elif title == "Product/Project Manager":
            manager_salary = salary
        elif title == "Data Scientist":
            data_scientist_salary = salary

    data_list = []
    business_analyst_ed_count_list = []
    data_analyst_ed_count_list = []
    data_engineer_ed_count_list = []
    dba_ed_count_list = []
    software_ed_count_list = []
    research_ed_count_list = []
    manager_ed_count_list = []
    data_scientist_ed_count_list = []

    for title, education, count in education_data:
        if title == "Business Analyst":
            business_analyst_ed_count_dict = {}
            business_analyst_ed_count_dict[education] = count
            business_analyst_ed_count_list.append(business_analyst_ed_count_dict)
            business_analyst_dict = {}
            business_analyst_dict[title] = {
                "education": business_analyst_ed_count_list,
                "salary": business_analyst_salary
            }
        elif title == "Data Analyst":
            data_analyst_ed_count_dict = {}
            data_analyst_ed_count_dict[education] = count
            data_analyst_ed_count_list.append(data_analyst_ed_count_dict)
            data_analyst_dict = {}
            data_analyst_dict[title] = {
                "education": data_analyst_ed_count_list,
                "salary": data_analyst_salary
            }
        elif title == "Data Engineer":
            data_engineer_ed_count_dict = {}
            data_engineer_ed_count_dict[education] = count
            data_engineer_ed_count_list.append(data_engineer_ed_count_dict)
            data_engineer_dict = {}
            data_engineer_dict[title] = {
                "education": data_engineer_ed_count_list,
                "salary": data_engineer_salary
            }
        elif title == "DBA/Database Engineer":
            dba_ed_count_dict = {}
            dba_ed_count_dict[education] = count
            dba_ed_count_list.append(dba_ed_count_dict)
            dba_dict = {}
            dba_dict[title] = {
                "education": dba_ed_count_list,
                "salary": dba_salary
            }
        elif title == "Software Engineer":
            software_ed_count_dict = {}
            software_ed_count_dict[education] = count
            software_ed_count_list.append(software_ed_count_dict)
            software_engineer_dict = {}
            software_engineer_dict[title] = {
                "education": software_ed_count_list,
                "salary": software_engineer_salary
            }
        elif title == "Research Scientist":
            research_ed_count_dict = {}
            research_ed_count_dict[education] = count
            research_ed_count_list.append(research_ed_count_dict)
            research_scientist_dict = {}
            research_scientist_dict[title] = {
                "education": research_ed_count_list,
                "salary": research_scientist_salary
            }
        elif title == "Product/Project Manager":
            manager_ed_count_dict = {}
            manager_ed_count_dict[education] = count
            manager_ed_count_list.append(manager_ed_count_dict)
            manager_dict = {}
            manager_dict[title] = {
                "education": manager_ed_count_list,
                "salary": manager_salary
            }
        elif title == "Data Scientist":
            data_scientist_ed_count_dict = {}
            data_scientist_ed_count_dict[education] = count
            data_scientist_ed_count_list.append(data_scientist_ed_count_dict)
            data_scientist_dict = {}
            data_scientist_dict[title] = {
                "education": data_scientist_ed_count_list,
                "salary": data_scientist_salary
            }

    data_list.append(business_analyst_dict)
    data_list.append(data_analyst_dict)
    data_list.append(dba_dict)
    data_list.append(data_engineer_dict)
    data_list.append(software_engineer_dict)
    data_list.append(research_scientist_dict)
    data_list.append(manager_dict)
    data_list.append(data_scientist_dict)

    return jsonify(data_list)



@app.route("/country_region_data")
def salary_visuals_data():
    session = Session(engine)

    # elif (filter_choice == "country_region_dataset1"):
    visuals_data = session.query(salary_data1.country.distinct(), salary_data1.region).all()
    session.close()

    data_list = []
    for country, region in visuals_data:
        data_list_dict = {}
        data_list_dict["country"] = country
        data_list_dict["region"] = region
        data_list.append(data_list_dict)

    return jsonify(data_list)

    # # query to obtain salaries of each chosen filter
    # if (filter_choice == "job_title_dataset2"):
    #     visuals_data = session.query(salary_data2.title, cast(func.count(salary_data2.title), Integer), cast(func.avg(salary_data2.salary), Integer)).\
    #         group_by(salary_data2.title).all()
    #     session.close()

    #     # adds data into a dictionary to be jsonified
    #     for title, count, salary in visuals_data:
    #         data_list_dict = {}
    #         data_list_dict["job_title"] = title
    #         data_list_dict["count"] = count
    #         data_list_dict["salary"] = salary
    #         data_list.append(data_list_dict)

    # elif (filter_choice == "gender"):
    #     visuals_data = session.query(salary_data2.gender, cast(func.count(salary_data2.gender), Integer), cast(func.avg(salary_data2.salary), Integer)).\
    #         group_by(salary_data2.gender).all()
    #     session.close()

    #     for gender, count, salary in visuals_data:
    #         data_list_dict = {}
    #         data_list_dict["gender"] = gender
    #         data_list_dict["count"] = count
    #         data_list_dict["salary"] = salary
    #         data_list.append(data_list_dict)

    # elif (filter_choice == "education_dataset2"):
    #     visuals_data = session.query(salary_data2.education, cast(func.count(salary_data2.education), Integer), cast(func.avg(salary_data2.salary), Integer)).\
    #         group_by(salary_data2.education).all()
    #     session.close()

    #     for education, count, salary in visuals_data:
    #         data_list_dict = {}
    #         data_list_dict["education"] = education
    #         data_list_dict["count"] = count
    #         data_list_dict["salary"] = salary
    #         data_list.append(data_list_dict)

    # elif (filter_choice == "country_dataset2"):
    #     visuals_data = session.query(salary_data2.country, cast(func.count(salary_data2.country), Integer), cast(func.avg(salary_data2.salary), Integer)).\
    #         group_by(salary_data2.country).all()
    #     session.close()

    #     for country, count, salary in visuals_data:
    #         data_list_dict = {}
    #         data_list_dict["country"] = country
    #         data_list_dict["count"] = count
    #         data_list_dict["salary"] = salary
    #         data_list.append(data_list_dict)

    # elif (filter_choice == "job_title_dataset1"):
    #     visuals_data = session.query(salary_data1.jobtitle, cast(func.count(salary_data1.jobtitle), Integer), cast(func.avg(salary_data1.salaryusd), Integer)).\
    #         group_by(salary_data1.jobtitle).all()
    #     session.close()

    #     for title, count, salary in visuals_data:
    #         data_list_dict = {}
    #         data_list_dict["job_title"] = title
    #         data_list_dict["count"] = count
    #         data_list_dict["salary"] = salary
    #         data_list.append(data_list_dict)

    # elif (filter_choice == "education_dataset1"):
    #     visuals_data = session.query(salary_data1.education, cast(func.count(salary_data1.education), Integer), cast(func.avg(salary_data1.salaryusd), Integer)).\
    #         group_by(salary_data1.education).all()
    #     session.close()

    #     for education, count, salary in visuals_data:
    #         data_list_dict = {}
    #         data_list_dict["education"] = education
    #         data_list_dict["count"] = count
    #         data_list_dict["salary"] = salary
    #         data_list.append(data_list_dict)

    # elif (filter_choice == "comp_education"):
    #     visuals_data = session.query(salary_data1.educationiscomputerrelated, cast(func.count(salary_data1.educationiscomputerrelated), Integer), cast(func.avg(salary_data1.salaryusd), Integer)).\
    #         group_by(salary_data1.educationiscomputerrelated).all()
    #     session.close()

    #     for comp_education, count, salary in visuals_data:
    #         data_list_dict = {}
    #         data_list_dict["is_education_comp_related"] = comp_education
    #         data_list_dict["count"] = count
    #         data_list_dict["salary"] = salary
    #         data_list.append(data_list_dict)

    # elif (filter_choice == "certifications"):
    #     visuals_data = session.query(salary_data1.certifications, cast(func.count(salary_data1.certifications), Integer), cast(func.avg(salary_data1.salaryusd), Integer)).\
    #         group_by(salary_data1.certifications).all()
    #     session.close()

    #     for certifications, count, salary in visuals_data:
    #         data_list_dict = {}
    #         data_list_dict["certifications"] = certifications
    #         data_list_dict["count"] = count
    #         data_list_dict["salary"] = salary
    #         data_list.append(data_list_dict)

    # elif (filter_choice == "country_dataset1"):
    #     visuals_data = session.query(salary_data1.country, cast(func.count(salary_data1.country), Integer), cast(func.avg(salary_data1.salaryusd), Integer)).\
    #         group_by(salary_data1.country).all()
    #     session.close()

    #     for country, count, salary in visuals_data:
    #         data_list_dict = {}
    #         data_list_dict["country"] = country
    #         data_list_dict["count"] = count
    #         data_list_dict["salary"] = salary
    #         data_list.append(data_list_dict)


# # tools of the trade page to render tools.html
# @app.route("/salary_visuals_data/<filter_choice>/<country>")
# def salary_visuals_data_by_country(filter_choice, country):
#     session = Session(engine)

#     data_list = []
#     # query to obtain salaries of each chosen filter
#     if (filter_choice == "job_title_dataset2"):
#         visuals_data = session.query(salary_data2.title, cast(func.count(salary_data2.title), Integer), cast(func.avg(salary_data2.salary), Integer)).\
#             filter(salary_data2.country == country).\
#             group_by(salary_data2.title).all()
#         session.close()

#         # adds data into a dictionary to be jsonified
#         for title, count, salary in visuals_data:
#             data_list_dict = {}
#             data_list_dict["job_title"] = title
#             data_list_dict["count"] = count
#             data_list_dict["salary"] = salary
#             data_list.append(data_list_dict)

#     elif (filter_choice == "gender"):
#         visuals_data = session.query(salary_data2.gender, cast(func.count(salary_data2.gender), Integer), cast(func.avg(salary_data2.salary), Integer)).\
#             filter(salary_data2.country == country).\
#             group_by(salary_data2.gender).all()
#         session.close()

#         for gender, count, salary in visuals_data:
#             data_list_dict = {}
#             data_list_dict["gender"] = gender
#             data_list_dict["count"] = count
#             data_list_dict["salary"] = salary
#             data_list.append(data_list_dict)

#     elif (filter_choice == "education_dataset2"):
#         visuals_data = session.query(salary_data2.education, cast(func.count(salary_data2.education), Integer), cast(func.avg(salary_data2.salary), Integer)).\
#             filter(salary_data2.country == country).\
#             group_by(salary_data2.education).all()
#         session.close()

#         for education, count, salary in visuals_data:
#             data_list_dict = {}
#             data_list_dict["education"] = education
#             data_list_dict["count"] = count
#             data_list_dict["salary"] = salary
#             data_list.append(data_list_dict)

#     elif (filter_choice == "job_title_dataset1"):
#         visuals_data = session.query(salary_data1.jobtitle, cast(func.count(salary_data1.jobtitle), Integer), cast(func.avg(salary_data1.salaryusd), Integer)).\
#             filter(salary_data1.country == country).\
#             group_by(salary_data1.jobtitle).all()
#         session.close()

#         for title, count, salary in visuals_data:
#             data_list_dict = {}
#             data_list_dict["job_title"] = title
#             data_list_dict["count"] = count
#             data_list_dict["salary"] = salary
#             data_list.append(data_list_dict)

#     elif (filter_choice == "education_dataset1"):
#         visuals_data = session.query(salary_data1.education, cast(func.count(salary_data1.education), Integer), cast(func.avg(salary_data1.salaryusd), Integer)).\
#             filter(salary_data1.country == country).\
#             group_by(salary_data1.education).all()
#         session.close()

#         for education, count, salary in visuals_data:
#             data_list_dict = {}
#             data_list_dict["education"] = education
#             data_list_dict["count"] = count
#             data_list_dict["salary"] = salary
#             data_list.append(data_list_dict)

#     elif (filter_choice == "comp_education"):
#         visuals_data = session.query(salary_data1.educationiscomputerrelated, cast(func.count(salary_data1.educationiscomputerrelated), Integer), cast(func.avg(salary_data1.salaryusd), Integer)).\
#             filter(salary_data1.country == country).\
#             group_by(salary_data1.educationiscomputerrelated).all()
#         session.close()

#         for comp_education, count, salary in visuals_data:
#             data_list_dict = {}
#             data_list_dict["is_education_comp_related"] = comp_education
#             data_list_dict["count"] = count
#             data_list_dict["salary"] = salary
#             data_list.append(data_list_dict)

#     elif (filter_choice == "certifications"):
#         visuals_data = session.query(salary_data1.certifications, cast(func.count(salary_data1.certifications), Integer), cast(func.avg(salary_data1.salaryusd), Integer)).\
#             filter(salary_data1.country == country).\
#             group_by(salary_data1.certifications).all()
#         session.close()

#         for certifications, count, salary in visuals_data:
#             data_list_dict = {}
#             data_list_dict["certifications"] = certifications
#             data_list_dict["count"] = count
#             data_list_dict["salary"] = salary
#             data_list.append(data_list_dict)

#     return jsonify(data_list)


# # api route to obtain the name data from salary_data1
# @app.route("/salary_data1/<title>")
# def all_salary_data1(title):
#     session = Session(engine)

#     all_data = session.query(salary_data1.salaryusd, salary_data1.primarydatabase,\
#         cast(salary_data1.yearswiththisdatabase, Integer), salary_data1.employmentstatus,\
#         salary_data1.jobtitle, salary_data1.managestaff, cast(salary_data1.yearswiththistypeofjob, Integer),\
#         salary_data1.otherpeopleonyourteam, salary_data1.databaseservers,\
#         salary_data1.education, salary_data1.educationiscomputerrelated,\
#         salary_data1.certifications, salary_data1.hoursworkedperweek, salary_data1.telecommutedaysperweek,\
#         salary_data1.employmentsector, salary_data1.region).\
#         filter(salary_data1.jobtitle == title).all()
#     session.close()

#     # adds data into a dictionary to be jsonified
#     data_list = []
#     for salary, database, years_database, status, title, manager, years_job, team, servers, education, education_comp, certs, hours, telecommute, sector, region in all_data:
#         data_list_dict = {}
#         data_list_dict["salary"] = salary
#         data_list_dict["primary_database"] = database
#         data_list_dict["years_with_this_database"] = years_database
#         data_list_dict["employment_status"] = status
#         data_list_dict["job_title"] = title
#         data_list_dict["manager"] = manager
#         data_list_dict["years_with_this_type_of_job"] = years_job
#         data_list_dict["other_people_on_your_team"] = team
#         data_list_dict["database_servers"] = servers
#         data_list_dict["education"] = education
#         data_list_dict["education_is_computer_related"] = education_comp
#         data_list_dict["certifications"] = certs
#         data_list_dict["years_with_this_type_of_job"] = hours
#         data_list_dict["telecommute_days_per_week"] = telecommute
#         data_list_dict["employment_sector"] = sector
#         data_list_dict["region"] = region
#         data_list.append(data_list_dict)

#     return jsonify(data_list)


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
        print(years_db, years_job, country, region, comp_ed, primary_db, employ_sector, telecommute, manager, title)

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

        prediction_rounded  = round(prediction_untransformed[0], 2)
        prediction_formatted = "{:,.2f}".format(prediction_rounded)
        prediction_string = f'Predicted Salary: ${prediction_formatted}'
        print("PREDICTION")
        print(prediction_string)

        return render_template('predictions.html', salary_prediction=prediction_string)

    else:
        return render_template("predictions.html")

if __name__ == "__main__":
    app.run(debug=True)
