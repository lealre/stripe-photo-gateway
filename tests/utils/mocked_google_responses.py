google_mocked_response_success = {
    'results': [
        {
            'address_components': [
                {
                    'long_name': 'Avenida Eusébio da Silva Ferreira',
                    'short_name': 'Av. Eusébio da Silva Ferreira',
                    'types': ['route'],
                },
                {
                    'long_name': 'Lisboa',
                    'short_name': 'Lisboa',
                    'types': ['locality', 'political'],
                },
                {
                    'long_name': 'São Domingos de Benfica',
                    'short_name': 'São Domingos de Benfica',
                    'types': ['administrative_area_level_3', 'political'],
                },
                {
                    'long_name': 'Lisboa',
                    'short_name': 'Lisboa',
                    'types': ['administrative_area_level_2', 'political'],
                },
                {
                    'long_name': 'Lisboa',
                    'short_name': 'Lisboa',
                    'types': ['administrative_area_level_1', 'political'],
                },
                {
                    'long_name': 'Portugal',
                    'short_name': 'PT',
                    'types': ['country', 'political'],
                },
                {
                    'long_name': '1500-313',
                    'short_name': '1500-313',
                    'types': ['postal_code'],
                },
            ],
            'formatted_address': (
                'Av. Eusébio da Silva Ferreira, 1500-313 Lisboa, Portugal'
            ),
            'geometry': {
                'bounds': {
                    'northeast': {'lat': 38.75626540000003, 'lng': -9.1822775},
                    'southwest': {'lat': 38.74844109999998, 'lng': -9.1895846},
                },
                'location': {'lat': 38.752826, 'lng': -9.1869552},
                'location_type': 'GEOMETRIC_CENTER',
                'viewport': {
                    'northeast': {'lat': 38.75626540000003, 'lng': -9.1822775},
                    'southwest': {'lat': 38.74844109999998, 'lng': -9.1895846},
                },
            },
            'place_id': (
                'EjlBdi4gRXVzw6liaW8gZGEgU2lsdmEgRmVycmVpcmEsIDE1MDAtMzEzIExpc2JvYSwgUG9'
                'ydHVnYWwiLiosChQKEgmD1nGB2DIZDRF1idA4hXADGRIUChIJgTHAftYyGQ0RYppR6P'
                '-jXRU'
            ),
            'types': ['route'],
        }
    ],
    'status': 'OK',
}

google_mocked_respone_not_in_portugal = {
    "results": [
        {
            "address_components": [
                {
                    "long_name": "Rua Professor Eurico Rabelo",
                    "short_name": "R. Prof. Eurico Rabelo",
                    "types": [
                        "route"
                    ]
                },
                {
                    "long_name": "Maracanã",
                    "short_name": "Maracanã",
                    "types": [
                        "political",
                        "sublocality",
                        "sublocality_level_1"
                    ]
                },
                {
                    "long_name": "Rio de Janeiro",
                    "short_name": "Rio de Janeiro",
                    "types": [
                        "administrative_area_level_2",
                        "political"
                    ]
                },
                {
                    "long_name": "Rio de Janeiro",
                    "short_name": "RJ",
                    "types": [
                        "administrative_area_level_1",
                        "political"
                    ]
                },
                {
                    "long_name": "Brazil",
                    "short_name": "BR",
                    "types": [
                        "country",
                        "political"
                    ]
                },
                {
                    "long_name": "20271-150",
                    "short_name": "20271-150",
                    "types": [
                        "postal_code"
                    ]
                }
            ],
            "formatted_address": "R. Prof. Eurico Rabelo - Maracanã, Rio de Janeiro - RJ, 20271-150, Brazil",
            "geometry": {
                "bounds": {
                    "northeast": {
                        "lat": -22.9118112,
                        "lng": -43.2279653
                    },
                    "southwest": {
                        "lat": -22.9162357,
                        "lng": -43.2341639
                    }
                },
                "location": {
                    "lat": -22.9139368,
                    "lng": -43.2310122
                },
                "location_type": "GEOMETRIC_CENTER",
                "viewport": {
                    "northeast": {
                        "lat": -22.9118112,
                        "lng": -43.2279653
                    },
                    "southwest": {
                        "lat": -22.9162357,
                        "lng": -43.2341639
                    }
                }
            },
            "partial_match": True,
            "place_id": "ChIJa8gasF1-mQARC-S2PxJqR9U",
            "types": [
                "route"
            ]
        }
    ],
    "status": "OK"
}

google_mocked_response_results_empty = {
    "results": [],
    "status": "ZERO_RESULTS"
}

google_mocked_response_invalid_fields = {
    "status": "ZERO_RESULTS"
}

google_mocked_response_multiple_results = {
    "results": [
        {
            "address_components": [
                {
                    "long_name": "Portugal",
                    "short_name": "PT",
                    "types": [
                        "country",
                        "political"
                    ]
                }
            ],
            "formatted_address": "Portugal",
            "geometry": {
                "bounds": {
                    "northeast": {
                        "lat": 42.1543111,
                        "lng": -6.189159200000001
                    },
                    "southwest": {
                        "lat": 29.8288392,
                        "lng": -31.4647999
                    }
                },
                "location": {
                    "lat": 39.39987199999999,
                    "lng": -8.224454
                },
                "location_type": "APPROXIMATE",
                "viewport": {
                    "northeast": {
                        "lat": 42.1543111,
                        "lng": -6.189159200000001
                    },
                    "southwest": {
                        "lat": 29.8288392,
                        "lng": -31.4647999
                    }
                }
            },
            "partial_match": True,
            "place_id": "ChIJ1SZCvy0kMgsRQfBOHAlLuCo",
            "types": [
                "country",
                "political"
            ]
        },
        {
            "address_components": [
                {
                    "long_name": "Biarritz",
                    "short_name": "Biarritz",
                    "types": [
                        "locality",
                        "political"
                    ]
                },
                {
                    "long_name": "Pyr\u00e9n\u00e9es-Atlantiques",
                    "short_name": "Pyr\u00e9n\u00e9es-Atlantiques",
                    "types": [
                        "administrative_area_level_2",
                        "political"
                    ]
                },
                {
                    "long_name": "Nouvelle-Aquitaine",
                    "short_name": "Nouvelle-Aquitaine",
                    "types": [
                        "administrative_area_level_1",
                        "political"
                    ]
                },
                {
                    "long_name": "France",
                    "short_name": "FR",
                    "types": [
                        "country",
                        "political"
                    ]
                },
                {
                    "long_name": "64200",
                    "short_name": "64200",
                    "types": [
                        "postal_code"
                    ]
                }
            ],
            "formatted_address": "64200 Biarritz, France",
            "geometry": {
                "bounds": {
                    "northeast": {
                        "lat": 43.4945125,
                        "lng": -1.5343895
                    },
                    "southwest": {
                        "lat": 43.44740720000001,
                        "lng": -1.5771914
                    }
                },
                "location": {
                    "lat": 43.4831519,
                    "lng": -1.558626
                },
                "location_type": "APPROXIMATE",
                "viewport": {
                    "northeast": {
                        "lat": 43.4945125,
                        "lng": -1.5343895
                    },
                    "southwest": {
                        "lat": 43.44740720000001,
                        "lng": -1.5771914
                    }
                }
            },
            "partial_match": True,
            "place_id": "ChIJMx7zCisVUQ0RMKgTSBdlBgQ",
            "types": [
                "locality",
                "political"
            ]
        }
    ],
    "status": "OK"
}
