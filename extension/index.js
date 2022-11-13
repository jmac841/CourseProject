const url = 'https://mquqv03qgi.execute-api.us-east-1.amazonaws.com/dev'

const submit = async () => {
    const textData = document.getElementById("inputTextArea").value
    const token = document.getElementById("accessToken").value
    const apiKey = document.getElementById("apiKey").value

    document.getElementById("loadingDiv").style.display = 'block';
    document.getElementById("form").style.visibility = 'hidden';
    document.getElementById("inputTextArea").value = '';

    let result = ''
    try {
        const rawResponse = await fetch(url, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': token,
                'x-api-key': apiKey
            },
            body: JSON.stringify({ data: textData })
        })
        
        const content = await rawResponse.json();
        let color = 'red'
        switch (content.statusCode) {
            case 200:
                result = `Sentiment is: ${content.body}`
                color = 'black'
                break
            case 400:
                result = 'Bad Request'
                break
            case 401:
                result = 'Unauthorized'
                break
            default:
                result = 'An unexpected error has occured'
                break
        }

        document.getElementById('result').innerText = result
        document.getElementById('result').style.color = color

    } catch (err) {
        console.error(err.message)
    }

    document.getElementById("form").style.visibility = 'visible';
    document.getElementById("loadingDiv").style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function (event) {
    document.getElementById("submitButton").addEventListener("click", submit);
    document.getElementById("loadingDiv").style.display = 'none';
    document.getElementById("loadingDiv").style.visibility = 'hidden';
});
