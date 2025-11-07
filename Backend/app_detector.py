"""Application detection based on domain patterns and ports"""

# Domain pattern to application mapping (ordered by priority)
# Keywords are checked against DNS queries and SNI fields
DOMAIN_PATTERNS = {
    # ============ SOCIAL MEDIA (50+ patterns) ============
    'facebook': {'app': 'Facebook', 'category': 'Social Media'},
    'fbcdn': {'app': 'Facebook', 'category': 'Social Media'},
    'fbstatic': {'app': 'Facebook', 'category': 'Social Media'},
    'instagram': {'app': 'Instagram', 'category': 'Social Media'},
    'cdninstagram': {'app': 'Instagram', 'category': 'Social Media'},
    'instaproxy': {'app': 'Instagram', 'category': 'Social Media'},
    'whatsapp': {'app': 'WhatsApp', 'category': 'Messaging'},
    'whatsapp-cdn': {'app': 'WhatsApp', 'category': 'Messaging'},
    'wa.me': {'app': 'WhatsApp', 'category': 'Messaging'},
    'twitter': {'app': 'Twitter/X', 'category': 'Social Media'},
    'twimg': {'app': 'Twitter/X', 'category': 'Social Media'},
    'twttr': {'app': 'Twitter/X', 'category': 'Social Media'},
    'twitter-cdn': {'app': 'Twitter/X', 'category': 'Social Media'},
    'x.com': {'app': 'Twitter/X', 'category': 'Social Media'},
    'linkedin': {'app': 'LinkedIn', 'category': 'Professional'},
    'licdn': {'app': 'LinkedIn', 'category': 'Professional'},
    'reddit': {'app': 'Reddit', 'category': 'Social Media'},
    'redd.it': {'app': 'Reddit', 'category': 'Social Media'},
    'redditstatic': {'app': 'Reddit', 'category': 'Social Media'},
    'snapchat': {'app': 'Snapchat', 'category': 'Social Media'},
    'snapchatcdn': {'app': 'Snapchat', 'category': 'Social Media'},
    'tiktok': {'app': 'TikTok', 'category': 'Social Media'},
    'musicallyapp': {'app': 'TikTok', 'category': 'Social Media'},
    'tiktok-cdn': {'app': 'TikTok', 'category': 'Social Media'},
    'douyin': {'app': 'Douyin (TikTok CN)', 'category': 'Social Media'},
    'pinterest': {'app': 'Pinterest', 'category': 'Social Media'},
    'pinimg': {'app': 'Pinterest', 'category': 'Social Media'},
    'tumblr': {'app': 'Tumblr', 'category': 'Social Media'},
    'tumblrcdn': {'app': 'Tumblr', 'category': 'Social Media'},
    'nextdoor': {'app': 'Nextdoor', 'category': 'Social Media'},
    'quora': {'app': 'Quora', 'category': 'Social Media'},
    'medium': {'app': 'Medium', 'category': 'Social Media'},
    'steemit': {'app': 'Steemit', 'category': 'Social Media'},
    'mastodon': {'app': 'Mastodon', 'category': 'Social Media'},
    'bluesky': {'app': 'Bluesky', 'category': 'Social Media'},
    'threads': {'app': 'Threads', 'category': 'Social Media'},
    'bereal': {'app': 'BeReal', 'category': 'Social Media'},
    'vsco': {'app': 'VSCO', 'category': 'Social Media'},
    'weibo': {'app': 'Weibo', 'category': 'Social Media'},
    'xiaohongshu': {'app': 'Little Red Book', 'category': 'Social Media'},
    'kuaishou': {'app': 'Kuaishou', 'category': 'Social Media'},
    'qq.com': {'app': 'QQ', 'category': 'Social Media'},
    'renren': {'app': 'Renren', 'category': 'Social Media'},
    'momo': {'app': 'Momo', 'category': 'Social Media'},

    # ============ VIDEO STREAMING (60+ patterns) ============
    'youtube': {'app': 'YouTube', 'category': 'Video'},
    'googlevideo': {'app': 'YouTube', 'category': 'Video'},
    'ytimg': {'app': 'YouTube', 'category': 'Video'},
    'youtube-cdn': {'app': 'YouTube', 'category': 'Video'},
    'youtu.be': {'app': 'YouTube', 'category': 'Video'},
    'netflix': {'app': 'Netflix', 'category': 'Video'},
    'nflxvideo': {'app': 'Netflix', 'category': 'Video'},
    'netflixcdn': {'app': 'Netflix', 'category': 'Video'},
    'nflximg': {'app': 'Netflix', 'category': 'Video'},
    'primevideo': {'app': 'Amazon Prime', 'category': 'Video'},
    'amazonvideo': {'app': 'Amazon Prime', 'category': 'Video'},
    'atv-ps': {'app': 'Amazon Prime', 'category': 'Video'},
    'hotstar': {'app': 'Disney+ Hotstar', 'category': 'Video'},
    'hotstarcdn': {'app': 'Disney+ Hotstar', 'category': 'Video'},
    'disneyplus': {'app': 'Disney+', 'category': 'Video'},
    'disneycdn': {'app': 'Disney+', 'category': 'Video'},
    'twitch': {'app': 'Twitch', 'category': 'Video'},
    'twitchcdn': {'app': 'Twitch', 'category': 'Video'},
    'hulu': {'app': 'Hulu', 'category': 'Video'},
    'hulucdn': {'app': 'Hulu', 'category': 'Video'},
    'hbo': {'app': 'HBO Max', 'category': 'Video'},
    'hbomax': {'app': 'HBO Max', 'category': 'Video'},
    'peacocktv': {'app': 'Peacock TV', 'category': 'Video'},
    'paramountplus': {'app': 'Paramount+', 'category': 'Video'},
    'appletv': {'app': 'Apple TV+', 'category': 'Video'},
    'vimeo': {'app': 'Vimeo', 'category': 'Video'},
    'vimeocdn': {'app': 'Vimeo', 'category': 'Video'},
    'dailymotion': {'app': 'Dailymotion', 'category': 'Video'},
    'rumble': {'app': 'Rumble', 'category': 'Video'},
    'odysee': {'app': 'Odysee', 'category': 'Video'},
    'bitchute': {'app': 'BitChute', 'category': 'Video'},
    'brighteon': {'app': 'Brighteon', 'category': 'Video'},
    'vk.com': {'app': 'VKontakte Video', 'category': 'Video'},
    'ok.ru': {'app': 'Odnoklassniki', 'category': 'Video'},
    'rutube': {'app': 'RuTube', 'category': 'Video'},
    'livejournal': {'app': 'LiveJournal', 'category': 'Video'},
    'youku': {'app': 'Youku', 'category': 'Video'},
    'iqiyi': {'app': 'iQIYI', 'category': 'Video'},
    'bilibili': {'app': 'Bilibili', 'category': 'Video'},
    'sohu': {'app': 'Sohu Video', 'category': 'Video'},
    'qq.video': {'app': 'Tencent Video', 'category': 'Video'},
    'mgtv': {'app': 'Mango TV', 'category': 'Video'},
    'le.com': {'app': 'LeEco', 'category': 'Video'},
    'vlive': {'app': 'V Live', 'category': 'Video'},
    'wavve': {'app': 'Wavve', 'category': 'Video'},
    'tving': {'app': 'TVING', 'category': 'Video'},
    'watcha': {'app': 'Watcha', 'category': 'Video'},
    'cinemax': {'app': 'Cinemax', 'category': 'Video'},
    'showtime': {'app': 'Showtime', 'category': 'Video'},

    # ============ COMMUNICATION & MESSAGING (50+ patterns) ============
    'zoom': {'app': 'Zoom', 'category': 'Video Call'},
    'zoomcdn': {'app': 'Zoom', 'category': 'Video Call'},
    'teams.microsoft': {'app': 'Microsoft Teams', 'category': 'Video Call'},
    'teams.cdn': {'app': 'Microsoft Teams', 'category': 'Video Call'},
    'meet.google': {'app': 'Google Meet', 'category': 'Video Call'},
    'discord': {'app': 'Discord', 'category': 'Messaging'},
    'discordapp': {'app': 'Discord', 'category': 'Messaging'},
    'discordcdn': {'app': 'Discord', 'category': 'Messaging'},
    'telegram': {'app': 'Telegram', 'category': 'Messaging'},
    't.me': {'app': 'Telegram', 'category': 'Messaging'},
    'slack': {'app': 'Slack', 'category': 'Messaging'},
    'slackb': {'app': 'Slack', 'category': 'Messaging'},
    'skype': {'app': 'Skype', 'category': 'Video Call'},
    'skypeassets': {'app': 'Skype', 'category': 'Video Call'},
    'webex': {'app': 'Webex', 'category': 'Video Call'},
    'webexcdn': {'app': 'Webex', 'category': 'Video Call'},
    'jitsi': {'app': 'Jitsi Meet', 'category': 'Video Call'},
    'whereby': {'app': 'Whereby', 'category': 'Video Call'},
    'whereby.com': {'app': 'Whereby', 'category': 'Video Call'},
    'signal': {'app': 'Signal', 'category': 'Messaging'},
    'signalcdn': {'app': 'Signal', 'category': 'Messaging'},
    'viber': {'app': 'Viber', 'category': 'Messaging'},
    'vibercdn': {'app': 'Viber', 'category': 'Messaging'},
    'line': {'app': 'LINE', 'category': 'Messaging'},
    'wechat': {'app': 'WeChat', 'category': 'Messaging'},
    'weixin': {'app': 'WeChat', 'category': 'Messaging'},
    'qqim': {'app': 'QQ', 'category': 'Messaging'},
    'wire': {'app': 'Wire', 'category': 'Messaging'},
    'threema': {'app': 'Threema', 'category': 'Messaging'},
    'session': {'app': 'Session', 'category': 'Messaging'},
    'briar': {'app': 'Briar', 'category': 'Messaging'},
    'matrix': {'app': 'Matrix', 'category': 'Messaging'},
    'element': {'app': 'Element', 'category': 'Messaging'},
    'rocket.chat': {'app': 'Rocket.Chat', 'category': 'Messaging'},
    'mattermost': {'app': 'Mattermost', 'category': 'Messaging'},
    'keybase': {'app': 'Keybase', 'category': 'Messaging'},

    # ============ GAMING (80+ patterns) ============
    'steampowered': {'app': 'Steam', 'category': 'Gaming'},
    'steamcdn': {'app': 'Steam', 'category': 'Gaming'},
    'steamstatic': {'app': 'Steam', 'category': 'Gaming'},
    'epicgames': {'app': 'Epic Games', 'category': 'Gaming'},
    'epiccdn': {'app': 'Epic Games', 'category': 'Gaming'},
    'riotgames': {'app': 'Riot Games', 'category': 'Gaming'},
    'lol': {'app': 'League of Legends', 'category': 'Gaming'},
    'valorant': {'app': 'Valorant', 'category': 'Gaming'},
    'ea.com': {'app': 'EA Games', 'category': 'Gaming'},
    'eacdn': {'app': 'EA Games', 'category': 'Gaming'},
    'origin': {'app': 'Origin', 'category': 'Gaming'},
    'playstation': {'app': 'PlayStation', 'category': 'Gaming'},
    'psn': {'app': 'PlayStation Network', 'category': 'Gaming'},
    'xbox': {'app': 'Xbox', 'category': 'Gaming'},
    'xboxlive': {'app': 'Xbox Live', 'category': 'Gaming'},
    'blizzard': {'app': 'Blizzard', 'category': 'Gaming'},
    'battle.net': {'app': 'Battle.net', 'category': 'Gaming'},
    'worldofwarcraft': {'app': 'World of Warcraft', 'category': 'Gaming'},
    'diablo': {'app': 'Diablo', 'category': 'Gaming'},
    'overwatch': {'app': 'Overwatch', 'category': 'Gaming'},
    'hearthstone': {'app': 'Hearthstone', 'category': 'Gaming'},
    'ubi': {'app': 'Ubisoft', 'category': 'Gaming'},
    'ubisoft': {'app': 'Ubisoft', 'category': 'Gaming'},
    'ubisoftcdn': {'app': 'Ubisoft', 'category': 'Gaming'},
    'activision': {'app': 'Activision', 'category': 'Gaming'},
    'bethesda': {'app': 'Bethesda', 'category': 'Gaming'},
    'elderscrolls': {'app': 'Elder Scrolls', 'category': 'Gaming'},
    'fallout': {'app': 'Fallout', 'category': 'Gaming'},
    'mojang': {'app': 'Minecraft', 'category': 'Gaming'},
    'minecraft': {'app': 'Minecraft', 'category': 'Gaming'},
    'roblox': {'app': 'Roblox', 'category': 'Gaming'},
    'robloxcdn': {'app': 'Roblox', 'category': 'Gaming'},
    'fortnite': {'app': 'Fortnite', 'category': 'Gaming'},
    'pubg': {'app': 'PUBG', 'category': 'Gaming'},
    'apex': {'app': 'Apex Legends', 'category': 'Gaming'},
    'csgo': {'app': 'CS:GO', 'category': 'Gaming'},
    'counter-strike': {'app': 'Counter-Strike', 'category': 'Gaming'},
    'dota': {'app': 'Dota 2', 'category': 'Gaming'},
    'gta': {'app': 'GTA Online', 'category': 'Gaming'},
    'rockstargames': {'app': 'Rockstar Games', 'category': 'Gaming'},
    'supercell': {'app': 'Supercell', 'category': 'Gaming'},
    'clash': {'app': 'Clash of Clans', 'category': 'Gaming'},
    'clashroyal': {'app': 'Clash Royale', 'category': 'Gaming'},
    'brawlstars': {'app': 'Brawl Stars', 'category': 'Gaming'},
    'pokemongo': {'app': 'Pokémon GO', 'category': 'Gaming'},
    'niantic': {'app': 'Niantic', 'category': 'Gaming'},
    'zynga': {'app': 'Zynga', 'category': 'Gaming'},
    'kingcdn': {'app': 'King', 'category': 'Gaming'},
    'playrix': {'app': 'Playrix', 'category': 'Gaming'},
    'scopely': {'app': 'Scopely', 'category': 'Gaming'},
    'glu': {'app': 'Glu Mobile', 'category': 'Gaming'},
    'netease': {'app': 'NetEase Games', 'category': 'Gaming'},
    'tencent': {'app': 'Tencent Games', 'category': 'Gaming'},
    'mihoyo': {'app': 'MiHoYo', 'category': 'Gaming'},
    'genshin': {'app': 'Genshin Impact', 'category': 'Gaming'},
    'honkai': {'app': 'Honkai: Star Rail', 'category': 'Gaming'},
    'nexon': {'app': 'Nexon', 'category': 'Gaming'},
    'ncsoft': {'app': 'NCSoft', 'category': 'Gaming'},
    'bandainamco': {'app': 'Bandai Namco', 'category': 'Gaming'},

    # ============ CLOUD & SERVICES (80+ patterns) ============
    'googleapis': {'app': 'Google Services', 'category': 'Cloud'},
    'google': {'app': 'Google', 'category': 'Search'},
    'googlesyndication': {'app': 'Google Ads', 'category': 'Advertising'},
    'gstatic': {'app': 'Google Static', 'category': 'CDN'},
    'googleusercontent': {'app': 'Google', 'category': 'Cloud'},
    'doubleclick': {'app': 'DoubleClick', 'category': 'Advertising'},
    'googleadservices': {'app': 'Google Ads', 'category': 'Advertising'},
    'googleapis.com': {'app': 'Google APIs', 'category': 'Cloud'},
    'amazonaws': {'app': 'AWS', 'category': 'Cloud'},
    'awscdn': {'app': 'AWS CDN', 'category': 'CDN'},
    'cloudfront': {'app': 'CloudFront', 'category': 'CDN'},
    'cloudflare': {'app': 'Cloudflare', 'category': 'CDN'},
    'cdnjs': {'app': 'Cloudflare CDNJS', 'category': 'CDN'},
    'akamai': {'app': 'Akamai CDN', 'category': 'CDN'},
    'microsoft': {'app': 'Microsoft', 'category': 'Cloud'},
    'apple': {'app': 'Apple Services', 'category': 'Cloud'},
    'icloud': {'app': 'iCloud', 'category': 'Cloud'},
    'icloudcdn': {'app': 'iCloud', 'category': 'Cloud'},
    'dropbox': {'app': 'Dropbox', 'category': 'Cloud'},
    'dropboxcdn': {'app': 'Dropbox', 'category': 'Cloud'},
    'office.com': {'app': 'Microsoft 365', 'category': 'Cloud'},
    'office365': {'app': 'Microsoft 365', 'category': 'Cloud'},
    'sharepoint': {'app': 'SharePoint', 'category': 'Cloud'},
    'live.com': {'app': 'Microsoft Live', 'category': 'Cloud'},
    'msftauth': {'app': 'Microsoft Auth', 'category': 'Cloud'},
    'gcp': {'app': 'Google Cloud', 'category': 'Cloud'},
    'azurecdn': {'app': 'Microsoft Azure', 'category': 'Cloud'},
    'fastly': {'app': 'Fastly CDN', 'category': 'CDN'},
    'limelight': {'app': 'Limelight CDN', 'category': 'CDN'},
    'edgecast': {'app': 'Edgecast CDN', 'category': 'CDN'},
    'maxcdn': {'app': 'MaxCDN', 'category': 'CDN'},
    'stackpath': {'app': 'StackPath', 'category': 'CDN'},
    'bunnycdn': {'app': 'BunnyCDN', 'category': 'CDN'},
    'digitalocean': {'app': 'DigitalOcean', 'category': 'Cloud'},
    'heroku': {'app': 'Heroku', 'category': 'Cloud'},
    'railway': {'app': 'Railway', 'category': 'Cloud'},
    'render': {'app': 'Render', 'category': 'Cloud'},
    'vercel': {'app': 'Vercel', 'category': 'Cloud'},
    'netlify': {'app': 'Netlify', 'category': 'Cloud'},
    'github': {'app': 'GitHub', 'category': 'Development'},
    'githubassets': {'app': 'GitHub', 'category': 'Development'},
    'githubusercontent': {'app': 'GitHub', 'category': 'Development'},
    'gitlab': {'app': 'GitLab', 'category': 'Development'},
    'gitlabcdn': {'app': 'GitLab', 'category': 'Development'},
    'bitbucket': {'app': 'Bitbucket', 'category': 'Development'},
    'gitea': {'app': 'Gitea', 'category': 'Development'},

    # ============ MUSIC & AUDIO (40+ patterns) ============
    'spotify': {'app': 'Spotify', 'category': 'Music'},
    'scdn': {'app': 'Spotify', 'category': 'Music'},
    'spotifycdn': {'app': 'Spotify', 'category': 'Music'},
    'pandora': {'app': 'Pandora', 'category': 'Music'},
    'apple-music': {'app': 'Apple Music', 'category': 'Music'},
    'applemusic': {'app': 'Apple Music', 'category': 'Music'},
    'music.apple': {'app': 'Apple Music', 'category': 'Music'},
    'amazonmusic': {'app': 'Amazon Music', 'category': 'Music'},
    'tidal': {'app': 'Tidal', 'category': 'Music'},
    'tidalmusic': {'app': 'Tidal', 'category': 'Music'},
    'soundcloud': {'app': 'SoundCloud', 'category': 'Music'},
    'sndcdn': {'app': 'SoundCloud', 'category': 'Music'},
    'bandcamp': {'app': 'Bandcamp', 'category': 'Music'},
    'deezer': {'app': 'Deezer', 'category': 'Music'},
    'qobuz': {'app': 'Qobuz', 'category': 'Music'},
    'audible': {'app': 'Audible', 'category': 'Music'},
    'audiobooks': {'app': 'Audiobooks', 'category': 'Music'},
    'podcast': {'app': 'Podcasts', 'category': 'Music'},
    'podbean': {'app': 'Podbean', 'category': 'Music'},
    'transistor': {'app': 'Transistor', 'category': 'Music'},
    'anchor': {'app': 'Anchor', 'category': 'Music'},
    'buzzsprout': {'app': 'Buzzsprout', 'category': 'Music'},

    # ============ SHOPPING & PAYMENT (60+ patterns) ============
    'amazon': {'app': 'Amazon', 'category': 'Shopping'},
    'amazoncdn': {'app': 'Amazon', 'category': 'Shopping'},
    'ebay': {'app': 'eBay', 'category': 'Shopping'},
    'walmart': {'app': 'Walmart', 'category': 'Shopping'},
    'walmarttcdn': {'app': 'Walmart', 'category': 'Shopping'},
    'shopify': {'app': 'Shopify', 'category': 'Shopping'},
    'shopifycdn': {'app': 'Shopify', 'category': 'Shopping'},
    'etsy': {'app': 'Etsy', 'category': 'Shopping'},
    'target': {'app': 'Target', 'category': 'Shopping'},
    'costco': {'app': 'Costco', 'category': 'Shopping'},
    'homedepot': {'app': 'Home Depot', 'category': 'Shopping'},
    'lowes': {'app': 'Lowes', 'category': 'Shopping'},
    'bestbuy': {'app': 'Best Buy', 'category': 'Shopping'},
    'ikea': {'app': 'IKEA', 'category': 'Shopping'},
    'h-and-m': {'app': 'H&M', 'category': 'Shopping'},
    'zara': {'app': 'Zara', 'category': 'Shopping'},
    'uniqlo': {'app': 'Uniqlo', 'category': 'Shopping'},
    'forever21': {'app': 'Forever 21', 'category': 'Shopping'},
    'gap': {'app': 'Gap', 'category': 'Shopping'},
    'nike': {'app': 'Nike', 'category': 'Shopping'},
    'adidas': {'app': 'Adidas', 'category': 'Shopping'},
    'puma': {'app': 'Puma', 'category': 'Shopping'},
    'footlocker': {'app': 'Foot Locker', 'category': 'Shopping'},
    'aliexpress': {'app': 'AliExpress', 'category': 'Shopping'},
    'alicdn': {'app': 'AliExpress', 'category': 'Shopping'},
    'wish': {'app': 'Wish', 'category': 'Shopping'},
    'gearbest': {'app': 'Gearbest', 'category': 'Shopping'},
    'banggood': {'app': 'Banggood', 'category': 'Shopping'},
    'dhgate': {'app': 'DHgate', 'category': 'Shopping'},
    'taobao': {'app': 'Taobao', 'category': 'Shopping'},
    'tmall': {'app': 'Tmall', 'category': 'Shopping'},
    'jd.com': {'app': 'JD.com', 'category': 'Shopping'},
    'suning': {'app': 'Suning', 'category': 'Shopping'},
    'flipkart': {'app': 'Flipkart', 'category': 'Shopping'},
    'snapdeal': {'app': 'Snapdeal', 'category': 'Shopping'},
    'paytm': {'app': 'Paytm', 'category': 'Shopping'},
    'myntra': {'app': 'Myntra', 'category': 'Shopping'},
    'olx': {'app': 'OLX', 'category': 'Shopping'},
    'quikr': {'app': 'Quikr', 'category': 'Shopping'},
    'paypal': {'app': 'PayPal', 'category': 'Payment'},
    'paypalsecurity': {'app': 'PayPal', 'category': 'Payment'},
    'stripe': {'app': 'Stripe', 'category': 'Payment'},
    'square': {'app': 'Square', 'category': 'Payment'},
    'skrill': {'app': 'Skrill', 'category': 'Payment'},
    'neteller': {'app': 'Neteller', 'category': 'Payment'},
    '2checkout': {'app': '2Checkout', 'category': 'Payment'},

    # ============ SOCIAL & PROFESSIONAL (50+ patterns) ============
    'linkedin': {'app': 'LinkedIn', 'category': 'Professional'},
    'licdn': {'app': 'LinkedIn', 'category': 'Professional'},
    'indeed': {'app': 'Indeed', 'category': 'Job Search'},
    'glassdoor': {'app': 'Glassdoor', 'category': 'Job Search'},
    'monster': {'app': 'Monster', 'category': 'Job Search'},
    'linkedin-events': {'app': 'LinkedIn Events', 'category': 'Professional'},
    'hackerrank': {'app': 'HackerRank', 'category': 'Learning'},
    'leetcode': {'app': 'LeetCode', 'category': 'Learning'},
    'codechef': {'app': 'CodeChef', 'category': 'Learning'},
    'codeforces': {'app': 'Codeforces', 'category': 'Learning'},
    'projecteuler': {'app': 'Project Euler', 'category': 'Learning'},

    # ============ NEWS & MEDIA (50+ patterns) ============
    'bbc': {'app': 'BBC', 'category': 'News'},
    'cnn': {'app': 'CNN', 'category': 'News'},
    'nytimes': {'app': 'New York Times', 'category': 'News'},
    'theguardian': {'app': 'The Guardian', 'category': 'News'},
    'reuters': {'app': 'Reuters', 'category': 'News'},
    'apnews': {'app': 'AP News', 'category': 'News'},
    'huffpost': {'app': 'HuffPost', 'category': 'News'},
    'buzzfeed': {'app': 'BuzzFeed', 'category': 'News'},
    'dailymail': {'app': 'Daily Mail', 'category': 'News'},
    'foxnews': {'app': 'Fox News', 'category': 'News'},
    'bbc.com': {'app': 'BBC', 'category': 'News'},

    # ============ PRODUCTIVITY & OFFICE (40+ patterns) ============
    'notion': {'app': 'Notion', 'category': 'Productivity'},
    'notioncdn': {'app': 'Notion', 'category': 'Productivity'},
    'evernote': {'app': 'Evernote', 'category': 'Productivity'},
    'onenote': {'app': 'OneNote', 'category': 'Productivity'},
    'todoist': {'app': 'Todoist', 'category': 'Productivity'},
    'asana': {'app': 'Asana', 'category': 'Productivity'},
    'monday': {'app': 'Monday.com', 'category': 'Productivity'},
    'trello': {'app': 'Trello', 'category': 'Productivity'},
    'jira': {'app': 'Jira', 'category': 'Productivity'},
    'confluence': {'app': 'Confluence', 'category': 'Productivity'},
    'notion.so': {'app': 'Notion', 'category': 'Productivity'},
    'drive.google': {'app': 'Google Drive', 'category': 'Cloud Storage'},
    'docs.google': {'app': 'Google Docs', 'category': 'Productivity'},
    'sheets.google': {'app': 'Google Sheets', 'category': 'Productivity'},

    # ============ VPN & PRIVACY (30+ patterns) ============
    'expressvpn': {'app': 'ExpressVPN', 'category': 'VPN'},
    'nordvpn': {'app': 'NordVPN', 'category': 'VPN'},
    'surfshark': {'app': 'Surfshark', 'category': 'VPN'},
    'cyberghost': {'app': 'CyberGhost', 'category': 'VPN'},
    'protonvpn': {'app': 'ProtonVPN', 'category': 'VPN'},
    'mullvad': {'app': 'Mullvad VPN', 'category': 'VPN'},
    'windscribe': {'app': 'Windscribe', 'category': 'VPN'},
    'hotspot': {'app': 'Hotspot Shield', 'category': 'VPN'},
    'privatevpn': {'app': 'Private VPN', 'category': 'VPN'},
    'ipvanish': {'app': 'IPVanish', 'category': 'VPN'},
    'torproject': {'app': 'Tor Browser', 'category': 'Privacy'},
    'tails': {'app': 'Tails OS', 'category': 'Privacy'},

    # ============ BANKING & FINANCE (50+ patterns) ============
    'paypal': {'app': 'PayPal', 'category': 'Finance'},
    'stripe': {'app': 'Stripe', 'category': 'Finance'},
    'revolut': {'app': 'Revolut', 'category': 'Finance'},
    'wise': {'app': 'Wise', 'category': 'Finance'},
    'transferwise': {'app': 'Wise', 'category': 'Finance'},
    'n26': {'app': 'N26', 'category': 'Finance'},
    'monzo': {'app': 'Monzo', 'category': 'Finance'},
    'hdfc': {'app': 'HDFC Bank', 'category': 'Finance'},
    'icici': {'app': 'ICICI Bank', 'category': 'Finance'},
    'axis': {'app': 'Axis Bank', 'category': 'Finance'},
    'sbi': {'app': 'SBI', 'category': 'Finance'},
    'yodlee': {'app': 'Yodlee', 'category': 'Finance'},
    'zerodha': {'app': 'Zerodha', 'category': 'Finance'},
    'upstox': {'app': 'Upstox', 'category': 'Finance'},
    'groww': {'app': 'Groww', 'category': 'Finance'},
}

