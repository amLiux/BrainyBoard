class WelcomeMessage:
    def __init__(self, translation_provider, channel, user, channel_description):
        self.channel = channel
        self.user = user
        self.icon_emoji = ':robot_face:'
        self.timestampp = ''
        self.completed = False
        self.translation_provider=translation_provider
        self.channel_description=channel_description
        self.START_TEXT = {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': self.translation_provider.translate('WELCOME_MESSAGE').replace('{change_channel}', f'#{self.channel}')
            }
        }

        self.DIVIDER = {'type': 'divider'}
    
    def get_message(self):
        return {
            'ts': self.timestampp,
            'channel': f'@{self.user}',
            'username': 'Welcome BrainyBoard!',
            'icon_emoji': self.icon_emoji,
            'blocks': [
                self.START_TEXT,
                self.DIVIDER,
                self._get_reaction_task()
            ]
        }
    
    def _get_reaction_task(self):
        checkmark = ':white_check_mark'
        if not self.completed:
            checkmark = ':white_large_square:'
        react_message = self.translation_provider.translate('REACT_MESSAGE')
        return {'type': 'section', 'text': {'type': 'mrkdwn', 'text': f'{checkmark} *{react_message}* \n{self.channel_description}'}}