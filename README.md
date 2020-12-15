# This is my server! It's not much, but it's mine.  
It runs on flask. It's kinda messy! This is one project I'm working on strictly for results - I just want to post stuff as easily as possible, with as little hassle as possible (but avoiding having to use PHP). There might be some slightly-more-complicated stuff in here using blueprints or subapplications, so that I can extend things! It's not done, though.

Poke. Poke.

I made a service file for use with systemd finally! It'll make it so that it'll automatically start when the server starts. That lives in `auriga.service`. It also has the `gunicorn` command for starting the server. I've removed the old hacky start script that kept it; if you want to run it locally, you should be able to just run `pure_flask.py`. If you need to run it manually, just copy and paste it from `auriga.service`. But don't do that. Just use `systemd`.
