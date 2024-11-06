function authenticate(event) {
    event.preventDefault(); // Prevent form submission
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Simple hardcoded credentials for demonstration
    const validUsername = 'sriram';
    const validPassword = 'mypass';

    // Check credentials
    if (username === validUsername && password === validPassword) {
        window.location.href = 'file_share.html'; // Redirect to the file sharing page
    } else {
        alert('Invalid username or password!');
    }
}