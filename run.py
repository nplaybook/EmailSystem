from app import app, scheduler


if __name__ == "__main__":
    scheduler.start()
    app.run(debug=True)