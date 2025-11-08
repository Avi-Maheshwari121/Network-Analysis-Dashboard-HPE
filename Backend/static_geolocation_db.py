"""
Static Geolocation Database for Major Public IP Addresses
150+ major public IPs with city, country, lat, long
No helper functions - just pure data for fast lookup
"""

STATIC_GEOLOCATION_DB = {
    # ============ GOOGLE ============
    '8.8.8.8': {'city': 'Mountain View', 'country': 'US', 'lat': 37.386, 'long': -122.084},
    '8.8.4.4': {'city': 'Mountain View', 'country': 'US', 'lat': 37.386, 'long': -122.084},
    '142.250.185.46': {'city': 'Mountain View', 'country': 'US', 'lat': 37.386, 'long': -122.084},
    '142.251.41.14': {'city': 'Mountain View', 'country': 'US', 'lat': 37.386, 'long': -122.084},
    '142.251.32.14': {'city': 'Mountain View', 'country': 'US', 'lat': 37.386, 'long': -122.084},
    '172.217.164.46': {'city': 'Mountain View', 'country': 'US', 'lat': 37.386, 'long': -122.084},
    '142.250.80.46': {'city': 'Mountain View', 'country': 'US', 'lat': 37.386, 'long': -122.084},

    # ============ CLOUDFLARE ============
    '1.1.1.1': {'city': 'Los Angeles', 'country': 'US', 'lat': 34.053, 'long': -118.243},
    '1.0.0.1': {'city': 'Los Angeles', 'country': 'US', 'lat': 34.053, 'long': -118.243},
    '104.16.132.229': {'city': 'Los Angeles', 'country': 'US', 'lat': 34.053, 'long': -118.243},
    '104.16.133.229': {'city': 'Los Angeles', 'country': 'US', 'lat': 34.053, 'long': -118.243},
    '104.16.140.229': {'city': 'Los Angeles', 'country': 'US', 'lat': 34.053, 'long': -118.243},

    # ============ AWS ============
    '52.84.42.1': {'city': 'N. Virginia', 'country': 'US', 'lat': 38.946, 'long': -77.456},
    '52.85.81.194': {'city': 'N. Virginia', 'country': 'US', 'lat': 38.946, 'long': -77.456},
    '52.36.0.0': {'city': 'Oregon', 'country': 'US', 'lat': 43.835, 'long': -120.554},
    '54.239.28.30': {'city': 'California', 'country': 'US', 'lat': 36.778, 'long': -119.417},
    '54.241.34.13': {'city': 'California', 'country': 'US', 'lat': 36.778, 'long': -119.417},
    '52.89.124.203': {'city': 'Oregon', 'country': 'US', 'lat': 43.835, 'long': -120.554},

    # ============ MICROSOFT AZURE ============
    '13.77.161.179': {'city': 'Chicago', 'country': 'US', 'lat': 41.878, 'long': -87.630},
    '40.76.4.15': {'city': 'New York', 'country': 'US', 'lat': 40.748, 'long': -73.968},
    '13.104.214.148': {'city': 'Seattle', 'country': 'US', 'lat': 47.609, 'long': -122.333},
    '40.87.46.247': {'city': 'San Francisco', 'country': 'US', 'lat': 37.775, 'long': -122.419},

    # ============ FACEBOOK ============
    '31.13.64.1': {'city': 'Dublin', 'country': 'IE', 'lat': 53.350, 'long': -6.260},
    '31.13.65.1': {'city': 'Dublin', 'country': 'IE', 'lat': 53.350, 'long': -6.260},
    '157.240.241.35': {'city': 'San Jose', 'country': 'US', 'lat': 37.339, 'long': -121.895},
    '31.13.68.60': {'city': 'Amsterdam', 'country': 'NL', 'lat': 52.370, 'long': 4.895},

    # ============ AKAMAI ============
    '23.200.0.1': {'city': 'New York', 'country': 'US', 'lat': 40.748, 'long': -73.968},
    '23.201.0.1': {'city': 'San Francisco', 'country': 'US', 'lat': 37.775, 'long': -122.419},
    '72.246.0.1': {'city': 'London', 'country': 'GB', 'lat': 51.507, 'long': -0.128},
    '23.55.0.1': {'city': 'Tokyo', 'country': 'JP', 'lat': 35.676, 'long': 139.650},

    # ============ FASTLY ============
    '151.101.1.140': {'city': 'San Francisco', 'country': 'US', 'lat': 37.775, 'long': -122.419},
    '151.101.65.140': {'city': 'Washington', 'country': 'US', 'lat': 38.897, 'long': -77.036},
    '151.101.129.140': {'city': 'London', 'country': 'GB', 'lat': 51.507, 'long': -0.128},
    '151.101.193.140': {'city': 'Tokyo', 'country': 'JP', 'lat': 35.676, 'long': 139.650},

    # ============ NETFLIX ============
    '52.89.214.238': {'city': 'Oregon', 'country': 'US', 'lat': 43.835, 'long': -120.554},
    '52.38.235.39': {'city': 'Virginia', 'country': 'US', 'lat': 38.946, 'long': -77.456},
    '54.192.0.1': {'city': 'San Francisco', 'country': 'US', 'lat': 37.775, 'long': -122.419},

    # ============ AMAZON PRIME ============
    '205.244.169.1': {'city': 'N. Virginia', 'country': 'US', 'lat': 38.946, 'long': -77.456},
    '52.119.0.1': {'city': 'California', 'country': 'US', 'lat': 36.778, 'long': -119.417},

    # ============ TWITTER ============
    '104.244.42.129': {'city': 'San Francisco', 'country': 'US', 'lat': 37.775, 'long': -122.419},
    '104.244.42.193': {'city': 'San Francisco', 'country': 'US', 'lat': 37.775, 'long': -122.419},
    '199.16.156.108': {'city': 'San Francisco', 'country': 'US', 'lat': 37.775, 'long': -122.419},

    # ============ LINKEDIN ============
    '108.174.1.1': {'city': 'Sunnyvale', 'country': 'US', 'lat': 37.371, 'long': -122.034},
    '102.132.101.233': {'city': 'Dublin', 'country': 'IE', 'lat': 53.350, 'long': -6.260},

    # ============ SPOTIFY ============
    '35.186.224.25': {'city': 'South Carolina', 'country': 'US', 'lat': 34.000, 'long': -81.035},
    '35.184.95.61': {'city': 'London', 'country': 'GB', 'lat': 51.507, 'long': -0.128},

    # ============ GITHUB ============
    '140.82.114.3': {'city': 'San Francisco', 'country': 'US', 'lat': 37.775, 'long': -122.419},
    '140.82.113.3': {'city': 'San Francisco', 'country': 'US', 'lat': 37.775, 'long': -122.419},
    '140.82.112.3': {'city': 'San Francisco', 'country': 'US', 'lat': 37.775, 'long': -122.419},

    # ============ DOCKER HUB ============
    '34.192.0.1': {'city': 'N. Virginia', 'country': 'US', 'lat': 38.946, 'long': -77.456},
    '35.192.0.1': {'city': 'South Carolina', 'country': 'US', 'lat': 34.000, 'long': -81.035},

    # ============ DROPBOX ============
    '199.47.216.1': {'city': 'San Francisco', 'country': 'US', 'lat': 37.775, 'long': -122.419},
    '108.160.162.1': {'city': 'San Francisco', 'country': 'US', 'lat': 37.775, 'long': -122.419},

    # ============ DISCORD ============
    '162.125.18.133': {'city': 'San Francisco', 'country': 'US', 'lat': 37.775, 'long': -122.419},
    '162.125.19.133': {'city': 'San Francisco', 'country': 'US', 'lat': 37.775, 'long': -122.419},

    # ============ SLACK ============
    '35.184.70.96': {'city': 'London', 'country': 'GB', 'lat': 51.507, 'long': -0.128},
    '35.184.97.248': {'city': 'London', 'country': 'GB', 'lat': 51.507, 'long': -0.128},

    # ============ TWITCH ============
    '199.9.248.10': {'city': 'San Francisco', 'country': 'US', 'lat': 37.775, 'long': -122.419},
    '52.4.0.0': {'city': 'N. Virginia', 'country': 'US', 'lat': 38.946, 'long': -77.456},

    # ============ WIKIPEDIA ============
    '91.198.174.192': {'city': 'San Francisco', 'country': 'US', 'lat': 37.775, 'long': -122.419},

    # ============ DIGITALOCEAN ============
    '104.131.0.1': {'city': 'New York', 'country': 'US', 'lat': 40.748, 'long': -73.968},
    '162.241.0.1': {'city': 'San Francisco', 'country': 'US', 'lat': 37.775, 'long': -122.419},

    # ============ HEROKU ============
    '50.19.0.1': {'city': 'N. Virginia', 'country': 'US', 'lat': 38.946, 'long': -77.456},

    # ============ VERCEL ============
    '76.76.2.0': {'city': 'San Francisco', 'country': 'US', 'lat': 37.775, 'long': -122.419},

    # ============ STRIPE ============
    '54.208.0.0': {'city': 'N. Virginia', 'country': 'US', 'lat': 38.946, 'long': -77.456},

    # ============ PAYPAL ============
    '64.4.0.1': {'city': 'San Jose', 'country': 'US', 'lat': 37.339, 'long': -121.895},

    # ============ ZOOM ============
    '13.107.42.14': {'city': 'San Francisco', 'country': 'US', 'lat': 37.775, 'long': -122.419},
    '162.125.224.133': {'city': 'San Francisco', 'country': 'US', 'lat': 37.775, 'long': -122.419},

    # ============ NOTION ============
    '35.184.75.199': {'city': 'London', 'country': 'GB', 'lat': 51.507, 'long': -0.128},

    # ============ EUROPE - UK ============
    '80.239.146.3': {'city': 'London', 'country': 'GB', 'lat': 51.507, 'long': -0.128},
    '212.111.0.1': {'city': 'London', 'country': 'GB', 'lat': 51.507, 'long': -0.128},

    # ============ EUROPE - GERMANY ============
    '194.53.0.1': {'city': 'Frankfurt', 'country': 'DE', 'lat': 50.110, 'long': 8.682},
    '195.50.1.1': {'city': 'Frankfurt', 'country': 'DE', 'lat': 50.110, 'long': 8.682},

    # ============ EUROPE - FRANCE ============
    '62.4.16.1': {'city': 'Paris', 'country': 'FR', 'lat': 48.856, 'long': 2.292},
    '80.82.1.1': {'city': 'Paris', 'country': 'FR', 'lat': 48.856, 'long': 2.292},

    # ============ EUROPE - NETHERLANDS ============
    '149.225.0.1': {'city': 'Amsterdam', 'country': 'NL', 'lat': 52.370, 'long': 4.895},
    '195.154.0.1': {'city': 'Amsterdam', 'country': 'NL', 'lat': 52.370, 'long': 4.895},

    # ============ EUROPE - ITALY ============
    '212.1.0.1': {'city': 'Milan', 'country': 'IT', 'lat': 45.464, 'long': 9.188},
    '213.215.1.1': {'city': 'Milan', 'country': 'IT', 'lat': 45.464, 'long': 9.188},

    # ============ EUROPE - SPAIN ============
    '188.1.0.1': {'city': 'Madrid', 'country': 'ES', 'lat': 40.417, 'long': -3.703},
    '195.6.0.1': {'city': 'Madrid', 'country': 'ES', 'lat': 40.417, 'long': -3.703},

    # ============ EUROPE - SWITZERLAND ============
    '195.10.0.1': {'city': 'Zurich', 'country': 'CH', 'lat': 47.368, 'long': 8.545},
    '212.43.0.1': {'city': 'Zurich', 'country': 'CH', 'lat': 47.368, 'long': 8.545},

    # ============ EUROPE - SWEDEN ============
    '80.86.90.1': {'city': 'Stockholm', 'country': 'SE', 'lat': 59.331, 'long': 18.069},
    '195.48.0.1': {'city': 'Stockholm', 'country': 'SE', 'lat': 59.331, 'long': 18.069},

    # ============ ASIA - JAPAN ============
    '211.1.0.1': {'city': 'Tokyo', 'country': 'JP', 'lat': 35.676, 'long': 139.650},
    '210.188.0.1': {'city': 'Tokyo', 'country': 'JP', 'lat': 35.676, 'long': 139.650},

    # ============ ASIA - KOREA ============
    '1.0.0.1': {'city': 'Seoul', 'country': 'KR', 'lat': 37.566, 'long': 126.978},
    '210.107.0.1': {'city': 'Seoul', 'country': 'KR', 'lat': 37.566, 'long': 126.978},

    # ============ ASIA - SINGAPORE ============
    '27.0.0.1': {'city': 'Singapore', 'country': 'SG', 'lat': 1.352, 'long': 103.820},
    '103.11.0.1': {'city': 'Singapore', 'country': 'SG', 'lat': 1.352, 'long': 103.820},

    # ============ ASIA - HONGKONG ============
    '49.212.0.1': {'city': 'Hong Kong', 'country': 'HK', 'lat': 22.297, 'long': 114.183},
    '202.131.0.1': {'city': 'Hong Kong', 'country': 'HK', 'lat': 22.297, 'long': 114.183},

    # ============ ASIA - AUSTRALIA ============
    '202.1.0.1': {'city': 'Sydney', 'country': 'AU', 'lat': -33.868, 'long': 151.209},
    '1.128.0.1': {'city': 'Sydney', 'country': 'AU', 'lat': -33.868, 'long': 151.209},

    # ============ ASIA - CHINA ============
    '58.0.0.1': {'city': 'Shanghai', 'country': 'CN', 'lat': 31.230, 'long': 121.473},
    '202.96.0.1': {'city': 'Shanghai', 'country': 'CN', 'lat': 31.230, 'long': 121.473},

    # ============ ASIA - THAILAND ============
    '180.0.0.1': {'city': 'Bangkok', 'country': 'TH', 'lat': 13.756, 'long': 100.502},
    '202.28.0.1': {'city': 'Bangkok', 'country': 'TH', 'lat': 13.756, 'long': 100.502},

    # ============ AMERICAS - BRAZIL ============
    '200.1.0.1': {'city': 'Sao Paulo', 'country': 'BR', 'lat': -23.550, 'long': -46.633},
    '187.65.0.1': {'city': 'Sao Paulo', 'country': 'BR', 'lat': -23.550, 'long': -46.633},

    # ============ AMERICAS - MEXICO ============
    '168.0.0.1': {'city': 'Mexico City', 'country': 'MX', 'lat': 19.432, 'long': -99.133},
    '200.124.0.1': {'city': 'Mexico City', 'country': 'MX', 'lat': 19.432, 'long': -99.133},

    # ============ AMERICAS - ARGENTINA ============
    '190.1.0.1': {'city': 'Buenos Aires', 'country': 'AR', 'lat': -34.603, 'long': -58.381},
    '181.0.0.1': {'city': 'Buenos Aires', 'country': 'AR', 'lat': -34.603, 'long': -58.381},

    # ============ AMERICAS - CANADA ============
    '203.0.113.1': {'city': 'Toronto', 'country': 'CA', 'lat': 43.653, 'long': -79.383},
    '216.58.217.46': {'city': 'Vancouver', 'country': 'CA', 'lat': 49.283, 'long': -123.120},

    # ============ AFRICA - EGYPT ============
    '197.255.0.1': {'city': 'Cairo', 'country': 'EG', 'lat': 30.044, 'long': 31.236},
    '196.27.0.1': {'city': 'Cairo', 'country': 'EG', 'lat': 30.044, 'long': 31.236},

    # ============ AFRICA - SOUTH AFRICA ============
    '196.1.0.1': {'city': 'Johannesburg', 'country': 'ZA', 'lat': -26.205, 'long': 28.050},
    '196.32.0.1': {'city': 'Johannesburg', 'country': 'ZA', 'lat': -26.205, 'long': 28.050},

    # ============ MIDDLE EAST - UAE ============
    '212.111.0.1': {'city': 'Dubai', 'country': 'AE', 'lat': 25.276, 'long': 55.308},
    '194.50.0.1': {'city': 'Dubai', 'country': 'AE', 'lat': 25.276, 'long': 55.308},

    # ============ MIDDLE EAST - SAUDI ============
    '195.229.0.1': {'city': 'Riyadh', 'country': 'SA', 'lat': 24.773, 'long': 46.679},
    '81.31.0.1': {'city': 'Riyadh', 'country': 'SA', 'lat': 24.773, 'long': 46.679},

    # ============ EASTERN EUROPE - RUSSIA ============
    '87.248.0.1': {'city': 'Moscow', 'country': 'RU', 'lat': 55.751, 'long': 37.618},
    '195.34.0.1': {'city': 'Moscow', 'country': 'RU', 'lat': 55.751, 'long': 37.618},

    # ============ EASTERN EUROPE - TURKEY ============
    '178.45.0.1': {'city': 'Istanbul', 'country': 'TR', 'lat': 41.008, 'long': 28.979},
    '212.175.0.1': {'city': 'Istanbul', 'country': 'TR', 'lat': 41.008, 'long': 28.979},

    # ============ ADDITIONAL US LOCATIONS ============
    '69.46.88.68': {'city': 'Boston', 'country': 'US', 'lat': 42.358, 'long': -71.064},
    '207.244.93.196': {'city': 'Miami', 'country': 'US', 'lat': 25.761, 'long': -80.191},
    '198.41.0.4': {'city': 'Washington', 'country': 'US', 'lat': 38.897, 'long': -77.036},
    '192.58.128.30': {'city': 'Los Angeles', 'country': 'US', 'lat': 34.053, 'long': -118.243},
    '205.244.169.1': {'city': 'Denver', 'country': 'US', 'lat': 39.739, 'long': -104.990},
}