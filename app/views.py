'''
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
'''
import os
from app import app
from app import db
from app.models import user_profile
from flask import render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import time
import random

###
# Routing for your application.
###

@app.route('/')
def home():
    '''Render website's home page.'''
    return render_template('home.html')

@app.route('/about/')
def about():
    '''Render the website's about page.'''
    return render_template('about.html', name = "INFO3180 Project 1")

@app.route('/profile', methods=['POST','GET'])
def profile():
    if request.method == 'POST':
        userid = random.randint(1000000, 1009999)
        username = request.form['username']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        age = request.form['age']
        bio = request.form['bio']
        gender = request.form['gender']
        #Picture handler
        pro_pic = request.files['pro_pic']
        file_folder = app.config['UPLOAD_FOLDER']
        filename = secure_filename(pro_pic.filename)
        pro_pic.save(os.path.join(file_folder, filename))
        ###
        date_created = time.strftime('%m %d %Y')
        
        user = user_profile(userid=userid,username=username,firstname=firstname,lastname=lastname,age=age,bio=bio,gender=gender,date_created=date_created,pro_pic=pro_pic.filename)
        db.session.add(user)
        db.session.commit()

        flash('Profile for '+ username +' added','success')
        return redirect(url_for('home'))
    return render_template('add_profile.html')

@app.route("/profiles", methods=['POST','GET'])
def listprofiles():
    profiles = db.session.query(user_profile).all()
    if request.headers['Content-Type']=='application/json' or request.method == "POST":
        userlist = []
        for profile in profiles:
            userlist.append({'userid':profile.userid, 'username':profile.username})
            profiles = {'Users':userlist}
        return jsonify(profiles)
    elif request.method == 'GET':
        return render_template('listprofile.html',profiles=profiles)


@app.route("/profile/<userid>", methods=['POST','GET'])
def viewprofile(userid):
    print userid
    profile = db.session.query(user_profile).filter_by(userid=userid).first()

    if request.headers['Content-Type']=='application/json' or request.method == "POST":
        return jsonify(userid=profile.userid, username=profile.username, profile_image=profile.pro_pic, gender=profile.gender, age=profile.age, profile_created_on=profile.date_created)
    else:
        return render_template('viewprofile.html', profile=profile)


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    '''Send your static text file.'''
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

@app.after_request
def add_header(response):
    '''
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    '''
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response

@app.errorhandler(404)
def page_not_found(error):
    '''Custom 404 page.'''
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port='8080')