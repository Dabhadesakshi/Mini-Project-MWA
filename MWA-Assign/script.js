let isLogin = false;

function toggleForm() {
  const form = document.getElementById('auth-form');
  const title = document.getElementById('form-title');
  const emailInput = document.getElementById('email');
  const button = form.querySelector('button');
  const toggleText = document.getElementById('toggle-text');

  isLogin = !isLogin;

  if (isLogin) {
    title.innerText = 'Login';
    emailInput.style.display = 'none';
    button.innerText = 'Login';
    toggleText.innerHTML = `Don't have an account? <span onclick="toggleForm()">Register</span>`;
    form.action = "login.php";
    console.log("Form switched to Login, action set to:", form.action);
  } else {
    title.innerText = 'Register';
    emailInput.style.display = 'block';
    button.innerText = 'Register';
    toggleText.innerHTML = `Already have an account? <span onclick="toggleForm()">Login</span>`;
    form.action = "register.php";
    console.log("Form switched to Register, action set to:", form.action);
  }
}
