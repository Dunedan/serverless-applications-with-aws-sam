import boto3
import os
import svgwrite
from io import StringIO

client = boto3.client('dynamodb')


def generate_counter_image(counter_value):
    """Generate an SVG page view counter image with the given value."""
    in_memory_svg = StringIO()
    drawing = svgwrite.Drawing(in_memory_svg, profile='full')
    drawing.add(drawing.rect(size=(30, 20), fill='#555'))
    drawing.add(drawing.rect(insert=(30, 0),size=(50, 20), fill='#4c1'))
    g = drawing.g(fill='#fff',
              style="font-family:DejaVu Sans,Verdana,Geneva,sans-serif;font-size:16;",
              text_anchor="middle")
    g.add(drawing.text('hits', insert=(15, 14)))
    g.add(drawing.text(counter_value, insert=(54, 14)))
    drawing.add(g)
    drawing.write(in_memory_svg)
    in_memory_svg.seek(0)
    return in_memory_svg.read()


def handler(event, context):
    counter_id = event['pathParameters']['id']

    response = client.update_item(TableName=os.environ['DYNAMODB_TABLE'],
                                  Key={'id': {'S': counter_id}},
                                  AttributeUpdates={'number': {
                                      'Action': 'ADD',
                                      'Value': {'N': '1'}}
                                  },
                                  ReturnValues='UPDATED_NEW')

    counter_value = int(response['Attributes']['number']['N'])

    return {
        "headers": {"content-type": "image/svg+xml"},
        "body": generate_counter_image(counter_value)
    }
