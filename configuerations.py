ELASTICSEARCH_DOCS_INDEX_MAP = {
            'mappings': {
                'properties': {
                    'id': {'type': 'keyword'},
                    'text': {'type': 'text'},
                    'bds_precent': {'type': 'float'},
                    'is_bds': {'type': 'boolean'},
                    'bds_thread_level': {'type': 'keyword'},
                    'name': {'type': 'keyword'},
                    'file_path': {'type': 'keyword'},
                    'size': {'type': 'keyword'},
                    'create_date': {
                        'type': 'date',
                        'format': 'yyyy-MM-dd HH:mm:ss'
                    },
                    'modified_date': {
                        'type': 'date',
                        'format': 'yyyy-MM-dd HH:mm:ss'
                    },
                    'last_access': {
                        'type': 'date',
                        'format': 'yyyy-MM-dd HH:mm:ss'
                    }
                }
            }
        }