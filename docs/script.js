async function buscarDados() {
    try {
        const resposta = await fetch("https://pesquisador.onrender.com");
        if (!resposta.ok) {
            throw new Error(`Erro na requisição: ${resposta.status}`);
        }
        const dados = await resposta.json();
        document.getElementById("resultado").innerText = JSON.stringify(dados, null, 2);
    } catch (erro) {
        document.getElementById("resultado").innerText = "Erro ao buscar dados: " + erro.message;
    }
}
