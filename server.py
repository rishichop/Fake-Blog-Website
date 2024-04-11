from flask import Flask, render_template, request
import requests
import smtplib

app = Flask(__name__)
BLOG_API = "https://api.npoint.io/674f5423f73deab1e9a7"
EMAIL = "chopaderishikesh@gmail.com"
PASS = ""


class Post:
    def __init__(self, post_id, title, subtitle, body, image_url):
        self.post_id = post_id
        self.title = title
        self.subtitle = subtitle
        self.body = body
        self.image_url = image_url


DATA = requests.get(url=BLOG_API).json()
POST_OBJS = []
for post in DATA:
    post_obj = Post(post_id=post["id"],
                    title=post["title"],
                    subtitle=post["subtitle"],
                    body=post["body"],
                    image_url=post["image_url"])
    POST_OBJS.append(post_obj)


@app.route('/')
def home():
    return render_template(template_name_or_list="index.html", posts=POST_OBJS)


@app.route('/about')
def about():
    return render_template(template_name_or_list="about.html")


@app.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        # print(request.form["name"])
        # print(request.form["email"])
        # print(request.form["phone"])
        # print(request.form["msg"])
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["msg"])
        return render_template(template_name_or_list="contact.html", msg_sent=True)
    else:
        return render_template(template_name_or_list="contact.html", msg_sent=False)


@app.route('/post/<int:p_id>')
def view_post(p_id):
    for post in POST_OBJS:
        if post.post_id == p_id:
            return render_template(template_name_or_list="post.html", post=post)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(EMAIL, PASS)
        connection.sendmail(EMAIL, PASS, email_message)


if __name__ == "__main__":
    app.run(debug=True)
