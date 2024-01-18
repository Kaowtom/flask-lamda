from flask import Flask, jsonify, make_response
import boto3
app = Flask(__name__)


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('peopleGSI-2')

# Create
@app.route("/create/<id>/<name>/<career>")
def create(id,name , career):
    response = table.put_item(
                Item={
                'id': id,
                'name': name,
                'career': career}
        )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        # print('response successful')
        return response
        # return jsonify(message=f"Creating successful for {id} {name} {career}")
    else:
        return jsonify(message=f"Creating unsuccessful for {id} {name} {career}")

# Read
@app.route("/view")
def view():
    response = table.scan()
    data = response['Items']
    print(data)
    return jsonify(message=data)

# Update
@app.route("/update/<id>/<new_name>/<new_career>")
def update(id, new_name, new_career):
    response = table.update_item(
        Key={
            'id': id
        },
        UpdateExpression='SET #name = :new_name, #career = :new_career',
        ExpressionAttributeNames={
            '#name': 'name',
            '#career': 'career'
        },
        ExpressionAttributeValues={
            ':new_name': new_name,
            ':new_career': new_career
        },
        ReturnValues='UPDATED_NEW'
    )

    updated_item = response.get('Attributes', {})

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return jsonify(message=f"Update successful for {id}. Updated Item: {updated_item}")
    else:
        return jsonify(message=f"Update unsuccessful for {id}")

# delete
@app.route("/delete/<id>")
def delete(id):
    response = table.delete_item(
        Key={'id': str(id)}
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return jsonify(message=f"Delete successful for {id}.")
    else:
        return jsonify(message=f"Delete unsuccessful for {id}")

@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)

# if __name__ == '__main__':
#     app.run(debug=True)

# Lambda handler function
def lambda_handler(event, context):
    app.run(port=5000)
