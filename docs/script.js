async function buscarDados() {
    const empresa = document.getElementById("empresa").value.trim();
    const resultadoDiv = document.getElementById("resultado");
    const loadingMsg = document.getElementById("loading");

    if (!empresa) {
        resultadoDiv.innerText = "Por favor, digite o nome da empresa.";
        return;
    }

    // Exibe a mensagem de carregamento e força o navegador a atualizar o DOM
    loadingMsg.style.display = "block";
    resultadoDiv.innerHTML = ""; // Limpa o resultado anterior
    await new Promise(resolve => setTimeout(resolve, 100)); // Pequeno delay para garantir atualização

    try {
        const resposta = await fetch("https://pesquisador.onrender.com/run-crew", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ company_name: empresa })
        });

        if (!resposta.ok) {
            throw new Error(`Erro na requisição: ${resposta.status}`);
        }

        const dados = await resposta.json();
        
        // Captura apenas o relatório final dentro do JSON
        const relatorioFinal = dados.data.raw || "Nenhum relatório encontrado.";

        // Atualiza a página com o relatório final formatado
        resultadoDiv.innerHTML = `<h2>Relatório Estratégico</h2><p>${relatorioFinal.replace(/\n/g, "<br>")}</p>`;
    } catch (erro) {
        resultadoDiv.innerText = "Erro ao buscar dados: " + erro.message;
    } finally {
        // Esconde a mensagem de carregamento quando a pesquisa termina
        loadingMsg.style.display = "none";
    }
}
