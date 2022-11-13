const { DynamoDBClient, GetItemCommand } = require("@aws-sdk/client-dynamodb");

exports.handler = async (event, context, callback) => {
    const token = event.authorizationToken

    const client = new DynamoDBClient({
        region: 'us-east-1'
    });
    
    const response = await client.send(new GetItemCommand({
        TableName: 'APIData',
        Key: {
          token: {
            S:'accessToken'
          }
        }
    }));
        
    if(token === response.Item.value.S) {
        callback(null, {
        "principalId": "user",
        "policyDocument": {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Action": "execute-api:Invoke",
              "Effect": "Allow",
              "Resource": "arn:aws:execute-api:*"
            }
          ]
        }
      })
    } else {
      callback("Unauthorized");
    }
};
