const url = 'http://localhost:5000/'

const submit = async () => {
    const textData = document.getElementById("inputTextArea").value

    document.getElementById("loadingDiv").style.display = 'block';
    document.getElementById("form").style.visibility = 'hidden';

    let result = ''
    let color = ''
    try {
        const rawResponse = await fetch(url, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: textData,
                model: document.querySelector('input[name="model"]:checked').value
            })
        })

        const content = await rawResponse.json();
        if (statusCode === 200) {
            result = `Sentiment is: ${content.body}`
            color = 'black'
        } else {
            result = 'An unexpected error has occured'
            color = 'red'
        }

        document.getElementById('result').innerText = result
        document.getElementById('result').style.color = color

    } catch (err) {
        console.error(err.message)
    }

    document.getElementById("form").style.visibility = 'visible';
    document.getElementById("loadingDiv").style.display = 'none';
}

document.addEventListener('DOMContentLoaded', async function (event) {
    document.getElementById("submitButton").addEventListener("click", submit);
    document.getElementById("loadingDiv").style.display = 'none';
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    let result;
    try {
        [{ result }] = await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            function: () => getSelection().toString(),
        });
        document.getElementById("inputTextArea").value = result
    } catch (e) {
        return;
    }
    document.getElementById('submitButton').focus()
});
