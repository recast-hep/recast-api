import yaml
import json
import recastapi.request.write
import click
import zipfile
import tempfile
import os

@click.command()
@click.argument('specfile')
def createscan(specfile):
    spec = yaml.load(open(specfile))
    scanrequest = recastapi.request.write.scan_request(
        spec['analysis_id'],
        spec['title'],
        spec['description'],
        spec['reason'],
        spec['additional_information']
    )

    parnames = spec['parameters']
    points = spec['points']

    point_requests = []
    basic_requests = []
    for p in points:
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
        pr = recastapi.request.write.point_request_with_coords(scanrequest['id'],pointdict)
        point_requests += [{'point':pointdict,'id':pr['id']}]
        br = recastapi.request.write.basic_request_with_archive(pr['id'],archive)
        basic_requests += [{'point':pointdict,'id':br['id']}]

    click.echo(yaml.safe_dump({
            'scan_id': scanrequest['id'],
            'point_requests': point_requests,
            'basic_requests': basic_requests
        },
        default_flow_style = False
    ))

if __name__ == '__main__':
    createscan()