# Port-based fallback for common services
PORT_MAPPINGS = {
    # ============ FILE TRANSFER (20-22) ============
    20: {'app': 'FTP-DATA', 'category': 'File Transfer'},
    21: {'app': 'FTP', 'category': 'File Transfer'},
    22: {'app': 'SSH', 'category': 'Remote Access'},

    # ============ REMOTE ACCESS (23, 3389, 5900) ============
    23: {'app': 'Telnet', 'category': 'Remote Access'},
    3389: {'app': 'RDP', 'category': 'Remote Access'},
    5900: {'app': 'VNC', 'category': 'Remote Access'},

    # ============ EMAIL (25, 110, 143, 465, 587, 993, 995) ============
    25: {'app': 'SMTP', 'category': 'Email'},
    110: {'app': 'POP3', 'category': 'Email'},
    143: {'app': 'IMAP', 'category': 'Email'},
    465: {'app': 'SMTPS', 'category': 'Email'},
    587: {'app': 'SMTP-TLS', 'category': 'Email'},
    993: {'app': 'IMAPS', 'category': 'Email'},
    995: {'app': 'POP3S', 'category': 'Email'},

    # ============ NETWORK INFRASTRUCTURE (53, 67, 68, 123, 161, 162) ============
    53: {'app': 'DNS', 'category': 'Network'},
    67: {'app': 'DHCP-Server', 'category': 'Network'},
    68: {'app': 'DHCP-Client', 'category': 'Network'},
    123: {'app': 'NTP', 'category': 'Network'},
    161: {'app': 'SNMP', 'category': 'Network'},
    162: {'app': 'SNMP-Trap', 'category': 'Network'},

    # ============ NETWORK SERVICES (111, 135, 139, 389, 445, 636) ============
    111: {'app': 'Portmap', 'category': 'Network Services'},
    135: {'app': 'RPC', 'category': 'Network Services'},
    139: {'app': 'NetBIOS', 'category': 'Network Services'},
    389: {'app': 'LDAP', 'category': 'Network Services'},
    445: {'app': 'SMB', 'category': 'File Sharing'},
    636: {'app': 'LDAPS', 'category': 'Network Services'},

    # ============ FILE SHARING (873, 2049) ============
    873: {'app': 'Rsync', 'category': 'File Transfer'},
    2049: {'app': 'NFS', 'category': 'File Sharing'},

    # ============ WEB PROTOCOLS (80, 8000, 8008, 8080) ============
    80: {'app': 'HTTP', 'category': 'Web'},
    8000: {'app': 'HTTP-ALT', 'category': 'Web'},
    8008: {'app': 'HTTP-ALT-2', 'category': 'Web'},
    8080: {'app': 'HTTP-PROXY', 'category': 'Web'},

    # ============ SECURE WEB (443, 8443) ============
    443: {'app': 'HTTPS', 'category': 'Web'},
    8443: {'app': 'HTTPS-ALT', 'category': 'Web'},

    # ============ PROXY SERVICES (1080, 3128, 8118) ============
    1080: {'app': 'SOCKS', 'category': 'Proxy'},
    3128: {'app': 'Squid-Proxy', 'category': 'Proxy'},
    8118: {'app': 'Privoxy', 'category': 'Proxy'},

    # ============ VPN (1194) ============
    1194: {'app': 'OpenVPN', 'category': 'VPN'},

    # ============ SSH RELATED (22, 2222) ============
    2222: {'app': 'SSH-ALT', 'category': 'Remote Access'},

    # ============ TELNET ALTERNATIVES (3000, 3001) ============
    3000: {'app': 'Development-HTTP', 'category': 'Development'},
    3001: {'app': 'Development-ALT', 'category': 'Development'},

    # ============ DATABASES (3306, 5432, 5984, 6379, 27017) ============
    3306: {'app': 'MySQL', 'category': 'Database'},
    5432: {'app': 'PostgreSQL', 'category': 'Database'},
    5984: {'app': 'CouchDB', 'category': 'Database'},
    6379: {'app': 'Redis', 'category': 'Cache'},
    27017: {'app': 'MongoDB', 'category': 'Database'},

    # ============ MESSAGE QUEUES (5671, 5672) ============
    5671: {'app': 'AMQPS', 'category': 'Message Queue'},
    5672: {'app': 'AMQP', 'category': 'Message Queue'},

    # ============ PRINTING SERVICES (515, 631) ============
    515: {'app': 'LPR', 'category': 'Printing'},
    631: {'app': 'IPP', 'category': 'Printing'},

    # ============ IRC (6667, 6697) ============
    6667: {'app': 'IRC', 'category': 'Messaging'},
    6697: {'app': 'IRC-TLS', 'category': 'Messaging'},

    # ============ CONTAINER (2375, 2376) ============
    2375: {'app': 'Docker', 'category': 'Container'},
    2376: {'app': 'Docker-TLS', 'category': 'Container'},

    # ============ ROUTING PROTOCOLS (179, 520, 521) ============
    179: {'app': 'BGP', 'category': 'Routing'},
    520: {'app': 'RIP', 'category': 'Routing'},
    521: {'app': 'RIPng', 'category': 'Routing'},

    # ============ LOGGING (514, 5140) ============
    514: {'app': 'Syslog', 'category': 'Logging'},
    5140: {'app': 'Syslog-TLS', 'category': 'Logging'},

    # ============ VERSION CONTROL (9418) ============
    9418: {'app': 'Git', 'category': 'Development'},

    # ============ GAMING (25565) ============
    25565: {'app': 'Minecraft', 'category': 'Gaming'},

    # ============ COMMON ALT PORTS (9000, 9001, 9999) ============
    9000: {'app': 'DevServer', 'category': 'Development'},
    9001: {'app': 'DevServer-ALT', 'category': 'Development'},
    9999: {'app': 'Custom-Service', 'category': 'Development'},

    # ============ COMMON RANGE (4000-4010) ============
    4000: {'app': 'Alternate-Web', 'category': 'Web'},
    4001: {'app': 'Alternate-Web-1', 'category': 'Web'},
    4002: {'app': 'Alternate-Web-2', 'category': 'Web'},
    4003: {'app': 'Alternate-Web-3', 'category': 'Web'},
    4004: {'app': 'Alternate-Web-4', 'category': 'Web'},
    4005: {'app': 'Alternate-Web-5', 'category': 'Web'},
    4006: {'app': 'Alternate-Web-6', 'category': 'Web'},
    4007: {'app': 'Alternate-Web-7', 'category': 'Web'},
    4008: {'app': 'Alternate-Web-8', 'category': 'Web'},
    4009: {'app': 'Alternate-Web-9', 'category': 'Web'},
    4010: {'app': 'Alternate-Web-10', 'category': 'Web'},

    # ============ COMMON RANGE (5000-5010) ============
    5000: {'app': 'Flask-Dev', 'category': 'Development'},
    5001: {'app': 'Dev-Server-1', 'category': 'Development'},
    5002: {'app': 'Dev-Server-2', 'category': 'Development'},
    5003: {'app': 'Dev-Server-3', 'category': 'Development'},
    5004: {'app': 'Dev-Server-4', 'category': 'Development'},
    5005: {'app': 'Dev-Server-5', 'category': 'Development'},
    5006: {'app': 'Dev-Server-6', 'category': 'Development'},
    5007: {'app': 'Dev-Server-7', 'category': 'Development'},
    5008: {'app': 'Dev-Server-8', 'category': 'Development'},
    5009: {'app': 'Dev-Server-9', 'category': 'Development'},
    5010: {'app': 'Dev-Server-10', 'category': 'Development'},

    # ============ KUBERNETES & APIS (6443, 8443, 8888) ============
    6443: {'app': 'Kubernetes-API', 'category': 'Container'},
    8888: {'app': 'Jupyter', 'category': 'Development'},

    # ============ ELASTICSEARCH & ANALYTICS (9200, 9300) ============
    9200: {'app': 'Elasticsearch', 'category': 'Database'},
    9300: {'app': 'Elasticsearch-Node', 'category': 'Database'},

    # ============ REDIS CLUSTER (6380-6390) ============
    6380: {'app': 'Redis-Cluster-1', 'category': 'Cache'},
    6381: {'app': 'Redis-Cluster-2', 'category': 'Cache'},
    6382: {'app': 'Redis-Cluster-3', 'category': 'Cache'},
    6383: {'app': 'Redis-Cluster-4', 'category': 'Cache'},
    6384: {'app': 'Redis-Cluster-5', 'category': 'Cache'},
    6385: {'app': 'Redis-Cluster-6', 'category': 'Cache'},
    6386: {'app': 'Redis-Cluster-7', 'category': 'Cache'},
    6387: {'app': 'Redis-Cluster-8', 'category': 'Cache'},
    6388: {'app': 'Redis-Cluster-9', 'category': 'Cache'},
    6389: {'app': 'Redis-Cluster-10', 'category': 'Cache'},
    6390: {'app': 'Redis-Cluster-11', 'category': 'Cache'},

    # ============ MEMCACHED (11211) ============
    11211: {'app': 'Memcached', 'category': 'Cache'},

    # ============ MONGODB REPLICA (27018-27020) ============
    27018: {'app': 'MongoDB-Replica-1', 'category': 'Database'},
    27019: {'app': 'MongoDB-Replica-2', 'category': 'Database'},
    27020: {'app': 'MongoDB-Replica-3', 'category': 'Database'},

    # ============ POSTGRESQL ALT (5433, 5434) ============
    5433: {'app': 'PostgreSQL-ALT-1', 'category': 'Database'},
    5434: {'app': 'PostgreSQL-ALT-2', 'category': 'Database'},

    # ============ MYSQL ALT (3307, 3308) ============
    3307: {'app': 'MySQL-ALT-1', 'category': 'Database'},
    3308: {'app': 'MySQL-ALT-2', 'category': 'Database'},

    # ============ KAFKA (9092, 9093) ============
    9092: {'app': 'Kafka', 'category': 'Message Queue'},
    9093: {'app': 'Kafka-TLS', 'category': 'Message Queue'},

    # ============ MSSQL (1433) ============
    1433: {'app': 'MSSQL', 'category': 'Database'},

    # ============ ORACLE (1521) ============
    1521: {'app': 'Oracle-DB', 'category': 'Database'},

    # ============ CASSANDRA (9042, 9160) ============
    9042: {'app': 'Cassandra', 'category': 'Database'},
    9160: {'app': 'Cassandra-Thrift', 'category': 'Database'},

    # ============ INFLUXDB (8086) ============
    8086: {'app': 'InfluxDB', 'category': 'Database'},

    # ============ PROMETHEUS (9090) ============
    9090: {'app': 'Prometheus', 'category': 'Monitoring'},

    # ============ CONSUL (8500) ============
    8500: {'app': 'Consul', 'category': 'Container'},

    # ============ VAULT (8200) ============
    8200: {'app': 'Vault', 'category': 'Security'},

    # ============ ETCD (2379, 2380) ============
    2379: {'app': 'Etcd-Client', 'category': 'Container'},
    2380: {'app': 'Etcd-Server', 'category': 'Container'},

    # ============ ZOOKEEPER (2181) ============
    2181: {'app': 'Zookeeper', 'category': 'Container'},

    # ============ SOLR (8983) ============
    8983: {'app': 'Solr', 'category': 'Database'},

    # ============ SPLUNK (8000, 8089) ============
    8089: {'app': 'Splunk', 'category': 'Logging'},

    # ============ LOGSTASH (5000, 9600) ============
    9600: {'app': 'Logstash', 'category': 'Logging'},

    # ============ KIBANA (5601) ============
    5601: {'app': 'Kibana', 'category': 'Analytics'},

    # ============ JENKINS (8080, 8081, 50000) ============
    8081: {'app': 'Jenkins-UI', 'category': 'Development'},
    50000: {'app': 'Jenkins-Agent', 'category': 'Development'},

    # ============ ARTIFACTORY (8081, 8082) ============
    8082: {'app': 'Artifactory', 'category': 'Development'},

    # ============ HARBOR REGISTRY (80, 443, 4443) ============
    4443: {'app': 'Harbor-Registry', 'category': 'Container'},

    # ============ RABBITMQ (5672, 15672) ============
    15672: {'app': 'RabbitMQ-UI', 'category': 'Message Queue'},

    # ============ ACTIVEMQ (61616) ============
    61616: {'app': 'ActiveMQ', 'category': 'Message Queue'},

    # ============ MQTT (1883, 8883) ============
    1883: {'app': 'MQTT', 'category': 'IoT'},
    8883: {'app': 'MQTT-TLS', 'category': 'IoT'},

    # ============ COAP (5683) ============
    5683: {'app': 'CoAP', 'category': 'IoT'},

    # ============ MODBUS (502) ============
    502: {'app': 'Modbus', 'category': 'Industrial'},

    # ============ GRPC (50051) ============
    50051: {'app': 'gRPC', 'category': 'Development'},

    # ============ XMPP (5222, 5269) ============
    5222: {'app': 'XMPP-Client', 'category': 'Messaging'},
    5269: {'app': 'XMPP-Server', 'category': 'Messaging'},

    # ============ SIP (5060, 5061) ============
    5060: {'app': 'SIP', 'category': 'VoIP'},
    5061: {'app': 'SIP-TLS', 'category': 'VoIP'},

    # ============ RTMP (1935) ============
    1935: {'app': 'RTMP', 'category': 'Streaming'},

    # ============ RTSP (554) ============
    554: {'app': 'RTSP', 'category': 'Streaming'},

    # ============ LDAP ALT (3268, 3269) ============
    3268: {'app': 'LDAP-GC', 'category': 'Network Services'},
    3269: {'app': 'LDAP-GC-TLS', 'category': 'Network Services'},

    # ============ KERBEROS (88) ============
    88: {'app': 'Kerberos', 'category': 'Security'},

    # ============ RADIUS (1812, 1813) ============
    1812: {'app': 'RADIUS-Auth', 'category': 'Security'},
    1813: {'app': 'RADIUS-Account', 'category': 'Security'},

    # ============ TACACS (49) ============
    49: {'app': 'TACACS', 'category': 'Security'},

    # ============ SAMBA (137, 138) ============
    137: {'app': 'NetBIOS-Name', 'category': 'File Sharing'},
    138: {'app': 'NetBIOS-Datagram', 'category': 'File Sharing'},
}

