# BrainyBoard Chatbot
BrainyBoard Chatbot is a chatbot that is connected to Trello, Slack, and OpenAI to help users manage their tickets. The chatbot allows users to view their assigned tickets using a simple and intuitive chat interface.

## Features
- *Ticket listing:* Users can view a list of their assigned tickets for a particular Trello board using the chatbot interface. e.g: `/tickets <listName>`

- *Board listing:* Users can fetch Trello boards to view their tickets from. e.g: `/get-lists`

- *Integration with Trello and Slack:* The chatbot integrates with Trello and Slack, allowing users to view their tickets within these platforms.

- *Guidance commands:* The chatbot provides users with a list of available commands to guide them through the ticket management process. e.g: `/guidance <ticketName>`

## Installation
To install BrainyBoard Chatbot, simply clone this repository to your local machine:
`git clone https://github.com/amLiux/BrainyBoard.git`

Then, navigate to the `BrainyBoard` directory and run the following command to install the necessary dependencies:
`pip install -r requirements.txt`


## Usage
Before starting the chatbot, make sure to create a `.env` file by copying the `env.sample` file and filling in the appropriate values:

`cp env.sample .env`

The `.env` file contains environment variables that are necessary for the chatbot to function properly. Here are the environment variables that need to be filled in:

```bash
slack_token=<your_slack_bot_token>
signing_secret=<your_slack_signing_secret>
trello_token=<your_trello_token>
trello_api_key=<your_trello_api_key>
board_id=<your_trello_board_id>
slack_endpoint=<your_slack_endpoint>
destination_language=<your_destination_language>
openai_api_key=<your_openai_api_key>
```

- `slack_token`: The Slack bot token that you received when you created your bot. You can find this token in the "OAuth & Permissions" page of your Slack app settings.
- `signing_secret`: The signing secret that you received when you created your Slack app. You can find this secret in the "Basic Information" page of your Slack app settings.
- `trello_token`: The Trello API token that you obtained by following the Trello API documentation.
- `trello_api_key`: The Trello API key that you obtained by following the Trello API documentation.
- `board_id`: The ID of the Trello board that you want to use for ticket management.
- `slack_endpoint`: The endpoint of your Slack app. This value should be `slack/events`.
- `destination_language`: The destination language for translation. You can choose any language supported by the Google Cloud Translate API.
- `openai_api_key`: The OpenAI API key that you obtained by following the OpenAI API documentation.

To start the chatbot, run the following command in the `BrainyBoard` directory:
`python bot.py`


## Contributing
If you'd like to contribute to BrainyBoard Chatbot, please fork this repository and submit a pull request. We welcome contributions of all kinds, including bug reports, feature requests, and code contributions.

## License
BrainyBoard Chatbot is released under the [MIT License](https://github.com/amLiux/BrainyBoard/blob/main/LICENSE).

## Credits
BrainyBoard Chatbot was created by [amLiux](https://github.com/amLiux).

## Contact
If you have any questions or comments about BrainyBoard Chatbot, please feel free to contact us at marceliux@jardinbinario.com

