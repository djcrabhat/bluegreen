import argparse
import boto3
import sys
import logging

logger = logging.getLogger('bluegreen')

parser = argparse.ArgumentParser(description='For blue-greening a deployment')
parser.add_argument('command')
parser.add_argument('--zone-id')
parser.add_argument('target', nargs="?", default='')
parser.add_argument('backend', nargs="?", default='')

class BotoHelper(object):
    def __init__(self):
        self.client = boto3.client('route53')
        pass
    def get_stacks(self,region="us-east-1"):
        return []
    def get_cname_info(self, zone_id, frontend):
        client = boto3.client('route53')
        response = client.list_resource_record_sets(HostedZoneId=zone_id, StartRecordName='*',StartRecordType='CNAME')
        cname_ret=dict()
        for set in response['ResourceRecordSets']:
            if set['Type']=='CNAME':
                records=set['ResourceRecords']
                cname_ret[set['Name']]=[r['Value'] for r in records]

        return cname_ret



    def update_dns(self, zone_id, frontend, backend):
        client = boto3.client('route53')
        batch=self._create_update_cname(frontend, backend)
        response = client.change_resource_record_sets(HostedZoneId=zone_id,ChangeBatch=batch)
        return response
    def _create_update_cname(self, hostname, backend_dns):
        obj={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet':{
                        'Name': hostname,
                        'Type': 'CNAME',
                        'TTL': 60,
                        'ResourceRecords':[
                            {"Value":backend_dns}
                        ]
                    }
                }]
        }
        return obj

class BlueGreen(object):
    def __init__(self, args=None):
        if args is None:
            self.args=self.parse_args()
        else:
            self.args=args

        self.boto_helper=BotoHelper()

    def get_matching_frontend(self, zone_id, frontend):
        cnames=self.boto_helper.get_cname_info(zone_id,frontend)
        matched_site=None
        if frontend in cnames:
            matched_site=cnames[frontend]
        return dict(cnames=cnames, matched_site=matched_site)

    @staticmethod
    def parse_args():
        args=parser.parse_args()
        return args

    def info(self, frontend):
        zone_id=self.args.zone_id
        if not frontend.endswith('.'):
            frontend=frontend+"."
        ret=self.get_matching_frontend(zone_id,frontend)


        logger.debug(ret)
        return ret

    def stage(self, frontend,backend):
        zone_id=self.args.zone_id
        if not frontend.endswith('.'):
            frontend=frontend+"."
        ret=self.boto_helper.update_dns(zone_id, frontend, backend)
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
            frontend=self.args.target
            self.info(frontend)
        elif command == 'stage':
            frontend=self.args.target
            backend=self.args.backend
            self.stage(frontend,backend)
        elif command == 'deploy':
            self.deploy()



if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.info("starting...")
    bg=BlueGreen()
    bg.main()









