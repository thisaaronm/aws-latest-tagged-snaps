#!/usr/bin/env python3

import boto3
import sys


def get_snaps():
    """
    Gets all snapshots with specified tag.
    ** Make sure to change the tag-key value. **
    """
    client   = boto3.client('ec2')
    response = client.describe_snapshots(
        Filters=[
            {
                'Name': 'tag-key',
                'Values': [
                    'tag-key-value', ## CHANGE ME
                ]
            },
        ],
        OwnerIds=[
            'self',
        ],
    )
    return response['Snapshots']


def get_vols(snaps):
    set_vols = set()
    for snap in snaps:
        try:
            set_vols.add(snap['VolumeId'])
        except Exception as e:
            pass
    return set_vols


def get_latest(vols, snaps):
    for vol in vols:
        vol_snaps = []
        for snap in snaps:
            if snap['VolumeId'] == vol:
                vol_snaps.append(snap)
                vol_snaps.sort(key=lambda date:date['StartTime'], reverse=True)
        v_snap = vol_snaps[0]
        print(f"{v_snap['SnapshotId']} > {v_snap['Tags'][0]['Value']} > {v_snap['VolumeId']} > {v_snap['StartTime']}")


def main():
    ec2 = boto3.resource('ec2')

    snapshots = get_snaps()
    volumes   = get_vols(snapshots)

    get_latest(volumes, snapshots)

if __name__ == "__main__":
    if sys.version[:3] != '3.6':
        print("Must be running Python 3.6.\nExiting...\n")
        sys.exit(1)
    try:
        main()
    except KeyboardInterrupt as eki:
        print("\n\nReceived CTRL+C.\nExiting...\n")
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)
