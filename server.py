from flask import Flask, render_template, url_for, render_template_string, send_from_directory, abort, session, request, redirect, jsonify
import data_managers


app = Flask(__name__, static_url_path='')
data = data_managers.JSON()
app.secret_key = data.secrty_key


# View Routes

@app.route("/")
def homeRoute():
    top_articles = data.getArticlesByViews('home')
    recent_articles = data.getArticlesByDate('home', 5)
    return render_template('home.html', top_articles=top_articles, recent_articles=recent_articles)

@app.route("/projects")
def projectsRoute():
    return getSub('projects', "Projects")

@app.route("/projects/<article>")
def projectsPageRoute(article):
    return getArticle('projects', article)

@app.route("/blog")
def blogRoute():
    return getSub('blog', "Blog")

@app.route("/blog/<article>")
def blogPageRoute(article):
    return getArticle('blog', article)

@app.route("/apps")
def appsRoute():
    return getSub('apps', "Apps")

@app.route("/apps/<article>")
def appsPageRoute(article):
    return getArticle('apps', article)

@app.route("/youtube")
def youtubeRoute():
    return getSub('youtube', "YouTube")

@app.route("/youtube/<article>")
def youtubePageRoute(article):
    return getArticle('youtube', article)

@app.route("/tools")
def toolsRoute():
    return getSub('tools', "Tools")

@app.route("/tools/<article>")
def toolsPageRoute(article):
    return getArticle('tools', article)

@app.route("/stats")
def statsRoute():
    total_views = data.getTotalViews()
    number_of_articles = data.getArticleCount()

    last_20_day_labels = data.getLast20DayLabels()
    last_20_day_data = data.getLast20DayData()
    prev_20_day_data = data.getPrev20DayData()

    hourly_data = data.getHourlyData()

    return render_template('stats.html',
                           total_views=str(total_views),
                           number_of_articles=str(number_of_articles),
                           last_20_day_labels=str(last_20_day_labels),
                           last_20_day_data=str(last_20_day_data),
                           prev_20_day_data=str(prev_20_day_data),
                           hourly_data=str(hourly_data))

@app.route("/admin", methods=['GET', 'POST'])
def adminRoute():
    if request.method == 'GET':
        if 'logged_in' in session and session['logged_in']:
            return render_template('admin.html')
        else:
            return render_template('login.html')
    else:
        if request.json['username'] == data.username and request.json['password'] == data.password:
            session['logged_in'] = True
            return jsonify({'success' : True})
        return jsonify({'success' : False})


# Work Routes

@app.route("/admin/logout")
def adminLogoutRoute():
    session['logged_in'] = False
    return jsonify({'success' : True})

@app.route("/admin/push_json")
def adminPushJsonRoute():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'success': False})

    return jsonify({'success': True})

@app.route("/admin/download_json")
def adminDownloadJsonRoute():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'success': False})

    return jsonify({'success': True})

@app.route("/admin/rescrape")
def adminRescrapeRoute():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'success': False})

    return jsonify({'success': True})

@app.route("/admin/download_stats")
def adminDownloadStatsRoute():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'success': False})

    return jsonify({'success': True})

@app.route("/admin/delete_article")
def adminDeleteArticleRoute():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'success': False})

    return jsonify({'success': True})

@app.route("/admin/create_article")
def adminCreateArticleRoute():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'success': False})

    return jsonify({'success': True})

@app.route("/admin/download_article")
def adminDownloadArticleRoute():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'success': False})

    return jsonify({'success': True})

@app.route("/non-static/<sub>/<article>/<img>")
def articleImageServing(sub, article, img):
    return send_from_directory(data.article_location + sub + "/" + article + "/", img)


# Recurring code

def getSub(sub, title):
    top_articles = data.getArticlesByViews(sub)
    recent_articles = data.getArticlesByDate(sub)
    return render_template('sub.html',
                           title=title,
                           display_icon=url_for('static', filename='img/' + sub + '-icon.svg'),
                           top_articles=top_articles,
                           recent_articles=recent_articles)

def getArticle(sub, article):
    if not data.articleExists(sub, article):
        abort(404)

    with open('articles/' + sub + '/' + article + '/view.html', 'r') as f:
        html = f.read()

    data.articleView(sub, article)
    return render_template_string(html, title=data.getArticleTitle(sub, article))


# For testing

@app.route("/json")
def jsonRoute():
    return str(data.data)

import os
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == '__main__':
    import socket
    ip = socket.gethostbyname(socket.gethostname())
    port = 8080
    print("Site starting on http://" + ip + ":" + str(port))
    app.run(debug=True, host=ip, port=port)
