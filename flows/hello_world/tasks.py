"""Tasks for the Hello World workflow."""

from datetime import datetime
import random

from garcon import task

from flows.hello_world import config


@task.decorate(timeout=60 * 3)
def bootstrap(activity, context_date, reload):
    """Bootstrap initial configuration."""
    date_obj = datetime.strptime(context_date, '%Y-%m-%d') if context_date else datetime.today()
    run_date = date_obj.strftime('%Y-%m-%d')

    print('Boostrapping initial configuration for {}...'.format(config.FEED_NAME + '_' + run_date))

    if reload == 'True':
        print('Delete status for feed: {} {} '.format(config.FEED_NAME, run_date))
        config.redis_client.delete(config.FEED_NAME + run_date)

    else:
        overall_status = config.redis_client.get(config.FEED_NAME + run_date)
        if overall_status == 'SUCCESS':
            result = {'stop': 'Everything is done for {}!'.format(run_date)}
            print(result)
            return result

    return {
        'date': run_date,
        'feed_name': config.FEED_NAME
    }


@task.decorate(timeout=60 * 5)
def say_hello(activity, feed_name, date):
    """Say Hello."""
    # mock some useful activity, e.g. an attempt to download daily files
    hello = random.choice(['Hello!', 'Hello is not available yet, UHODI!', 'ERROR'])

    if hello == 'Hello!':
        print('Hello world!')
        status_to_set = 'SUCCESS'
    elif hello == 'ERROR':
        print('say_hello task failed!')
        status_to_set = 'ERROR'
    else:
        print('Hello is not available yet, UHODI!')
        status_to_set = 'NOT_AVAILABLE'

    return {'status_to_set': status_to_set}


@task.decorate(timeout=60 * 5)
def set_overall_status(activity, feed_name, date, status_to_set):
    """Set overall flow execution status."""
    config.redis_client.set(feed_name + date, status_to_set)
    print('Status {} is set, exit...'.format(status_to_set))