# Cache for IP to application mapping (from DNS resolution)
# This maps an IP address (e.g., "1.2.3.4") to its identified application info.
ip_to_app_cache = {}

def identify_app_from_domain(domain):
    """
    Identify application from domain name using pattern matching.
    Returns app info dict or None.
    """
    if not domain:
        return None
    domain_lower = domain.lower()
    # Check each pattern (prioritized order)
    for pattern, app_info in DOMAIN_PATTERNS.items():
        if pattern in domain_lower:
            return app_info
    return None

def identify_app_from_port(port):
    """
    Fallback: identify application from port number.
    Returns app info dict or None.
    """
    if not port:
        return None
    try:
        port_num = int(port)
        return PORT_MAPPINGS.get(port_num)
    except (ValueError, TypeError):
        return None

def cache_dns_mapping(ip, domain):
    """
    Cache the DNS query result for future lookups.
    Maps IP address to application based on domain.
    """
    if not ip or not domain:
        return
    app_info = identify_app_from_domain(domain)
    if app_info:
        # Store the mapping in our cache
        ip_to_app_cache[ip] = app_info

def get_app_from_ip(ip):
    """Get cached application info from IP address."""
    return ip_to_app_cache.get(ip)

# ... (all your dictionaries and other functions remain the same) ...

