async function buscarDados() {
    const empresa = document.getElementById("empresa").value.trim();
    const resultadoDiv = document.getElementById("resultado");

    if (!empresa) {
        resultadoDiv.innerHTML = `<p style="color: red;">⚠️ Por favor, digite o nome da empresa.</p>`;
        return;
    }

    // Exibir mensagem informativa e limpar resultado anterior
    resultadoDiv.innerHTML = `<p style="color: blue;">🔎 Buscando informações sobre "${empresa}", aguarde...</p>`;

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
        const relatorioMarkdown = dados.data.raw || "**Nenhum relatório encontrado.**";

        // Converte o Markdown para HTML
        const relatorioHTML = marked.parse(relatorioMarkdown);

        // Exibe o relatório formatado
        resultadoDiv.innerHTML = `<h2>📋 Relatório Estratégico</h2>${relatorioHTML}`;
    } catch (erro) {
        resultadoDiv.innerHTML = `<p style="color: red;">❌ Erro ao buscar dados: ${erro.message}</p>`;
    }
}
