async function buscarDados() {
    const empresa = document.getElementById("empresa").value.trim();
    
    if (!empresa) {
        document.getElementById("resultado").innerText = "Por favor, digite o nome da empresa.";
        return;
    }

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
        document.getElementById("resultado").innerHTML = `<h2>Relatório Estratégico</h2><p>${relatorioFinal.replace(/\n/g, "<br>")}</p>`;
    } catch (erro) {
        document.getElementById("resultado").innerText = "Erro ao buscar dados: " + erro.message;
    }
}