def detect_application(src_ip, dst_ip, src_port, dst_port, protocol, dns_query, dns_responses, sni_hostname, quic_sni):
    """
    Main detection function:
    Prioritizes TLS SNI, then QUIC SNI, then DNS, then IP cache, then ports.
    """
    
    # --- STRATEGY 1: TLS SNI (For TCP/TLS traffic) ---
    if sni_hostname:
        app_info = identify_app_from_domain(sni_hostname)
        if app_info:
            cache_dns_mapping(dst_ip, sni_hostname)
            return app_info

    # --- STRATEGY 2: QUIC SNI (For UDP/QUIC traffic) ---
    # This specifically checks QUIC packets for their own SNI tag.
    if quic_sni:
        app_info = identify_app_from_domain(quic_sni)
        if app_info:
            cache_dns_mapping(dst_ip, quic_sni)
            return app_info
            
    # --- STRATEGY 3: DNS Query Name (Accurate, but only for DNS packets) ---
    if dns_query:
        app_info = identify_app_from_domain(dns_query)
        if app_info:
            if dns_responses:
                for resp_ip in dns_responses.split(','):
                    cache_dns_mapping(resp_ip, dns_query)
            return app_info
            
    # --- STRATEGY 4: Check Cached IP Mappings (Less Accurate) ---
    for ip in [dst_ip, src_ip]:
        cached_app = get_app_from_ip(ip)
        if cached_app:
            return cached_app
            
    # --- STRATEGY 5: Port-based Fallback (Least Accurate) ---
    app_info = identify_app_from_port(dst_port)
    if app_info:
        return app_info

    # Default: Unknown
    return {'app': 'Unknown', 'category': 'Other'}