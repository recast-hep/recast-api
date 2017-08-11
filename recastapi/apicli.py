import yaml
import json
import recastapi.analysis.read
import recastapi.request.write
import click
import zipfile
import tempfile
import os

def addpoints_to_scan(scanid,req_format,parnames,points):
    point_requests = []
    basic_requests = []

    for i,p in enumerate(points):
        coordinates = p['coordinates']
        data = p['data']

        if os.path.isdir(data):
            _,archive = tempfile.mkstemp()
            with zipfile.ZipFile(archive,'w') as archivefile:
                for d,_,fl in os.walk(data):
                    for f in fl:
                        archivefile.write(os.path.join(d,f), arcname = os.path.relpath(os.path.join(d,f),data))
        elif zipfile.is_zipfile(data):
            archive = data
        else:
            print data
            print os.path.isdir(data)
            print zipfile.is_zipfile(data)
            raise click.ClickException('point data needs to be zipfiles or directory')

        pointdict = dict(zip(parnames,coordinates))
        pr = recastapi.request.write.point_request_with_coords(scanid,pointdict)
        point_requests += [{'point':pointdict,'id':pr['id']}]
        br = recastapi.request.write.basic_request_with_archive(pr['id'],archive,req_format)
        basic_requests += [{'point':pointdict,'id':br['id'], 'point_request': pr['id']}]
        click.secho('uploaded {}/{} requests'.format(i+1,len(points)))
    return point_requests, basic_requests


@click.command()
@click.argument('specfile')
@click.argument('outputfile')
def createscan(specfile,outputfile):
    spec = yaml.load(open(specfile))

    analysis_info = recastapi.analysis.read.analysis_by_pub_identifier(*spec['pubkey'].split('/'))
    if not analysis_info:
        raise click.ClickException('Analysis {} not known, import it first.'.format(spec['pubkey']))

    scanrequest = recastapi.request.write.scan_request(
        analysis_info['id'],
        spec['title'],
        spec['description'],
        spec['reason'],
        spec['additional_information']
    )


    parnames = spec['parameters']
    points = spec['points']

    prlist, brlist = addpoints_to_scan(scanrequest['id'],spec['request_format'],parnames,points)

    yaml.safe_dump({
            'scan_id': scanrequest['id'],
            'point_requests': prlist,
            'basic_requests': brlist
        },
        open(outputfile,'w'),
        default_flow_style = False
    )

@click.command()
@click.argument('specfile')
@click.argument('outputfile')
def addtoscan(specfile,outputfile):
    #existing_points = {tuple(x['value'] for x in p['point_coordinates']):p['id'] for p in  recastapi.request.read.point_request_of_scan(2) }
    pass

if __name__ == '__main__':
    createscan()