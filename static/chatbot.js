const chatbox = document.getElementById('chatbox');
const userInput = document.getElementsByName('user_message')[0];
// userInput.style.fontSize = 'larger';
userInput.setAttribute("size", "50");
chatbox.scrollTop = chatbox.scrollHeight;

const form = document.getElementById('user-input');

form.addEventListener('submit', function(event) {
    event.preventDefault();

    // Get the user's input message
    const userMessage = userInput.value;

    // Display the user's message in the chatbox
    displayMessage(userMessage.toUpperCase(), 'user');
    // displayMessage('-------------------- \n', 'empty-line');

    // Send the user's message to the chatbot API to get a response
    const requestOptions = {
        method: 'POST',
        headers: {
           'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'user_message=' + encodeURIComponent(userMessage)
    };
    fetch('/process_text', requestOptions)
        .then(response => response.json())
        .then(data => {
            // Display the chatbot's response in the chatbox
            const botMessage = data.bot_message;
            displayMessage(botMessage, 'bot');
    	    // displayMessage('-------------------- \n', 'empty-line');

	    // Reset the form element
            form.reset();
        });
});

function displayMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add(sender + '-message');
    messageElement.textContent = message;
    chatbox.appendChild(messageElement);
}

var copyButton = document.getElementById("copy-button");
    copyButton.addEventListener("click", function() {
        var chatbox = document.getElementById("chatbox");
        var range = document.createRange();
        range.selectNodeContents(chatbox);
        var selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
        document.execCommand("copy");
        alert("Chat messages copied to clipboard!");
    });