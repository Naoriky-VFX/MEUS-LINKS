
/* proteção do site de links: conteúdo escondido até o login */
(function () {
  var CHAVE = "nk_auth";
  var ALVO = "7db12d29549cce44f9559fb081be287ba66388f58060bbb5b39fb50a1b1cc826";
  var ok = sessionStorage.getItem(CHAVE) === "1";

  // esconde tudo antes de qualquer renderização
  var esconde = document.createElement("style");
  esconde.textContent = "html.nk-lock body{visibility:hidden}";
  document.head.appendChild(esconde);
  if (!ok) document.documentElement.classList.add("nk-lock");

  function liberar() {
    document.documentElement.classList.remove("nk-lock");
    var o = document.getElementById("nk-login");
    if (o) o.remove();
    document.documentElement.style.overflow = "";
  }

  if (ok) { liberar(); return; }

  async function hash(txt) {
    var buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(txt));
    return Array.from(new Uint8Array(buf)).map(function (b) {
      return b.toString(16).padStart(2, "0");
    }).join("");
  }

  function montar() {
    var css = document.createElement("style");
    css.textContent = `
    #nk-login{position:fixed;inset:0;z-index:99999;visibility:visible!important;background:#0b0710;display:flex;
      align-items:center;justify-content:center;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
    #nk-login .box{width:min(340px,90vw);background:#160f22;border:1px solid #3a2f4e;
      border-radius:16px;padding:26px 22px;box-shadow:0 20px 60px rgba(0,0,0,.6)}
    #nk-login h1{margin:0 0 4px;font-size:1.15rem;color:#f4f0ff}
    #nk-login p{margin:0 0 18px;font-size:.82rem;color:#9a8bb5}
    #nk-login input{width:100%;margin-bottom:10px;padding:11px 12px;border-radius:10px;
      border:1px solid #3a2f4e;background:#0e0916;color:#f4f0ff;font-size:.9rem;outline:none}
    #nk-login input:focus{border-color:#a855f7}
    #nk-login button{width:100%;margin-top:6px;padding:11px;border:0;border-radius:10px;
      background:#a855f7;color:#fff;font-weight:700;font-size:.9rem;cursor:pointer}
    #nk-login .erro{margin-top:10px;font-size:.78rem;color:#f87171;min-height:16px}`;
    document.head.appendChild(css);

    var box = document.createElement("div");
    box.id = "nk-login";
    box.innerHTML = `
      <div class="box">
        <h1>Meus links</h1>
        <p>Acesso restrito</p>
        <input id="nk-user" placeholder="usuario" autocomplete="username">
        <input id="nk-pass" type="password" placeholder="senha" autocomplete="current-password">
        <button id="nk-go">Entrar</button>
        <div class="erro" id="nk-erro"></div>
      </div>`;
    document.body.appendChild(box);

    var user = box.querySelector("#nk-user");
    var pass = box.querySelector("#nk-pass");
    var erro = box.querySelector("#nk-erro");

    async function tentar() {
      var calculado = await hash(user.value.trim().toLowerCase() + ":" + pass.value);
      if (calculado === ALVO) {
        sessionStorage.setItem(CHAVE, "1");
        liberar();
      } else {
        erro.textContent = "Usuario ou senha incorretos.";
        pass.value = "";
        pass.focus();
      }
    }

    box.querySelector("#nk-go").addEventListener("click", tentar);
    box.addEventListener("keydown", function (e) { if (e.key === "Enter") tentar(); });
    user.focus();
  }

  if (document.body) montar();
  else document.addEventListener("DOMContentLoaded", montar);
})();
