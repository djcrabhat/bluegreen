import argparse
import boto3
import logging

logger = logging.getLogger('bluegreen')

parser = argparse.ArgumentParser(description='For blue-greening a deployment')
parser.add_argument('command')
parser.add_argument('config')


class BotoHelper(object):
    def __init__(self):
        pass
    def get_stacks(self,region="us-east-1"):
        return []
    def get_dns_entries(self):
        client = boto3.client('route53')
        return []

class BlueGreen(object):
    def __init__(self, args=None):
        if args is None:
            self.args=self.parse_args()
        else:
            self.args=args

    @staticmethod
    def parse_args():
        args=parser.parse_args()
        return args

    def info(self):
        ret=dict(info="current info!")
        logger.debug(ret)
        return ret

    def stage(self):
        ret = dict(info="staging!")
        logger.debug(ret)
        return ret

    def deploy(self):
        ret=dict(deploy="do it!")
        logger.debug(ret)
        return ret

    def main(self, command=None):
        if command is None:
            command=self.args.command
        if command is None:
            raise AttributeError("must set a command")

        if command == 'info':
            self.info()
        elif command == 'stage':
            self.stage()
        elif command == 'deploy':
            self.deploy()











