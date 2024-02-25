@app.route("/success", methods=["POST"])
def success():
    if request.method == "POST":
        f = fname()
        # f = request.files['file']
        f.save(os.path.join('uploads', f.filename))
        # run autotune main function
        main_at(os.path.join('uploads', f.filename))
        # remove audio after get the optput.wav
        os.remove(os.path.join('uploads', f.filename))
        return render_template("output.html", name=f.filename)