import datetime

from schema import Schema, Optional

model_config = Schema({
    'run_info': {
        'information_horizon': datetime.date,
        'run_mode': str,
    },

    'run_param': {
        'random_seed': int,
        'use_cross_validation': bool,
        'nb_folds': int,
    },

    'demand_forecast': {
        'model': dict,
        'features': dict,
        'range_week_sales': int,
        'nan_strategy': str,
        "granularity": dict,
        "target": str,
        'training_context': {
            Optional('location'): dict,
            Optional('products'): dict,
            'time': {
                'granularity': str,
                'time_range': int},
            'min_sales': int,
        },
        'prediction_context': {
            Optional('location'): dict,
            Optional('products'): dict,
            'time': {
                'granularity': str,
                'time_range': int,
            }

        },
    }
})


infra_config = Schema({
    Optional('data_warehouse'): {
        Optional('connect'): bool,
    },
    'db': {
        'host': str,
        'port': int,
        'user': str,
        'password': str,
        'database': str,
    }
})

test_config = Schema({
    'name': str,
    'other': int,
})
