""" Port-based fallback for common services"""

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
