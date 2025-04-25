
const chatBtn = document.getElementById('chatBtn');
const chatPopup = document.getElementById('chatPopup');
const closeBtn = document.getElementById('closeBtn');
const sendBtn = document.getElementById('sendBtn');
const userInput = document.getElementById('userInput');
const chatBody = document.getElementById('chatBody');

chatBtn.onclick = () => chatPopup.classList.add('open');
closeBtn.onclick = () => chatPopup.classList.remove('open');

sendBtn.onclick = () => {
    const msg = userInput.value.trim();
    if (msg) {
        const userDiv = document.createElement('div');
        userDiv.className = 'message user';
        userDiv.textContent = msg;
        chatBody.appendChild(userDiv);
        userInput.value = '';
        const aliciDiv = document.createElement('div');
        aliciDiv.className = 'message alici';
        aliciDiv.textContent = "Estou processando...";
        chatBody.appendChild(aliciDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
    }
};
