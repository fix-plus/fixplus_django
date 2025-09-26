from config.env import env


AZ_IRANIAN_BANK_GATEWAYS = {
    'GATEWAYS': {
        'ZARINPAL': {
            'MERCHANT_CODE': env('ZARINPAL_MERCHANT_CODE'),
            'SANDBOX': 0,  # Set to 0 for production
        },
    },
    'DEFAULT': 'ZARINPAL',
    'CURRENCY': 'IRT',  # Iranian Rial, matches your final_phase_one_cost
    'TRACKING_CODE_QUERY_PARAM': 'tracking_code',
    'TRACKING_CODE_LENGTH': 16,
    'SETTING_VALUE_READER_CLASS': 'azbankgateways.readers.DefaultReader',
    'BANK_PRIORITIES': ['ZARINPAL'],
    'IS_SAFE_GET_GATEWAY_PAYMENT': True,
}