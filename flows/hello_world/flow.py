"""Hello World ETL."""

import datetime

from garcon import activity
from garcon import runner

from flows.hello_world import config
from flows.hello_world import tasks


class Flow:
    """Class representing the workflow."""

    def __init__(self):
        """Initialize flow object."""
        self.name = config.FEED_NAME
        self.version = '2.0'
        self.domain = 'dev_uvarov'
        self.timeout = 60 * 3

        self.create = activity.create(
            self.domain, self.name, version=self.version,
            on_exception=self.on_exception)

    def decider(self, schedule):
        """Activity decider.

        Args:
            schedule (callable): The scheduler method.

        """
        bootstrap = schedule(
            'bootstrap',
            self.bootstrap)

        # Stop flow if everything is done for today
        if bootstrap.result.get('bootstrap.stop'):
            return bootstrap.result.get('bootstrap.stop')

        say_hello = schedule(
            'say_hello',
            self.say_hello,
            requires=[bootstrap])

        schedule(
            'set_overall_status',
            self.set_overall_status,
            requires=[say_hello])

    @property
    def bootstrap(self):
        """Populate stats table with the fresh queries."""
        return self.create(
            name='bootstrap',
            tasks=runner.Sync(
                tasks.bootstrap.fill(
                    namespace='bootstrap',
                    context_date='context_date',
                    reload='reload')))

    @property
    def say_hello(self):
        """Say hello to everyone."""
        return self.create(
            name='say_hello',
            retry=2,
            tasks=runner.Sync(
                tasks.say_hello.fill(namespace='say_hello')))

    @property
    def set_overall_status(self):
        """Set an overall status for a day."""
        return self.create(
            name='set_overall_status',
            tasks=runner.Sync(
                tasks.set_overall_status.fill(
                    namespace='set_overall_status',
                    feed_name='bootstrap.feed_name',
                    date='bootstrap.date',
                    status_to_set='say_hello.status_to_set')))

    def workflow_id(self, initial_context):
        """Generate workflow id.

        Assumes a unique workflow is defined by it's context date and
        defaults to today's date. If that is not the case this method
        should be overridden.

        Args:
            initial_context (dict): The initial context for the flow.

        Returns:
            str: A unique identifier for a workflow being executed
                In the forms of '<self.flow_name>-YYYY-MM-DD', where
                YYYY-MM-DD is the context date or, if none passed the
                current date.
        """
        if 'context_date' not in initial_context:
            date = datetime.datetime.today().strftime('%Y-%m-%d')
        else:
            date = initial_context['context_date']

        return '{flow_name}-{date}'.format(
            flow_name=self.name,
            date=date)

    def on_exception(self, actor, exception):
        """Capture an exception that has occurred in the application.

        Args:
            actor (ActivityWorker, DeciderWorker): The actor that has received
                the exception.
            exception (Exception): The exception to capture.

        """
        raise Exception
