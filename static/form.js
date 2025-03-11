document.getElementById('togglepwd').addEventListener('click',function(){
    var pwd=document.getElementById('pwd');
    type=pwd.type==='password'?'text':'password';
    pwd.type=type;
    this.textContent=type==='password'?'Show password':'Hide password';
    this.style.backgroundColor=type==='password'?'green':'red';
})