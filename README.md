# dinnerbot for Slack

Testing the python client for slack to create a simple bot.

Based on the tutorial at [Full Stack Python](https://www.fullstackpython.com/blog/build-first-slack-bot-python.html)

To-do
- [x] Handle DMs and @ messages
- [x] Place search with google places API
- [ ] Location search with google maps API
- [ ] Save user suggestions using firebase
- [ ] Incorporate user suggestions into search results
- [ ] Conversational dialog handler
- [ ] Logging messages

Want to run locally?

- Create a python environment (conda or virtualenv) with slackclient, python-dotenv and requests installed (you can use the `environment.yml` in the project directory for conda)
- Create a `.env` file in the project folder with the structure:
    ```shell    
    SLACK_BOT_TOKEN=<YOUR SLACK BOT TOKEN>
    BOT_ID=<YOUR SLACK BOT ID>
    GOOGLE_KEY=<YOUR GOOGLE PLACES API KEY>
    ```
- Run with
    ```shell
    $ python dinnerbot.py
    ```
