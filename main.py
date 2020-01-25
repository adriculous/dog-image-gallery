from flask import Flask, render_template, request

import requests

#imports a dictionary of data from dog_breeds.py and "prettifies", or styles, the dog names when they appear in the HTML page
from dog_breeds import prettify_dog_breed

app = Flask("app")

#function adds a dash in the URL between breed names with multiple words like miniature poodle
def check_breed(breed):
  return "/".join(breed.split("-"))

@app.route("/", methods=["GET","POST"])
def dog_image_gallery():
  errors = []
  if request.method == "POST":
    breed = request.form.get("breed")
    number = request.form.get("number")
    if not breed:
      errors.append("Oops! Please choose a breed.")
    if not number:
      errors.append("Oops! Please choose a number.")
    if breed and number:
      response = requests.get("https://dog.ceo/api/breed/" + check_breed(breed) + "/images/random/" + number)
    data = response.json()
    dog_images = data["message"]
    return render_template("dogs.html", images=dog_images, breed=prettify_dog_breed(breed), errors=[])
  return render_template("dogs.html", images=[], breed="", errors=errors)

@app.route("/random", methods=["POST"])
def get_random():
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    data = response.json()
    dog_images = [data["message"]]
    return render_template("dogs.html", images=dog_images)

app.debug = True
app.run(host='0.0.0.0', port=8080)