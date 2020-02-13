"""CLI functions to run decider, worker and exec processes."""

import argparse
import importlib
import json
import time

import boto.swf.layer2 as swf
from garcon import activity
from garcon import decider


def execute_flow(flow, context, **kwargs):
    """Launch the workflow execution.

    Args:
        flow (module): Garcon flow module.
        context (str): Initial context parsed from JSON.

    """
    start_kwargs = dict(
        workflow_id=flow.workflow_id(json.loads(context)),
        input=context)

    if hasattr(flow, 'timeout'):
        start_kwargs.update(execution_start_to_close_timeout=str(flow.timeout))

    execution = swf.WorkflowType(
        name=flow.name,
        domain=flow.domain,
        version=flow.version,
        task_list=flow.name).start(**start_kwargs)

    return execution


def run_decider(flow, **kwargs):
    """Launch the SWF decider process.

    Args:
        flow (module): Garcon flow module.

    """
    worker = decider.DeciderWorker(flow)
    while True:
        worker.run()
        time.sleep(1)


def run_activity_worker(flow, **kwargs):
    """Launch the activity worker process.

    Args:
        flow (module): Garcon flow module.

    """
    worker = activity.ActivityWorker(flow)
    worker.run()


def garcon(*args):
    """Entry point for the Garcon command line integration.

    Args:
        args (tuple): Args for the flow.

    """
    _COMMANDS = {
        'exec': execute_flow,
        'decider': run_decider,
        'worker': run_activity_worker
    }

    parser = argparse.ArgumentParser(description='Garcon command line util')
    parser.add_argument('cmd', choices=_COMMANDS.keys(),
                        help='garcon command')
    parser.add_argument('flow', help='name of the flow')
    parser.add_argument('-c', '--context',
                        help='initial context [json]')

    args = parser.parse_args(args) if args else parser.parse_args()

    # import the flow module
    flow = importlib.import_module('.{}.flow'.format(args.flow), 'flows')
    flow_class = getattr(flow, 'Flow', None)
    flow = flow_class()

    # execute command
    args.context = args.context or '{}'
    _COMMANDS[args.cmd](flow=flow, context=args.context)


if __name__ == '__main__':
    garcon()
